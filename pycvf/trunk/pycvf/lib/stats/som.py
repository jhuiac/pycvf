#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import random, math

"""
Author: Marilen Corciovei
Version: $Id: som.py,v 1.9 2007/01/12 23:04:56 len Exp $
Description: Basic SOM algorithm implementation class
License: BSD

"""

class SOM_algorithm:
    
    def __init__(self, r, epochs = 100, epoch_iterations = 50, initial_learning_rate = 0.9):
        self.epochs = epochs;
        self.epoch_iterations = epoch_iterations
        self.initial_learning_rate = initial_learning_rate;
        self.r = r;
        #internal parameters
        self.time_constant = self.epochs/math.log(self.r/2)
    
    def radius_decay(self, t):
        """ returns the radius of influence for current epoch """
        return self.r / 2  * math.exp(-float(t/self.time_constant))

    def learning_rate_decay(self, t):
        """ returns the learning rate for current epoch """
        return self.initial_learning_rate * math.exp(-float(t/(self.epochs - t)))
    
    def distance(self, input, node):
        """ calculates the 'distance' in value space """
        dist = 0
        for i in range(len(input)):
            dist = dist + (input[i] - node[i]) * (input[i] - node[i])
        return dist
        
    def influence_decay(self, dist, radius):
        """ calculates the neiborhood function depending on dist to bmu and current radius
        both dist and radius are squared """
        return math.exp(- float(dist / 2 / radius))

class SA_two_phases(SOM_algorithm):
    
    def __init__(self, r, phaseOne = 200, phaseTwo = 100, epoch_iterations = 50, \
                initial_learning_rate = 0.9, phaseOne_learning_rate = 0.1, phaseTwo_learning_rate = 0):
        self.phaseOne = phaseOne
        self.phaseTwo = phaseTwo
        self.epochs = phaseOne + phaseTwo
        self.epoch_iterations = epoch_iterations
        self.r = r
        self.r2 = r/2
        
        self.lr0 = initial_learning_rate
        self.lr1 = phaseOne_learning_rate
        self.lr2 = phaseTwo_learning_rate
        #internal parameters
        self.radius = self.r2;
        self.radius_reduction = phaseOne / (self.r2 - 1) + 1;
        
        self.delta_lr = (self.lr0 - self.lr1)/self.phaseOne
        self.lr = self.lr0
        
    def radius_decay(self, t):
        if t > self.phaseOne:
            return 1
        # lineary discreet function
        if t % self.radius_reduction == 0:
            self.radius = self.radius - 1;
        return self.radius;
        
    def learning_rate_decay(self, t):
        if t < self.phaseOne:
            self.lr = self.lr - self.delta_lr
            return self.lr
        
        if t == self.phaseOne:
            self.lr = self.lr1
            self.delta_lr = (self.lr1 - self.lr2)/self.phaseTwo
            return self.lr
            
        self.lr = self.lr - self.delta_lr
        return self.lr

class SOM:
    def __init__(self, r, n, algorithm):
        """
        r * r = the square number of nodes
        n = the dimension of input
        """
        self.r = r
        self.n = n
        self.epoch = 1
        self.alg = algorithm

    def initialize_nodes(self):
        self.nodes = [[random.random() for j in range(self.n)] for i in range(self.r*self.r)]

    def initialize_samples(self):
        """ implement this if needed """

    def next_sample(self):
        v = []
        for i in range(self.n):
            v.append(random.random())
        return v

    def find_bmu(self, v):
        bmu = (0, self.alg.distance(v, self.nodes[0]))
        for i in range(1, self.r * self.r):
            dist = self.alg.distance(v, self.nodes[i]) 
            if dist < bmu[1]:
                bmu = (i, dist)
        return bmu

    def nodes_distance(self, i, j):
        xi = i % self.r
        yi = int(i / self.r)
        xj = j % self.r
        yj = int(j / self.r)
        return (xi - xj) * (xi - xj) + (yi - yj)*(yi - yj)
        

    def adjust_nodes(self, bmu, v, radius, learning_rate):
        for i in range(self.r * self.r):
            dist = self.nodes_distance(bmu[0], i)
            sqRadius = radius * radius
            if dist < sqRadius:
                influence = self.alg.influence_decay(dist,sqRadius)
                for j in range(self.n):
                    #adjust a single node
                    self.nodes[i][j] = self.nodes[i][j] + influence * learning_rate * (v[j] - self.nodes[i][j])

    def train_step(self):
        if self.epoch >= self.alg.epochs:
            print "Training completed"
            return 1
        radius = self.alg.radius_decay(self.epoch)
        learning_rate = self.alg.learning_rate_decay(self.epoch)
        print 'Epoch %d %0.2f %0.4f' %(self.epoch, radius, learning_rate)
        
        for i in range(self.alg.epoch_iterations):
            v = self.next_sample()
            bmu = self.find_bmu(v)
            self.adjust_nodes(bmu, v, radius, learning_rate)
        
        self.epoch = self.epoch + 1
        return 0
