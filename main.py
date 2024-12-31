import streamlit as st
from dataclasses import dataclass
from typing import List
from itertools import combinations
import random
import csv
import pandas as pd
from datetime import datetime
import os

@dataclass
class EquipoFutbolin:
    nombre: str
    jugador1: str
    jugador2: str
    golesAFavor: int = 0
    golesEnContra: int = 0
    partidasGanadas: int = 0
    partidasPerdidas: int = 0

@dataclass
class Enfrentamiento:
    equipo1: str
    equipo2: str
    goles_equipo1: int = 0
    goles_equipo2: int = 0
    jugado: bool = False

class LigaFutbolin:
    def __init__(self):
        # Definir la ruta local donde guardar los archivos en el dispositivo móvil
        self.ruta_local = "./"  # Reemplaza esta ruta con la ubicación en tu dispositivo

        # Inicializar las listas de equipos y enfrentamientos
        self.nombre_csv_enfrentamientos = "enfrentamientos.csv"
        self.equipos: List[EquipoFutbolin] = self.cargar_equipos()
        self.enfrentamientos: List[Enfrentamiento] = self.cargar_enfrentamientos()
        
        # Crear la carpeta si no existe
        os.makedirs(self.ruta_local, exist_ok=True)

    def agregar_equipo(self, equipo: EquipoFutbolin):
        self.equipos.append(equipo)
        self.guardar_equipos()

    def eliminar_equipo(self, nombre_equipo):
        self.equipos = [equipo for equipo in self.equipos if equipo.nombre != nombre_equipo]
        self.guardar_equipos()

    def generar_enfrentamientos(self, num_partidos):
        self.enfrentamientos = []
        combinaciones_equipos = list(combinations(self.equipos, 2))

        for i in range(num_partidos):
            enfrentamientos_temporales = []

            for enfrentamiento in combinaciones_equipos:
                equipo1, equipo2 = enfrentamiento

                if i % 2 == 0:
                    enfrentamiento_obj = Enfrentamiento(equipo2.nombre, equipo1.nombre)
                else:
                    enfrentamiento_obj = Enfrentamiento(equipo1.nombre, equipo2.nombre)

                enfrentamientos_temporales.append(enfrentamiento_obj)

            random.shuffle(enfrentamientos_temporales)
            self.enfrentamientos.extend(enfrentamientos_temporales)
        #self.nombre_csv_enfrentamientos = f"enfrentamientos_{datetime.now().strftime('%H-%M')}.csv"
        self.guardar_enfrentamientos()

    def guardar_equipos(self):
        local_filename = os.path.join(self.ruta_local, 'equipos.csv')
        with open(local_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Jugador1", "Jugador2", "GolesAFavor", "GolesEnContra", "PartidasGanadas", "PartidasPerdidas"])
            for equipo in self.equipos:
                writer.writerow([equipo.nombre, equipo.jugador1, equipo.jugador2, equipo.golesAFavor, equipo.golesEnContra, equipo.partidasGanadas, equipo.partidasPerdidas])

    def cargar_equipos(self):
        local_filename = os.path.join(self.ruta_local, 'equipos.csv')
        equipos = []
        try:
            with open(local_filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    equipos.append(EquipoFutbolin(
                        nombre=row['Nombre'],
                        jugador1=row['Jugador1'],
                        jugador2=row['Jugador2'],
                        golesAFavor=int(row['GolesAFavor']),
                        golesEnContra=int(row['GolesEnContra']),
                        partidasGanadas=int(row['PartidasGanadas']),
                        partidasPerdidas=int(row['PartidasPerdidas'])
                    ))
        except FileNotFoundError:
            pass
        return equipos

    def guardar_enfrentamientos(self, filename="enfrentamientos.csv"):
        local_filename = os.path.join(self.ruta_local, filename)
        with open(local_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Equipo1", "Equipo2", "GolesEquipo1", "GolesEquipo2", "Jugado"])
            for enfrentamiento in self.enfrentamientos:
                writer.writerow([enfrentamiento.equipo1, enfrentamiento.equipo2, enfrentamiento.goles_equipo1, enfrentamiento.goles_equipo2, enfrentamiento.jugado])

    def cargar_enfrentamientos(self, filename="enfrentamientos.csv"):
        local_filename = os.path.join(self.ruta_local, filename)
        enfrentamientos = []
        try:
            with open(local_filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    enfrentamientos.append(Enfrentamiento(
                        equipo1=row['Equipo1'],
                        equipo2=row['Equipo2'],
                        goles_equipo1=int(row['GolesEquipo1']),
                        goles_equipo2=int(row['GolesEquipo2']),
                        jugado=row['Jugado'] == 'True'
                    ))
        except FileNotFoundError:
            pass
        return enfrentamientos

liga = LigaFutbolin()

st.title("Liga de Futbolín")
menu = st.sidebar.selectbox("Menú", ["Registrar Equipo", "Eliminar Equipo", "Mostrar Equipos", "Generar Enfrentamientos", "Mostrar Enfrentamientos", "Jugar Enfrentamiento", "Resultados"])

if menu == "Registrar Equipo":
    st.header("Registrar Equipo")
    nombre = st.text_input("Nombre del Equipo")
    jugador1 = st.text_input("Jugador 1")
    jugador2 = st.text_input("Jugador 2")
    if st.button("Registrar"):
        if nombre and jugador1 and jugador2:
            liga.agregar_equipo(EquipoFutbolin(nombre, jugador1, jugador2))
            st.success(f"Equipo '{nombre}' registrado con éxito.")
        else:
            st.error("Por favor, completa todos los campos.")

elif menu == "Eliminar Equipo":
    st.header("Eliminar Equipo")
    if liga.equipos:
        opciones = [equipo.nombre for equipo in liga.equipos]
        equipo_seleccionado = st.selectbox("Seleccionar Equipo", opciones)
        if st.button("Eliminar"):
            liga.eliminar_equipo(equipo_seleccionado)
            st.success(f"Equipo '{equipo_seleccionado}' eliminado con éxito.")
    else:
        st.warning("No hay equipos registrados.")

elif menu == "Mostrar Equipos":
    st.header("Equipos Registrados")
    if liga.equipos:
        equipos_data = pd.DataFrame({
            'Nombre': [equipo.nombre for equipo in liga.equipos],
            'Jugador 1': [equipo.jugador1 for equipo in liga.equipos],
            'Jugador 2': [equipo.jugador2 for equipo in liga.equipos],
            'PG': [equipo.partidasGanadas for equipo in liga.equipos],
            'PP': [equipo.partidasPerdidas for equipo in liga.equipos],
            'GF': [equipo.golesAFavor for equipo in liga.equipos],
            'GC': [equipo.golesEnContra for equipo in liga.equipos]
        })
        st.table(equipos_data)
    else:
        st.warning("No hay equipos registrados.")

elif menu == "Generar Enfrentamientos":
    st.header("Generar Enfrentamientos")
    if len(liga.equipos) > 1:
        num_partidos = st.number_input("Número de enfrentamientos", min_value=1, step=1)
        if st.button("Generar"):
            liga.generar_enfrentamientos(num_partidos)
            st.success("Enfrentamientos generados con éxito.")
    else:
        st.warning("No hay suficientes equipos registrados para generar enfrentamientos.")

elif menu == "Mostrar Enfrentamientos":
    st.header("Enfrentamientos")
    liga.enfrentamientos = liga.cargar_enfrentamientos()
    if liga.enfrentamientos:
        enfrentamientos_data = pd.DataFrame({
            'Equipo 1': [enfrentamiento.equipo1 for enfrentamiento in liga.enfrentamientos],
            'Equipo 2': [enfrentamiento.equipo2 for enfrentamiento in liga.enfrentamientos],
            'Goles Equipo 1': [enfrentamiento.goles_equipo1 for enfrentamiento in liga.enfrentamientos],
            'Goles Equipo 2': [enfrentamiento.goles_equipo2 for enfrentamiento in liga.enfrentamientos]
        })
        st.table(enfrentamientos_data)
    else:
        st.warning("No hay enfrentamientos registrados.")

elif menu == "Jugar Enfrentamiento":
    st.header("Jugar Enfrentamiento")
    enfrentamientos_pendientes = [e for e in liga.enfrentamientos if not e.jugado]
    if enfrentamientos_pendientes:
        enfrentamiento_actual = st.selectbox("Seleccionar Enfrentamiento", [f"{e.equipo1} vs {e.equipo2}" for e in enfrentamientos_pendientes])
        index = [f"{e.equipo1} vs {e.equipo2}" for e in enfrentamientos_pendientes].index(enfrentamiento_actual)
        enfrentamiento = enfrentamientos_pendientes[index]

        st.subheader(f"{enfrentamiento.equipo1} vs {enfrentamiento.equipo2}")

        goles_equipo1 = st.number_input(f"Goles de {enfrentamiento.equipo1}", value=enfrentamiento.goles_equipo1, step=1)
        goles_equipo2 = st.number_input(f"Goles de {enfrentamiento.equipo2}", value=enfrentamiento.goles_equipo2, step=1)

        if st.button("Terminar Enfrentamiento"):
            # Marcar como jugado
            enfrentamiento.jugado = True

            # Actualizar goles en el enfrentamiento
            enfrentamiento.goles_equipo1 = goles_equipo1
            enfrentamiento.goles_equipo2 = goles_equipo2
            
            # Actualizar los equipos correspondientes
            equipo1 = next(e for e in liga.equipos if e.nombre == enfrentamiento.equipo1)
            equipo2 = next(e for e in liga.equipos if e.nombre == enfrentamiento.equipo2)

            # Actualizar goles a favor y en contra para ambos equipos
            equipo1.golesAFavor += goles_equipo1
            equipo1.golesEnContra += goles_equipo2
            equipo2.golesAFavor += goles_equipo2
            equipo2.golesEnContra += goles_equipo1

            # Actualizar partidas ganadas y perdidas
            if goles_equipo1 > goles_equipo2:
                equipo1.partidasGanadas += 1
                equipo2.partidasPerdidas += 1
            elif goles_equipo2 > goles_equipo1:
                equipo2.partidasGanadas += 1
                equipo1.partidasPerdidas += 1

            # Guardar los enfrentamientos y los equipos
            liga.guardar_enfrentamientos()
            liga.guardar_equipos()

            # Mostrar mensaje de éxito
            st.success("Enfrentamiento terminado.")

            # Volver a cargar los enfrentamientos para asegurarnos de que la lista está actualizada
            liga.enfrentamientos = liga.cargar_enfrentamientos()
    else:
        st.warning("No hay enfrentamientos pendientes.")
    
elif menu == "Resultados":
    st.header("Resultados de los Partidos")

    # Cargar los equipos directamente desde el archivo CSV
    liga.equipos = liga.cargar_equipos()

    # Si hay equipos registrados
    if liga.equipos:
        # Ordenar los equipos por partidas ganadas y goles a favor
        equipos_ordenados = sorted(liga.equipos, key=lambda e: (-e.partidasGanadas, -e.golesAFavor))

        # Mostrar los resultados
        resultados_data = []
        for equipo in equipos_ordenados:
            resultados_data.append([equipo.nombre, equipo.partidasGanadas, equipo.partidasPerdidas, equipo.golesAFavor, equipo.golesEnContra])

        # Mostrar la tabla con los resultados
        st.table(pd.DataFrame(resultados_data, columns=["Equipo", "Partidas Ganadas", "Partidas Perdidas", "Goles a Favor", "Goles en Contra"]))
    else:
        st.warning("No hay equipos registrados.")
