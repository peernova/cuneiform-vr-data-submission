import os
import json
import hmac
import hashlib
from typing import List, Dict, Any
from datetime import datetime
import requests



def create_token(api_key: str, api_secret: str) -> str:
    timestamp = int(datetime.now().timestamp())
    signature_data = f"{timestamp}:{api_key}"
    signature_hmac = hmac.new(api_secret.encode(), signature_data.encode(), hashlib.sha256).hexdigest()
    return f"{timestamp}.{signature_hmac}"

def get_api_base_url(mode: str) -> str:
    urls = {
        "prod": "clearconsensus.io",
        "onboarding": "onboarding.clearconsensus.io",
    }
    return f"https://{urls.get(mode, 'clearconsensus.io')}/apigw/api/v1/"

class Asset:
    def __init__(self, name: str, sub_asset: str, service: str, snap_time: str, date: str):
        self.name = name
        self.sub_asset = sub_asset
        self.service = service
        self.snap_time = snap_time
        self.date = date

    def dict(self):
        return {
            "name": self.name,
            "sub_asset": self.sub_asset,
            "service": self.service,
            "snap_time": self.snap_time,
            "date": self.date
        }

class Upload:
    def __init__(self, filepath: str, asset: Asset, client: str, api_url: str):
        self.filepath = filepath
        self.asset = asset
        self.client = client
        self.api_url = api_url
        self.upload_link = None

    def get_headers(self, api_key: str, api_secret: str):
        return {
            "x-api-key": api_key,
            "x-api-token": create_token(api_key, api_secret),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def generate_upload_link(self, api_key: str, api_secret: str, description: str):
        payload = {
            "client": self.client,
            "file_name": os.path.basename(self.filepath),
            "mode": "submission",
            "asset": self.asset.dict(),
            "description": description,
        }

        try:
            print(f"Sending request to: {self.api_url}upload/data")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            headers = self.get_headers(api_key, api_secret)
            print(f"Headers: {json.dumps(headers, indent=2)}")
            
            response = requests.post(
                f"{self.api_url}upload/data",
                json=payload,
                headers=headers
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
            
            
            response.raise_for_status()
            data = response.json()
            
            if data and "s3Url" in data:
                self.upload_link = data["s3Url"]
                self.upload_file()
                print(f"{self.filepath} uploaded!")
            else:
                print(f"Unexpected response structure: {json.dumps(data, indent=2)}")
                raise ValueError("Invalid response from server: missing s3Url")
        except requests.exceptions.RequestException as error:
            print(f"Failed to generate upload link for {self.filepath}: {str(error)}")
            if hasattr(error, 'response') and error.response:
                print("Error response:", json.dumps(error.response.json(), indent=2))
                print("Error status:", error.response.status_code)
                print("Error headers:", error.response.headers)
            raise
        except json.JSONDecodeError:
            print("Failed to parse response as JSON")
            print(f"Raw response: {response.text}")
            raise

    def upload_file(self):
        try:
            with open(self.filepath, "rb") as file:
                response = requests.put(self.upload_link, data=file, headers={"Content-Type": "text/plain"})
                response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"Failed to upload file {self.filepath}: {str(error)}")
            raise

    def move_file(self, output_folder: str):
        source_file = self.filepath
        target_file = os.path.join(output_folder, os.path.basename(self.filepath))
        
        try:
            os.makedirs(output_folder, exist_ok=True)
            os.rename(source_file, target_file)
            print(f"File moved successfully from {source_file} to {target_file}")
        except IOError as error:
            print(f"Error moving file: {str(error)}")
            raise

def get_list_of_files(directory: str, extension: str) -> List[str]:
    print(f"Reading files from: {directory}")
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(f".{extension}")
    ]

def submission_upload(api_key: str, api_secret: str, mode: str, description: str):
    if not api_key or not api_secret:
        raise ValueError(f"{mode} API key and secret are required")

    api_url = get_api_base_url(mode)
    Input_folder = os.path.join(os.path.dirname(__file__), "Input")
    output_folder = os.path.join(os.path.dirname(__file__), "Uploaded")

    try:
        print("Waiting for file system ...")
        

        files = get_list_of_files(Input_folder, "csv")

        for filepath in files:
            try:
                filename = os.path.basename(filepath)
                print(f"Processing file: {filename}")

                payload_file_name = os.path.splitext(filename)[0]
                asset_name, sub_asset, service, client, snap_date, snap_time = payload_file_name.split("_")

                asset = Asset(
                    name=asset_name,
                    sub_asset=sub_asset,
                    service=service,
                    snap_time=snap_time,
                    date=snap_date
                )

                upload = Upload(filepath, asset, client, api_url)
                upload.generate_upload_link(api_key, api_secret, description)
                upload.move_file(output_folder)

                print(f"{filename} uploaded!")
            except Exception as error:
                print(f"Error processing file {filepath}: {str(error)}")
                continue


    except Exception as error:
        print("Error in submission upload:", str(error))
        raise

if __name__ == "__main__":
    # Example usage
    submission_upload(
        api_key="_API_KEY_HERE_",
        api_secret="_API_SECRET_HERE_",
        mode="onboarding",
        description="Sample submission upload"
    )