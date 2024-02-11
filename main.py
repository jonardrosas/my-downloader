import argparse
from src.app.enums import FileTypeEnums
from src.app import AppDownloader


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="Input file extension you want to download",
        choices=[FileTypeEnums.PDF.value],
    )
    parser.add_argument("url", help="Url link", type=str)
    parser.add_argument("--output", help="Ouput path where you want to store")
    args = parser.parse_args()
    ext = args.input
    url = args.url
    output_path = args.output
    app = AppDownloader(ext, url, output_path=output_path)
    app.download()


if __name__ == "__main__":
    run()
