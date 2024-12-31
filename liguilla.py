import streamlit as st
from dataclasses import dataclass
from typing import List
from itertools import combinations
import random

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

class LigaFutbolin:
    def __init__(self):
        self.equipos: List[EquipoFutbolin] = []
        self.enfrentamientos: List[Enfrentamiento] = []

    def agregar_equipo(self, equipo: EquipoFutbolin):
        self.equipos.append(equipo)

    def eliminar_equipo(self, nombre_equipo):
        self.equipos = [equipo for equipo in self.equipos if equipo.nombre != nombre_equipo]

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

liga = LigaFutbolin()

st.title("Liga de Futbolín")
menu = st.sidebar.selectbox("Menú", ["Registrar Equipo", "Eliminar Equipo", "Mostrar Equipos", "Generar Enfrentamientos", "Mostrar Enfrentamientos"])

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
        equipos_data = [
            [equipo.nombre, equipo.jugador1, equipo.jugador2, equipo.partidasGanadas,
             equipo.partidasPerdidas, equipo.golesAFavor, equipo.golesEnContra]
            for equipo in liga.equipos
        ]
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
    if liga.enfrentamientos:
        enfrentamientos_data = [
            [enfrentamiento.equipo1, enfrentamiento.equipo2, enfrentamiento.goles_equipo1, enfrentamiento.goles_equipo2]
            for enfrentamiento in liga.enfrentamientos
        ]
        st.table(enfrentamientos_data)
    else:
        st.warning("No hay enfrentamientos registrados.")
