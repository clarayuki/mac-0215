import os
import sys

import pretty_midi
import pandas as pd
from scipy.io.wavfile import write
import numpy as np
import IPython.display as ipd

sys.path.append('..')
import libfmp.c1

# load the MIDI file
fn = os.path.join('.', 'A Thousand Miles.mid')
midi_data = pretty_midi.PrettyMIDI(fn)

# synthesize the audio data
Fs = 22050
audio_data = midi_data.synthesize(fs=Fs)

# play the audio in a Jupyter Notebook 
ipd.display(ipd.Audio(audio_data, rate=Fs))

# convert the audio data to 16-bit PCM format if it's in float format
if np.issubdtype(audio_data.dtype, np.floating):
    audio_data = np.int16(audio_data * 32767)  # scale to 16-bit range

# Save the synthesized audio to a WAV file
output_wav = 'A_Thousand_Miles.wav'
write(output_wav, Fs, audio_data)
print(f"Audio saved to '{output_wav}'")