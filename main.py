from screens import StartScreen
from tkinter import *

# Display a tkinter window
window = Tk()
window.title("Typing Test")
window.config(width=200, height=200, padx=50, pady=50, bg="wheat1")

StartScreen(window)

window.mainloop()
