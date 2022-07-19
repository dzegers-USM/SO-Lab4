# Laboratorio 4
## Integrantes
Benjamín Soto 
Rol: 201973522-5 
Par: 200
Daniel Zegers 
Rol: 201973551-9
Par: 200

## Instrucciones de uso
Ejecutar el script y esperar a que finalice. Se creará el directorio 'out' y los archivos de salida se colocarán ahí.

## Aclaraciones:
- Por enunciado, las películas no pueden comenzar hasta que se haya llenado la sala. Aquí, a modo de permitir que el programa finalice, se permite que la película comienze en una sala que no está a capacidad máxima habiendo transcurrido unos segundos, cantidad definida en la constante TIMEOUT.
- El método .get() de queue bloquea mientras se está escribiendo, por lo que es seguro utilizarlo incluso cuando muchas hebras escriben al mismo queue.
