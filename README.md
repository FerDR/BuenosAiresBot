# BuenosAiresBot
Bot que simula una guerra entre los barrios de Buenos Aires ó provincias de Argentina ó partidos del conurbano (localidades del conurbano coming soon)


Al principio se tiene que correr el startwar.py. y la función arrancar() con los parámetros que se quiera, en particular el mapa a usar
Tarda alrededor de unos minutos y genera en el mismo directorio un conjunto de archivos .npy

Cuando termina se corre resumewar.py. que define la función hacer_turno() que genera un turno del mapa especificado y puede o no subirlo a facebook.
Para loopear se loopea afuera de la función con runwar.py, a diferencia de antes como corre en función y el sleep está afuera es más liviano para la memoria. Los argumentos opcionales que se le pueden pasar a resumewar son

1)turns: hacer N turnos seguidos, usarlo para pruebas offline rápidas ya que los hace inmediatos 

2)uplo: boolean que dice si sube la imagen a facebook o no

3)overwrite: si turno a turno sobreescribe la imagen (la guarda con nombre {lugar}'imagen' o no (la guarda con un numero al final)

4)save: si guarda los turnos que va generando, cuando es falso se puede correr varias veces desde el mismo estado inicial

5)restart: si es True la guerra vuelve a arrancar, combinandolo con save = True se pierde todo el progreso, ojo!
