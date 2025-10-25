import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import streamlit as st
from corregir_nombres import corregir_nombre
import requests
from io import BytesIO
import warnings
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime
import pytz
from sqlalchemy import text
from db_utils import crear_engine, obtener_notas_planetscale, listado_general_planetscale , planeacion_semanal_planetscale

#Esta nota es para verificar llave ssh
st.set_page_config(layout="wide")


ingles = ['INGLES LISTENING','INGLES READING','INGLES SPEAKING', 'INGLES WRITING']



def cargar_listado():
    df = listado_general_planetscale()

def cargar_planeacion():
    response = requests.get(url_excel_planeacion)
    response.raise_for_status()  # Lanza error si hay HTTP 403/404/500
    df = pd.read_excel(BytesIO(response.content), sheet_name='bachillerato')
    return df

@st.cache_data
def cargar_notas():
    df = obtener_notas_planetscale()
    df['grado'] = df['grado'].astype(str)
    df['estudiante'] = df['estudiante'].apply(corregir_nombre)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df[~df['asignatura'].isin(ingles)]
    return df

@st.cache_data
def cargar_notas_ingles():
    df = obtener_notas_planetscale()
    df['grado'] = df['grado'].astype(str)
    df['estudiante'] = df['estudiante'].apply(corregir_nombre)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df[df['asignatura'].isin(ingles)]
    return df

notas = cargar_notas()

notas_ingles = cargar_notas_ingles()
planeacion_bachillerato = planeacion_semanal_planetscale('bachillerato')
planeacion_bachillerato.insert(1, 'ingles', 'x') #Se agrega columna ingles despues de estudiante porque el codigo para generar F1's lee por ubicacion de columna
estudiantes = cargar_listado()

notas['grado'] = notas['grado'].astype(str)
notas['estudiante'] = notas['estudiante'].apply(corregir_nombre)


################################################################################################################
asignaturas_6_7= ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA',
                  'HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','FILOSOFIA',
                  'COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS',
                  'ARITMETICA','ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS']

ciencias_6_7  = ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA']
sociales_6_7  = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','FILOSOFIA']
lenguaje_6_7  = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS']
matemati_6_7  = ['ARITMETICA','ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS']
sociales_4_5  = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','PENSAMIENTO RELIGIOSO']
lenguaje_4_5  = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','PENSAMIENTO RELIGIOSO']

######################################################################################################################################

asignaturas_8_9= ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA',
                  'HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','FILOSOFIA',
                  'COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS',
                  'ALGEBRA', 'ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS']

ciencias_8_9  = ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA']
sociales_8_9  = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','FILOSOFIA']
lenguaje_8_9  = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS']
matemati_8_9  = ['ALGEBRA','ANIMAPLANOS', 'ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS']

######################################################################################################################################


asignaturas_10=  ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA',
                  'CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS','FILOSOFIA',
                  'COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','METODOLOGIA',
                  'TRIGONOMETRIA','ANIMAPLANOS', 'ESTADISTICA', 'MATEMATICA FINANCIERA', 'DIBUJO TECNICO', 'SISTEMAS']

ciencias_10  = ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA','METODOLOGIA']
sociales_10  = ['CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS','FILOSOFIA','METODOLOGIA']
lenguaje_10  = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','METODOLOGIA']
matemati_10  = ['TRIGONOMETRIA','ANIMAPLANOS', 'ESTADISTICA', 'MATEMATICA FINANCIERA', 'DIBUJO TECNICO', 'SISTEMAS','METODOLOGIA']

######################################################################################################################################
asignaturas_11=  ['QUIMICA','MEDIO AMBIENTE','FISICA',
                  'CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS','FILOSOFIA',
                  'COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','METODOLOGIA',
                  'CALCULO','ANIMAPLANOS', 'ESTADISTICA', 'MATEMATICA FINANCIERA', 'DIBUJO TECNICO', 'SISTEMAS']

ciencias_11  = ['QUIMICA','MEDIO AMBIENTE','FISICA','METODOLOGIA']
sociales_11  = ['CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS','FILOSOFIA','METODOLOGIA']
lenguaje_11  = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','METODOLOGIA']
matemati_11  = ['CALCULO','ANIMAPLANOS','ESTADISTICA', 'MATEMATICA FINANCIERA', 'DIBUJO TECNICO', 'SISTEMAS','METODOLOGIA']

##################################################################################################################

##Asignaturas globales para el formulario de cargar notas

ciencias_global = ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA','METODOLOGIA']
sociales_global = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','FILOSOFIA','CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS','METODOLOGIA','PENSAMIENTO RELIGIOSO']
lenguaje_global = ['PENSAMIENTO RELIGIOSO','COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','METODOLOGIA','PENSAMIENTO RELIGIOSO']
matematicas_global = ['ARITMETICA','ALGEBRA','TRIGONOMETRIA','CALCULO','ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS','METODOLOGIA','MATEMATICA FINANCIERA']




##########################################################################################

col1, col2 = st.columns(2)

with col1:

    # Barra de búsqueda con opciones específicas
    area_seleccionada = st.selectbox(
        "Selecciona una opción:",
        ['C1','C2', 'S1','S2', 'L', 'M1','M2','E1']
    )


    # Procesar solo si hay selección
    if area_seleccionada:


        #Lista de modulos
        LMOD1l = ["LMOD1"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 2] == area_seleccionada].iloc[:, 0].tolist()
        LMOD2l = ["LMOD2"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 7] == area_seleccionada].iloc[:, 0].tolist()
        MMOD1l = ["MMOD1"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 3] == area_seleccionada].iloc[:, 0].tolist()
        MMOD2l = ["MMOD2"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 8] == area_seleccionada].iloc[:, 0].tolist()
        WMOD1l = ["WMOD1"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 4] == area_seleccionada].iloc[:, 0].tolist()
        WMOD2l = ["WMOD2"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 9] == area_seleccionada].iloc[:, 0].tolist()
        JMOD1l = ["JMOD1"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 5] == area_seleccionada].iloc[:, 0].tolist()
        JMOD2l = ["JMOD2"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 10] == area_seleccionada].iloc[:, 0].tolist()
        VMOD1l = ["VMOD1"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 6] == area_seleccionada].iloc[:, 0].tolist()
        VMOD2l = ["VMOD2"] + planeacion_bachillerato[planeacion_bachillerato.iloc[:, 11] == area_seleccionada].iloc[:, 0].tolist()
        
        LMOD1 = pd.DataFrame(LMOD1l)
        LMOD2 = pd.DataFrame(LMOD2l)
        MMOD1 = pd.DataFrame(MMOD1l)
        MMOD2 = pd.DataFrame(MMOD2l)
        WMOD1 = pd.DataFrame(WMOD1l)
        WMOD2 = pd.DataFrame(WMOD2l)
        JMOD1 = pd.DataFrame(JMOD1l)
        JMOD2 = pd.DataFrame(JMOD2l)
        VMOD1 = pd.DataFrame(VMOD1l)
        VMOD2 = pd.DataFrame(VMOD2l)
        
        df_nombres = pd.concat([LMOD1, LMOD2, MMOD1, MMOD2, WMOD1, WMOD2, JMOD1, JMOD2, VMOD1, VMOD2], ignore_index=True)

        # Crear un diccionario clave estudiante y valor grupo
        grupo_map = dict(zip(estudiantes['estudiante'], estudiantes['grupo']))
        grado_map = dict(zip(estudiantes['estudiante'], estudiantes['grado']))

        # Asignar grupo y grado correspondiente a cada estudiante de df_nombres
        df_nombres['1'] = df_nombres.iloc[:, 0].map(grupo_map)
        df_nombres['2'] = df_nombres.iloc[:, 0].map(grado_map)

        filasn, _ = df_nombres.shape

        #Crea siete vectores vacios tan grandes como la lista generada dos bloques anteriores, en el primero ira el bloque en el que esta el estudiante
        #en el segundo la Asignatura que debe ver y los cinco restantes corresponden respectivamente a si se marca el primero al primer desempeño
        #el segundo al segundo desempeño y asi sucesivamente hasta el quinto el quinto desempeño 

        df_bloque = pd.DataFrame([""] * filasn)
        df_asignatura = pd.DataFrame([""] * filasn)
        df_desempeño1 = pd.DataFrame([""] * filasn)
        df_desempeño2 = pd.DataFrame([""] * filasn)
        df_desempeño3 = pd.DataFrame([""] * filasn)
        df_desempeño4 = pd.DataFrame([""] * filasn)
        df_desempeño5 = pd.DataFrame([""] * filasn)


        if (area_seleccionada == 'M1') or (area_seleccionada =='M2'):
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                materias_especificas_6_7 = ['ARITMETICA','ANIMAPLANOS','GEOMETRIA', 'ESTADISTICA', 'DIBUJO TECNICO', 'SISTEMAS']
                materias_especificas_8_9 = ['ALGEBRA','ANIMAPLANOS', 'GEOMETRIA', 'ESTADISTICA', 'DIBUJO TECNICO', 'SISTEMAS']
                materias_especificas_10 =  ['TRIGONOMETRIA','ANIMAPLANOS', 'MATEMATICA FINANCIERA', 'ESTADISTICA', 'DIBUJO TECNICO', 'SISTEMAS']
                materias_especificas_11 =  ['CALCULO','ANIMAPLANOS', 'MATEMATICA FINANCIERA', 'ESTADISTICA', 'DIBUJO TECNICO', 'SISTEMAS']
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['ARITMETICA', 'ANIMAPLANOS','GEOMETRIA','MATEMATICA FINANCIERA', 'ALGEBRA', 'ESTADISTICA', 'DIBUJO TECNICO', 'SISTEMAS','TRIGONOMETRIA','CALCULO']

                #Esta parte del codigo hace que no planee nada de matematicas si ya completo matematicas pero no ha terminado el bloque
                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                
                    if grado_actual in ['4','5''6','7']:
                        notas_bloque_matematicas = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_6_7))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_matematicas) == 30):
                            desempeno_encontrado = True
                            break
                    if grado_actual in ['8','9']:
                        notas_bloque_matematicas = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_8_9))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_matematicas) == 30):
                            desempeno_encontrado = True
                            break
                    
                    if grado_actual == '10' :
                        notas_bloque_matematicas = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_10))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_matematicas) == 30):
                            desempeno_encontrado = True
                            break
                    
                    if grado_actual == '11' :
                        notas_bloque_matematicas = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_10))]
                        if (len(notas_bloque_completo) < 75) and (len(notas_bloque_matematicas) == 30):
                            desempeno_encontrado = True
                            break

                if desempeno_encontrado:
                        continue


                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    if grado_actual in ['4','5','6','7']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_6_7)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 30 and not desempeno_encontrado:
                            continue 
                        if longitud_bloque < 30 and not desempeno_encontrado:
                            for materia in materias_especificas_6_7:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 30 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 30 and not desempeno_encontrado:
                            for materia in materias_especificas_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual == '10':
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_10)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 30 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 30 and not desempeno_encontrado:
                            for materia in materias_especificas_10:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual == '11':
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 30 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 30 and not desempeno_encontrado:
                            for materia in materias_especificas_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break

        if  (area_seleccionada == 'C1') or (area_seleccionada =='C2'):
            
            for i in range(filasn):
                
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Biología', 'QUIMICA', 'MEDIO AMBIENTE', 'FISICA']
                asignaturas_11 = ['QUIMICA', 'MEDIO AMBIENTE', 'FISICA']

                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                
                    if grado_actual in ['4','5','6','7','8','9','10']:
                        notas_bloque_ciencias = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_ciencias) == 20):
                            desempeno_encontrado = True
                            break
                    
                    if grado_actual == '11' :
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas_11))]
                        if (len(notas_bloque_completo) < 75) and (len(notas_bloque_sociales) == 15):
                            desempeno_encontrado = True
                            break

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    
                    if grado_actual in ['4','5','6','7','8','9','10']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in asignaturas:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual == '11':
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 15 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 15 and not desempeno_encontrado:
                            for materia in asignaturas_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break
                    

        if area_seleccionada == 'S1':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                materias_especificas_6_7_8_9 = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA', 'FILOSOFIA']
                materias_especificas_10_11 = ['CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS', 'FILOSOFIA']
            
                        
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Historia', 'Geografía', 'CIENCIAS ECONOMICAS', 'Participación política','CIENCIAS POLITICAS','FILOSOFIA']

                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                
                    if grado_actual in ['4','5','6','7','8','9']:
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_6_7_8_9))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_sociales) == 20):
                            desempeno_encontrado = True
                            break
                    if grado_actual == '10':
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_10_11))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_sociales) == 15):
                            desempeno_encontrado = True
                            break
                    
                    if grado_actual == '11' :
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_10_11))]
                        if (len(notas_bloque_completo) < 75) and (len(notas_bloque_sociales) == 15):
                            desempeno_encontrado = True
                            break

                if desempeno_encontrado:
                        continue


                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    
                    
                    if grado_actual in ['4','5','6','7','8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_6_7_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in materias_especificas_6_7_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['10','11']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_10_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 15 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 15 and not desempeno_encontrado:
                            for materia in materias_especificas_10_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break


        if area_seleccionada == 'S2':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                materias_especificas_6_7_8_9 = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA', 'FILOSOFIA']
                materias_especificas_10_11 = ['CIENCIAS ECONOMICAS', 'CIENCIAS POLITICAS', 'FILOSOFIA']
            
                        
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Historia', 'Geografía', 'CIENCIAS ECONOMICAS', 'Participación política','CIENCIAS POLITICAS','FILOSOFIA']

                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                
                    if grado_actual in ['4','5','6','7','8','9']:
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_6_7_8_9))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_sociales) == 20):
                            desempeno_encontrado = True
                            break
                    if grado_actual == '10':
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_10_11))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_sociales) == 15):
                            desempeno_encontrado = True
                            break
                    
                    if grado_actual == '11' :
                        notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(materias_especificas_10_11))]
                        if (len(notas_bloque_completo) < 75) and (len(notas_bloque_sociales) == 15):
                            desempeno_encontrado = True
                            break

                if desempeno_encontrado:
                        continue

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    
                    
                    if grado_actual in ['4','5','6','7','8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_6_7_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in materias_especificas_6_7_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['10','11']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_10_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 15 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 15 and not desempeno_encontrado:
                            for materia in materias_especificas_10_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break


        if area_seleccionada == 'L':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas_6_7_8_9 = ['Comunicación y SISTEMAS simbólicos', 'Producción e interpretación de textos']
                asignaturas_10_11 = ['Comunicación y SISTEMAS simbólicos', 'Producción e interpretación de textos','METODOLOGIA']
                asignaturas = ['Comunicación y SISTEMAS simbólicos', 'Producción e interpretación de textos','METODOLOGIA']

                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                
                    if grado_actual in ['4','5','6','7','8','9']:
                        notas_bloque_lenguaje = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas_6_7_8_9))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_lenguaje) == 10):
                            desempeno_encontrado = True
                            break
                    if grado_actual in ['10']:
                        notas_bloque_lenguaje = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas_10_11))]
                        if (len(notas_bloque_completo) < 80) and (len(notas_bloque_lenguaje) == 15):
                            desempeno_encontrado = True
                            break
                    if grado_actual in ['11']:
                        notas_bloque_lenguaje = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas_10_11))]
                        if (len(notas_bloque_completo) < 75) and (len(notas_bloque_lenguaje) == 15):
                            desempeno_encontrado = True
                            break

                if desempeno_encontrado:
                        continue

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    if grado_actual in ['4','5','6','7','8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas_6_7_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 10 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 10 and not desempeno_encontrado:
                            for materia in asignaturas_6_7_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['10','11']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas_10_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 15 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 15 and not desempeno_encontrado:
                            for materia in asignaturas_10_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break        
        df_horario = pd.concat([df_nombres, df_bloque, df_asignatura, df_desempeño1, df_desempeño2, df_desempeño3, df_desempeño4, df_desempeño5], ignore_index=True, axis=1)

        for i in range(len(df_horario)):
            for k in range(i + 1, len(df_horario)):
                if df_horario.iloc[i, 0] == df_horario.iloc[k, 0]:
                    if 'X' in df_horario.iloc[i].values:
                        b = df_horario.iloc[i].eq('X').idxmax()
                        if b + 1 < len(df_horario.columns):
                            df_horario.iloc[k, b + 1] = 'X'
                            for col in range(5, b + 1):
                                df_horario.iloc[k, col] = np.nan
                    break

        if area_seleccionada == 'M1':
            adicionar = ['LIC-M1','OLIMPIADAS','SIMULACRO-M1','PG-M1']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        if area_seleccionada == 'M2':
            adicionar = ['LIC-M2','OLIMPIADAS','SIMULACRO-M2','PG-M2','SABER-M2']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)


        
        
        if area_seleccionada == 'C2':
            adicionar = ['LIC-C2','SIMULACRO-C2','PG-C2','SABER-C2']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        if area_seleccionada == 'C1':
            adicionar = ['LIC-C1','SIMULACRO-C1','PG-C1']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)


        if area_seleccionada == 'S1':
            adicionar = ['LIC-S1','KAIPOMUN','SIMONU','PG-S1']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        if area_seleccionada == 'S2':
            adicionar = ['LIC-S2','KAIPOMUN','SIMONU','PG-S2','SABER-S2']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        if area_seleccionada == 'L':
            adicionar = ['LIC-L','SABER-L','PG-L']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_bachillerato.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'L':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'L.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'M.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'W.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'J.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'V.1':
                        lista_del_modulo = planeacion_bachillerato[planeacion_bachillerato[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)


        st.subheader("F1")
        st.write(df_horario)

    # Diccionario de tablas según área
    tablas_por_area = {
        "Sociales 1": "bachillerato_s1",
        "Sociales 2": "bachillerato_s2",
        "Matemáticas 1": "bachillerato_m1",
        "Matemáticas 2": "bachillerato_m2",
        "Lenguaje": "bachillerato_l",
        "Ciencias 1": "bachillerato_c1",
        "Ciencias 2": "bachillerato_c2",
        "Inglés": "bachillerato_e1" 
    }

    
    # Área seleccionada (ya la tienes de tu selectbox inicial)
    area_visualizacion = st.selectbox("Selecciona un área para ver la tabla:", list(tablas_por_area.keys()))

    tabla = tablas_por_area.get(area_visualizacion)

    if tabla:
        try:
            engine = crear_engine()
            with engine.connect() as conn:
                # Usar text() para el query
                query = text(f"SELECT fecha, estudiante, grado, docente,asignatura, bloque, periodo, etapa, calificacion  FROM {tabla} WHERE procesamiento = 'NO' ORDER BY fecha DESC")
                result = conn.execute(query)
                data = result.fetchall()
                cols = result.keys()  # nombres de columnas

            # Mostrar la tabla en Streamlit
            df = pd.DataFrame(data, columns=cols)
            st.write(f"Tabla: {tabla}")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Ocurrió un error al cargar la tabla: {e}")
    else:
        st.warning("Área no válida seleccionada")


with col2:
    # Barra de búsqueda con autocompletado
    estudiante_seleccionado = st.selectbox(
        "Selecciona un estudiante:",
        estudiantes['estudiante'].unique()
    )

    # Definir el orden personalizado para etapa
    orden_etapas = {"D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5}
    # Nombres de las columnas
    columnas_personalizadas = [f"A{i}" for i in range(1,6)] + [f"B{i}" for i in range(1,6)] + [f"C{i}" for i in range(1,6)] + [f"D{i}" for i in range(1,6)]

    # Procesar solo si hay selección
    if estudiante_seleccionado and area_seleccionada in ['C1','C2','S1','S2','L','M1','M2','E1']:

        # Filtrar la base principal por el estudiante seleccionado
        grado = estudiantes.loc[estudiantes['estudiante'] == estudiante_seleccionado, 'grado'].values[0]
        grado = str(grado)

        #aqui se crea el f5 de acuerdo al area si el grado es sexto o septimo

        if grado in ['4','5','6', '7'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_6_7), 20), "", dtype=str), index=ciencias_6_7, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['4','5'] and area_seleccionada in ['S1', 'S2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_4_5), 20), "", dtype=str), index=sociales_4_5, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones


        if grado in ['6', '7'] and area_seleccionada in ['S1', 'S2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_6_7), 20), "", dtype=str), index=sociales_6_7, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones


        if grado in ['4','5'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_4_5), 20), "", dtype=str), index=lenguaje_4_5, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones



        if grado in ['6','7'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_6_7), 20), "", dtype=str), index=lenguaje_6_7, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['4','5','6', '7'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_6_7), 20), "", dtype=str), index=matemati_6_7, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones


        ########################################## AQUI SE CREA EL F5 SI EL grado ES OCTAVO O NOVENO

        if grado in ['8', '9'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_8_9), 20), "", dtype=str), index=ciencias_8_9, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['8', '9'] and area_seleccionada in ['S1', 'S2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_8_9), 20), "", dtype=str), index=sociales_8_9, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['8','9'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_8_9), 20), "", dtype=str), index=lenguaje_8_9, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['8', '9'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_8_9), 20), "", dtype=str), index=matemati_8_9, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones


        ######################## AQUI SE CREA EL F5 SI EL grado ES DECIMO

        if grado in ['10'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_10), 20), "", dtype=str), index=ciencias_10, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['10'] and area_seleccionada in ['S1', 'S2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_10), 20), "", dtype=str), index=sociales_10, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['10'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_10), 20), "", dtype=str), index=lenguaje_10, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['10'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_10), 20), "", dtype=str), index=matemati_10, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones


        ######################################## AQUI SE CREA EL F5 SI EL grado ES 11

        if grado in ['11'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_11), 20), "", dtype=str), index=ciencias_11, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['11'] and area_seleccionada in ['S1', 'S2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_11), 20), "", dtype=str), index=sociales_11, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['11'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_11), 20), "", dtype=str), index=lenguaje_11, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['11'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_11), 20), "", dtype=str), index=matemati_11, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        ######################################## AQUI SE CREA EL F5 SI EL AREA ES INGLES

        if area_seleccionada in ['E1']:
            F5_2 = pd.DataFrame(np.full((len(ingles), 20), "", dtype=str), index=ingles, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas_ingles[ (notas_ingles['estudiante'] == estudiante_seleccionado) & (notas_ingles['grado'] == grado) & (notas_ingles['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

    st.subheader("Notas")
    st.write(F5_2)

    ############################# Parte de ingresar notas

    # Lista de areas
    materias = ["Matemáticas 1","Matemáticas 2", "Lenguaje", "Inglés", "Ciencias 1","Ciencias 2", "Sociales 1", "Sociales 2",'Ingles']

    

    # Selectbox para materia
    area = st.selectbox("Area:", materias)

    ##################################################CAMBIAR CADA PERIODO ####################################
    periodo_seleccionado = '4'

    # Fijar zona horaria y seleccionar fecha actual
    bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(bogota).date()  # solo día, mes, año

    st.write(f"Fecha del registro: {fecha_actual}")
    st.write(f"Periodo actual: {periodo_seleccionado}")

    # --- Formulario ---
    with st.form("formulario_estudiante"):
        # Diccionario {estudiante: grado}
        estudiantes_dict = dict(zip(estudiantes["estudiante"], estudiantes["grado"]))

        # Grado automático según estudiante
        grado = estudiantes_dict[estudiante_seleccionado]
        st.write(f"Grado del estudiante: {grado}")

        ### Asignaturas Segun el Area

        if area == "Ciencias 1":
            asignatura = st.selectbox("Asignatura", ciencias_global)
        elif area == "Ciencias 2":
            asignatura = st.selectbox("Asignatura", ciencias_global)
        elif area == "Sociales 1":
            asignatura = st.selectbox("Asignatura", sociales_global)
        elif area == "Sociales 2":
            asignatura = st.selectbox("Asignatura", sociales_global)
        elif area == "Lenguaje":
            asignatura = st.selectbox("Asignatura", lenguaje_global)
        elif area == "Matemáticas 1":
            asignatura = st.selectbox("Asignatura", matematicas_global)
        elif area == "Matemáticas 2":
            asignatura = st.selectbox("Asignatura", matematicas_global)
        elif area == "Inglés":
            asignatura = st.selectbox("Asignatura", ingles)
        else:
            asignatura = None  # En caso de que no se haya escogido área
            
        # --- Otros campos ---
        bloque = st.selectbox("Bloque", ["A", "B", "C", "D"])
        etapa = st.selectbox("Etapa", ["D1", "D2", "D3", "D4", "D5"])
        calificacion = st.number_input("Calificación", min_value=3.6, max_value=5.0, step=0.1)

        # Docente y tabla según área
        area_info = {
            "Sociales 1": ("ALEJANDRO M", "bachillerato_s1"),
            "Sociales 2": ("CAMILO G", "bachillerato_s2"),
            "Matemáticas 1": ("ALEJANDRO R", "bachillerato_m1"),
            "Matemáticas 2": ("JORGE", "bachillerato_m2"),
            "Lenguaje": ("JULIANNA", "bachillerato_l"),
            "Ciencias 1": ("SANDRA", "bachillerato_c1"),
            "Ciencias 2": ("ANA S", "bachillerato_c2"),
            "Inglés": ("VANESSA", "bachillerato_e1"),
        }

        docente, tabla = area_info.get(area, ("Desconocido", None))
        st.write(f"Docente: {docente}")

        # --- Botón de submit ---
        submitted = st.form_submit_button("Guardar")

        if submitted:
            if asignatura is None or tabla is None:
                st.warning("Selecciona un área válida primero")
            else:
                try:
                    engine = crear_engine()
                    
                    with engine.connect() as conn:
                        query = text(f"""
                            INSERT INTO {tabla} (fecha, estudiante, grado, docente, asignatura, bloque, periodo, etapa, calificacion)
                            VALUES (:fecha, :estudiante, :grado, :docente, :asignatura, :bloque, :periodo, :etapa, :calificacion)
                        """)
                        
                        # Ejecutar con parámetros nombrados (más seguro y legible)
                        conn.execute(query, {
                            'fecha': fecha_actual,
                            'estudiante': estudiante_seleccionado,
                            'grado': grado,
                            'docente': docente,
                            'asignatura': asignatura,
                            'bloque': bloque,
                            'periodo': periodo_seleccionado,
                            'etapa': etapa,
                            'calificacion': calificacion
                        })
                        
                        # Hacer commit de la transacción
                        conn.commit()
                    
                    st.success(f"Registro guardado correctamente en {tabla} ✅")
                    
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")

    

    