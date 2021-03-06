import pytest
import numpy as np
import scipy.constants as const
import Test_states
from Field_effect import Field_effect
from P_state_update import Update
"""A class to test areas of the simulations using specific enviroments with
 pre calculated analitic solutions"""
class test_master():
    "testing the electric feild generation"
    def test_E_fields():
        "assigning enriroment and solution state 1: feild generated by a charged disk"
        Test_state=Test_states.E_Teststates.Teststate_1()

        Testing_state=Test_state[0]
        Expected_solution=Test_state[1]
        "running test enviroment through feild effect class"
        Function_solution=Field_effect(None, True, Testing_state)
        "checking simulation solution and analitic solution are the same within a relative tolerance rtol"
        print("Electric feild calculation.   x:simulation result, y:analytical solution")
        np.testing.assert_allclose(Function_solution.E_effect()[0][0], Expected_solution[0], rtol=0.00001) 
        print(100*(Expected_solution[0]-Function_solution.E_effect()[0][0])/(Expected_solution[0])," % ", "difference from expected value")

    "Testing the M feild generation"
    def test_M_fields():
        "assigning enviroment and solution state 1: paticle with set velocity and set required radius"
        Test_state=Test_states.M_Teststates.Teststate_1()

        Testing_state=Test_state[0]
        Expected_solution=Test_state[1]
        Function_solution=Field_effect.M_effect(None,True,Testing_state)
        "checking simulation solution and analitic solution are the same within a relative tolerance rtol"
        print("Magnetic feild calculation.   x:simulation result, y:analytical solution")

        np.testing.assert_allclose(Function_solution[2], Expected_solution[2], rtol=0.000000000001) 
        print(100*(Expected_solution-Function_solution)/(Expected_solution[2])," % ", "difference from expected value")
    
    "Testing that kinimatics of a particle are correctly updated"
    def test_kinimatic_updater_linear_acceleration():
        "assigning enviroment and solution state 1: particle with initial velocity in a constant gravitational feild"
        Test_state=Test_states.Kin_Teststates.Teststate_1()
        Testing_state=Update(None,True,Test_state[0])
        Expected_solution=Test_state[1]
        N_steps=round(Test_state[0][11]/Test_state[0][9])

        "simulating enviroment over teststate specified time"
        for Time_i in range(0,N_steps):
            Testing_state.update(acc=Testing_state.acc[0],formulae=["acc","0","0"])

        Function_solution=Testing_state.pos
        print("Kinetic simuation (Lin Acc) (Y pos).   x:simulation result, y:analytical solution")
        np.testing.assert_allclose(Function_solution[2], Expected_solution[2], rtol=0.0000000000000000001)
        print(Expected_solution[2],Function_solution[2],100*(Expected_solution[2]-Function_solution[2])/(Expected_solution[2])," % ", "difference from expected value")
    
    "testing energy convervation"
    def test_kin_updater_SHM():
        """assigning enviroment and solution state 1: a particle in simple harmonic 
        motion due to a restorative force"""
        Test_state=Test_states.Kin_Teststates.Teststate_2() 
        Testing_state=Update(None,True,Test_state[0])
        Expected_solution=Test_state[1]
        N_steps=round(Test_state[0][11]/Test_state[0][9])
        for Time_i in range(0,N_steps):
            Testing_state.update(pos_x=Testing_state.pos[0],vel_x=Testing_state.vel[0],acc_x=Testing_state.acc[0] ,formulae=["-0.25*pos_x","-0.25*vel_x","-0.25*acc_x"])
        Function_solution=Testing_state.pos
        print("kinetic simulation (SHM) (X pos).   x:simulation result, y:analytical solution")
        np.testing.assert_allclose(Function_solution[0], Expected_solution[0], rtol=0.00000000000000001)
        print(100*(Expected_solution[0]-Function_solution[0])/(Expected_solution[0])," % ", "difference from expected value")
    
    
    "user selection of test to run"
    
    print("please select test to run from the following list:")
    print("1:test electric field calculations, 2:test magnetic field calculations, 3:test kinetic simulation, with linear acceleration, 4: Test kinetic simulation, with simple harmonic motion")
    User_selection=int(input("Enter selection: "))
    
    "running user selected test"
    if User_selection == 1:
        test_E_fields()
    elif User_selection == 2:
       test_M_fields()
    elif User_selection == 3:
        test_kinimatic_updater_linear_acceleration()
    elif User_selection == 4:
        test_kin_updater_SHM()
