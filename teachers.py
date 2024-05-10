import re
import tkinter as tk
from tkinter import messagebox, ttk
from connection_db import Connection

class Teachers:
    def __init__(self, root, name):
        self.root = root
        self.root.title("Maestros")

        self.root.geometry("600x400")
        self.root.resizable(height=False, width=False)

        self.name = name
        tk.Label(self.root, text=f'¡USUARIO ACTUAL: {self.name}!', font='Arial 10').place(x=30, y=30)

        tk.Label(self.root, text='Ingresa email del Maestro: ').place(x=60, y=60)
        self.txt_email_search = tk.Entry(self.root)
        self.txt_email_search.place(x=210, y=60)

        tk.Label(self.root, text='Área: ').place(x=20, y=260)
        self.txt_area = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_area.place(x=120, y=260)

        self.update_area_options()
        
        def update_state(event):
            query = "SELECT usuarios.email FROM usuarios LEFT JOIN maestros ON maestros.email = usuarios.email WHERE maestros.email IS NULL AND usuarios.perfil = 3;"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
                    self.txt_email['values'] = cursor.fetchall()

        tk.Label(self.root, text='Email: ').place(x=20, y=100)
        self.txt_email = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_email.place(x=120, y=100)
        query = "SELECT usuarios.email FROM usuarios LEFT JOIN maestros ON maestros.email = usuarios.email WHERE maestros.email IS NULLAND usuarios.perfil = 3;"
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


        tk.Label(self.root, text='Situacion: ').place(x=310, y=100)
        self.txt_situation = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_situation["values"] = ["ACTIVO", "INACTIVO"]
        self.txt_situation.place(x=410, y=100)
        

        tk.Label(self.root, text='Nivel de estudios: ').place(x=310, y=140)
        self.txt_education_level = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_education_level.place(x=410, y=140)
        query = "SELECT nombre FROM niveles_estudio"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
                self.txt_education_level['values'] = cursor.fetchall()
        
        #BUTTONS

        self.btn_search = tk.Button(self.root, text='BUSCAR', command=self.search_teachers)
        self.btn_search.place(x=350, y=55)

        self.btn_new = tk.Button(self.root, text='NUEVO', command=self.new_teachers)
        self.btn_new.place(x=50, y=310)

        self.btn_save = tk.Button(self.root, text='GUARDAR', command=self.save_teachers, state=tk.DISABLED)
        self.btn_save.place(x=120, y=310)

        self.btn_edit = tk.Button(self.root, text='EDITAR', command=self.edit_teachers, state=tk.DISABLED)
        self.btn_edit.place(x=205, y=310)

        self.btn_cancel = tk.Button(self.root, text='CANCELAR', command=self.principal_state, state=tk.DISABLED)
        self.btn_cancel.place(x=275, y=310)

        self.btn_delete = tk.Button(self.root, text='ELIMINAR', command=self.delete_teachers, state=tk.DISABLED)
        self.btn_delete.place(x=365, y=310) 

    def principal_state(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_name['state'] = tk.NORMAL
        self.txt_last['state'] = tk.NORMAL
        self.txt_mother_last['state'] = tk.NORMAL
        self.txt_situation['state'] = tk.NORMAL
        self.txt_education_level['state'] = tk.NORMAL

        self.txt_email.delete(0, tk.END)
        self.txt_email_search.delete(0, tk.END)
        self.txt_name.delete(0, tk.END)
        self.txt_last.delete(0, tk.END)
        self.txt_mother_last.delete(0, tk.END)
        self.txt_situation.delete(0, tk.END)
        self.txt_education_level.delete(0, tk.END)
        
        self.txt_email['state'] = tk.DISABLED
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_name['state'] = tk.DISABLED
        self.txt_last['state'] = tk.DISABLED
        self.txt_mother_last['state'] = tk.DISABLED
        self.txt_situation['state'] = tk.DISABLED
        self.txt_education_level['state'] = tk.DISABLED
        
        self.btn_new['state'] = tk.NORMAL
        self.btn_edit['state'] = tk.DISABLED
        self.btn_save['state'] = tk.DISABLED
        self.btn_cancel['state'] = tk.DISABLED
        self.btn_delete['state'] = tk.DISABLED
        self.btn_search['state'] = tk.NORMAL  

    def new_teachers(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_name['state'] = tk.NORMAL
        self.txt_last['state'] = tk.NORMAL
        self.txt_mother_last['state'] = tk.NORMAL
        self.txt_situation['state'] = tk.NORMAL
        self.txt_education_level['state'] = tk.NORMAL

        self.btn_new['state'] = tk. DISABLED
        self.btn_edit['state'] = tk.DISABLED
        self.btn_save['state'] = tk.NORMAL
        self.btn_cancel['state'] = tk.NORMAL
        self.btn_delete['state'] = tk.DISABLED
        self.btn_search['state'] = tk.NORMAL  

    def save_teachers(self):
        if(len(self.txt_email.get()) != 0 and len(self.txt_name.get()) != 0 and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0 and len(self.txt_education_level.get()) != 0 and len(self.txt_situation.get()) != 0):
                
            if(self.valid_email(self.txt_email.get())):
                if self.situacion(self.txt_situation.get()):
                    query = f"SELECT id_niveles FROM niveles_estudio WHERE nombre='{self.txt_education_level.get()}'"
                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query)
                            education_level = cursor.fetchall()
                            query2 = f"""INSERT INTO maestros(email, nombre, apellido_paterno, apellido_materno, nivel_estudios, situacion) 
                            VALUES ('{self.txt_email.get()}', '{self.txt_name.get()}', '{self.txt_last.get()}', '{self.txt_mother_last.get()}', {int(education_level[0][0])}, '{self.txt_situation.get()}')"""
                            cursor.execute(query2)
                            query3 = f"""UPDATE usuarios SET perfil = 3 WHERE usuarios.email = '{self.txt_email.get()}' """
                            cursor.execute(query3)
                            query4 = f"""DELETE FROM alumnos WHERE email = '{self.txt_email.get()}' """
                            cursor.execute(query4)
                    messagebox.showinfo(message='¡Maestro AGREGADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showinfo(message='Error: Situacion no reconocida')
                    self.principal_state()
            else:
                messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
        else:
            messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
            self.principal_state()

    def edit_teachers(self):
        if(len(self.txt_email.get()) != 0 and len(self.txt_name.get()) != 0 and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0 and len(self.txt_education_level.get()) != 0 and len(self.txt_situation.get()) != 0):
                
            if(self.valid_email(self.txt_email.get())):
                if self.situacion(self.txt_situation.get()):
                    query2 = f"SELECT id_niveles FROM niveles_estudio WHERE nombre='{self.txt_education_level.get()}'"
                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query2)
                            education_level = cursor.fetchall()
                            query2 = f"""UPDATE maestros SET email='{self.txt_email.get()}', nombre='{self.txt_name.get()}', apellido_paterno='{self.txt_last.get()}', 
                            apellido_materno='{self.txt_mother_last.get()}', nivel_estudios='{int(education_level[0][0])}', situacion='{self.txt_situation.get()}'
                            WHERE email='{self.txt_email_search.get()}'"""
                            cursor.execute(query2)
                            
                    messagebox.showinfo(message='¡Maestro MODIFICADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showinfo(message='Error: Situacion no reconocida')
                    self.principal_state()
            else:
                messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
        else:
            messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
            self.principal_state()


    def delete_teachers(self):
        table = 'maestros'
        query = f"UPDATE {table} SET situacion='INACTIVO' WHERE email='{self.txt_email.get()}'"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
        messagebox.showinfo(message='¡El usuario se ha dado de BAJA exitosamente!')
        self.principal_state() 

    def search_teachers(self):
        if(len(self.txt_email_search.get())!=0):
            query = f"SELECT * FROM usuarios WHERE email='{self.txt_email_search.get()}' AND perfil = 3"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
                    data = cursor.fetchall()
                    print(data)
                    if not data:
                        messagebox.showwarning(title='ALERTA',message='¡No se ha encontrado registro con ese ID!')
                        self.principal_state()
                    else:
                        query = f"SELECT * FROM maestros WHERE email='{data[0][0]}'"
                        cursor.execute(query)
                        maestro = cursor.fetchall()
                        query = f"SELECT nombre FROM niveles_estudio WHERE id_niveles={maestro[0][4]}"
                        cursor.execute(query)
                        education_level = cursor.fetchall()

                        self.txt_email['state'] = tk.NORMAL
                        self.txt_email_search['state'] = tk.NORMAL
                        self.txt_name['state'] = tk.NORMAL
                        self.txt_last['state'] = tk.NORMAL
                        self.txt_mother_last['state'] = tk.NORMAL
                        self.txt_situation['state'] = tk.NORMAL
                        self.txt_education_level['state'] = tk.NORMAL

                        self.txt_email.delete(0, tk.END)
                        self.txt_name.delete(0, tk.END)
                        self.txt_last.delete(0, tk.END)
                        self.txt_mother_last.delete(0, tk.END)
                        self.txt_situation.delete(0, tk.END)
                        self.txt_education_level.delete(0, tk.END)

                        self.txt_email.insert(0, data[0][0])
                        self.txt_name.insert(0, maestro[0][1])
                        self.txt_last.insert(0, maestro[0][2])
                        self.txt_mother_last.insert(0, maestro[0][3])
                        self.txt_situation.insert(0, maestro[0][5])
                        self.txt_education_level.insert(0, education_level[0][0])

                        self.btn_new['state'] = tk.DISABLED
                        self.btn_save['state'] = tk.DISABLED
                        self.btn_edit['state'] = tk.NORMAL
                        self.btn_delete['state'] = tk.NORMAL
                        self.btn_cancel['state'] = tk.NORMAL


    def valid_email(self, email):
        #example@mail.com
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, email):
            return True
        else:
            return False
        
    def situacion(self, texto):
        # Patrones para las situaciones
        patrones = ["ACTIVO", "INACTIVO"]

        # Buscar coincidencias exactas con los patrones
        for patron in patrones:
            if re.search(r'\b' + re.escape(patron) + r'\b', texto):
                return True
        return False

    def update_area_options(self):
            # Consultar todas las áreas disponibles desde la base de datos
            query = "SELECT nombre FROM areas"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
                    all_areas = cursor.fetchall()


if __name__ == "__main__":
    root = tk.Tk()
    app = Teachers(root, 'Prueba')
    root.mainloop()
        