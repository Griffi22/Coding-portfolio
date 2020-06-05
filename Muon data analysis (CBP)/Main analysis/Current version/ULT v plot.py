import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import scipy.integrate as integrate
import scipy.special as special
import math

plt.style.use('ggplot')


pro_dir=np.load('Directory.npy')
class Analysis():
    Stop=False
    while Stop==False:
        def inputs():
            print("\n Welcome to Complete_analysis,  please choose an option from the following menu.")
            print("(The default order of the anlysis_V1, analysis functions are 1st,2nd,3rd,4th.")
            print("If this is your first time running the program please select 'program settings' and define a program directory before use")
            Selection = int(input("Analysis options: 1=Raw Data Analysis, 2= Active Against Control Comparison \n3=Altitude dependence, 4=Variation comparison across location, 0=program settings \n \n(Enter selection using assoiated number): "))
            return(Selection)
        
        
        def Settings():
            print("Please enter the program directory. This is the directory leading to and including '\Cosmic bae project' ")
            Program_dir=input("Program directory: ")
            np.save('Directory', Program_dir)
            


        if pro_dir == "#####        'please enter a directory by running the settings function'         #####":
            print("The current program directory is 'None'!")
            Settings()
            pro_dir = np.load('Directory.npy')

        Set=inputs()
        
        pro_dir = np.load('Directory.npy')

        def RawFile_Analysis():
            
            Alt_dep=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\settings\Alt_Dep.npy')
            #print(Alt_dep[0],Alt_dep[1])
            Rel_Eff=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\settings\D_Rel_Eff.npy')
            
            file_list_TS=os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 1\Timestamps\\')            
            
            file_list_TS.sort()
            
            file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 1\\') if x.endswith(".txt")]
            
            file_list.sort()
            
            Run_num=1
            if Run_num < len(file_list):
                print(file_list,file_list_TS)
                for Index in range(0,len(file_list)):

                    Rawfile=file_list[Index]
                    Savefile=str(file_list[Index])[:-4]+'_pro'
                    Savefile_avg=str(file_list[Index])[:-4]+'_avg'
                    TS_input=str(file_list_TS[Index])
                    l=3
                    print(len(file_list), Run_num )

                    "This Raw_Data defines the path taken to the raw data directory and specified file, the +str(D)+ allows for the detector data file defined by the value of n"
                    "to be specified as the file name is in the form of (Dntest) where n=the index of the detector"
                    "The name of the location the test detector was placed in should be imputed after the +str(n)+ with the first letter capitalised"
                    Raw_data = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 1\\'+str(Rawfile))
                    "This opens the file specified by raw data, and adds each entry line of the raw data to a list called (lines)"
                    text_file = open(Raw_data, 'r')        
                    lines = text_file.readlines()
                    
                    TS_path = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 1\Timestamps\\'+str(TS_input))
                    
                    TS_file = open(TS_path, 'r')
                       
                    TS_raw = TS_file.readlines()
                
                    "setting up initial global variables and lists for later use"
                    
                    "the total number of data entries to check"
                    y=len(lines)
                
                    "starting data entry to read from"
                    print(y, file_list[Index],"len data")
                    print(len(TS_raw), file_list_TS[Index], "len TS")
                    x=0
                    r=int(input("number of seconds to average over?"))

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
                                count.append((k-40000)*(100/float(Rel_Eff[0][0])))
                                count_err.append(((k-40000)*(100/float(Rel_Eff[0][0])))**0.5)
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
                    plt.close("all")
                    "Save Count_AVG to the directory specified under the name (D(n)_AVG) as an .npy file."
                    'lets combine data lists into singular arrays'
                    CR_AVG= [Time_AVG, Count_AVG, Count_AVG_err]#, time, count]
                    CR = [time, count]
                    np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Averaged\\'+str(Savefile_avg), CR_AVG)
                    np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Processed\\'+str(Savefile), CR)
                    
                    
                    "Save Time_AVG to the directory specified under the name (Time(n)_AVG) as an .npy file."
                    np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Timestamp\\'+str(Savefile_avg)+'_TS',TS)
                    
                    Run_num=Run_num+1
                    
                    
            if Run_num >= len(file_list):
                file_list_Alt=os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 3\Altitude (W.R.T, D_Ctrl)\\')
                file_list_Alt.sort()
                
                file_list_TS=os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 3\Timestamps\\')            
                file_list_TS.sort()
                
                file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 3\\') if x.endswith(".txt")]
                file_list.sort()
                
                Run_num=0
                
                if Run_num < len(file_list):
                    print(file_list,file_list_TS)
                    for Index in range(0,len(file_list)):

                        Rawfile=file_list[Index]
                        Altitude_file=file_list_Alt[Index]
                        Savefile=str(file_list[Index])[:-4]+'_pro'
                        Savefile_avg=str(file_list[Index])[:-4]+'_avg'
                        TS_input=str(file_list_TS[Index])
                        l=3
        
                        "This Raw_Data defines the path taken to the raw data directory and specified file, the +str(D)+ allows for the detector data file defined by the value of n"
                        "to be specified as the file name is in the form of (Dntest) where n=the index of the detector"
                        "The name of the location the test detector was placed in should be imputed after the +str(n)+ with the first letter capitalised"
                       
                        Raw_data = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 3\\'+str(Rawfile))
                        "This opens the file specified by raw data, and adds each entry line of the raw data to a list called (lines)"
                        text_file = open(Raw_data, 'r')        
                        lines = text_file.readlines()
                        
                        
                        TS_path = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 3\Timestamps\\'+str(TS_input))
                        TS_file = open(TS_path, 'r')
                        TS_raw = TS_file.readlines()
                        
                        
                        Altitude_data = Path(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Detector 3\Altitude (W.R.T, D_Ctrl)\\'+str(Altitude_file))
                        Alt_file= open(Altitude_data, 'r')                        
                        Alt=Alt_file.readlines()
                        
                        
                        "setting up initial global variables and lists for later use"
                        
                        "the total number of data entries to check"
                        y=len(lines)
                    
                        "starting data entry to read from"
                        print(y, file_list[Index],"len data")
                        print(len(TS_raw), file_list_TS[Index], "len TS")
                        r=int(input("number of seconds to average over?"))

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
                                    #print(float(Alt[0])*(float(Alt_dep[0])/100))
                                    count.append((k-40000)*(100/float(Rel_Eff[0][2]))  *(1-(float(Alt[0])*(float(Alt_dep[0])/100))))
                                    count_err.append(((k-40000)*(100/float(Rel_Eff[0][0])))**0.5)


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
                        plt.title(''+str(Rawfile)+'detector. count rate AVG over '+str(R)+'s intervals ')
                        "limits need to be manually set for best looking plot results, will improve this in future version"
                        #plt.ylim(2.25, 4.25)
                        
                        plt.plot(Time_AVG, Count_AVG,'o', color='black')
                        plt.errorbar(Time_AVG, Count_AVG, yerr=Count_AVG_err, fmt=' ', ecolor='grey')
                        plt.xlabel('Time (s)')
                        plt.ylabel('Count rate AVG (Hz)')
                        #plt.ylim(3, 3.90)
                        plt.savefig(fname=r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\Count Plots Different Locations\Processed Raw data\\'+str(Savefile_avg))

                        "close the raw data file being accessed"
                        text_file.close()
                        plt.close("all")
                        "Save Count_AVG to the directory specified under the name (D(n)_AVG) as an .npy file."
                        'lets combine data lists into singular arrays'
                        CR_AVG= [Time_AVG, Count_AVG, Count_AVG_err]#, time, count]
                        CR = [time, count]
                        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Averaged\\'+str(Savefile_avg), CR_AVG)
                        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 3\Processed\\'+str(Savefile), CR)
                        
                        
                        "Save Time_AVG to the directory specified under the name (Time(n)_AVG) as an .npy file."
                        np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 3\Timestamp\\'+str(Savefile_avg)+'_TS',TS)
                        Run_num=Run_num+1
#            print("analysis results are now saved to data_AVG and plots folders")
            
                
        
        
        
        
        
        "Active vs control comparison"
        "loading the processed control and active detector data"
        def Actv_Ctrl_Comp():
                file_list_Ctrl = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Processed\\') if x.endswith(".npy")]
                file_list_Actv = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 3\Processed\\') if x.endswith(".npy")]
                file_list_Ctrl_TS = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Timestamp\\') if x.endswith(".npy")]
                file_list_Actv_TS = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 3\Timestamp\\') if x.endswith(".npy")]
                
                file_list_Ctrl.sort()
                file_list_Actv.sort()
                file_list_Ctrl_TS.sort()
                file_list_Actv_TS.sort()
                
                for i in range(0,len(file_list_Ctrl)):
                    
                    print(file_list_Ctrl[i][:-4], file_list_Actv[i][:-4])
                    D_pro_Ctrl_input = file_list_Ctrl[i][:-4]
                    D_pro_Actv_input = file_list_Actv[i][:-4]
                    TS_Ctrl_input = file_list_Ctrl_TS[i][:-4]
                    TS_Actv_input = file_list_Actv_TS[i][:-4]
                    
                    File_Synced_avg_data_input='D_'+str(file_list_Ctrl[i][3:-8])+'_avg'
                    File_Var_input='D_'+str(file_list_Ctrl[i][3:-8])+'_var'
                    
                    D_pro_Ctrl = np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Processed\\'+str(D_pro_Ctrl_input)+'.npy')
                    D_pro_Actv = np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 3\Processed\\'+str(D_pro_Actv_input)+'.npy')
                                    
                    "Loading the control and active detector time stamp data"
                    
                    TS_Ctrl=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 1\Timestamp\\'+str(TS_Ctrl_input)+'.npy')
                    TS_Actv=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\Detector 3\Timestamp\\'+str(TS_Actv_input)+'.npy')
                    
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
                    R=int(input("how many seconds to average over? : "))
                    
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
                    plt.figure(figsize=(8,4))
                    plt.title('active verses control detector:'+str(File_Synced_avg_data_input)+' count rate averaged over '+str(R)+' seconds')
                    plt.plot(TE_C_C_avg, D_C_C_avg,'bo:', label='Control detector', color='blue')
                    plt.errorbar(TE_C_C_avg, D_C_C_avg, yerr=D_C_C_avg_err, fmt=' ', ecolor='grey', capsize=3)
                    plt.plot(TE_A_C_avg, D_A_C_avg,'go-', label='Active detector',color='green')
                    plt.errorbar(TE_A_C_avg, D_A_C_avg, yerr=D_A_C_avg_err, fmt=' ', ecolor='grey', capsize=3)
                    plt.legend()
                    plt.xlabel('Time elapsed (s)')
                    plt.ylabel('Average count rate (Hz)')
                    plt.savefig(fname=r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\Count Plots Different Locations\Synced Actv Vs Ctrl detector data\\'+str(File_Synced_avg_data_input))
                    plt.close('all')
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
                    plt.title(' Percentage variation of active count rate, with respect to control, averaged over ' +str(R)+ ' seconds')
                    plt.plot(Var_[1],Var_[0] ,'bo-', label='% variation', color='black')
                    plt.errorbar(Var_[1], Var_[0], yerr=Var_[2] , fmt=' ', ecolor='grey', capsize=3)
                    plt.legend()
                    plt.xlabel('Time elapsed (s)')
                    plt.ylabel('% Variation')
                    plt.savefig(fname=r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\plots\Count Plots Different Locations\Synced Actv Vs Ctrl detector data\\'+str(File_Var_input))
                    plt.show
                    plt.close('all')                    
                    "Saving comparison results"
                    np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\\Variation\\'+str(File_Var_input), Var_)
                    np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\\Average\\'+str(File_Synced_avg_data_input), Synced_avg_data)
        
        def Altitude_dependence():
            N=int(input("number of locations to plot? :"))
            Var_=[]
            Name_Altitude_Sheilding=[[],[]]
            
            for I in range(0,N):
                Var_file_input=input('Variation file '+str(I+1)+' name? (no file estension) : ')
                Altitude_input=float(int(input("altitude of active detector?"))-84.68)
                Var_file_I=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Actv_V_Ctrl\Variation\\'+str(Var_file_input)+'.npy')
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
            
            Alt_dep=[Grad_v_a,Grad_v_a_err]
            
            np.save(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\settings\Alt_Dep', Alt_dep)

        
        def Var_comp():
            file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Beth plot\\') if x.endswith(".npy")]
            Var_=[]
            "Var_[I] layout [[Var][Time][Var_Err]]"
            
            
            for I in range(0,len(file_list)):
            #       Altitude_input=float(input("altitude of active detector?"))
               Var_file_I=np.load(r''+str(pro_dir)+'\Cosmic Baes Mega Update\Cosmic Baes\program development\Beth plot\\'+str(file_list[I]))
               Var_.append(Var_file_I)
               
            Var_AVG_=[[],[]] #[var avg], [var avg err]
            zero_line=[]
            for i in range(0,len(file_list)):
                Var_AVG_[0].append(float(sum(Var_[i][0]/len(Var_[i][0]))))
                Var_AVG_[1].append((sum((Var_[i][2])**2)/len(Var_[i][2]))**0.5)
                zero_line.append(0)
            
            plt.figure(2)
            plt.figure(figsize=(4,8))
            plt.title('% Variation Avg count rate, relative to control, across different locations')
            #plt.plot(file_list ,Var_AVG_[0], 'o')
            plt.bar(file_list,Var_AVG_[0],width=0.4,color='grey', edgecolor='black',linewidth=1.4,yerr=Var_AVG_[1],capsize=4)
            plt.plot(file_list ,zero_line, 'b:', label='Control detector')
            #plt.errorbar(file_list, Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='grey', capsize=3)
            plt.legend()
            plt.grid(True)
            plt.xlabel('Location code')
            plt.ylabel('% Variation from control')
            plt.show        
            
            Sheild=[]
            for Loc in range(0,len(file_list)):       
                var=((Var_AVG_[0][Loc]/100))
                Mom_s1_I_0=float(0.2)
                Mom_s1_I_Fin=float(40)
                split=int(3980)
                
                I_F=[]
                I_F_ratio=[]
               
                Delta_s1=(Mom_s1_I_Fin-Mom_s1_I_0)/split
                s1=[Mom_s1_I_0]
                
                for Index in range(1, split+1):
                    s1.append(Mom_s1_I_0+Index*Delta_s1)
                
                for Index in range(0,split):
                    result = integrate.quad(lambda p: 2.95*10**-3*p**-(0.3061+1.2743*math.log10(p)-0.2630*(math.log10(p))**2+0.0252*(math.log10(p))**3) , s1[Index],s1[Index+1] )
                    I_F.append(result[0]-result[1])
            
                Flux_tot=sum(I_F)
                
                for Index in range(0,len(I_F)):            
                    I_F_ratio.append(I_F[Index]/Flux_tot)
                
                #def Stopping_Power_Functions():
                Delta_flux_ratio=0
                Index=0
                while Delta_flux_ratio<=np.abs(var):
                    Delta_flux_ratio+=I_F_ratio[Index]
                    #print(Index)
                    Index+=1
                if 0.2 < s1[Index] < 0.4:
                    Stop_Pow=3.97*10**-3
                if 0.4<s1[Index] < 0.8:
                    Stop_Pow=4.05*10**-3
                if 0.8< s1[Index] < 1:
                    Stop_Pow=4.18*10**-3
                if 1< s1[Index] < 1.4:
                    Stop_Pow=4.28*10**-3
                if 1.4<s1[Index] < 2:
                    Stop_Pow=4.41*10**-3
                if 2< s1[Index] < 3:
                    Stop_Pow=4.56*10**-3
                if 3<s1[Index] < 4:
                    Stop_Pow=4.70*10**-3
                if 4<s1[Index] < 8:
                    Stop_Pow=4.92*10**-3
                if 8<s1[Index] < 10:
                    Stop_Pow=5.05*10**-3
                if 10<s1[Index] < 14:
                    Stop_Pow=5.16*10**-3
                if 14<s1[Index] < 20:
                    Stop_Pow=5.29*10**-3
                if 20<s1[Index] < 30:
                    Stop_Pow=5.45*10**-3
                if 30<s1[Index] < 40:
                    Stop_Pow=5.62*10**-3
                PosNeg=-1*np.abs(var)/var
                
                sheilding=(file_list[Loc],PosNeg*s1[Index]/Stop_Pow,' = effective cm of concrete sheilding')
                print(sheilding)
                Sheild.append(sheilding[1])
                print(sheilding)

            plt.figure(2)
            plt.figure(figsize=(8,8))
            plt.title('Estimated concrete sheilding relative to control across locations')
            plt.plot(file_list ,Sheild, 'o')
            plt.plot(file_list ,zero_line, 'b:', label='Control sheilding')
            #plt.errorbar(file_list, Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='grey', capsize=3)
            plt.legend()
            plt.grid(True)
            plt.xlabel('Location code')
            plt.ylabel('Estimated sheilding (CM) ')
            plt.show
            
            
        
        
        
        if Set == 0:
            Settings()
            R_to_start=int(input("select another option?: (Y=1/N=0) "))
            if R_to_start==1:
                Stop=False
            if R_to_start==0:
                Stop=True


        elif Set == 1:
           RawFile_Analysis()
           R_to_start=int(input("select another option?: (Y=1/N=0) "))
           if R_to_start==1:
                Stop=False
           if R_to_start==0:
                Stop=True
        elif Set == 2:
            Actv_Ctrl_Comp()
            R_to_start=int(input("select another option?: (Y=1/N=0) "))
            if R_to_start==1:
                Stop=False
            if R_to_start==0:
                Stop=True
        elif Set == 3:
            Altitude_dependence()
            R_to_start=int(input("select another option?: (Y=1/N=0) "))
            if R_to_start==1:
                Stop=False
            if R_to_start==0:
                Stop=True
        elif Set == 4:
            Var_comp()
            R_to_start=int(input("select another option?: (Y=1/N=0) "))
            if R_to_start==1:
                Stop=False
            if R_to_start==0:
                Stop=True
        