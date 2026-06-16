import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from funciones import calc_m, calc_b, calc_fc, calc_fd, save_xlsx, graficar
from fisico_teorico import fisico_teorico
from cremer import cremer
from sharp import sharp
from davy import davy
from iso import iso

#definición de la clase 'Material'
class Material:
    def __init__(self, tipo, densidad, myoung, fperd, mpoisson, dimensiones):
        self.tipo = tipo
        self.rho = float(densidad)
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

        #variables para almacenar el estado de selección de cada modelo
        self.check_fisico_teorico = ctk.BooleanVar(value = False)
        self.check_iso = ctk.BooleanVar(value = False)
        self.check_cremer = ctk.BooleanVar(value = False)
        self.check_sharp = ctk.BooleanVar(value = False)
        self.check_davy = ctk.BooleanVar(value = False)

        #creación y posicionamiento de componentes
        self.title('Calculadora de Aislamiento Acústico - Paneles Simples')
        self.geometry("1200x800")

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

        #entradas dimensiones
        self.label_alto = ctk.CTkLabel(self.sidebar, text = 'Alto (m):')
        self.label_alto.pack(padx = 20, pady = 5, anchor = 'w')
        self.input_alto = ctk.CTkEntry(self.sidebar, placeholder_text = '3')
        self.input_alto.insert(0, '3')
        self.input_alto.pack(padx = 20, pady = 5, fill = 'x')

        self.label_ancho = ctk.CTkLabel(self.sidebar, text = 'Ancho (m):')
        self.label_ancho.pack(padx = 20, pady = 5, anchor = 'w')
        self.input_ancho = ctk.CTkEntry(self.sidebar, placeholder_text = '7')
        self.input_ancho.insert(0, '7')
        self.input_ancho.pack(padx = 20, pady = 5, fill = 'x')

        self.label_espesor = ctk.CTkLabel(self.sidebar, text = 'Espesor (cm):')
        self.label_espesor.pack(padx = 20, pady = 5, anchor = 'w')
        self.input_espesor = ctk.CTkEntry(self.sidebar, placeholder_text = '2')
        self.input_espesor.insert(0, '2')
        self.input_espesor.pack(padx = 20, pady = 10, fill = 'x')

        #botón refresh
        self.btn_calcular = ctk.CTkButton(self.sidebar, text = 'Aplicar dimensiones y material', command = self.calcular)
        self.btn_calcular.pack(padx = 20,  pady = 20, fill = 'x')

        #selectores de modelos
        selector_fisico_teorico = ctk.CTkCheckBox(
            self.sidebar,
            text = 'Modelo Físico-Teórico',
            variable = self.check_fisico_teorico,
            command = self.calcular,
            onvalue = True,
            offvalue = False
        )
        selector_fisico_teorico.pack(padx = 20, pady = 5, anchor = 'w')

        selector_iso = ctk.CTkCheckBox(
            self.sidebar,
            text = 'Modelo ISO 12354-1',
            variable = self.check_iso,
            command = self.calcular,
            onvalue = True,
            offvalue = False
        )
        selector_iso.pack(padx = 20, pady = 5, anchor = 'w')

        selector_cremer = ctk.CTkCheckBox(
            self.sidebar,
            text = 'Modelo Cremer',
            variable = self.check_cremer,
            command = self.calcular,
            onvalue = True,
            offvalue = False
        )
        selector_cremer.pack(padx = 20, pady = 5, anchor = 'w')

        selector_sharp = ctk.CTkCheckBox(
            self.sidebar,
            text = 'Modelo Sharp',
            variable = self.check_sharp,
            command = self.calcular,
            onvalue = True,
            offvalue = False
        )
        selector_sharp.pack(padx = 20, pady = 5, anchor = 'w')

        selector_davy = ctk.CTkCheckBox(
            self.sidebar,
            text = 'Modelo Davy',
            variable = self.check_davy,
            command = self.calcular,
            onvalue = True,
            offvalue = False
        )
        selector_davy.pack(padx = 20, pady = 5, anchor = 'w')

        #botón guardar
        self.btn_guardar = ctk.CTkButton(self.sidebar, text = 'Guardar', command = self.guardar)
        self.btn_guardar.pack(padx = 20, fill = 'x', pady = 20)

        #gráfico
        self.frame_grafico = ctk.CTkFrame(self, corner_radius = 10)
        self.frame_grafico.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = 'nsew')

        self.fig, self.ax = plt.subplots(figsize = (6, 5), dpi = 100)
        self.configurar_ejes_grafico()

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_grafico)
        self.canvas.get_tk_widget().pack(padx=20, pady=20, fill='both', expand=True)

        #inicialización del popup
        self.popup = None

        #variables de selectores
        self.ind_sel = 9
        self.material = None

        #vectores de resultados
        self.r_fisico_teorico = None
        self.r_iso = None
        self.r_cremer = None
        self.r_sharp = None
        self.r_davy = None

        #llamada a función onclose
        self.protocol('WM_DELETE_WINDOW', self.cerrar)

    #función onclose
    def cerrar(self):
        #cierre ordenado del popup
        if self.popup and self.popup.winfo_exists():
            if hasattr(self.popup, 'fade_id') and self.popup.fade_id:
                self.popup.after_cancel(self.popup.fade_id)

            self.popup.destroy()

        #cierre ordenado del gráfico
        try:
            plt.close(self.fig)
            self.canvas.get_tk_widget().destroy()
        except:
            pass
        
        self.update_idletasks()

        self.destroy()

    #función actualización del material seleccionado
    def cambiar_material(self, mat):
        self.ind_sel = mats.index(mat)

    #función configuración y refresh de los ejes
    def configurar_ejes_grafico(self, material = None):
        self.ax.clear()
        self.ax.set_xscale('log')
        self.ax.set_xlabel('Frecuencia [Hz]')
        self.ax.set_ylabel('R [dB]')

        if material != None:
            self.ax.set_title(f'R para un panel simple de {material.tipo.lower()} de {str(material.dim[0]).replace(".", ",")}m x {str(material.dim[1]).replace(".", ",")}m x {str(material.dim[2]).replace(".", ",")}m', fontsize = '16')
        else:
            self.ax.set_title('')

        self.ax.set_xlim(20, 20000)
        self.ax.set_ylim(0, 130)
        self.ax.grid(True, which = 'both', ls = '--', alpha = 0.5)
        self.ax.set_xticks(frecuencias)
        self.ax.set_xticklabels([str(int(f)) if float(f).is_integer() else float(f) for f in frecuencias], rotation = 45)

    #función generación de popup
    def mostrar_error(self, error):
        if hasattr(self, 'popup') and self.popup and self.popup.winfo_exists():
            self.popup.destroy()

        self.popup = ctk.CTkToplevel(self)
        popup = self.popup
        popup.title('Aviso')
        
        popup.attributes('-topmost', True)
        popup.resizable(False, False)

        popup_label = ctk.CTkLabel(
            popup,
            text = error,
            font = ctk.CTkFont('Calibri', size = 20, weight = 'bold'),
            text_color = "#000000"
        )
        popup_label.pack(expand = True, padx = 30, pady = 30)

        popup.update_idletasks()

        reqwidth = popup.winfo_reqwidth()
        reqheight = popup.winfo_reqheight()

        swidth = popup.winfo_screenwidth()
        sheight = popup.winfo_screenheight()

        posx = int((swidth - reqwidth) / 2)
        posy = int((sheight - reqheight) / 2)

        popup.geometry(f'{reqwidth}x{reqheight}+{posx}+{posy}')

        popup.fade_id = None

        def onclose():
            if popup.winfo_exists():
                if popup.fade_id:
                    popup.after_cancel(popup.fade_id)
                    popup.fade_id = None

                popup.update_idletasks()
                popup.destroy()
                self.popup = None

        def fade():
            if not popup.winfo_exists():
                return
            
            current_alpha = popup.attributes('-alpha')

            if current_alpha > 0.05:
                new_alpha = current_alpha - 0.05
                popup.attributes('-alpha', new_alpha)

                popup.fade_id = popup.after(30, fade)
            else:
                onclose()
        
        popup.protocol('WM_DELETE_WINDOW', onclose)
        popup.fade_id = popup.after(2500, fade)

    #función de cálculo de resultados y graficación
    def calcular(self):
        try:
            #adquisición de datos desde los inputs
            dim = (float(self.input_alto.get().replace(',', '.')), float(self.input_ancho.get().replace(',', '.')), float(self.input_espesor.get().replace(',', '.')) / 100)
            ind = self.ind_sel

            if any(n < 0 for n in dim):
                self.mostrar_error('Advertencia: entrada inadecuada. Las dimensiones no pueden ser números negativos')
            else:
                #instanciación de un objeto de la clase 'Material'
                self.material = Material(db.iloc[ind, 1], db.iloc[ind, 2], db.iloc[ind, 3], db.iloc[ind, 4], db.iloc[ind, 5], dim)

                #cálculo de la frecuencia crítica y de la frecuencia de densidad
                fc = calc_fc(self.material, c)
                fd = calc_fd(self.material)

                self.configurar_ejes_grafico(self.material)

                #cálculo de R con los modelos y graficación
                if self.check_fisico_teorico.get():
                    self.r_fisico_teorico = fisico_teorico(frecuencias, self.material, fc, fd, rho0, c)
                    graficar(self.ax, frecuencias, self.r_fisico_teorico, 'Físico-Teórico', '#E69F00')
                    self.ax.axvline(x = fd, color = 'black', ls = '--', label = f'Frecuencia de densidad (≈{round(fd)} Hz)')

                if self.check_iso.get():
                    self.r_iso = iso(frecuencias, self.material, fc, rho0, c)
                    graficar(self.ax, frecuencias, self.r_iso, 'ISO 12354-1', '#56B4E9')  

                if self.check_cremer.get():
                    self.r_cremer = cremer(frecuencias, self.material, fc, fd)
                    graficar(self.ax, frecuencias, self.r_cremer, 'Cremer', "#3AA641")
                    self.ax.axvline(x = fd, color = 'black', ls = '--', label = f'Frecuencia de densidad (≈{round(fd)} Hz)')

                if self.check_sharp.get():
                    self.r_sharp = sharp(frecuencias, self.material, fc, rho0, c)
                    graficar(self.ax, frecuencias, self.r_sharp, 'Sharp', "#E982F3")
                
                if self.check_davy.get():
                    self.r_davy = davy(frecuencias, self.material, fc, rho0, c)
                    graficar(self.ax, frecuencias, self.r_davy, 'Davy', "#B51919")

                #vaciado de los vectores de resultados de los modelos no seleccionados
                if not self.check_fisico_teorico.get():
                    self.r_fisico_teorico = None
                
                if not self.check_iso.get():
                    self.r_iso = None
                
                if not self.check_cremer.get():
                    self.r_cremer = None

                if not self.check_sharp.get():
                    self.r_sharp = None
                
                if not self.check_davy.get():
                    self.r_davy = None

                self.ax.axvline(x = fc, color = 'black', ls = '--', label = f'Frecuencia de coincidencia (≈{round(fc)} Hz)')
                self.ax.legend(loc="upper left")
                self.canvas.draw()

        except ValueError:
            self.mostrar_error('Advertencia: entrada inadecuada. Las dimensiones deben ser números válidos')

        except ZeroDivisionError:
            self.mostrar_error('Advertencia: entrada inadecuada. Las dimensiones no pueden ser cero')

    #función de guardado de los datos
    def guardar(self):
        try:
            #creación del DataFrame con los resultados
            data_R = [self.r_fisico_teorico, self.r_iso, self.r_cremer, self.r_sharp, self.r_davy]
            modelos = ['Físico-teórico', 'ISO 12354-1', 'Cremer', 'Sharp', 'Davy']
                    
            pares = [(d, modelo) for d, modelo in zip(data_R, modelos) if d is not None]

            if pares:
                data_R, modelos = map(list, zip(*pares))

                res = pd.DataFrame(
                data = data_R,
                index = modelos,
                columns = frecuencias
                )

                #guardado en formato excel
                save_xlsx(res, self.material, modelos)
                self.mostrar_error('Archivo guardado correctamente')

            else:
                self.mostrar_error('Error de guardado. Seleccione al menos un modelo')

        except:
            self.mostrar_error('Error de guardado. Introduzca los datos correctamente')

if __name__ == '__main__':
    app = AppR()
    app.mainloop()