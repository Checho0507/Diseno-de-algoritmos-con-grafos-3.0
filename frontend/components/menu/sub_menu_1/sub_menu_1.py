import streamlit as st
from streamlit_react_flow import react_flow
from frontend.components.menu.sub_menu_1.sub_menu_2 import sub_menu_2
from backend.utils import file_json
from backend.models.graph import Grafo
from backend.generators import json_elements
from backend.generators import graph_generator

Elements = Grafo()
# Placeholder for storing questions and answers
qa_store = {}

def file_menu():
    st.subheader("Seleccionaste el menu de archivo")
    # Opciones del submenú "Archivo"
    file_options = ["Nuevo Grafo", "Abrir", "Cerrar", "Guardar", "Guardar como", "Exportar Datos", "Importar Datos",
                   "Salir"]
    selected_option = st.sidebar.selectbox("Opciones de Archivo", file_options, index=1)

    if selected_option is not None:
        if selected_option == "Nuevo Grafo":
            sub_menu_2.new_grafo_menu()
        elif selected_option == "Exportar Datos":
            st.write(f"Seleccionaste la opción de menu: {selected_option}")
            sub_menu_2.export_data_menu()
        elif selected_option == "Importar Datos":
            st.write(f"Seleccionaste la opción de menu: {selected_option}")
            elements = []
            Elements.set_elements(elements)
            Elements.open_txt()
        elif selected_option == "Abrir":
            st.write(f"Seleccionaste la opción de menu: {selected_option}")
            Elements.open_json()
        elif selected_option == "Guardar":
            if Elements.get_elements() == []:
               st.write("No existen elementos a guardar")
            else:
               st.write(f"Seleccionaste la opción: {selected_option}")
               file_json.save_elements_to_json(Elements.get_elements(), "documents/saved")
        elif selected_option == "Guardar como":
            if Elements.get_elements() == []:
               st.write("No existen elementos a guardar")
            else:
               nombreArchivo = st.text_input("Ingrese el nombre del archivo a guardar:")
               if nombreArchivo != "":
                   file_json.save_elements_to_json_as(Elements.get_elements(), "documents/saved_as", nombreArchivo)
        elif selected_option == "Cerrar":
            st.write("De clic en confirmar para cerrar el espacio de trabajo")
            clic = st.button("Confirmar")
            if clic:
               elements = []
               Elements.set_elements(elements)
               st.warning("Se ha cerrado el espacio de trabajo")
        elif selected_option == "Salir":
            st.write("Cerrando pestaña...")
            # Redirigir a una página inexistente para cerrar la pestaña
            st.markdown("<meta http-equiv='refresh' content='0;URL=about:blank' />", unsafe_allow_html=True)
        else:
            st.write(f"Seleccionaste la opción de archivo: {selected_option}")

    return Elements

def edit_menu():
    graph_generator.custom_elements = []
    if Elements.get_elements():
        st.subheader("Seleccionaste el menu de editar")
        st.sidebar.subheader("Editar")
        # Opciones del submenú "Editar"
        edit_options = ["Deshacer", "Nodo", "Arista"]
        selected_option = st.sidebar.selectbox("Opciones de Editar", edit_options, index=1)
        if selected_option is not None:
            st.write(f"Seleccionaste la opción de editar: {selected_option}")
            if selected_option == "Nodo":
               sub_menu_2.edit_nodo_menu()
            elif selected_option == "Arista":
               sub_menu_2.edit_arco_menu()
            elif selected_option == "Deshacer":
               Elements.set_elements(Elements.undo_last_change(Elements.get_elements()))
    else:
        st.warning("Selecciona un archivo a editar, o crea un grafo")
        
def tools_menu(elements):
   st.subheader("Seleccionaste el menu de herramientas")
   st.sidebar.subheader("Herramientas")
   # Opciones del submenú "Herramientas"
   tools_options = ["Ventana Gráfica", "Tabla"]
   selected_option = st.sidebar.selectbox("Opciones de Herramientas", tools_options)

   # Mostrar mensaje dependiendo de la opción seleccionada
   st.write(f"Seleccionaste la opción de herramientas: {selected_option}")

def window_menu(elements):
   st.subheader("Seleccionaste el menu de ventana")
   st.sidebar.subheader("Ventana")
   # Opciones del submenú "Ventana"
   window_options = ["Gráfica", "Tabla"]
   selected_option = st.sidebar.selectbox("Opciones de Ventana", window_options)

   # Mostrar mensaje dependiendo de la opción seleccionada
   st.write(f"Seleccionaste la opción de ventana: {selected_option}")

def help_menu():
    st.subheader("Seleccionaste el menu de ayuda")
    st.sidebar.subheader("Ayuda")
    # Opciones del submenú "Ayuda"
    help_options = ["Ayuda", "Acerca de Grafos"]
    selected_option = st.sidebar.selectbox("Opciones de Ayuda", help_options)

    # Mostrar mensaje dependiendo de la opción seleccionada
    st.write(f"Seleccionaste la opción de ayuda: {selected_option}")

    if selected_option == "Acerca de Grafos":
        st.subheader("Acerca de Grafos")
        st.write("""
        ## Introducción a los Grafos
        Un grafo es una estructura matemática usada para modelar relaciones entre objetos. Un grafo se compone de nodos (o vértices) y aristas (o enlaces) que conectan pares de nodos. Los grafos pueden ser dirigidos, donde las aristas tienen una dirección, o no dirigidos, donde las aristas no tienen dirección.
        """)
        st.image("https://resumos.leic.pt/static/55afcc0f50f213fce2d31f0065bd92e4/0aaa2/0018-grafop.png", caption="Ejemplo de un Grafo")

        st.write("""
        ### Grafos Bipartitos
        Un grafo bipartito es un tipo especial de grafo cuyas nodos pueden dividirse en dos conjuntos disjuntos U y V, tales que ninguna arista conecta dos nodos dentro del mismo conjunto. Es decir, cada arista en el grafo conecta un nodo en U con un nodo en V.
        """)
        st.image("https://aprende.olimpiada-informatica.org/sites/default/files/inline-images/grafobipartito.png", caption="Ejemplo de un Grafo Bipartito")

        st.write("""
        ### Propiedades de los Grafos Bipartitos
        - No contienen ciclos de longitud impar.
        - Pueden representarse mediante una matriz de incidencia.
        - Se utilizan comúnmente en problemas de emparejamiento.

        ### Aplicaciones de los Grafos en la Vida Real
        Los grafos tienen una amplia variedad de aplicaciones prácticas, incluyendo:
        """)

        st.write("""
        #### Redes Sociales
        En las redes sociales, los usuarios son representados como nodos y las amistades como aristas. Esto permite analizar la estructura de la red social, identificar comunidades, y encontrar influenciadores.
        """)
        st.image("https://www.inesem.es/revistadigital/informatica-y-tics/files/2017/03/Sin-t%C3%ADtulo-1.png", caption="Análisis de Redes Sociales")

        st.write("""
        #### Redes de Transporte
        En las redes de transporte, las estaciones son representadas como nodos y las rutas como aristas. Esto permite optimizar rutas, analizar la conectividad de la red, y mejorar la eficiencia del transporte.
        """)
        st.image("https://tse4.explicit.bing.net/th?id=OIP.Id0uRl9XjGWq41enPn2V8wHaDU&pid=Api&P=0&h=180.png", caption="Red de Transporte de París")

        st.write("""
        #### Redes Neuronales
        En las redes neuronales, las neuronas son representadas como nodos y las conexiones sinápticas como aristas. Esto permite modelar y entender el funcionamiento del cerebro, así como desarrollar algoritmos de inteligencia artificial.
        """)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Artificial_neural_network.svg/1280px-Artificial_neural_network.svg.png", caption="Red Neuronal Artificial")

    if selected_option == "Ayuda":
        st.write("¿Necesitas ayuda?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sí"):
                st.session_state.help_selected = "ask_problems"
                st.experimental_rerun()
        with col2:
            if st.button("No"):
                st.success("Fue un placer ayudarte")

    if "help_selected" in st.session_state and st.session_state.help_selected == "ask_problems":
        ask_problems()

def ask_problems():
    global qa_store
    st.write("Seleccione uno de los problemas iniciales o ingrese su propia pregunta:")
    # Combina las preguntas predefinidas con las preguntas del usuario
    problems = [
        "¿Cómo eliminar un nodo?",
        "¿Cómo agregar una arista?",
        "¿Cómo crear un grafo aleatorio?"
    ] + list(qa_store.keys()) + ["Mi pregunta no aparece"]
    
    selected_problem = st.radio("Problemas:", problems, index = 0)

    if selected_problem == problems[0]:
        st.write("1) Asegúrese de tener un grafo abierto, dé clic en editar, nodo y luego en eliminar, posteriormente seleccione el nodo a eliminar.")
    elif selected_problem == problems[1]:
        st.write("2) Asegúrese de tener al menos dos nodos, dé clic en editar, arista y luego en agregar, posteriormente seleccione el tipo de arista y los nodos a conectar.")
    elif selected_problem == problems[2]:
        st.write("3) Dé clic en archivo, nuevo grafo y luego en aleatorio, ingrese la cantidad de nodos a crear y el tipo de grafo deseado.")
    elif selected_problem == problems[-1]:  # La opción "Mi pregunta no aparece"
        custom_question()
    else:
        show_question_answer(selected_problem)

def custom_question():
    global qa_store
    question = st.text_input("Ingrese su pregunta:")
    if question:
        if question not in qa_store:
            st.write("Gracias por tu pregunta. Será almacenada para futuras referencias.")
            st.write("¿Tienes una respuesta para esta pregunta?")
            response = st.text_area("Escribe tu respuesta aquí:")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sí, tengo una respuesta"):
                    qa_store[question] = {"answer": response, "no_votes": 0}
                    st.success("Gracias! Tu pregunta y respuesta han sido guardadas.")
                    st.experimental_rerun()
            with col2:
                if st.button("No, no tengo respuesta"):
                    qa_store[question] = {"answer": None, "no_votes": 0}
                    st.warning("Tu pregunta ha sido guardada. Trataremos de encontrar una respuesta en el futuro.")
                    st.experimental_rerun()
        else:
            show_question_answer(question)

def show_question_answer(question):
    global qa_store
    if qa_store[question]["answer"]:
        st.write(f"Pregunta: {question}")
        st.write(f"Respuesta almacenada: {qa_store[question]['answer']}")
        st.write("¿Te sirvió la respuesta?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sí :)"):
                st.success("Nos alegra haberte ayudado.")
                st.experimental_rerun()
        with col2:
            if st.button("No :("):
                qa_store[question]["no_votes"] += 1
                if qa_store[question]["no_votes"] >= 3:
                    qa_store[question] = {"answer": None, "no_votes": 0}
                    st.warning("La respuesta ha sido eliminada debido a repetidas evaluaciones negativas.")
                else:
                    st.warning("Lo sentimos. Trabajaremos para mejorar nuestras respuestas.")
    else:
        st.write("No tenemos una respuesta para esta pregunta.") 
        st.write("¿Deseas agregar una respuesta?")
        response = st.text_area("Escribe tu respuesta aquí:")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sí, agregar respuesta"):
                qa_store[question]["answer"] = response
                qa_store[question]["no_votes"] = 0
                st.success("Gracias! Tu respuesta ha sido guardada.")
                st.experimental_rerun()
        with col2:
            if st.button("No, no agregar respuesta"):
                st.warning("Gracias por tu pregunta. Trataremos de encontrar una respuesta en el futuro.")
                st.experimental_rerun()

if "help_selected" not in st.session_state:
    st.session_state.help_selected = None