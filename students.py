import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from connection_db import Connection
from tkcalendar import DateEntry


class Students:
    def __init__(self, root, name):
        self.root = root
        self.root.title("Alumnos")

        self.root.geometry("600x400")
        self.root.resizable(height=False, width=False)

        self.name = name
        tk.Label(self.root, text=f'¡USUARIO ACTUAL: {self.name}!', font='Arial 10').place(x=30, y=30)

        tk.Label(self.root, text='Ingresa email de Alumno: ').place(x=60, y=60)
        self.txt_email_search = tk.Entry(self.root)
        self.txt_email_search.place(x=210, y=60)
        
        def update_state(event):
            query = "SELECT usuarios.email FROM usuarios LEFT JOIN alumnos ON alumnos.email = usuarios.email WHERE alumnos.email IS NULL ;"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
                    self.txt_email['values'] = cursor.fetchall()

        tk.Label(self.root, text='Email: ').place(x=20, y=100)
        self.txt_email = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_email.place(x=120, y=100)
        query = "SELECT usuarios.email FROM usuarios LEFT JOIN alumnos ON alumnos.email = usuarios.email WHERE alumnos.email IS NULL AND usuarios.perfil = 2;"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
                self.txt_email['values'] = cursor.fetchall()
        self.txt_email.bind("<<ComboboxSelected>>", update_state)

        tk.Label(self.root, text='Nombre(s): ').place(x=20, y=140)
        self.txt_name = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_name.place(x=120, y=140)

        tk.Label(self.root, text='Apellido Paterno: ').place(x=20, y=180)
        self.txt_last = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_last.place(x=120, y=180)

        tk.Label(self.root, text='Apellido Materno (opcional): ').place(x=20, y=220)
        self.txt_mother_last = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_mother_last.place(x=180, y=220)

        tk.Label(self.root, text='Fecha de Nacimiento: ').place(x=310, y=100)
        self.txt_birth_date = DateEntry(self.root, state=tk.DISABLED, date_pattern='yyyy-mm-dd')
        self.txt_birth_date.place(x=440, y=100)

        tk.Label(self.root, text='Carrera: ').place(x=310, y=140)
        self.txt_carrer = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_carrer.place(x=410, y=140)
        query = "SELECT clave FROM carreras"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
                self.txt_carrer['values'] = cursor.fetchall()

        tk.Label(self.root, text='Fecha de Ingreso: ').place(x=310, y=180)
        self.txt_admission_date = DateEntry(self.root, state=tk.DISABLED, date_pattern='yyyy-mm-dd')
        self.txt_admission_date.place(x=410, y=180)

        tk.Label(self.root, text='Situacion: ').place(x=310, y=220)
        self.txt_situation = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_situation["values"] = ["ACTIVO", "INACTIVO"]
        self.txt_situation.place(x=410, y=220)

        tk.Label(self.root, text='Codigo: ').place(x=20, y=260)
        self.txt_code = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_code.place(x=120, y=260)

        #BUTTONS

        self.btn_search = tk.Button(self.root, text='BUSCAR', command=self.search_student)
        self.btn_search.place(x=350, y=55)

        self.btn_new = tk.Button(self.root, text='NUEVO', command=self.new_student)
        self.btn_new.place(x=50, y=310)

        self.btn_save = tk.Button(self.root, text='GUARDAR', command=self.save_student, state=tk.DISABLED)
        self.btn_save.place(x=120, y=310)

        self.btn_edit = tk.Button(self.root, text='EDITAR', command=self.edit_student, state=tk.DISABLED)
        self.btn_edit.place(x=205, y=310)

        self.btn_cancel = tk.Button(self.root, text='CANCELAR', command=self.principal_state, state=tk.DISABLED)
        self.btn_cancel.place(x=275, y=310)

        self.btn_delete = tk.Button(self.root, text='ELIMINAR', command=self.delete_student, state=tk.DISABLED)
        self.btn_delete.place(x=365, y=310)   

    def principal_state(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_name['state'] = tk.NORMAL
        self.txt_last['state'] = tk.NORMAL
        self.txt_mother_last['state'] = tk.NORMAL
        self.txt_situation['state'] = tk.NORMAL
        self.txt_birth_date['state']  =tk.NORMAL
        self.txt_carrer['state'] = tk.NORMAL
        self.txt_admission_date['state'] = tk.NORMAL
        self.txt_code['state'] = tk.NORMAL

        self.txt_email.delete(0, tk.END)
        self.txt_email_search.delete(0, tk.END)
        self.txt_name.delete(0, tk.END)
        self.txt_last.delete(0, tk.END)
        self.txt_mother_last.delete(0, tk.END)
        self.txt_situation.delete(0, tk.END)
        self.txt_birth_date.delete(0, tk.END)
        self.txt_carrer.delete(0, tk.END)
        self.txt_admission_date.delete(0, tk.END)
        self.txt_code.delete(0, tk.END)
        
        self.txt_email['state'] = tk.DISABLED
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_name['state'] = tk.DISABLED
        self.txt_last['state'] = tk.DISABLED
        self.txt_mother_last['state'] = tk.DISABLED
        self.txt_situation['state'] = tk.DISABLED
        self.txt_birth_date['state']  =tk.DISABLED
        self.txt_carrer['state'] = tk.DISABLED
        self.txt_admission_date['state'] = tk.DISABLED
        self.txt_code['state'] = tk.DISABLED

        self.btn_new['state'] = tk.NORMAL
        self.btn_edit['state'] = tk.DISABLED
        self.btn_save['state'] = tk.DISABLED
        self.btn_cancel['state'] = tk.DISABLED
        self.btn_delete['state'] = tk.DISABLED
        self.btn_search['state'] = tk.NORMAL        

    def new_student(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_email_search['state'] = tk.DISABLED

        self.txt_name['state'] = tk.NORMAL
        self.txt_last['state'] = tk.NORMAL
        self.txt_mother_last['state'] = tk.NORMAL
        self.txt_birth_date['state']  =tk.NORMAL
        self.txt_carrer['state'] = tk.NORMAL
        self.txt_admission_date['state'] = tk.NORMAL
        self.txt_situation['state'] = tk.NORMAL
        self.txt_code['state'] = tk.NORMAL

        hora_actual = datetime.now()
        hora_formateada = hora_actual.strftime("%Y-%m-%d")
        self.txt_admission_date.insert(0, hora_formateada)
        self.txt_birth_date.insert(0, '2000-01-01')

        self.btn_new['state'] = tk.DISABLED
        self.btn_edit['state'] = tk.DISABLED
        self.btn_delete['state'] = tk.DISABLED
        self.btn_save['state'] = tk.NORMAL
        self.btn_cancel['state'] = tk.NORMAL
        self.btn_search['state'] = tk.DISABLED

    def save_student(self):
        if (len(self.txt_email.get()) != 0 and len(self.txt_name.get()) != 0
            and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0
            and len(self.txt_birth_date.get()) != 0 and len(self.txt_carrer.get()) != 0
            and len(self.txt_admission_date.get()) != 0 and len(self.txt_situation.get()) != 0
            and len(self.txt_code.get()) != 0):

            # Validate email format
            if self.valid_email(self.txt_email.get()):
                # Validate date formats
                if self.validar_fecha(self.txt_admission_date.get()) and self.validar_fecha(self.txt_birth_date.get()):
                    # Validate situation
                    if self.situacion(self.txt_situation.get()):
                        # Check if the code already exists
                        with Connection.get_connection() as cnn:
                            with cnn.cursor() as cursor:
                                query_code = f"SELECT COUNT(*) FROM alumnos WHERE codigo = '{self.txt_code.get()}'"
                                cursor.execute(query_code)
                                code_count = cursor.fetchone()[0]
                                if code_count > 0:
                                    messagebox.showerror(message='Error: El código ya está en uso')
                                else:
                                    # Insert new student
                                    query_insert = f"""INSERT INTO alumnos(email, nombre, apellido_paterno, apellido_materno, 
                                                    fecha_nacimiento, carrera, fecha_ingreso, situacion, codigo) 
                                                    VALUES ('{self.txt_email.get()}', '{self.txt_name.get()}', 
                                                    '{self.txt_last.get()}', '{self.txt_mother_last.get()}', 
                                                    '{self.txt_birth_date.get()}', '{self.txt_carrer.get()}', 
                                                    '{self.txt_admission_date.get()}', '{self.txt_situation.get()}', 
                                                    '{self.txt_code.get()}')"""
                                    cursor.execute(query_insert)
                                    query_update = f"""UPDATE usuarios SET perfil = 2 WHERE email = '{self.txt_email.get()}' """
                                    cursor.execute(query_update)
                                    query_delete = f"""DELETE FROM maestros WHERE email = '{self.txt_email.get()}' """
                                    cursor.execute(query_delete)
                                    messagebox.showinfo(message='¡Alumno agregado exitosamente!')
                                    self.principal_state()
                    else:
                        messagebox.showinfo(message='Error: Situacion no reconocida')
                        self.principal_state()
                else:
                    messagebox.showinfo(message='Error: Formato de la fecha incorrecta')
                    self.principal_state()
            else:
                messagebox.showerror(message='Usuario o contraseña no válidos: Formato incorrecto')
        else:
            messagebox.showerror(message='ERROR: Todos los campos deben llenarse')
            self.principal_state()
        

    def edit_student(self):
        if(len(self.txt_email.get()) != 0 and  len(self.txt_name.get()) != 0
            and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0 and len(self.txt_birth_date.get()) != 0 and len(self.txt_carrer.get()) != 0
            and len(self.txt_admission_date.get()) != 0 and len(self.txt_situation.get()) != 0 and len(self.txt_code.get()) != 0):

            if(self.valid_email(self.txt_email.get())):
                if self.validar_fecha(self.txt_admission_date.get()) and self.validar_fecha(self.txt_birth_date.get()):
                    if self.situacion(self.txt_situation.get()):
                        with Connection.get_connection() as cnn:
                            with cnn.cursor() as cursor:
                                query2 = f"""UPDATE alumnos SET email='{self.txt_email.get()}', nombre='{self.txt_name.get()}', apellido_paterno='{self.txt_last.get()}', 
                                apellido_materno='{self.txt_mother_last.get()}', fecha_nacimiento='{self.txt_birth_date.get()}', carrera='{self.txt_carrer.get()}', 
                                fecha_ingreso='{self.txt_admission_date.get()}', situacion='{self.txt_situation.get()}', codigo='{self.txt_code.get()}'
                                WHERE email='{self.txt_email_search.get()}'"""
                                cursor.execute(query2)
                                
                        messagebox.showinfo(message='¡Alumno MODIFICADO exitosamente!')
                        self.principal_state()
                    else:
                        messagebox.showinfo(message='Error: Situacion no reconocida')
                        self.principal_state()
                else:
                    messagebox.showinfo(message='Error: Formato de la fecha incorrecta')
                    self.principal_state()
            else:
                messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
        else:
            messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
            self.principal_state()

    def delete_student(self):
        table = 'alumnos'
        query = f"UPDATE {table} SET situacion='INACTIVO' WHERE email='{self.txt_email.get()}'"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
        messagebox.showinfo(message='¡El usuario se ha dado de BAJA exitosamente!')
        self.principal_state() 
        

    def search_student(self):
        if(len(self.txt_email_search.get())!=0):
            query = f"SELECT * FROM usuarios WHERE email='{self.txt_email_search.get()}' AND perfil = 2"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
                    data = cursor.fetchall()
                    print(data)
                    if not data:
                        messagebox.showwarning(title='ALERTA',message='¡No se ha encontrado registro con ese ID!')
                        self.principal_state()
                    else:
                        query = f"SELECT * FROM alumnos WHERE email='{data[0][0]}'"
                        cursor.execute(query)
                        alumno = cursor.fetchall()
                        query = f"SELECT nombre FROM perfiles WHERE id_perfiles={data[0][2]}"

                        self.txt_email['state'] = tk.NORMAL
                        self.txt_email_search['state'] = tk.NORMAL
                        
                        self.txt_name['state'] = tk.NORMAL
                        self.txt_last['state'] = tk.NORMAL
                        self.txt_mother_last['state'] = tk.NORMAL
                        self.txt_birth_date['state']  =tk.NORMAL
                        self.txt_carrer['state'] = tk.NORMAL
                        self.txt_admission_date['state'] = tk.NORMAL
                        self.txt_situation['state'] = tk.NORMAL
                        self.txt_code['state'] = tk.NORMAL

                        self.txt_email.delete(0, tk.END)
                        self.txt_name.delete(0, tk.END)
                        self.txt_last.delete(0, tk.END)
                        self.txt_mother_last.delete(0, tk.END)
                        self.txt_situation.delete(0, tk.END)
                        self.txt_birth_date.delete(0, tk.END)
                        self.txt_carrer.delete(0, tk.END)
                        self.txt_admission_date.delete(0, tk.END)
                        self.txt_code.delete(0, tk.END)

                        self.txt_email.insert(0, data[0][0])
                        self.txt_name.insert(0, alumno[0][1])
                        self.txt_last.insert(0, alumno[0][2])
                        self.txt_mother_last.insert(0, alumno[0][3])
                        self.txt_situation.insert(0, alumno[0][7])
                        self.txt_birth_date.insert(0, alumno[0][4])
                        self.txt_carrer.insert(0, alumno[0][5])
                        self.txt_admission_date.insert(0, alumno[0][6])
                        self.txt_code.insert(0, alumno[0][8])

                        self.btn_new['state'] = tk.DISABLED
                        self.btn_save['state'] = tk.DISABLED
                        self.btn_edit['state'] = tk.NORMAL
                        self.btn_delete['state'] = tk.NORMAL
                        self.btn_cancel['state'] = tk.NORMAL
        else:
            messagebox.showerror(message='ERROR: Llena el campo ID Cliente a buscar')
            self.principal_state()

    def valid_email(self, email):
        #example@mail.com
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, email):
            return True
        else:
            return False
    
    def validar_fecha(self, fecha):
        try:
            # Intenta convertir la cadena de fecha en un objeto datetime
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
            # Comprueba si el año es mayor a 1990
            if fecha_dt.year > 1990 and fecha_dt.year < 2025:
                return True
            else:
                return False
        except ValueError:
            # Si hay un error al convertir la fecha, retorna False
            return False
        
    def situacion(self, texto):
        # Patrones para las situaciones
        patrones = ["ACTIVO", "INACTIVO"]

        # Buscar coincidencias exactas con los patrones
        for patron in patrones:
            if re.search(r'\b' + re.escape(patron) + r'\b', texto):
                return True
        return False
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Students(root, 'Prueba')
    root.mainloop()
        