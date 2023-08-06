import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
class analizar_datos(generar_datos):
    """
    Clase que hereda la clase generar_datos
    Genera descriptivos y visualizaciones de los datos metereológicos. 

    """
    def __init__(self, provincia,api_key,out_path='.'):
        """ inicializar los atributos del objeto. 
        Ejecuta tambien el método heredado extraer info para guardar como atributo 
        los datos en formato json. 

        Atributos heredados
        -------------------
            provincia : str. Obligatorio.
                Nombre de la provincia de la que se quieren obtener los datos metereológicos
            api_key : str. Obligatorio.
                La llave necesaria para acceder a la API de OpenWeatherMap.
        
        Atributos
        ----------
            out_path : str. 
                No obligatorio. Por defecto, ubicación actual. 
                Directorio para guardar las visualizaciones que se generan. 
                En caso de no existir el directorio, se pone por defecto el directorio actual. 
        """  
        self.out_path = out_path
        
        super().__init__(provincia, api_key)
        super().extraer_info()
    
    @property
    def out_path(self):
        return self.__out_path
    
    @out_path.setter
    def out_path(self, out_path):
        if os.path.isdir(out_path):
            self.__out_path = out_path
        else:
            self.__out_path = '.'


    def descriptivos(self,variable = 'todos'):
        """Genera los descriptivos de las variables metereológicos.
        Args:
        -----
            variable: (str)
            No obligatoria.
            Por defecto: todos. Otras opciones: temperatura, humedad, viento, precipitacion, cielo.
            - Por defecto: 
                Genera los descriptivos de todas las variables. 
            - Otras opciones:
                Genera los descriptivos de la variable seleccionada.
            
            Obtiene los datos de los métodos heredados. 

        Returns:
        ---------
            descrip : Pandas DataFrame
        """

        if variable == 'todos':
            temp = super().temperatura()
            hume = super().humedad()
            vient = super().viento()
            precpt = super().precipitacion()
            cielo = super().cielo()
            df = pd.DataFrame({'temperatura':temp, 'humedad':hume, 'precipitacion':precpt[-len(temp):],'viento':vient, 'cielo':cielo})
            descrip = df.describe(), df['cielo'].describe()
        else:
            bar = getattr(super(), variable)
            descrip = (pd.Series(bar())).describe()
        return descrip
    
    def boxplots(self,variable = 'todos'):
        """Genera boxplots (visualizaciones) de las variables metereológicas.
        Args:
        -----
            variable: (str)
            No obligatoria.
            Por defecto: todos. Otras opciones: temperatura, humedad, viento, precipitacion, cielo.
            - Por defecto: 
                Genera una figura de múltiples boxplots correspondientes a las variables. 
            - Otras opciones:
                Genera una figura, un boxplot, de la variable seleccionada.
            
            Obtiene los datos de los métodos heredados. 

        Returns:
        --------
            fig : figura de matplotlib
        """
        if variable == 'todos':
            temp = super().temperatura()
            hume = super().humedad()
            vient = super().viento()
            precpt = super().precipitacion()
            df = pd.DataFrame({'temp':temp, 'humedad':hume, 'preciptc':precpt[-len(temp):],'viento':vient})
            
            fig1, ax1 = plt.subplots()
            sns.boxplot(data= df, orient = 'h', ax=ax1)
            ax1.set_title('TIEMPO EN %s'%self.provincia)
            fig1.savefig(os.path.join(self.out_path,'boxplots_%s.png'%variable))
        else:
            bar = getattr(super(), variable)
            serie = (pd.Series(bar()))
            fig1, ax1 = plt.subplots()
            sns.boxplot(y= serie, ax=ax1)
            ax1.set_title(variable)
            fig1.savefig(os.path.join(self.out_path,'boxplot_%s.png'%variable))
        return fig1

    def lineas(self,variable = 'todos'):
        """Genera gráficos de líneas de las variables metereológicas.
        Args:
        -----
            variable: (str)
            No obligatoria.
            Por defecto: todos. Otras opciones: temperatura, humedad, viento, precipitacion, cielo.
            - Por defecto: 
                Genera una figura de múltiples gráficos de líneas correspondientes a las variables. 
            - Otras opciones:
                Genera una figura, un gráfico de líneas, de la variable seleccionada.
            
            Obtiene los datos de los métodos heredados. 

        Returns:
        ---------
            fig : figura de matplotlib
        """
        if variable == 'todos':
            temp = super().temperatura()
            hume = super().humedad()
            vient = super().viento()
            precpt = super().precipitacion()
            now = datetime.now() - timedelta(hours=48)
            horas = [now + timedelta(hours=n) for n in range(48)]
            df = pd.DataFrame({'hora':horas, 'temp':temp, 'humedad':hume, 'preciptc':precpt[-len(temp):],'viento':vient})
            fig1, ax1 = plt.subplots(4, figsize=(12, 8))
            ax1[0].plot(df["hora"], df["temp"], color = 'red')
            ax1[0].set_title("Temperatura")
            ax1[1].plot(df["hora"], df["humedad"], color = 'green')
            ax1[1].set_title("Humedad")
            ax1[2].plot(df["hora"], df["preciptc"], color = 'blue')
            ax1[2].set_title("Precipitación") ##es en minutos??
            ax1[3].plot(df["hora"], df["viento"], color = 'gray')
            ax1[3].set_title("Viento")
            fig1.tight_layout()
            fig1.savefig(os.path.join(self.out_path,'lineas_%s.png'%variable))
        else:
            bar = getattr(super(), variable)
            serie = (pd.DataFrame(bar())).rename(columns={0:variable})
            now = datetime.now() - timedelta(hours=48)
            serie["hora"]=[now + timedelta(hours=n) for n in range(48)]
            fig1, ax1 = plt.subplots(figsize=(12, 4))
            ax1.plot(serie["hora"], serie[variable])
            ax1.set_title(variable)
            fig1.savefig(os.path.join(self.out_path,'linea_%s.png'%variable))
        return fig1

    def barras(self):
        """Genera gráfico de barras del estado del cielo de las últimas 48 horas. 

        Returns:
        --------
            fig : figura de matplotlib
        """
        cielo = pd.Series(super().cielo()).value_counts()
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        ax1.bar(cielo.index, cielo)
        ax1.set_title('Estados de cielo en los últimos 2 días en %s'%self.provincia)
        fig1.savefig(os.path.join(self.out_path,'barra_cielo.png'))
        return fig1

    
