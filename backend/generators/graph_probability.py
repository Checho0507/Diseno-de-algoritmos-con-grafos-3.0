import streamlit as st
import time
import matplotlib.pyplot as plt
from pyemd import emd
import numpy as np
import uuid
import re
from queue import PriorityQueue
from itertools import combinations
from backend.models.graph import Grafo
from backend.generators.graph_operations import *
from frontend.components.menu.sub_menu_1.sub_menu_2 import sub_menu_2
from streamlit_react_flow import react_flow
from scipy.stats import wasserstein_distance
from itertools import combinations

# Datos globales
probabilities = []
states = []
graph = []

def create_distance_matrix(n):
    # Crear una matriz n x n donde cada entrada (i, j) es |i - j|
    distance_matrix = np.abs(np.arange(n).reshape(-1, 1) - np.arange(n))
    return distance_matrix

def trabajar_sistema():
    global probabilities
    global states
    string = st.text_input("Introduce el sistema a trabajar:")
    execution_time = 0
    if st.button("Empezar"):
        fu_states, pr_states, iState = parse_input_string(string)
        r = generate_combinations(pr_states, fu_states)
        matriz_sistema_original(fu_states, pr_states)
        print(len(r))
        r = functionTensor([0.75,0.25],[0,0,1,0])
        o=np.array([0,0,0,0,1,0,0,0], dtype=np.float64)
        d=np.array([0,0,0.75,0,0,0,0.25,0], dtype=np.float64)
        dm = create_distance_matrix(len(o)).astype(np.float64)
        emd_value = emd(o, d, dm)
        print(emd_value, 'emd')
        print(r, 'tensor')
        st.success(f"El tiempo de ejecución de branch_and_bound_example fue de {execution_time:.4f} segundos.")
    else:
        crear_grafo()


def measure_execution_time(func, *args):
    """
    Mide el tiempo de ejecución de una función.

    :param func: Función a ejecutar.
    :param args: Argumentos de la función.
    :return: Tiempo de ejecución en segundos.
    """
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time


def editar_matriz():
    global probabilities
    x = st.number_input("Ingrese las coordenadas X (Filas):", value=0)
    y = st.number_input("Ingrese las coordenadas Y (Columnas):", value=0)
    st.write(f"Coordenadas ingresadas: X = {x}, Y = {y}")
    new_value = st.number_input("Ingrese el nuevo valor para las coordenadas ingresadas:")
    if st.button("Actualizar Matriz"):
        update_matrix(x, y, new_value)


def update_matrix(x, y, new_value):
    """
    Actualiza la matriz de probabilidades con un nuevo valor.

    :param x: Coordenada X.
    :param y: Coordenada Y.
    :param new_value: Nuevo valor.
    """
    global probabilities
    if 0 <= new_value <= 1 and x > 0 and y > 0:
        probabilities = [
            [round(new_value if i == x and j == y else probabilities[i][j], 2) for j in range(len(probabilities[i]))]
            for i in range(len(probabilities))
        ]
    else:
        st.warning("Ingrese valores válidos para las coordenadas y el valor debe estar entre 0 y 1.")


def generate_combinations(present_states, future_states):
    return [
        (present_state, future_state)
        for i in range(len(present_states) + 1)
        for present_state in combinations(present_states, i)
        for j in range(len(future_states) + 1)
        for future_state in combinations(future_states, j)
        if not (present_state == future_state and present_state != ())
           and not (present_state == () and future_state == ())
           and not (present_state == tuple(present_states) and future_state == tuple(future_states))
    ]

def getIndicesToMargenalice(states, state):
    availableIndices = []
    indices = {}
    csValue = ""
    for i in range(len(state)):
        if state[i] != None:
            availableIndices.append(i)
            csValue = str(state[i]) + csValue

    for i in range(len(states)):
        key = "".join(str(states[i][index]) for index in availableIndices)
        indices[key] = indices.get(key, []) + [i]

    return indices, int(csValue, 2) if csValue else 0


def margenaliceNextState(nsIndices, probabilities):
    nsTransitionTable = [[None] * len(nsIndices) for _ in range(len(probabilities))]
    for currentColumn, indices in enumerate(nsIndices.values()):
        for i in range(len(nsTransitionTable)):
            nsTransitionTable[i][currentColumn] = sum(probabilities[i][index] for index in indices)
    return nsTransitionTable


def margenaliceCurrentState(csIndices, nsTransitionTable):
    csTransitionTable = [[None] * len(nsTransitionTable[0]) for _ in range(len(csIndices))]
    for currentRow, indices in enumerate(csIndices.values()):
        for i in range(len(csTransitionTable[0])):
            csTransitionTable[currentRow][i] = sum(nsTransitionTable[index][i] for index in indices) / len(indices)
    return csTransitionTable


def functionTensor(dividedSystem1, dividedSystem2):
    return np.outer(dividedSystem1, dividedSystem2)


def calc_emd(original_distribution, divided_distribution):
    original_array = np.array(original_distribution)
    divided_array = np.array(divided_distribution)
    emd = wasserstein_distance(np.arange(len(original_array)), np.arange(len(divided_array)), original_array,
                               divided_array)
    return round(emd / 2, 2)


def translate_systems(system_tuple, initialState):
    letters = [chr(65 + i) for i in range(cantidad_nodos())]
    results = []
    for i, tuple_item in enumerate(system_tuple):
        result_tuple = [0 if letter in tuple_item else None for letter in letters]
        if i % 2 == 0:
            result_tuple = [1 if initialState[idx] == 1 and letter in tuple_item else val for idx, (letter, val) in
                            enumerate(zip(letters, result_tuple))]
        results.append(tuple(result_tuple))
    return results


def parse_input_string(input_string):
    match = re.match(r"([A-Za-z-Ø]+)ᵗ⁺¹\|([A-Za-z-Ø]+)ᵗ\s*=\s*(\d+)", input_string)
    if not match:
        raise ValueError("Formato de cadena no válido")
    pr_states = tuple(match.group(1))
    fu_states = tuple(match.group(2))
    iState = [int(digit) for digit in match.group(3)]
    return pr_states, fu_states, iState

def primera_particion(resultado1):
    destinos1, origenes1 = [], []
    div = False
    for char in resultado1:
        if char == '|':
            div = True
        elif char != ' ':
            (origenes1 if div else destinos1).append(char)
    return destinos1, origenes1


def segunda_particion(resultado2):
    destinos2, origenes2 = [], []
    div = False
    for char in resultado2:
        if char == '|':
            div = True
        elif char != ' ':
            (origenes2 if div else destinos2).append(char)
    return destinos2, origenes2


def get_element_by_label(grafo, label):
    return next((element for element in grafo if 'data' in element and element['data']['label'] == label), None)


def get_element_by_id(grafo, id):
    return next((element for element in grafo if element['id'] == id), None)


def cambiar_aristas(resultado1, resultado2, grafo):
    graph = Grafo()
    destinos1, origenes1 = primera_particion(resultado1)
    if 'Ø' not in destinos1 and 'Ø' not in origenes1:
        for origen in origenes1:
            for destino in destinos1:
                if origen != destino:
                    graph.add_edge(grafo, get_element_by_label(grafo, origen),
                                   get_element_by_label(grafo, f"{destino}'"), True, 0)
    destinos2, origenes2 = segunda_particion(resultado2)
    if 'Ø' not in destinos2 and 'Ø' not in origenes2:
        for origen in origenes2:
            for destino in destinos2:
                if origen != destino and get_element_by_label(grafo, origen) and get_element_by_label(grafo,
                                                                                                      f"{destino}'"):
                    graph.add_edge(grafo, get_element_by_label(grafo, origen),
                                   get_element_by_label(grafo, f"{destino}'"), True, 0)


def calculate_lower_bound(original_distribution, divided_dist):
    return np.max(np.abs(np.array(original_distribution).flatten() - np.array(divided_dist).flatten()))



def cantidad_nodos():
    return int(np.log2(len(probabilities)))


def crear_grafo():
    global graph
    agregar_nodos(cantidad_nodos())
    agregar_conexiones()
    flow_styles = {"height": 8000, "width": 800}
    react_flow("graph", elements=graph, flow_styles=flow_styles)

def mostrar_tabla():
    global probabilities
    columns = [f'F{i}' for i in range(len(probabilities))]
    index = [f'C{i}' for i in range(len(probabilities))]
    matriz_redondeada = [[round(valor, 2) for valor in fila] for fila in probabilities]
    df = pd.DataFrame(matriz_redondeada, columns=columns, index=index)
    st.table(df.style.format("{:.2f}"))

def crear_dict_pr(pr_states):
    primera = 'A'
    pr = {}
    j = 0

    while (len(pr_states) != len(pr)):
        if primera in pr_states:
            pr[primera] = j
        j += 1
        primera = siguiente_letra_mayuscula(primera)

    return pr

def crear_dict_fu(fu_states):
    primera = 'A'
    fu = {}
    j = 0

    while (len(fu_states) != len(fu)):
        if primera in fu_states:
            fu[primera] = j
        j += 1
        primera = siguiente_letra_mayuscula(primera)

    return fu

def crear_diccionarios(fu_states, pr_states):
    return crear_dict_pr(pr_states), crear_dict_fu(fu_states)

def matriz_sistema_original(fu_states, pr_states):
    print(fu_states,pr_states)
    pr, fu = crear_diccionarios(fu_states, pr_states)

    print(pr,fu)

def generate_remaining_states(combinations_list, complete_present_state, complete_future_state):
    return [(tuple(sorted(set(complete_present_state) - set(present_state))), tuple(sorted(set(complete_future_state) - set(future_state))))
            for present_state, future_state in combinations_list]



