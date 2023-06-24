import requests
import os

def download_file(url, directory=None):
    if directory is None:
        directory = os.getcwd()

    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(directory, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

    return local_filename


def download_tap_checkpoint(directory=None):
    url = 'https://cmu.box.com/shared/static/043aw8m3s5fhsviritddv2x4xv69rrmn'
    download_file(url, directory)


def download_tap_transforms(directory=None):
    url = 'https://github.com/konan-ai/konanai/raw/main/research/TemporalAcousticPhonetics/TemporalAcousticPhonetics/tap_transforms.pt'
    download_file(url, directory)


def download_tap_examples(directory=None):
    url = 'https://github.com/konan-ai/konanai/raw/main/research/TemporalAcousticPhonetics/TemporalAcousticPhonetics/tap_examples.pt'
    download_file(url, directory)
