from controlador import Controlador
from vista import Vista

if __name__ == "__main__":
    # Crear la vista primero, pasando 'None' al controlador
    controlador = Controlador(None)  # Pasar None si la vista se inicializa después

    # Crear la vista y enlazarla con el controlador
    vista = Vista(controlador)
    controlador.vista = vista  # Enlazar la vista al controlador
    
    # Cargar la lista de clientes al iniciar la aplicación
    vista.actualizar_lista_clientes()
    
    # Iniciar la interfaz gráfica
    vista.ventana.mainloop()
