import os
import requests, zipfile, io
from pprint import pp
from pathlib import Path

class write:
    """

    """

    @staticmethod
    def zip_to_file(url:str, destination_directory:str, headers:dict) -> str:
        """
        Download a zip file from a url and extract it to the destination
        Headers should contatin auth
        """
        destination_directory = Path( os.path.dirname(destination_directory) ).resolve()
        os.makedirs(destination_directory, exist_ok=True)

        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(destination_directory)
            return destination_directory
        return None
