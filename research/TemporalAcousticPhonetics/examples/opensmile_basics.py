### Requires:
### pip install git+https://github.com/konan-ai/konanai.git@main#subdirectory=research/TemporalAcousticPhonetics
### pip install opensmile

import torch
import numpy
import opensmile

from TemporalAcousticPhonetics import (
    download_tap_checkpoint,
    download_tap_examples)

download_tap_checkpoint()
download_tap_examples()

CHECKPOINT = torch.load("tap_checkpoint.pt")
EXAMPLES   = torch.load("tap_examples.pt")

### Get example waveform
male_waveform   = EXAMPLES["example_male"]["metadata"]["waveform"]
male_samplerate = EXAMPLES["example_male"]["metadata"]["samplerate"]

### Define acoustic calculator
LLD = opensmile.Smile(
    feature_set   = opensmile.FeatureSet.eGeMAPSv02,
    feature_level = opensmile.FeatureLevel.LowLevelDescriptors)

### Define optional waveform padding
getPadded = lambda x: numpy.pad(x, ((0,0), (0,160*5)), mode="symmetric")

### Derive raw acoustics
male_waveform = getPadded(male_waveform.numpy())
male_rawAcoustics = LLD.process_signal(male_waveform, male_samplerate)
male_rawAcoustics = torch.Tensor(male_rawAcoustics.to_numpy()[None, :, :])

### Define acoustic standardization
mu = CHECKPOINT["acoustic_detail"]["mean"]
sigma = CHECKPOINT["acoustic_detail"]["standard_deviation"]
getStandardized = lambda x: (x-mu)/sigma

### Derive target acoustics
male_targetAcoustics = getStandardized(male_rawAcoustics)

### Confirm derived target acoustics are consistent with authors
assert torch.nn.functional.l1_loss(
    male_targetAcoustics,
    EXAMPLES['example_male']['target']['acoustics']) < 1e-6
