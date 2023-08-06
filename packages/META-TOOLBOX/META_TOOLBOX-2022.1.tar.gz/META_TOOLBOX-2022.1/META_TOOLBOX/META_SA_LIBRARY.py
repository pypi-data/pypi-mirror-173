import numpy as np
import META_TOOLBOX.META_CO_LIBRARY as META_CO

# DETERMINAÇÃO DA TEMPERATURA INCIIAL QUE GERA UMA PROBABILIDADE DE ACEITE DE 80% EM RELAÇÃO A SOLUÇÃO INICIAL
def START_TEMPERATURE(OF_FUNCTION, NULL_DIC, N_POP, D, X, X_L, X_U, OF, SIGMA, TEMP = None, STOP_CONTROL_TEMP = None):
    """ 
    This function calculates the initial temperature in function of a probability of acceptance of 80% of the initial solutions.  

    Input:
    OF_FUNCTION        | External def user input this function in arguments           | Py function
    N_POP              | Number of population                                         | Integer
    D                  | Problem dimension                                            | Integer
    X                  | Design variables                                             | Py Numpy array[N_POP x D]
    X_L                | Lower limit design variables                                 | Py list[D]
    X_U                | Upper limit design variables                                 | Py list[D]
    OF                 | All objective function values                                | Py Numpy array[N_POP x 1]
    SIGMA              | Standard deviation the normal distribution in percentage     | Float
    TEMP               | Initial temperature or automatic temperature value that has  | Float
                       | an 80% probability of accepting the movement of particles    |
    STOP_CONTROL_TEMP  | Stop criteria about initial temperature try                  | Float
                       | or automatic value = 1000                   
        
    Output:
    T_INITIAL          | Initial temperature SA algorithm                             | Float
    """
    # Automatic temperature p > 80%
    if TEMP == None:
        # Start internal variables
        X_TRY = np.zeros((N_POP, D))
        OF_TRY = np.zeros((N_POP, 1))
        ENERGY = np.zeros((N_POP, 1))
        # Controlling stop criteria
        if STOP_CONTROL_TEMP == None:
            STOP_CRITERIA = 1000
        else:
            STOP_CRITERIA = STOP_CONTROL_TEMP
        # initial probability state and stop counter
        PROBABILITY_STATE = 0.0; STOP = 0.0
        # Looping to determine annealing temperature
        while PROBABILITY_STATE < 0.80:
            # Infinite looping controlling
            if STOP > STOP_CRITERIA:
                break           
            # Particles random movement
            for I_COUNT in range(N_POP):
                # Particle movement
                for J_COUNT in range(D):
                    MEAN_VALUE = X[I_COUNT, J_COUNT]
                    SIGMA_VALUE = abs(MEAN_VALUE * SIGMA)
                    X_TRY[I_COUNT, J_COUNT] = np.random.normal(MEAN_VALUE, SIGMA_VALUE, 1)
                # Check boundes
                X_TRY[I_COUNT, :] = META_CL.CHECK_INTERVAL(X_TRY[I_COUNT, :], X_L, X_U)  
                # Evaluation of the objective function
                OF_TRY[I_COUNT, 0] = OF_FUNCTION(X_TRY[I_COUNT, :], NULL_DIC)
                # Evaluation of the annealing energy
                ENERGY[I_COUNT, 0] = OF_TRY[I_COUNT, 0] -  OF[I_COUNT, 0]
            ENERGY_MAX = ENERGY.max()
            # Initial temperature
            if ENERGY_MAX >= 0:
                T_INITIAL = - ENERGY_MAX / np.log(0.80)
                PROBABILITY_STATE = 0.81
            else:
                PROBABILITY_STATE = 0.00
            # Internal stop counter update
            STOP += 1
    # User temperature
    else:
        # Initial temperature
        T_INITIAL = TEMP
    return T_INITIAL  