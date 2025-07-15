import tkinter as tk

def run_gui():
    root = tk.Tk()
    root.title("Benvenuto nel tuo primo Programma Schillinger")
    
    label = tk.Label(root, text="Welcome to the Schillinger GUI!")
    label.pack(pady=20)

    button = tk.Button(root, text="Exit", command=root.quit)
    button.pack(pady=10)

    root.mainloop()