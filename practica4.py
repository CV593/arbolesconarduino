from tkinter import Tk, Canvas
import serial
from serial.tools.list_ports import comports
from threading import Thread
from time import sleep

valor_potenciometro = 0
estado_leds = [0, 0, 0]
estado_botones = [0, 0, 0]
color = ["grey", "blue", "green"]
orden = ["InOrden", "PosOrden", "PreOrden"]
caracter_recibido = False
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
arbol = Nodo('B')
arbol.izquierda = Nodo('C') # type: ignore
arbol.derecha = Nodo('D') # type: ignore

def update_from_arduino():
    global valor_potenciometro
    global estado_botones
    global caracter_recibido
    while True:
        if puerto.in_waiting:
            data = puerto.readline().strip().decode()
            values = data.split(',')
            if len(values) >= 4:
                if values[0]:
                    pot_value = values[0]
                else:
                    pot_value = 0
                valor_potenciometro = pot_value
                draw()
                if int(values[1]) == 1:
                    inorden(arbol)
                elif int(values[2]) == 1:
                    posorden(arbol)
                elif int(values[3]) == 1:
                    preorden(arbol)
                sleep(0.1)
                enviar_a_arduino("E")
                enviar_a_arduino("A")
        

def inorden(nodo):
    if nodo is not None:
        enviar_a_arduino(str(nodo.valor))
        sleep(1)
        inorden(nodo.izquierda)
        inorden(nodo.derecha)

def posorden(nodo):
    if nodo is not None:
        posorden(nodo.izquierda)
        posorden(nodo.derecha)
        enviar_a_arduino(str(nodo.valor))
        sleep(1)

def preorden(nodo):
    if nodo is not None:
        enviar_a_arduino(str(nodo.valor))
        sleep(1)
        preorden(nodo.izquierda)
        preorden(nodo.derecha)

def draw():
    global estado_leds
    global estado_botones
    global valor_potenciometro
    canvas.delete("all")
    canvas.create_oval(250, 50, 350, 150, fill=color[0] if estado_leds[0] == 1 else "white", tags=("led1",))
    for i in range(2):
        x = 100 + i * 300
        canvas.create_oval(x, 200, x + 100, 300, fill=color[i + 1] if estado_leds[i + 1] == 1 else "white", tags=("led" + str(i + 2),))
    for i in range(3):
        x = 50 + i * 150
        fill_color = "black" if estado_botones[i] == 1 else "white"
        tag = f"btn{i + 1}"
        canvas.create_rectangle(725, x, 825, x + 75, fill=fill_color, tags=(tag,))
        canvas.create_text(855, x + 37.5, text=f"Metodo\n{orden[i]}", anchor="w")
    draw_rectangle(str(valor_potenciometro))

def setup_serial():
    global puerto
    puerto = serial.Serial(comports()[0].device, 9600)
    sleep(2)

def draw_rectangle(data):
    global valor_potenciometro
    canvas.delete("rectangle")
    canvas.delete("text")
    canvas.create_rectangle(width - 150, height - 50, width - 50, height - 50 - int(valor_potenciometro) // 3, fill="grey", tags=("rectangle",))
    canvas.create_text(width - 100, height - 25, text=f"Valor del Potenciómetro: {data} ohm", fill="black", anchor="center", tags=("text",))

def enviar_a_arduino(valor):
    puerto.write(valor.encode())

root = Tk()
width = 1100
height = 500
root.geometry(f"{width}x{height}")
canvas = Canvas(root, width=width, height=height)
canvas.pack()
setup_serial()
valor_potenciometro = 0

# Crear un hilo para la comunicación serial
serial_thread = Thread(target=update_from_arduino, daemon=True)
serial_thread.start()

# Dibujar la interfaz gráfica inicial
draw()

# Ejecutar el loop principal de la interfaz gráfica
root.mainloop()

# Cerrar el puerto serial al salir
puerto.close()
