import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class Altitude_dependance:
    N=int(input("number of locations to plot? :"))
    Var_=[]
    Name_Altitude_Sheilding=[[],[]]
    
    for I in range(0,N):
        Var_file_input=input('Variation file '+str(I+1)+' name? (no file estension) : ')
        Altitude_input=float(int(input("altitude of active detector?"))-71)
        Var_file_I=np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Variation\\'+str(Var_file_input)+'.npy')
        Var_.append(Var_file_I)
        Name_Altitude_Sheilding[0].append(Var_file_input)
        Name_Altitude_Sheilding[1].append(Altitude_input)
        
    print(Var_[1][2][1],Name_Altitude_Sheilding[0][1])
    "Var_ layout [[Var_H],[Var_A],[Var_O]]"
    "Var_[I] layout [[Var][Time][Var_Err]]"
    
    plt.figure(1)
    plt.figure(figsize=(15,7))
    plt.title('% Variation Avg count rate relative to control across different locations')
    
    for I in range(0,N):
        plt.plot(Var_[I][1],Var_[I][0], label=str(Name_Altitude_Sheilding[0][I]))
        plt.errorbar(Var_[I][1], Var_[I][0], yerr=Var_[I][2] , fmt=' ', ecolor='grey', capsize=3)
    plt.legend()
    plt.xlabel('Time elapsed (s)')
    plt.ylabel('% Variation')
    plt.show
    
    Var_AVG_=[[],[]] 
    "Var avg, VAR avg_Err"
    for i in range(0,N):
        Var_AVG_[0].append(float(sum(Var_[i][0]/len(Var_[i][0]))))
        Var_AVG_[1].append((sum((Var_[i][2])**2)/len(Var_[i][2]))**0.5)
    
    plt.figure(2)
    plt.figure(figsize=(15,7))
    plt.title('% Variation Avg count rate relative to control against altitude across different locations')
    plt.plot(Name_Altitude_Sheilding[1],Var_AVG_[0])
    plt.errorbar(Name_Altitude_Sheilding[1], Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='grey', capsize=3)
    plt.xlabel('Altitude W.R.T D1 (m)')
    plt.ylabel('% Variation from control')
    plt.show
    
    Grad_v_a=((Var_AVG_[0][len(Var_AVG_[0])-1]-Var_AVG_[0][0])/(Name_Altitude_Sheilding[1][len(Name_Altitude_Sheilding[1])-1]-Name_Altitude_Sheilding[1][0]))
    Grad_v_a_err=((((Var_AVG_[0][len(Var_AVG_[0])-1]+Var_AVG_[1][len(Var_AVG_[0])-1]-Var_AVG_[0][0]-Var_AVG_[1][0])/(Name_Altitude_Sheilding[1][len(Name_Altitude_Sheilding[1])-1]-Name_Altitude_Sheilding[1][0]))-Grad_v_a)**2)**0.5

    print('Gradient_Variation against relative altitude from D1=' ,Grad_v_a,'+/-',Grad_v_a_err,' %/Meter')