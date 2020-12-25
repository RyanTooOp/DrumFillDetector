#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:53:14 2020

@author: ryanwang
"""

class MusicNote(object):
    
    def __init__(self, pitch):

        self.pitch = pitch
        self.duration = 1
    def getPitch(self):
        return self.pitch
    def getDuration(self):
        return self.duration
    def addDuration(self):
        self.duration += 1
    def __repr__(self):
        return (repr(self.pitch) + " note | " + repr(self.duration) + " long")
    
    
class MusicInstant(object):
    # pitchValues is a numpy array thats 12 elements long, each element represents the probability of a note
    def __init__(self, pitchValues):
        #noteObjArr holds an array of 1 and 0, each element corresponding to a particular music
        self.noteObjArr = []
        for pitchProbability in pitchValues:
            if pitchProbability < 0.8:
                self.noteObjArr += [0]
            else:
                self.noteObjArr += [1]

        
    def getNoteObjArr(self):
        return self.noteObjArr
    
