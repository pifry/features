import logging

from dataset import KonVidDataset
from video import Video

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    #KonVid150kA = KonVidDataset("http://datasets.vqa.mmsp-kn.de/archives/k150ka.zip", "http://datasets.vqa.mmsp-kn.de/archives/k150ka_scores.csv") # ~176GB
    KonVid150kB = KonVidDataset("http://datasets.vqa.mmsp-kn.de/archives/k150kb.zip", "http://datasets.vqa.mmsp-kn.de/archives/k150kb_scores.csv") # ~2GB
    for video in KonVid150kB.random_part(count=1):
        print(video)
        video.play()
