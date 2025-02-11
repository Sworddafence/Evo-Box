import pygame
import math
import random
import numpy as np

MUTATIONRATE = 0.1
BIGMUTATIONRATE = 0.01
class Box:
    def __init__(self, dna):
        self.dna = dna
        self.muscle_array1 = np.array(self.dna[:24])
        self.muscle_array2 = np.array(self.dna[24:48])
        self.friction_array1 = np.array(self.dna[48:64])
        self.friction_array2 = np.array(self.dna[64:80])

    def mutation(self):
        mutation = np.clip(np.random.normal(0.0, 1.0, self.dna.shape), -99, 99)
        result = self.dna + mutation * MUTATIONRATE

        if (random.uniform(0,1) < BIGMUTATIONRATE):
            bigmutation = random.randint(0,79)
            delta = 0
            while abs(delta) < 0.5:
                delta = np.random.normal(0.0, 1.0, 1)
            result[bigmutation] = result[bigmutation] + delta
        
        return result
    








