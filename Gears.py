#Ejecutar: Crtl+Alt+B

#Paquetes a utilizar
import math
from math import floor #Redondear al valor inferior
from math import ceil #Redondear al valor superior
from tabulate import tabulate
import os

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

#Codigo para truncar numeros
def truncate(number, digits) -> float:		
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


#Listas globales creadas:
ListaRT = []			#Lista que almacena las Relaciones de Tranmisión def por el usuario
Matriz = []				#Matriz de varias dimensiones las cuales vamos a comparar.
ListaModulos = []		#Creo la lista de los modulos segun Orbeg
ListaN1min = []			#Lista para almacenar los N1 minimos de cada relacion de transmision
Resultados = []
ResultadosFinales = []

#Debemos leer el archivo ModulosNormalizados.txt el cual tiene los módulos normalizados 
	#-	Determinar su tamaño real es decir (Sin contar el título)
	#- 	Recordar que los archivos se guardan como un string por lo tanto se debe cambiar su formato a float.
ModulosNormalizados = open("ModulosNormalizados.txt", "r")		#Abró en formato "leer" el .txt
ModulosNormalizados.readline()		#Linea para ignorar el titulo (Primera linea del .txt)
for Line in ModulosNormalizados:
	ListaModulos.append(float(Line))	#Agrego cada linea del .txt a una lista y cada elemento lo convierto a float


#Crear las matrices necesarias con el metodo "CrearMatrices"
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

print("	DISEÑO DE UN SISTEMA DE TRANsMISIÓN DE VARIAS RELACIONES")	#Este será lo primero que vea el usuario.
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


#Definir las entradas iniciales del usuario.
	#Tomando como referencia el flujograma de Gapper y mi persona, necesitaremos de primera entrada:
		#-	Error permisible (%) 
		#-	Ángulo de presión Phi (°)
		#-	Valor de alpha para determinar el ancho de cara (F)
	#Segunda parte del proyecto que queda pendiente por la complejidad del mismo.
		#-	Potencia de entrada (POT - hp)
		#-	Velocidad Angular (rpm)
		#-	Criterios de Falla (Seria mejor poder definirlos todos)***************************************************
		#-	Intervalo permisible del factor de seguridad
		#- 	Ángulo de hélice Psi (°)


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
	#- 	N1min con la ecuación respectiva tomando en cuenta el diente sin recorte.
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
				Matriz[a][i+1][0].append(round(N1*ListaModulos[i],3))	#Diametro de paso 1
				Matriz[a][i+1][1].append(round(N2*ListaModulos[i],3))	#Diametro de paso 2
				Matriz[a][i+1][2].append(round((N1*ListaModulos[i])/2 + (N2*ListaModulos[i])/2 , 3))	#Distancia entre centros Co

		else:
			if ((abs(ListaRT[a]-(floor(N2)/N1))/ListaRT[a])*100) < ErrorRT:
				Matriz[a][0][0].append(N1)
				Matriz[a][0][1].append(floor(N2))
				Matriz[a][0][2].append(round(floor(N2)/N1,2))

				for i in range(len(ListaModulos)):
					Matriz[a][i+1][0].append(round(N1*ListaModulos[i],3))	#Diametro de paso 1
					Matriz[a][i+1][1].append(round(floor(N2)*ListaModulos[i],3))	#Diametro de paso 2
					Matriz[a][i+1][2].append(round((N1*ListaModulos[i])/2 + (floor(N2)*ListaModulos[i])/2 ,3)) 	#Distancia Co

			if ((abs(ListaRT[a]-(ceil(N2)/N1))/ListaRT[a])*100) < ErrorRT:
				Matriz[a][0][0].append(N1)
				Matriz[a][0][1].append(ceil(N2))
				Matriz[a][0][2].append(round(ceil(N2)/N1,2))

				for i in range(len(ListaModulos)):
					Matriz[a][i+1][0].append(round(N1*ListaModulos[i],3)) #Diametro de paso 1
					Matriz[a][i+1][1].append(round(ceil(N2)*ListaModulos[i],3)) #Diametro de paso 2
					Matriz[a][i+1][2].append(round((N1*ListaModulos[i])/2 + (ceil(N2)*ListaModulos[i])/2 , 3 ))	


#Determinar las distancias entre centros iguales entre los trenes creados por el usuario.
	#Estas distancias se iteran pasando a la otra relacion de tranmision y despues por todos los modulos.


#Tarea #5: Llenar la matriz Resultados, ya creada en el inciso 1.
	#La cual será una lista de listas que  contienen los resultados deseados.
for a in range(1, len(Matriz[0][:])):
	for i in range(len(Matriz[0][a][2][:])):
		#Tenemos el valor de la variable
		Co_ith_A = Matriz[0][a][2][i]
		ParametrosdeA = [Matriz[0][0][0][i], Matriz[0][0][1][i], Matriz[0][0][2][i], ListaModulos[a-1]]
		Resultado = [ParametrosdeA]
		Bandera = False
		#Codigo para recorrer la segunda matriz principal (Relacion de transmision B)
		for p in range(1, len(ListaRT)):
			for q in range(1, len(Matriz[p][:])):
				for r in range(len(Matriz[p][q][2][:])):

					#Hacemos la comparacion entre el valor de la matriz de la relacion de transmision A y B.
					if Matriz[0][a][2][i] == Matriz[p][q][2][r]:
						Bandera = True
						Parametros_Match = [Matriz[p][0][0][r], Matriz[p][0][1][r], Matriz[p][0][2][r], ListaModulos[q-1]]
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
			
#Ahora se crearra una lista llamada ResultadosFinales con el fin de imprimir con más orden utilizando la función tabulate()

#Se procede a agregar una lista con los encabezados que corresponden a N1, N2, MgReal y el Modulo de cada 
#relación de transmisión encontrada, en la posición [0] de la lista ResultadosFinales.
Encabezados = []
for a in range(len(ListaRT)):
	Encabezados.append('N1')
	Encabezados.append('N2')
	Encabezados.append('MgReal')
	Encabezados.append('Módulo')
ResultadosFinales.insert(0, Encabezados)

#Se procede a pasar los datos de la lista Resultados a lista ResultadosFinales con el fin de organizar la lista final
#antes de llamar la función tabulate() 
for a in range(len(Resultados[:])):
	Lista = []
	for e in range(len(ListaRT)):
		for i in range(4):
			Lista.append(Resultados[a][e][i])
			ResultadosFinales.insert(a+1, Lista)

print("") #Para imprmir un salto de linea

#Se utiliza la función tabulate() para generar los resultados tabulados.
print(tabulate(ResultadosFinales,headers='firstrow',showindex=True))




#Guardar los resultados obtenidos en un .tex
print("")
print("¿Desea guardar los resultados obtenidos?")
Check=True
while(Check):	
	O = input("Digite, <Si> para guardar, <No> para salir: ")
	if O == "Si":
		#Aqui debo de guardar el codigo en el .txt
		print("Guardando... -Vaya por un cafecito-")
		CuadroFinal = open("Resultados.txt", "w")
		CuadroFinal.write(tabulate(ResultadosFinales,headers='firstrow',showindex=True))
		CuadroFinal.close()
		Check=False
		print("Se han guardado los datos obtenidos en el documento <Resultados.txt>")
		print("Nota: El documento <Resultados.txt> se reescribirá al ejecutar nuevamente el programa.")
	elif O == "No":
		#Aqui debo de no hacer nada para el usuario pueda leer lo que ocupe y lo cierre cuando quiera
		print("Cerrando...")
		Check=False
	else:
		#Si no puso ninguna de las anteriores, que siga probando hasta que ponga la entrada correcta.
		pass
print("Programa Terminado")
input()



 # Recomendaciones:
 	#Co sea un Set() para mejorar la busqueda
 	#A la relacion de transmision agregar un diccionario cuya llave sea: el valor Co para el m_ith
		# y su valor sean los parametros que generaron este Co.
	#Reestructurar a formato objeto.