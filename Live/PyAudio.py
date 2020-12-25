"""
Notebook for streaming data from a microphone in realtime

audio is captured using pyaudio
then converted from binary data to ints using struct
then displayed using matplotlib

scipy.fftpack computes the FFT

if you don't have pyaudio, then run

>>> pip install pyaudio

note: with 2048 samples per chunk, I'm getting 20FPS
when also running the spectrum, its about 15FPS
"""
#Displays in a separate TK window
#%matplotlib qt

import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError



# constants
CHUNK = 1024 * 4             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))


'''


The bottom graph: 
    The x axis has length 44100, separated equally into "chunk" intervals
        There will be chunk amounts of data each time by the sound sensor (sensor collects chunk amounts of data per second)
            Each one of these chunks (one of the 4096) will map to a certain rate within 44100
        The distribution of the data will be in logx (bcz of some sound law)
    The y axis ranges from 0 to 1.0

'''

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform) | Creates a list of 0 to 2*CHUNK with spacing 2

#(Start, stop, number of numbers between the two numbers (inclusive))
#Can be seen as the number of chunks within one second
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
#Only changes the scale of the number scale
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# format spectrum axes
ax2.set_xlim(20, RATE)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()


count = 0

while True:
    
    # binary data
    data = stream.read(CHUNK, exception_on_overflow=False)  
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    
    
    line.set_ydata(data_np)
    
    # compute FFT and update line
    yf = fft(data_int)
    arrData = np.abs(yf[0:CHUNK])  / (128 * CHUNK)
    
    
    
    ##################################################
    #The following is my code
    ##################################################
    
    startRaw = 100
    endRaw = 10000
    
    startRecord = 4096 * startRaw // 44100#10
    
    endRecord = 4096 * endRaw // 44100 #929
    
    
    if count%50 == 0:
        #The data to be processed: arrData
        #Length: 4096 points
        
        #print(max(arrData))
        data = list(arrData)[startRecord:endRecord]
        print(len(data))
        print(max(data))
        print(data[:10])
        print(data.index(max(data)))
        
        rawHigh = 44100*max(data)//4096
        print("rawHigh = " + repr(rawHigh))
    
    
    
    count += 1
    
    arrData[:startRecord] = 0
    arrData[endRecord:] = 0

    line_fft.set_ydata(arrData)
    
    
    #How to test the x-axis of the grah
    #testArr = np.full((1, 4096), 0.5)
    #testArr = np.full((4096), 0.5)
    
    #testArr[1024:2048] = 0.8
    
    
    #line_fft.set_ydata(testArr)
    
    
    ##################################################
    #My code ends here
    ##################################################
    
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break