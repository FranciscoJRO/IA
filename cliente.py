import socket
import itertools

# Conexión al servidor
HOST = "132.248.59.195"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

class WumpusClient:
    def __init__(self):
        self.knowledge_base = set()
        self.visited = set()
        self.safe_cells = {(1, 1)}

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def disconnect(self):
        self.s.close()

    def send_action(self, action):
        self.s.sendall(action.encode('utf-8'))

    def receive_sense(self):
        return self.s.recv(1024).decode('utf-8')

    def update_knowledge_base(self, perception, position):
        x, y = position
        if 'Olor' in perception:
            self.knowledge_base.add(f"W({x+1},{y}) or W({x-1},{y}) or W({x},{y+1}) or W({x},{y-1})")
        if 'Brisa' in perception:
            self.knowledge_base.add(f"P({x+1},{y}) or P({x-1},{y}) or P({x},{y+1}) or P({x},{y-1})")
        if 'Brillo' in perception:
            self.knowledge_base.add(f"G({x},{y})")

    def dpll(self, clauses):
        # Implementación simplificada del algoritmo DPLL
        def unit_propagate(clauses, assignment):
            while True:
                unit_clauses = [c for c in clauses if len(c) == 1]
                if not unit_clauses:
                    break
                unit = unit_clauses[0]
                literal = next(iter(unit))
                clauses = [c - {literal, -literal} for c in clauses if literal not in c]
                assignment.add(literal)
            return clauses, assignment

        def pure_literal_assign(clauses, assignment):
            literals = set(itertools.chain.from_iterable(clauses))
            pure_literals = {l for l in literals if -l not in literals}
            for pure in pure_literals:
                clauses = [c for c in clauses if pure not in c]
                assignment.add(pure)
            return clauses, assignment

        def choose_literal(clauses):
            for clause in clauses:
                for literal in clause:
                    return literal

        def dpll_recursive(clauses, assignment):
            clauses, assignment = unit_propagate(clauses, assignment)
            if not clauses:
                return True, assignment
            if set() in clauses:
                return False, None
            clauses, assignment = pure_literal_assign(clauses, assignment)
            literal = choose_literal(clauses)
            new_clauses = [c | {literal} for c in clauses] + [{-literal}]
            solvable, new_assignment = dpll_recursive(new_clauses, assignment)
            if solvable:
                return True, new_assignment
            new_clauses = [c | {-literal} for c in clauses] + [{literal}]
            return dpll_recursive(new_clauses, assignment)

        return dpll_recursive(clauses, set())

    def solve(self):
        self.connect()
        current_position = (1, 1)
        direction = 'E'

        while True:
            sense = self.receive_sense()
            print("Received:", sense)
            if sense == 'Perdiste':
                break

            self.update_knowledge_base(sense, current_position)
            # Convertir la base de conocimiento en una lista de cláusulas para DPLL
            clauses = [set(map(int, clause.split())) for clause in self.knowledge_base]
            solvable, assignment = self.dpll(clauses)
            
            if not solvable:
                print("No se pudo encontrar una solución segura.")
                break

            # Seleccionar la siguiente celda segura para moverse
            next_position = None
            for cell in self.safe_cells:
                if cell not in self.visited:
                    next_position = cell
                    break

            if next_position:
                x, y = current_position
                next_x, next_y = next_position

                if next_x > x:
                    direction = 'E'
                elif next_x < x:
                    direction = 'O'
                elif next_y > y:
                    direction = 'N'
                elif next_y < y:
                    direction = 'S'

                current_position = next_position
                self.visited.add(current_position)
                self.send_action(f"Avanzar:{direction}")
            else:
                print("No hay más celdas seguras para moverse.")
                break

        self.disconnect()

if __name__ == '__main__':
    client = WumpusClient()
    client.solve()
