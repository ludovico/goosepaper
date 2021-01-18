import argparse
from pathlib import Path

from rmapy.document import ZipDocument
from rmapy.api import Client
from rmapy.folder import Folder
from rmapy.exceptions import AuthError


def upload(filepath=None):

    if not filepath:
        parser = argparse.ArgumentParser("Upload Goosepaper to reMarkable tablet")
        parser.add_argument(
            "file", default=None, help="The file to upload",
        )
        args = parser.parse_args()
        filepath = args.file

    filepath = Path(filepath)

    client = Client()

    try:
        client.renew_token()
    except AuthError:
        print(
            "Looks like this if the first time you've uploaded, need to register the device"
        )
        print("Get the code from here: https://my.remarkable.com/connect/remarkable")
        code = input()
        print("registering")
        client.register_device(code)
        if not client.renew_token():
            print("registration failed D:")
        else:
            print("registration successful")

    folder = None
    for item in client.get_meta_items():
        if item.VissibleName == "Papers":
            folder = Folder(ID=item.ID)

        if item.VissibleName == filepath.stem:
            print("Honk! Paper already exists!")
            return False

    if not folder:
        print("creating folder")
        folder = Folder("Papers")
        client.create_folder(folder)

    doc = ZipDocument(doc=str(filepath.resolve()))
    items = client.get_meta_items()

    if client.upload(doc, to=folder):
    #if client.upload(doc):
        print("Honk! Upload successful!")
    else:
        print("Honk! Error with upload!")

    return True
