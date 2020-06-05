from Particle import Particle
from Acc_calc import Acc_calc
#import SS_sim3
import math
import matplotlib.pyplot as plt
import numpy as np
import copy
from mpl_toolkits import mplot3d
'''This program loads an external data storage file and pulls the data logging it internally in lists, simmilarly to the SS_sim3 program.
This data can then easily and quickly be analysised in  number of different without the need
to repeat the entire simulation.'''

#Set load external data command to easy to use variable.
file1 = np.load("SimulationDataFile.npy")

#Creating a empty list for each desired catagory of bodie's data.
x =  []
y =  []
z =  []
KE = []
Names = []

#Creating additional lists
t =  []
KE_tot=[]

#Expanding the data Catagory lists to contain individual lists for each entry in the list of bodies.
body=file1[0][1].bodies
for i in body:
    x.append([])
    y.append([])
    z.append([])
    KE.append([])
    Names.append(i.Name)
    
#Loop over each time=step logged.
for line in file1:
    
    #pulling body data lists out of external file
    solar_system = line[1]
    bodies = solar_system.bodies

    #logging the time
    t.append(line[0])
    KE_tmp=0

    #records the pulled data into internal data lists for each body
    for i in range(len(x)):
        x[i].append(bodies[i].pos[0])
        y[i].append(bodies[i].pos[1])
        z[i].append(bodies[i].pos[2])
        KE[i].append(bodies[i].KE)
        KE_tmp += bodies[i].KE
    KE_tot.append(KE_tmp)
    
    

#3D plot of the bodies motion. 
plt.figure(1)
plt.figure(figsize=(15,7.5))
ax = plt.axes(projection='3d')

#loop over list of bodies
plt.title('Trajectories')
for i in range(len(x)):
    plt.plot(x[i], y[i], z[i],label=Names[i])
ax.set_xlabel('x-position (m)')
ax.set_ylabel('y-position (m)')
ax.set_zlabel('z-position (m)')
plt.legend()
plt.show()

#Plot KE of each body.
plt.figure(2)
plt.figure(figsize=(10,5))
plt.title('Individual Kinetic energies')
for i in range(len(x)):
    plt.plot(t, KE[i], label=Names[i])
plt.yscale('log')
plt.xlabel('Time (s)')
plt.ylabel('Log(KE (J))')
plt.legend()
plt.show()

#plot of total KE.
plt.figure(3)
plt.figure(figsize=(10,5))
plt.title('Total Kinetic energy')
plt.plot(t, KE_tot)
plt.xlabel('Time (s)')
plt.ylabel('KE (J)')
plt.legend()
plt.show()
plt.save(plt.figure(1))


