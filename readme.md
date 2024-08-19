# ClearConsensus API Upload Instructions

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Script Configuration](#script-configuration)
3. [Prepare Files for Upload](#prepare-files-for-upload)
4. [Run the Upload Script](#run-the-upload-script)
5. [Post-Upload Steps](#post-upload-steps)
6. [Troubleshooting](#troubleshooting)

## Initial Setup

1. Log into your account on the Cuneiform for Valuation Risk platform at [https://onboarding.clearconsensus.io/](https://onboarding.clearconsensus.io/)
2. Click on _Account_ in the bottom left of the screen.
3. Click on the grey user icon in the small pop up that appears. This should lead you to a page with API Keys.
4. Click on _Create API Key_.
5. Select the `read_write` option for all relevant asset classes, choose a name for the key pair and click _Create_.
6. Copy both the _Access Key_ and the _Access Secret_. You'll need these for the script configuration.

Note: If you're using a different environment, replace the URL with the appropriate one provided by your Cuneiform administrator.

## Script Configuration

1. Ensure you have Python installed on your system. This script is compatible with Python 3.6+.
2. Install the required Python packages by running:
   ```bash
   pip install requests
   ```
3. Download the `submission_upload.py` script to your local machine.
4. Open the `submission_upload.py` script in a text editor.
5. Locate the `if __name__ == "__main__":` section at the bottom of the script.
6. Update the following parameters with your API credentials and desired settings:
   ```python
   submission_upload(
       api_key="YOUR_API_KEY_HERE",
       api_secret="YOUR_API_SECRET_HERE",
       mode="onboarding",  # or the appropriate mode for your use case
       description="Your upload description here"
   )
   ```
7. Save the changes to the script.

## Prepare Files for Upload

1. Create an `Input` folder in the same directory as the `submission_upload.py` script if it doesn't already exist.
2. Ensure your CSV files are named correctly. The expected format is:
   ```
   AssetName_SubAsset_Service_Client_YYYY-mm-dd_SnapTime.csv
   ```
   For example:
   ```
   Caps & Floors
   Rates_Caps & Floors_Non Linear_Zbank1_2024-07-31_London 4 PM.csv
   Rates_Caps & Floors_Non Linear_Zbank1_2024-07-31_New York 4 PM.csv

   Swaptions
   Rates_Swaptions_Non Linear_Zbank1_2024-07-31_London 4 PM.csv
   Rates_Swaptions_Non Linear_Zbank1_2024-07-31_New York 4 PM.csv

   FXO
   Foreign Exchange_Options_Vanilla_Zbank1_2024-07-31_New York 4 PM.csv
   Foreign Exchange_Options_Vanilla_Zbank1_2024-07-31_London 4 PM.csv

   FXF
   Foreign Exchange_Forwards_Vanilla_Zbank1_2024-07-31_New York 4 PM.csv
   Foreign Exchange_Forwards_Vanilla_Zbank1_2024-07-31_London 4 PM.csv

   ```
3. Add all CSV files you want to upload into the `Input` folder.

## Run the Upload Script

1. Open a terminal or command prompt.
2. Navigate to the directory containing the `submission_upload.py` script.
3. Run the Python script:
   ```bash
   python submission_upload.py
   ```
4. The script will process each CSV file in the `Input` folder, attempt to upload it, and move successfully uploaded files to an `Uploaded` folder.

## Post-Upload Steps

1. Check the console output for any error messages or upload status for each file.
2. Verify that the files have been moved from the `Input` folder to the `Uploaded` folder.
3. Log into the ClearConsensus platform and check the submission status for data quality issues (optional).

## Troubleshooting

If you encounter any errors:

- **API Key Issues**: 
  - Ensure your API key and secret are correct.
  - Check that your API key has the necessary permissions (read_write access).
  - Verify that you're using the correct `mode` for your API endpoint.

- **File Issues**:
  - Confirm that your CSV files are named correctly according to the specified format.
  - Check that the CSV files contain the expected data and are not corrupted.

- **Network Issues**:
  - Verify your internet connection.
  - Check if there are any firewalls or proxy servers blocking the connection to the Cuneiform for Valuation Risk API.

- **Script Errors**:
  - Ensure you have the latest version of the script.
  - Check that you've installed all required Python packages (`requests`).

- **Unexpected Responses**:
  - Review any error messages in the console output for specific issues.
  - If you see "Access denied: permissions validation failed", double-check your API key permissions and the asset classes you're trying to upload.

If problems persist after checking these items, please contact Cuneiform for Valuation Risk support with the following information:
1. The exact error message from the console output.
2. The name of the file(s) you were trying to upload.
3. The API key used (do NOT share the secret).
4. Any relevant screenshots of the Cuneiform for Valuation Risk platform showing the issue.

**Remember: Always keep your API credentials secure and never share them publicly or with unauthorized individuals.**
