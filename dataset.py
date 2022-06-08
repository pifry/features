
from pathlib import Path
from tqdm import tqdm
import requests
import os
import logging
import zipfile

class Dataset:

    LOCATION = Path("datasets")

    def __init__(self) -> None:
        pass

    def fetch(self):
        raise NotImplementedError


class KonVidDataset(Dataset):
    def __init__(self, data_url, score_url) -> None:
        super().__init__()
        self.data_url = data_url
        self.score_url = score_url
        self.fetch()

    def url_to_local(self, url):
        return self.LOCATION / Path(url).name

    def fetch_file(self, url, dir):
        os.makedirs(dir, exist_ok=True)
        file_path = self.url_to_local(url)
        if file_path.is_file():
            logging.warning(f"{file_path} already exists. Skipping download.")
            return
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(file_path, "wb") as handle:
            for data in response.iter_content(chunk_size=100*1024):
                progress_bar.update(len(data))
                handle.write(data)
        progress_bar.close()

    def unzip_file(self, url):        
        with zipfile.ZipFile(self.url_to_local(url), 'r') as zip_ref:
            zip_ref.extractall(self.LOCATION)

    def fetch(self):
        self.fetch_file(self.score_url, self.LOCATION)
        self.fetch_file(self.data_url, self.LOCATION)
        self.unzip_file(self.data_url)
