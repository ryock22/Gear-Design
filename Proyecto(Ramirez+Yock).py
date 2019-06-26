#Ejecutar: Crtl+Alt+B
#Paquetes a utilizar
import math
from math import floor #Redondear al valor inferior
from math import ceil #Redondear al valor superior

def truncate(number, digits) -> float:		#Codigo para truncar numeros
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


#Listas globales creadas:
ListaRT = []			#Lista que almacena las Relaciones de Tranmisión def por el usuario
Matriz = []				#Matriz de varias dimensiones las cuales vamos a comparar.
ListaModulos = []		#Creo la lista de los modulos segun Orbeg
ListaN1min = []			#Lista para almacenar los N1 minimos de cada relacion de transmision

#Tarea #2: Debemos leer el archivo ModulosNormalizados.txt el cual tiene los módulos normalizados 
	#-	Determinar su tamaño real es decir (Sin contar el título)
	#- 	Recordar que los archivos se guardan como un string por lo tanto se debe cambiar su formato a float.

ModulosNormalizados = open("ModulosNormalizados.txt", "r")		#Abró en formato "leer" el .txt
ModulosNormalizados.readline()		#Linea para ignorar el titulo (Primera linea del .txt)
for Line in ModulosNormalizados:
	#print(Line, end='')
	ListaModulos.append(float(Line))	#Agrego cada linea del .txt a una lista y cada elemento lo convierto a float


#Tarea #0: Crear las matrices necesarias con el metodo "CrearMatrices"
	#Matrices a crear vistas de afuera hacia adentro.
		#a	Relación de Transmisión 1					Matriz[0]
			#e	Parametros iniciales						Matriz[0][0]
				#i	N1											Matriz[0][0][0].append()
				#i	N2											Matriz[0][0][1]
				#i	MgReal										Matriz[0][0][2]
			#e	Modulo 1									Matriz[0][1]
				#i	Diametro de paso 1							Matriz[0][1][0]
				#i	Diametro de paso 2							Matriz[0][1][1]
				#i	Distancia entre centros 1-2					Matriz[0][1][2]
			#e	Modulo 2									Matriz[0][2]
				#i	Diametro de paso 1							Matriz[0][2][0]
				#i	Diametro de paso 2							Matriz[0][2][1]
				#i	Distancia entre centros 1-2					Matriz[0][2][2]
			#e	Modulo 3									Matriz[0][3]
			#...											Matriz[0][...]			
			#e	Modulo 51 (Final)							Matriz[0][52]
		#a	Relación de Transmisión 2					Matriz[1]
	#Para poder determinar el tamaño de la primera matriz necesitamos saber la cantidad de relaciones de transmisión
	#que va a tener el sistema.

print("	DISEÑO DE UN SISTEMA DE TRANsMISIÓN DE VARIAS RELACIONES")
RT = int(input("Número de relaciones de transimisión: "))
for a in range(RT):
	a = []
	Matriz.append(a)
	for e in range(len(ListaModulos)+1):
		e = []
		a.append(e)
		for i in range(3):
			i = []
			e.append(i)


#Ahora procedemos crear una lista que almacene las relaciones de transimisión
#definidas por el usuario:
for a in range(1,RT+1):
	e = a-1
	ListaRT.append(float(input("Relación de transimisión "+ str(a) + ": ")))
#print(ListaRT[:])


#Tarea #1: Definir las entradas iniciales del usuario.
	#Tomando como referencia el flujo grama de Gapper y mi persona, necesitaremos de primera entrada:
		#-	Potencia de entrada (POT - hp)
		#-	Velocidad Angular (rpm)
		#-	Error permisible (%) 
		#-	Criterios de Falla (Seria mejor poder definirlos todos)***************************************************
		#-	Intervalo permisible del factor de seguridad
		#-	Valor de alpha para determinar el ancho de cara (F)
		#-	Ángulo de presión Phi (°)
		#- 	Ángulo de hélice Psi (°)
		#- N1min con la ecuación respectiva tomando en cuenta el diente sin recorte.

print("	DIGITE LOS SIGUIENTES PARÁMETROS")
#Pot = float(input("Potencia (hp): "))
#wi = float(input("Velocidad angular (rpm): "))
ErrorRT = float(input("Error permisible en la relacion de transimisión +/-(%): "))
#FSegPermisible = float(input("Intervalo permisible en el factor de seguridad +/-(%): "))
#print("Rango de alpha recomendado (3<alpha<5)")
print("Angulos de presión recomendados: 14.5° - 20° - 22.5° - 25°")
Phi = float(input("Ángulo de presión (°): "))
Phi = Phi*math.pi/180
#print("Angulos de hélice recomendados: 15° - 20° - 25° - 30°")
#Psi = float(input("Ángulo de hélice (°): "))
#Psi = Psi*math.pi/180

#Tarea #3: Llenar las demás matrices con las formulas del curso.
	#Primeramente vamos a llenar N1, N2 y MgReal
		#-	N1 partiendo del N1min.
		

IteracMax = int(input("Número de iteracciones maxima para N1: "))
for a in range(RT):
	ListaN1min.append(ceil(((2)/((1+2*ListaRT[a])*math.pow(math.sin(Phi),2)))*(ListaRT[a]+math.sqrt(math.pow(ListaRT[a],2)+(1+2*ListaRT[a])*math.pow(math.sin(Phi),2))))) 
	e=0
	for e in range(IteracMax):
		N1 = ListaN1min[a]+e
		N2 = N1*ListaRT[a]
		N2P = N2-floor(N2)
		if N2P ==0:
			Matriz[a][0][0].append(N1)
			Matriz[a][0][1].append(N2)
			Matriz[a][0][2].append(round(N2/N1,2))

			for i in range(len(ListaModulos)):
				Matriz[a][i+1][0].append(N1*ListaModulos[i])	#Diametro de paso 1
				Matriz[a][i+1][1].append(N2*ListaModulos[i])	#Diametro de paso 2
				Matriz[a][i+1][2].append(round((N1*ListaModulos[i])/2 + (N2*ListaModulos[i])/2 , 3))	#Distancia entre centros Co
			e= e+1
		else:
			if ((abs(ListaRT[a]-(floor(N2)/N1))/ListaRT[a])*100) < ErrorRT:
				Matriz[a][0][0].append(N1)
				Matriz[a][0][1].append(floor(N2))
				Matriz[a][0][2].append(round(floor(N2)/N1,2))

				for i in range(len(ListaModulos)):
					Matriz[a][i+1][0].append(N1*ListaModulos[i])	#Diametro de paso 1
					Matriz[a][i+1][1].append(floor(N2)*ListaModulos[i])	#Diametro de paso 2
					Matriz[a][i+1][2].append(round((N1*ListaModulos[i])/2 + (floor(N2)*ListaModulos[i])/2 ,3)) 	#Distancia Co

			if ((abs(ListaRT[a]-(ceil(N2)/N1))/ListaRT[a])*100) < ErrorRT:
				Matriz[a][0][0].append(N1)
				Matriz[a][0][1].append(ceil(N2))
				Matriz[a][0][2].append(round(ceil(N2)/N1,2))

				for i in range(len(ListaModulos)):
					Matriz[a][i+1][0].append(N1*ListaModulos[i])
					Matriz[a][i+1][1].append(ceil(N2)*ListaModulos[i])
					Matriz[a][i+1][2].append(round((N1*ListaModulos[i])/2 + (ceil(N2)*ListaModulos[i])/2 , 3 ))
			e=e+1	


#Tarea #4: Determinar las distancias entre centros iguales entre los trenes creados por el usuario.
	#Estas distancias se iteran pasando a la otra relacion de tranmision y despues por todos los modulos.


Resultados = []
#Codigo para leer la matriz principal con la Relacion de transmision A
for a in range(1, len(Matriz[0][:])):
	for i in range(len(Matriz[0][a][2][:])):
		#Tenemos el valor de la variable
		Co_ith_A = Matriz[0][a][2][i]
		ParametrosdeA = [Matriz[0][0][0][i], Matriz[0][0][1][i], Matriz[0][0][2][i]]
		Resultado = [ParametrosdeA]
		Bandera = False
		#Codigo para recorrer la segunda matriz principal (Relacion de transimision B)
		for p in range(1, len(ListaRT)):
			for q in range(1, len(Matriz[p][:])):
				for r in range(len(Matriz[p][q][2][:])):

					#Hacemos la comparacion entre el valor de la matriz de la relacion de transmision A y B.
					if Matriz[0][a][2][i] == Matriz[p][q][2][r]:
						Bandera = True
						Parametros_Match = [Matriz[p][0][0][r], Matriz[p][0][1][r], Matriz[p][0][2][r]]
						Resultado.append(Parametros_Match)
						break
				if Bandera == True:
					break
			if Bandera == True:
				Bandera = False
			else:
				break
		if len(Resultado) == len(ListaRT):
			Resultados.append(Resultado)
			














						#Si se cumple recorremos la tercera matriz principal (Relacion de transmision C)
						for x in range(p+1, len(ListaRT)):
							for y in range(1, len(Matriz[x][:])):
								for z in range(len(Matriz[x][y][2][:])):
									#Hacemos la comparacion el valor de la matriz de la relacion de transmision A y C.
									if Matriz[0][a][2][i] == Matriz[x][y][2][z]:
										#Debo de guardar los datos respectivos en una matriz resultado.
										pass
									else:
										pass
							break		
					else:
						pass

			break




print("	Analisis Final")
print("ListaRT")
print(ListaRT)
print(" ")
print("Lista de Modulos")
print(ListaModulos)
print(" ")
print("Lista de N1min")
print(ListaN1min)
print(" ")
print("IteracMax = "+str(IteracMax))
print(" ")
print("Matriz[]")
print(len(Matriz[:]))
print(" ")
print("len.Matriz[0]")
print(len(Matriz[0]))
print("El resultado es 52 porque son 51 modulos y 1 bloque parametros")
print(" ")
print("Matriz[0][0]")
print(len(Matriz[0][0]))
print(" ")
print("Matriz[0][0][0]")
print(len(Matriz[0][0][0]))
print(" ")
print("Matriz[0][0][0][i]=N1")
for i in range(len(Matriz[0][0][0])):
	print(Matriz[0][0][0][i])
print("Matriz[0][0][1][i]=N2" )
for i in range(len(Matriz[0][0][0])):
	print(Matriz[0][0][1][i])
print("Matriz[0][0][2][i]=Mg")
for i in range(len(Matriz[0][0][0])):
	print(Matriz[0][0][2][i])
print("Siguiente matriz")
print("Matriz[0][m=3][0][i]=D1")
for i in range(len(Matriz[0][0][0])):
	print(Matriz[0][ListaModulos.index(3)+1][0][i])
print("Matriz[0][m=3][1][i]=D2" )
for i in range(len(Matriz[0][0][0])):
	print(Matriz[0][ListaModulos.index(3)+1][1][i])
print("Matriz[0][m=3][2][i]=Co")
for i in range(len(Matriz[0][0][0])):
	print(Matriz[0][ListaModulos.index(3)+1][2][i])
print("lenMatriz[0][0][0]")
print(len(Matriz[0][0][0]))	
print("lenMatriz[0][0][0][:]")
print(len(Matriz[0][0][0][:]))

#Tarea #5: Llenar la matriz resultado, ya creada en el inciso 1.

#Tarea #6: Guardar los resultados obtenidos en un .tex


 # Recomendaciones:
 	#Co sea un Set() para mejorar la busqueda
 	#A la relacion de transmision agregar un diccionario cuya llave sea: el valor Co para el m_ith
		# y su valor sean los parametros que generaron este Co.
	#Reestructurar a formato objeto.
