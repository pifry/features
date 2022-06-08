
from pathlib import Path
from tqdm import tqdm
import requests
import os
import logging
import zipfile
import csv
from random import choices

class Dataset:

    LOCATION = Path("datasets")

    def __init__(self) -> None:
        self.movies_list = None

    def fetch(self):
        raise NotImplementedError

    def random_part(self, fraction):
        for x in choices(self.movies_list, k=int(len(self.movies_list)*fraction)):
            yield x 


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
            #file_path.stat().st_size == 
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
        file_path = self.url_to_local(url)
        self.movies_dir = self.LOCATION / file_path.stem
        if self.movies_dir.is_dir():
            #file_path.stat().st_size == 
            logging.warning(f"{self.movies_dir} already exists. Skipping extraction.")
            return  
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(self.movies_dir)

    def load_movies_list(self):
        score_file = open(self.url_to_local(self.score_url), 'r')
        self.movies_list = [(name, mean_opinion, self.movies_dir / name) for name, mean_opinion, raw_mean_opinion in csv.reader(score_file, delimiter=',')]

    def fetch(self):
        self.fetch_file(self.score_url, self.LOCATION)
        self.fetch_file(self.data_url, self.LOCATION)
        self.unzip_file(self.data_url)
        self.load_movies_list()
