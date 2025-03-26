import numpy as np

"""

Autores: 


Simulación Falcon 9

Tipo de Motor: Merlin 1A
    Empuje (vacio) 981 KN
    Empuje (nivel del mar) 845 KN
    Impulso (vacio) 3.0 km/s
    Impulso (nivel del mar) 2.6 km/s

Masa_Total: 549 054 Kg
Etapas: 
    Etapa-1 
        9 Motores
        Masa: 22.200 kg
        Masa_de_comb: 410.900kg 
        Masa_total: 
    Etapa-2 
        1 Motor
        Masa: 111.500kg
Altura: 70m

La etapa 1 es la que hace la reentrada y aterriza, la etapa 2 seria el satelite.

"""

m1 = 22200 # kg
m1_comb = 410900 # kg
tasa_con_comb = 2450 # kg/s

m1_total = m1+m1_comb # Masa inicial, para el momento del despegue

empuje_total_e1 = 7607 # kN a nivel de mar



def gravedad_tierra():
    return 0

def consumoComb():  # Esta funcion debera ejecutarse cada segundo para actualizar la masa

    m1_comb -= m1_comb-tasa_con_comb
    m1_total = m1+m1_comb
    return m1_total


