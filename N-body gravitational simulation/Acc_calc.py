import Particle 
import matplotlib.pyplot as plt 
import math
import copy
import numpy as np
'''This program receives bodies list from SS_sim
 and updates the acceleration experianced by each body due to all other body'''

class Acc_calc:
#Bodies data imported from SS_sim3.
    def __init__(self, bodies):
        self.bodies = bodies

    def Acc_updater(self):
        G_const = 6.67408e-11
        #Loop of target body.
        for body_i in self.bodies:
            body_i.acc=(0, 0, 0)
            #Loop of all non-target bodies.
            for body_j in self.bodies:
                if body_i != body_j:
                    #Displacement array.
                    diff_ij = body_i.pos - body_j.pos
                    #Distance apart.
                    Radius_ij=np.linalg.norm(diff_ij)
                    #Acceleration calucator using Newtons vector equation for gravitation aceleration.
                    body_i.acc=body_i.acc + (-G_const*body_j.Mass*diff_ij)/(Radius_ij**3)
                    