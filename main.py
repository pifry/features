import logging

from dataset import KonVidDataset

from tabulate import tabulate
import argparse


def markdown_link(name, path):
    return f"[{name}]({path})"


def html_link(name, path):
    return f'<a href="{path}">{name}</a>'


def parse_args():
    parser = argparse.ArgumentParser(description="Features extractor")
    parser.add_argument("--ohtml", help="html output path", default=None)
    parser.add_argument("--ocsv", help="csv output path", default=None)
    parser.add_argument(
        "-n",
        type=int,
        help="Number of entries to process. If not defined, process all entries in dataset",
        default=None,
    )
    parser.add_argument(
        "--ds_name", help="Name od the dataset to process", default="k150kb"
    )
    return parser.parse_args()


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

    results = []

    for i, video in enumerate(dataset.items()):

        if i == opts.n:
            break

        results.append(
            {
                "filename": html_link(video.name, video.path),
                "score": video.score,
                "fps": video.get_fps(),
                "width": video.get_width(),
                "height": video.get_height(),
                "ratio": video.get_width() / video.get_height(),
            }
        )

    if opts.ohtml:
        with open(opts.ohtml, "w+") as file:
            file.write(tabulate(results, headers="keys", tablefmt="unsafehtml"))

    if opts.ocsv:
        with open(opts.ocsv, "w+") as file:
            file.write(tabulate(results, headers="keys", tablefmt="tsv"))
