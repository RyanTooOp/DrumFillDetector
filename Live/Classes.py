#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 13:26:39 2020

@author: ryanwang
"""
import random

#The class that represents a node of a certain level of pitch (within 44100)
class PitchNode(object):
    #Initializes the class
    def __init__(self, newPitchValue):
        self.leftNode = None
        self.rightNode = None
        self.pitchValue = newPitchValue
    #Adds a node by either forwarding it to its child or making it a child
    def nodeAddNode(self, newNode):
        if newNode.getValue() > self.getValue():
            if self.getRightNode() == None:
                self.setRightNode(newNode)
            else:
                self.getRightNode().nodeAddNode(newNode)
        else:
            if self.getLeftNode() == None:
                self.setLeftNode(newNode)
            else:
                self.getLeftNode().nodeAddNode(newNode)
    #Performs the inorder traversal on a node basis
    def nodeInorderTrav(self):
        tempArr = []
        if self.getRightNode() != None and self.getLeftNode() != None:
            tempArr += self.getRightNode().nodeInorderTrav()
            tempArr += [self]
            tempArr += self.getLeftNode().nodeInorderTrav()
        elif self.getRightNode() != None and self.getLeftNode() == None:
            tempArr += self.getRightNode().nodeInorderTrav()
            tempArr += [self]
        elif self.getRightNode() == None and self.getLeftNode() != None:
            tempArr += [self]
            tempArr += self.getLeftNode().nodeInorderTrav()
        else:
            tempArr += [self]
        return tempArr
    
    #Getters and setters of the following: 
    def getLeftNode(self):
        return self.leftNode
    def getRightNode(self):
        return self.rightNode
    def getValue(self):
        return self.pitchValue
    def setLeftNode(self, newLeftNode):
        self.leftNode = newLeftNode
    def setRightNode(self, newRightNode):
        self.rightNode = newRightNode
    
    def __repr__(self):
        return str(self.getValue())
    
#The class that represents a single sample / a time period
class InstanceBinaryTree(object):
    #Initializes the class
    def __init__(self, newRootVal, newThreshold, newMaxNodesAllowed):
        self.rootNode = PitchNode(newRootVal)
        self.totalNode = 1
        self.minValue = newRootVal
        self.threshold = newThreshold
        self.maxNodesAllowed = newMaxNodesAllowed
        
    ##################################################################
    #The following is about normal inserting node
    ##################################################################
        
    #Compares new node with the minimal node to see if it needs to be added into the tree
    def isBiggerMin(self, newNode):
        return newNode.getValue() > self.getMinValue()
    def resetRoot(self):
        currentNode = self.getRootNode()
        countHorizontal = 0
        while currentNode.getRightNode() != None:
            currentNode = currentNode.getRightNode()
            countHorizontal += 1
        #If the amount of horizontal strip is smaller than 20 in total
        if countHorizontal < 11:
            #We do not need to reset the base
            return
        #Sets the  new root to be half of the size of the remaining horizontal nodes
        halfHorizontal = (countHorizontal - 10) // 2
        tempRoot = self.getRootNode()
        oldRoot = self.getRootNode()
        for i in range(halfHorizontal - 1):
            tempRoot = tempRoot.getRightNode()
        newRoot = tempRoot.getRightNode()
        print("newRoot = " + repr(newRoot))
        tempRoot.setRightNode(None)
        self.setRootNode(newRoot)
        self.getRootNode().nodeAddNode(oldRoot) #Adds the old root as a new root
        print("Root Reseted")
        
    #Detects whether we need to reset the root
    def isRequireResetRoot(self):
        currentNodeLeft = self.getRootNode()
        for left in range(self.getThreshold()):
            if currentNodeLeft.getLeftNode() == None:
                print("True in left!")
                print("Left = " + repr(left))
                return True
            currentNodeLeft = currentNodeLeft.getLeftNode()
        print("False!")
        return False
    #Function to get the minimum node value | Usually called after deleting node
    #Recursively performs this, numLoops prevents infinite loops
    def deleteSmallestNode(self, numLoops):
        currentNode = self.getRootNode()
        #Base Case #1
        if currentNode.getLeftNode() == None and numLoops < 1:
            self.resetRoot()
            #We do not have to set it to none, as there are no longer pointers for the node
            smallNode = self.getRootNode()
            #Prevents infinite recursion
            if self.getRootNode() == currentNode:
                self.deleteSmallestNode(numLoops + 1)
                return
            while smallNode.getLeftNode() != currentNode:
                smallNode = smallNode.getLeftNode()
            smallNode.setLeftNode(currentNode.getRightNode())
            
            currentNode.setRightNode(None) #just in case having a pointer to a node keeps it in memory
        elif (self.isRequireResetRoot() == True and numLoops <= 1):
            self.resetRoot()
            self.deleteSmallestNode(numLoops + 1)
        
        
        
        #elif currentNode.getLeftNode().getLeftNode() == None:
        #    self.resetRoot()
        #    self.deleteSmallestNode()
        

        #Base Case #2
        else:
            while currentNode.getLeftNode().getLeftNode() != None:
                currentNode = currentNode.getLeftNode()
            
            smallNode = self.getRootNode()
            while smallNode.getLeftNode() != None:
                smallNode = smallNode.getLeftNode()
            currentNode.setLeftNode(smallNode.getRightNode())
            smallNode.setRightNode(None)

    def updateMinimum(self):
        currentNode = self.getRootNode()
        while currentNode.getLeftNode() != None:
            currentNode = currentNode.getLeftNode()
        self.setMinValue(currentNode.getValue())

    #Adds a node into the binary tree
    def treeInsertNode(self, newNodeVal):
        newNode = PitchNode(newNodeVal)
        #If it is bigger than the minimum:
        if self.isBiggerMin(newNode):
            #Actually add it into the binary tree
            self.getRootNode().nodeAddNode(newNode)
            #Delete the smallest node
            self.deleteSmallestNode(0)
            #Update the smallest node
            self.updateMinimum()
        #else, its not added
    
    ##################################################################
    #The following is about traversing inorder of the tree
    ##################################################################
    
    #Returns the nodes from biggest to smallest in value
    def treeInorderTrav(self):
        returnArr = self.getRootNode().nodeInorderTrav()
        return returnArr
    
    ##################################################################
    #The following is used to incremenet
    ##################################################################
    
    #The function to call when initializing the binary tree up to maxNodesAllowed nodes
    def treeInitializeInsertNode(self, newNodeVal):
        self.getRootNode().nodeAddNode(PitchNode(newNodeVal))
        self.incrementTotalNode()
        return self.getTotalNode() >= self.getMaxNodesAllowed()
    
    
    ##################################################################
    #The following are getters and setters
    ##################################################################
    
    #Getters and setters
    def getMinValue(self):
        return self.minValue
    def setMinValue(self, newMinValue):
        self.minValue = newMinValue
    def getTotalNode(self):
        return self.totalNode
    def incrementTotalNode(self):
        self.totalNode += 1
    def getRootNode(self):
        return self.rootNode
    def setRootNode(self, otherNode):
        self.rootNode = otherNode
    def getThreshold(self):
        return self.threshold
    def getMaxNodesAllowed(self):
        return self.maxNodesAllowed
    
            

def run():

    totalCount = 1
    
    threshold = int(input("What is the threshold for the binary tree?"))
    maxNodesAllowed = int(input("What is the maximum nodes allowed?"))
    firstVal = int(input("First node? "))
    
    currentTree = InstanceBinaryTree(firstVal, threshold, maxNodesAllowed)
    
    #for i in testArr:
    #    currentTree.treeInitializeInsertNode(i)
    while True:
        '''
        #inputStr = input("Give me a number")
        
        
        x = int(input("Are you ready?"))
        currentTree.treeInsertNode(x)
        print(currentTree.treeInorderTrav())
        '''
        inputStr = random.randint(0, 1000)
        if totalCount < maxNodesAllowed:
            currentTree.treeInitializeInsertNode(int(inputStr))
            totalCount += 1
        else:
            input("Are you ready?")
            currentTree.treeInsertNode(int(inputStr))
        print(currentTree.treeInorderTrav())
        
        
            
    '''
    currentTree = InstanceBinaryTree(0)
    for i in range(1,10):
        status = currentTree.treeInitializeInsertNode(i)
        print("status = " + repr(status))
    if status == False:
        print("ERRORRRR")
    currentTree.treeInsertNode(5) #The program does all the backend work
    #print(currentTree.treeInorderTrav())
    currentTree.treeInsertNode(-2)
    currentTree.treeInsertNode(14)
    currentTree.treeInsertNode(5.5)
    currentTree.treeInsertNode(5.6)
    currentTree.treeInsertNode(6.5)
    print(currentTree.treeInorderTrav())
    '''

run()
    

        