#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:18:28 2020

@author: ryanwang
"""

from __future__ import print_function

# We'll need numpy for some mathematical operations
import numpy as np

# matplotlib for displaying the output
import matplotlib.pyplot as plt


# and IPython.display for audio output
#import IPython.display

# Librosa for audio
import librosa
# And the display module for visualization
import librosa.display

#audio_path = librosa.util.example_audio_file()

# or uncomment the line below and point it at your favorite song:
#
audio_path = './../Music/AutumnLeavesOld.m4a'

y, sr = librosa.load(audio_path)


y_harmonic, y_percussive = librosa.effects.hpss(y)




#####################################################################

# We'll use a CQT-based chromagram with 36 bins-per-octave in the CQT analysis.  An STFT-based implementation also exists in chroma_stft()
# We'll use the harmonic component to avoid pollution from transients
C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, bins_per_octave=36)

print(C.shape)
# Make a new figure

'''
plt.figure(figsize=(12,4))

# Display the chromagram: the energy in each chromatic pitch class as a function of time
# To make sure that the colors span the full range of chroma values, set vmin and vmax
librosa.display.specshow(C, sr=sr, x_axis='time', y_axis='chroma', vmin=0, vmax=1)

plt.title('Chromagram')
plt.colorbar()

plt.tight_layout()
print(repr(C))

'''