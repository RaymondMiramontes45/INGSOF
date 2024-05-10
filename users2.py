import re
import tkinter as tk
from tkinter import messagebox, ttk
from connection_db import Connection

class User2:
    def __init__(self, root, name):
        self.root = root
        self.root.title("USUARIOS")

        self.root.geometry("600x300")
        self.root.resizable(height=False, width=False)

        self.name = name
        tk.Label(self.root, text=f'¡USUARIO ACTUAL: {self.name}!', font='Arial 10').place(x=30, y=30)

        tk.Label(self.root, text='Ingresa email de Usuario: ').place(x=60, y=60)
        self.txt_email_search = tk.Entry(self.root)
        self.txt_email_search.place(x=210, y=60)

        tk.Label(self.root, text='Perfil: ').place(x=20, y=100)
        self.txt_profile = ttk.Combobox(self.root, state=tk.DISABLED)
        self.txt_profile.place(x=120, y=100)
        query = "SELECT nombre FROM perfiles"
        with Connection.get_connection() as cnn:
            with cnn.cursor() as cursor:
                cursor.execute(query)
                self.txt_profile['values'] = cursor.fetchall()

        tk.Label(self.root, text='Email: ').place(x=20, y=140)
        self.txt_email = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_email.place(x=120, y=140)

        tk.Label(self.root, text='Contraseña: ').place(x=20, y=180)
        self.txt_password = tk.Entry(self.root, state=tk.DISABLED)
        self.txt_password.place(x=120, y=180)

        #BUTTONS

        self.btn_search = tk.Button(self.root, text='BUSCAR', command=self.search_user)
        self.btn_search.place(x=350, y=55)

        self.btn_new = tk.Button(self.root, text='NUEVO', command=self.new_user)
        self.btn_new.place(x=50, y=220)

        self.btn_save = tk.Button(self.root, text='GUARDAR', command=self.save_user, state=tk.DISABLED)
        self.btn_save.place(x=120, y=220)

        self.btn_edit = tk.Button(self.root, text='EDITAR', command=self.edit_user, state=tk.DISABLED)
        self.btn_edit.place(x=205, y=220)

        self.btn_cancel = tk.Button(self.root, text='CANCELAR', command=self.principal_state, state=tk.DISABLED)
        self.btn_cancel.place(x=275, y=220)

        self.btn_delete = tk.Button(self.root, text='ELIMINAR', command=self.delete_user, state=tk.DISABLED)
        self.btn_delete.place(x=365, y=220)   

    def principal_state(self):
        self.txt_email['state'] = tk.NORMAL
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_password['state'] = tk.NORMAL
        self.txt_profile['state'] = tk.NORMAL
        

        self.txt_email.delete(0, tk.END)
        self.txt_email_search.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)
        self.txt_profile.delete(0, tk.END)
        
        self.txt_email['state'] = tk.DISABLED
        self.txt_email_search['state'] = tk.NORMAL
        self.txt_password['state'] = tk.DISABLED
        self.txt_profile['state'] = tk.DISABLED

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
        if(len(self.txt_email.get()) != 0 and len(self.txt_password.get()) != 0 and len(self.txt_profile.get()) != 0):
            if(self.valid_email(self.txt_email.get())) and len(self.txt_password.get()) >= 10:
                query = f"SELECT id_perfiles FROM perfiles WHERE nombre='{self.txt_profile.get()}'"

                with Connection.get_connection() as cnn:
                    with cnn.cursor() as cursor:
                        cursor.execute(query)
                        data = cursor.fetchall()
                        query2 = f"""INSERT INTO usuarios(email, password, perfil) VALUES ('{self.txt_email.get()}', '{self.txt_password.get()}', {int(data[0][0])})"""
                        cursor.execute(query2)
                messagebox.showinfo(message='¡Administrador AGREGADO exitosamente!')
                self.principal_state()
            else:
                messagebox.showerror(message='Usuario o contraseña no validos: Formato Incorrecto')
        else:
            messagebox.showerror(message='ERORR: Todos los campos deben llenarse')
            self.principal_state()

    def edit_user(self):
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

    def delete_user(self):
        try:
            query = f"DELETE FROM usuarios WHERE email='{self.txt_email.get()}'"
            with Connection.get_connection() as cnn:
                with cnn.cursor() as cursor:
                    cursor.execute(query)
            messagebox.showinfo(message='¡El usuario se ha ELIMINADO exitosamente!')
            self.principal_state()
        except:
            messagebox.showinfo(message='El usuario tiene una relacion')
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
                        query2 = f"SELECT nombre FROM perfiles WHERE id_perfiles={data[0][2]}"
                        cursor.execute(query2)
                        profile = cursor.fetchone()[0]

                        self.txt_email['state'] = tk.NORMAL
                        self.txt_email_search['state'] = tk.NORMAL
                        self.txt_password['state'] = tk.NORMAL
                        self.txt_profile['state'] = tk.NORMAL

                        self.txt_email.delete(0, tk.END)
                        self.txt_password.delete(0, tk.END)
                        self.txt_profile.delete(0, tk.END)

                        self.txt_email.insert(0, data[0][0])
                        self.txt_password.insert(0, data[0][1])
                        self.txt_profile.insert(0, profile)

                        self.btn_new['state'] = tk.DISABLED
                        self.btn_edit['state'] = tk.NORMAL
                        self.btn_delete['state'] = tk.NORMAL
                        self.btn_save['state'] = tk.DISABLED
                        self.btn_cancel['state'] = tk.NORMAL
                        self.btn_search['state'] = tk.DISABLED
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
    app = User2(root, 'Prueba')
    root.mainloop()