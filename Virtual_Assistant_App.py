import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opciones de voz / idioma.
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'


# voz a texto

def voz_a_texto():
    # almacenar recognizer en una variable.
    r = sr.Recognizer()

    # config. microfono
    with sr.Microphone() as origen:
        # tiempo de espera.
        r.pause_threshold = 0.8

        # informar que la grabacion empezo.
        print('Puedes hablar!')

        # guardar audio escuchado.
        audio = r.listen(origen)

        try:
            # buscar en google lo escuchado.
            pedido = r.recognize_google(audio, language='es-es')

            # prueba de que pudo ingresar.
            print(f'Dijiste: {pedido}')

            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print('No te he oido bien.')

            # devovler error
            return 'sigo esperando.'

        # en caso de no poder resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print('No te podido cumplir con tu peticion.')

            # devovler error
            return 'sigo esperando.'

        # error inesperado.
        except:
            # prueba de que no comprendio el audio
            print('Algo ha salido mal.')

            # devovler error
            return 'sigo esperando.'


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana.
def pedir_dia():
    # crear variable con datos de hoy.
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana.
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miercoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sabado',
                  6: 'Domingo'}

    # decir dia de la semana.
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar que hora es
def pedir_hora():
    # crear variable con datos de la hora.

    hora = datetime.datetime.now()
    hora = f'Son las {hora.hour} con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora.

    hablar(hora)


# funcion saludo inicial.
def saludo_inicial():
    # crear variable con datos de hora.
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour >= 18:
        momento = 'Buenas noches'
    elif hora.hour >= 12 or hora.hour < 18:
        momento = 'Buenas tardes'
    else:
        momento = 'Buen día'

    # decir saludo
    hablar(f'{momento}. Soy Malena. provengo de petare y me pica el culo, '
           f'y soy tu asistente personal. En que te puedo ayudar?')


# funcion central del asistente.
def activar_asistente():
    # activar saludo inicial.
    saludo_inicial()

    # variable de corte o finalizacion.
    comenzar = True

    # loop central
    while comenzar:

        # activar el microfono y guardar el pedido en un string.
        peticion = voz_a_texto().lower()

        if 'abrir youtube' in peticion:
            hablar('Abriendo yutub')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in peticion:
            hablar('Claro, estoy en eso.')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in peticion:
            pedir_dia()
            continue
        elif 'qué hora es' in peticion:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in peticion:
            hablar('Buscando...')
            peticion = peticion.replace('wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(peticion, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in peticion:
            hablar('Estoy en eso.')
            peticion = peticion.replace('busca en internet', '')
            pywhatkit.search(peticion)
            hablar(f'Mostrando resultados de {peticion}: ')

        elif 'te equivocaste' in peticion:
            hablar('Siento el haberme equivocado, ¿puedes repetirme tu petición una vez más?')

        elif 'quiero que reproduzcas' in peticion:
            hablar('Claro!, enseguida estoy en eso.')
            pywhatkit.playonyt(peticion)
            continue
        elif 'broma' in peticion:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in peticion:
            accion = peticion.split('de')[-1].strip()
            cartera = {'apple': 'APPL', 'amazon': 'AMZN', 'google': 'GOOGL'}

            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'El precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('No la he podido encontrar.')
        elif 'adiós' in peticion:
            hablar('Hasta luego.')
            break


activar_asistente()
