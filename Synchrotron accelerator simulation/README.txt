Computational model(Synchrotron particle accelerator): User guide.


*ALL VALUES USED ARE IN SI UNITS*

Basics of running the simulation:
	In order to use main simulation, run Simulator.py in your IDE (coded in spyder so this is suggested IDE)
	
	Enter timestep in terminal once promted.(reccomended values are suggested)
	 
	Enter simulation time in terminal once promted.(reccomended values are suggested)

	Select Particle to simulate from list, this is case sensitive. (reccomended values are suggested)

	Once simulation is complete the relevant data will be saved to a csv file named "ParticleData.csv",
	 this file is likely located in the "PA" folder directory.

	Plots of the simulation will appear in either the terminal of your IDE or as pop up windows. 
	these plots can be saved using the save icon in the pop up window or by right clicking
	 and selecting the save image in the terminal.

Using the Test functions:
	Open Test_PA.py in your prefered IDE and click run file button.

	Select premade tests once prompted by entering the number corridponding to test into the terminal.

	Results of the test will display in the terminal onces calculations are complete.

Changing the non-user defined variables (not reccomended):
	initial particle position:
		Open Particle_list.py in editer, on line 18 edit the Pos_start values.
		(reccomended that the magnitude of your starting position is approximately equal to the path radius)

	Initial particle velcoity:
		Open Particle_list.py in editer, on line 20 edit the Vel_start values.

	Other Particle properites:
		Open Particle_list.py in editer, on line 22 is Particle_lists, edit the list entry values (use format guide on line 13).
	
	electric source disk radius:
		Open Fields.py in editer, edit value on line 10

	number of electric source disks:
		Open Fields.py in editer, edit value on line 14
	
	Path radius:
		Open Fields.py in editer, edit value on line 16
	
	Eletric source disk charge density:
		Open Fields.py in editer, edit value on line 25

	Remove Magnetic feild effect: 
		Open Field_effect.py and replace lines 65-69 with "B=np.array([0.0,0.0,0.0], dtype=float)"
Accessing data from a simlation:
	The data of the last simulation ran is saved as ParticleData.csv in the program directory. 
	Open this file using program like excel to access individual data entries.
ENJOY THE PROGRAM! 