import networkx as nx
import numpy as np#permite crear matrices muy grandes y usar funciones matematicas
import time
import math
import re
import os
import csv
import tkinter
import os #para obtener la ruta de directorio actual de trabajo
import matplotlib.pyplot as plt
from tkinter import messagebox
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import matplotlib.animation as animation
#agrego y quito celulas con el click izquierdo
#el boton reset solo funciona si esta en pausa el programa, solo checo si la celula esta en estado 1 en las matrices. Con esto se x,y que me serviran para dibujar una celula negra y actualizar el estado de la celula a 0
#PRIMERO SE EJECUTA TODO LO QUE ESTA EN FUNCIONES
global colorelegidoparaCelulaMuerta,colorelegidoparaCelulaViva,var_textNpz,ventanaSalvarConfiguracion,ventanaCargarConfiguracion
global nombreArchivoNpz,juego,estadoDelJuegoNuevo,estadoDelJuego,anchoCelula,altoCelula,numFilas,numColumnas,numeroEstado,celulasVivas
global listaEstados,listaCelulasVivasPorEstado,otroProceso,posicionDeBarra,bornMin,bornMax,supervivMin,supervivMax
global estadoDelJuegoNuevo2,estadoDelJuego2,anchoCelula2,altoCelula2,numFilas2,numColumnas2,numeroEstado2,celulasVivas2
global G,numeroEstado2
#Los objetos tkinter son globales. Pueden ser utilizados en cualquier funcion y no es necesario especificar con la palabra reservada "gglobal" en cada funcion
def agregarQuitarCelula(event):#al agregar o quitar celula, actualizamos matrices y el canvas
    canvas= event.widget 
    posY, posX = canvas.canvasx(event.x),canvas.canvasy(event.y)#donde se de click, obtenemos las posiciones x,y para las matrices
    #siendo el espacioCelularCanvas un canvas desplazable, la forma de obtener las coordenas al dar un click izquierdo sobre él se especifica en la linea 15 y 16
    #print(posX)#
    #print(posY)#
    global estadoDelJuegoNuevo,estadoDelJuego,anchoCelula,altoCelula,celulasVivas,colorelegidoparaCelulaViva,colorelegidoparaCelulaMuerta
    #y, x = int(np.floor(posY/altoCelula)), int(np.floor(posX/anchoCelula))
    y, x = int(np.floor(posY/anchoCelula)), int(np.floor(posX/altoCelula))#averiguamos la posicion en y,x de donde se dio clik, que va a corresponder a las matrices
    print(x)#salen coordenadas deltro del triangulo
    print(y)#
    if estadoDelJuegoNuevo[x,y] == 0:
        estadoDelJuegoNuevo[x,y]=1
        estadoDelJuego[x,y]=1
        celulasVivas+=1
        celula = espacioCelularCanvas.create_rectangle((y*anchoCelula) ,(x*altoCelula),((y+1)*altoCelula),((x+1)*altoCelula), fill = colorelegidoparaCelulaViva,outline="White")
    else:
        estadoDelJuegoNuevo[x,y]=0
        estadoDelJuego[x,y]=0
        celulasVivas-=1
        celula = espacioCelularCanvas.create_rectangle((y*anchoCelula) ,(x*altoCelula),((y+1)*altoCelula),((x+1)*altoCelula), fill = colorelegidoparaCelulaMuerta, outline="White")#fill = "black",outline=white

    etiquetaNESTADO.config(text=etiquetaNESTADO['text'])
    etiquetaNCELVIVAS.config(text=str(celulasVivas))
    #ventanaPrincipal.update()

def callback1(*args):#PARA COLOREAR CELULAS VIVAS
    global colorelegidoparaCelulaViva,estadoDelJuegoNuevo,numFilas,numColumnas
    colorelegidoparaCelulaViva=format(ColorDeCelulaViva.get())#ColorDeCelulaViva es StringVar de tkinter, creo que funciona aca arriba, si se declara allá abajo
    #print(colorelegidoparaCelulaViva)
    for posicionEnX in range(0,numFilas):
        for posicionEnY in range(0,numColumnas):
            #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
            if estadoDelJuegoNuevo[posicionEnX,posicionEnY] == 1:#dibujo un rectangulo negro
                celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva,outline="White")

def callback2(*args):#PARA COLOREAR CELULAS MUERTAS
    global colorelegidoparaCelulaMuerta,estadoDelJuegoNuevo,numFilas,numColumnas,anchoCelula,altoCelula
    colorelegidoparaCelulaMuerta=format(ColorDeCelulaMuerta.get())#ColorDeCelulaViva es StringVar de tkinter, creo que funciona aca arriba, si se declara allá abajo
    #print(colorelegidoparaCelulaViva)
    for posicionEnX in range(0,numFilas):
        for posicionEnY in range(0,numColumnas):
            #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
            if estadoDelJuegoNuevo[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
                celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White"  )

def callback3(*args):#PARA CAMBIAR EL TAMANIO DE LAS CELULAS
    global colorelegidoparaCelulaMuerta,colorelegidoparaCelulaViva,estadoDelJuegoNuevo,numFilas,numColumnas,anchoCelula,altoCelula
    tamElegidoCel=format(TamCelulas.get())#ColorDeCelulaViva es StringVar de tkinter, creo que funciona aca arriba, si se declara allá abajo
    anchoCelula=int(tamElegidoCel)
    altoCelula=int(tamElegidoCel)
    espacioCelularCanvas.delete(tkinter.ALL)#quitamos todas las células dentro del canvas
    espacioCelularCanvas.config(scrollregion=(0, 0, numColumnas*anchoCelula,numFilas*altoCelula))#vamos a hacer un scroll region de esta manera. El acho de cada celula por numero de columnas corresponde a que tanto vamos a poder desplazarnos horizontalmente en el canvas
    for posicionEnX in range(0,numFilas):
        for posicionEnY in range(0,numColumnas):           
            if estadoDelJuegoNuevo[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
                celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White"  )
            else:
            	celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva,outline="White")
    ventanaPrincipal.update()

def callback4(*args):#PARA REPINTAR EL CANVAS DEL ESPACIO CELUALR 2 QUE REFIEREN A LOS ARBOLES
    global estadoDelJuegoNuevo2,numFilas2,numColumnas2,anchoCelula2,altoCelula2,estadoDelJuego2
    tamUniArb=format(tamUniversoArboles.get())#ColorDeCelulaViva es StringVar de tkinter, creo que funciona aca arriba, si se declara allá abajo
    #print(tamUniArb)
    espacioCelularCanvas2.delete("all")
    if (tamUniArb=="2x2"):
        numColumnas2=2
        numFilas2=2
        anchoCelula2=(120/numColumnas2)
        altoCelula2=(120/numFilas2)
    elif (tamUniArb=="3x3"):
        numColumnas2=3
        numFilas2=3
        anchoCelula2=(120/numColumnas2)
        altoCelula2=(120/numFilas2)
    elif (tamUniArb=="4x4"):
        numColumnas2=4
        numFilas2=4
        anchoCelula2=(120/numColumnas2)
        altoCelula2=(120/numFilas2)
    elif (tamUniArb=="5x5"):
        numColumnas2=5
        numFilas2=5
        anchoCelula2=(120/numColumnas2)
        altoCelula2=(120/numFilas2)
    elif (tamUniArb=="6x6"):
        numColumnas2=6
        numFilas2=6
        anchoCelula2=(120/numColumnas2)
        altoCelula2=(120/numFilas2)

    ##
    #ESTADO INICIAL de los arboles. LOS REPINTAMOS
    estadoDelJuego2=np.zeros((numFilas2,numColumnas2))
    estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
    numeroEstado2=0
    celulasVivas2=0
    estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
    for posicionEnX in range(0,numFilas2):
        for posicionEnY in range(0,numColumnas2):
            #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
            if estadoDelJuego2[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
                celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
            else:
                celulasVivas2+=1
                celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaViva,outline=colorelegidoparaCelulaViva )

def callback5(*args):
	global estadoDelJuegoNuevo,numFilas,numColumnas,anchoCelula,altoCelula,estadoDelJuego
	tamUniLife=format(tamUniversoLife.get())
	espacioCelularCanvas.delete("all")

	
	if (tamUniLife=="100x100"):
		numFilas=100
		numColumnas=100
	elif (tamUniLife=="500x500"):
		numFilas=500
		numColumnas=500
	elif (tamUniLife=="1000x1000"):
		numFilas=1000
		numColumnas=1000
	elif (tamUniLife=="5000x5000"):
		numFilas=5000
		numColumnas=5000
	elif (tamUniLife=="10000x10000"):
		numFilas=10000
		numColumnas=10000
	
	
	espacioCelularCanvas.config(scrollregion=(0, 0, numColumnas*anchoCelula,numFilas*altoCelula))#vamos a hacer un scroll region de esta manera. El acho de cada celula por numero de columnas corresponde a que tanto vamos a poder desplazarnos horizontalmente en el canvas
	###############################SCROLLfin
	estadoDelJuego=np.zeros((numFilas,numColumnas))
	estadoDelJuegoNuevo=np.copy(estadoDelJuego)
	celulasVivas=0
	
	for posicionEnX in range(0,numFilas):
		for posicionEnY in range(0,numColumnas):
		    #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
		    if estadoDelJuego[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
		        celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
		    else:
		        celulasVivas+=1
		        celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva,outline=colorelegidoparaCelulaViva )

	
	etiquetaNCELVIVAS=tkinter.Label(ventanaPrincipal,text=str(celulasVivas))
	etiquetaNCELVIVAS.config(font=("Arial", 24))
	etiquetaNCELVIVAS.place(x= 900.0,y= 200.0)
	etiquetaNESTADO=tkinter.Label(ventanaPrincipal,text=str(0))
	etiquetaNESTADO.config(font=("Arial", 24))
	etiquetaNESTADO.place(x= 900.0,y= 100.0) 
	ventanaPrincipal.update()
	



   


def accionBtnPausar():
    global juego,otroProceso#especificamos que es global estas variables
    if juego==True and otroProceso==True:
        juego=False
        otroProceso=False#esta variable controla los botones
        #campoRegla.configure(state=tkinter.NORMAL)

def accionBtnCargar():
    global juego, celulasVivas,estadoDelJuegoNuevo,estadoDelJuego,anchoCelula,altoCelula,otroProceso,colorelegidoparaCelulaViva
    if (not juego) and (not otroProceso):#si esta en pausa el juego. os.getcwd() contiene una cadena que es la ruta del directorio de trabajo actual (ruta donde esta ubicado el programa)
        archivoNpy=tkinter.filedialog.askopenfilename(title="Open archive",initialdir=os.getcwd(),filetypes=[("Archives npy","*.NPY")])
        #print(archivoNpy)
        #el archivo Npy contiene una ruta hacia un archivo .npy, que en realidad se trata de una matriz de datos
        matrizConfigurada=np.load(archivoNpy)#cargamos ese archivoNPY a una matriz
        for posicionEnX in range(0,numFilas):
            for posicionEnY in range(0,numColumnas):
                #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                if matrizConfigurada[posicionEnX,posicionEnY] == 1:#dibujo un rectangulo blanco
                    celulasVivas+=1
                    celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva,outline=colorelegidoparaCelulaViva )
                    estadoDelJuegoNuevo[posicionEnX,posicionEnY]=1
                    estadoDelJuego[posicionEnX,posicionEnY]=1
    etiquetaNCELVIVAS.config(text=str(celulasVivas))

def accionBtnGuardar():#de la ventanaPrincipal
    global juego,otroProceso,celulasVivas
    if (not juego) and (not otroProceso) and (celulasVivas>0):#abrimos una ventana extra
        #ventanaPrincipal.withdraw()
        otroProceso=True
        global ventanaSalvarConfiguracion,var_textNpz
        ventanaSalvarConfiguracion=tkinter.Toplevel(ventanaPrincipal)#ventana principal es un objeto tkinter
        ventanaSalvarConfiguracion.title("Save configuration")
        ventanaSalvarConfiguracion.geometry("300x300")
        ventanaSalvarConfiguracion.protocol("WM_DELETE_WINDOW",accionCerrarVentanaSalvarConfiguracion)
        var_textNpz=tkinter.StringVar()# el texto ingresado en campo se va a guardar en una variable de tipo String
        campo=tkinter.Entry(ventanaSalvarConfiguracion,textvariable=var_textNpz,width=30).place(x=60,y=100)#NombreConf va especificado en el Entry
        botonGuardarConfiguracion=tkinter.Button(ventanaSalvarConfiguracion,command=lambda: accionGuardarNpy(),text="Save configuration",font=("Arial",10)).place(x=90,y=140)
        

def accionGuardarNpy():#ssi doy click en el boton de la ventana de salvar configuracion, ya no hay un proceso activo
    global nombreArchivoNpz,otroProceso,estadoDelJuegoNuevo,var_textNpz
    otroProceso=False
    #print(nombreConf.get())
    nombreArchivoNpz=var_textNpz.get()
    print(nombreArchivoNpz)
    np.save(nombreArchivoNpz,estadoDelJuegoNuevo)
    ventanaSalvarConfiguracion.destroy()

def accionCerrarVentanaSalvarConfiguracion():#ssi se cierra la ventana de salvar configuracion, ya no hay un proceso activo
    global otroProceso,ventanaSalvarConfiguracion
    otroProceso=False
    ventanaSalvarConfiguracion.destroy()

def realizarGraficas():
    global listaEstados,listaCelulasVivasPorEstado,otroProceso#usamos las variables globales
   	#plt es una grafia (plano cartesiano)
    plt.style.use('ggplot')
    plt.title("Live cell density")
    plt.xlabel("State")
    plt.ylabel("Living cells")
    plt.plot(listaEstados,listaCelulasVivasPorEstado,"o-",linewidth=1,label="Function")#USAR ESTA LINEA,en la grafica, colocamos la correspondencia de numero de estado-celulas vivas. Con "o-" indicamos que vamos a colocar puntos y estaran unidos con una linea
    #plt.plot(listaEstados,listaCelulasVivasPorEstado,linewidth=1,label="Function")
    #plt.plot(listaEstados,listaCelulasVivasPorEstado)
    plt.legend()#se refiere a la funcion
    plt.ion()
    plt.show()
    """
    plt.style.use('ggplot')
    fig, (ax1,ax2) = plt.subplots(2)
    fig.suptitle('Results')
    ax1.plot(listaEstados, listaCelulasVivasPorEstado)
    ax1.set_title("Live cell density")
    ax1.set_ylabel("Living cells")
    listaMedia=[]
    tamListaCelulasVivasPorEstado=0
    for i in listaCelulasVivasPorEstado:
    	tamListaCelulasVivasPorEstado+=1


    for i1 in range(0,tamListaCelulasVivasPorEstado):
    	i2=0
    	sumaParcial=0#media del actual estado
    	mediaActual=0
    	while i2<=i1:
    		sumaParcial+=listaCelulasVivasPorEstado[i2]
    		i2+=1
    	
    	mediaActual=(sumaParcial/i2)
    	listaMedia.append(mediaActual)


    ax2.plot(listaEstados, listaMedia)
    ax2.set_title("Media")
    ax2.set_xlabel("State")
    ax2.set_ylabel("Media")
    plt.show()
    """


def accionBtnReiniciar():#borramos celulas cuando juego = false, actualizamos las matrices, y agregamos celula negra en canvas
    global numFilas,numColumnas,estadoDelJuegoNuevo,estadoDelJuego,anchoCelula,altoCelula,celulasVivas,juego,otroProceso,colorelegidoparaCelulaMuerta
    if (not juego) and (not otroProceso):#if juego==False:
        for posicionEnX in range(0,numFilas):
            for posicionEnY in range(0,numColumnas):
                #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                if estadoDelJuegoNuevo[posicionEnX,posicionEnY] == 1:#dibujo un rectangulo negro
                    celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
                    estadoDelJuegoNuevo[posicionEnX,posicionEnY]=0
                    estadoDelJuego[posicionEnX,posicionEnY]=0
                    celulasVivas-=1
        
        etiquetaNCELVIVAS.config(text=str(celulasVivas))#esto forma parte del if
        ventanaPrincipal.update()

def accionBtnResultados():
    global juego
    if (not juego):#si juego es false (pausa el programa), se niega y juego es verdadero. Muestro grafica
        realizarGraficas()
        


def accionBtnReproducir():#Ejecuta el juego de la vida. Por cada iteracion, se actualizan las matrices y se dibujan las celulas (rectangulos) en el canvas espaciocelular
    global juego,otroProceso
    reglaValida=False
    if(len(regla.get())>0):
        reglaValida=validar(regla.get())
        if(reglaValida==False):
            messagebox.showinfo("Warning", "The rule is invalid")
    else:
        reglaValida=False
        messagebox.showinfo("Warning", "The string is empty")
    
    if (not juego) and (not otroProceso) and reglaValida:
        global colorelegidoparaCelulaMuerta,colorelegidoparaCelulaViva,estadoDelJuegoNuevo,estadoDelJuego,anchoCelula,altoCelula,numFilas,numColumnas,numeroEstado,celulasVivas,bornMin,bornMax,supervivMin,supervivMax,posicionDeBarra
        juego=True
        otroProceso=True
        informacionNacimiento=""
        informacionSupervivencia=""
        #print("La cadena "+cadenaEnMayusculas+" es valida")

        #obtenemos cadena para validar el nacimiento de una celula muerta (Extraemos lo que hay entre B y /)
        cadenaEnMayusculas=regla.get().upper()
        #messagebox.showinfo("Mayusculas", cadenaEnMayusculas)
        informacionBornInicio=cadenaEnMayusculas[1]
        informacionBornFin=cadenaEnMayusculas[posicionDeBarra-1]

        if(informacionBornInicio=='/' and informacionBornFin=='B'):
            #bornMin=1
            #bornMax=8
            informacionNacimiento="12345678"
        else:
            #bornMin=(ord(informacionBornInicio)-48)
            #bornMax=(ord(informacionBornFin)-48)
            informacionNacimiento=cadenaEnMayusculas[1:posicionDeBarra]#extraccion de subcadena (numeros) de la cadena regla desde el caracter 1 hasta antes de la posicionDebarra

        #print("\nBorn minimo: ",bornMin)
        #print("\nBorn maximo: ",bornMax)
        #messagebox.showinfo("Mayusculas", cadenaEnMayusculas)
        #obtenemos cadena para validar la supervivencia de una celula viva (Extraemos lo que hay entre S y hasta el final)
        posicionDeS=posicionDeBarra+1
        if((posicionDeS+1)==len(cadenaEnMayusculas)):#por ejemplo b26/s
            #supervivMin=1
            #supervivMax=8
            informacionSupervivencia="12345678"
        else:
            informacionSupervivencia=cadenaEnMayusculas[(posicionDeS+1):]#extraigo lo que hay despues de S hasta el final de la cadena
            
        #messagebox.showinfo("Cadena 1", informacionNacimiento)
        #messagebox.showinfo("Cadena 2", informacionSupervivencia)   
        #print("\nSuperviv minimo: ",supervivMin)
        #print("\nSuperviv maximo: ",supervivMax)
        #print("\n\nFuncion de transicion\n\n")
        #print("f("+str(bornMin)+","+str(bornMax)+","+str(supervivMin)+","+str(supervivMax)+")")

        #campoRegla.config(state='disabled')
        while juego:
            #celulasVivas=0
            espacioCelularCanvas.delete(tkinter.ALL)#clave para que sea rapido el programa. Borro todas las celulas dibujadas en el panel 
            if numeroEstado==0:
                #Dibujamos celulas
                estadoDelJuegoNuevo=np.copy(estadoDelJuego)
                celulasVivas=0
                for posicionEnX in range(0,numFilas):
                    for posicionEnY in range(0,numColumnas):
                        #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                        if estadoDelJuego[posicionEnX,posicionEnY] == 0:
                            celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
                        else:
                            celulasVivas+=1
                            celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva, outline=colorelegidoparaCelulaViva)#aqui cambio el color
                    #print(posicionEnX)#ESTO FORMA PARTE DEL PRIMER FOR
            else:
                estadoDelJuegoNuevo=np.copy(estadoDelJuego)
                #print("hola")
                celulasVivas=0
                #Visitamos cada posicion de la matriz "estadoDelJuego"
                for posicionEnX in range(0,numFilas):
                    for posicionEnY in range(0,numColumnas):
                        #contamos vecinos vivos
                        vecinasVivas= 0
                        limiteinferiorY=0
                        limitesuperiorY=0
                        if (posicionEnY+1)==numColumnas:#es el ultimo
                            limitesuperiorY=(posicionEnY)
                        else:
                            limitesuperiorY=(posicionEnY+1)

                        if (posicionEnY-1)>=0:
                            limiteinferiorY=(posicionEnY-1)
                        else:
                            limiteinferiorY=(posicionEnY)

                        
                        #analizamos celulas de en medeio
                        itposY=limiteinferiorY
                        while itposY<=limitesuperiorY:
                            if (itposY!=posicionEnY):
                                vecinasVivas=(vecinasVivas+estadoDelJuego[(posicionEnX)][itposY])  
                            itposY+=1
                            

                        #analizamos celulas de arriba
                        if (posicionEnX-1)>=0:
                            itposY=limiteinferiorY
                            while itposY<=limitesuperiorY:
                                vecinasVivas=(vecinasVivas+estadoDelJuego[(posicionEnX-1)][itposY]) 
                                itposY+=1        
                        
                        #analizamos celulas de abajo
                        if (posicionEnX+1)<numFilas:
                            itposY=limiteinferiorY
                            while itposY<=limitesuperiorY:
                                vecinasVivas=(vecinasVivas+estadoDelJuego[(posicionEnX+1)][itposY]) 
                                itposY+=1 

                        #FIN DEL CONTEO DE LAS CELULAS
                        #REGLAS
                        #tendria que cambiar por igual al ir analizando cadenas B/S (esta es igual a B12345678/S12345678)
                        #Creo que voy a partir la cadena BNUMEROS Y SNUMEROS
                        #Convierto vecinasVivas a cadena para usar la funcion re.search
                        vecinasVivas=int(vecinasVivas)#vecinas vivas al principio es un valor decimal, para arreglar eso, lo convertimos a entero
                        vecViv=str(vecinasVivas)
                        #messagebox.showinfo("Inf", vecViv)
                        #messagebox.showinfo("Inf", informacionNacimiento)
                        #messagebox.showinfo("Inf", informacionSupervivencia)  
                        numeroEncontradoNac=re.search(vecViv,informacionNacimiento)#numeroEncontrado
                        numeroEncontradoSup=re.search(vecViv,informacionSupervivencia)#numeroEncontrado
                        #print(numeroEncontradoNac)
                        #print("\n")
                        #print(numeroEncontradoSup)
                        #print("\n")
                        #Reglas
                        #messagebox.showinfo("Inf", numeroEncontradoNac)
                        #messagebox.showinfo("Inf", numeroEncontradoSup)
                        if estadoDelJuego[posicionEnX,posicionEnY]==0:#si la celula esta muerta 
                            if(numeroEncontradoNac is not None):#y si se hallo el numero vecViv en la cadena informacionNacimiento, nace esa celula muerta
                                estadoDelJuegoNuevo[posicionEnX,posicionEnY]=1    
                        elif estadoDelJuego[posicionEnX,posicionEnY]==1:#si la celula esta viva 
                            if(numeroEncontradoSup is None):#y si no se hallo el numero vecVic en la cadena informacionSupervivencia, muere esa celula viva
                                estadoDelJuegoNuevo[posicionEnX,posicionEnY]=0
                            
                        #FIN REGLAS    
                        #Creamos celulas y las coloreamos, basandonos en la la matriz de juego nuevo, que es la actualizada
                        if estadoDelJuegoNuevo[posicionEnX,posicionEnY]==0:
                            celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
                        else:
                            celulasVivas+=1
                            celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva, outline=colorelegidoparaCelulaViva )

            #Luego, actualizamos datos
            etiquetaNESTADO.config(text=str(numeroEstado))
            etiquetaNCELVIVAS.config(text=str(celulasVivas))
            #Llenamos array para las graficas
            listaEstados.append(numeroEstado)
            listaCelulasVivasPorEstado.append(celulasVivas)                
            numeroEstado+=1
            estadoDelJuego=np.copy(estadoDelJuegoNuevo)
            """
            plt.style.use('ggplot')
            plt.title("Live cell density")
            plt.xlabel("State")
            plt.ylabel("Living cells")
            #plt.plot(listaEstados,listaCelulasVivasPorEstado,"o-",linewidth=1,label="Function")#en la grafica, colocamos la correspondencia de numero de estado-celulas vivas. Con "o-" indicamos que vamos a colocar puntos y estaran unidos con una linea
            plt.scatter(listaEstados,listaCelulasVivasPorEstado,color="r")#
            plt.pause(0.05)
            plt.plot(listaEstados,listaCelulasVivasPorEstado,color="b",linewidth=1,label="Function")#lineas
            #plt.legend()#se refiere a la funcion
            plt.ion()#activa el modo interactivo. La grafica tiene el modo interactivo. Mientras se van actualizando los arrays,la grafica de puntos tambien lo haran. Esto lo permite el metodo ion. Metodo ion permite que el metodo show NO detenga la ejecucion del bucle
            plt.show()#mostramos el grafico que estara siempre
			
            """
            ventanaPrincipal.update()
            #espacioContenedorCelular.update()

def accionBtnReproducir2():
    global juego,otroProceso,numFilas2,numColumnas2,G,numeroEstado2

    reglaValida=False
    if(len(regla.get())>0):
        reglaValida=validar(regla.get())
        if(reglaValida==False):
            messagebox.showinfo("Warning", "The rule is invalid")
    else:
        reglaValida=False
        messagebox.showinfo("Warning", "The string is empty")
    
    if (not juego) and (not otroProceso) and reglaValida:
        global colorelegidoparaCelulaMuerta,colorelegidoparaCelulaViva,estadoDelJuegoNuevo2,estadoDelJuego2,anchoCelula2,altoCelula2,numFilas2,numColumnas2,numeroEstado2,celulasVivas2,bornMin,bornMax,supervivMin,supervivMax,posicionDeBarra
        juego=True
        otroProceso=True
        informacionNacimiento=""
        informacionSupervivencia=""
        #print("La cadena "+cadenaEnMayusculas+" es valida")

        #obtenemos cadena para validar el nacimiento de una celula muerta (Extraemos lo que hay entre B y /)
        cadenaEnMayusculas=regla.get().upper()
        #messagebox.showinfo("Mayusculas", cadenaEnMayusculas)
        informacionBornInicio=cadenaEnMayusculas[1]
        informacionBornFin=cadenaEnMayusculas[posicionDeBarra-1]

        if(informacionBornInicio=='/' and informacionBornFin=='B'):
            #bornMin=1
            #bornMax=8
            informacionNacimiento="12345678"
        else:
            #bornMin=(ord(informacionBornInicio)-48)
            #bornMax=(ord(informacionBornFin)-48)
            informacionNacimiento=cadenaEnMayusculas[1:posicionDeBarra]#extraccion de subcadena (numeros) de la cadena regla desde el caracter 1 hasta antes de la posicionDebarra

        #print("\nBorn minimo: ",bornMin)
        #print("\nBorn maximo: ",bornMax)
        #messagebox.showinfo("Mayusculas", cadenaEnMayusculas)
        #obtenemos cadena para validar la supervivencia de una celula viva (Extraemos lo que hay entre S y hasta el final)
        posicionDeS=posicionDeBarra+1
        if((posicionDeS+1)==len(cadenaEnMayusculas)):#por ejemplo b26/s
            #supervivMin=1
            #supervivMax=8
            informacionSupervivencia="12345678"
        else:
            informacionSupervivencia=cadenaEnMayusculas[(posicionDeS+1):]#extraigo lo que hay despues de S hasta el final de la cadena
            
        #messagebox.showinfo("Cadena 1", informacionNacimiento)
        #messagebox.showinfo("Cadena 2", informacionSupervivencia)   
        #print("\nSuperviv minimo: ",supervivMin)
        #print("\nSuperviv maximo: ",supervivMax)
        #print("\n\nFuncion de transicion\n\n")
        #print("f("+str(bornMin)+","+str(bornMax)+","+str(supervivMin)+","+str(supervivMax)+")")
        numNodos=pow(2,numFilas2*numColumnas2)
        print("Numero de nodos: "+str(numNodos))
        nodoActual=0
        ##solo aumento el nodo cuando
        G = nx.DiGraph() # crear un grafo
        listaCadenasGrafo=[]
        listaAtractores=[]
        

        #numeroEstado2=0
        #
        #campoRegla.config(state='disabled')
        rule=""
        if regla.get()=="B3/S23":
            rule="B3S23"
        elif regla.get()=="B2/S7":
            rule="B2S7"
        else:
            rule=regla.get()



        file=None
        file2=None
        if numNodos==16:
            file = open("D:/grafos2x2_"+rule+".txt", "w")
            file2 = open("D:/atractores2x2_"+rule+".txt", "w")
        elif numNodos==512:
            file = open("D:/grafos3x3_"+rule+".txt", "w")
            file2 = open("D:/atractores3x3_"+rule+".txt", "w")
        elif numNodos==65536:
            file = open("D:/grafos4x4_"+rule+".txt", "w")
            file2 = open("D:/atractores4x4_"+rule+".txt", "w")
        elif numNodos==33554432:
            file = open("D:/grafos5x5_"+rule+".txt", "w")
            file2 = open("D:/atractores5x5_"+rule+".txt", "w")
        #file.write("Primera línea" + os.linesep)#os.linesep es un salto de linea
        #file.write("Segunda línea")
        #file.close()

        while nodoActual<numNodos:
            #numDecInicial=nodoActual
            #G.add_node(str(numDecInicial))
            #celulasVivas=0
            #G.add_node(str(nodoActual))
            espacioCelularCanvas2.delete(tkinter.ALL)#clave para que sea rapido el programa. Borro todas las celulas dibujadas en el panel 
            numBits=(numFilas2*numColumnas2)
            cadenaBinInicial=(format(nodoActual,'0'+str(numBits)+'b'))#convierte numeros a su elemento binario correspondiente
            #
            #print("Cadena bin inicial: "+str(cadenaBinInicial))
            
            
            posicionCadenaBin=0
            #ESTADO INICIAL de las matrices de los arboles
            estadoDelJuego2=np.zeros((numFilas2,numColumnas2))
            estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
            #Pongo la cadena en la matriz
            for posicionEnX in range(0,numFilas2):
                for posicionEnY in range(0,numColumnas2):
                    #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                    if cadenaBinInicial[posicionCadenaBin] == "0":#dibujo un rectangulo negro
                        estadoDelJuego2[posicionEnX,posicionEnY]=0
                        posicionCadenaBin+=1

                    else:
                        estadoDelJuego2[posicionEnX,posicionEnY]=1
                        posicionCadenaBin+=1
            #
            #Guardo
            #print(estadoDelJuego2)
            estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
            #print(estadoDelJuegoNuevo2)#actualizada
           
            #print("Ancho celula2: "+str(anchoCelula2))
            #print("Alto celula2: "+str(altoCelula2))
            
            numeroEstado2=0
            celulasVivas2=0

            #PINTAMOS CELULAS
            for posicionEnX in range(0,numFilas2):
                for posicionEnY in range(0,numColumnas2):
                    #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                    if estadoDelJuego2[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
                        celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaMuerta,outline="Gray" )#fill = "black",outline="white" 
                    else:
                        celulasVivas2+=1
                        celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaViva,outline="Gray" )

            
            #Hasta aqui hemos inicializado el espacio en cadenas 0000,0001,...,1111 (en el caso de 2x2)
            banderaContinuidad=True
            listaCadenas=[]#esta lista contiene numeros decimales
            
            #listaCadenasAnterior=np.array([])
            #print("Tam lista cadenas: "+str(len(listaCadenas)))#muestra un 0

            while banderaContinuidad:
                
                
                espacioCelularCanvas2.delete(tkinter.ALL)#clave para que sea rapido el programa. Borro todas las celulas dibujadas en el panel 
                
                #estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
                #print("hola")
                celulasVivas2=0
                #Visitamos cada posicion de la matriz "estadoDelJuego"
                for posicionEnX in range(0,numFilas2):
                    for posicionEnY in range(0,numColumnas2):
                        #contamos vecinos vivos
                        vecinasVivas= 0
                        limiteinferiorY=0
                        limitesuperiorY=0
                        if (posicionEnY+1)==numColumnas2:#es el ultimo
                            limitesuperiorY=(posicionEnY)
                        else:
                            limitesuperiorY=(posicionEnY+1)

                        if (posicionEnY-1)>=0:
                            limiteinferiorY=(posicionEnY-1)
                        else:
                            limiteinferiorY=(posicionEnY)

                        
                        #analizamos celulas de en medeio
                        itposY=limiteinferiorY
                        while itposY<=limitesuperiorY:
                            if (itposY!=posicionEnY):
                                vecinasVivas=(vecinasVivas+estadoDelJuego2[(posicionEnX)][itposY])  
                            itposY+=1
                            

                        #analizamos celulas de arriba
                        if (posicionEnX-1)>=0:
                            itposY=limiteinferiorY
                            while itposY<=limitesuperiorY:
                                vecinasVivas=(vecinasVivas+estadoDelJuego2[(posicionEnX-1)][itposY]) 
                                itposY+=1        
                        
                        #analizamos celulas de abajo
                        if (posicionEnX+1)<numFilas2:
                            itposY=limiteinferiorY
                            while itposY<=limitesuperiorY:
                                vecinasVivas=(vecinasVivas+estadoDelJuego2[(posicionEnX+1)][itposY]) 
                                itposY+=1 

                        #FIN DEL CONTEO DE LAS CELULAS
                        #REGLAS
                        #tendria que cambiar por igual al ir analizando cadenas B/S (esta es igual a B12345678/S12345678)
                        #Creo que voy a partir la cadena BNUMEROS Y SNUMEROS
                        #Convierto vecinasVivas a cadena para usar la funcion re.search
                        vecinasVivas=int(vecinasVivas)#vecinas vivas al principio es un valor decimal, para arreglar eso, lo convertimos a entero
                        vecViv=str(vecinasVivas)
                        #messagebox.showinfo("Inf", vecViv)
                        #messagebox.showinfo("Inf", informacionNacimiento)
                        #messagebox.showinfo("Inf", informacionSupervivencia)  
                        numeroEncontradoNac=re.search(vecViv,informacionNacimiento)#numeroEncontrado
                        numeroEncontradoSup=re.search(vecViv,informacionSupervivencia)#numeroEncontrado
                        #print(numeroEncontradoNac)
                        
                        #print(numeroEncontradoSup)
                        
                        #Reglas
                        #messagebox.showinfo("Inf", numeroEncontradoNac)
                        #messagebox.showinfo("Inf", numeroEncontradoSup)
                        if estadoDelJuego2[posicionEnX,posicionEnY]==0:#si la celula esta muerta 
                            if(numeroEncontradoNac is not None):#y si se hallo el numero vecViv en la cadena informacionNacimiento, nace esa celula muerta
                                estadoDelJuegoNuevo2[posicionEnX,posicionEnY]=1    
                        elif estadoDelJuego2[posicionEnX,posicionEnY]==1:#si la celula esta viva 
                            if(numeroEncontradoSup is None):#y si no se hallo el numero vecVic en la cadena informacionSupervivencia, muere esa celula viva
                                estadoDelJuegoNuevo2[posicionEnX,posicionEnY]=0
                            
                        #FIN REGLAS    
                        #Creamos celulas y las coloreamos, basandonos en la la matriz de juego nuevo, que es la actualizada
                        if estadoDelJuegoNuevo2[posicionEnX,posicionEnY]==0:
                            celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaMuerta,outline="Gray" )#fill = "black",outline="white" 
                        else:
                            celulasVivas2+=1
                            celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaViva, outline="Gray" )
                
            
                print("Nodo o iteracion actual: "+str(nodoActual))
                #print("Representacion binaria: "+format(nodoActual,'0'+str(numBits)+'b'))
                #print("Matriz actual: ")
                #print(estadoDelJuego2)
                #print("Matriz nueva: ")
                #print(estadoDelJuegoNuevo2)
                #agrego nodos (el estado actual y el estado nuevo, ambos que estan en binario los pasamos a decimal)
                #FORMO LAS CADENAS
                cadBinEstadoActual=""
                cadBinEstadoNuevo=""
                for posicionEnX in range(0,numFilas2):
                    for posicionEnY in range(0,numColumnas2):
                        #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                        if estadoDelJuego2[posicionEnX,posicionEnY]==0:#dibujo un rectangulo negro
                            cadBinEstadoActual+="0"
                            

                        else:
                            cadBinEstadoActual+="1"
                            
                #
                for posicionEnX in range(0,numFilas2):
                    for posicionEnY in range(0,numColumnas2):
                        #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
                        if estadoDelJuegoNuevo2[posicionEnX,posicionEnY]==0:#dibujo un rectangulo negro
                            cadBinEstadoNuevo+="0"
                            

                        else:
                            cadBinEstadoNuevo+="1"
                #recorro matrices para formar cadenas
                #print("Cad bin actual estado actual: "+cadBinEstadoActual)
                #print("Cad bin nuevo estado nuevo: "+cadBinEstadoNuevo)
                decimalActual=int(cadBinEstadoActual,base=2)
                decimalNuevo=int(cadBinEstadoNuevo,base=2)
                #print("Decimal de Cad bin actual estado actual: "+str(decimalActual))
                #print("Decimal de Cad bin nuevo estado nuevo: "+str(decimalNuevo))
                
                G.add_node(str(decimalActual))
                G.add_node(str(decimalNuevo))
                #file.write(str(decimalActual)+"->"+str(decimalNuevo)+", ")
                
                #Funcion para guardar el par de nodos NODOA -> NODOB en el archivo .txt, (SIN QUE SE REPITAN)
                #Checo si el par de nodos NODOA -> NODOB esta en el conjunto (array o lista) de pares de nodos

                if (str(decimalActual)+"->"+str(decimalNuevo) in listaCadenasGrafo):
                	#print(str(decimalActual)+"->"+str(decimalNuevo))
                	#print(listaCadenasGrafo)
                	pass
                else:
                	file.write(str(decimalActual)+"->"+str(decimalNuevo)+", ")

                
                #arrayParNodos=[[decimalActual,decimalNuevo]]
                #writer = csv.writer(file)
                #writer.writerows(arrayParNodos)
    			#aniado arista (uno a uno, del estado viejo al nuevo)
                G.add_edge(str(decimalActual), str(decimalNuevo))
                listaCadenas.append(decimalActual)
                listaCadenasGrafo.append(str(decimalActual)+"->"+str(decimalNuevo))#ver si esto esta bien
                #print(listaCadenasGrafo)

                
                
                if numColumnas2==5 or numColumnas2==4 or numColumnas2==3 or numColumnas2==2:
                    #print(listaCadenas)
                    if len(listaCadenas)>1:
                    	posLC=0
                    	while (posLC<len(listaCadenas)):
                            if listaCadenas[posLC]==decimalActual:
                                #print("se encontro un ciclo")
                                if decimalActual in listaAtractores:
                                    pass
                                else:
                                    listaAtractores.append(decimalActual)
                                    file2.write(str(decimalActual)+",")
                                
                                banderaContinuidad=False
                                nodoActual+=1
                                break
                            else:
                                posLC+=1


                estadoDelJuego2=np.copy(estadoDelJuegoNuevo2)
                ventanaPrincipal.update()
                #print("----------------------------------------------------------")
                #espacioContenedorCelular.update()
                
            #FIN DEL WHILE INTERNO    



        juego=False
        otroProceso=False
        print("GRAFO GENERADO")
        file.close()
        file2.close()


def accionBtnVerArboles():
    global G
    nx.draw_kamada_kawai(G, node_size=500, width=0.5, with_labels=True,font_size=12)  # Dibujar el grafo G con una interfaz particular
    #nx.draw_random(G, node_size=10, width=0.5, with_labels=False,font_size=8)
    #nx.circular_layout(G, scale=1, center=None, dim=2)  # Dibujar el grafo G con una interfaz particular
    plt.axis("equal")  # Redimensionar los ejes a longitudes iguales
    plt.show()  # Mostrar el grado d-regular por pantalla
        

def validar(cadenaEnMayusculas):
    cadenaEnMayusculas=cadenaEnMayusculas.upper()
    print("Cadena a analizar: "+cadenaEnMayusculas)
    #Primera parte la cadena
    i=0
    if(cadenaEnMayusculas[i]=='B'):
        i=1
    else:#return false
        return False


    textoAEncontrar="/"

    textoEncontrado=re.search(textoAEncontrar,cadenaEnMayusculas)#devuelve None si no se encontro el texto "/"

    global posicionDeBarra

    posicionDeBarra=0
    if textoEncontrado is not None:
        #reglas+=1
        #print("Texto hallado /")
        posicionDeBarra=textoEncontrado.start()
        #print("Posicion: "+str(posicionDeBarra))
    else:
        return False


    caracterActual=ord(cadenaEnMayusculas[i])
    caracterSiguiente=ord(cadenaEnMayusculas[i+1])
    while(i<posicionDeBarra):
        if(cadenaEnMayusculas[i+1]=='/'):
            break
        elif((ord(cadenaEnMayusculas[i])>=48 and ord(cadenaEnMayusculas[i])<=56) and (ord(cadenaEnMayusculas[i+1])>=48 and ord(cadenaEnMayusculas[i+1])<=56) and (ord(cadenaEnMayusculas[i])<ord(cadenaEnMayusculas[i+1]))):    #si es un digito entero el caracter actual y el siguiente tambien  y el actual es menor al asiguiente
            i+=1
        else:
            return False

    #Segunda parte de la cadena
    if(cadenaEnMayusculas[posicionDeBarra+1]=='S'):
        i=posicionDeBarra+2
    else:
        return False

    while(i<len(cadenaEnMayusculas)):
        if(((i+1)==len(cadenaEnMayusculas) and (ord(cadenaEnMayusculas[i])>=48 and ord(cadenaEnMayusculas[i])<=56))):#si ya es el ultimo caracter y es un numero
            return True
        elif((ord(cadenaEnMayusculas[i])>=48 and ord(cadenaEnMayusculas[i])<=56) and (ord(cadenaEnMayusculas[i+1])>=48 and ord(cadenaEnMayusculas[i+1])<=56) and (ord(cadenaEnMayusculas[i])<ord(cadenaEnMayusculas[i+1]))):    #si es un digito entero el caracter actual y el siguiente tambien  y el actual es menor al asiguiente
            i+=1
        else:
            return False

    return True


#FUNCIONES 


#SECCION 1 DEL CODIGO
otroProceso=False
#Inicializamos arrays para realizar las graficas
listaEstados=[]
listaCelulasVivasPorEstado=[]
#Inicializamos variables
juego=False
numeroEstado=0
#Dimensiones de la celula
anchoCelula=10
altoCelula=10
#ancho y alto deben ser las mismas
#hasta ahora solo funciona con el ancho y el alto de las celula igualess
#creamos Celulas
numFilas=100#
numColumnas=100#
#el espacio es cuadrado numFilas = num columnas
#creamos matriz inicializada en 0
estadoDelJuego=np.zeros((numFilas,numColumnas))
estadoDelJuegoNuevo=np.copy(estadoDelJuego)

#Creamos ventana
ventanaPrincipal=tkinter.Tk()
ventanaPrincipal.title("Conway")
ventanaPrincipal.geometry("1366x768")

#creamos una ventana 2
espacioContenedorCelular=tkinter.Frame(ventanaPrincipal, width=800, height=670, bg='black')
espacioContenedorCelular.place(x=0.0,y=0.0)
#creamos canvas encima de espacioContenedorCelular
espacioCelularCanvas=tkinter.Canvas(espacioContenedorCelular,width=800,height=670,bg="Gray")
espacioCelularCanvas.place(x=0.0,y=0.0)
##########################SCROLLIN

#Creamos scrollbar horizontal y vertical al frame 
sbarV = tkinter.Scrollbar(espacioContenedorCelular, orient=tkinter.VERTICAL, command=espacioCelularCanvas.yview)
sbarH = tkinter.Scrollbar(espacioContenedorCelular, orient=tkinter.HORIZONTAL, command=espacioCelularCanvas.xview)

#los posiciono en el frame
sbarV.pack(side=tkinter.RIGHT, fill=tkinter.Y)
sbarH.pack(side=tkinter.BOTTOM, fill=tkinter.X)
espacioCelularCanvas.config(yscrollcommand=sbarV.set)
espacioCelularCanvas.config(xscrollcommand=sbarH.set)
espacioCelularCanvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
espacioCelularCanvas.config(scrollregion=(0, 0, numColumnas*anchoCelula,numFilas*altoCelula))#vamos a hacer un scroll region de esta manera. El acho de cada celula por numero de columnas corresponde a que tanto vamos a poder desplazarnos horizontalmente en el canvas
###############################SCROLLfin
"""
celula = espacioCelularCanvas.create_rectangle(0,0,20,20, fill = "yellow",outline="white" )#ancho
celula = espacioCelularCanvas.create_rectangle(20,0,40,20, fill = "red",outline="white" )
"""

###############################################
etiquetaMensajeColorCelulaViva=tkinter.Label(ventanaPrincipal,text="Living cells color")
etiquetaMensajeColorCelulaViva.config(font=("Arial", 18))
etiquetaMensajeColorCelulaViva.place(x=860,y=500)
#Agregamos lista de colores para celulas vivas
ColorDeCelulaViva=tkinter.StringVar(ventanaPrincipal)
ColorDeCelulaViva.set('White')
colorelegidoparaCelulaViva="White"
varioscoloresCELULASVIVASyMUERTAS=['Blue','Red','White','Green','Yellow','Gray','Pink','Orange','Cyan','Black']#esta misma lista se usa para
menuColoresCelulasVivas=tkinter.OptionMenu(ventanaPrincipal,ColorDeCelulaViva,*varioscoloresCELULASVIVASyMUERTAS).place(x=1050,y=500)
ColorDeCelulaViva.trace("w",callback1)#ESTO FUNCIONA CUANDO ELIJO UN ITEM DEL MENU DESPLEGABLE, SOLO AHI,,significa que llamará a la función callback cuando variable sea escrita o seleccionada por el usuario.
###############################################esto se ejecuta siempre porque esta en Ventana principal, que tiene mainloop
etiquetaMensajeColorCelulaMuerta=tkinter.Label(ventanaPrincipal,text="Dying cells color")
etiquetaMensajeColorCelulaMuerta.config(font=("Arial", 18))
etiquetaMensajeColorCelulaMuerta.place(x=860,y=550)
########Agregamos lista de colores de las celulas muertas
ColorDeCelulaMuerta=tkinter.StringVar(ventanaPrincipal)
ColorDeCelulaMuerta.set('Black')
colorelegidoparaCelulaMuerta="Black"
menuColoresCelulasMuertas=tkinter.OptionMenu(ventanaPrincipal,ColorDeCelulaMuerta,*varioscoloresCELULASVIVASyMUERTAS).place(x=1050,y=550)
ColorDeCelulaMuerta.trace("w",callback2)#ESTO FUNCIONA CUANDO ELIJO UN ITEM DEL MENU DESPLEGABLE, SOLO AHI,,significa que llamará a la función callback cuando variable sea escrita o seleccionada por el usuario.
################################################
etiquetaMensajeTamCelulas=tkinter.Label(ventanaPrincipal,text="Cell size (px)")
etiquetaMensajeTamCelulas.config(font=("Arial", 18))
etiquetaMensajeTamCelulas.place(x=860,y=600)
####################################################
TamCelulas=tkinter.StringVar(ventanaPrincipal)#Creamos una variable que guarde el valor del item seleccionado del tkinter.OptionMenu
TamCelulas.set('10')
varioTamsParaCelulas=['1','2','3','4','5','6','7','8','9','10']
menuTamCels=tkinter.OptionMenu(ventanaPrincipal,TamCelulas,*varioTamsParaCelulas).place(x=1050,y=600)
TamCelulas.trace("w",callback3)
#############################################################

###############################################

#ESTADO INICIAL
numeroEstado=0
celulasVivas=0
estadoDelJuegoNuevo=np.copy(estadoDelJuego)
for posicionEnX in range(0,numFilas):
    for posicionEnY in range(0,numColumnas):
        #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
        if estadoDelJuego[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
            celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
        else:
            celulasVivas+=1
            celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = colorelegidoparaCelulaViva,outline=colorelegidoparaCelulaViva )

#Las etiquetas declaradas aqui podran ser actualizadas en las funciones de arriba
etiqueta1=tkinter.Label(ventanaPrincipal,text="State")#etiqueta 1 es el estado
etiqueta1.config(font=("Arial", 24))
etiqueta1.place(x= 860.0,y= 50.0)
etiquetaNESTADO=tkinter.Label(ventanaPrincipal,text=str(numeroEstado))
etiquetaNESTADO.config(font=("Arial", 24))
etiquetaNESTADO.place(x= 900.0,y= 100.0)

etiqueta2=tkinter.Label(ventanaPrincipal,text="Living cells")#etiqueta 1 es el estado
etiqueta2.config(font=("Arial", 24))
etiqueta2.place(x= 860.0,y= 150.0)
etiquetaNCELVIVAS=tkinter.Label(ventanaPrincipal,text=str(celulasVivas))
etiquetaNCELVIVAS.config(font=("Arial", 24))
etiquetaNCELVIVAS.place(x= 900.0,y= 200.0)                


etiqueta5=tkinter.Label(ventanaPrincipal,text="Size of the\n cell space")#etiqueta 1 es el estado
etiqueta5.config(font=("Arial", 24))
etiqueta5.place(x= 860.0,y= 250)

tamUniversoLife=tkinter.StringVar(ventanaPrincipal)#Creamos una variable que guarde el valor del item seleccionado del tkinter.OptionMenu
tamUniversoLife.set('100x100')
varioTamsUniversosLife=['100x100','500x500','1000x1000','5000x5000','10000x10000']
menuTamUniversosLife=tkinter.OptionMenu(ventanaPrincipal,tamUniversoLife,*varioTamsUniversosLife).place(x=880,y=350)
tamUniversoLife.trace("w",callback5)


estadoDelJuego=np.copy(estadoDelJuegoNuevo)

#Agregamos caracteristica de click en canvas (panel negro) que es el espacio celualr Canvas. Su usa la funcion bind
espacioCelularCanvas.bind("<Button-1>",agregarQuitarCelula)
#Creamos botones. Lod agregamos a ventana principal
botonReproducir=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnReproducir(),text="Play",font=("Arial",24)).place(x=1040,y=50)
botonPausar=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnPausar(),text="Pause",font=("Arial",24)).place(x=1040,y=130)
botonReiniciar=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnReiniciar(),text="Restart",font=("Arial",24)).place(x=1040,y=210)
botonResultados=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnResultados(),text="Results",font=("Arial",24)).place(x=1200,y=50)
botonCargar=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnCargar(),text="Load",font=("Arial",24)).place(x=1200,y=130)
botonGuardar=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnGuardar(),text="Save",font=("Arial",24)).place(x=1200,y=210)

etiqueta4=tkinter.Label(ventanaPrincipal,text="Rule\nB0-8/S0-8")#etiqueta 1 es el estado
etiqueta4.config(font=("Arial", 18))
etiqueta4.place(x= 1150.0,y= 500)
regla=tkinter.StringVar(ventanaPrincipal)
regla.set("B3/S23")
campoRegla=tkinter.Entry(ventanaPrincipal, textvariable=regla, width=20).place(x=1165, y=580)


#Creamos espacio para los arboles, que puede ser de 6x6 como maximo
numColumnas2=2
numFilas2=2
anchoCelula2=(120/numColumnas2)
altoCelula2=(120/numFilas2)
#creamos una ventana 3
espacioContenedorCelular2=tkinter.Frame(ventanaPrincipal, width=120, height=120, bg='black')
espacioContenedorCelular2.place(x=1040,y=350)
#creamos canvas encima de espacioContenedorCelular
espacioCelularCanvas2=tkinter.Canvas(espacioContenedorCelular2,width=120,height=120,bg="Gray")
espacioCelularCanvas2.place(x=1040,y=350)
##########################SCROLLIN

#Creamos scrollbar horizontal y vertical al frame 
sbarV2 = tkinter.Scrollbar(espacioContenedorCelular2, orient=tkinter.VERTICAL, command=espacioCelularCanvas2.yview)
sbarH2 = tkinter.Scrollbar(espacioContenedorCelular2, orient=tkinter.HORIZONTAL, command=espacioCelularCanvas2.xview)

#los posiciono en el frame
sbarV2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
sbarH2.pack(side=tkinter.BOTTOM, fill=tkinter.X)
espacioCelularCanvas2.config(yscrollcommand=sbarV2.set)
espacioCelularCanvas2.config(xscrollcommand=sbarH2.set)
espacioCelularCanvas2.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
espacioCelularCanvas2.config(scrollregion=(0, 0, numColumnas2*anchoCelula2,numFilas2*altoCelula2))#vamos a hacer un scroll region de esta manera. El acho de cada celula por numero de columnas corresponde a que tanto vamos a poder desplazarnos horizontalmente en el canvas
###############################SCROLLfin


#ESTADO INICIAL de los arboles
estadoDelJuego2=np.zeros((numFilas2,numColumnas2))
estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
numeroEstado2=0
celulasVivas2=0
estadoDelJuegoNuevo2=np.copy(estadoDelJuego2)
for posicionEnX in range(0,numFilas2):
    for posicionEnY in range(0,numColumnas2):
        #celula = espacioCelularCanvas.create_rectangle((posicionEnY*anchoCelula) ,(posicionEnX*altoCelula),((posicionEnY+1)*altoCelula),((posicionEnX+1)*altoCelula), fill = "yellow",outline="white" )
        if estadoDelJuego2[posicionEnX,posicionEnY] == 0:#dibujo un rectangulo negro
            celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaMuerta,outline="White" )#fill = "black",outline="white" 
        else:
            celulasVivas2+=1
            celula = espacioCelularCanvas2.create_rectangle((posicionEnY*anchoCelula2) ,(posicionEnX*altoCelula2),((posicionEnY+1)*altoCelula2),((posicionEnX+1)*altoCelula2), fill = colorelegidoparaCelulaViva,outline=colorelegidoparaCelulaViva )

####
tamUniversoArboles=tkinter.StringVar(ventanaPrincipal)#Creamos una variable que guarde el valor del item seleccionado del tkinter.OptionMenu
tamUniversoArboles.set('2x2')
varioTamsUniversos=['2x2','3x3','4x4','5x5']
menuTamUniversos=tkinter.OptionMenu(ventanaPrincipal,tamUniversoArboles,*varioTamsUniversos).place(x=1200,y=350)
tamUniversoArboles.trace("w",callback4)

##creamos boton play2
botonReproducir2=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnReproducir2(),text="Generate trees",font=("Arial",12)).place(x=1200,y=400)
##creamos boton seeArboles
botonVerArboles=tkinter.Button(ventanaPrincipal,command=lambda: accionBtnVerArboles(),text="See trees",font=("Arial",12)).place(x=1200,y=450)
#Mostramos nuestra interfaz para siempre con mainloop
ventanaPrincipal.mainloop()