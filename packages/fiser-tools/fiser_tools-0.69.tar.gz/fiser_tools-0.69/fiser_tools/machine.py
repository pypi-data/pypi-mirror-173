import pandas as pd

def fis_machine_crear_lags(df, num_lags = 7):

    #Crea el objeto data frame
    lags = pd.Dataframe()

    #Crear todos los lags
    for cada in range(1, num_lags):
        lags['lag_'+str(cada))] = df.shift(cada).iloc[:0]

    return(lags)

def fis_machine_rolling_mean(df, num_periodos = 7):

    mm = pd.DataFrame()

    for cada in range (1, num_periodos):
        mm['mm_'+str(cada)] = df.shift(1).rolling(cada).mean().iloc[:,0]

    return(mm)
