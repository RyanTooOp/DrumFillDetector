#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 13:26:39 2020

@author: ryanwang
"""

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
    def __init__(self, newRootVal):
        self.rootNode = PitchNode(newRootVal)
        self.totalNode = 1
        self.minValue = newRootVal
        
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
        #Sets the  new root to be half of the size of the remaining horizontal nodes
        halfHorizontal = countHorizontal // 2
        tempRoot = self.getRootNode()
        oldRoot = self.getRootNode()
        for i in range(halfHorizontal - 1):
            tempRoot = tempRoot.getRightNode()
        newRoot = tempRoot.getRightNode()
        tempRoot.setRightNode(None)
        print("newRoot = " + repr(newRoot))
        self.setRootNode(newRoot)
        self.getRootNode().nodeAddNode(oldRoot) #Adds the old root as a new root
        print("Help me = " + repr(self.treeInorderTrav()))
        '''
        
        tempNode = self.getRootNode()
        
        
        
        
        
        
        
        
        
        for i in range(halfHorizontal-1):
            tempNode = tempNode.getRightNode()
        newRoot = tempNode.getRightNode()
        rootSmallestChild = newRoot
        while rootSmallestChild.getLeftNode() != None:
            rootSmallestChild = rootSmallestChild.getLeftNode()
        rootSmallestChild.setLeftNode(tempNode)
        tempNode.setRightNode(None)
        self.setRootNode(newRoot)
        '''
    #Function to get the minimum node value | Usually called after deleting node
    def deleteSmallestNode(self):
        currentNode = self.getRootNode()
        if currentNode.getLeftNode() == None:
            print("enter")
            self.resetRoot()
            #We do not have to set it to none, as there are no longer pointers for the node
            
            smallNode = self.getRootNode()
            while smallNode.getLeftNode() != currentNode:
                smallNode = smallNode.getLeftNode()
            smallNode.setLeftNode(currentNode.getRightNode())
            
            currentNode.setRightNode(None) #just in case having a pointer to a node keeps it in memory
        elif currentNode.getLeftNode().getLeftNode() == None:
            self.resetRoot()
            self.deleteSmallestNode()
            
            
            '''
            smallNode = self.getRootNode()
            while smallNode.getLeftNode() != currentNode:
                smallNode = smallNode.getLeftNode()
            smallNode.setLeftNode(currentNode.getRightNode())
            #print("before = " + repr(self.treeInorderTrav()))
            
            self.getRootNode().nodeAddNode(currentNode.getLeftNode())
            #print("after = " + repr(self.treeInorderTrav()))
            currentNode.setLeftNode(None)
            currentNode.setRightNode(None)
            '''
        else:
            while currentNode.getLeftNode().getLeftNode() != None:
                currentNode = currentNode.getLeftNode()
            
            smallNode = self.getRootNode()
            while smallNode.getLeftNode() != None:
                smallNode = smallNode.getLeftNode()
            currentNode.setLeftNode(smallNode.getRightNode())
            smallNode.setRightNode(None)
            '''
            smallNode.setLeftNode(currentNode.getRightNode())
            currentNode.setRightNode(None)
            '''
    def updateMinimum(self):
        currentNode = self.getRootNode()
        print("currentNode = " + repr(currentNode.getLeftNode().getLeftNode()))
        while currentNode.getLeftNode() != None:
            print("hello test")
            print("currentNode = " + repr(currentNode))
            currentNode = currentNode.getLeftNode()
        self.setMinValue(currentNode.getValue())

    #Adds a node into the binary tree
    def treeInsertNode(self, newNodeVal):
        newNode = PitchNode(newNodeVal)
        #If it is bigger than the minimum:
        if self.isBiggerMin(newNode):
            #Actually add it into the binary tree
            self.getRootNode().nodeAddNode(newNode)
            print(self.treeInorderTrav())
            #Delete the smallest node
            self.deleteSmallestNode()
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
    
    #The function to call when initializing the binary tree up to 10 nodes
    def treeInitializeInsertNode(self, newNodeVal):
        self.getRootNode().nodeAddNode(PitchNode(newNodeVal))
        self.incrementTotalNode()
        return self.getTotalNode() >= 10
    
    
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
    
            

def run():
    currentTree = InstanceBinaryTree(0)
    for i in range(1,10):
        status = currentTree.treeInitializeInsertNode(i)
        print("status = " + repr(status))
    if status == False:
        print("ERRORRRR")
    print(currentTree.treeInorderTrav())
    currentTree.treeInsertNode(5) #The program does all the backend work
    #print(currentTree.treeInorderTrav())
    currentTree.treeInsertNode(-2)
    currentTree.treeInsertNode(14)
    currentTree.treeInsertNode(100)
    currentTree.treeInsertNode(6)
    print(currentTree.treeInorderTrav())
    
    
run()
    

        