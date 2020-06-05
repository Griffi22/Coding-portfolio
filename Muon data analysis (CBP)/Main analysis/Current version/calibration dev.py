import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
pro_dir = np.load('Directory.npy')

"calibration test of relative effency"
def Detector_Calibration():
    
    file_list_TS=os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Caliberation data\Timestamps\\')            
    file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Caliberation data\\') if x.endswith(".txt")]
    for Index in range(0,len(file_list)):
        print(file_list,file_list_TS)
        Rawfile=file_list[Index]
        Savefile=str(file_list[Index])[:-4]+'_pro'
        Savefile_avg=str(file_list[Index])[:-4]+'_avg'
        TS_input=str(file_list_TS[Index])
        r=600
        l=3

        "This Raw_Data defines the path taken to the raw data directory and specified file, the +str(D)+ allows for the detector data file defined by the value of n"
        "to be specified as the file name is in the form of (Dntest) where n=the index of the detector"
        "The name of the location the test detector was placed in should be imputed after the +str(n)+ with the first letter capitalised"
        Raw_data = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Caliberation data\\'+str(Rawfile))
        "This opens the file specified by raw data, and adds each entry line of the raw data to a list called (lines)"
        text_file = open(Raw_data, 'r')        
        lines = text_file.readlines()
        
        TS_path = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Caliberation data\Timestamps\\'+str(TS_input))
        
        TS_file = open(TS_path, 'r')
           
        TS_raw = TS_file.readlines()
    
        "setting up initial global variables and lists for later use"
        
        "the total number of data entries to check"
        y=len(lines)
    
        "starting data entry to read from"
        print(y, file_list[Index],"len data")
        print(len(TS_raw), file_list_TS[Index], "len TS")
        x=0
        "time index at first data read (x)"
        h=0
        "the current chain decay measurments at start of data read"
        f=0
        "index for valid measurments list"
        N=0
        R=r
        "sum of count values over R time"
        k_i=0
        "t_i is the time step in seconds between each entry in the count AVG list starting at entry 1"
        t_i=R
        
        "defining our data lists as empty lists"
        count=[]
        count_err=[]
        
        Count_AVG=[]
        Count_AVG_err=[]
        
        TS=[]
        
        time=[]    
    
        Time_AVG=[]
                            
        "central loop over raw data entries"
        while x<y:
        
                "chain decay feedback error check"
                k=int(lines[int(x)])
                T=TS_raw[int(x)]
                f=0
                if k<39999:
                    "setting temp entry index and entry caller for error check"
                    x4=x
                    kc=int(lines[int(x4)])
                    while kc<39999:           
                        x4=x4+1
                        kc=int(lines[int(x4)])
                        "length of decay entry chain"
                        f=f+1
                
                if f>l-1:
                    "If decay error occurs (defined by f>l-1 value where l is the error threshold of decays/second)"
                    "skip false data entries"
                    x=x+f
                    h=h+1
                
                "if data valid add to count list, entrys with k<40000 are decay data and are not valid counts"
                if k>39999:
                    "add the count value k to the count list, minus the 40000 due to raw data format adding 40000 to the muon count value"
                    count.append(k-40000)
                    count_err.append((k-40000)**0.5)
                    TS.append(T)
                    N=N+1
                    time.append(h)
                    h=h+1
                
                    "average calulator"
                    if N%R==0 and N != 0:
                        "k_i, total counts in R seconds"
                        for i in range (N-R , N, 1):
                            k_i=k_i+count[int(i)]
                        
                        Count_AVG.append(k_i/R)
                        Count_AVG_err.append((k_i**0.5)/R)
                        Time_AVG.append(t_i)
                        t_i=t_i+R
                        k_i=0
                        
                "move to next entry"   
                x = x+1
                
        "plot of valid counts against time"
        #plt.figure(1)
        #plt.figure(figsize=(15,7))
        #plt.title('detector  count rate')
        #plt.plot(time, count)
        #plt.errorbar(time, count, yerr=count_err)
        #plt.xlabel('Time (s)')
        #plt.ylabel('Count rate (Hz)')
        #print(Count_AVG)
        #print(Count_AVG_err)
        
        "plot of counts against time averaged over (R) seconds"
        plt.figure(2)
        plt.figure(figsize=(8,4))
        
        ax=plt.axes()
        ax.set_facecolor("lightgrey")
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('0.1')
        ax.spines['top'].set_color('0.1')
        ax.spines['right'].set_color('0.1')
        ax.spines['left'].set_color('0.1')
        ax.spines['bottom'].set_lw(1.5)
        ax.spines['top'].set_lw(1.5)
        ax.spines['right'].set_lw(1.5)
        ax.spines['left'].set_lw(1.5)
        
        
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.tick_params(axis='both', colors='black')

        plt.grid(True,color='grey',linestyle='--')
        
        plt.title(''+str(Rawfile)+'detector. count rate AVG over '+str(R)+'s intervals ')
        "limits need to be manually set for best looking plot results, will improve this in future version"
        
        
        plt.plot(Time_AVG, Count_AVG,'o', color='black')
        plt.errorbar(Time_AVG, Count_AVG, yerr=Count_AVG_err, fmt=' ', ecolor='grey')
        plt.xlabel('Time (s)')
        plt.ylabel('Count rate AVG (Hz)')
        plt.show
        plt.savefig(fname=r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\Count Plots Different Locations\Processed Raw data\\'+str(Savefile_avg))

        "close the raw data file being accessed"
        text_file.close()
        #plt.close("all")
        "Save Count_AVG to the directory specified under the name (D(n)_AVG) as an .npy file."
        'lets combine data lists into singular arrays'
        CR_AVG= [Time_AVG, Count_AVG, Count_AVG_err]#, time, count]
        CR = [time, count]
        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Averaged\\'+str(Savefile_avg), CR_AVG)
        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Processed\\'+str(Savefile), CR)
        
        
        "Save Time_AVG to the directory specified under the name (Time(n)_AVG) as an .npy file."
        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Timestamp\\'+str(Savefile_avg)+'_TS',TS)
#Detector_Calibration()

def Det_Var():
    Effeincy_baseline = np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Processed\D1_Cali_pro.npy')
    file_list_Actv = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Processed\\') if x.endswith(".npy")]
    Effeincy_baseline_TS = np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Timestamp\D1_Cali_avg_TS.npy')
    file_list_Actv_TS = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Timestamp\\') if x.endswith(".npy")]
    
    file_list_Actv.sort()
    file_list_Actv_TS.sort()
    
    for i in range(0,len(file_list_Actv)):        
        D_pro_Actv_input = file_list_Actv[i][:-4]     
        TS_Actv_input = file_list_Actv_TS[i][:-4]
        
        File_Synced_avg_data_input=str(file_list_Actv[i][:-8])+'_avg'
        File_Var_input=str(file_list_Actv[i][:-8])+'_var'
        
        D_pro_Ctrl =Effeincy_baseline
        D_pro_Actv = np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Processed\\'+str(D_pro_Actv_input)+'.npy')
                        
        "Loading the control and active detector time stamp data"
        
        TS_Ctrl=Effeincy_baseline_TS
        TS_Actv=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Caliberation data\Timestamp\\'+str(TS_Actv_input)+'.npy')
        
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
        
        print(len(D_pro_Ctrl[1]), "D_pro_Ctrl[1]")
        print(len(D_pro_Actv[1]),"D_pro_Actv[1]")
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
        print(len(D_A_C_c),"D_A_C_c")
        print(desync_f,"desync_f")
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
        print(len(D_A_C_c),"D_A_C_c")
        
        "averaging synced data"
        R=int(15000)
        
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
                
        "temporary Chunk of code to fix the detectors turning on and off (improve to auto for general version)"
        
        del TE_C_C_avg[0]
        del D_C_C_avg[0]
        del D_C_C_avg_err[0]
        
        del TE_C_C_avg[len(TE_C_C_avg)-1]
        del D_C_C_avg[len(D_C_C_avg)-1]
        del D_C_C_avg_err[len(D_C_C_avg_err)-1]
   
        del TE_A_C_avg[0]
        del D_A_C_avg[0]
        del D_A_C_avg_err[0]
   
        
        del TE_A_C_avg[len(TE_A_C_avg)-1]
        del D_A_C_avg[len(D_A_C_avg)-1]
        del D_A_C_avg_err[len(D_A_C_avg_err)-1]
        
        "plotting results"
        plt.figure(1)
        plt.figure(figsize=(8,4))
    
        ax=plt.axes()
        ax.set_facecolor("lightgrey")
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('0.1')
        ax.spines['top'].set_color('0.1')
        ax.spines['right'].set_color('0.1')
        ax.spines['left'].set_color('0.1')
        ax.spines['bottom'].set_lw(1.5)
        ax.spines['top'].set_lw(1.5)
        ax.spines['right'].set_lw(1.5)
        ax.spines['left'].set_lw(1.5)
        
        
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.tick_params(axis='both', colors='black')

        plt.grid(True,color='grey',linestyle='--')
        
        plt.title('active verses control detector:'+str(File_Synced_avg_data_input)+' count rate averaged over '+str(R)+' seconds')
        plt.plot(TE_C_C_avg, D_C_C_avg,'bo:', label='Control detector', color='blue')
        plt.errorbar(TE_C_C_avg, D_C_C_avg, yerr=D_C_C_avg_err, fmt=' ', ecolor='grey', capsize=3)
        plt.plot(TE_A_C_avg, D_A_C_avg,'go-', label='Active detector',color='green')
        plt.errorbar(TE_A_C_avg, D_A_C_avg, yerr=D_A_C_avg_err, fmt=' ', ecolor='grey', capsize=3)
        plt.legend()
        plt.xlabel('Time elapsed (s)')
        plt.ylabel('Average count rate (Hz)')
        plt.savefig(fname=r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\count plot (muon decay fixed)\caliberation\Week long calibration\\'+str(File_Synced_avg_data_input))
 #       plt.close('all')
        "Calculate the Modulus percentage variation of the active data against the control"

        
        Var_=[[],[],[]]
        "[Var][Time][VAR_err]"
        print(len(D_C_C_avg), "D_C_C_avg",len(D_A_C_avg),"D_A_C_avg")
        
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
                
        print(len(D_C_C_avg), "D_C_C_avg",len(D_A_C_avg),"D_A_C_avg")
        
                
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
        plt.figure(figsize=(8,4))
        
        ax=plt.axes()
        ax.set_facecolor("lightgrey")
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('0.1')
        ax.spines['top'].set_color('0.1')
        ax.spines['right'].set_color('0.1')
        ax.spines['left'].set_color('0.1')
        ax.spines['bottom'].set_lw(1.5)
        ax.spines['top'].set_lw(1.5)
        ax.spines['right'].set_lw(1.5)
        ax.spines['left'].set_lw(1.5)
        
        
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.tick_params(axis='both', colors='black')
    
        plt.grid(True,color='grey',linestyle='--')

        plt.title(' Percentage variation of active count rate, with respect to control, averaged over ' +str(R)+ ' seconds')
        plt.plot(Var_[1],Var_[0] ,'bo-', label='% variation', color='black')
        plt.errorbar(Var_[1], Var_[0], yerr=Var_[2] , fmt=' ', ecolor='grey', capsize=3)
        plt.legend()
        plt.xlabel('Time elapsed (s)')
        plt.ylabel('% Variation')
        plt.savefig(fname=r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\count plot (muon decay fixed)\caliberation\Week long calibration\\'+str(File_Var_input))
        plt.show
#        plt.close('all')                    
        "Saving comparison results"
        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Calibration data\Variation\\'+str(File_Var_input), Var_)
        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Calibration data\Average\\'+str(File_Synced_avg_data_input), Synced_avg_data)
        

    
#Det_Var()


def Rel_Eff():
#    N=int(input("number of detectors to compare? :"))
 
    Var_=[]
    D_ref=[]
    
    file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Calibration data\Variation\\') if x.endswith(".npy")]
    
    
    for I in range(0,len(file_list)):
        
#        Var_file_input=input('Variation file '+str(I+1)+' name? (no file estension) : ')
#        Altitude_input=float(int(input("altitude of active detector?"))-71)
        Var_file_I=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Calibration data\Variation\\'+str(file_list[I]))
        Var_.append(Var_file_I)
        D_ref.append(file_list[I][:-13])
        
        
#    print(Var_[1][2][1],D_ref)
    "Var_ layout [[Var_H],[Var_A],[Var_O]]"
    "Var_[I] layout [[Var][Time][Var_Err]]"
    
    plt.figure(1)
    plt.figure(figsize=(15,7))
    ax=plt.axes()
    ax.set_facecolor("lightgrey")
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_color('0.1')
    ax.spines['top'].set_color('0.1')
    ax.spines['right'].set_color('0.1')
    ax.spines['left'].set_color('0.1')
    ax.spines['bottom'].set_lw(1.5)
    ax.spines['top'].set_lw(1.5)
    ax.spines['right'].set_lw(1.5)
    ax.spines['left'].set_lw(1.5)
    
    
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.tick_params(axis='both', colors='black')

    plt.grid(True,color='grey',linestyle='--')
    plt.title('% Variation Avg count rate relative to control across different detectors')
    for I in range(0,len(file_list)):
        plt.plot(Var_[I][1], Var_[I][0], label=str(D_ref[I]))
        plt.errorbar(Var_[I][1], Var_[I][0], yerr=Var_[I][2] , fmt=' ', ecolor='grey', capsize=3)
    plt.legend()
    plt.xlabel('Detector')
    plt.ylabel('% Variation')
    plt.show
    
    Rel_Effciency=[[],[],[]] 
    "Var avg, VAR avg_Err"
    for i in range(0,len(file_list)):
        Rel_Effciency[0].append(float(sum(Var_[i][0]/len(Var_[i][0])))+100)
        Rel_Effciency[1].append((sum((Var_[i][2])**2)/len(Var_[i][2]))**0.5)
        Rel_Effciency[2].append(D_ref[i])
    print(Rel_Effciency)
    
    plt.figure(2)
    plt.figure(figsize=(7,8))
    ax=plt.axes()
    ax.set_facecolor("lightgrey")
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_color('0.1')
    ax.spines['top'].set_color('0.1')
    ax.spines['right'].set_color('0.1')
    ax.spines['left'].set_color('0.1')
    ax.spines['bottom'].set_lw(1.5)
    ax.spines['top'].set_lw(1.5)
    ax.spines['right'].set_lw(1.5)
    ax.spines['left'].set_lw(1.5)
    
    
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.tick_params(axis='both', colors='black')

    plt.grid(True,color='grey',linestyle='--')
    plt.title('% relative effciency of detectors')
    plt.bar(D_ref,Rel_Effciency[0],width=0.4,color='skyblue', edgecolor='black',linewidth=1.4)
    #plt.errorbar(D_ref, Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='grey', capsize=3)
    plt.xlabel('Detector')
    plt.ylabel('% Efficiency of detectors')
    plt.show
    np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\settings\D_Rel_Eff', Rel_Effciency)

Rel_Eff()
