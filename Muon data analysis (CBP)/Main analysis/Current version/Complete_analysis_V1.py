import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import scipy.integrate as integrate
#import scipy.special as special
import math
                ###complete analysis V1### 

#loading program directory file
pro_dir=np.load('Directory.npy')

class Analysis():
    #while stop is false program continues to run
    Stop=False
    while Stop==False:
        #user selects analysis function in interface menu
        def inputs():
            print("\n Welcome to Complete_analysis,  please choose an option from the following menu.")
            print("(The default order of the anlysis_V1, analysis functions are 1st,2nd,3rd,4th.")
            print("If this is your first time running the program on a device please select 'program settings' and define a program directory before use")
            Selection = int(input("Analysis options: 1=Raw Data Analysis, 2= Active Against Control Comparison \n3=Altitude dependence, 4=Variation comparison across location, 5=Pressure dependance, 0=program settings \n \n(Enter selection using assoiated number): "))
            return(Selection)
        
        #setting the program directory for a device
        def Settings():
            print("Please enter the program directory. This is the directory leading to and including '\Muon data analysis (CBP)' ")
            Program_dir=input("Program directory: ")
            np.save('Directory', Program_dir)
            

        #if program directory file is blank "settings" function is automatically run
        if pro_dir == "#####        'please enter a directory by running the settings function'         #####":
            print("The current program directory is 'None'!")
            Settings()
            pro_dir = np.load('Directory.npy')
            
        #setting a variable for user selected function
        Set=inputs()
        #loading assigning program directory
        pro_dir = np.load('Directory.npy')
        
        #Analysing the raw data format, removes redundent data and error in datasets, corrects countrates for enviromental variables
        def RawFile_Analysis():
            #user selects data sets to be processes, different datasets have different enviromental corrections
            Data_set=int(input("Select a data set: (1=mapping data, 2=pit/ULT, 3=Lead test, 4=Altitude data) "))
            
            if Data_set ==1:
                #specific file extension to access this data set
                set_path='Mapping data'
                #assigns variable to correct for effect of lead sheilding on countrate of active detector    
                pb_coeff=np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\Mapping data\Detector 1\Pb correct\D1 no pb halo count correction.npy')
                print(pb_coeff)
                #The detector number corrisponding to which detector was used 1,2 or 3: required to correct relative effiency corrections
                ADn=3
            elif Data_set ==2:
                #specific file extension to access this data set
                set_path='Non mapping data\Pit v ULT'
                #if no lead sheildnig used set variable to 1
                pb_coeff=1
                #The detector number corrisponding to which detector was used 1,2 or 3: required to correct relative effiency corrections
                ADn=3
            elif Data_set ==3:
                #specific file extension to access this data set
                set_path='Non mapping data\Lead test(D3 = D2)'
                #if no lead sheildnig used set variable to 1
                pb_coeff=1
                #The detector number corrisponding to which detector was used 1,2 or 3: required to correct relative effiency corrections
                ADn=2
            elif Data_set ==4:
                #specific file extension to access this data set
                set_path = "Non mapping data\Altitude dependance"
                #if no lead sheildnig used set variable to 1
                pb_coeff=1
                #The detector number corrisponding to which detector was used 1,2 or 3: required to correct relative effiency corrections
                ADn=3
            #Loading the count rate altitude dependance
            Alt_dep=np.load(r''+str(pro_dir)+'\Main analysis\Current version\settings\Alt_Dep.npy')
            #print(Alt_dep[0],Alt_dep[1])
            #Loading the relative effiency list of the detectors
            Rel_Eff=np.load(r''+str(pro_dir)+'\Main analysis\Current version\settings\D_Rel_Eff.npy')
            
            
            #list of raw timestamp data files in chosen data directory: control detector
            file_list_TS=os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 1\Timestamps\\')            
            file_list_TS.sort()

            #list of raw data files in chosen data directory: control detector
            file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 1\\') if x.endswith(".txt")]
            file_list.sort()
            
            #Control detector data analysis and processing
            #'run num' and 'Index' are both the index of the file being analyise in file_list and file_list_TS
            Run_num=0
            if Run_num < len(file_list):
                print(file_list,file_list_TS)
                for Index in range(0,len(file_list)):
                    #setting save file names to corrispond to the raw data names iwth extentions _pro for processed and _avg for averaged
                    Savefile=str(file_list[Index])[:-4]+'_pro'
                    Savefile_avg=str(file_list[Index])[:-4]+'_avg'
                    #threshold for removing data likely to be due to the decay chain error in the detector
                    Decay_chain_error_threshold=3
                    print('Total files: ',len(file_list),' current file index: ', Run_num )

                    #This Raw_Data defines the path taken to the specified file in the raw data directory
                    Raw_data = Path(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 1\\'+str(file_list[Index]))
                    #This opens the file specified by raw_data, and adds each element (corresponding to a line in the file) of the raw data to a list called 'lines'
                    text_file = open(Raw_data, 'r')        
                    lines = text_file.readlines()
                    
                    #This TS_path defines the path taken to the specified file in the raw data timestamp directory
                    TS_path = Path(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 1\Timestamps\\'+str(file_list_TS[Index]))
                    #This opens the file specified by TS_path, and adds each element (corresponding to a line in the file) of the raw timestamp data to a list called 'TS_raw'
                    TS_file = open(TS_path, 'r')
                    TS_raw = TS_file.readlines()
                
                    #setting up initial variables and lists used later
                    
                    #the total number of data entries to check
                    Tot_ele=len(lines)
                

                    print('Total count entries: ',Tot_ele,', in file', file_list[Index])
                    print('Total count entries: ',len(TS_raw),', in file', file_list_TS[Index])
                    
                    #starting data entry index (ele_i)           
                    ele_i=0
                    
                    #Number of seconds to average count data over (T_avg)
                    T_avg=int(round(len(TS_raw)/(50))) #input("number of seconds to average over?"))

                    #time index at first data read (ts_ele_i)
                    TS_ele_i=0
                    
                    #setting Decay_Chain to initial chain decay streak
                    Decay_Chain=0
                    #index for valid count data list"
                    N=0
                    #sum of counts over T_avg time"
                    C_T_sum=0
                    #TE_avg is the elapsed time in seconds for each entry in the count AVG list starting at entry 1"
                    TE_avg=T_avg
                    
                    #defining our data lists as empty lists
                    
                    # processed count data
                    count=[]
                    count_err=[]
                    # processed average count data
                    Count_AVG=[]
                    Count_AVG_err=[]
                    # Processed timestamp data list [Computer epoch time]
                    TS=[]
                    # Processed timestamp data list [seconds]
                    time=[]    
                    # Processed time entries for AVG count list [seconds]
                    Time_AVG=[]
                                        
                    #Master loop over all raw data entries"
                    while ele_i<Tot_ele:
                    
                            #reading element_i data from count and timestamp lists
                            count_i=int(lines[int(ele_i)])
                            T=TS_raw[int(ele_i)]
                            
                            #chain decay streak calculation"
                            Decay_Chain=0
                            #if count_i<39999 this corrisponds to a decay count element in data
                            if count_i<39999:
                                #setting temp entry index and count variable for forward element checking"
                                ele_i_temp=ele_i
                                count_i_temp=int(lines[int(ele_i_temp)])
                                
                                while count_i_temp<39999:           
                                    ele_i_temp=ele_i_temp+1
                                    count_i_temp=int(lines[int(ele_i_temp)])
                                    #length of decay element chain"
                                    Decay_Chain=Decay_Chain+1
                            #checking is Decay chain is a hardware error
                            if Decay_Chain>Decay_chain_error_threshold-1:
                                #If decay error occurs (defined by Decay_Chain>Decay_chain_error_threshold-1)
                                #skip error data entries in count and timestamp lists
                                ele_i=ele_i+Decay_Chain
                                TS_ele_i=TS_ele_i+1
                            
                            
                            #if data element is non-decay add to count list, entrys with k<40000 are decay data and are redundent for our project
                            if count_i>39999:
                                #appending count_i value to the count list, 40000 is removed as this occurs due to formatting and is not real count data"
                                #multiply by correction coeff's for relative effency of detector and lead effect
                                counttemp=(count_i-40000)*(100/float(Rel_Eff[0][0]))*pb_coeff
                                count.append((count_i-40000)*(100/float(Rel_Eff[0][0]))*pb_coeff)
                                #calculating count err in the case no counts observed count_i=40000
                                if count_i == 40000:
                                    count_err.append(0)

                                #calculating count error with correction coeffs
                                else:
                                    count_err.append(((count_i-40000)**0.5)*(100/float(Rel_Eff[0][0]))*pb_coeff)
                                #adding time element to time lists
                                TS.append(T)
                                time.append(TS_ele_i)
                                TS_ele_i=TS_ele_i+1
                                
                                #increasing valid count list index
                                N=N+1
                            
                                #average count calulator
                                #checking if T_avg time has elapsed between Count_avg calculations
                                if N%T_avg==0 and N != 0:
                                    #C_T_avg, sum of counts in T_avg seconds
                                    for i in range (N-T_avg , N, 1):
                                        C_T_sum=C_T_sum+count[int(i)]
                                    #appending lists for count average and corrisponding time elapsed
                                    Count_AVG.append(C_T_sum/T_avg)
                                    Count_AVG_err.append((C_T_sum**0.5)/T_avg)
                                    Time_AVG.append(TE_avg)
                                    TE_avg=TE_avg+T_avg
                                    #resetting the sum of counts
                                    C_T_sum=0
                                    
                            #move to next data element   
                            ele_i = ele_i+1
                            
                    
                    #plot of counts against time averaged over (T_avg) seconds
                    plt.figure(1)
                    plt.figure(figsize=(8,4))
                    ax = plt.axes()
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
                    plt.title(''+str(file_list[Index])[:-4]+' detector: Count rate AVG over '+str(T_avg)+'s intervals ')
                    plt.tick_params(labelsize=14)
                    plt.plot(Time_AVG, Count_AVG,'o',mfc='firebrick',mec='black')
                    plt.errorbar(Time_AVG, Count_AVG, yerr=Count_AVG_err, fmt=' ', ecolor='black',capsize=3)
                    plt.xlabel('Time (s)', fontsize=18)
                    plt.ylabel('Count rate AVG (Hz)',fontsize=18)
                    plt.show
                    plt.savefig(fname=r''+str(pro_dir)+'\Main analysis\Current version\plots\Count Plots Different Locations\Processed Raw data\\'+str(Savefile_avg))


                    #close the raw data file being accessed
                    text_file.close()
                    #close plotting functions
                    plt.close("all")
                    
                    #Combine data lists into arrays to reduce number of files'
                    CR_AVG= [Time_AVG, Count_AVG, Count_AVG_err]
                    CR = [time, count, count_err]
                    #Save processed and averaged counts to Data_AVG directory as .npy file."                
                    np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Averaged\\'+str(Savefile_avg), CR_AVG)
                    np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\\'+str(Savefile), CR)
                    
                    #saving TS data list as npy file
                    np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Timestamp\\'+str(Savefile_avg)+'_TS',TS)
                    
                    Run_num=Run_num+1
                    
            #Active detector data analysis and processing
            if Run_num >= len(file_list):
                #listing altitude count data files for analysis
                file_list_Alt=os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 3\Altitude (W.R.T, D_Ctrl)\\')
                file_list_Alt.sort()
                #listing active timestamp data files in directory
                file_list_TS=os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 3\Timestamps\\')            
                file_list_TS.sort()
                #listing active detector count data files
                file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 3\\') if x.endswith(".txt")]
                file_list.sort()
                

                #Control detector data analysis and processing

                #'run num' and 'Index' are both the index of the file being analyise in file_list and file_list_TS
                Run_num=0                
                if Run_num < len(file_list):
                    print(file_list,file_list_TS)
                    for Index in range(0,len(file_list)):
                    #setting save file names to corrispond to the raw data names iwth extentions _pro for processed and _avg for averaged
                        Savefile=str(file_list[Index])[:-4]+'_pro'
                        Savefile_avg=str(file_list[Index])[:-4]+'_avg'
                        #threshold for removing data likely to be due to the decay chain error in the detector
                        Decay_chain_error_threshold=3
        
                        #Raw_Data defines the path taken to the specified file in the raw data directory
                        Raw_data = Path(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 3\\'+str(file_list[Index]))
                        #opens the file specified by raw_data, and adds each element (corresponding to a line in the file) of the raw data to a list called 'lines'
                        text_file = open(Raw_data, 'r')        
                        lines = text_file.readlines()
                        
                        #TS_path defines the path taken to the specified file in the raw data timestamp directory
                        TS_path = Path(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 3\Timestamps\\'+str(file_list_TS[Index]))
                        TS_file = open(TS_path, 'r')
                        TS_raw = TS_file.readlines()
                        
                        #Altitude_data defines the path taken to the specified file containing relative altitude of the location
                        Altitude_data = Path(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\\'+str(set_path)+'\Detector 3\Altitude (W.R.T, D_Ctrl)\\'+str(file_list_Alt[Index]))
                        Alt_file= open(Altitude_data, 'r')                        
                        Alt=Alt_file.readlines()
                        
                        
                        #setting up initial variables and lists used later
                        
                        #the total number of data entries to check
                        Tot_ele=len(lines)
                    
                        print('Total count entries: ',Tot_ele,', in file', file_list[Index])
                        print('Total count entries: ',len(TS_raw),', in file', file_list_TS[Index])
                        
                        #starting data entry index (ele_i)           
                        ele_i=0
                        
                        #Number of seconds to average count data over (T_avg)
                        T_avg=int(round(len(TS_raw)/(50))) #input("number of seconds to average over?"))
                        
                        #time index at first data read (ts_ele_i)
                        TS_ele_i=0

                        #setting Decay_Chain to initial chain decay streak
                        Decay_Chain=0
                        #index for valid count data list"
                        N=0
                        #sum of counts over T_avg time"
                        C_T_sum=0
                        #TE_avg is the elapsed time in seconds for each entry in the count AVG list starting at entry 1"
                        TE_avg=T_avg
                        
                        #defining our data lists as empty lists                       
                        # processed count data
                        count=[]
                        count_err=[]
                        # processed average count data
                        Count_AVG=[]
                        Count_AVG_err=[]
                        # Processed timestamp data list [Computer epoch time]
                        TS=[]
                        # Processed timestamp data list [seconds]
                        time=[]    
                        # Processed time entries for AVG count list [seconds]
                        Time_AVG=[]
                                            
                        #master loop over all raw entries in file
                        while ele_i<Tot_ele:
                        
                                #reading element_i data from count and timestamp lists
                                count_i=int(lines[int(ele_i)])
                                T=TS_raw[int(ele_i)]
                                
                                #chain decay streak calculation"
                                Decay_Chain=0
                                #if count_i<39999 this corrisponds to a decay count element in data
                                if count_i<39999:
                                    #setting temp entry index and count variable for forward element checking"
                                    ele_i_temp=ele_i
                                    count_i_temp=int(lines[int(ele_i_temp)])
                                    
                                    while count_i_temp<39999:           
                                        ele_i_temp=ele_i_temp+1
                                        count_i_temp=int(lines[int(ele_i_temp)])
                                        #length of decay element chain"
                                        Decay_Chain=Decay_Chain+1
                                #checking is Decay chain is a hardware error
                                if Decay_Chain>Decay_chain_error_threshold-1:
                                    #If decay error occurs (defined by Decay_Chain>Decay_chain_error_threshold-1)
                                    #skip error data entries in count and timestamp lists
                                    ele_i=ele_i+Decay_Chain
                                    TS_ele_i=TS_ele_i+1
                                    
                                #if data element is non-decay add to count list, entries with count_i<40000 are decay data and are redundent for our project
                                if count_i>39999:
                                    #appending count_i value to the count list, 40000 is removed as this occurs due to formatting and is not real count data"
                                    #multiply by correction coeff's for relative effency of detector and location's relative altitude
                                    counttemp=(count_i-40000)*(100/float(Rel_Eff[0][ADn-1]))*(1-(float(Alt[0])*(float(Alt_dep[0])/100)))
                                    count.append((count_i-40000)*(100/float(Rel_Eff[0][ADn-1]))*(1-(float(Alt[0])*(float(Alt_dep[0])/100))))
                                    #calculating count err in the case no counts observed count_i=40000
                                    if count_i==40000:
                                        count_err.append(0)
                                        
                                    #calculating count error with correction coeffs
                                    else:
                                        count_err.append(counttemp*( ((count_i-40000)**0.5/(count_i-40000))**2+(float(Rel_Eff[1][ADn-1])/float(Rel_Eff[0][ADn-1]))**2+(float(Alt_dep[1])/float(Alt_dep[0]))**2)**0.5) #+ (float(Alt_dep[1])/float(Alt_dep[0]))**2
                                    #adding time element to time lists
                                    TS.append(T)
                                    time.append(TS_ele_i)
                                    TS_ele_i=TS_ele_i+1
                                    
                                    #increasing valid count list index
                                    N=N+1

                                    #average count calulator
                                    #checking if T_avg time has elapsed between Count_avg calculations
                                    if N%T_avg==0 and N != 0:
                                        #C_T_avg, sum of counts in T_avg seconds
                                        for i in range (N-T_avg , N, 1):
                                            C_T_sum=C_T_sum+count[int(i)]
                                        #appending lists for count average and corrisponding time elapsed
                                        Count_AVG.append(C_T_sum/T_avg)
                                        Count_AVG_err.append((C_T_sum**0.5)/T_avg)
                                        Time_AVG.append(TE_avg)
                                        TE_avg=TE_avg+T_avg
                                        #resetting the sum of counts
                                        C_T_sum=0
                                        
                                #move to next data element   
                                ele_i = ele_i+1
                                

                        #plot of counts against time averaged over (T_avg ) seconds
                        plt.figure(2)
                        plt.figure(figsize=(8,4))
                        ax = plt.axes()
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
                        plt.tick_params(labelsize=14)
                        plt.title(''+str(file_list[Index])[:-4]+' detector: Count rate AVG over '+str(T_avg)+'s intervals ')
                        #plt.ylim(2.25, 4.25)
                        plt.plot(Time_AVG, Count_AVG,'o',mfc='firebrick',mec='black')
                        plt.errorbar(Time_AVG, Count_AVG, yerr=Count_AVG_err, fmt=' ', ecolor='black',capsize=3)
                        plt.xlabel('Time (s)',fontsize=18)
                        plt.ylabel('Count rate AVG (Hz)',fontsize=18)
                        #plt.ylim(3, 3.90)
                        plt.savefig(fname=r''+str(pro_dir)+'\Main analysis\Current version\plots\Count Plots Different Locations\Processed Raw data\\'+str(Savefile_avg))

                        #close the raw data file being accessed
                        text_file.close()
                        #close plotting functions
                        plt.close("all")
                        
                        #Combine data lists into arrays to reduce number of files'
                        CR_AVG= [Time_AVG, Count_AVG, Count_AVG_err]#, time, count]
                        CR = [time, count, count_err]

                        #Save processed and averaged counts to Data_AVG directory as .npy file."                
                        np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Averaged\\'+str(Savefile_avg), CR_AVG)
                        np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 3\Processed\\'+str(Savefile), CR)
                        
                        
                        #saving TS data list as npy file
                        np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 3\Timestamp\\'+str(Savefile_avg)+'_TS',TS)
                        Run_num=Run_num+1
            print("Processed data and plots of results are now saved to data_AVG and plots folders")
            
                
        
        
        
        
        
        #Active vs control detector data comparison
        #loading the processed control and active detector data'
        def Actv_Ctrl_Comp():
                #listing processed control and active count data files in Data_AVG directory
                file_list_Ctrl = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\\') if x.endswith(".npy")]
                file_list_Actv = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 3\Processed\\') if x.endswith(".npy")]
                #listing control and active timestamp data files in Data_AVG directory
                file_list_Ctrl_TS = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Timestamp\\') if x.endswith(".npy")]
                file_list_Actv_TS = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 3\Timestamp\\') if x.endswith(".npy")]
                #sorting file lists
                file_list_Ctrl.sort()
                file_list_Actv.sort()
                file_list_Ctrl_TS.sort()
                file_list_Actv_TS.sort()
                #Main loop over all location codes
                for i in range(0,len(file_list_Ctrl)):
                                       
                    print(file_list_Ctrl[i][:-4], file_list_Actv[i][:-4])
                    #setting save files names and plot titles to D_'location code'_avg and  D_'location code'_var
                    File_Synced_avg_data_input='D_'+str(file_list_Ctrl[i][3:-8])+'_avg'
                    File_Var_input='D_'+str(file_list_Ctrl[i][3:-8])+'_var'
                    
                    #loading processed count data files for comparision
                    D_pro_Ctrl = np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\\'+str(file_list_Ctrl[i][:-4])+'.npy')
                    D_pro_Actv = np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 3\Processed\\'+str(file_list_Actv[i][:-4])+'.npy')
                                    
                    #loading processed time data files for comparision                    
                    TS_Ctrl=np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Timestamp\\'+str(file_list_Ctrl_TS[i][:-4])+'.npy')
                    TS_Actv=np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 3\Timestamp\\'+str(file_list_Actv_TS[i][:-4])+'.npy')
                    
                    #Correcting the initial and final measurment desync of the detectors data, count data must be simulatainious
                    #timestamp value for first element
                    TS_Ctrl_pos_i=int(TS_Ctrl[0])
                    TS_Actv_pos_i=int(TS_Actv[0])
                    #creating lists for synced data avg
                    D_A_C_c=[]
                    D_A_A_c=[]
                    D_A_C_c_Err=[]
                    D_A_A_c_Err=[]
                    
                    #calcuating initial desync of measurments
                    if TS_Ctrl_pos_i>TS_Actv_pos_i:
                        desync_i =TS_Ctrl_pos_i - TS_Actv_pos_i 
                    if TS_Ctrl_pos_i<=TS_Actv_pos_i:
                        desync_i = TS_Actv_pos_i - TS_Ctrl_pos_i
                    
                    #timestamp value for final element
                    TS_Ctrl_pos_f=int(TS_Ctrl[len(TS_Ctrl)-1])
                    TS_Actv_pos_f=int(TS_Actv[len(TS_Actv)-1])
                    
                    #calcuating final desync of measurments
                    if TS_Ctrl_pos_f>TS_Actv_pos_f:
                        desync_f = TS_Ctrl_pos_f - TS_Actv_pos_f 
                    if TS_Ctrl_pos_f<=TS_Actv_pos_f:
                        desync_f = TS_Actv_pos_f - TS_Ctrl_pos_f
                    #printing length of each data set before syncing
                    print(len(D_pro_Ctrl[1]), "Length of control(D1) data")
                    print(len(D_pro_Actv[1]),"Length of active(D3) data")
                    
                    #syncing data
                    
                    #initial allignment
                    #if control detector starts earlier:
                    if TS_Ctrl_pos_i<=TS_Actv_pos_i:
                        #create control data list D_A_C_c and append all processed control data after initial desync value.
                        for Index in range(0, len(D_pro_Ctrl[1])-desync_i):    
                            D_A_C_c.append(D_pro_Ctrl[1][Index+desync_i-1])
                            D_A_C_c_Err.append(D_pro_Ctrl[2][Index+desync_i-2])
                        #create active data list D_A_A_c and append all processed active data.
                        for Index in range(0,len(D_pro_Actv[1])):
                            D_A_A_c.append(D_pro_Actv[1][Index])
                            D_A_A_c_Err.append(D_pro_Actv[2][Index])
                            
                    #if active detector starts earlier:
                    if TS_Ctrl_pos_i>TS_Actv_pos_i:
                        #create active data list D_A_A_c and append all processed active after initial desync value.
                        for Index in range(0,len(D_pro_Actv[1])-desync_i):
                            D_A_A_c.append(D_pro_Actv[1][Index+desync_i-1])
                            D_A_A_c_Err.append(D_pro_Actv[2][Index+desync_i])
                        #create control data list D_A_C_c and append all processed control data.
                        for Index in range(0,len(D_pro_Ctrl[1])):
                            D_A_C_c.append(D_pro_Ctrl[1][Index])
                            D_A_C_c_Err.append(D_pro_Ctrl[2][Index])
                    
                    #final allignment
                    #if control detector measurments finish later:
                    if TS_Ctrl_pos_f>TS_Actv_pos_f:
                        
                        for Index in range(0, desync_f):
                            #deleting last element of control list repeatedly until final timestamps are alligned'   
                            del D_A_C_c[len(D_A_C_c)-1]
                            del D_A_C_c_Err[len(D_A_C_c_Err)-1]
                    #if active detector measurment finish later:
                    if TS_Ctrl_pos_f<=TS_Actv_pos_f:
                        for Index in range(0, desync_f):
                            #deleting last element of control list repeatedly until final timestamps are alligned'   
                            del D_A_A_c[len(D_A_A_c)-1]
                            del D_A_A_c_Err[len(D_A_A_c_Err)-1]
                            
                    #control and active data is now approximately synced (decay data removal may cause minor desyncing)"
                    print('Synced Active dataset length ',len(D_A_A_c),', Synced Control dataset length ',len(D_A_C_c))
                    
                    #averaging the now synced data sets
                    #R=time to average counts over
                    R=int(len(D_pro_Actv[1])/50)
                    
                    #loop to reduce repetative code
                    for D in range(0,2):
                        #setting variables
                        #index of count element in data
                        index=0
                        #lists for count average over R, and the error.
                        C_AVG=[]
                        C_AVG_Err=[]
                        #Time elapsed.
                        TE_index=0
                        #List of the time elapsed at each entry in C_AVG
                        TE_AVG=[]
                        #total counts over R time
                        C_sum=0
                        #Error in C_sum
                        C_Err_sum=0
                        #iteration one sets values for Active data averaging
                        if D==1:
                            count=D_A_A_c
                            count_Err=D_A_A_c_Err
                            Loop_len=len(D_A_A_c)
                        #iteration zero sets values for control data averaging
                        if D==0:
                            count=D_A_C_c
                            count_Err=D_A_C_c_Err
                            Loop_len=len(D_A_C_c)
                            
                        #looping over all entries in set data
                        while index<Loop_len:
                             #check if R time has elapsed since last calculation
                             if index%R==0:
                                 for i in range (index-R , index+1):
                                     #sum of counts in time R
                                     C_sum += count[i]
                                     C_Err_sum+=count_Err[i]
                                 #average counts over period R    
                                 C_AVG.append(C_sum/R)
                                 C_AVG_Err.append((C_Err_sum/R))
                                 #Recording timeelapsed for C_AVG element
                                 TE_AVG.append(TE_index)
                                 #Increasing time elapsed to next AVG point
                                 TE_index += int(R)
                                 #resetting sums
                                 C_sum=0
                                 C_Err_sum=0
                             index += 1         
                        #assigning active and control detectors the corrisponding avg lists
                        if D==1:
                            D_A_C_avg=C_AVG
                            D_A_C_avg_err=C_AVG_Err
                            TE_A_C_avg=TE_AVG
                        if D==0:
                            D_C_C_avg=C_AVG
                            D_C_C_avg_err=C_AVG_Err
                            TE_C_C_avg=TE_AVG
                    
                    #generating plots of results
                    plt.figure(3)
                    plt.figure(figsize=(8,4))
                    ax = plt.axes()
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
                    plt.tick_params(labelsize=14)
                    plt.title('Active v control: '+str(File_Synced_avg_data_input)[2:-4]+' countrate averaged over '+str(R)+' sec')
                    plt.plot(TE_C_C_avg, D_C_C_avg,'o:', label='Control detector',mfc='firebrick',mec='black',lw=2)
                    plt.errorbar(TE_C_C_avg, D_C_C_avg, yerr=D_C_C_avg_err, fmt=' ', ecolor='black', capsize=3)
                    plt.plot(TE_A_C_avg, D_A_C_avg,'o-',color='seagreen', label='Active detector',mfc='firebrick',mec='black',lw=2,marker="s")
                    plt.errorbar(TE_A_C_avg, D_A_C_avg, yerr=D_A_C_avg_err, fmt=' ', ecolor='black', capsize=3)
                    plt.legend()
                    plt.xlabel('Time elapsed (s)',fontsize=18)
                    plt.ylabel('Average count rate (Hz)',fontsize=18)
                    #Save plots
                    plt.savefig(fname=r""+str(pro_dir)+"\Main analysis\Current version\plots\Count Plots Different Locations\Synced Actv Vs Ctrl detector data\\"+str(File_Synced_avg_data_input))
                    plt.close('all')
                    
                    
                    
                    #Calculate the percentage variation of active data against the control

                    
                    Var_=[[],[],[]]#'[%Var][Time][%VAR_err]'
                    print(len(D_C_C_avg), "D_C_C_avg",len(D_A_C_avg),"D_A_C_avg")
                    
                    #removing any desync from averaging, same method as previously:
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
                    
                    #combining averaged data into array
                    Synced_avg_data=[D_A_C_avg,[D_C_C_avg]]
                    index_non_zero=0
#                   if len(D_C_C_avg)>len(D_A_C_avg):
                    for Index in range(0,len(D_C_C_avg)-1):
                        #condition to avoid math errors
                        if D_C_C_avg[Index]!=0.0:
                            #perentage variation of active avg count W.R.T control avg count
                            Var_[0].append(100*((D_A_C_avg[Index]-D_C_C_avg[Index]))/D_C_C_avg[Index])
                            #Time elapsed list corrisponding to count AVG list
                            Var_[1].append(TE_C_C_avg[Index])
                            #Error in percentage variation
                            Var_[2].append(Var_[0][index_non_zero]*((D_A_C_avg_err[Index]/D_A_C_avg[Index])**2+(D_C_C_avg_err[Index]/D_A_C_avg[Index])**2)**0.5)
                            index_non_zero+=1
                    index_non_zero=0

                    #Plotting percentage variation results
                    plt.figure(4)
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
                    ax.tick_params(axis='both', colors='black')
                    plt.tick_params(labelsize=14)
                    plt.grid(True,color='grey',linestyle='--')
                    plt.title('% Variation of '+str(File_Synced_avg_data_input)[2:-4]+', W.R.T control, averaged over ' +str(R)+ ' sec')
                    plt.plot(Var_[1],Var_[0],'o-', color='seagreen', mfc='firebrick',mec='black', lw=2,label='% Variation')
                    plt.errorbar(Var_[1], Var_[0], yerr=Var_[2] , fmt=' ', ecolor='black', capsize=3)
                    plt.legend()
                    plt.xlabel('Time elapsed (s)',fontsize=18)
                    plt.ylabel('% Variation',fontsize=18)
                    plt.savefig(fname=r''+str(pro_dir)+'\Main analysis\Current version\plots\Count Plots Different Locations\Synced Actv Vs Ctrl detector data\\'+str(File_Var_input))
                    plt.show
                    plt.close('all')
                    
                    #Saving comparison results"
                    np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_Actv_V_Ctrl\\Variation\\'+str(File_Var_input), Var_)
                    np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_Actv_V_Ctrl\\Average\\'+str(File_Synced_avg_data_input), Synced_avg_data)
                print('Comparison complete: data for synced countrates and %countrate variation is saved to Data_Actv_V_Ctrl directory.')
                print('Plots are available in Plots directory')
                
                
        #Calculations of muon Flux altitude dependance. (Needs automating)       
        def Altitude_dependence():
            #user input for number of locations in altitude dependance calculation
            N=int(input("number of locations? :"))
            #list for count rate variation for each location
            Var_=[]
            #list for location code and altitude data of each location
            Name_Altitude=[[],[]]
            #appending location data to lists
            for I in range(0,N):
                #user input of var file name without file extension
                Var_file_input=input('Variation file '+str(I+1)+' name? (no file estension) : ')
                Var_file_I=np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_Actv_V_Ctrl\Variation\\'+str(Var_file_input)+'.npy')
                Var_.append(Var_file_I)
                #Altitude of location relative to sea level, corrected for control altitude
                Altitude_input=float(int(input("altitude of active detector?"))-84.68)
                Name_Altitude[0].append(Var_file_input)
                Name_Altitude[1].append(Altitude_input)
                
            print(Var_[1][2][1],Name_Altitude[0][1])
            "Var_ layout [[Var_H],[Var_A],[Var_O]]"
            "Var_[I] layout [[Var][Time][Var_Err]]"
            #plot of variation in each location W.R.T control over time
            plt.figure(5)
            plt.figure(figsize=(16,8))
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
            
            plt.tick_params(labelsize=14)
            ax.xaxis.label.set_color('black')
            ax.yaxis.label.set_color('black')
            ax.tick_params(axis='both', colors='black')
            plt.grid(True,color='grey',linestyle='--')
            #plt.title('% Variation Avg count rate relative to control across different locations')
            for I in range(0,N):
                plt.plot(Var_[I][1],Var_[I][0], label=str(Name_Altitude[0][I])[:-4])
                plt.errorbar(Var_[I][1], Var_[I][0], yerr=Var_[I][2] , fmt=' ', ecolor='black', capsize=3)
            plt.legend()
            plt.xlabel('Time elapsed (s)',fontsize=18)
            plt.ylabel('% Variation',fontsize=18)
            plt.show
            
            #calcuating the avg variation over measurment and average variation error
            Var_AVG_=[[],[]] 
            "Var avg, VAR avg_Err"
            for i in range(0,N):
                Var_AVG_[0].append(float(sum(Var_[i][0]/len(Var_[i][0]))))
                Var_AVG_[1].append((sum((Var_[i][2]**2)**0.5)/len(Var_[i][2])))
            #plotting the average variation against altitude
            plt.figure(6)
            plt.figure(figsize=(14,7))
            #plt.title('% Variation Avg count rate relative to control against altitude across different locations')
            plt.plot(Name_Altitude[1],Var_AVG_[0])
            plt.errorbar(Name_Altitude[1], Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='grey', capsize=3)
            plt.xlabel('Altitude W.R.T D1 (m)',fontsize=18)
            plt.ylabel('% Variation from control',fontsize=18)
            plt.show
            #calculatng the gradient of average variation in count rate against altitude
            Grad_v_a=((Var_AVG_[0][len(Var_AVG_[0])-1]-Var_AVG_[0][0])/(Name_Altitude[1][len(Name_Altitude[1])-1]-Name_Altitude[1][0]))
            Grad_v_a_err=((((Var_AVG_[0][len(Var_AVG_[0])-1]+Var_AVG_[1][len(Var_AVG_[0])-1]-Var_AVG_[0][0]-Var_AVG_[1][0])/(Name_Altitude[1][len(Name_Altitude[1])-1]-Name_Altitude[1][0]))-Grad_v_a)**2)**0.5
        
            print('Gradient_Variation against relative altitude from D1=' ,Grad_v_a,'+/-',Grad_v_a_err,' %/Meter')
            
            Alt_dep=[Grad_v_a,Grad_v_a_err]
            #saving countrate altitude dependance
            np.save(r''+str(pro_dir)+'\Main analysis\Current version\settings\Alt_Dep', Alt_dep)


        #calculating the pressure dependance
        def Pressure_comp():
            #listing averaged control data files 
            file_list = [x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\pressure comp file\\') if x.endswith(".npy")]
            #listing pressure data files
            Pressure_list=[x for x in os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\pressure comp file\pressure\\') if x.endswith(".txt")]
            #setting lists for Average pressure over measurement, average count rate of control detector, and the location code
            Avg_pres=[]
            Avg_ctrl=[[],[]]
            Loc_list=[]
            #loop over all locations
            for i in range(0,len(file_list)):
                #loading and opening count rate data file
                CR_data=np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\pressure comp file\\'+str(file_list[i]))
                #loading and opening Pressure data file
                P_path = Path(r''+str(pro_dir)+'\Main analysis\Current version\Data_AVG\Detector 1\Processed\pressure comp file\pressure\\'+str(Pressure_list[i]))
                P_file = open(P_path, 'r')
                pressure_I = P_file.readlines()
                #assigning location code name to list
                Loc_list.append(str(file_list[i])[3:-8])
                #Calculating the average count rate over entire measurement and the error
                Avg_ctrl[0].append(float(sum(CR_data[1])/len(CR_data[1])))
                Avg_ctrl[1].append((sum((CR_data[2]**2))**0.5/len(CR_data[1])))
                #assigning the average pressure over measurement
                Avg_pres.append(float(pressure_I[0]))
            #numpy functions for calculating the gradient
            coef = np.polyfit(Avg_pres,Avg_ctrl[0],1)
            poly1d_fn = np.poly1d(coef)
            #Gradient calculation
            Gradient=(poly1d_fn(Avg_pres)[len(poly1d_fn(Avg_pres))-1]-poly1d_fn(Avg_pres)[0])/(Avg_pres[len(Avg_pres)-1]-Avg_pres[0])
            print(Gradient," [countrate/mBar]")
            #plotting average countrate of control against pressure for each locations measurement
            plt.figure(7)
            plt.figure(figsize=(16,8))
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
            plt.tick_params(labelsize=14)                    
            plt.grid(True,color='grey',linestyle='--')
            plt.title('Average control countrate against atmopsheric pressure')
            
            plt.plot(Avg_pres ,Avg_ctrl[0],'o', mfc='firebrick',mec='black', lw=2)
            plt.plot(Avg_pres,Avg_ctrl[0], ' ', Avg_pres, poly1d_fn(Avg_pres), '--b',label="Linear fit")
            for i in range(0,len(Loc_list)):
                plt.text(Avg_pres[i]+0.15+0.07*i, Avg_ctrl[0][i]+0.01+0.002*i,'('+str(Loc_list[i])+')',fontsize=8)
            plt.text(Avg_pres[0]+0.7,Avg_ctrl[0][0]+0.08,'Gradient = '+str(round(Gradient,4))+'[Countrate/mBar]',fontsize=16)
            plt.errorbar(Avg_pres, Avg_ctrl[0], yerr=Avg_ctrl[1] , fmt=' ', ecolor='black', capsize=3)
            plt.legend()
            plt.xlabel('Pressure (mBar)',fontsize=18)
            plt.ylabel('Average Countrate (Hz)',fontsize=18)
            plt.show      
            #saving plot for later use
            plt.savefig(fname=r''+str(pro_dir)+'\Main analysis\Current version\plots\Count Plots Different Locations\\Countrate against Pressure')

        #calculating the estimated sheilding (Need to add dynamic stopping power as muon looses KE?)
        def Var_comp():
            #listing all the locations variation files
            file_list=os.listdir(r''+str(pro_dir)+'\Main analysis\Current version\Data_Actv_V_Ctrl\Variation\\')
            #setting list for variation data from each location
            Var_=[]
            "Var_[I] layout [[Var][Time][Var_Err]]"
            
            #appending the variation data for each location
            for I in range(0,len(file_list)):
               Var_file_I=np.load(r''+str(pro_dir)+'\Main analysis\Current version\Data_Actv_V_Ctrl\Variation\\'+str(file_list[I]))
               Var_.append(Var_file_I)
            #list of average variation over measurement for each location and its error
            Var_AVG_=[[],[]] #[var avg], [var avg err]
            #list to show zero variation on plot
            zero_line=[]
            #appending average variation of each location to Var_AVG list and the error in each variation average
            for i in range(0,len(file_list)):
                Var_AVG_[0].append(float(sum(Var_[i][0]/len(Var_[i][0]))))
                Var_AVG_[1].append((sum((Var_[i][2]**2)**0.5)/len(Var_[i][2])))
                zero_line.append(0)
            
            
            
            
            #Calculating the effect of the lead sheilding being applied to the active detector (adding lead halo to one detector but not both seems pointless? i just have to undo its effect)
            for i in range(0,len(file_list)):
                #only loads the lead variation data file
                if file_list[i] == "D_pb_var.npy":
                    print(Var_AVG_[0])
                    #lead correction coeff
                    pb_var=(1+float(Var_AVG_[0][i])/100)
            #saving coeff
            np.save(r''+str(pro_dir)+'\Main analysis\Current version\Data_Raw\Mapping data\Detector 1\Pb correct\\D1 no pb halo count correction', pb_var)
            
            #location code list for plotting data
            Loc_list=[]
            for i in range(0,len(file_list)):
                Loc_list.append(str(file_list[i])[2:-8])
            #User inputs the correction modifiers that have been applied, this adds them to the save names of data and plots 
            saveinput="Variation across all loc ("+str(input("Correction modifiers used in analysis? (for file naming purposes) 'Rel_Eff''Pb sheilding''altitude', default is 'all': "))+")"
            #plotting the variation W.R.T control, averaged over measurment, accross all locations.
            plt.figure(8)
            plt.figure(figsize=(16,8))
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
            plt.tick_params(labelsize=14)                    

            plt.grid(True,color='grey',linestyle='--')
            plt.title('% Variation Avg count rate (relative to control) across different locations')
            plt.plot(Loc_list ,Var_AVG_[0],'o', mfc='firebrick',mec='black', lw=2)
            for i in range(0,len(Loc_list)):
                plt.text(str(Loc_list[i]), Var_AVG_[0][i]+1,'('+str(round(Var_AVG_[0][i]))+'%)',fontsize=9)
            
            plt.plot(Loc_list ,zero_line, 'b:', label='Control detector')
            plt.errorbar(Loc_list, Var_AVG_[0], yerr=Var_AVG_[1] , fmt=' ', ecolor='black', capsize=3)
            plt.legend()
            plt.xlabel('Location code',fontsize=18)
            plt.ylabel('% Variation from control',fontsize=18)
            plt.show        
            #saving plots
            plt.savefig(fname=r''+str(pro_dir)+'\Main analysis\Current version\plots\Count Plots Different Locations\Var across all locations\Final version\\'+str(saveinput))
            
            
            #list for estimated sheilding of each location and the error
            Sheild=[[],[]]
            #loop over all locations
            for Loc in range(0,len(file_list)):
                #Variation ratio of location and the error
                var=[[((Var_AVG_[0][Loc]/100))],[((Var_AVG_[1][Loc]/100))]]
                #min muon momentum threshold
                Muon_mom_min=float(0.2)
                #Max muon momentum aborbed by sheilding
                Muon_mom_max=float(800)
                #splitting the momentum range into 1/100GeV steps
                split=int((Muon_mom_max-Muon_mom_min)*100)
                #1/100GeV momentum step
                Delta_mom=(1/100)
                
                #muon momentum range list minimum value
                Mom_range=[Muon_mom_min]
                #filling Muon momentum range up to Max muon momentum value
                for Index in range(1, split+1):
                    Mom_range.append(Muon_mom_min+Index*Delta_mom)
                
                #list for integrated muon flux
                I_F=[]
                #list for integrated muon flux ratios at different momentum ranges
                I_F_ratio=[]
                #Calcuating the integral muon Flux for each Delta_mom step in the muon momentum range Mom_range
                for Index in range(0,split):
                    result = integrate.quad(lambda p: 2.95*10**-3*p**-(0.3061+1.2743*math.log10(p)-0.2630*(math.log10(p))**2+0.0252*(math.log10(p))**3) , Mom_range[Index],Mom_range[Index+1] )
                    I_F.append(result[0]-result[1])
                #total flux over momentum range
                Flux_tot=sum(I_F)
                #calculating the ratio of the integral flux at each momentum step.
                for Index in range(0,len(I_F)):            
                    I_F_ratio.append(I_F[Index]/Flux_tot)
                #Delta_flux_ratio is the sum of integrated flux ratios up to the count rate variation observed
                Delta_flux_ratio=0
                Delta_flux_ratio_Err=0
                #Index is how many momentum steps the Delta_flux_ratio goes through before reaching the variation ratio observed 
                Index=0
                Index_Err=1
                #calcuating the momentum range absorbed in the variation observed 
                while Delta_flux_ratio<=np.abs(var[0]):
                    Delta_flux_ratio+=I_F_ratio[Index]
                    Index+=1
                while Delta_flux_ratio_Err<np.abs(var[1]):
                    Delta_flux_ratio_Err+=I_F_ratio[Index+Index_Err]
                    Index_Err+=1
                #calculating the stopping power value of concrete to use for the momentum range absorbed to explain the drop in variation observed (GeV/cm)
                if 0.2 < Mom_range[Index] < 0.4:
                    Stop_Pow=3.97*10**-3
                if 0.4<Mom_range[Index] < 0.8:
                    Stop_Pow=4.05*10**-3
                if 0.8< Mom_range[Index] < 1:
                    Stop_Pow=4.18*10**-3
                if 1< Mom_range[Index] < 1.4:
                    Stop_Pow=4.28*10**-3
                if 1.4<Mom_range[Index] < 2:
                    Stop_Pow=4.41*10**-3
                if 2< Mom_range[Index] < 3:
                    Stop_Pow=4.56*10**-3
                if 3<Mom_range[Index] < 4:
                    Stop_Pow=4.70*10**-3
                if 4<Mom_range[Index] < 8:
                    Stop_Pow=4.92*10**-3
                if 8<Mom_range[Index] < 10:
                    Stop_Pow=5.05*10**-3
                if 10<Mom_range[Index] < 14:
                    Stop_Pow=5.16*10**-3
                if 14<Mom_range[Index] < 20:
                    Stop_Pow=5.29*10**-3
                if 20<Mom_range[Index] < 30:
                    Stop_Pow=5.45*10**-3
                if 30<Mom_range[Index] < 40:
                    Stop_Pow=5.62*10**-3
                if 40<Mom_range[Index] < 80:
                    Stop_Pow=5.93*10**-3
                if 80<Mom_range[Index] < 100:
                    Stop_Pow=6.28*10**-3                
                if 100<Mom_range[Index] < 140:
                    Stop_Pow=6.59*10**-3
                if 140<Mom_range[Index] < 200:
                    Stop_Pow=7.09*10**-3
                if 200<Mom_range[Index] < 300:
                    Stop_Pow=7.88*10**-3
                if 300<Mom_range[Index] < 400:
                    Stop_Pow=8.86*10**-3
                if 400<Mom_range[Index] < 700:
                    Stop_Pow=10.8*10**-3
                if 700<Mom_range[Index] < 800:
                    Stop_Pow=12.8*10**-3

                #converting negative/positive variation into positive/negative sheilding.
                PosNeg=-1*np.abs(var[0])/var[0]
                #calculating the sheilding depth required to stop muons with Mom_range[Index] momentum
                sheilding=(file_list[Loc],PosNeg*Mom_range[Index]/Stop_Pow,' = effective cm of concrete sheilding')
                #sheilding error calculation
                Sheilding_Err=(file_list[Loc],(Mom_range[Index+Index_Err]-Mom_range[Index])/Stop_Pow, '= +- effective cm of concrete sheilding Error')
                print(sheilding,Sheilding_Err)
                #appending result for location to the sheild list
                Sheild[0].append(sheilding[1])
                Sheild[1].append(Sheilding_Err[1])
                
            #User inputs corrections modifers applied such as relative effiency of detectors altitude detendance etc
            #used for plot titles and save names of files
            saveinput="Shielding across all loc ("+str(input("Correction modifiers used in analysis? (for file naming purposes) 'Rel_Eff''Pb sheilding''altitude', default is 'all': "))+")"
            
            #plotting final results of sheilding estimations
            plt.figure(9)
            plt.figure(figsize=(16,8))
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
            plt.tick_params(labelsize=14)
            plt.grid(True,color='grey',linestyle='--')
            plt.plot(Loc_list ,Sheild[0],'o', mfc='firebrick',mec='black', lw=2)
            for i in range(0,len(Loc_list)):
                plt.text(str(Loc_list[i]), Sheild[0][i]+6,'('+str(int((Sheild[0][i])))+'cm)',fontsize=9)
            plt.plot(Loc_list ,zero_line, 'b:', label='Control sheilding')
            plt.errorbar(Loc_list, Sheild[0], yerr=Sheild[1] , fmt=' ', ecolor='black', capsize=3)
            plt.legend(fontsize=10)
            plt.xlabel('Location code',fontsize=18)
            plt.ylabel('Estimated shielding (CM) ', fontsize=18)
            plt.show
            #saving plot
            plt.savefig(fname=r''+str(pro_dir)+'\Main analysis\Current version\plots\Count Plots Different Locations\Sheilding across all locations\\'+str(saveinput))

            
            
            
        #User selected function input being converted to calling the functions
        #additional choice to select another function after previous choice is complete
        #if no further choice selected program loop terminates, Stop=True
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
        elif Set == 5:
            Pressure_comp()
            R_to_start=int(input("select another option?: (Y=1/N=0) "))
            if R_to_start==1:
                Stop=False
            if R_to_start==0:
                Stop=True
                
        