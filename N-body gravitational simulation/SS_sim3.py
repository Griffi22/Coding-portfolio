import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import copy
import numpy as np
import Particle
import Acc_calc

'''This Program is the umbrella program.
 it receives the user input such as planetary data,
 allows for the changing or variables and methods of calculcation used.
 It also runs the time loops used in the simulation and does does both.
 External data logging via the use of the copy module
 and internal data logging and plotting.
 '''

#Setting variables and simulation methods.
Method_of_trajectory_calc = 2  #(1=Euler Forward, 2=Euler_Cromer)


Time_intial = 0
Time_Final = 1e7 #(larger timespan lengthens calculation time)
TimeStep = 18000 #(smaller time-steps lengthen calculation time)

G=6.67408e-11


T = Time_intial
T_tot = Time_Final
deltaT = TimeStep
b = Method_of_trajectory_calc


#Input Body data in format: c

Sun = Particle.Particle([-81597899,1102919760,-9382152], [-1.338737677e01,3.781914,3.3748E-01], [0,0,0], "Sol", 1.9885e30, 1.9252579e32, deltaT)
Mercury = Particle.Particle([-1.800197122445462E+10,4.474462103204492E+10,5.200709745065896E+09], [-5.486329194479745E+04,-1.668019428299234E+01,3.668853420147829E+03], [0,0,0], "Mercury", 3.302e23, 0.5*3.302e23*((-5.486329194479745E+04)**2+(-1.668019428299234E+01)**2+(3.668853420147829E+03)**2)**0.5, deltaT)
Venus = Particle.Particle([-1.175424568769578E+10,1.080576744948187E+11,2.131765975594059E+09], [-3.494652777236348E+04,-3.984915950394390E+03,1.961520559446439E+03], [0,0,0], "Venus",48.685e23 ,0.5*48.685e23*((3.494652777236348E+04)**2+(3.984915950394390E+03)**2+(1.961520559446439E+03)**2)**0.5 , deltaT)
Earth = Particle.Particle([4.418716483E+10,1.417345895442196E+11,-1.630065561202168E+07], [-2.8922068544E+04,8.844747243E+3,3.199700435E-01], [0,0,0], "Earth", 5.97219e24, 2.7314277e+33, deltaT)
Moon = Particle.Particle([4.391597411839680E+10,1.414613237496988E+11,1.667071943025291E+07], [-2.822668624971186E+04,8.097778232201142E+03,-2.424402787139446E1], [0,0,0], "Moon", 7.343e22, 0.5*7.343e22*1022**2 , deltaT)
Satellite =  Particle.Particle([99496000+4.418716483E+10,1.417345895442196E+11,-1.630065561202168E+07], [-2.8922068544E+04,math.sqrt(G*5.97237e24/(99496000))+8.844747243E+3,3.199700435E-01], [0,0,0], "Satellite",  100, 50*2001.5**2, deltaT)
Mars = Particle.Particle([1.920045167733837E+11,9.312889760864952E+10,-2.794432002963759E+09], [-9.558176531075405E+03,2.392471275749791E+04,7.357852551726296E2], [0,0,0], "Mars",6.4171e23 ,0.5*6.4171e23*((-9.558176531075405E+03)**2+(2.392471275749791E+04)**2+(7.357852551726296E2)**2)**0.5 , deltaT)
Jupiter = Particle.Particle([-3.467425641908271E+11,-7.214683314489207E+11,1.074844098301512E+10], [1.162025165128791E+04,-5.036462590463360E+03,-2.390091753832320E2], [0,0,0], "Jupiter",1898.13e24 , 0.5*1898.13e24*((1.162025165128791E+04)**2+(-5.036462590463360E+03)**2+(-2.390091753832320E2)**2)**0.5 , deltaT)
Saturn = Particle.Particle([2.721444792942777E+11,-1.479152264376614E+12,1.488557125525457E+10], [8.967118938140448E+03,1.716425386516668E+03,-3.863114007191832E2], [0,0,0], "Saturn", 5.6834e26, 0.5*5.6834e26*((8.967118938140448E+03)**2+(1.716425386516668E+03)**2+(-3.863114007191832E2)**2)**0.5 , deltaT)
Uranus = Particle.Particle([2.553733391684733E+12,1.520568990757016E+12,-2.743652095306754E+10], [-3.533940557738904E+03,5.533859576630062E+03,6.640740183920046E1], [0,0,0], "Uranus", 86.813e24, 0.5*86.813e24*((-3.533940557738904E+03)**2+(5.533859576630062E+03)**2+(6.640740183920046E1)**2)**0.5, deltaT)
Neptune = Particle.Particle([4.332488300089594E+12, -1.131520321689376E+12, -7.654505933143669E+10], [1.336745534716727E+03,5.291388385864740E+03,-1.391180478873115E2], [0,0,0], "Neptune",102.413e24 , 0.5*(102.413e24)*((1.336745534716727E+03)**2+(5.291388385864740E+03)**2+(-1.391180478873115E2)**2)**0.5, deltaT)


#List of bodies to simulate.
solar_system = Acc_calc.Acc_calc([Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune])



#Creating a set of lists for each body.
x = []
y = []
z = []
KE = []
Names = []
KE_tot=[]
for i in solar_system.bodies:
    x.append([])
    y.append([])
    z.append([])
    KE.append([])
    Names.append(i.Name)

Data = []
Time=[]
#Loop over total time in incrimental timesteps of deltaT.

while (T<T_tot):
    #(Body data: Acceleration) updater using Acc_calc.py program.
    solar_system.Acc_updater()

    #(Body data: Position, Velocity,Kinetic energy) updater using Particle.py program.
    for body_i in solar_system.bodies:
        body_i.Pos_Vel_KE_Updater(b)
    #Percentage completion display.
    print(100*T/T_tot, '%')
    #time updater
    T += deltaT

    #External body data recorder.

    item = [T,copy.deepcopy(solar_system)]
    Data.append(item)
    np.save("SimulationDataFile", Data)

    Time.append(T)
    ke_tmp=0.0
    #Internal body data recorder.
    for i in range(len(x)):
        x[i].append(solar_system.bodies[i].pos[0])
        y[i].append(solar_system.bodies[i].pos[1])
        z[i].append(solar_system.bodies[i].pos[2])
        KE[i].append(solar_system.bodies[i].KE)
        ke_tmp += solar_system.bodies[i].KE
    KE_tot.append(ke_tmp)
#Plotting 3D Tregetory of all bodies.
fig=plt.figure()
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

#Plotting KE of each body
plt.figure(figsize=(15,7.5))
plt.title('Individual Kinetic energies')
for i in range(len(x)):
    plt.plot(KE[i], label=Names[i])
plt.yscale('log')
plt.xlabel('Time (s)')
plt.ylabel('Log(KE (J))')
plt.legend()
plt.show()

#plot of total kinetic energy
plt.figure(figsize=(15,7.5))
plt.title('Total Kinetic energy')
plt.plot(Time,KE_tot)
plt.xlabel('Time (s)')
plt.ylabel('KE (J)')
plt.legend()
plt.show()