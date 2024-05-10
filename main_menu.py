import tkinter as tk
from tkinter import messagebox
from users2 import User2
from classroom import Classroom
from carrers import Carrers
from courses import Course
from students import Students
from teachers import Teachers
from schedules import Schedule

class MainMenu:
    def __init__(self, root, name, profile):
        self.root = root
        self.root.title("CONTROL ESCOLAR")

        self.root.geometry("500x300")
        self.root.resizable(height=False, width=False)

        self.menu_bar = tk.Menu(self.root)
        
        self.root.config(menu = self.menu_bar)
        self.root.config(bg='white')

        self.menu_bar.add_command(label='Usuarios', command=self.open_users)
        self.menu_bar.add_command(label='Alumnos', command=self.open_students)
        self.menu_bar.add_command(label='Maestros', command=self.open_teachers)
        self.menu_bar.add_command(label='Cursos', command=self.open_courses)
        self.menu_bar.add_command(label='Carreras', command=self.open_carrers)
        self.menu_bar.add_command(label='Horarios', command=self.open_schedules)
        self.menu_bar.add_command(label='Salones', command=self.open_rooms)
        self.menu_bar.add_command(label='Oferta', command=self.open_offer)


        self.name = name
        self.profile = profile

        self.lbl_username = tk.Label(self.root, text=f'¡Bienvenido {self.name}!', font='Arial 20', bg='white')
        self.lbl_username.place(x=40, y=40)
        
        if profile == 1:
            pass
        elif profile == 2:
            self.menu_bar.entryconfig(index='Usuarios', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Maestros', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Carreras', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Horarios', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Salones', state=tk.DISABLED)
        elif profile == 3:
            self.menu_bar.entryconfig(index='Usuarios', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Alumnos', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Carreras', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Horarios', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Salones', state=tk.DISABLED)
            self.menu_bar.entryconfig(index='Oferta', state=tk.DISABLED)            
        else:
            messagebox.showerror(message='Hay un ERROR en el perfil')


    def open_users(self):
        root = tk.Tk()
        window_users = User2(root, self.name)

    def open_students(self):
        root = tk.Tk()
        window_users = Students(root, self.name)

    def open_teachers(self):
        root = tk.Tk()
        window_users = Teachers(root, self.name)

    def open_courses(self):
        root = tk.Tk()
        window_users = Course(root, self.name)

    def open_carrers(self):
        root = tk.Tk()
        window_users = Carrers(root, self.name)

    def open_schedules(self):
        root = tk.Tk()
        window_users = Schedule(root, self.name)

    def open_rooms(self):
        root = tk.Tk()
        window_users = Classroom(root, self.name)
        

    def open_offer():
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root, 'prueba', 1)
    root.mainloop()
