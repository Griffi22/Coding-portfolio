"importing relelvent modules"
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
" i suggest not using default unless you have specified the files you want with the default settings"

def RawFile_Analysis():
    H=int(input("Default settings? (Y=1/N=0):"))
    
    "##User defined values##"
    
    if H==1:
        "number of raw data files to access: user prompt/input"
    
        'input file name entry from raw data folder'
        Rawfile = str(input("name of the raw data file to load? :"))
        'input final name for the processed data file'
        Savefile=str(input("desired name of the processed base data file? :"))
        Savefile_avg=str(input("desired name of the processed data avg file? :"))
        
#        TS_input=str(input("name of the control detector timestamp file? :"))
        
        "R is the variable for how many seconds to average the counts over: user input"
        Avg_num_points=int(input('Number of data points for the average calulation (default = 50) :'))
        
        "the chain decay measure error threshold: user input"
        l=int(input('Error threshold for Chain decay entry length? :'))
    
    # DEFAULT SETTINGS  #
    else:
        Avg_num_points=50
        l=3
        Rawfile='D1_Cali'
        Savefile='\D1_Cali_pro'
        Savefile_avg='\D1_Cali_avg'
#        TS_input=str("D1_a44_p2_TS")
    
    class Data_input:
        "This Raw_Data defines the path taken to the raw data directory and specified file, the +str(D)+ allows for the detector data file defined by the value of n"
        "to be specified as the file name is in the form of (Dntest) where n=the index of the detector"
        "The name of the location the test detector was placed in should be imputed after the +str(n)+ with the first letter capitalised"
        Raw_data = Path(r'C:\Users\griffi22\Downloads\Cosmic Bae analysis 19th Jan Update\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\Caliberation data\\'+str(Rawfile)+'.txt')
        "This opens the file specified by raw data, and adds each entry line of the raw data to a list called (lines)"
        text_file = open(Raw_data, 'r')        
        lines = text_file.readlines()
        
#        TS_path = Path(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_Raw\\'+str(TS_input)+'.txt')
        
#        TS_file = open(TS_path, 'r')
           
#        TS_raw = TS_file.readlines()
    
        "setting up initial global variables and lists for later use"
        
        "the total number of data entries to check"
        y=len(lines)
        r=len(lines)/Avg_num_points
        "starting data entry to read from"
        #print(y)
        x=0
        #5949 'value for Atrium'
        Desync_start = x
        Desync_end = 0
        #1097 'value for atrium'
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
#                T=TS_raw[int(x)]
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
#                    TS.append(T)
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
        #plt.title('detector '+str(n)+' count rate')
        #plt.plot(time, count)
        #plt.errorbar(time, count, yerr=count_err)
        #plt.xlabel('Time (s)')
        #plt.ylabel('Count rate (Hz)')
        #print(Count_AVG)
        #print(Count_AVG_err)
        
        "plot of counts against time averaged over (R) seconds"
        plt.figure(2)
        plt.figure(figsize=(15,7))
        plt.title(''+str(Rawfile)+'detector. count rate AVG over '+str(R)+'s intervals ')
        "limits need to be manually set for best looking plot results, will improve this in future version"
        #plt.ylim(2.25, 4.25)
        
        plt.plot(Time_AVG, Count_AVG,'o', color='black')
        plt.errorbar(Time_AVG, Count_AVG, yerr=Count_AVG_err, fmt=' ', ecolor='grey')
        plt.xlabel('Time (s)')
        plt.ylabel('Count rate AVG (Hz)')
        #plt.ylim(3, 3.90)
        "close the raw data file being accessed"
        text_file.close()
        
        "Save Count_AVG to the directory specified under the name (D(n)_AVG) as an .npy file."
        'lets combine data lists into singular arrays'
        CR_AVG= [Time_AVG, Count_AVG, Count_AVG_err]#, time, count]
        CR = [time, count]
        np.save(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(Savefile_avg), CR_AVG)
        np.save(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(Savefile), CR)
        
        
        "Save Time_AVG to the directory specified under the name (Time(n)_AVG) as an .npy file."
#        np.save(r'C:\Users\based god\Desktop\Cosmic bae project\Cosmic Baes Mega Update\Cosmic Baes\program development\Data_AVG\\'+str(Savefile_avg)+'_TS',TS)
