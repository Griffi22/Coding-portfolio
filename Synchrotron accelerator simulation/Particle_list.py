import numpy as np
import math
import copy
import scipy.constants as const
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Fields import fields
import pandas as pd
from P_state_update import Update

"Class to create particle objects to simulate"

#Entryformat= ([initPos], [initVel], [initAcc],[initAcc_dt1],[initAcc_dt2], [Name], [Mass],[Charge],KE, [deltaT],E_plate_index)
class Particle_data_list:
    "User specified timestep input"
    DeltaT=float(input("Timestep[s] (recomended entry, 0.0001): "))
    "defining the start position for particles (using the accelerator radius)"
    Pos_start=[fields.E_prop_list()[3],10.0,0.0]
    "defining the start velocity"
    Vel_start=[0.0, 300000, 0.0]
    "Defining the list of particles and their inital properties for simlation"
    Particle_list={'Proton':Update([Pos_start,Vel_start,[0,0,0],[0,0,0],[0,0,0],'Proton',const.m_p,const.elementary_charge,0, DeltaT,0],False, None),
                   'Electron':Update([Pos_start,Vel_start,[0,0,0],[0,0,0],[0,0,0],'Electron',const.m_e,const.elementary_charge,0, DeltaT, 0],False, None),
                   'Positron':Update([Pos_start,Vel_start,[0,0,0],[0,0,0],[0,0,0],'Positron',const.m_e,const.elementary_charge,0, DeltaT, 0],False, None),
                   }