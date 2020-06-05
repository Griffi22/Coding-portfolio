import numpy as np
import math
import copy
import scipy.constants
import matplotlib.pyplot as plt
import timeit
import sympy as sy
from Field_effect import Field_effect
from Field_effect import Field_effect_derivitives

"Class to update the particle state parameters over the timestep"
class Update:

    
    "initialising the program with the required particle state properties"
    """    def __init__(self, initpos, initvel, initacc,acc_dt1,acc_dt2, name, mass,charge,ke, deltat,e_plate_index):
        self.name = name
        self.pos = np.array(initpos,dtype=float)
        self.vel = np.array(initvel,dtype=float)
        self.acc = np.array(initacc,dtype=float)
        self.mass = mass
        self.charge=charge
        self.deltat=deltat
        self.ke=ke
        self.e_plate_index=e_plate_index
        self.acc_dt1= np.array(acc_dt1,dtype=float)
        self.acc_dt2= np.array(acc_dt2,dtype=float)"""
    def __init__(self,Particle_state, Testing_OnOff, Testing_state):
        if Testing_OnOff == False:
            self.pos = np.array(Particle_state[0],dtype=float)
            self.vel = np.array(Particle_state[1],dtype=float)
            self.acc = np.array(Particle_state[2],dtype=float)
            self.Acc_dt1= np.array(Particle_state[3],dtype=float)
            self.Acc_dt2= np.array(Particle_state[4],dtype=float)
            self.Name = Particle_state[5]
            self.mass = Particle_state[6]
            self.charge=Particle_state[7]
            self.KE=Particle_state[8]
            self.DeltaT=Particle_state[9]
            self.E_plate_index=Particle_state[10]
            self.Testing_OnOff=Testing_OnOff
        if Testing_OnOff == True:
            self.pos = np.array(Testing_state[0],dtype=float)
            self.vel = np.array(Testing_state[1],dtype=float)
            self.acc = np.array(Testing_state[2],dtype=float)
            self.Acc_dt1= np.array(Testing_state[3],dtype=float)
            self.Acc_dt2= np.array(Testing_state[4],dtype=float)
            self.Name = Testing_state[5]
            self.mass = Testing_state[6]
            self.charge=Testing_state[7]
            self.KE=Testing_state[8]
            self.DeltaT=Testing_state[9]
            self.E_plate_index=Testing_state[10]
            self.Testing_OnOff=Testing_OnOff
    def __repr__(self):
        return('Particle: {0}, Mass: {1:12.3e}, pos: {2}, vel: {3}, acc: {4}'.format(self.Name,self.mass,self.pos, self.vel,self.acc))
    "updating KE"
    def KineticEnergy(self):
        self.KE=0.5*self.mass*np.linalg.norm(self.vel)**2
        return 0.5*self.mass*np.vdot(self.vel,self.vel)
    "updating mom"
    def momentum(self):
        return self.mass*np.array(self.vel,dtype=float)
    "updating pos, vel, acc"
    def update(self, formulae, **kwargs):
        "Timer for runtime optimisation"
        #start = timeit.default_timer()
        
        "collection of print statements showing the particle parameters in realtime used in development"
        #print('Vel:  ', np.linalg.norm(self.vel)*self.DeltaT)
        #print('Pos:  ', self.pos)
        #print('Acc:  ', self.acc)#*self.DeltaT)
        #print('Acc_dt1:  ', np.linalg.norm(self.Acc_dt1)*self.DeltaT)
        
        """collecting relevant parameters into a list for simmilar entry format
        to test states in feild effect"""
        Particle_state=[self.pos,self.vel,self.charge,self.mass, self.E_plate_index]
        
        """passing the particle state and assigning the feild variables required for
        the lorentz force equations the arguments given also include a boolian for determining
        whether to use the particle or test states and a test state here set to 'None' """
        if self.Testing_OnOff == False:
            fields=Field_effect(Particle_state, False, None) 
            B=fields.M_effect(False,None)
            E_eff_result_list=fields.E_effect()
            E=E_eff_result_list[0]
            self.E_plate_index=E_eff_result_list[1]
            
            """Initialising the feild deriviative subclass with any additional arguments needed
            and setting the feild deriviative variables"""
            fields_dt=Field_effect_derivitives(Particle_state, False, None, self.acc, self.Acc_dt1)
            E_dt1=fields_dt.E_effect_dt1()
            B_dt1=fields_dt.M_effect_dt1()
            E_dt2=fields_dt.E_effect_dt2()
            B_dt2=fields_dt.M_effect_dt2()
            
            "calculating the acceleration and its temporal derivatives"
            self.Acc_dt2 = (self.charge/self.mass)*(E_dt2+np.cross(self.Acc_dt1,B)+np.cross(self.acc,B_dt1)+np.cross(self.acc,B_dt1)+np.cross(self.vel,B_dt2))
            self.Acc_dt1 = (self.charge/self.mass)*(E_dt1+(np.cross(self.acc,B)+np.cross(self.vel,B_dt1)))
            self.acc = (self.charge/self.mass)*(E+np.cross(self.vel,B))
        if self.Testing_OnOff == True:
                expr_acc = sy.sympify(formulae[0])
                expr_acc_dt1 = sy.sympify(formulae[1])
                expr_acc_dt2 = sy.sympify(formulae[2])
                print(self.acc[0])
                self.acc[0]=expr_acc.evalf(subs=kwargs)
                self.Acc_dt1[0]=expr_acc_dt1.evalf(subs=kwargs)
                self.Acc_dt2[0]=expr_acc_dt2.evalf(subs=kwargs)

                print(self.acc[0])
#            Need to work out how to make the state update using equations stored in the test state function for this to be general!!!
        "calculating the velocity and position using taylor expansion of classical equations"
#        self.vel +=  (self.acc*self.DeltaT)+(self.Acc_dt1*self.DeltaT**2)/2+(self.Acc_dt2*self.DeltaT**3)/6
        self.pos +=  (self.vel*self.DeltaT)+(self.acc*self.DeltaT**2)/2+(self.Acc_dt1*self.DeltaT**3)/6+(self.Acc_dt2*self.DeltaT**4)/24
        self.vel +=  (self.acc*self.DeltaT)+(self.Acc_dt1*self.DeltaT**2)/2+(self.Acc_dt2*self.DeltaT**3)/6
        #stop = timeit.default_timer()
        #print('update time', stop-start)
        
        
        
        
        