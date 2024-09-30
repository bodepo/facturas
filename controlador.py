import modelo

class Controlador:
    def __init__(self, vista):
        self.vista = vista

    def alta_cliente(self, nombre, edad, telefono):
        modelo.alta_cliente(nombre, edad, telefono)

    def modificar_cliente(self, id_cliente, nombre, edad, telefono):
        modelo.modificar_cliente(id_cliente, nombre, edad, telefono)

    def baja_cliente(self, id_cliente):
        modelo.baja_cliente(id_cliente)

    def obtener_clientes(self):
        return modelo.obtener_clientes()

    def obtener_datos_cliente(self, id_cliente):
        return modelo.obtener_datos_cliente(id_cliente)

    def obtener_nombre_cliente(self, id_cliente):
        # Obtener el nombre del cliente a partir de los datos
        datos_cliente = modelo.obtener_datos_cliente(id_cliente)
        return datos_cliente[0]  # Asumiendo que el nombre es el primer dato

    def generar_factura(self, id_cliente, monto, concepto, numero_factura):
        modelo.guardar_factura(id_cliente, monto, concepto, numero_factura)

    def obtener_facturas_cliente(self, id_cliente):
        return modelo.obtener_facturas_cliente(id_cliente)

    def generar_factura_pdf(self, id_cliente, monto, concepto, numero_factura):
        # Obtener el nombre del cliente
        nombre_cliente = self.obtener_nombre_cliente(id_cliente)
        # Generar el PDF de la factura
        modelo.generar_factura_pdf(nombre_cliente, monto, concepto, numero_factura)

    def guardar_factura(self, id_cliente, monto, concepto, numero_factura):
        modelo.guardar_factura(id_cliente, monto, concepto, numero_factura)

	
