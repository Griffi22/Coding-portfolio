import numpy as np
import math
import copy
import scipy.constants
#This class populates the simulation with feild sources
class fields:
    def E_prop_list():
        "Setting the inital variables needed"
        "E_plate_radius:radius of the virtual charged plates"
        E_plate_radius=20
        "List for allocation of plate position"
        E_source_pos_list=[]
        "Number of source plates to generate"
        num_E_source=200
        "Defining the accelerator radius"
        Path_rad=10000

        "Generating the sources equally spaced across the accelerator path, using angular spacing."
        for i in range(0,num_E_source):
            phi=i*2*math.pi/num_E_source
            E_source_pos_list.append([Path_rad*math.cos(phi),Path_rad*math.sin(phi),0.00])
        "Setting the charge density of each source plate"
        E_source_chargedensity_list=[]
        for i in range(0,len(E_source_pos_list)):
            E_source_chargedensity_list.append(1*10**-11)
        "Making the E lists circular by linking the last and first entry"
        E_source_pos_list.append(E_source_pos_list[0])
        E_source_chargedensity_list.append(E_source_chargedensity_list[0])
        "returning variables to be used elsewhere"
        return(E_source_pos_list,E_source_chargedensity_list,E_plate_radius,Path_rad,num_E_source)

    def M_prop_list(self,P_vel):
        """This function is currently unused as the magnetic feild effect required is calculated
        instead of resulting from a magnetic source distribution"""
        B=np.array([0.0,0.0,0], dtype=float)
        return(B)



