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

def fis_machine_metric_compute(real, scoring, umbral=0.5,graf_umbral=False,model=None,x=None,y=None):
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
    print('====================  Metric Report  ==== Threshold {:.2f} % ========='.format(umbral_100))
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
        discrimination_threshold(model,x,y, exclude = 'queue_rate')
        plt.show()
    print('\n====================================================================')
    
def fis_machine_max_roi(real,scoring, salida = 'grafico',itn=0,ifp=-15,ifn=-85,itp=85):
    """
    #DEFINIMOS LA MATRIZ DE IMPACTO
    itn   #true negatvie
    ifp   #false positive
    ifn   #false negative
    itp   #true positive
    """
    #DEFINIMOS LA MATRIZ DE IMPACTO
    ITN = itn   #true negatvie
    IFP = ifp   #false positive
    IFN = ifn   #false negative
    ITP = itp   #true positive
    
    #DEFINIMOS LA FUNCION DEL VALOR ESPERADO
    def valor_esperado(matriz_conf):
        TN, FP, FN, TP = conf.ravel()
        VE = (TN * ITN) + (FP * IFP) + (FN * IFN) + (TP * ITP)
        return(VE)
    
    #CREAMOS UNA LISTA PARA EL VALOR ESPERADO
    ve_list = []
    
    #ITERAMOS CADA PUNTO DE CORTE Y RECOGEMOS SU VE
    for umbral in np.arange(0,1,0.01):
        predicho = np.where(scoring > umbral,1,0) 
        conf = confusion_matrix(real,predicho)
        ve_temp = valor_esperado(conf)
        ve_list.append(tuple([umbral,ve_temp]))
        
    #DEVUELVE EL RESULTADO COMO TGRAFICO O COMO EL UMBRAL ÓPTIMO
    df_temp = pd.DataFrame(ve_list, columns = ['umbral', 'valor_esperado'])
    if salida == 'grafico':
        solo_ve_positivo = df_temp[df_temp.valor_esperado > 0]
        plt.figure(figsize = (12,6))
        sns.lineplot(data = solo_ve_positivo, x = 'threshold', y = 'expected_value')
        plt.xticks(solo_ve_positivo.umbral, fontsize = 14)
        plt.yticks(solo_ve_positivo.valor_esperado, fontsize = 12);        
    else:    
        return(df_temp.iloc[df_temp.valor_esperado.idxmax(),0])