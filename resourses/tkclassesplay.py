#https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
# 
#         # configure the root window
#         self.title("Python Tutorial App")
#         self.geometry("300x50")
# 
#         # label
#         self.label = ttk.Label(self, text = "Hello, Tkinter!")
#         self.label.pack()
#         # pack is simpler when playing round compared to grid but less accurate
# 
#         # button
#         self.button = ttk.Button(self, text =" Click Me")
#         self.button["command"] = self.button_clicked
#         self.button.pack()
# 
#         # event
# 
#     def button_clicked(self):
#         showinfo(title = "Information", message = "Hello, TKinter!")
# 
# 
# class InputFrame(ttk.Frame):
#     def __init__(self, container):
#         super().__init__(container)
#         # setup the grid Layout manager
#         self.columnconfigure(0, weight = 1)
#         self.columnconfigure(0, weight = 3)
#         
#         self.__create_widgets()
# 
#     def __create_widgets(self):
#         #Find what
#         ttk.Label(self, text = 'Find what:').grid(column = 0, row = 0, sticky = tk.W)
#         keyword = ttk.Entry(self, width = 30)
#         keyword.focus()
#         keyword.grid(column = 1, row = 0, sticky = tk.W)
#         
#         # Replace with:
#         ttk.Label(self, text = 'Replace with:').grid(column = 0, row = 1, sticky = tk.W)
#         replacement = ttk.Entry(self, width = 30)
#         replacement.grid(column = 1, row = 1, sticky = tk.W)
#         
#         #Match case checkbox
#         match_case = tk.StringVar()
#         match_case_check = ttk.Checkbutton(self, text = 'Match case', variable = match_case,
#                                            command = lambda: print(match_case.get()))
#         match_case_check.grid(column = 0, row = 2, sticky = tk.W)
#         
#         #Wrap Around checkbox
#         wrap_around = tk.StringVar()
#         wrap_around_check = ttk.Checkbutton(self, variable = wrap_around,
#                                             text = 'Wrap around', command = lambda: print(wrap_around.get()))
#         wrap_around_check.grid(column = 0, row = 3, sticky = tk.W)
#         
#         for widget in self.winfo_children():
#             widget.grid(padx = 0, pady = 5)
# 
# class ButtonFrame(ttk.Frame):
#     def __init__(self, container):
#         super().__init__(container)
#         #set the grid layout manager
#         self.columnconfigure(0, weight = 1)
#         
#         self.__create_widgets()
#     
#     def __create_widgets(self):
#         ttk.Button(self, text = 'Find Next').grid(column = 0, row = 0)
#         ttk.Button(self, text = 'Replace').grid(column = 0, row = 1)    
#         ttk.Button(self, text = 'Replace All').grid(column = 0, row = 2)   
#         ttk.Button(self, text = 'Cancel').grid(column = 0, row = 3)
#         
#         for widget in self.winfo_children():
#             widget.grid(padx = 0, pady = 3)
#             
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
# 
#         # configure the root window
#         self.title("Replace")
#         self.geometry("400x150")
#         self.resizable(0, 0)
#         #windows only remove the minimize/maximize button
#         self.attributes('-toolwindow', True)
#         
#         #layout on the rood window
#         
#         self.columnconfigure(0, weight = 4)
#         self.columnconfigure(1, weight = 1)
#         
#         self.__create_widgets()
#         
#     def __create_widgets(self):
#         input_frame = InputFrame(self)
#         input_frame.grid(column = 0, row = 0)
#         
#         button_frame = ButtonFrame(self)
#         button_frame.grid(column = 1, row = 0)
        
        


# https://www.pythontutorial.net/tkinter/tkinter-object-oriented-application/

"""A fully functional temperature converter"""
#A class that has a static method that converts from Farenheit to celcius
#static methods are an object member that are directly accessible to the constructor
class TemperatureConverter:
    @staticmethod
    def fahrenheit_to_celcius(f):#Note: this causes a bug... I am working on it.
        return (f - 32) * 5/9
#converter frame that inherits from ttk.Frame for creating widgets and calling events

class ConverterFrame(ttk.Frame):
    """Create a frame to contain the converter elements"""
    def __init__(self, container):
        """Create a function to build the container frame"""
        super().__init__(container) #call the constructor
        #must always start with a super().__init__ to intialize the constructor
        
        #field options
        options = {'padx':5, 'pady':5}
        
        #temperature Label
        self.temperature_label = ttk.Label(self, text = 'Fahrenheit')
        self.temperature_label.grid(column = 0, row = 0, sticky = tk.W, **options)
        
        #temperature entry
        self.temperature = tk.StringVar() # allows the use of a dot get fucnction
        self.temperature_entry = ttk.Entry(self, textvariable = self.temperature)
        self.temperature_entry.grid(column = 1, row = 0, **options)
        self.temperature_entry.focus()
        
        self.convert_button = ttk.Button(self, text = 'Convert')
        self.convert_button['command'] = self.convert
        self.convert_button.grid(column = 2, row = 0, sticky = tk.W, **options)
        
        #result Label
        self.result_label = ttk.Label(self)
        self.result_label.grid(row = 1, columnspan = 3, **options)
        
        #add padding to the frame and show it
        self.grid(padx = 10, pady = 10, sticky = tk.NSEW)
        
    def convert(self):
        """button click event handler to perform the conversion"""
        #error handling function to do the conversion
        try:
            f = float(self.temperature.get())
            c = TemperatureConverter.fahrenheit_to_celsius(f)
            result = f'{f} Fahrenheit = {c:.2f} Celsius'
            self.result_label.config(text = result)
        except ValueError as error:
            showerror(title = 'Error', message = error)
    
            
class App(tk.Tk):
    """Class to run the program"""
    def __init__(self):
        super().__init__()
        
        self.title('Temperature Converter')
        self.geometry('300x70')
        self.resizable(False, False)
        
        
if __name__ == "__main__":
    app = App()
    ConverterFrame(app)
    app.mainloop()

#    app()