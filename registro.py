import tkinter as tk
from tkinter import messagebox, ttk
from connection_db import Connection

class Registro:
    def __init__(self, root, name):
        self.root = root
        self.root.title("REGISTRO")

        self.root.geometry("800x400")
        self.root.resizable(height=False, width=False)

        self.name = name
        tk.Label(self.root, text=f'¡USUARIO ACTUAL: {self.name}!', font='Arial 10').place(x=30, y=30)

        tk.Label(self.root, text=f'Ingresa los NRC de las materias que deseas agendar (Unicamente correspondientes a tu carrera)', font='Arial 10').place(x=30, y=60)

        tk.Label(self.root, text='NRC: ').place(x=20, y=100)
        self.txt_nrc = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_nrc.place(x=120, y=100)

        self.save_clase = tk.Button(self.root, text='GUARDAR', command=self.save_clase)
        self.save_clase.place(x=300, y=95)

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

    def save_clase(self):
        if(len(self.txt_nrc.get) != 0):
            error = 0
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    query = f"""SELECT c.nombre AS nombre_curso
                                FROM Alumnos a
                                JOIN Cursos c ON a.carrera = c.carrera
                                JOIN Ofertas o ON c.clave = o.curso
                                WHERE a.email = '{self.name}';"""
                    cursor.execute(query)
                    data = cursor.fetchall()

                    if not data:
                        messagebox.showinfo(message='Error: NO PERTENECES A ESA CARRERA')
                    else:
                        query = f"""SELECT email, codigo, FROM alumnos WHERE email = '{self.name}'"""
                        cursor.execute(query)
                        alumno = cursor.fetchall()

                        query = f"""SELECT * FROM registro WHERE codigo_alumo = '{alumno[0][1]}"""
                        cursor.execute(query)
                        registro_alumno = cursor.fetchall()

                        for registro in registro_alumno:
                            if self.txt_nrc.get() in registro:
                                messagebox.showinfo(message='Error: Ya agendaste esa materia')
                                error = 1
                                break

                        if error != 1:
                            query = f"""SELECT horario, COUNT(*) AS cantidad
                                        FROM (
                                            SELECT r.codigo_alumno, r.nrc_oferta, o.horario
                                            FROM registro r
                                            JOIN ofertas o ON r.nrc_oferta = o.nrc
                                            WHERE r.codigo_alumno = '{alumno[0][1]}'
                                        ) AS subconsulta
                                        GROUP BY horario;"""
                            
                            cursor.execute(query)
                            data = cursor.fetchall()

                            if not data:
                                query = f"INSERT INTO registro(codigo_alumno, nrc_oferta) VALUES('{alumno[0][1]}', '{self.txt_nrc.get()}')"
                            else:
                                messagebox.showinfo(message='Error: Incongruencias con los HORARIOS')
        else:
            messagebox.showinfo(message='Error: El campo NRC debe llenarse')

if __name__ == '__main__':
    root = tk.Tk()
    app = Registro(root, 'Prueba')
    root.mainloop()