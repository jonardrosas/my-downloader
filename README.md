Installations

    $python -m venv env
    $source env/bin/activate (linux) env/Script/activate (windows)
    $pip install -r requirements.txt


Usage:
    $python main.py fileformat <url> --output=<location>

    $python main.py .jpg https://www.acer.com/sg-en/laptops
    $python main.py img https://www.acer.com/sg-en/laptops
    $python main.py .pdf https://jonardrosas.com

fileformat
   - pdf, img, jpg, webp
url
   - the url where you want to search
output
   - optional location to store the downloaded file
