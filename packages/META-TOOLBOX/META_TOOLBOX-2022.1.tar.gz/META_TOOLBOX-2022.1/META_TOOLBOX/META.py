import numpy as np
import time
import META_TOOLBOX.META_CO_LIBRARY as META_CO
import META_TOOLBOX.META_HC_LIBRARY as META_HC
import META_TOOLBOX.META_SA_LIBRARY as META_SA
import META_TOOLBOX.META_FA_LIBRARY as META_FA
from datetime import datetime

def HELLO():
    """
    Test function.
    """
    print("hello world")
    return

def HILL_CLIMBING_001(OF_FUNCTION, SETUP):
    """ 
    Standard Hill climbing algorithm. Continuous version. The algorithm also presents the results formatted in a spreadsheet.

    See documentation in https://wmpjrufg.github.io/META_TOOLBOX/HC001.html
    """
    
    # Setup config
    N_REP = SETUP['N_REP']
    N_ITER = SETUP['N_ITER']
    N_POP = SETUP['N_POP']
    D = SETUP['D']
    X_L = SETUP['X_L']
    X_U = SETUP['X_U']
    SIGMA = SETUP['SIGMA']
    NULL_DIC = SETUP['NULL_DIC']
    
    # Creating variables in the repetitions procedure
    RESULTS_REP = []
    BEST_REP = []
    WORST_REP = []
    AVERAGE_REP = []
    NAME = []
    if NULL_DIC == None:
        NULL_DIC = []
    else:
        pass 
    
    # Repetition looping
    INIT = time.time()
    for REP in range(N_REP):
        
        # Creating variables in the iterations procedure
        OF = np.zeros((N_POP, 1)); 
        FIT = np.zeros((N_POP, 1))
        RESULTS_ITER = [{'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'PARAMETERS': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': J} for J in range(N_POP)]
        BEST_ITER = {'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'PARAMETERS': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': np.empty(N_ITER + 1)}
        AVERAGE_ITER = {'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1)}
        WORST_ITER = {'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': np.empty(N_ITER + 1)}
        NEOF_COUNT = 0 
        
        # Initial population
        X = META_CO.INITIAL_POPULATION_01(N_POP, D, X_L, X_U)
        for I in range(N_POP):
            OF[I, 0] = OF_FUNCTION(X[I, :], NULL_DIC)
            FIT[I, 0] = META_CO.FIT_VALUE(OF[I, 0])
            NEOF_COUNT += 1
               
        # Storage all values in RESULTS_ITER
        for I, X_ALL, OF_ALL, FIT_ALL, in zip(RESULTS_ITER, X, OF, FIT):
            I['X_POSITION'][0, :] = X_ALL
            I['OF'][0] = OF_ALL
            I['FIT'][0] = FIT_ALL
            I['PARAMETERS'][0] = None
            I['NEOF'][0] = NEOF_COUNT
        
        # Best, average and worst storage
        BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE = META_CO.BEST_VALUES(X, OF, FIT, N_POP)
        BEST_ITER['ID_PARTICLE'][0] = BEST_POSITION
        WORST_ITER['ID_PARTICLE'][0] = WORST_POSITION
        BEST_ITER['X_POSITION'][0, :] = X_BEST
        WORST_ITER['X_POSITION'][0, :] = X_WORST
        BEST_ITER['OF'][0] = OF_BEST
        AVERAGE_ITER['OF'][0] = OF_AVERAGE
        WORST_ITER['OF'][0] = OF_WORST
        BEST_ITER['FIT'][0] = FIT_BEST
        AVERAGE_ITER['FIT'][0] = FIT_AVERAGE
        WORST_ITER['FIT'][0] = FIT_WORST
        BEST_ITER['PARAMETERS'][0] = None
        BEST_ITER['NEOF'][0] = NEOF_COUNT
        AVERAGE_ITER['NEOF'][0] = NEOF_COUNT
        WORST_ITER['NEOF'][0] = NEOF_COUNT
        
        # Iteration procedure
        for ITER in range(N_ITER):

            # Population movement
            for POP in range(N_POP):
                
                # Hill Climbing particle movement
                X_ITEMP, OF_ITEMP, FIT_ITEMP, NEOF = META_HC.HC_MOVEMENT(OF_FUNCTION, NULL_DIC, X[POP, :], X_L, X_U, D, SIGMA) 
                
                # New design variables
                if FIT_ITEMP > FIT[POP, 0]:
                    X[POP, :] = X_ITEMP
                    OF[POP, 0] = OF_ITEMP
                    FIT[POP, 0] = FIT_ITEMP
                else:
                    pass
                
                # Update NEOF (Number of Objective Function Evaluations)
                NEOF_COUNT += NEOF
            
            # Storage all values in RESULTS_ITER
            for I, X_ALL, OF_ALL, FIT_ALL  in zip(RESULTS_ITER, X, OF, FIT):
                I['X_POSITION'][ITER + 1, :] = X_ALL
                I['OF'][ITER + 1] = OF_ALL
                I['FIT'][ITER + 1] = FIT_ALL
                I['PARAMETERS'][ITER + 1] = None
                I['NEOF'][ITER + 1] = NEOF_COUNT
            
            # Best, average and worst storage
            BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE = META_CO.BEST_VALUES(X, OF, FIT, N_POP)
            BEST_ITER['ID_PARTICLE'][ITER + 1] = BEST_POSITION
            WORST_ITER['ID_PARTICLE'][ITER + 1] = WORST_POSITION
            BEST_ITER['X_POSITION'][ITER + 1, :] = X_BEST
            WORST_ITER['X_POSITION'][ITER + 1, :] = X_WORST
            BEST_ITER['OF'][ITER + 1] = OF_BEST
            AVERAGE_ITER['OF'][ITER + 1] = OF_AVERAGE
            WORST_ITER['OF'][ITER + 1] = OF_WORST
            BEST_ITER['FIT'][ITER + 1] = FIT_BEST
            AVERAGE_ITER['FIT'][ITER + 1] = FIT_AVERAGE
            WORST_ITER['FIT'][ITER + 1] = FIT_WORST
            BEST_ITER['PARAMETERS'][ITER + 1] = None
            BEST_ITER['NEOF'][ITER + 1] = NEOF_COUNT
            AVERAGE_ITER['NEOF'][ITER + 1] = NEOF_COUNT
            WORST_ITER['NEOF'][ITER + 1] = NEOF_COUNT
        
        # Append iteration results
        RESULTS_REP.append(RESULTS_ITER)
        BEST_REP.append(BEST_ITER)
        AVERAGE_REP.append(AVERAGE_ITER)
        WORST_REP.append(WORST_ITER)
        
        # Progress bar update
        time.sleep(0.01)
        META_CO.PROGRESS_BAR(REP + 1, N_REP)
    END = time.time()
    
    # Resume process (Time and Excel outputs)
    print('Process Time: %.2f' % (END - INIT), 'Seconds', '\n', 'Seconds per repetition: %.2f' % ((END - INIT) / N_REP))
    STATUS_PROCEDURE = META_CO.SUMMARY_ANALYSIS(BEST_REP, N_REP, N_ITER)
    for REP in range(N_REP):
        NAME.append('META_HC001_' + 'REP_' + str(REP) + '_BEST_' + str(REP) + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S')))
        META_CO.EXCEL_WRITER_ITERATION(NAME[REP], D, BEST_REP[REP])
    NAME_RESUME = 'META_HC001_' + 'RESUME' + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S'))
    META_CO.EXCEL_PROCESS_RESUME(NAME_RESUME, D, BEST_REP, N_ITER, N_REP)    
    
    return RESULTS_REP, BEST_REP, AVERAGE_REP, WORST_REP, STATUS_PROCEDURE

def SIMULATED_ANNEALING_001(OF_FUNCTION, SETUP):
    """ 
    Standard Simulated annealing algorithm. Continuous version. The algorithm also presents the results formatted in a spreadsheet.

    See documentation in https://wmpjrufg.github.io/META_TOOLBOX/SA001.html
    """
    
    # Setup config
    N_REP = SETUP['N_REP']
    N_ITER = SETUP['N_ITER']
    N_POP = SETUP['N_POP']
    D = SETUP['D']
    X_L = SETUP['X_L']
    X_U = SETUP['X_U']
    SIGMA = SETUP['SIGMA']
    ALPHA = SETUP['ALPHA']
    TEMP_INI = SETUP['TEMP']
    SCHEDULE = SETUP['SCHEDULE']
    NULL_DIC = SETUP['NULL_DIC']
    
    # Creating variables in the repetitions procedure
    RESULTS_REP = []
    BEST_REP = []
    WORST_REP = []
    AVERAGE_REP = []
    NAME = []
    if NULL_DIC == None:
        NULL_DIC = []
    else:
        pass 
    
    # Repetition looping
    INIT = time.time()
    for REP in range(N_REP):
        
        # Creating variables in the iterations procedure
        OF = np.zeros((N_POP, 1)); 
        FIT = np.zeros((N_POP, 1))
        RESULTS_ITER = [{'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'PARAMETERS': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': J} for J in range(N_POP)]
        BEST_ITER = {'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'PARAMETERS': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': np.empty(N_ITER + 1)}
        AVERAGE_ITER = {'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1)}
        WORST_ITER = {'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': np.empty(N_ITER + 1)}
        NEOF_COUNT = 0 
        
        # Initial population
        X = META_CO.INITIAL_POPULATION_01(N_POP, D, X_L, X_U)
        for I in range(N_POP):
            OF[I, 0] = OF_FUNCTION(X[I, :], NULL_DIC)
            FIT[I, 0] = META_CO.FIT_VALUE(OF[I, 0])
            NEOF_COUNT += 1
        
        # Initial temperature
        TEMPERATURE = TEMP_INI
        #TEMPERATURE = META_SA.START_TEMPERATURE(OF_FUNCTION, NULL_DIC, N_POP, D, X, X_L, X_U, OF, SIGMA, TEMP, STOP_CONTROL_TEMP)
                       
        # Storage all values in RESULTS_ITER
        for I, X_ALL, OF_ALL, FIT_ALL, in zip(RESULTS_ITER, X, OF, FIT):
            I['X_POSITION'][0, :] = X_ALL
            I['OF'][0] = OF_ALL
            I['FIT'][0] = FIT_ALL
            I['PARAMETERS'][0] = TEMPERATURE
            I['NEOF'][0] = NEOF_COUNT
        
        # Best, average and worst storage
        BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE = META_CO.BEST_VALUES(X, OF, FIT, N_POP)
        BEST_ITER['ID_PARTICLE'][0] = BEST_POSITION
        WORST_ITER['ID_PARTICLE'][0] = WORST_POSITION
        BEST_ITER['X_POSITION'][0, :] = X_BEST
        WORST_ITER['X_POSITION'][0, :] = X_WORST
        BEST_ITER['OF'][0] = OF_BEST
        AVERAGE_ITER['OF'][0] = OF_AVERAGE
        WORST_ITER['OF'][0] = OF_WORST
        BEST_ITER['FIT'][0] = FIT_BEST
        AVERAGE_ITER['FIT'][0] = FIT_AVERAGE
        WORST_ITER['FIT'][0] = FIT_WORST
        BEST_ITER['PARAMETERS'][0] = TEMPERATURE
        BEST_ITER['NEOF'][0] = NEOF_COUNT
        AVERAGE_ITER['NEOF'][0] = NEOF_COUNT
        WORST_ITER['NEOF'][0] = NEOF_COUNT
        
        # Iteration procedure
        for ITER in range(N_ITER):

            # Population movement
            for POP in range(N_POP):
                
                # Simulated Annealing particle movement (Same Hill Climbing movement)
                X_ITEMP, OF_ITEMP, FIT_ITEMP, NEOF = META_HC.HC_MOVEMENT(OF_FUNCTION, NULL_DIC, X[POP, :], X_L, X_U, D, SIGMA) 
                
                # Energy
                DELTAE = OF_ITEMP - OF[POP, 0]
                
                # Probability of acceptance of the movement
                if DELTAE < 0:
                    PROBABILITY_STATE = 1
                elif DELTAE >= 0:
                    PROBABILITY_STATE = np.exp(- DELTAE / TEMPERATURE)
                
                # New design variables
                RANDON_NUMBER = np.random.random()
                if RANDON_NUMBER < PROBABILITY_STATE:
                    X[POP, :] = X_ITEMP
                    OF[POP, 0] = OF_ITEMP
                    FIT[POP, 0] = FIT_ITEMP
                else:
                    pass
                
                # Update NEOF (Number of Objective Function Evaluations)
                NEOF_COUNT += NEOF
            
            # Storage all values in RESULTS_ITER
            for I, X_ALL, OF_ALL, FIT_ALL  in zip(RESULTS_ITER, X, OF, FIT):
                I['X_POSITION'][ITER + 1, :] = X_ALL
                I['OF'][ITER + 1] = OF_ALL
                I['FIT'][ITER + 1] = FIT_ALL
                I['PARAMETERS'][ITER + 1] = TEMPERATURE
                I['NEOF'][ITER + 1] = NEOF_COUNT
            
            # Best, average and worst storage
            BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE = META_CO.BEST_VALUES(X, OF, FIT, N_POP)
            BEST_ITER['ID_PARTICLE'][ITER + 1] = BEST_POSITION
            WORST_ITER['ID_PARTICLE'][ITER + 1] = WORST_POSITION
            BEST_ITER['X_POSITION'][ITER + 1, :] = X_BEST
            WORST_ITER['X_POSITION'][ITER + 1, :] = X_WORST
            BEST_ITER['OF'][ITER + 1] = OF_BEST
            AVERAGE_ITER['OF'][ITER + 1] = OF_AVERAGE
            WORST_ITER['OF'][ITER + 1] = OF_WORST
            BEST_ITER['FIT'][ITER + 1] = FIT_BEST
            AVERAGE_ITER['FIT'][ITER + 1] = FIT_AVERAGE
            WORST_ITER['FIT'][ITER + 1] = FIT_WORST
            BEST_ITER['PARAMETERS'][ITER + 1] = TEMPERATURE
            BEST_ITER['NEOF'][ITER + 1] = NEOF_COUNT
            AVERAGE_ITER['NEOF'][ITER + 1] = NEOF_COUNT
            WORST_ITER['NEOF'][ITER + 1] = NEOF_COUNT

            # Update temperature
            # Linear annealing schedule
            if SCHEDULE == 0:
                TEMPERATURE = TEMPERATURE * ALPHA
            # ???? annealing schedule
            elif SCHEDULE == 1:
                pass      
        
        # Append iteration results
        RESULTS_REP.append(RESULTS_ITER)
        BEST_REP.append(BEST_ITER)
        AVERAGE_REP.append(AVERAGE_ITER)
        WORST_REP.append(WORST_ITER)
        
        # Progress bar update
        time.sleep(0.01)
        META_CO.PROGRESS_BAR(REP + 1, N_REP)
    END = time.time()
    
    # Resume process (Time and Excel outputs)
    print('Process Time: %.2f' % (END - INIT), 'Seconds', '\n', 'Seconds per repetition: %.2f' % ((END - INIT) / N_REP))
    STATUS_PROCEDURE = META_CO.SUMMARY_ANALYSIS(BEST_REP, N_REP, N_ITER)
    for REP in range(N_REP):
        NAME.append('META_SA001_' + 'REP_' + str(REP) + '_BEST_' + str(REP) + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S')))
        META_CO.EXCEL_WRITER_ITERATION(NAME[REP], D, BEST_REP[REP])
    NAME_RESUME = 'META_SA001_' + 'RESUME' + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S'))
    META_CO.EXCEL_PROCESS_RESUME(NAME_RESUME, D, BEST_REP, N_ITER, N_REP)    
    
    return RESULTS_REP, BEST_REP, AVERAGE_REP, WORST_REP, STATUS_PROCEDURE

def FIREFLY_ALGORITHM_001(OF_FUNCTION, SETUP):
    """ 
    Standard Firefly algorithm.

    See documentation in www.github.io/teste
    """
    
    # Setup config
    N_REP = SETUP['N_REP']
    N_ITER = SETUP['N_ITER']
    N_POP = SETUP['N_POP']
    D = SETUP['D']
    X_L = SETUP['X_L']
    X_U = SETUP['X_U']
    BETA_0 = SETUP['BETA_0']
    GAMMA = SETUP['GAMMA']
    ALPHA_MIN = SETUP['ALPHA_MIN']
    ALPHA_MAX = SETUP['ALPHA_MAX']
    THETA = SETUP['THETA']
    NULL_DIC = SETUP['NULL_DIC']
    ALPHA_UPDATE = 0 # ??????????????????????????
    
    # Creating variables in the repetitions procedure
    RESULTS_REP = []
    BEST_REP = []
    WORST_REP = []
    AVERAGE_REP = []
    NAME = []
    if NULL_DIC == None:
        NULL_DIC = []
    else:
        pass 
    
    # Repetition looping
    INIT = time.time()
    for REP in range(N_REP):
        
        # Creating variables in the iterations procedure
        OF = np.zeros((N_POP, 1)); 
        FIT = np.zeros((N_POP, 1))
        RESULTS_ITER = [{'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'PARAMETERS': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': J} for J in range(N_POP)]
        BEST_ITER = {'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'PARAMETERS': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': np.empty(N_ITER + 1)}
        AVERAGE_ITER = {'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1)}
        WORST_ITER = {'X_POSITION': np.empty((N_ITER + 1, D)), 'OF': np.empty(N_ITER + 1), 'FIT': np.empty(N_ITER + 1), 'NEOF': np.empty(N_ITER + 1), 'ID_PARTICLE': np.empty(N_ITER + 1)}
        NEOF_COUNT = 0 
        
        # Initial population
        X = META_CO.INITIAL_POPULATION_01(N_POP, D, X_L, X_U)
        for I in range(N_POP):
            OF[I, 0] = OF_FUNCTION(X[I, :], NULL_DIC)
            FIT[I, 0] = META_CO.FIT_VALUE(OF[I, 0])
            NEOF_COUNT += 1
        
        # Initial random parameter
        ALPHA = ALPHA_MAX
   
        # Storage all values in RESULTS_ITER
        for I, X_ALL, OF_ALL, FIT_ALL, in zip(RESULTS_ITER, X, OF, FIT):
            I['X_POSITION'][0, :] = X_ALL
            I['OF'][0] = OF_ALL
            I['FIT'][0] = FIT_ALL
            I['PARAMETERS'][0] = ALPHA
            I['NEOF'][0] = NEOF_COUNT
        
        # Best, average and worst storage
        BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE = META_CO.BEST_VALUES(X, OF, FIT, N_POP)
        BEST_ITER['ID_PARTICLE'][0] = BEST_POSITION
        WORST_ITER['ID_PARTICLE'][0] = WORST_POSITION
        BEST_ITER['X_POSITION'][0, :] = X_BEST
        WORST_ITER['X_POSITION'][0, :] = X_WORST
        BEST_ITER['OF'][0] = OF_BEST
        AVERAGE_ITER['OF'][0] = OF_AVERAGE
        WORST_ITER['OF'][0] = OF_WORST
        BEST_ITER['FIT'][0] = FIT_BEST
        AVERAGE_ITER['FIT'][0] = FIT_AVERAGE
        WORST_ITER['FIT'][0] = FIT_WORST
        BEST_ITER['PARAMETERS'][0] = ALPHA
        BEST_ITER['NEOF'][0] = NEOF_COUNT
        AVERAGE_ITER['NEOF'][0] = NEOF_COUNT
        WORST_ITER['NEOF'][0] = NEOF_COUNT
        
        # Iteration procedure
        for ITER in range(N_ITER):
            
            # Ordering firefly according to fitness
            X_TEMP = X.copy()
            OF_TEMP = OF.copy()
            FIT_TEMP = FIT.copy()
            SORT_POSITIONS = np.argsort(OF_TEMP.T)
            for I in range(N_POP):
                AUX = SORT_POSITIONS[0, I]
                X[I, :] = X_TEMP[AUX, :]
                OF[I, 0] = OF_TEMP[AUX, 0] 
                FIT[I, 0] = FIT_TEMP[AUX, 0]
            
            # Population movement
            X_J = X.copy()
            FITJ = FIT.copy()
            for POP_I in range(N_POP):
                FIT_I = FIT[POP_I, 0]
                for POP_J in range(N_POP):
                    FIT_J = FITJ[POP_J, 0]
                    if FIT_I < FIT_J:
                        BETA = META_FA.ATTRACTIVENESS_FIREFLY_PARAMETER(BETA_0, GAMMA, X[POP_I, :], X_J[POP_J, :], D)                            
                        X_TEMPORARYI, OF_TEMPORARYI, FIT_TEMPORARYI, NEOF = META_FA.FIREFLY_MOVEMENT(OF_FUNCTION, X[POP_I, :], X_J[POP_J, :], BETA, ALPHA, D, X_L, X_U, NULL_DIC)
                        ##### X_ITEMP, OF_ITEMP, FIT_ITEMP
                    else:
                        X_TEMPORARYI = X[POP_I, :]
                        OF_TEMPORARYI = OF[POP_I, 0]
                        FIT_TEMPORARYI = FIT[POP_I, 0]
                        NEOF = 0
                    
                    # New design variables
                    X[POP_I, :] = X_TEMPORARYI
                    OF[POP_I, 0] = OF_TEMPORARYI
                    FIT[POP_I, 0] = FIT_TEMPORARYI
                    NEOF_COUNT += NEOF
            
            # Storage all values in RESULTS_ITER
            for I, X_ALL, OF_ALL, FIT_ALL  in zip(RESULTS_ITER, X, OF, FIT):
                I['X_POSITION'][ITER + 1, :] = X_ALL
                I['OF'][ITER + 1] = OF_ALL
                I['FIT'][ITER + 1] = FIT_ALL
                I['PARAMETERS'][ITER + 1] = ALPHA
                I['NEOF'][ITER + 1] = NEOF_COUNT
            
            # Best, average and worst storage
            BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE = META_CO.BEST_VALUES(X, OF, FIT, N_POP)
            BEST_ITER['ID_PARTICLE'][ITER + 1] = BEST_POSITION
            WORST_ITER['ID_PARTICLE'][ITER + 1] = WORST_POSITION
            BEST_ITER['X_POSITION'][ITER + 1, :] = X_BEST
            WORST_ITER['X_POSITION'][ITER + 1, :] = X_WORST
            BEST_ITER['OF'][ITER + 1] = OF_BEST
            AVERAGE_ITER['OF'][ITER + 1] = OF_AVERAGE
            WORST_ITER['OF'][ITER + 1] = OF_WORST
            BEST_ITER['FIT'][ITER + 1] = FIT_BEST
            AVERAGE_ITER['FIT'][ITER + 1] = FIT_AVERAGE
            WORST_ITER['FIT'][ITER + 1] = FIT_WORST
            BEST_ITER['PARAMETERS'][ITER + 1] = ALPHA
            BEST_ITER['NEOF'][ITER + 1] = NEOF_COUNT
            AVERAGE_ITER['NEOF'][ITER + 1] = NEOF_COUNT
            WORST_ITER['NEOF'][ITER + 1] = NEOF_COUNT

            # Update random parameter
            if ALPHA_UPDATE == 0:
                ALPHA = ALPHA_MIN + (ALPHA_MAX - ALPHA_MIN) * THETA ** ITER
            elif ALPHA_UPDATE == 1:
                pass      
        
        # Append iteration results
        RESULTS_REP.append(RESULTS_ITER)
        BEST_REP.append(BEST_ITER)
        AVERAGE_REP.append(AVERAGE_ITER)
        WORST_REP.append(WORST_ITER)
        
        # Progress bar update
        time.sleep(0.01)
        META_CO.PROGRESS_BAR(REP + 1, N_REP)
    END = time.time()
    
    # Resume process (Time and Excel outputs)
    print('Process Time: %.2f' % (END - INIT), 'Seconds', '\n', 'Seconds per repetition: %.2f' % ((END - INIT) / N_REP))
    STATUS_PROCEDURE = META_CO.SUMMARY_ANALYSIS(BEST_REP, N_REP, N_ITER)
    for REP in range(N_REP):
        NAME.append('META_FA001_' + 'REP_' + str(REP) + '_BEST_' + str(REP) + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S')))
        META_CO.EXCEL_WRITER_ITERATION(NAME[REP], D, BEST_REP[REP])
    NAME_RESUME = 'META_FA001_' + 'RESUME' + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S'))
    META_CO.EXCEL_PROCESS_RESUME(NAME_RESUME, D, BEST_REP, N_ITER, N_REP)    
    
    return RESULTS_REP, BEST_REP, AVERAGE_REP, WORST_REP, STATUS_PROCEDURE