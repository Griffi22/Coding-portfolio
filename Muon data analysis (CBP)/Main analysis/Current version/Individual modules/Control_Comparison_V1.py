"importing useful modules"
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
"importing the class containing the relelvant varibles from Data analysis program"
#from General_Analysis_V1 import Data_input

"Active vs control comparison"
"loading the processed control and active detector data"

def Actv_Ctrl_Comp():
        H=0 #input("info input type? (custom=1 / default=0)")
        if H==1:
            D_avg_Ctrl_input = str(input("name of the averaged control detector data  file to load? (without file extension) :"))
            D_avg_Actv_input = str(input("name of the averaged active detector data file to load? (without file extension) :"))
            
            D_pro_Ctrl_input = str(input("name of the processed control detector data file to load? (without file extension) :"))
            D_pro_Actv_input = str(input("name of the processed active detector data file to load? (without file extension) :"))
            
            File_Synced_avg_data_input=input("name of save file for Synced Ctrl & Actv Avg Count rate data (dont use file extensions): ")
            File_Var_input=input("name of % variation save file between Ctrl and Actv detectors? (dont use file extensions): ")
            
            TS_Ctrl_input=str(input("name of the control detector timestamp file? (without file extension) :"))
            TS_Actv_input=str(input("name of the active detector timestamp file? (without file extension) :"))
        
        if H!=1:
            Loc=str(input("location code?"))
            D_avg_Ctrl_input = 'D1_'+str(Loc)+'_avg'
            D_avg_Actv_input = 'D3_'+str(Loc)+'_avg'
            
            D_pro_Ctrl_input = 'D1_'+str(Loc)+'_pro'
            D_pro_Actv_input = 'D3_'+str(Loc)+'_pro'
            
            TS_Ctrl_input='D1_'+str(Loc)+'_avg_TS' 
            TS_Actv_input='D3_'+str(Loc)+'_avg_TS'
            
            File_Synced_avg_data_input='D_'+str(Loc)+'_avg'
            File_Var_input='D_'+str(Loc)+'_var'
        
        D_pro_Ctrl = np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(D_pro_Ctrl_input)+'.npy')
        D_pro_Actv = np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(D_pro_Actv_input)+'.npy')
        
        D_avg_Ctrl = np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(D_avg_Ctrl_input)+'.npy')
        D_avg_Actv = np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(D_avg_Actv_input)+'.npy')
        
        "Loading the control and active detector time stamp data"
        
        #TS_Ctrl_input=str(input("name of the control detector timestamp file? (without file extension) :"))
        #TS_Actv_input=str(input("name of the active detector timestamp file? (without file extension) :"))
        
        
        TS_Ctrl=np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(TS_Ctrl_input)+'.npy')
        TS_Actv=np.load(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(TS_Actv_input)+'.npy')
        
        "calulating the initial and final desync of the detectors"
        
        TS_Ctrl_pos_i=int(TS_Ctrl[0])
        TS_Actv_pos_i=int(TS_Actv[0])
        D_A_C_c=[]
        D_A_A_c=[]
        
        if TS_Ctrl_pos_i>TS_Actv_pos_i:
            desync_i =TS_Ctrl_pos_i - TS_Actv_pos_i 
        
        if TS_Ctrl_pos_i<=TS_Actv_pos_i:
            desync_i = TS_Actv_pos_i - TS_Ctrl_pos_i
        
        TS_Ctrl_pos_f=int(TS_Ctrl[len(TS_Ctrl)-1])
        TS_Actv_pos_f=int(TS_Actv[len(TS_Actv)-1])
        
        if TS_Ctrl_pos_f>TS_Actv_pos_f:
            desync_f = TS_Ctrl_pos_f - TS_Actv_pos_f 
        
        if TS_Ctrl_pos_f<=TS_Actv_pos_f:
            desync_f = TS_Actv_pos_f - TS_Ctrl_pos_f
        
        print(len(D_pro_Ctrl[1]))
        print(len(D_pro_Actv[1]))
        "data entry allignment"
        "initial allignment"
        if TS_Ctrl_pos_i<=TS_Actv_pos_i:
            for Index in range(0, len(D_pro_Ctrl[1])-desync_i):    
                D_A_C_c.append(D_pro_Ctrl[1][Index+desync_i-1]) 
            for Index in range(0,len(D_pro_Actv[1])):
                D_A_A_c.append(D_pro_Actv[1][Index])
            
        if TS_Ctrl_pos_i>TS_Actv_pos_i:
            for Index in range(0,len(D_pro_Actv[1])-desync_i):
                D_A_A_c.append(D_pro_Actv[1][Index+desync_i-1])
            for Index in range(0,len(D_pro_Ctrl[1])):
                D_A_C_c.append(D_pro_Ctrl[1][Index])
        print(len(D_A_C_c))
        print(desync_f)
        "final allignment"
        if TS_Ctrl_pos_f>TS_Actv_pos_f:
            for Index in range(0, desync_f):
                'cut end of the ctrl'   
                del D_A_C_c[len(D_A_C_c)-1]
                
        if TS_Ctrl_pos_f<=TS_Actv_pos_f:
            for Index in range(0, desync_f):
                'cut end of the actv'
                del D_A_A_c[len(D_A_A_c)-1]
        "data now ~synced"
        print(len(D_A_C_c))
        
        "averaging synced data"
        R=int(input("number of seconds to Avg over? :"))
        
        for D in range(0,2):
            if D==1:
                count=D_A_A_c
                Loop_len=len(D_A_A_c)
            if D==0:
                count=D_A_C_c
                Loop_len=len(D_A_C_c)
            index=0
            C_AVG=[]
            C_AVG_Err=[]
            TE_AVG=[]
            TE_index=0
            C_sum=0
            while index<Loop_len:
                 #print("p2")
                 if index%R==0:
                     for i in range (index-R , index+1):
                         C_sum += count[i]
                     C_AVG.append(C_sum/R)
                     C_AVG_Err.append((C_sum**0.5)/R)
                     TE_AVG.append(TE_index)
                     TE_index += int(R)
                     C_sum=0
                 index += 1         
            if D==1:
                D_A_C_avg=C_AVG
                D_A_C_avg_err=C_AVG_Err
                TE_A_C_avg=TE_AVG
            if D==0:
                D_C_C_avg=C_AVG
                D_C_C_avg_err=C_AVG_Err
                TE_C_C_avg=TE_AVG
        
        "plotting results"
        plt.figure(1)
        plt.figure(figsize=(15,7))
        plt.title('active verses control detector count rate averaged over ' +str(R)+ ' seconds')
        plt.plot(TE_C_C_avg, D_C_C_avg,'bo:', label='Control detector', color='blue')
        plt.errorbar(TE_C_C_avg, D_C_C_avg, yerr=D_C_C_avg_err, fmt=' ', ecolor='grey', capsize=3)
        plt.plot(TE_A_C_avg, D_A_C_avg,'go-', label='Active detector',color='green')
        plt.errorbar(TE_A_C_avg, D_A_C_avg, yerr=D_A_C_avg_err, fmt=' ', ecolor='grey', capsize=3)
        plt.legend()
        plt.xlabel('Time elapsed (s)')
        plt.ylabel('Average count rate (Hz)')
        plt.savefig(fname=r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\Count Plots Different Locations\Synced Actv Vs Ctrl detector data\\'+str(File_Synced_avg_data_input))
        plt.show
        
        "Calculate the Modulus percentage variation of the active data against the control"
        
        Var_=[[],[],[]]
        "[Var][Time][VAR_err]"
        print(len(D_C_C_avg),len(D_A_C_avg))
        
        if len(D_C_C_avg)>=len(D_A_C_avg):
            Desync_avg=len(D_C_C_avg)-len(D_A_C_avg)
        if len(D_C_C_avg)<len(D_A_C_avg):
            Desync_avg=-len(D_C_C_avg)+len(D_A_C_avg)
        
        if len(D_C_C_avg)>=len(D_A_C_avg):
            for Cut in range(0,Desync_avg):
                del D_C_C_avg[len(D_C_C_avg)-1]
                del D_C_C_avg_err[len(D_C_C_avg_err)-1]
                
        if len(D_C_C_avg)<len(D_A_C_avg):
            for Cut in range(0,Desync_avg):
                del D_A_C_avg[len(D_A_C_avg)-1]
                del D_A_C_avg_err[len(D_A_C_avg_err)-1]
                
        print(len(D_C_C_avg),len(D_A_C_avg))
        
                
        Synced_avg_data=[D_A_C_avg,[D_C_C_avg]]
        if len(D_C_C_avg)>len(D_A_C_avg):
            for Index in range(0,len(D_C_C_avg)-1):
        #        Var_[0].append(100*((D_A_C_avg[Index]-D_C_C_avg[Index])**2)**0.5/D_C_C_avg[Index])
                Var_[0].append(100*((D_A_C_avg[Index]-D_C_C_avg[Index]))/D_C_C_avg[Index])
        
                Var_[1].append(TE_C_C_avg[Index])
                Var_[2].append(Var_[0][Index]*((D_A_C_avg_err[Index]/D_A_C_avg[Index])**2+(D_C_C_avg_err[Index]/D_A_C_avg[Index])**2)**0.5)
        if len(D_C_C_avg)<=len(D_A_C_avg):
            for Index in range(0,len(D_A_C_avg)-1):
        #        Var_[0].append(100*((D_A_C_avg[Index]-D_C_C_avg[Index])**2)**0.5/D_C_C_avg[Index])
                Var_[0].append(100*((D_A_C_avg[Index]-D_C_C_avg[Index]))/D_C_C_avg[Index])
        
                Var_[1].append(TE_A_C_avg[Index])
                Var_[2].append(Var_[0][Index]*((D_A_C_avg_err[Index]/D_A_C_avg[Index])**2+(D_C_C_avg_err[Index]/D_A_C_avg[Index])**2)**0.5)
        
        "Plotting percentage variation results"
        plt.figure(2)
        plt.figure(figsize=(15,7))
        plt.title(' Percentage variation of active count rate, with respect to control, averaged over ' +str(R)+ ' seconds')
        plt.plot(Var_[1],Var_[0] ,'bo-', label='% variation', color='black')
        plt.errorbar(Var_[1], Var_[0], yerr=Var_[2] , fmt=' ', ecolor='grey', capsize=3)
        plt.legend()
        plt.xlabel('Time elapsed (s)')
        plt.ylabel('% Variation')
        plt.savefig(fname=r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\Count Plots Different Locations\Synced Actv Vs Ctrl detector data\\'+str(File_Var_input))
        
        plt.show
        
        "Saving comparison results"
        np.save(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\\Variation\\'+str(File_Var_input), Var_)
        np.save(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\\Average\\'+str(File_Synced_avg_data_input), Synced_avg_data)
