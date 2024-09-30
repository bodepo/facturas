from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

class Vista:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Oficina")

        # Crear el Notebook
        notebook = ttk.Notebook(self.ventana)
        notebook.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Pestaña de gestión de clientes
        self.tab_clientes = ttk.Frame(notebook)
        notebook.add(self.tab_clientes, text="Gestión de Clientes")
        self.crear_seccion_clientes()

        # Pestaña de generación de facturas
        self.tab_facturas = ttk.Frame(notebook)
        notebook.add(self.tab_facturas, text="Generación de Facturas")
        self.crear_seccion_facturas()

        # Pestaña de generación de justificantes
        self.tab_justificantes = ttk.Frame(notebook)
        notebook.add(self.tab_justificantes, text="Generación de Justificantes")

    # Crear la sección de gestión de clientes
    def crear_seccion_clientes(self):
        tk.Label(self.tab_clientes, text="Nombre del Cliente").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(self.tab_clientes)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(self.tab_clientes, text="Edad").grid(row=1, column=0)
        self.entry_edad = tk.Entry(self.tab_clientes)
        self.entry_edad.grid(row=1, column=1)

        tk.Label(self.tab_clientes, text="Teléfono").grid(row=2, column=0)
        self.entry_telefono = tk.Entry(self.tab_clientes)
        self.entry_telefono.grid(row=2, column=1)

        tk.Button(self.tab_clientes, text="Alta cliente", command=self.alta_cliente).grid(row=3, column=0, pady=10)
        tk.Button(self.tab_clientes, text="Modificar cliente", command=self.modificar_cliente).grid(row=3, column=1, pady=10)
        tk.Button(self.tab_clientes, text="Baja cliente", command=self.baja_cliente).grid(row=4, column=0, pady=10)

        self.listbox_clientes = tk.Listbox(self.tab_clientes)
        self.listbox_clientes.grid(row=5, column=0, columnspan=2)
        self.listbox_clientes.bind("<<ListboxSelect>>", self.mostrar_datos_cliente)
		
    # Crear la sección de generación de facturas
    def crear_seccion_facturas(self):
        # Listbox para los clientes
        tk.Label(self.tab_facturas, text="clientes").grid(row=0, column=0, padx=10, pady=10)
        self.listbox_clientes_factura = tk.Listbox(self.tab_facturas)
        self.listbox_clientes_factura.grid(row=1, column=0, padx=10, pady=10)
        self.listbox_clientes_factura.bind("<<ListboxSelect>>", self.cargar_facturas_cliente)
	    
        # Listbox para las facturas emitidas al cliente seleccionado
        tk.Label(self.tab_facturas, text="Facturas").grid(row=0, column=1, padx=10, pady=10)
        self.listbox_facturas = tk.Listbox(self.tab_facturas)
        self.listbox_facturas.grid(row=1, column=1, padx=10, pady=10)
	    
        # Añadir otros controles (como la generación de facturas)
        tk.Label(self.tab_facturas, text="Monto").grid(row=2, column=0, padx=10, pady=10)
        self.entry_monto = tk.Entry(self.tab_facturas)
        self.entry_monto.grid(row=3, column=0)
	    
        tk.Label(self.tab_facturas, text="Concepto").grid(row=2, column=1, padx=10, pady=10)
        self.entry_concepto = tk.Entry(self.tab_facturas)
        self.entry_concepto.grid(row=3, column=1)
	    
        tk.Label(self.tab_facturas, text="Número de Factura").grid(row=4, column=0, padx=10, pady=10)
        self.entry_numero_factura = tk.Entry(self.tab_facturas)
        self.entry_numero_factura.grid(row=5, column=0)
	    
        tk.Button(self.tab_facturas, text="Generar Factura", command=self.generar_factura_cliente_existente).grid(row=5, column=1, padx=10, pady=10)
	    
        # Cargar el listado de clientes
        self.actualizar_lista_clientes_facturas()

    def cargar_facturas_cliente(self, event=None):
        try:
            index = self.listbox_clientes_factura.curselection()[0]
            cliente_seleccionado = self.listbox_clientes_factura.get(index)
            
            id_cliente = int(cliente_seleccionado.split(" - ")[0])
            facturas = self.controlador.obtener_facturas_cliente(id_cliente)
            
            self.listbox_facturas.delete(0, tk.END)
            for factura in facturas:
                self.listbox_facturas.insert(tk.END, f"Factura N° {factura[1]} - Monto: {factura[2]}")
        except IndexError:
            pass
    def actualizar_lista_clientes_facturas(self):
        self.listbox_clientes_factura.delete(0, tk.END)
        clientes = self.controlador.obtener_clientes()
        for cliente in clientes:
            self.listbox_clientes_factura.insert(tk.END, f"{cliente[0]} - {cliente[1]}")

    def alta_cliente(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        telefono = self.entry_telefono.get()
	    
        if not nombre or not edad or not telefono:
            messagebox.showerror("Error", "Por favor, completa todos los campos del cliente.")
            return
	    
        self.controlador.alta_cliente(nombre, edad, telefono)
        self.actualizar_lista_clientes()
	    
        # Limpiar los campos de entrada
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
	
    def modificar_cliente(self):
        cliente_seleccionado = self.listbox_clientes.get(tk.ACTIVE)
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un cliente.")
            return
        id_cliente = int(cliente_seleccionado.split(" - ")[0])
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        telefono = self.entry_telefono.get()
        self.controlador.modificar_cliente(id_cliente, nombre, edad, telefono)
        self.actualizar_lista_clientes()

    def baja_cliente(self):
        cliente_seleccionado = self.listbox_clientes.get(tk.ACTIVE)
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un cliente.")
            return
        id_cliente = int(cliente_seleccionado.split(" - ")[0])
        self.controlador.baja_cliente(id_cliente)
        self.actualizar_lista_clientes()

    def generar_factura_cliente_existente(self):
       cliente_seleccionado = self.listbox_clientes_factura.get(tk.ACTIVE)
       
       if not cliente_seleccionado:
           messagebox.showerror("Error", "Por favor, selecciona un cliente.")
           return
       
       id_cliente = int(cliente_seleccionado.split(" - ")[0])
       monto = self.entry_monto.get()
       concepto = self.entry_concepto.get()
       numero_factura = self.entry_numero_factura.get()
    
       if not monto or not concepto or not numero_factura:
           messagebox.showerror("Error", "Por favor, completa todos los campos de la factura.")
           return
       
       try:
           monto = float(monto)
       except ValueError:
           messagebox.showerror("Error", "El monto debe ser un número válido.")
           return
    
       # 1. Generar el PDF de la factura
       self.controlador.generar_factura_pdf(id_cliente, monto, concepto, numero_factura)
    
       # 2. Guardar la factura en la base de datos
       self.controlador.guardar_factura(id_cliente, monto, concepto, numero_factura)
    
       # 3. Actualizar el Listbox de facturas
       self.cargar_facturas_cliente(None)
    
       messagebox.showinfo("Éxito", f"Factura {numero_factura} generada exitosamente.")
       self.limpiar_campos_factura()

    def actualizar_lista_clientes(self):
        self.listbox_clientes.delete(0, tk.END)
        clientes = self.controlador.obtener_clientes()
        for cliente in clientes:
            self.listbox_clientes.insert(tk.END, f"{cliente[0]} - {cliente[1]}")
	
    def mostrar_datos_cliente(self, event):
        try:
            index = self.listbox_clientes.curselection()[0]
            cliente_seleccionado = self.listbox_clientes.get(index)
	    
            id_cliente = int(cliente_seleccionado.split(" - ")[0])
            datos_cliente = self.controlador.obtener_datos_cliente(id_cliente)
	    
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, datos_cliente[0])
	    
            self.entry_edad.delete(0, tk.END)
            self.entry_edad.insert(0, datos_cliente[1])
	    
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, datos_cliente[2])
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un cliente.")
    def limpiar_campos_factura(self):
        self.entry_monto.delete(0, tk.END)
        self.entry_concepto.delete(0, tk.END)
        self.entry_numero_factura.delete(0, tk.END)
    