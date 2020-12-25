#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:20:03 2020

@author: ryanwang
"""

import aubio

def detect(filename):
        downsample = 8
        samplerate = 44100 // downsample
        print("Samplerate = " + repr(samplerate))
        win_s = 4096 // downsample # fft size - Number of chunks we are dividing the music into
        print("win_s = " + repr(win_s))
        hop_s = 512  // downsample # hop size - Number of samples read each call
        print("hop_s = " + repr(hop_s))
        s = aubio.source(filename, samplerate, hop_s)
        samplerate = s.samplerate
        tolerance = 0.8
        pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
        pitch_o.set_unit("freq")
        pitch_o.set_tolerance(tolerance)
        pitches = []
        confidences = []
        # total number of frames read
        total_frames = 0
        counter = 0
        while True:
            samples, read = s()
            print("----------")
            print("samples = " + repr(samples))
            print("read = " + repr(read))
            pitch = pitch_o(samples)[0] #Two elements. Second element is the data type of the pitch variable
            print("pitch = " + repr(pitch))
            confidence = pitch_o.get_confidence()
            print("confidence = " + repr(confidence))
            if confidence < 0.8:
                pitch = 0.
            else:
                break
            #Sample number, pitch, confidence
            print ("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
            pitches += [pitch]
            confidences += [confidence]
            total_frames += read
            if read < hop_s: break
        return pitches
    
print(detect("./../Music/AutumnLeaves.m4a"))