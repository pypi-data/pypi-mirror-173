import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from yellowbrick.classifier import discrimination_threshold

def fis_machine_crear_lags(df, num_lags = 7):
    #Crea el objeto data frame
    lags = pd.Dataframe()
    #Crear todos los lags
    for cada in range(1, num_lags):
        lags['lag_'+str(cada)] = df.shift(cada).iloc[:0]
    return(lags)

def fis_machine_rolling_mean(df, num_periodos = 7):
    mm = pd.DataFrame()
    for cada in range (1, num_periodos):
        mm['mm_'+str(cada)] = df.shift(1).rolling(cada).mean().iloc[:,0]
    return(mm)

def fis_machine_metric_compute(real, scoring, umbral=0.5,graf_umbral=False):
    #CALCULAR LA DECISION SEGUN EL UMBRAL
    predicho = np.where(scoring > umbral,1,0)
    umbral_100 = umbral * 100
    
    #CALCULAR TODAS LAS MÉTRICAS
    conf = confusion_matrix(real,predicho)

    tn, fp, fn, tp = conf.ravel()

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = 2 * (precision * recall) / (precision + recall)

    #IMPRIMIR RESULTADOS
    print('====================      Metric Report   ====Threshold  {:.2f} %%==========='.format(umbral_100))
    sns.heatmap(conf,annot=True, cmap="YlGnBu" ,fmt='g') 
    plt.tight_layout() 
    plt.title('Confusion matrix') 
    plt.ylabel('Current') 
    plt.xlabel('Predicted')
    plt.show()
    
    print('Precision:',round(precision,3))
    print('Recall   :',round(recall,3))
    print('F1       :',round(F1,3))
    if graf_umbral:
        discrimination_threshold(rl,x,y, exclude = 'queue_rate')
        plt.show()
    print('\n====================================================================')