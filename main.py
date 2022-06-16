import logging
import os
from pathlib import Path

from dataset import KonVidDataset

from tabulate import tabulate
import argparse

from features import FeaturesControl
from frame_features import FrameFeatures
from global_features import GlobalFeatures
from features_plot import PlotFeatures

from multiprocessing import Pool
import tqdm


class Features(FeaturesControl, FrameFeatures, GlobalFeatures, PlotFeatures):
    pass


def markdown_link(name, path):
    return f"[{name}]({path})"


def html_link(name, path):
    return f'<a href="{path}">{name}</a>'


def normalize(results, key):
    max_value = max([x[key] for x in results])
    for row in results:
        row[key] = row[key] / max_value


def parse_args():
    parser = argparse.ArgumentParser(description="Features extractor")
    parser.add_argument("--ohtml", help="html output path", default=None)
    parser.add_argument("--ocsv", help="csv output path", default=None)
    parser.add_argument(
        "--plots",
        help="path to save plots, as default no plots will be generated",
        default=None,
    )
    parser.add_argument(
        "-n",
        type=int,
        help="Number of entries to process. If not defined, process all entries in dataset",
        default=None,
    )
    parser.add_argument(
        "-j",
        type=int,
        help="Number of concurent jobs",
        default=1,
    )
    parser.add_argument(
        "--ds_name", help="Name od the dataset to process", default="k150kb"
    )
    return parser.parse_args()


def worker(args):
    video, opts = args
    features = Features()

    if opts.plots:
        features.plot(Path(opts.plots), video)

    return {
        "filename": html_link(video.name, video.path),
        "score": video.score,
        **features(video),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    opts = parse_args()

    if opts.ds_name == "k150ka":
        dataset = KonVidDataset(
            "http://datasets.vqa.mmsp-kn.de/archives/k150ka.zip",
            "http://datasets.vqa.mmsp-kn.de/archives/k150ka_scores.csv",
        )  # ~176GB
    elif opts.ds_name == "k150kb":
        dataset = KonVidDataset(
            "http://datasets.vqa.mmsp-kn.de/archives/k150kb.zip",
            "http://datasets.vqa.mmsp-kn.de/archives/k150kb_scores.csv",
        )  # ~2GB

    if opts.plots:
        os.makedirs(opts.plots, exist_ok=True)

    import time

    start = time.time()

    if opts.j == 1:
        results = tqdm.tqdm(
            [worker((item, opts)) for item in dataset.items(opts.n)], total=opts.n
        )
    else:
        with Pool(opts.j) as p:
            results = list(
                tqdm.tqdm(
                    p.imap(
                        worker,
                        ((item, opts) for item in dataset.items(opts.n)),
                        chunksize=1,
                    ),
                    total=opts.n,
                )
            )

    end = time.time()
    print(f"Time elapsed: {end - start}")

    for key in results[0].keys():
        if not isinstance(results[0][key], str):
            normalize(results, key)

    if opts.ohtml:
        with open(opts.ohtml, "w+") as file:
            file.write(tabulate(results, headers="keys", tablefmt="unsafehtml"))

    if opts.ocsv:
        with open(opts.ocsv, "w+") as file:
            file.write(tabulate(results, headers="keys", tablefmt="tsv"))
