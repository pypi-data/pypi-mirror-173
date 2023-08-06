import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def fis_tools_clean_df_columns(df):
    """
    Pasamos un DataFrame y nos lo devuelve con las columnas con un correcto formato para trabajo
    """
    for col in df.columns:
        new_col = col.lower()
        new_col = new_col.replace(" ", "_")
        new_col = new_col.replace("ó", "o").replace("ò","o")
        new_col = new_col.replace("í", "i").replace("á", "a").replace("é", "e")
        new_col = new_col.replace("ü", "u").replace("à","a").replace("è","e")
        new_col = new_col.replace("(", "")
        new_col = new_col.replace(")", "")
        new_col = new_col.replace("-", "")
        new_col = new_col.replace('º', "").replace("__", "_")
        new_col = new_col.replace("ñ", "n").replace("ú", "u").replace("í", "i")
        df.rename({col: new_col}, axis=1, inplace=True)
    return df
    
def fis_tools_frec_cat(df_cat):
    """
    Salida en formato DataFrame de la frecuencia de las variables categoricas en %
    """
    resultado = df_cat.apply(lambda x: x.value_counts(normalize = True)).T.stack()\
                .to_frame().reset_index()\
                .rename(columns={'level_0':'Variable','level_1':'Valor',0: "Frecuencia"})\
                .sort_values(by = ['Variable','Frecuencia'])
    return(resultado)
    
def fis_tools_stats_cont(df_cont):
    """
    Salida en formato DataFrame de todos los estadísticos de variable contínua + mediana
    """
    #Calculamos describe
    estadisticos = df_cont.describe().T
    #Añadimos la mediana
    estadisticos['median'] = df_cont.median()
    #Reordenamos para que la mediana esté al lado de la media
    estadisticos = estadisticos.iloc[:,[0,1,8,2,3,4,5,6,7]]
    #Lo devolvemos
    return(estadisticos)
    
def fis_tools_graph_eda_cat(df_cat):
    """
    Salida gráfica de todas las variables categoricas para exploration data analysis
    """
    #Calculamos el número de filas que necesitamos
    from math import ceil
    filas = ceil(df_cat.shape[1] / 2)

    #Definimos el gráfico
    f, ax = plt.subplots(nrows = filas, ncols = 2, figsize = (16, filas * 6))

    #Aplanamos para iterar por el gráfico como si fuera de 1 dimensión en lugar de 2
    ax = ax.flat 

    #Creamos el bucle que va añadiendo gráficos
    for cada, variable in enumerate(df_cat):
        df_cat[variable].value_counts().plot.barh(ax = ax[cada])
        ax[cada].set_title(variable, fontsize = 12, fontweight = "bold")
        ax[cada].tick_params(labelsize = 12)
        
def fis_tools_graph_eda_cont(df_cont):
    """
    Salida gráfica de todas las variables continuas para exploration data analysis
    """
    #Calculamos el número de fila que necesitamos
    from math import ceil
    filas = ceil(df_cont.shape[1] / 2)

    #Definimos el gráfico
    f, ax = plt.subplots(nrows = filas, ncols = 2, figsize = (16, filas * 6))

    #Aplanamos para iterar por el gráfico como si fuera de 1 dimensión en lugar de 2
    ax = ax.flat 

    #Creamos el bucle que va añadiendo gráficos
    for cada, variable in enumerate(df_cont):
        df_cont[variable].plot.density(ax = ax[cada])
        ax[cada].set_title(variable, fontsize = 12, fontweight = "bold")
        ax[cada].tick_params(labelsize = 12)
        
#Función para agrupar categorías raras en 'OTROS'
def fis_tools_group_cat_unknown(variable, criterio = 0.05,nombre='OTHERS'):
    """
    A partir del porcentaje de recurrencia (criterio) se agrupan N categorias en 1 sola nombre = 'OTHERS'
    """
    #Calcula las frecuencias
    frecuencias = variable.value_counts(normalize=True)
    #Identifica las que están por debajo del criterio
    temp = [cada for cada in frecuencias.loc[frecuencias < criterio].index.values]
    #Las recodifica en 'OTROS'
    temp2 = np.where(variable.isin(temp),nombre,variable)
    #Devuelve el resultado
    return(pd.Series(temp2))
    
def fis_tools_quitar_tildes(palabra):
    """
    Limpieza de tildes para análisis
    """
    #Definimos la versión con tildes y símbolos y la sin
    con = 'áéíóúüñÁÉÍÓÚÜÑ'
    sin = 'aeiouunAEIOUUN'
    #Creamos un traductor
    traductor = str.maketrans(con,sin)
    #Aplicamos el traductor y devolvemos la palabra limpia
    return(palabra.translate(traductor))
    
def fis_tools_pre_strong_corr(df,lim_inf = 0.3, lim_sup = 1,drop_dupli=True):
    """
    Extracción de variables correlacionadas a partir de un umbral lim_inf y tope lim_sup
    """
    #Calcula la matriz de correlación
    c = df.corr().abs()
    #Lo pasa todo a filas
    c= c.unstack()
    #Pasa el índice a columnas y le pone nombres
    c = pd.DataFrame(c).reset_index()
    c.columns = ['var1','var2','corr']
    #A dataframe, filtra limites y ordena en descendiente
    c = c.loc[(c['corr'] > lim_inf) &  (c['corr'] < lim_sup),:].sort_values(by = 'corr', ascending=False)
    #Desduplica las correlaciones (o no si drop_dupli es False)
    c = c if drop_dupli == False else c.drop_duplicates(subset = ['corr'])
    #Devuelve la salida
    return(c)
    
def fis_tools_pre_ranking_mi(mutual_selector, predictors_df, modo = 'tabla'):
    """
    Salida Mejorada de la salida from sklearn.feature_selection import mutual_info_classif
    """
    #Maqueta el ranking
    ranking_mi = pd.DataFrame(mutual_selector, index = predictors_df.columns).reset_index()
    ranking_mi.columns = ['variable','importancia_mi']
    ranking_mi = ranking_mi.sort_values(by = 'importancia_mi', ascending = False)
    ranking_mi['ranking_mi'] = np.arange(0,ranking_mi.shape[0])
    #Muestra la salida
    if modo == 'tabla':
        return(ranking_mi)
    else:
        g = ranking_mi[0:15].importancia_mi.sort_values().plot.barh()
        g.set_yticklabels(ranking_mi[0:15].sort_values(by = 'importancia_mi').variable)
        return(g)

def fis_tools_pre_ranking_per(predictoras,rfe_ranking):
    """
    Salida Mejorada de la salida from sklearn.feature_selection import RFECV
    """
    rank_rfe = pd.DataFrame({'variable': predictoras.columns, 'ranking_rfe': rfe_ranking}).sort_values(by = 'ranking_rfe')
    return(rank_rfe)
 
def fis_tools_pre_ranking_per(predictoras,permutacion,modo='tabla'):
    """
    Salida Mejorada de la salida from sklearn.inspection import permutation_importance
    """
    ranking_per = pd.DataFrame({'variable': predictoras.columns, 'importancia_per': permutacion.importances_mean}).sort_values(by = 'importancia_per', ascending = False)
    ranking_per['ranking_per'] = np.arange(0,ranking_per.shape[0])
    if modo == 'tabla':
        return(ranking_per)
    else:
        ranking_per.set_index('variable').importancia_per.sort_values().plot.barh(figsize = (8,10));
    
def fis_tools_pre_ranking_tot(rank_mi, rank_rfe,rank_per,modo='tabla'):
    """
    Comparativa de todos los rankings (mi, rfe, permutation) grafica y por tabla
    """
    ranking_tot = pd.merge(pd.merge(rank_mi,rank_rfe),rank_per)
    ranking_tot['puntos'] = ranking_tot.ranking_mi + ranking_tot.ranking_rfe + ranking_tot.ranking_per
    ranking_tot.sort_values(by = 'puntos', inplace=True)
    ranking_tot['ranking_tot'] = range(0,len(ranking_tot.variable))
    if modo == 'tabla':
        return(ranking_tot)
    else:
        ranking_tot.set_index('variable').puntos.sort_values(ascending = False).plot.barh(figsize = (8,10));