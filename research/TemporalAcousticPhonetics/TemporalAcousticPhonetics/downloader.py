import os
import requests

URLS = {
    "checkpoint": 'https://cmu.box.com/shared/static/043aw8m3s5fhsviritddv2x4xv69rrmn',
    "transforms": 'https://cmu.box.com/shared/static/gywgfl9mjq57vsj3vwscmlnnm5wpaays',
    "examples": 'https://cmu.box.com/shared/static/dfv57ax0fkhqx6fzismssalafyr84b79'
}

FILENAMES = {
    "checkpoint": "tap_checkpoint.pt",
    "transforms": "tap_transforms.pt",
    "examples": "tap_examples.pt",
}

def download_file(url, dest_folder, filename):
    """
    Downloads a file from the provided URL and saves it to the specified directory.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create directory

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(dest_folder, filename), 'wb') as fp:
            fp.write(response.content)
    else:
        print(f"Failed to download file from {url}")

def download_tap_checkpoint(directory='.'):
    download_file(URLS["checkpoint"], directory, FILENAMES["checkpoint"])

def download_tap_transforms(directory='.'):
    download_file(URLS["transforms"], directory, FILENAMES["transforms"])

def download_tap_examples(directory='.'):
    download_file(URLS["examples"], directory, FILENAMES["examples"])
