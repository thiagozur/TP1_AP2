import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from funciones import calc_m, calc_b, calc_fc, calc_fd, save_xlsx
from fisico_teorico import fisico_teorico
from cremer import cremer
from sharp import sharp
from davy import davy
from iso import iso

#definición de la clase 'Material'
class Material:
    def __init__(self, tipo, densidad, myoung, fperd, mpoisson, dimensiones):
        self.tipo = tipo
        self.rho = int(densidad)
        self.e = float(myoung)
        self.eta = float(fperd)
        self.sigma = float(mpoisson)
        self.dim = dimensiones
        self.m = calc_m(self.rho, self.dim)
        self.b = calc_b(self.e, self.sigma, self.dim)

#definición del array de frecuencias centrales y de los ticks para el gráfico
frecuencias = np.array([
    20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
    1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000
])

#definición de constantes
c = 343
rho0 = 1.18

#lectura del archivo de materiales y definición del material y sus dimensiones
db = pd.read_excel('./materiales.xlsx')
mats = db['Material'].tolist()

#interfaz gráfica
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class AppR(ctk.CTk):
    def __init__(self):
        super().__init__()

        #creación y posicionamiento de componentes
        self.title('Calculadora de Aislamiento Acústico - Paneles Simples')
        self.geometry("1200x700")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 3)
        self.grid_rowconfigure(0, weight = 1)

        self.sidebar = ctk.CTkFrame(self, width = 300, corner_radius = 10)
        self.sidebar.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = 'nsew')

        self.titulo_inputs = ctk.CTkLabel(self.sidebar, text = 'Parámetros del panel', font = ctk.CTkFont(size = 18, weight = 'bold'))
        self.titulo_inputs.pack(padx = 20, pady = 20)

        #desplegable materiales
        self.label_ind = ctk.CTkLabel(self.sidebar, text = 'Seleccionar Material:')
        self.label_ind.pack(padx = 20, pady = 5, anchor = 'w')
        self.menu_ind = ctk.CTkOptionMenu(
            self.sidebar, 
            values = mats, 
            command = self.cambiar_material
        )
        self.menu_ind.pack(padx = 20, pady = 5, fill = 'x')
        self.menu_ind.set(mats[9])

        #dimensiones
        self.label_ancho = ctk.CTkLabel(self.sidebar, text = 'Ancho (m):')
        self.label_ancho.pack(padx = 20, pady = 5, anchor = 'w')
        self.input_ancho = ctk.CTkEntry(self.sidebar, placeholder_text = '7')
        self.input_ancho.insert(0, '7')
        self.input_ancho.pack(padx = 20, pady = 5, fill = 'x')

        self.label_alto = ctk.CTkLabel(self.sidebar, text = 'Alto (m):')
        self.label_alto.pack(padx = 20, pady = 5, anchor = 'w')
        self.input_alto = ctk.CTkEntry(self.sidebar, placeholder_text = '3')
        self.input_alto.insert(0, '3')
        self.input_alto.pack(padx = 20, pady = 5, fill = 'x')

        self.label_espesor = ctk.CTkLabel(self.sidebar, text = 'Espesor (m):')
        self.label_espesor.pack(padx = 20, pady = 5, anchor = 'w')
        self.input_espesor = ctk.CTkEntry(self.sidebar, placeholder_text = '0.02')
        self.input_espesor.insert(0, '0.02')
        self.input_espesor.pack(padx = 20, pady = 5, fill = 'x')
        
        #botón
        self.btn_calcular = ctk.CTkButton(self.sidebar, text = 'Calcular y graficar', command = self.calcular)
        self.btn_calcular.pack(padx = 20, pady = 30, fill = 'x')

        #gráfico
        self.frame_grafico = ctk.CTkFrame(self, corner_radius = 10)
        self.frame_grafico.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = 'nsew')

        self.fig, self.ax = plt.subplots(figsize = (6, 5), dpi = 100)
        self.configurar_ejes_grafico()

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_grafico)
        self.canvas.get_tk_widget().pack(padx=20, pady=20, fill='both', expand=True)

        #variable índice de material
        self.ind_sel = 9


    def cambiar_material(self, mat):
        self.ind_sel = mats.index(mat)
    
    def configurar_ejes_grafico(self, material = None):
        self.ax.clear()
        self.ax.set_xscale('log')
        self.ax.set_xlabel('Frecuencia [Hz]')
        self.ax.set_ylabel('R [dB]')

        if material != None:
            self.ax.set_title(f'R para un panel simple de {material.tipo.lower()} de {material.dim[0]}m x {material.dim[1]}m x {str(material.dim[2]).replace(".", ",")}m', fontsize = '16')
        else:
            self.ax.set_title('')

        self.ax.set_xlim(20, 20000)
        self.ax.set_ylim(0, 130)
        self.ax.grid(True, which = 'both', ls = '--', alpha = 0.5)
        self.ax.set_xticks(frecuencias)
        self.ax.set_xticklabels([str(int(f)) if float(f).is_integer() else float(f) for f in frecuencias], rotation = 45)

    def calcular(self):
        try:
            dim = (float(self.input_alto.get()), float(self.input_ancho.get()), float(self.input_espesor.get()))
            ind = self.ind_sel

            #instanciación de un objeto de la clase 'Material'
            material = Material(db.iloc[ind, 1], db.iloc[ind, 2], db.iloc[ind, 3], db.iloc[ind, 4], db.iloc[ind, 5], dim)

            #cálculo de la frecuencia crítica y de la frecuencia de densidad
            fc = calc_fc(material.e, material.rho, material.dim, c)
            fd = calc_fd(material.m, material.e, material.b, material.rho)

            #cálculo de r con los modelos
            r_fisico_teorico = fisico_teorico(frecuencias, material.m, material.eta, fc, fd, rho0, c)
            r_iso = iso(frecuencias, material.m, material.eta, material.dim, fc, rho0, c)
            r_cremer = cremer(frecuencias, material.m, material.eta, fc, fd)
            r_sharp = sharp(frecuencias, material.m, material.eta, fc, rho0, c)
            r_davy = davy(frecuencias, material.rho, material.e, material.sigma, material.dim, material.m, material.eta, fc, rho0, c)

            #creación del array de resultados
            data_R = [r_fisico_teorico, r_iso, r_cremer, r_sharp, r_davy]
            modelos = ['Físico-teórico', 'ISO 12354-1', 'Cremer', 'Sharp', 'Davy']

            res = pd.DataFrame(
                data = data_R,
                index = modelos,
                columns = frecuencias
            )

            #guardado en formato excel
            save_xlsx(res, material)

            #graficación
            self.configurar_ejes_grafico(material)
            self.ax.plot(frecuencias, r_fisico_teorico, label = 'Físico-teórico')
            self.ax.plot(frecuencias, r_iso, label = 'ISO 12354-1')
            self.ax.plot(frecuencias, r_cremer, label = 'Cremer')
            self.ax.plot(frecuencias, r_sharp, label = 'Sharp')
            self.ax.plot(frecuencias, r_davy, label = 'Davy')
            self.ax.axvline(x=fc, color='black', ls='--', label = f'Frecuencia de coincidencia (≈{round(fc)} Hz)')
            self.ax.legend(loc="upper left")
            self.canvas.draw()

        except ValueError:
            print('Ingrese números válidos')

if __name__ == '__main__':
    app = AppR()
    app.mainloop()