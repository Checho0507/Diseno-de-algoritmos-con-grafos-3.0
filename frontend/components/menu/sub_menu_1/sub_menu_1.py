import streamlit as st
from streamlit_react_flow import react_flow
from frontend.components.menu.sub_menu_1.sub_menu_2 import sub_menu_2
from backend.utils import file_json
from backend.models.graph import Elements
from backend.generators import json_elements


def file_menu():
    st.subheader("Seleccionaste el menu de archivo")
    # Opciones del submenú "Archivo"
    file_options = ["Nuevo Grafo", "Abrir", "Cerrar", "Guardar", "Guardar como", "Exportar Datos", "Importar Datos",
                    "Salir"]
    selected_option = st.sidebar.selectbox("Opciones de Archivo", file_options, index=1)

    if selected_option is not None:
        if selected_option == "Nuevo Grafo":
            elementos = []
            Elements.set_elements(elementos)
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
                elementos = json_elements.convert_to_save_elements(Elements.get_elements())
                st.write(f"Seleccionaste la opción: {selected_option}")
                file_json.save_elements_to_json(elementos, "documents/saved")
        elif selected_option == "Guardar como":
            if Elements.get_elements() == []:
                st.write("No existen elementos a guardar")
            else:
                elementos = json_elements.convert_to_save_elements(Elements.get_elements())
                nombreArchivo = st.text_input("Ingrese el nombre del archivo a guardar:")
                if nombreArchivo != "":
                    file_json.save_elements_to_json_as(elementos, "documents/saved_as", nombreArchivo)
        elif selected_option == "Cerrar":
            elements = []
            Elements.set_elements(elements)
            st.warning("Se ha cerrado el espacio de trabajo")
        elif selected_option == "Salir":
            st.write("Cerrando pestaña...")
            # Redirigir a una página inexistente para cerrar la pestaña
            st.markdown("<meta http-equiv='refresh' content='0;URL=about:blank' />", unsafe_allow_html=True)
        else:
            st.write(f"Seleccionaste la opción de archivo: {selected_option}")
    selected_option = None

    return Elements


def edit_menu():
    if Elements.get_elements():
        st.subheader("Seleccionaste el menu de editar")
        st.sidebar.subheader("Editar")
        # Opciones del submenú "Editar"
        edit_options = ["Deshacer", "Nodo", "Arista"]
        selected_option = st.sidebar.selectbox("Opciones de Editar", edit_options, index=0)
        if selected_option is not None:
            st.write(f"Seleccionaste la opción de editar: {selected_option}")
            if selected_option == "Nodo":
                sub_menu_2.edit_nodo_menu()
            elif selected_option == "Arista":
                sub_menu_2.edit_arco_menu()
            elif selected_option == "Deshacer":
                Elements.set_elements(Elements.undo_last_change(Elements.get_elements()))

        Elements.set_elements(json_elements.create_elements_from_list(Elements.get_elements()))
        flow_styles = {"height": 500, "width": 800}
        react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)
    else:
        st.subheader("Selecciona un archivo a editar, o crea un grafo")


def execute_menu(elements):
    st.subheader("Seleccionaste el menu de ejecutar")
    st.sidebar.subheader("Ejecutar")
    # Opciones del submenú "Ejecutar"
    execute_options = ["Procesos"]
    selected_option = st.sidebar.selectbox("Opciones de Ejecutar", execute_options)

    if selected_option == "Procesos":
        processes_menu()
    else:
        st.write(f"Seleccionaste la opción de procesos: {selected_option}")


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


def help_menu(elements):
    st.subheader("Seleccionaste el menu de ayuda")
    st.sidebar.subheader("Ayuda")
    # Opciones del submenú "Ayuda"
    help_options = ["Ayuda", "Acerca de Grafos"]
    selected_option = st.sidebar.selectbox("Opciones de Ayuda", help_options)

    # Mostrar mensaje dependiendo de la opción seleccionada
    st.write(f"Seleccionaste la opción de ayuda: {selected_option}")