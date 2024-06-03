import socket
import tkinter as tk
from tkinter import messagebox

class WumpusClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Hunt the Wumpus")

        self.host = 'localhost'  # Cambia esto si estás usando una IP específica
        self.port = 65432

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.output_text = tk.Text(root, height=20, width=50, state='disabled')
        self.output_text.pack()

        self.input_text = tk.Entry(root, width=50)
        self.input_text.pack()
        self.input_text.bind("<Return>", self.send_action)

        self.send_button = tk.Button(root, text="Enviar", command=self.send_action)
        self.send_button.pack()
        
        self.reset_button = tk.Button(root, text="Reiniciar", command=self.reset_game)
        self.reset_button.pack()

        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.conn.connect((self.host, self.port))
            self.receive_data()
        except ConnectionRefusedError:
            messagebox.showerror("Error", "No se pudo conectar al servidor")

    def reset_game(self):
        self.conn.close()  # Cerrar la conexión existente
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un nuevo socket
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)  # Limpiar la ventana de salida
        self.output_text.config(state='disabled')
        self.connect_to_server()  # Reconectar al servidor

    def send_action(self, event=None):
        action = self.input_text.get()
        self.conn.sendall(action.encode('utf-8'))
        self.input_text.delete(0, tk.END)
        self.receive_data()

    def receive_data(self):
        data = self.conn.recv(1024).decode('utf-8')
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, "Servidor: " + data + "\n")
        self.output_text.config(state='disabled')

if __name__ == '__main__':
    root = tk.Tk()
    app = WumpusClient(root)
    root.mainloop()
