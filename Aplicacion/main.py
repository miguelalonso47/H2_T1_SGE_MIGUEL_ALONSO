import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib import pyplot as plt

from database import insert_encuesta, get_encuestas, update_encuesta, delete_encuesta, get_encuestas_filtradas
from export import export_to_excel
from graphs import mostrar_grafico_barras

class EncuestaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Encuestas de Consumo de Alcohol")
        self.geometry("1100x800")

        # Frame para los campos de entrada, inicialmente ocultos
        self.frame_entradas = tk.Frame(self)

        fields = [
            "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
            "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
            "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
        ]

        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(self.frame_entradas, text=field + ":").grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(self.frame_entradas)
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Frame para los botones de acción
        self.frame_botonera = tk.Frame(self)
        self.frame_botonera.pack(side="bottom", fill="x", pady=20)

        # Botón de agregar encuesta
        self.boton_agregar = tk.Button(self.frame_botonera, text="Agregar Encuesta",
                                       command=self.mostrar_campos_agregar)
        self.boton_agregar.pack(side="left", padx=10)

        # Botón para filtrar
        self.boton_filtrar = tk.Button(self.frame_botonera, text="Filtrar", command=self.mostrar_filtro)
        self.boton_filtrar.pack(side="left", padx=10)

        # Otros botones
        tk.Button(self.frame_botonera, text="Actualizar Encuesta", command=self.actualizar_encuesta).pack(side="left",
                                                                                                          padx=10)
        tk.Button(self.frame_botonera, text="Eliminar Encuesta", command=self.eliminar_encuesta).pack(side="left",
                                                                                                      padx=10)

        tk.Button(self.frame_botonera, text="Mostrar Gráfico", command=self.mostrar_ventana_grafico).pack(side="left",
                                                                                                          padx=10)

        # Frame para la tabla de encuestas
        self.frame_tabla = tk.Frame(self)
        self.frame_tabla.pack(pady=10, expand=True, fill="both")

        # Añadimos 'idEncuesta' a las columnas de la tabla
        self.tree = ttk.Treeview(self.frame_tabla, columns=["idEncuesta"] + fields, show="headings")

        # Cabeceras
        self.tree.heading("idEncuesta", text="ID Encuesta")
        for field in fields:
            self.tree.heading(field, text=field)

        # Configuración de alineación para centrar los datos y los encabezados
        self.tree.column("idEncuesta", anchor="center", width=100)  # Alineamos al centro
        for field in fields:
            self.tree.column(field, anchor="center", width=100)  # Alineamos los valores al centro

        self.tree.pack(fill="both", expand=True)

        self.cargar_encuestas()

        # Campo de entrada para filtro (inicialmente oculto)
        self.frame_filtro = tk.Frame(self)
        self.frame_filtro.pack_forget()

        # Menú para seleccionar el campo a filtrar
        tk.Label(self.frame_filtro, text="Filtrar por:").grid(row=0, column=0, padx=10, pady=5)
        self.filtro_campo = ttk.Combobox(self.frame_filtro, values=fields, state="readonly")
        self.filtro_campo.grid(row=0, column=1, padx=10, pady=5)
        self.filtro_campo.set(fields[0])  # Seleccionamos el primer campo por defecto

        # Campo para ingresar el valor del filtro
        tk.Label(self.frame_filtro, text="Valor del Filtro:").grid(row=1, column=0, padx=10, pady=5)
        self.filtro_valor = tk.Entry(self.frame_filtro)
        self.filtro_valor.grid(row=1, column=1, padx=10, pady=5)

        # Botón para aplicar el filtro
        self.boton_aplicar_filtro = tk.Button(self.frame_filtro, text="Aplicar Filtro", command=self.aplicar_filtro)
        self.boton_aplicar_filtro.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para cancelar el filtro
        self.boton_cancelar_filtro = tk.Button(self.frame_filtro, text="Cancelar", command=self.cancelar_filtro)
        self.boton_cancelar_filtro.grid(row=3, column=0, columnspan=2, pady=5)

    def obtener_valores(self):
        return [entry.get() for entry in self.entries.values()]

    def mostrar_campos_agregar(self):
        # Ocultar los botones y mostrar los campos de entrada
        self.frame_botonera.pack_forget()  # Ocultamos los botones de la parte inferior
        self.boton_agregar.config(state="disabled")  # Deshabilitamos el botón "Agregar Encuesta"

        # Volver a mostrar los campos de entrada
        self.frame_entradas.pack(pady=20)

        # Agregar un campo para el ID, que será de solo lectura
        tk.Label(self.frame_entradas, text="ID Encuesta:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_id = tk.Entry(self.frame_entradas, state="readonly")
        self.entry_id.grid(row=0, column=1, padx=10, pady=5)

        # Mostrar el siguiente ID disponible
        self.obtener_proximo_id()

        # Agregamos un botón para guardar la encuesta
        self.boton_guardar = tk.Button(self.frame_entradas, text="Guardar Encuesta", command=self.agregar_encuesta)
        self.boton_guardar.grid(row=len(self.entries) + 1, column=0, columnspan=2, pady=10)

        # Botón para cancelar y volver a la vista principal
        self.boton_cancelar = tk.Button(self.frame_entradas, text="Cancelar", command=self.cancelar_agregar)
        self.boton_cancelar.grid(row=len(self.entries) + 2, column=0, columnspan=2, pady=5)

    def obtener_proximo_id(self):
        encuesta = get_encuestas()[-1] if get_encuestas() else None
        siguiente_id = encuesta["idEncuesta"] + 1 if encuesta else 1
        self.entry_id.insert(0, str(siguiente_id))

    def cancelar_agregar(self):
        # Ocultar los campos de entrada y volver a mostrar los botones
        self.frame_entradas.pack_forget()  # Ocultamos los campos de entrada
        self.frame_botonera.pack(side="bottom", fill="x", pady=20)  # Volvemos a mostrar los botones
        self.boton_agregar.config(state="normal")  # Habilitamos el botón de "Agregar Encuesta"

    def agregar_encuesta(self):
        data = self.obtener_valores()  # Obtenemos todos los valores de los campos
        insert_encuesta(data)  # Llamamos a la función para insertar la encuesta (sin necesidad de incluir idEncuesta)
        messagebox.showinfo("Éxito", "Encuesta agregada correctamente")
        self.cargar_encuestas()
        self.cancelar_agregar()

    def actualizar_encuesta(self):
        # Asegurarnos de que no queden botones visibles
        for widget in self.frame_entradas.winfo_children():
            widget.destroy()

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una encuesta para actualizar")
            return

        item = self.tree.item(selected_item)
        id_encuesta = item["values"][0]  # Obtenemos el ID de la encuesta seleccionada
        encuesta = get_encuestas_filtradas("idEncuesta", id_encuesta)[0]

        # Ocultar los botones y mostrar los campos de entrada para la actualización
        self.frame_botonera.pack_forget()
        self.frame_entradas.pack(pady=20)

        # Mostrar el ID de la encuesta, pero como campo de solo lectura
        tk.Label(self.frame_entradas, text="ID Encuesta:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_id = tk.Entry(self.frame_entradas, state="readonly")
        self.entry_id.grid(row=0, column=1, padx=10, pady=5)
        self.entry_id.insert(0, id_encuesta)

        # Llenar los campos con los datos de la encuesta seleccionada
        for i, (field, value) in enumerate(encuesta.items()):
            if field != "idEncuesta":  # Excluimos el ID, ya que es solo lectura
                tk.Label(self.frame_entradas, text=f"{field}:").grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
                entry = tk.Entry(self.frame_entradas)
                entry.insert(0, value)
                entry.grid(row=i + 1, column=1, padx=10, pady=5)
                self.entries[field] = entry

        # Botón para guardar los cambios
        self.boton_guardar = tk.Button(self.frame_entradas, text="Guardar Cambios", command=self.guardar_actualizacion)
        self.boton_guardar.grid(row=len(encuesta) + 1, column=0, columnspan=2, pady=10)

        # Botón para cancelar la actualización
        self.boton_cancelar = tk.Button(self.frame_entradas, text="Cancelar", command=self.cancelar_actualizacion)
        self.boton_cancelar.grid(row=len(encuesta) + 2, column=0, columnspan=2, pady=5)

    def guardar_actualizacion(self):
        # Recogemos los datos de los campos
        data = self.obtener_valores()
        id_encuesta = self.entry_id.get()  # Obtenemos el ID de la encuesta que estamos actualizando

        # Imprimir los datos para ver si son correctos
        print("Datos a actualizar:", data)
        print("ID Encuesta:", id_encuesta)

        # Llamamos a la función para actualizar la encuesta en la base de datos
        update_encuesta(data, id_encuesta)

        # Verificación: Mostrar los datos actualizados
        encuestas = get_encuestas_filtradas("idEncuesta", id_encuesta)  # Obtén la encuesta actualizada
        print("Encuesta actualizada:", encuestas)

        messagebox.showinfo("Éxito", "Encuesta actualizada correctamente")
        self.cargar_encuestas()  # Recarga la tabla
        self.cancelar_actualizacion()  # Cierra el modo de actualización

    def cancelar_actualizacion(self):
        # Limpiar todos los widgets del frame de entradas
        for widget in self.frame_entradas.winfo_children():
            widget.destroy()

        # Ocultar el frame de entradas y volver a mostrar los botones principales
        self.frame_entradas.pack_forget()
        self.frame_botonera.pack(side="bottom", fill="x", pady=20)

    def eliminar_encuesta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una encuesta para eliminar")
            return

        item = self.tree.item(selected_item)
        id_encuesta = item["values"][0]
        delete_encuesta(id_encuesta)
        messagebox.showinfo("Éxito", "Encuesta eliminada correctamente")
        self.cargar_encuestas()

    def mostrar_filtro(self):
        # Mostrar el frame de filtro
        self.frame_filtro.pack(pady=10)

    def aplicar_filtro(self):
        campo_filtro = self.filtro_campo.get()
        valor_filtro = self.filtro_valor.get()

        if not valor_filtro:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un valor para el filtro")
            return

        # Obtener las encuestas filtradas
        self.encuestas_filtradas = get_encuestas_filtradas(campo_filtro, valor_filtro)

        # Limpiar los resultados anteriores
        for row in self.tree.get_children():
            self.tree.delete(row)

        for encuesta in self.encuestas_filtradas:
            self.tree.insert("", "end",
                             values=[encuesta["idEncuesta"]] + [encuesta[field] for field in encuesta.keys()][1:])

        # Mostrar el botón de exportación solo cuando haya resultados filtrados
        self.mostrar_boton_exportar()

    def mostrar_boton_exportar(self):
        # Eliminar cualquier botón de exportación existente
        for widget in self.frame_botonera.winfo_children():
            if widget.cget("text") == "Exportar a Excel":
                widget.destroy()

        # Ahora agregamos el botón de exportación
        self.boton_exportar = tk.Button(self.frame_botonera, text="Exportar a Excel", command=self.exportar_excel)
        self.boton_exportar.pack(side="left", padx=10)

    def cancelar_filtro(self):
        # Cancelar el filtro y mostrar todas las encuestas
        self.frame_filtro.pack_forget()  # Ocultamos el frame de filtro
        self.cargar_encuestas()  # Recargamos todas las encuestas

    def mostrar_tabla(self, encuestas):
        # Primero, eliminamos todas las filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ahora insertamos las filas con los nuevos datos
        for encuesta in encuestas:
            self.tree.insert("", "end", values=[encuesta["idEncuesta"]] + list(encuesta.values())[1:])

    def cargar_encuestas(self):
        encuestas = get_encuestas()  # Asegúrate de que esta función está trayendo los datos correctos
        self.mostrar_tabla(encuestas)  # Actualiza la tabla con los datos más recientes

    def exportar_excel(self):
        if not hasattr(self, "encuestas_filtradas"):
            messagebox.showwarning("Advertencia", "No hay datos filtrados para exportar")
            return

        export_to_excel(self.encuestas_filtradas)  # Exportamos las encuestas filtradas

    def mostrar_grafico(self):
        encuestas = get_encuestas()
        mostrar_grafico_barras(encuestas)

    def mostrar_ventana_grafico(self):
        # Crear una nueva ventana emergente para elegir el gráfico
        ventana_grafico = tk.Toplevel(self)
        ventana_grafico.title("Seleccionar Gráfico")
        ventana_grafico.geometry("300x200")

        # Etiqueta y campo para seleccionar el campo del gráfico
        tk.Label(ventana_grafico, text="Seleccionar campo para el gráfico:").pack(padx=10, pady=5)

        campos_grafico = [
            "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
            "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
            "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
        ]

        # ComboBox para seleccionar el campo
        campo_seleccionado = ttk.Combobox(ventana_grafico, values=campos_grafico, state="readonly")
        campo_seleccionado.set(campos_grafico[0])  # Selecciona un campo por defecto
        campo_seleccionado.pack(padx=10, pady=10)

        # Etiqueta y campo para seleccionar el tipo de gráfico
        tk.Label(ventana_grafico, text="Seleccionar tipo de gráfico:").pack(padx=10, pady=5)

        tipos_grafico = ["Barras", "Líneas"]
        tipo_grafico_seleccionado = ttk.Combobox(ventana_grafico, values=tipos_grafico, state="readonly")
        tipo_grafico_seleccionado.set(tipos_grafico[0])  # Selecciona el tipo de gráfico por defecto
        tipo_grafico_seleccionado.pack(padx=10, pady=10)

        # Botón para aceptar y mostrar el gráfico
        boton_aceptar = tk.Button(ventana_grafico, text="Aceptar", command=lambda: self.generar_grafico(
            campo_seleccionado.get(), tipo_grafico_seleccionado.get(), ventana_grafico))
        boton_aceptar.pack(pady=10)

    def generar_grafico(self, campo, tipo_grafico, ventana):
        # Obtener las encuestas
        encuestas = get_encuestas()

        # Extraer los datos según el campo seleccionado
        datos = [encuesta[campo] for encuesta in encuestas]

        # Generar el gráfico según el tipo seleccionado
        if tipo_grafico == "Barras":
            plt.bar(range(len(datos)), datos)
            plt.ylabel(campo)
            plt.xlabel('Id')
            plt.title(f'Gráfico de {campo} - Tipo de Gráfico: Barras')
        elif tipo_grafico == "Líneas":
            plt.plot(range(len(datos)), datos)
            plt.ylabel(campo)
            plt.xlabel('Id')
            plt.title(f'Gráfico de {campo} - Tipo de Gráfico: Líneas')

        # Mostrar el gráfico
        plt.show()

        # Cerrar la ventana de selección de gráfico después de generar el gráfico
        ventana.destroy()

if __name__ == "__main__":
    app = EncuestaApp()
    app.mainloop()






