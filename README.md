# BuenosAiresBot
Bot que simula una guerra entre los barrios de Buenos Aires


Al principio se tiene que correr el startwar.py.
Tarda alrededor de unos minutos y genera en el mismo directorio un conjunto de archivos .npy
Para usarlo con otras imágenes hay que cambiar el archivo que carga y dependiendo de la imagen el criterio para delimitación de areas.
El vector de colores está hecho completamente a ojo, en el futuro va a ser reemplazado por una función que genere colores distintos.

Cuando termina se corre resumewar2.py.
Así como está sube cada una hora posts a facebook y en cada iteración reemplaza todas las variables, lo único que necesita es un acces token que depende de la página de facebook.
Si por algo se corta con ejecutarlo devuelta arranca desde donde se quedó, salvo por el tiempo, cuando arranca sube y desde ahí es cada una hora.
Hay que definirlo como función para no tener que cambiar cosas a mano pero por ahora cosas que se pueden querer cambiar (para correr local o debuguear):

1)Que no sobreescriba las variables, para poder arrancar varias veces desde el mismo punto, para esto hay que comentar la linea de save_all

2)Número controlado de iteraciones, reemplazar while not end por while i < N al principio del loop

3)Que no suba a facebook, comentar la línea de upload

4)Que no espere una hora, cambiar el argumento de time.sleep() al final del loop

5)Que guarde todas las imagenes, cambiar el nombre de la imagen que guarda para que dependa de la iteración
