import argparse
from src.app.enums import FileTypeEnums
from src.app import AppDownManger


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="Input file extension you want to download",
        choices=[choice.value for choice in FileTypeEnums],
    )
    parser.add_argument("url", help="Url link", type=str)
    parser.add_argument("--output", help="Output path is where you want to store the retrieved item")
    args = parser.parse_args()
    ext = args.input
    url = args.url
    output_path = args.output
    app = AppDownManger(ext, url, output_path=output_path)
    app.download()


if __name__ == "__main__":
    run()
