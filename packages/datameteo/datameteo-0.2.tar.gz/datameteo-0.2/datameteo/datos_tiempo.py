
import json
import requests
from geopy.geocoders import Nominatim


class generar_datos():
    """ Obtiene datos metereológicos de las 48h previas a través de la API de OpenWeatherMap."""        
    def __init__(self, provincia, api_key):
        """ inicializar los atributos del objeto
        Atributos
        ----------
        provincia : str. Obligatorio
            Nombre de la provincia de la que se quieren obtener los datos metereológicos
        api_key : str. Obligatorio
            La llave necesaria para acceder a la API de OpenWeatherMap.
        __url0:
            Variable encapsulada. Es el url para efectuar la descarga de los datos.
        """        
        self.provincia = provincia
        self.api_key = api_key
        self.__url0 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric"

    @property
    def url0(self):
        return self.__url0
    
    def coordenadas(self):
        """Proporciona la latitud y longitud de la provincia mediante la API Nominatim.
        Returns:
        --------
            lat : float
            log : float
        """
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(self.provincia)
        lat, lon = location.latitude, location.longitude
        return lat, lon

    def extraer_info(self):
        """Llama a la función de coordeanadas para obtener las coordenadas.
        A partir de la latitud y longitud que la función devuelve una petición a 
        OperWeatherMap para obtener los datos en formato json. Si la petición no es posible
        salta un error de falta de conexión a internet.

        Returns:
        ---------
            data : json
            Información metereológica en formato json. 
        """

        lat, lon = self.coordenadas()
        url = self.__url0 % (lat, lon, self.api_key)
        try:
            response = requests.get(url)
            data = json.loads(response.text)
            self.data = data
            return data
        except:
            "No hay conexión a internet"

    def temperatura(self):
        """Genera una lista horaria de la temperatura en grados ºC de las últimas 48 horas a partir 
        del json data.

        Returns:
        --------
            temp : list of float
            Una lista de floats correspondiente a las temperaturas. 
        """
        temp = [(info['temp']) for info in self.data['hourly']]
        return temp

    def humedad(self):
        """Genera una lista horaria de la humedad en g/m^3 de las últimas 48 horas a partir 
        del json data.

        Returns:
        --------
            hum : list of float
            Una lista de floats correspondiente a las humedades. 
        """
        hum = [(info['humidity']) for info in self.data['hourly']]
        return hum

    def viento(self):
        """Genera una lista horaria del viento (m/s) de las últimas 48 horas a partir 
        del json data.

        Returns:
        --------
            viento : list of float
            Una lista de floats correspondiente al viento. 
        """
        viento = [(info['wind_speed']) for info in self.data['hourly']]
        return viento

    def precipitacion(self):
        """Genera una lista en minutos de las precipitaciones en l/m2 a partir 
        del json data.

        Returns:
        --------
            prec : list of float
            Una lista de floats correspondiente a la precipitación. 
        """
        prec = [(info['precipitation']) for info in self.data['minutely']]
        return prec

    def cielo(self):
        """Genera una lista horaria del estado del cielo de las últimas 48 horas

        Returns:
        --------
            estado : list of str
            Una lista de strings correspondiente a los estados del cielo. 
        """
        estado = [(info['weather'][0]['description']) for info in self.data['hourly']]
        return estado


    def show(self):
        """Muestra en pantalla la descripción completa de los últimos valores recogidos 
        en OpenWeatherMap.

        Returns:
        --------
            None
        """
        print("""At this moment the weather in %s is the following: \nThe state of the sky is %s with %sºC and a humidity of %sg/m3. 
        The wind in this moment is %sm/s and during the day it has rained %sl/m2""" 
                %(self.provincia, self.cielo()[-1], self.temperatura()[-1], self.humedad()[-1], self.viento()[-1], sum(self.precipitacion())))


