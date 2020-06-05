import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

file_list=os.listdir(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Variation\\')
Var_=[]
"Var_[I] layout [[Var][Time][Var_Err]]"


for I in range(0,len(file_list)):
#       Altitude_input=float(input("altitude of active detector?"))
   Var_file_I=np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Variation\\'+str(file_list[I]))
   Var_.append(Var_file_I)
   
Var_AVG_=[[],[]] #[var avg], [var avg err]
zero_line=[]
for i in range(0,len(file_list)):
    Var_AVG_[0].append(float(sum(Var_[i][0]/len(Var_[i][0]))))
    Var_AVG_[1].append((sum((Var_[i][2])**2)/len(Var_[i][2]))**0.5)
    zero_line.append(0)

plt.figure(2)
plt.figure(figsize=(30,14))
plt.title('% Variation Avg count rate, relative to control, across different locations')
plt.plot(file_list ,Var_AVG_[0], 'o')
plt.plot(file_list ,zero_line, 'b:', label='Control detector')
plt.errorbar(file_list, Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='grey', capsize=3)
plt.legend()
plt.xlabel('Location code')
plt.ylabel('% Variation from control')
plt.show
