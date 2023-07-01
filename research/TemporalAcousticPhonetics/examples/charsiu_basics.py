### Requires
### !pip install git+https://github.com/konan-ai/konanai.git@main#subdirectory=research/TemporalAcousticPhonetics
### !git clone https://github.com/lingjzhu/charsiu
### !pip install transformers praatio g2p_en g2pM

import os
import sys
import pandas as pd
import numpy
import librosa
import itertools
import torch

from TemporalAcousticPhonetics import (
    download_tap_checkpoint,
    download_tap_examples)

download_tap_checkpoint()
download_tap_examples()

CHECKPOINT = torch.load("tap_checkpoint.pt")
EXAMPLES   = torch.load("tap_examples.pt")

os.chdir('/content/charsiu')
sys.path.insert(0,'src')

from Charsiu import charsiu_forced_aligner
from Charsiu import charsiu_predictive_aligner

def forced_align(cost, phone_ids): ### SAME AS SOURCE
    D,align = librosa.sequence.dtw(C=-cost[:,phone_ids],step_sizes_sigma=numpy.array([[1, 1], [1, 0]]))
    align_seq = [-1 for i in range(max(align[:,0])+1)]
    for i in list(align):
        if align_seq[i[0]]<i[1]:
            align_seq[i[0]]=i[1]
    align_id = list(align_seq)
    return align_id

def seq2duration(phones,resolution=0.01): ### SAME AS SOURCE
    counter = 0
    out = []
    for p,group in itertools.groupby(phones):
        length = len(list(group))
        out.append((round(counter*resolution,2),round((counter+length)*resolution,2),p))
        counter += length
    return out

def custom_predictive_align(self, audio):
    audio = self.charsiu_processor.audio_preprocess(audio,sr=self.sr)
    audio = torch.Tensor(audio).unsqueeze(0).to(self.device)
    with torch.no_grad():
        out = self.aligner(audio)
    logits = out.logits.detach().cpu().numpy() ### MODIFICATION TO SOURCE

    pred_ids = torch.argmax(out.logits.squeeze(),dim=-1)
    pred_ids = pred_ids.detach().cpu().numpy()
    pred_phones = [self.charsiu_processor.mapping_id2phone(int(i)) for i in pred_ids]
    pred_phones = seq2duration(pred_phones,resolution=self.resolution)
    return pred_phones, logits ### MODIFICATION TO SOURCE

def custom_forced_align(self, audio, text):
    audio = self.charsiu_processor.audio_preprocess(audio,sr=self.sr)
    audio = torch.Tensor(audio).unsqueeze(0).to(self.device)
    phones, words = self.charsiu_processor.get_phones_and_words(text)
    phone_ids = self.charsiu_processor.get_phone_ids(phones)
    with torch.no_grad():
        out = self.aligner(audio)
    logits = out.logits.detach().cpu().numpy() ### MODIFICATION TO SOURCE
    cost = torch.softmax(out.logits,dim=-1).detach().cpu().numpy().squeeze()
    sil_mask = self._get_sil_mask(cost)
    nonsil_idx = numpy.argwhere(sil_mask!=self.charsiu_processor.sil_idx).squeeze()
    if nonsil_idx is None:
        raise Exception("No speech detected! Please check the audio file!")
    aligned_phone_ids = forced_align(cost[nonsil_idx,:],phone_ids[1:-1])
    aligned_phones = [self.charsiu_processor.mapping_id2phone(phone_ids[1:-1][i]) for i in aligned_phone_ids]
    pred_phones = self._merge_silence(aligned_phones,sil_mask)
    pred_phones = seq2duration(pred_phones,resolution=self.resolution)
    pred_words = self.charsiu_processor.align_words(pred_phones,phones,words)
    return pred_phones, pred_words, logits ### MODIFICATION TO SOURCE

charsiu_forced_aligner.align     = custom_forced_align
charsiu_predictive_aligner.align = custom_predictive_align

CFA = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')
CPA = charsiu_predictive_aligner(aligner='charsiu/en_w2v2_fc_10ms')

### Get example transcript
male_transcript = "This is a LibriVox recording. All LibriVox recordings are in the public domain. For more information, or to volunteer, please visit librivox dot org."

### Get example waveform
male_waveform   = EXAMPLES["example_male"]["metadata"]["waveform"]
male_samplerate = EXAMPLES["example_male"]["metadata"]["samplerate"]

### Define optional waveform padding
getPadded = lambda x: numpy.pad(x, ((0,0), (0,160*3)), mode="symmetric")
male_waveform = getPadded(male_waveform.numpy())

### Derive phoneme alignment, word alignment, and phoneme logits
male_alignment = CFA.align(
    audio = male_waveform ,
    text  = male_transcript    )

### Index the phoneme alignment
male_phonemeAlignment = pd.DataFrame(
    data    = male_alignment[0],
    columns = ['start', 'end', 'phoneme'])

### Index the word alignment
male_wordAlignment = pd.DataFrame(
    data    = male_alignment[1],
    columns = ['start', 'end', 'phoneme'])

### Index the phoneme logits
male_phonemeLogits = torch.tensor(male_alignment[2])

### Confirm derived phoneme logits are consistent with authors
assert torch.nn.functional.l1_loss(
    male_phonemeLogits,
    EXAMPLES['example_male']['target']['phoneme_logits']) < 1e-6
