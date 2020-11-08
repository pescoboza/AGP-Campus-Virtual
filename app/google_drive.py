import sys
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    # "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

MIME = {
    "folder": "application/vnd.google-apps.folder",
    "google_sheets": "application/vnd.google-apps.spreadsheet"
}


def google_drive_init(creds_filename="secret/token.pickle", fallback="secret/client_secret.json"):
    """
    Instantiates a Google Drive API v3 object from a serialized token file or
    a credentials json file. 

    Opens a browswer authenthication window to select a google account and 
    stores a serialized token object for further use without authentication.

    :param str creds_filename: Serialized pickle token file
    :param str fallback: File name for the user credentials file if no serialized token is given
    """
    creds = None
    # The file token.pickle stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(creds_filename):
        with open(creds_filename, "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                fallback, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(creds_filename, "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    return service


def upload_csv_as_google_sheets(drive, src_filename, upload_filename, parent_folder=None, log=sys.stdout):
    """
    Uploads a csv file as google sheets. 
    Puts it in a folder if given the parent folder name.
    If the file is already found and not in trash, it updated its content.

    :param drive: Google drive object to be used as cursor
    :param str src_filename: Local file name to be used as updload media body
    :param str upload_filename: Name given to the file upload with no extension
    :param str parent_folder: Name of the folder in the drive to put the upload in
    :param log: Printable output object, such as a file or console output
    """

    folder_id = None

    # If the google sheets goes in a folder
    if parent_folder != None:

        folder_metadata = {"name": parent_folder, "mimeType": MIME["folder"]}

        # Check if the folder already exists
        query = "name = '{}' and mimeType = '{}' and trashed = false".format(
            parent_folder, MIME["folder"])
        result = drive.files().list(q=query).execute().get("files", [])

        # If reponse was valid and not in trash bin
        if result:
            folder = result[0]
            folder_id = folder.get("id")

        # Create the folder if it does not already exist
        else:
            folder = drive.files().create(body=folder_metadata, fields="id").execute()
            folder_id = folder.get("id")

            # Log the result
            if log != None:
                print("[GOOGLE DRIVE] Created folder with id: {}".format(
                    folder.get("id", "[ERROR]")), file=log)

    # CSV file query
    query = "name = '{}' and mimeType = '{}' and trashed = false".format(
        upload_filename, MIME["google_sheets"])
    # Add the parent folder if it was found
    if folder_id != None:
        query += " and '{}' in parents".format(folder_id)

    result = drive.files().list(q=query).execute().get("files", [])
    file_id = result[0].get("id") if result else None

    # File found
    if file_id:

        result = drive.files().update(fileId=file_id, media_body=src_filename).execute()

        # Log the result
        if log != None:
            print("[GOOGLE DRIVE] Updated {} ({})".format(
                result["name"], result["mimeType"]), file=log)

    # File not found, create a new one
    else:
        # File metadata information for filename and mimetype of
        # google sheets file.
        csv_metadata = {"name": upload_filename,
                        "mimeType": MIME["google_sheets"]}
        if folder_id != None:
            csv_metadata["parents"] = [folder_id]

        # Upload csv file as google sheets with the drive v3 API
        result = drive.files().create(body=csv_metadata, media_body=src_filename).execute()

        # Log result
        if log != None:
            print("[GOOGLE DRIVE] Uploaded {} as {} ({})".format(
                src_filename, upload_filename, result["mimeType"]), file=log)


if __name__ == "__main__":
    upload_csv_as_google_sheets(
        src_filename="test.csv",
        upload_filename="test_csv",
        parent_folder="PythonTests",
        log=sys.stdout
    )
