import logging

from dataset import KonVidDataset

from tabulate import tabulate


def markdown_link(name, path):
    return f"[{name}]({path})"


def html_link(name, path):
    return f'<a href="{path}">{name}</a>'


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    # KonVid150kA = KonVidDataset("http://datasets.vqa.mmsp-kn.de/archives/k150ka.zip", "http://datasets.vqa.mmsp-kn.de/archives/k150ka_scores.csv") # ~176GB
    KonVid150kB = KonVidDataset(
        "http://datasets.vqa.mmsp-kn.de/archives/k150kb.zip",
        "http://datasets.vqa.mmsp-kn.de/archives/k150kb_scores.csv",
    )  # ~2GB

    results = []

    for video in KonVid150kB.random_part(count=10):

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
        # video.play()

    print(tabulate(results, headers="keys", tablefmt="unsafehtml"))
