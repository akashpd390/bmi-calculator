try:
    from ctypes import windll, byref, sizeof, c_int
except Exception as e:
    pass
from setting import *
import customtkinter as ctk
import tkinter as tk


class App(ctk.CTk):
    def __init__(self):

        #root
        super().__init__(fg_color=GREEN)
        self.title('BMI')
        self.geometry('400x400')
        self.resizable(False,False)
        try:
            self.title_color()
        except Exception as e:
            pass


        #layout
        self.rowconfigure((0,1,2,3),weight=1,uniform='a')
        self.columnconfigure(0,weight=1,uniform='a')

        #data
        self.weight_variable = tk.DoubleVar(value=65)
        self.height_variable=tk.IntVar(value=150)
        self.bmi_variable=tk.IntVar()
        self.bmi_update()

        #tracing
        self.height_variable.trace('w',self.bmi_update)
        self.weight_variable.trace('w',self.bmi_update)

        #calling
        weight_input(self,self.weight_variable)
        height_input(self,self.height_variable)
        bmi(self,self.bmi_variable)


        self.mainloop()

    def title_color(self):
        HWND = windll.user32.GetParent(self.winfo_id())
        COLOR = TITLE_BAR_HEX
        windll.dwmapi.DwmSetWindowAttribute(HWND,35,byref(c_int(COLOR),sizeof(c_int)))
       
    def bmi_update(self,*args):
        weight=self.weight_variable.get()
        height=self.height_variable.get()/100
        # print(weight,height)
        bmi_ratio=round(weight/height**2,2)
        self.bmi_variable.set(bmi_ratio)
        

class bmi(ctk.CTkLabel):
    def __init__(self,parent,bmi_variable):
        font = ctk.CTkFont(family=FONT,size=MAIN_TEXT_SIZE)
        super().__init__(parent,text='17.9',font=font,textvariable=bmi_variable)
        self.grid(row= 0,column=0,rowspan=2)


class weight_input(ctk.CTkFrame):
    def __init__(self,parent,label_variable):
        super().__init__(parent,fg_color=WHITE,height=50)

        #layout
        self.rowconfigure(0,weight=1,uniform='a')
        self.columnconfigure(0,weight=2,uniform='a')
        self.columnconfigure(1,weight=1,uniform='a')
        self.columnconfigure(2,weight=3,uniform='a')
        self.columnconfigure(3,weight=1,uniform='a')
        self.columnconfigure(4,weight=2,uniform='a')

        #create button
        plus_button=ctk.CTkButton(self,command=lambda: self.update(('small','plus')),text='+',hover_color=LIGHT_GRAY,text_color=BLACK,fg_color=GRAY,corner_radius=5).grid(row=0,column=3,sticky='ew',padx=10,pady=10)
        lplus_button=ctk.CTkButton(self,command=lambda: self.update(('large','plus')),text='+',hover_color=LIGHT_GRAY,text_color=BLACK,fg_color=GRAY).grid(row=0,column=4,sticky='nsew',padx=10,pady=10)
        minus_button=ctk.CTkButton(self,command=lambda: self.update(('small','minus')),text='-',hover_color=LIGHT_GRAY,text_color=BLACK,fg_color=GRAY,corner_radius=5).grid(row=0,column=1,sticky='ew',padx=10,pady=10)
        lminus_button=ctk.CTkButton(self,command=lambda: self.update(('large','minus')),text='-',hover_color=LIGHT_GRAY,text_color=BLACK,fg_color=GRAY).grid(row=0,column=0,sticky='nsew',padx=10,pady=10)

        #weight_meter
        self.label_variable=label_variable
        self.output_variable = tk.StringVar(value='65 kg')

        font = ctk.CTkFont(family=FONT,size=INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self,text='65',textvariable=self.output_variable,text_color=BLACK,font=font).grid(row=0,column=2,sticky='nsew')

        self.grid(row=2, column=0,sticky='nsew',padx=10,pady=10)

    def update(self,info=None):
        amount= 1 if info[0]=='large' else 0.1
        if info[1]=='plus' :
            self.label_variable.set(self.label_variable.get()+amount)
        else :
            self.label_variable.set(self.label_variable.get()-amount)

        self.output_variable.set(f'{round(self.label_variable.get(),1)}kg')


class height_input(ctk.CTkFrame):
    def __init__(self,parent,height_variable):
        super().__init__(parent,fg_color=WHITE)

        #variable
        self.slide_variable=height_variable
        self.height_variable=tk.StringVar(value='1.5 m')

        #widgets
        slide=ctk.CTkSlider(self,command=self.update_text,from_=100,to=250,fg_color=GRAY,button_hover_color=GRAY,button_color=GREEN,progress_color=GREEN,variable=self.slide_variable).pack(side='left',expand=True,fill='x',padx=10,pady=10)
        label=ctk.CTkLabel(self,textvariable=self.height_variable, font=ctk.CTkFont(family=FONT,size=SWITCH_FONT_SIZE),text_color=BLACK).pack(side='left' ,expand=True,fill='x')

        self.grid(row=3, column=0,sticky='nsew',padx=10,pady=10)

    def update_text(self,ammount):
        text_string=str(int(ammount))
        self.height_variable.set(f'{text_string[0]}.{text_string[1]} m')



App()