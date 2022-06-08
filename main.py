from dataset import KonVidDataset
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    KonVid150kB = KonVidDataset("http://datasets.vqa.mmsp-kn.de/archives/k150kb.zip", "http://datasets.vqa.mmsp-kn.de/archives/k150kb_scores.csv")