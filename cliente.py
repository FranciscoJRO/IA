import socket
from pysat.solvers import Glucose3  # type: ignore # Importar Glucose3 para usar DPLL

class AgenteInteligente:
    def __init__(self):
        self.HOST = 'localhost'  # Cambia esto si estás usando una IP específica
        self.PORT = 65432  # Puerto del servidor
        self.percepciones = None
        self.dir = 'E'
        self.acciones = []
        self.posicion_actual = (1, 1)  # Inicializar la posición actual
        self.visitadas = set()  # Celdas visitadas
        self.conectarse()
        
        # Knowledge Base inicial
        self.KB = []
        self.solver = Glucose3()
        self.init_knowledge_base()

    def conectarse(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.HOST, self.PORT))
            self.percepciones = self.s.recv(1024).decode('utf-8')
            print(f"Conectado al servidor y recibí: {self.percepciones}")
        except Exception as e:
            print(f"Error al conectar: {e}")

    def enviar_accion(self, accion):
        try:
            self.s.sendall(accion.encode('utf-8'))
            self.percepciones = self.s.recv(1024).decode('utf-8')
            print(f"Recibido: {self.percepciones}")
        except Exception as e:
            print(f"Error al enviar acción: {e}")
            self.percepciones = "Perdiste"

    def init_knowledge_base(self):
        # Inicializar la base de conocimiento con el conocimiento inicial
        self.KB.append(self.encode_position(self.posicion_actual, "safe"))  # La celda inicial es segura
        self.solver.add_clause([self.encode_position(self.posicion_actual, "safe")])

    def encode_position(self, pos, attribute):
        # Codificar la posición y el atributo en una proposición
        x, y = pos
        if attribute == "safe":
            return x * 10 + y
        elif attribute == "wumpus":
            return -(x * 10 + y)
        elif attribute == "pit":
            return -(x * 10 + y + 100)
        elif attribute == "gold":
            return x * 10 + y + 200

    def update_knowledge_base(self, percepciones):
        x, y = self.posicion_actual
        if "Olor" in percepciones:
            # Si hay olor, hay un wumpus cerca
            self.solver.add_clause([self.encode_position((x+1, y), "wumpus")])
            self.solver.add_clause([self.encode_position((x-1, y), "wumpus")])
            self.solver.add_clause([self.encode_position((x, y+1), "wumpus")])
            self.solver.add_clause([self.encode_position((x, y-1), "wumpus")])
        if "Brisa" in percepciones:
            # Si hay brisa, hay un pozo cerca
            self.solver.add_clause([self.encode_position((x+1, y), "pit")])
            self.solver.add_clause([self.encode_position((x-1, y), "pit")])
            self.solver.add_clause([self.encode_position((x, y+1), "pit")])
            self.solver.add_clause([self.encode_position((x, y-1), "pit")])
        if "Brillo" in percepciones:
            # Si hay brillo, hay oro en la celda actual
            self.solver.add_clause([self.encode_position((x, y), "gold")])
        if "No siento nada" in percepciones:
            # Si no hay ninguna percepción, las celdas adyacentes son seguras
            self.solver.add_clause([self.encode_position((x+1, y), "safe")])
            self.solver.add_clause([self.encode_position((x-1, y), "safe")])
            self.solver.add_clause([self.encode_position((x, y+1), "safe")])
            self.solver.add_clause([self.encode_position((x, y-1), "safe")])

    def deduce_safe_cells(self):
        safe_cells = []
        for x in range(1, 5):
            for y in range(1, 5):
                if self.solver.solve(assumptions=[self.encode_position((x, y), "safe")]):
                    safe_cells.append((x, y))
        return safe_cells

    def deduce_gold_cells(self):
        gold_cells = []
        for x in range(1, 5):
            for y in range(1, 5):
                if self.solver.solve(assumptions=[self.encode_position((x, y), "gold")]):
                    gold_cells.append((x, y))
        return gold_cells

    def jugar(self):
        while True:
            if not self.percepciones:
                print("No se recibieron percepciones.")
                break

            percepciones = self.percepciones.split()
            if "Perdiste" in percepciones:
                print("He perdido el juego.")
                break
            if "oro" in percepciones:
                print("He ganado el juego.")
                break

            # Actualizar la base de conocimiento con las nuevas percepciones
            self.update_knowledge_base(percepciones)
            
            # Deduce celdas seguras
            safe_cells = self.deduce_safe_cells()
            print(f"Celdas seguras deducidas: {safe_cells}")
            
            # Deduce celdas con oro
            gold_cells = self.deduce_gold_cells()
            print(f"Celdas con oro deducidas: {gold_cells}")

            if gold_cells:
                # Si se deducen celdas con oro, moverse hacia ellas
                for cell in gold_cells:
                    if cell not in self.visitadas:
                        self.visitadas.add(cell)
                        self.enviar_accion(f"Avanzar: {cell}")
                        self.posicion_actual = cell
                        break
            else:
                # Selecciona la siguiente acción basada en celdas seguras
                for cell in safe_cells:
                    if cell not in self.visitadas:
                        self.visitadas.add(cell)
                        self.enviar_accion(f"Avanzar: {cell}")
                        self.posicion_actual = cell
                        break
                else:
                    print("No hay más celdas seguras para moverse.")
                    break

if __name__ == '__main__':
    agente = AgenteInteligente()
    agente.jugar()
