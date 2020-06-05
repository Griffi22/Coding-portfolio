import numpy as np
import math
import matplotlib.pyplot as plt
'''This program takes a single bodie's data
It then depending on the user instructions updates the body's
position and velocity using the Euler forward or Euler-Cromer method.
This program also updates the particles Kinetic energy
based on the updated velocity values.'''
class Particle:

        #Receives corrisponding data to whichever body is being updated.
        def __init__(self, initialPosition, initialVelocity, initialAcceleration, Name, Mass, KE, deltaT):
            self.pos = np.array(initialPosition)
            self.vel = np.array(initialVelocity)
            self.acc = np.array(initialAcceleration)
            self.Name = Name
            self.Mass = Mass
            self.deltaT = deltaT
            self.KE= KE


        def __repr__(self):
            return 'Particle: %10s, Mass: %.5e, Position: %s, Velocity: %s, Acceleration:%s' %(self.Name,self.Mass,self.pos, self.vel, self.acc)

        #Data updating, housing both methods of update alongside a kinetic energy updater.
        def Pos_Vel_KE_Updater(self, a):
            #If statment to give the user the desired update statment based on the assigned value of argument "a".
            if a == 1: #Euler forward update method
                self.pos = self.pos+self.vel*self.deltaT
                self.vel = self.vel+self.acc*self.deltaT
                #KE updater
                self.KE=0
                self.KE=0.5*self.Mass*(np.linalg.norm(self.vel))**2
            elif a == 2: #Euler-Cromer update method
                self.vel = self.vel+self.acc*self.deltaT
                self.pos = self.pos+self.vel*self.deltaT
                #KE updater
                self.KE=0
                self.KE=0.5*self.Mass*(np.linalg.norm(self.vel))**2
