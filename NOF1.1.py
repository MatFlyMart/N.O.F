#%%
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import animation, rc
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QFont
rc('animation', html='html5')
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, QGraphicsScene, QGraphicsView
#%% 

ui_file = "Cuerpo Ventana1.1.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_file)

ui_file2 = "Cuerpo Ventana2.3.ui"
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(ui_file2)

class Ventana(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #Esconder todos los botones q no necesitas
        Ventana.Hide(self.Uni, self.Uni2, self.bot1_2, self.bot2_2,
                 self.PregUni, self.Preg, self.bot1_2, self.bot2_2,
                 self.bAtras)
        
        #Funciones q hace cada boton
        self.A.clicked.connect(lambda: self.OpsUni("MRU"))
        self.B.clicked.connect(lambda: self.OpsUni("MRUV"))
        self.C.clicked.connect(lambda: self.mostrarOpciones())
        self.Uni.clicked.connect(lambda: self.abrirMovimiento("Km/h"))
        self.Uni2.clicked.connect(lambda: self.abrirMovimiento("M/s"))
        self.bot1_2.clicked.connect(lambda: self.OpsUni("Tiro OblicuoA"))
        self.bot2_2.clicked.connect(lambda: self.OpsUni("Tiro OblicuoB"))
        self.bAtras.clicked.connect(self.Atras)

    def Hide(*Items):
        for item in Items:
            item.hide()

    def Show(*Items):
        for item in Items:
            item.show()
 
    def Atras(self):
        Ventana.Hide(self.PregUni, self.Uni, self.Uni2, self.bot1_2, self.bot2_2, self.Preg, self.bAtras)
        Ventana.Show(self.A, self.B, self.C, self.PregunIni)
                                
    # PORQUE NO PUEDO HIDEAR 2 VECES USANDO SELF?                
    def OpsUni(self, tipo):
        Ventana.Hide(self.A, self.B, self.C, self.PregunIni)
        Ventana.Show(self.PregUni, self.Uni, self.Uni2, self.bAtras)
        self.tipo = tipo
        
        if tipo == "Tiro OblicuoA" or tipo == "Tiro OblicuoB": 
            Ventana.Hide(self.Preg, self.bot1_2, self.bot2_2)
            
    def mostrarOpciones(self):
        Ventana.Hide(self.A, self.B, self.C, self.PregunIni)
        Ventana.Show(self.Preg, self.bot1_2, self.bot2_2)
                                  
    def abrirMovimiento(self, unidad):
        VentanaGraph = movimiento(self.tipo, unidad)
        self.close()
        VentanaGraph.show() 
        
        #Comandos para q cuando vuelvas atras en la ventana del grafico este todo como q no tocaste nada
        Ventana.Show(self.A, self.B, self.C, self.PregunIni)
        Ventana.Hide(self.bAtras, self.Uni, self.Uni2, self.PregUni)

      
class movimiento(QMainWindow, Ui_MainWindow2):
    
    def __init__(self, tipo, unidad):
        super().__init__()
        self.setupUi(self)
        plt.style.use("bmh")
        self.fig, self.ax = plt.subplots(figsize = (9.5,7),dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry() 
        self.animacion = None
        self.textUni = ('Km' if unidad=='Km/h' else 'Mts')
        self.UnidadTemp = ("Horas" if unidad == "Km/h" else "Segundos")
        self.UniAcel = ("Km/h²" if unidad == "Km/h" else "Mts/seg²")
        self.setAx()
        self.a_0 = 0
        
        scene = QGraphicsScene(self)
        scene.setSceneRect(60, 60 , 800, 600)
        view = QGraphicsView(scene)
        scene.addWidget(self.canvas)
        self.Grafico.setScene(scene)
        
        
        Hides = []
        LayoutsHide = []
        Geometrys = [self.Respuesta2, self.Respuesta3, self.bResp2, self.bResp3, self.Pregunta2, self.Pregunta3]
        self.Geometry = {}
        if tipo == "MRU":
            Hides = [self.bA0, self.bVy0, self.bY0, self.bV0, self.bAng, 
                     self.A0, self.Vy0, self.Y0, self.V0, self.Ang,] 
            LayoutsHide = [self.LayoutA0, self.LayoutVy0, self.LayoutY0, self.LayoutV0, self.LayoutAng]    
        elif tipo == "Tiro OblicuoB":
            Hides = [self.bVx0, self.bA0, self.bVy0, self.bT0,  
                     self.Vx0, self.A0, self.Vy0, self.T0]
            LayoutsHide = [self.LayoutVx0, self.LayoutA0, self.LayoutVy0, self.LayoutT0]
        elif tipo == "Tiro OblicuoA":
            Hides = [self.bA0, self.bV0, self.bAng, self.bT0, 
                     self.A0, self.V0, self.Ang, self.T0,]
            LayoutsHide = [self.LayoutA0, self.LayoutV0, self.LayoutAng, self.LayoutT0]
        else:
            Hides = [self.bVy0, self.bY0, self.bV0, self.bAng, 
                     self.Vy0, self.Y0, self.V0, self.Ang]
            LayoutsHide = [self.LayoutVy0, self.LayoutY0, self.LayoutV0, self.LayoutAng]
        
        for elemento in Hides:
            elemento.setParent(None)
        for Layout in LayoutsHide:
            Layout.deleteLater()    
        for item in Geometrys:
            self.Geometry[item] = item.geometry()
            item.hide()
        
        self.bLimpiar.setEnabled(False)
        self.Tabs2.setTabEnabled(1, False)
        self.Tabs2.setCurrentIndex(0)
        self.bAtras.clicked.connect(self.abrir)
        self.bLimpiar.clicked.connect(self.LimpiarGrafico)
        self.bGraficar.clicked.connect(lambda: self.graficar(tipo, unidad))
        self.bNewPreg.clicked.connect(lambda: self.NuevaPregunta(tipo, self.tFin, self.xFin))
        self.bDatos.clicked.connect(lambda: self.ViewDatos(tipo))
        self.bResp2.clicked.connect(lambda: self.Respuestas(2))
        self.bResp3.clicked.connect(lambda: self.Respuestas(3))  
    
    #Metodos "Globales"
    def EcVel(v0, a, t0, t):
            return v0 + a * (t - t0)
        
    def EcMov (p0, v0, t0, a, t):
            return p0 + v0 * (t-t0) + (1/2) * a * ((t-t0)**2)
        
    def CalcTempDist (p0, v0, t0, a0, Fin, subindice):
            Z = v0 + a0 * t0
            Ñ = (p0 - Fin) - v0 * t0 - a0 * t0**2 * 1/2
            M = Z**2 -  2 * a0 * Ñ
            if subindice == "Primera":
                return (-Z - np.sqrt(M)) / (a0) # Arreglar
            else:
                return (-Z + np.sqrt(M)) / (a0)
        
    def ecTemp(v0, a0, t0):
        return ((-v0)/(a0) + t0 if a0 !=0 else -1)
    
    def tempFormat(v0, a0, t0):
            tFren = (-v0)/(a0) + t0
            horas = int(tFren)
            minutos = int((tFren - horas) * 60)
            return horas + minutos/100    
    
    #Metodos "Privados del objeto"
    def setAx(self):
            self.ax.set_title("Posicion en funcion del tiempo")
            self.ax.set_xlabel('Posicion en X (' + self.textUni + ')')
            self.ax.set_ylabel('Posicion en Y (' + self.textUni + ')')
            self.ax.grid(linewidth=0.5, color='black')

    def abrir(self):
        self.ax.clear()
        VentIni.show()
        self.close()
            
    def LimpiarGrafico(self):
            if self.running == True:
                self.animacion.event_source.stop() 
                
            Ventana.Hide(self.Respuesta2, self.Respuesta3, self.bResp2, self.bResp3)
            Valores = [self.X0, self.Y0, self.Vx0, self.Vy0,
                       self.V0, self.T0, self.Ang, self.A0]
            for item in Valores:
                item.setValue(0)
        
            self.ax.clear()
            self.setAx()
            self.ax.plot([], []) 
            self.ax.set_xlim(0,1)
            self.ax.set_ylim(0,1)
            self.canvas.draw()    
             
            self.bGraficar.setEnabled(True)
            self.bLimpiar.setEnabled(False) 
            self.Tabs2.setCurrentIndex(0)
            self.Tabs2.setTabEnabled(1, False)  
            self.Tabs2.setTabEnabled(0, True)                                      
        
    def NuevaPregunta(self, tipo, A, B):
            Pregunta1 = self.PregRandom(tipo, A, B)
            texto = Pregunta1[0]
            self.Resp2 = Pregunta1[1]
            
            Pregunta2 = self.PregRandom(tipo, A, B)
            texto1 = Pregunta2[0]
            self.Resp3 = Pregunta2[1]

            self.Pregunta2.setText(texto)
            self.Pregunta3.setText(texto1)
            
            Show = [self.Respuesta2, self.Respuesta3, self.bResp2, self.bResp3]
            for item in Show:
                item.setGeometry(self.Geometry[item])  # Restaura la geometría original
                item.show()
            
            self.Pregunta2.show()
            self.Pregunta3.show()
            self.Pregunta2.resize(160, 130)
            self.Pregunta3.resize(160, 130)
          
    def PregRandom(self, tipo, StopTemp, StopDist):
            NumRan1 = random.randrange(0, 100)
            NumRan2 = random.randrange(0, int(StopTemp) if NumRan1 < 50 else int(StopDist))  
            if tipo == "MRUV" or tipo == "MRU":
                if NumRan1 < 25:
                    return f" Que velocidad tiene la particula en: t = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcVel(self.x_0, self.a_0, self.t_0, NumRan2)))
                elif NumRan1 < 50:
                    return f" Cual es la posicion que tiene la particula habiendo pasado: t = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, NumRan2)))
                elif NumRan1 < 75:
                    if tipo == "MRUV":
                        return (f" Si tenemos un sensor de velocidad puesto a los x = {NumRan2} {self.textUni} del punto de partida,"
                        + f"que velocidad nos marca el aparato??"),float("{:.1f}".format(movimiento.EcVel(self.x_0, self.a_0, self.t_0, movimiento.CalcTempDist(self.x_0, self.a_0, self.t_0, self.a_0, NumRan2, "segunda"))))
                    else:
                        return f" Que velocidad tiene la particula en: x = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcVel(self.x_0, self.a_0, self.t_0, (NumRan2 - self.x_0)/ self.vx_0)))
                else:
                    if self.Frena == True:  
                        NumRan3 = random.randrange(0, 100)
                        if NumRan3 < 50:                  
                            return f" A que distancia se frena el objeto??",  float("{:.1f}".format(self.xFrena))
                        else:
                            return f" Cuanto tiempo pasa hasta que la particula se frene completamente??", float("{:.1f}".format(self.tFrena))
                    else:
                        return f" Que velocidad tiene la particula en: x = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcVel(self.x_0, self.a_0, self.t_0, (NumRan2 - self.x_0)/ self.vx_0)))
            else: 
                NumRan3 = random.randrange(1, 100)         
                if NumRan1 < 25:
                    if NumRan3 <50:
                        return f" Que velocidad en x tiene la particula en: t = {NumRan2} {self.UnidadTemp}?? ",  float("{:.1f}".format(self.vx_0))
                    else:
                        return f" Que velocidad en y tiene la particula en: t = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcVel(self.vy_0, -self.g, self.t_0, NumRan2)))
                elif NumRan1 < 50:
                    if NumRan3 < 50:
                        return f" Cuanta distancia horizontal recorrio la particula en: t = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, NumRan2)))
                    else:
                        return f" Que altura alcanza la particula en: t = {NumRan2} {self.UnidadTemp}??", float("{:.1f}".format(movimiento.EcMov(self.y_0, self.vy_0, self.t_0, -self.g, NumRan2)))
                elif NumRan1 < 75:
                    if NumRan3 < 50:
                        return f" Que velocidad neta o total tiene la particula en: x = {NumRan2} {self.textUni}??", float("{:.1f}".format(np.sqrt((movimiento.EcVel(self.vy_0, self.t_0, -self.g, (NumRan2 - self.x_0)/ self.vx_0))**2 + (self.vx_0)**2)))
                    else:
                         return f" Que altura alcanza la particula en: x = {NumRan2} {self.textUni}??", str(movimiento.EcMov(self.y_0, self.vy_0, self.t_0, self.g, (NumRan2 - self.x_0)/ self.vx_0)).strip()    #reahcer, la idea esq solo sean preguntas de los datos q dio
                else:
                    NumRan4 = random.randrange(self.y_0, int(self.yAltMax))
                    if NumRan3 < 50:
                        return f" Que velocidad neta o total tiene la particula la primera vez que pasa por : y = {NumRan4} {self.textUni}??", float("{:.1f}".format(np.sqrt((movimiento.EcVel(self.vy_0, self.t_0, -self.g, movimiento.CalcTempDist(self.y_0, self.vy_0, self.t_0, -self.g, NumRan4, "Primera")**2 + (self.vx_0)**2)))))
                    else:
                        return f" Que velocidad neta o total tiene la particula la segunda vez que pasa por : y = {NumRan4} {self.textUni}??", float("{:.1f}".format(np.sqrt((movimiento.EcVel(self.vy_0, self.t_0, -self.g, movimiento.CalcTempDist(self.y_0, self.vy_0, self.t_0, -self.g, NumRan4, "Segunda")**2 + (self.vx_0)**2))))) #este es
                                 
    def ViewDatos(self, tipo):
            self.Pregunta2.resize(160, 160)
            self.Pregunta3.resize(160, 160)
            Ventana.Hide(self.Respuesta2, self.Respuesta3, self.bResp2, self.bResp3)
            
            if tipo == "MRUV":
                font = QFont("Courier", 16)  # Cambia "Arial" por la fuente que desees y 16 por el tamaño deseado
                self.Pregunta2.setFont(font)
                self.Pregunta2.show()
                self.Pregunta2.setText(f"La particula se frena en x = {float('{:.1f}'.format(self.xFrena))} {self.textUni}"
                                       + f", el tiempo transcurrido antes de que se frene es de t = {float('{:.1f}'.format(self.tFrena))} {self.UnidadTemp}")
                self.Pregunta2.resize(160, 330)
            else:
                self.Pregunta2.show()
                self.Pregunta3.show()   
                self.Pregunta2.setText(f"El tiempo que tarda la particula en llegar al suelo nuevamente es de t = {float('{:.1f}'.format(self.tFin))} {self.UnidadTemp}"
                                       + f", este tiempo indica que la distancia recorrida es de x = {float('{:.1f}'.format(self.xFin))} {self.textUni}")
                self.Pregunta3.setText(f"La altura maxima a la que llega la particula es de y = {float('{:.1f}'.format(self.yAltMax))} {self.textUni}"
                                       + f", dicha altura se alcanza a los x = {float('{:.1f}'.format(self.xAltMAx))} {self.textUni}"
                                       + f", lo cual tarda t = {float('{:.1f}'.format(self.tAltMax))} {self.UnidadTemp} en llegar a el")         
    
    def Respuestas(self, numero):#Mejorar, ver como obtener que pregunta es, y q boton lo esta llamando (poner algo como boton.clicked.connect(que boton es))
            
        if numero == 2:
            RespuestaUsuario = self.Respuesta3.value()
            RespuestaCorrecta = self.Resp2
        else:
            RespuestaUsuario = self.Respuesta3.value()
            RespuestaCorrecta = self.Resp3
              
        print(RespuestaUsuario)
        print(RespuestaCorrecta)
        
            
        if RespuestaUsuario == RespuestaCorrecta:
            print("Anda")
        else:
            print("No anda")
         
    def graficar(self, tipo, unidad):
         
        self.y_0 = self.Y0.value()
        self.x_0 = self.X0.value()
        self.t_0 = self.T0.value()
        self.vx_0 = self.Vx0.value()

        if tipo == "Tiro OblicuoA" or tipo == "Tiro OblicuoB":     
            self.g = 9.8       
            if tipo == "Tiro OblicuoB":
                self.Angulo = self.Ang.value()
                self.vy_0 = self.V0.value() * np.sin(np.radians(self.Angulo))
                self.vx_0 = self.V0.value() * np.cos(np.radians(self.Angulo))
            else:
                self.vy_0 = self.Vy0.value()
                angulo = (np.tanh(self.vy_0/self.vx_0) * 180 / np.pi if self.vx_0 != 0 else 45) #VER ANG NEG
                self.Angulo = float("{:.1f}".format(angulo))
            
            self.Pregunta1.setText(f"Parametros:\n\nX0  = {self.x_0} {self.textUni}\nY0  = {self.y_0} {self.textUni}\nVx0 = {float('{:.1f}'.format(self.vx_0))} {unidad}\n"
                                   + f"Vy0 = {float('{:.1f}'.format(self.vy_0))} {unidad}\nA0  = {-self.g} {self.UniAcel}\nAng = {self.Angulo}º")
          
            self.tFin = movimiento.CalcTempDist(self.y_0, self.vy_0, self.t_0, -self.g, 0, "Primera")
            self.xFin = movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, self.tFin)
            t = np.linspace(0, self.tFin, 100)
            self.tAltMax = movimiento.ecTemp(self.vy_0, -self.g, self.t_0)
            self.xAltMAx =  movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, self.tAltMax)
            self.yAltMax =  movimiento.EcMov(self.y_0, self.vy_0, self.t_0, -self.g, self.tAltMax)
        else:            
            self.g = 0
            self.vy_0 = 0
            
            self.tFin = (20 if unidad == "Km/h" else 300)
            t = np.linspace(0, self.tFin, 200)
            self.xFin = max(movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, t)) 

            self.bDatos.setEnabled(False)
            
            if tipo == "MRUV":
                self.a_0 = self.A0.value()
                self.Pregunta1.setText(f"Parametros:\nX0 = {self.x_0} {self.textUni}\nY0 = {self.y_0} {self.textUni}\nT0 = {self.t_0} {self.UnidadTemp}\nVx0 = {self.vx_0} {unidad}\nA0 = {self.a_0}")
                
                if movimiento.ecTemp(self.vx_0, self.a_0,self.t_0) > 0:
                    self.Frena = True
                    self.bDatos.setEnabled(True)
                    self.tFrena = movimiento.ecTemp(self.vx_0, self.a_0, self.t_0)
                    self.xFrena = movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, self.tFrena) #esto tiene muchos decimales
                    if self.tFrena > self.tFin:
                        t = np.linspace(0, self.tFrena * 1.15, 500)
                else:
                    self.Frena = False
            else:
                self.Pregunta1.setText(f"Datos Utilizados:\nX0 = {self.x_0} {self.textUni}\nY0 = {self.y_0} {self.textUni}\nT0 = {self.t_0} {self.UnidadTemp}\nVx0 = {self.vx_0}")

        x_data = [] 
        y_data = []
        
        self.running = True
        def actualizar_animacion(frame):
            
            if frame == t[-1]:
                self.running = False
            
            if tipo == "Tiro OblicuoA" or tipo == "Tiro OblicuoB":    
                self.ax.set_ylim(-self.yAltMax * 0.05, self.yAltMax * 1.05)
                self.ax.set_xlim(self.x_0 - self.xFin * 0.05, self.xFin * 1.05)
            else:
                self.ax.set_ylim(self.y_0 - 2, self.y_0 + 2)
                self.ax.set_xlim(min(movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, t)) * 1.05, 
                                 max(movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, t)) * 1.05)

            x = movimiento.EcMov(self.x_0, self.vx_0, self.t_0, self.a_0, frame) 
            y = movimiento.EcMov(self.y_0, self.vy_0, self.t_0, -self.g, frame)  
            point, = self.ax.plot([], [], 'bo', markersize = 12, label = "Particula")
            point.set_data([], [])
            line, = self.ax.plot([], [], 'r--', label = "Trayectoria")
            line.set_data([], [])
            x_data.append(x)
            y_data.append(y)
            
            line.set_data(x_data, y_data) 
            point.set_data(x,y)
            
            return point, line,
        
        self.animacion = animation.FuncAnimation(self.fig, actualizar_animacion, frames=t, interval=(50 if tipo == "TiroOblicuoA" or "TiroOblicuoB" else 1), 
                                                cache_frame_data=False, save_count=0 ,repeat = False, blit = True)
        

        self.bLimpiar.setEnabled(True)
        self.canvas.draw()
        self.bGraficar.setEnabled(False)
        self.Tabs2.setTabEnabled(1, True)
        self.Tabs2.setTabEnabled(0, False)
        self.Tabs2.setCurrentIndex(1)
        
                    
if __name__ == '__main__':
    # Inicializar la aplicación
    app = QApplication([])
    VentIni = Ventana()
    VentIni.show() 
    sys.exit(app.exec_())
    
# %%