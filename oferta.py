from algorithm.algoritmo_genetico import Algoritmo
from algorithm.poblacion import Poblacion
from algorithm.data import Data
from connection_db import Connection
import tkinter as tk
from tkinter import ttk

class OfertaW:
    def __init__(self, root, name):
        self.root = root
        self.root.title("OFERTA")

        self.root.geometry("1600x800")
        self.root.resizable(height=False, width=False)

        self.name = name
        tk.Label(self.root, text=f'¡USUARIO ACTUAL: {self.name}!', font='Arial 10').place(x=30, y=30)

        self.btn_generate_oferta = tk.Button(self.root, text='GENERAR OFERTA', command=self.generate_oferta)
        self.btn_generate_oferta.place(x=350, y=55)

        # -------------------- TABLE --------------------------

        # Table
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Calibri", 14, 'bold'), padding=7)
        self.table = ttk.Treeview(self.root, columns=('', '', '', '', '', '', ''), show='headings')
        self.table.tag_configure('estilo_personalizado', font=('Arial', 12), background='light grey')
        # self.table.grid(row=5, column=0, columnspan=2, padx=70, pady=30)
        self.table.place(x=90, y=250, height=400)
        self.table.heading('#1', text='NRC')
        self.table.heading('#2', text='Curso')
        self.table.heading('#3', text='Horario')
        self.table.heading('#4', text='Salon')
        self.table.heading('#5', text='Profesor')
        self.table.heading('#6', text='Fecha de Inicio')
        self.table.heading('#7', text='Fecha Fin')
        for i in range(1, 8):
            self.table.column(f'#{i}', anchor=tk.CENTER)


    def show_registers(self, where=""):
        registers = self.table.get_children()
        for register in registers:
            self.table.delete(register)

        if len(where) > 0:
            query_select = f'SELECT * FROM ofertas {where}'
        else:
            query_select = 'SELECT * FROM ofertas'
        with Connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_select)
                data = cursor.fetchall()
                for a in (data):
                    self.table.insert('', 'end', values=a, tags='estilo_personalizado')


    def generate_oferta(self):
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                query = "DELETE FROM ofertas"
                cursor.execute(query)

        data = Data()
        n_generacion = 1
        print(f'\n GENERACION #{n_generacion}')
        poblacion = Poblacion(data.TAMANIO_POBLACION, data)
        poblacion.get_ofertas().sort(key=lambda x: x.get_fitness(), reverse=True)
        for oferta in poblacion.get_ofertas():
            print(f'**OFERTA**\n{oferta}\n\n')

        genetico = Algoritmo()

        while (poblacion.get_ofertas()[0].get_fitness() != 1.0):
            if (n_generacion == 1500):
                print('\n\n****SOLUCION NO ENCONTRADA****\n\n')
                break
            n_generacion += 1
            print('---------------------------------------------------------------------------------')
            print(f'\n GENERACION #{n_generacion}')
            poblacion = genetico.evolucionar(poblacion)
            poblacion.get_ofertas().sort(key=lambda x: x.get_fitness(), reverse=True)
            for oferta in poblacion.get_ofertas():
                print(f'**OFERTA** \n{oferta}\n\n')

        oferta_final = poblacion.get_ofertas()[0]

        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                for clase in oferta_final.get_final_clases():
                    query= f"""INSERT INTO ofertas(nrc, curso, horario, salon, maestro, fecha_inicio, fecha_fin)
                            VALUES('{clase.get_id()}', '{clase.get_curso().get_numero()}', {clase.get_tiempo().get_id()},
                            '{clase.get_salon().get_numero()}', '{clase.get_profesor().get_id()}', '16/01/2024', '01/06/2024')"""
                    cursor.execute(query)
        
        self.show_registers()

if __name__ == '__main__':
    root = tk.Tk()
    app = OfertaW(root, 'Prueba')
    root.mainloop()