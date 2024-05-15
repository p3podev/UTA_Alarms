import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import telepot
import time



# Configuración de los pines
led_pin1 = 7 # Número de pin GPIO para el primer LED
led_pin2 = 5  # Número de pin GPIO para el segundo LED

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

# Configuración del bot de Telegram
telegram_token = "6010623366:AAFfPQxMKitDO1SIzUCY173KRf2a3x6odsY"
chat_id = "-955084563"

# Funciones para encender y apagar los LEDs

    
def encender_led(pin):
    GPIO.output(pin, GPIO.HIGH)

def apagar_led(pin):
    GPIO.output(pin, GPIO.LOW)
    
    
# Función de callback que se ejecuta cuando se recibe un mensaje MQTT   
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    partes= payload.split(";")
    print(partes)
    #mensaje_ubi = (f"Mensaje recibido en el tema {topic}:{payload}")
    #print(mensaje_ubi)
    
    if topic == "mqtt/led":
        if partes[0] == "1":
            encender_led(led_pin1)
            enviar_mensaje_telegram("Aviso1")
            enviar_mensaje_telegram(partes[1])
            time.sleep(5) # Mantener el LED encendido durante 10 segundos
            apagar_led(led_pin1)
            
            client.publish("mqtt/led", "0")

    elif topic == "mqtt/led2":
        if partes[0] == "1":
            encender_led(led_pin2)
            enviar_mensaje_telegram("Aviso2")
            enviar_mensaje_telegram(partes[1])
            time.sleep(5)  # Mantener el LED encendido durante 10 segundos
            apagar_led(led_pin2)
            client.publish("mqtt/led2", "0")
    #elif topic == "mqtt/ubicacion":
        #enviar_mensaje_telegram(payload)
    
# Función para enviar un mensaje al grupo de Telegram
def enviar_mensaje_telegram(mensaje):
    bot = telepot.Bot(telegram_token)
    bot.sendMessage(chat_id, mensaje)

# Configuración del cliente MQTT
client = mqtt.Client()
broker = "broker.hivemq.com"
port = 1883

# Configuración de la función de callback
client.on_message = on_message

# Conexión al broker MQTT y suscripción a los temas
client.connect(broker, port, 60)
client.subscribe("mqtt/led")
client.subscribe("mqtt/led2")
client.subscribe("mqtt/ubicacion")

# Bucle principal para mantener la conexión MQTT y procesar los mensajes
client.loop_start()

# Mantener el programa en ejecución
try:
    while True:
        # Simulación de otra tarea o lógica del programa
        time.sleep(1)

except KeyboardInterrupt:
    pass

# Finalización del programa y limpieza de los pines GPIO
client.loop_stop()
GPIO.cleanup()
