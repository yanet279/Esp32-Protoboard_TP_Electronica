import random
import time

# import machine

# Para ESP32
# bd0 = machine.Pin(23, machine.Pin.OUT)
# bd1 = machine.Pin(22, machine.Pin.OUT)
#bd2 = machine.Pin(21, machine.Pin.OUT)
#bd3 = machine.Pin(19, machine.Pin.OUT)
#bd4 = machine.Pin(18, machine.Pin.OUT)
#bd5 = machine.Pin(5, machine.Pin.OUT)
#bd6 = machine.Pin(4, machine.Pin.OUT)
#bd7 = machine.Pin(2, machine.Pin.OUT)
#bi0 = machine.Pin(32, machine.Pin.OUT)
#bi1 = machine.Pin(33, machine.Pin.OUT)
#bi2 = machine.Pin(25, machine.Pin.OUT)
#bi3 = machine.Pin(26, machine.Pin.OUT)
#bi4 = machine.Pin(27, machine.Pin.OUT)
#bi5 = machine.Pin(14, machine.Pin.OUT)
#bi6 = machine.Pin(12, machine.Pin.OUT)
#bi7 = machine.Pin(13, machine.Pin.OUT)

#Simulación de machine.Pin
class FakePin:
    def __init__(self, pin_number, mode):
        self.pin_number = pin_number
        self.state = False
    
    def value(self, val=None):
        if val is not None:
            self.state = val
        return self.state

#SIN ESP32
bd0 = FakePin(23, None)
bd1 = FakePin(22, None)
bd2 = FakePin(21, None)
bd3 = FakePin(19, None)
bd4 = FakePin(18, None)
bd5 = FakePin(5, None)
bd6 = FakePin(4, None)
bd7 = FakePin(2, None)
bi0 = FakePin(32, None)
bi1 = FakePin(33, None)
bi2 = FakePin(25, None)
bi3 = FakePin(26, None)
bi4 = FakePin(27, None)
bi5 = FakePin(14, None)
bi6 = FakePin(12, None)
bi7 = FakePin(13, None)

class Empaquetado:
  def __init__(self,alarmas_depr, alarmas_vel, emp_por_hora, emp_por_robot):
      self.alarmas_depresion = alarmas_depr
      self.alarmas_velocidad = alarmas_vel
      self.empaquetados_por_hora = [emp_por_hora]*24
      self.empaquetados_por_robot = [emp_por_robot]*4
  
  
  def set_alarmas_depresion(self,valor):
    self.alarmas_depresion+=valor

  def set_alarmas_velocidad(self,valor):
      
    self.alarmas_velocidad+=valor
      
  def set_empaquetados_por_hora(self,hora):
    self.empaquetados_por_hora[hora] += 1
      
      
  def set_empaquetados_por_robot(self,robot):
    self.empaquetados_por_robot[robot] += 1
  
  def get_alarmas_depresion(self):
    return self.alarmas_depresion

  def get_alarmas_velocidad(self):
    return self.alarmas_velocidad

  def get_empaquetados_por_hora(self):
    return self.empaquetados_por_hora

  def get_empaquetados_por_robot(self): 
    return self.empaquetados_por_robot
    
        
def simular_datos(empaquetado):
  random.seed()
  cont=0
  velocidad_inferior=0
  num= random.randint(0, 255)
  s1=bin((num&16)>>4)
  s2=bin((num&8)>>3)
  while(s1!=s2):
    #print(s1,"\t",s2)
    num= random.randint(0, 255)
    print("\nNumero random:", num)
    print("Numero random:", bin(num))
    s1=bin((num&16)>>4)
    s2=bin((num&8)>>3)

    fin=bin(num>>5)  
    while(int(fin,2)!=7):
      mostrar_leds(num)
      cont+=1
      horario=time.localtime()
      robot=bin(num&3)
      control=bin((num&4)>>2)
        
      dato=random.randint(0, 127)
      print("\nNumero DDDDDDD:", dato)
      print("Numero DDDDDDD:", bin(dato))
      if(int(control,2)==1):
        depresion = dato/100
        if(depresion>=0.2 and depresion<=0.5):
          empaquetado.set_alarmas_depresion(depresion)
          print("\nAlarma de depresión:", depresion)
          print("Hora y minuto de ocurrencia:", horario[3],":",horario[4])
      else:
        if(dato>=20 and dato<=50):
          empaquetado.set_alarmas_velocidad(dato)
          print("\nAlarma de velocidad:", dato)
          print("Hora y minuto de ocurrencia:", horario[3],":",horario[4])
        
        if(dato<20):
          velocidad_inferior+=1
        
      empaquetado.set_empaquetados_por_hora(horario[3])
      empaquetado.set_empaquetados_por_robot(int(robot,2))
        
      num= random.randint(0, 255)
      ss1=bin((num&16)>>4)
      s2=bin((num&8)>>3) 
      while(s1!=s2):
        num= random.randint(0, 255)
        s1=bin((num&16)>>4)
        s2=bin((num&8)>>3)
      print("\nNumero random:", num)
      print("Numero random:", bin(num))
      fin=bin(num>>5)
        
  return velocidad_inferior,cont
  
def robot_menos_empaqueto(empaquetado):
  print("\nROBOTS QUE MENOS EMPAQUETARON\nRobot")
  for i in range(4):
    dato=empaquetado.empaquetados_por_robot[i]
    if(i==0 or dato<minimo):
      minimo=dato 
  for i in range(4):
    dato=empaquetado.empaquetados_por_robot[i]
    if(dato==minimo):
      print("  ",i)
            
def mostrar_leds(num):
  bit1=bin(num&1)
  bit2=bin((num&2)>>1)
  bit3=bin((num&4)>>2)
  bit4=bin((num&8)>>3)
  bit5=bin((num&16)>>4)
  bit6=bin((num&32)>>5)
  bit7=bin((num&64)>>6)
  bit8=bin((num&128)>>7)

  if(int(bit1,2)==1):
    bd0.value(True)
    bi0.value(True)
  if(int(bit2,2)==1):
    bd1.value(True)
    bi1.value(True)
  if(int(bit3,2)==1):
    bd2.value(True)
    bi2.value(True)
  if(int(bit4,2)==1):
    bd3.value(True)
    bi3.value(True)
  if(int(bit5,2)==1):
    bd4.value(True)
    bi4.value(True)
  if(int(bit6,2)==1):
    bd5.value(True)
    bi5.value(True)
  if(int(bit7,2)==1):
    bd6.value(True)
    bi6.value(True)
  if(int(bit8,2)==1):
    bd7.value(True)
    bi7.value(True)
  
  time.sleep(3)
  bd0.value(False)
  bd1.value(False)
  bd2.value(False)
  bd3.value(False)
  bd4.value(False)
  bd5.value(False)
  bd6.value(False)
  bd7.value(False)
  bi0.value(False)
  bi1.value(False)
  bi2.value(False)
  bi3.value(False)
  bi4.value(False)
  bi5.value(False)
  bi6.value(False)
  bi7.value(False)

def mostrar_atributo(empaquetado):    
  print("\n----- Atributos de la clase Empaquetado -----\n")
  print("Cantidad de alarmas por depresión:", empaquetado.get_alarmas_depresion())
  print("Cantidad de alarmas por velocidad:", empaquetado.get_alarmas_velocidad())
  
  print("\nEMPAQUETADOS POR HORA:", )
  print("Hora\t Cantidad")
  for i in range(len(empaquetado.get_empaquetados_por_hora())):
    print(i,"\t\t",empaquetado.get_empaquetados_por_hora()[i])
  
  print("\nEMPAQUETADOS POR ROBOT:", )
  print("Robot\t Cantidad")
  for i in range(len(empaquetado.get_empaquetados_por_robot())):
    print(i,"\t\t",empaquetado.get_empaquetados_por_robot()[i])
      

empaquetado = Empaquetado(0,0,0,0)

# Simular los datos y procesarlos
velocidad_inferior,cont=simular_datos(empaquetado)
if(cont>0):
  #Resultados:
  mostrar_atributo(empaquetado)
  print("\nCantidad de veces que la velocidad fue inferior a 20 cm/seg:",velocidad_inferior)
  robot_menos_empaqueto(empaquetado)
else:
  print("No hubo datos validos antes de finalizar el programa...")