import pandas as pd

def run(data):

    #Typical time interval
    intTimeStep=(data.index.to_series().diff().dt.total_seconds().median()/60).round(0).astype(int)
    meanTimeStep=intTimeStep
    #Longest run session. Used to abort long runs. And som declarations, may me adjusted if appropriate
    intTimeStop=300
    cvLimit=0.01
    intTimeStepFirstRun=intTimeStep
    intTimeStepVector = range(intTimeStep, intTimeStop + 1, intTimeStep)
    
    #Used as a limit when data can be concluded as "good enough"
    cvorg=data['value'].std()/data['value'].mean()
    
    #Round time stamp to closest minute
    data.index = data.index.round('min')
    #Mean value of duplicated time stamps
    data = data.groupby(data.index).mean()
    #Resample data and calculate rolling mean
    dataResample = data.resample('min').interpolate(method='linear')
    dataRollingMean=dataResample.rolling(window=intTimeStep).mean()
    
    #Match with original data, indexTimestep
    dataTorture = data.copy()
    dataTorture.update(dataRollingMean)
    cv1=dataTorture['value'].std()/dataTorture['value'].mean()
    
    def autoMA(intTimeStep, data):
        #Calculate the rolling mean with a window
        dataRollingMean=dataResample.rolling(window=intTimeStep).mean()
        #Match with original data, indexTimestep
        dataTorture = data.copy()
        dataTorture.update(dataRollingMean)
        cv2=dataTorture['value'].std()/dataTorture['value'].mean()
        return cv2, dataTorture
    
    #Test if raw data reach set cvlimit, otherwise run MA-function
    if (cvorg - cv1) > cvLimit:
        cv2 = 0
        for i in intTimeStepVector:
            intTimeStep = i + intTimeStepFirstRun
            cv2, dataTorture = autoMA(intTimeStep, data)
            if ((cv1/cvorg)-(cv2/cvorg)) < cvLimit:
                print('Int timestep: ', intTimeStep, 'CV-value: ', (cv1/cvorg)-(cv2/cvorg))
                break
            else:
                print('Int timestep: ', intTimeStep, 'CV-value: ', (cv1/cvorg)-(cv2/cvorg))
                cv1 = cv2
    
    #Test if the raw data was good enough
    if intTimeStep == intTimeStepFirstRun:
        result = pd.DataFrame()
        print('raw data good enough')
        return result
    else:
        result = dataTorture
        print('Used median time step: ', meanTimeStep)
        return result
        