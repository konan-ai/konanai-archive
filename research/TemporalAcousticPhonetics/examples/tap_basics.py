 ### Requires:
### pip install git+https://github.com/konan-ai/konanai.git@main#subdirectory=research/TemporalAcousticPhonetics

import torch

from TemporalAcousticPhonetics import (
    Estimator,
    download_tap_checkpoint,
    download_tap_transforms,
    download_tap_examples)

download_tap_checkpoint()
download_tap_transforms()
download_tap_examples()

CHECKPOINT = torch.load("tap_checkpoint.pt")
TRANSFORMS = torch.jit.load("tap_transforms.pt")
EXAMPLES   = torch.load("tap_examples.pt")

### Instantiate and load acoustic estimator
model = Estimator(return_phoneme_logits=False)
model.load_state_dict(CHECKPOINT['model_state_dict'])

### Get example waveform
male_waveform   = EXAMPLES["example_male"]["metadata"]["waveform"]
male_samplerate = EXAMPLES["example_male"]["metadata"]["samplerate"]

### Derive input spectrogram
male_inputSpectrogram = TRANSFORMS(male_waveform)

### Confirm derived input spectrogram is consistent with authors
assert torch.nn.functional.l1_loss(
    male_inputSpectrogram,
    EXAMPLES['example_male']['input']['spectrogram']) < 1e-6

### Derive output acoustics
with torch.inference_mode():
    male_outputAcoustics = model(male_inputSpectrogram)

### Confirm derived output acoustics are consistent with authors
assert torch.nn.functional.l1_loss(
    male_outputAcoustics,
    EXAMPLES['example_male']['output']['acoustics']) < 1e-6

### Optional inverse standardization
mu = CHECKPOINT["acoustic_detail"]["mean"]
sigma = CHECKPOINT["acoustic_detail"]["standard_deviation"]
inverseStandardization = lambda x: (x * sigma) + mu

### Apply inverse standardization
male_estimatedAcoustics = inverseStandardization(male_outputAcoustics)
