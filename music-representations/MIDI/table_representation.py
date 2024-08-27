import os
import sys

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import colors
import pretty_midi
import pandas as pd
import IPython.display as ipd

sys.path.append('..')
import libfmp.c1

# load the MIDI file
fn = os.path.join('.', 'A Thousand Miles.mid')
midi_data = pretty_midi.PrettyMIDI(fn)
midi_list = []

# extract notes from the MIDI file
for instrument in midi_data.instruments:
    for note in instrument.notes:
        start = note.start
        end = note.end
        pitch = note.pitch
        velocity = note.velocity
        midi_list.append([start, end, pitch, velocity, instrument.name])
        
# sort the notes by start time and pitch
midi_list = sorted(midi_list, key=lambda x: (x[0], x[2]))

# create a DataFrame from the note information
df = pd.DataFrame(midi_list, columns=['Start', 'End', 'Pitch', 'Velocity', 'Instrument'])

# convert the DataFrame to HTML
html = df.to_html(index=False)

# save the HTML table to a file
with open('midi_table.html', 'w') as f:
    f.write(html)

print("HTML table saved to 'midi_table.html'")

# display the HTML table in a Jupyter Notebook 
ipd.HTML(html)

