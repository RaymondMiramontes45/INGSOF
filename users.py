import re
import tkinter as tk
from tkinter import messagebox, ttk
from connection_db import Connection

class User:
    def __init__(self, root, name):
        self.root = root
        self.root.title("USUARIOS")

        self.root.geometry("600x500")
        self.root.resizable(height=False, width=False)

        self.name = name
        tk.Label(self.root, text=f'¡USUARIO ACTUAL: {self.name}!', font='Arial 10').place(x=30, y=30)

        tk.Label(self.root, text='Ingresa email de Usuario: ').place(x=60, y=60)
        self.txt_email_search = tk.Entry(self.root)
        self.txt_email_search.place(x=210, y=60)

        def update_state(event):
            if self.txt_profile.get() == 'Administrador':
                self.txt_name['state'] = tk.DISABLED
                self.txt_last['state'] = tk.DISABLED
                self.txt_mother_last['state'] = tk.DISABLED
                self.txt_situation['state'] = tk.DISABLED
                self.txt_education_level['state'] = tk.DISABLED
                self.txt_birth_date['state']  =tk.DISABLED
                self.txt_carrer['state'] = tk.DISABLED
                self.txt_admission_date['state'] = tk.DISABLED
                self.txt_code['state'] = tk.DISABLED
            elif self.txt_profile.get() == 'Alumno':
                self.txt_name['state'] = tk.NORMAL
                self.txt_last['state'] = tk.NORMAL
                self.txt_mother_last['state'] = tk.NORMAL
                self.txt_birth_date['state']  =tk.NORMAL
                self.txt_carrer['state'] = tk.NORMAL
                self.txt_admission_date['state'] = tk.NORMAL
                self.txt_situation['state'] = tk.NORMAL
                self.txt_code['state'] = tk.NORMAL
                self.txt_education_level['state'] = tk.DISABLED
            elif self.txt_profile.get() == 'Maestro':
                self.txt_name['state'] = tk.NORMAL
                self.txt_last['state'] = tk.NORMAL
                self.txt_mother_last['state'] = tk.NORMAL
                self.txt_situation['state'] = tk.NORMAL
                self.txt_education_level['state'] = tk.NORMAL
                self.txt_birth_date['state']  =tk.DISABLED
                self.txt_carrer['state'] = tk.DISABLED
                self.txt_admission_date['state'] = tk.DISABLED
                self.txt_code['state'] = tk.DISABLED

        tk.Label(self.root, text='Perfil: ').place(x=20, y=100)
        self.txt_profile = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_profile.place(x=120, y=100)
        query = "SELECT nombre FROM perfiles"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
                self.txt_profile['values'] = cursor.fetchall()

        self.txt_profile.bind("<<ComboboxSelected>>", update_state)

        tk.Label(self.root, text='Email: ').place(x=20, y=140)
        self.txt_email = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_email.place(x=120, y=140)

        tk.Label(self.root, text='Contraseña: ').place(x=20, y=180)
        self.txt_password = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_password.place(x=120, y=180)

        tk.Label(self.root, text='Nombre(s): ').place(x=20, y=220)
        self.txt_name = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_name.place(x=120, y=220)

        tk.Label(self.root, text='Apellido Paterno: ').place(x=20, y=260)
        self.txt_last = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_last.place(x=120, y=260)

        tk.Label(self.root, text='Apellido Materno (opcional): ').place(x=20, y=300)
        self.txt_mother_last = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_mother_last.place(x=180, y=300)

        tk.Label(self.root, text='Fecha de Nacimiento: ').place(x=310, y=100)
        self.txt_birth_date = tk.Entry(self.root, state=tk.DISABLED)
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
        self.txt_admission_date = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_admission_date.place(x=410, y=180)

        tk.Label(self.root, text='Situacion: ').place(x=310, y=220)
        self.txt_situation = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_situation.place(x=410, y=220)

        tk.Label(self.root, text='Codigo: ').place(x=310, y=260)
        self.txt_code = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_code.place(x=410, y=260)

        tk.Label(self.root, text='Nivel de estudios: ').place(x=310, y=300)
        self.txt_education_level = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_education_level.place(x=410, y=300)
        query = "SELECT nombre FROM niveles_estudio"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
                self.txt_education_level['values'] = cursor.fetchall()

        #BUTTONS

        self.btn_search = tk.Button(self.root, text='BUSCAR', command=self.search_user)
        self.btn_search.place(x=350, y=55)

        self.btn_new = tk.Button(self.root, text='NUEVO', command=self.new_user)
        self.btn_new.place(x=50, y=350)

        self.btn_save = tk.Button(self.root, text='GUARDAR', command=self.save_user, state=tk.DISABLED)
        self.btn_save.place(x=120, y=350)

        self.btn_edit = tk.Button(self.root, text='EDITAR', command=self.edit_user, state=tk.DISABLED)
        self.btn_edit.place(x=205, y=350)

        self.btn_cancel = tk.Button(self.root, text='CANCELAR', command=self.principal_state, state=tk.DISABLED)
        self.btn_cancel.place(x=275, y=350)

        self.btn_delete = tk.Button(self.root, text='ELIMINAR', command=self.delete_user, state=tk.DISABLED)
        self.btn_delete.place(x=365, y=350)   

    def principal_state(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_password['state'] = tk.NORMAL
        self.txt_profile['state'] = tk.NORMAL
        self.txt_name['state'] = tk.NORMAL
        self.txt_last['state'] = tk.NORMAL
        self.txt_mother_last['state'] = tk.NORMAL
        self.txt_situation['state'] = tk.NORMAL
        self.txt_education_level['state'] = tk.NORMAL
        self.txt_birth_date['state']  =tk.NORMAL
        self.txt_carrer['state'] = tk.NORMAL
        self.txt_admission_date['state'] = tk.NORMAL
        self.txt_code['state'] = tk.NORMAL

        self.txt_email.delete(0, tk.END)
        self.txt_email_search.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)
        self.txt_profile.delete(0, tk.END)
        self.txt_name.delete(0, tk.END)
        self.txt_last.delete(0, tk.END)
        self.txt_mother_last.delete(0, tk.END)
        self.txt_situation.delete(0, tk.END)
        self.txt_education_level.delete(0, tk.END)
        self.txt_birth_date.delete(0, tk.END)
        self.txt_carrer.delete(0, tk.END)
        self.txt_admission_date.delete(0, tk.END)
        self.txt_code.delete(0, tk.END)
        
        self.txt_email['state'] = tk.DISABLED
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_password['state'] = tk.DISABLED
        self.txt_profile['state'] = tk.DISABLED
        self.txt_name['state'] = tk.DISABLED
        self.txt_last['state'] = tk.DISABLED
        self.txt_mother_last['state'] = tk.DISABLED
        self.txt_situation['state'] = tk.DISABLED
        self.txt_education_level['state'] = tk.DISABLED
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

    def new_user(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_password['state'] = tk.NORMAL
        self.txt_profile['state'] = tk.NORMAL

        self.txt_email_search['state'] = tk.DISABLED

        self.btn_new['state'] = tk.DISABLED
        self.btn_edit['state'] = tk.DISABLED
        self.btn_delete['state'] = tk.DISABLED
        self.btn_save['state'] = tk.NORMAL
        self.btn_cancel['state'] = tk.NORMAL
        self.btn_search['state'] = tk.DISABLED

    def save_user(self):
        email = self.txt_email.get()
        
        # Check if the email already exists in the database
        query_check_email = f"SELECT COUNT(*) FROM usuarios WHERE email='{email}'"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query_check_email)
                result = cursor.fetchone()
                if result[0] > 0:
                    messagebox.showerror(message='ERROR: El email ya está registrado en la base de datos')
                    return

        # Continue with the rest of the save process
        if self.txt_profile.get() == 'Administrador':
            if len(email) != 0 and len(self.txt_password.get()) != 0 and len(self.txt_profile.get()) != 0:
                if self.valid_email(email):
                    query_get_profile_id = f"SELECT id_perfiles FROM perfiles WHERE nombre='{self.txt_profile.get()}'"
                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query_get_profile_id)
                            profile_id = cursor.fetchone()[0]
                            query_insert_admin = f"""INSERT INTO usuarios(email, password, perfil) 
                                                    VALUES ('{email}', '{self.txt_password.get()}', {profile_id})"""
                            cursor.execute(query_insert_admin)
                    messagebox.showinfo(message='¡Administrador AGREGADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showerror(message='Usuario o contraseña no válidos: Formato incorrecto')
            else:
                messagebox.showerror(message='ERROR: Todos los campos deben llenarse')
                self.principal_state()
        elif(self.txt_profile.get() == 'Maestro'):
            if(len(self.txt_email.get()) != 0 and len(self.txt_password.get()) != 0 and len(self.txt_profile.get()) != 0 and len(self.txt_name.get()) != 0
               and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0 and len(self.txt_education_level.get()) != 0 and len(self.txt_situation.get()) != 0):
                
                if(self.valid_email(self.txt_email.get())):
                    query = f"SELECT id_perfiles FROM perfiles WHERE nombre='{self.txt_profile.get()}'"
                    query2 = f"SELECT id_niveles FROM niveles_estudio WHERE nombre='{self.txt_education_level.get()}'"

                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query)
                            profile = cursor.fetchall()
                            cursor.execute(query2)
                            education_level = cursor.fetchall()
                            query = f"""INSERT INTO usuarios(email, password, perfil) VALUES ('{self.txt_email.get()}', '{self.txt_password.get()}', {int(profile[0][0])})"""
                            query2 = f"""INSERT INTO maestros(email, nombre, apellido_paterno, apellido_materno, nivel_estudios, situacion) 
                            VALUES ('{self.txt_email.get()}', '{self.txt_name.get()}', '{self.txt_last.get()}', '{self.txt_mother_last.get()}', {int(education_level[0][0])}, 
                            '{self.txt_situation.get()}')"""
                            cursor.execute(query)
                            cursor.execute(query2)
                    messagebox.showinfo(message='¡Maestro AGREGADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
            else:
                messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
                self.principal_state()

    def edit_user(self):
        if (self.txt_profile.get() == 'Administrador'):
            if(len(self.txt_email.get()) != 0 and len(self.txt_password.get()) != 0 and len(self.txt_profile.get()) != 0):
                if(self.valid_email(self.txt_email.get())):
                    query = f"SELECT id_perfiles FROM perfiles WHERE nombre='{self.txt_profile.get()}'"
                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query)
                            profile = cursor.fetchall()
                            query2 = f"""UPDATE usuarios SET email='{self.txt_email.get()}', password='{self.txt_password.get()}',
                                perfil={int(profile[0][0])} WHERE email='{self.txt_email_search.get()}'"""
                            cursor.execute(query2)
                    messagebox.showinfo(message='¡Administrador MODIFICADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
            else:
                messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
                self.principal_state()
        elif(self.txt_profile.get() == 'Alumno'):
            if(len(self.txt_email.get()) != 0 and len(self.txt_password.get()) != 0 and len(self.txt_profile.get()) != 0 and len(self.txt_name.get()) != 0
               and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0 and len(self.txt_birth_date.get()) != 0 and len(self.txt_carrer.get()) != 0
               and len(self.txt_admission_date.get()) != 0 and len(self.txt_situation.get()) != 0 and len(self.txt_code.get()) != 0):
        
                if(self.valid_email(self.txt_email.get())):
                    query = f"SELECT id_perfiles FROM perfiles WHERE nombre='{self.txt_profile.get()}'"
                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query)
                            profile = cursor.fetchall()
                            query = f"""UPDATE usuarios SET email='{self.txt_email.get()}', password='{self.txt_password.get()}',
                                perfil={int(profile[0][0])} WHERE email='{self.txt_email_search.get()}'"""
                            query2 = f"""UPDATE alumnos SET email='{self.txt_email.get()}', nombre='{self.txt_name.get()}', apellido_paterno='{self.txt_last.get()}', 
                            apellido_materno='{self.txt_mother_last.get()}', fecha_nacimiento='{self.txt_birth_date.get()}', carrera='{self.txt_carrer.get()}', 
                            fecha_ingreso='{self.txt_admission_date.get()}', situacion='{self.txt_situation.get()}', codigo='{self.txt_code.get()}'
                            WHERE email='{self.txt_email_search.get()}'"""
                            cursor.execute(query)
                            cursor.execute(query2)
                    messagebox.showinfo(message='¡Alumno MODIFICADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
            else:
                messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
                self.principal_state()
        elif(self.txt_profile.get() == 'Maestro'):
            if(len(self.txt_email.get()) != 0 and len(self.txt_password.get()) != 0 and len(self.txt_profile.get()) != 0 and len(self.txt_name.get()) != 0
               and len(self.txt_last.get()) != 0 and len(self.txt_mother_last.get()) != 0 and len(self.txt_education_level.get()) != 0 and len(self.txt_situation.get()) != 0):
                
                if(self.valid_email(self.txt_email.get())):
                    query = f"SELECT id_perfiles FROM perfiles WHERE nombre='{self.txt_profile.get()}'"
                    query2 = f"SELECT id_niveles FROM niveles_estudio WHERE nombre='{self.txt_education_level.get()}'"
                    with Connection.get_connection() as cnn:
                        with cnn.cursor() as cursor:
                            cursor.execute(query)
                            profile = cursor.fetchall()
                            query = f"""UPDATE usuarios SET email='{self.txt_email.get()}', password='{self.txt_password.get()}',
                                perfil={int(profile[0][0])} WHERE email='{self.txt_email_search.get()}'"""
                            query2 = f"""UPDATE maestros SET email='{self.txt_email.get()}', nombre='{self.txt_name.get()}', apellido_paterno='{self.txt_last.get()}', 
                            apellido_materno='{self.txt_mother_last.get()}', nivel_estudios='{self.txt_education_level.get()}', situacion='{self.txt_situation.get()}'
                            WHERE email='{self.txt_email_search.get()}'"""
                            cursor.execute(query)
                    messagebox.showinfo(message='¡Maestro MODIFICADO exitosamente!')
                    self.principal_state()
                else:
                    messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
            else:
                messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
                self.principal_state()

    def delete_user(self):
        if(self.txt_profile.get() == 'Administrador'):
            query = f"DELETE FROM usuarios WHERE email='{self.txt_email.get()}'"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
            messagebox.showinfo(message='¡El usuario se ha ELIMINADO exitosamente!')
            self.principal_state()
        else:
            if(self.txt_profile.get() == 'Alumno'):
                table = 'alumnos'
            elif(self.txt_profile.get() == 'Maestro'):
                table = 'maestros'
            query = f"UPDATE {table} SET situacion='INACTIVO' WHERE email='{self.txt_email.get()}'"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
            messagebox.showinfo(message='¡El usuario se ha dado de BAJA exitosamente!')
            self.principal_state()                

    def search_user(self):
        if(len(self.txt_email_search.get())!=0):
            query = f"SELECT * FROM usuarios WHERE email='{self.txt_email_search.get()}'"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
                    data = cursor.fetchall()
                    print(data)
                    if not data:
                        messagebox.showwarning(title='ALERTA',message='¡No se ha encontrado registro con ese ID!')
                        self.principal_state()
                    else:
                        if(data[0][2] == 1):
                            query = f"SELECT nombre FROM perfiles WHERE id_perfiles={data[0][2]}"
                            cursor.execute(query)
                            profile = cursor.fetchall()

                            self.txt_email['state'] = tk.NORMAL
                            self.txt_email_search['state'] = tk.NORMAL
                            self.txt_password['state'] = tk.NORMAL
                            self.txt_profile['state'] = tk.NORMAL

                            self.txt_email.delete(0, tk.END)
                            self.txt_password.delete(0, tk.END)
                            self.txt_profile.delete(0, tk.END)
                            self.txt_name.delete(0, tk.END)
                            self.txt_last.delete(0, tk.END)
                            self.txt_mother_last.delete(0, tk.END)
                            self.txt_situation.delete(0, tk.END)
                            self.txt_birth_date.delete(0, tk.END)
                            self.txt_carrer.delete(0, tk.END)
                            self.txt_admission_date.delete(0, tk.END)
                            self.txt_code.delete(0, tk.END)
                            self.txt_education_level.delete(0, tk.END)

                            self.txt_email.insert(0, data[0][0])
                            self.txt_password.insert(0, data[0][1])
                            self.txt_profile.insert(0, profile[0][0])

                            self.txt_name['state'] = tk.DISABLED
                            self.txt_last['state'] = tk.DISABLED
                            self.txt_mother_last['state'] = tk.DISABLED
                            self.txt_birth_date['state']  =tk.DISABLED
                            self.txt_carrer['state'] = tk.DISABLED
                            self.txt_admission_date['state'] = tk.DISABLED
                            self.txt_situation['state'] = tk.DISABLED
                            self.txt_code['state'] = tk.DISABLED
                            self.txt_education_level['state'] = tk.DISABLED

                        elif(data[0][2] == 2):
                            query = f"SELECT * FROM alumnos WHERE email='{data[0][0]}'"
                            cursor.execute(query)
                            alumno = cursor.fetchall()
                            query = f"SELECT nombre FROM perfiles WHERE id_perfiles={data[0][2]}"
                            cursor.execute(query)
                            profile = cursor.fetchall()

                            self.txt_email['state'] = tk.NORMAL
                            self.txt_email_search['state'] = tk.NORMAL
                            self.txt_password['state'] = tk.NORMAL
                            self.txt_profile['state'] = tk.NORMAL
                            self.txt_name['state'] = tk.NORMAL
                            self.txt_last['state'] = tk.NORMAL
                            self.txt_mother_last['state'] = tk.NORMAL
                            self.txt_birth_date['state']  =tk.NORMAL
                            self.txt_carrer['state'] = tk.NORMAL
                            self.txt_admission_date['state'] = tk.NORMAL
                            self.txt_situation['state'] = tk.NORMAL
                            self.txt_code['state'] = tk.NORMAL
                            self.txt_education_level.delete(0, tk.END)

                            self.txt_email.delete(0, tk.END)
                            self.txt_password.delete(0, tk.END)
                            self.txt_profile.delete(0, tk.END)
                            self.txt_name.delete(0, tk.END)
                            self.txt_last.delete(0, tk.END)
                            self.txt_mother_last.delete(0, tk.END)
                            self.txt_situation.delete(0, tk.END)
                            self.txt_birth_date.delete(0, tk.END)
                            self.txt_carrer.delete(0, tk.END)
                            self.txt_admission_date.delete(0, tk.END)
                            self.txt_code.delete(0, tk.END)

                            self.txt_email.insert(0, data[0][0])
                            self.txt_password.insert(0, data[0][1])
                            self.txt_profile.insert(0, profile[0][0])
                            self.txt_name.insert(0, alumno[0][1])
                            self.txt_last.insert(0, alumno[0][2])
                            self.txt_mother_last.insert(0, alumno[0][3])
                            self.txt_situation.insert(0, alumno[0][7])
                            self.txt_birth_date.insert(0, alumno[0][4])
                            self.txt_carrer.insert(0, alumno[0][5])
                            self.txt_admission_date.insert(0, alumno[0][6])
                            self.txt_code.insert(0, alumno[0][8])

                            self.txt_education_level['state'] = tk.DISABLED

                        elif(data[0][2] == 3):
                            query = f"SELECT * FROM maestros WHERE email='{data[0][0]}'"
                            cursor.execute(query)
                            maestro = cursor.fetchall()
                            query = f"SELECT nombre FROM perfiles WHERE id_perfiles={data[0][2]}"
                            cursor.execute(query)
                            profile = cursor.fetchall()
                            query = f"SELECT nombre FROM niveles_estudio WHERE id_niveles={maestro[0][4]}"
                            cursor.execute(query)
                            education_level = cursor.fetchall()

                            self.txt_email['state'] = tk.NORMAL
                            self.txt_email_search['state'] = tk.NORMAL
                            self.txt_password['state'] = tk.NORMAL
                            self.txt_profile['state'] = tk.NORMAL
                            self.txt_name['state'] = tk.NORMAL
                            self.txt_last['state'] = tk.NORMAL
                            self.txt_mother_last['state'] = tk.NORMAL
                            self.txt_birth_date['state']  =tk.NORMAL
                            self.txt_carrer['state'] = tk.NORMAL
                            self.txt_admission_date['state'] = tk.NORMAL
                            self.txt_situation['state'] = tk.NORMAL
                            self.txt_code['state'] = tk.NORMAL
                            self.txt_education_level['state'] = tk.NORMAL

                            self.txt_email.delete(0, tk.END)
                            self.txt_password.delete(0, tk.END)
                            self.txt_profile.delete(0, tk.END)
                            self.txt_name.delete(0, tk.END)
                            self.txt_last.delete(0, tk.END)
                            self.txt_mother_last.delete(0, tk.END)
                            self.txt_situation.delete(0, tk.END)
                            self.txt_birth_date.delete(0, tk.END)
                            self.txt_carrer.delete(0, tk.END)
                            self.txt_admission_date.delete(0, tk.END)
                            self.txt_code.delete(0, tk.END)
                            self.txt_education_level.delete(0, tk.END)

                            self.txt_email.insert(0, data[0][0])
                            self.txt_password.insert(0, data[0][1])
                            self.txt_profile.insert(0, profile[0][0])
                            self.txt_name.insert(0, maestro[0][1])
                            self.txt_last.insert(0, maestro[0][2])
                            self.txt_mother_last.insert(0, maestro[0][3])
                            self.txt_situation.insert(0, maestro[0][5])
                            self.txt_education_level.insert(0, education_level[0][0])

                            self.txt_code['state'] = tk.DISABLED
                            self.txt_birth_date['state']  =tk.DISABLED
                            self.txt_carrer['state'] = tk.DISABLED
                            self.txt_admission_date['state'] = tk.DISABLED

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

if __name__ == "__main__":
    root = tk.Tk()
    app = User(root, 'Prueba')
    root.mainloop()
        