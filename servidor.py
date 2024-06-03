import ctypes  # No utilizado, se puede eliminar
import random as rnd
import struct  # No utilizado, se puede eliminar
import socket

class Conexion:
    def __init__(self):
        # Configuración del servidor
        HOST = socket.gethostname()
        PORT = 65432  # Puerto para escuchar

        # Inicialización del socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen()

        # Espera y acepta una conexión
        conn, addr = self.s.accept()
        with conn:
            print(f"Connected by {addr}")
            e = Escenario()
            print(e)
            sense = e.sense()
            conn.sendall(bytearray(sense.encode('utf-8')))
            while sense != 'Perdiste':
                data = conn.recv(1024).decode('utf-8')
                print(data)
                if not data:
                    break
                a = data.split(":")
                if a[0] == 'Girar':
                    dir = a[1]
                    sense = e.accion(a[0], dir)
                else:
                    sense = e.accion(a[0])
                conn.sendall(bytearray(sense.encode('utf-8')))
        self.s.close()
        conn.close()

class Escenario:
    def __init__(self):
        rnd.seed(3)
        self.puntuacion = 0
        self.wumpus = (rnd.randint(1, 4), rnd.randint(1, 4))
        self.gold = (rnd.randint(1, 4), rnd.randint(1, 4), False)
        self.pits = []
        for i in range(4):
            for j in range(4):
                if rnd.uniform(0, 1) < 0.2:
                    self.pits.append((i + 1, j + 1))
        self.player = ((1, 1, 'E'))

    def __str__(self):
        escena = [''] * 16
        coords = lambda x, y: x + 4 * (4 - y) - 1

        escena[coords(self.wumpus[0], self.wumpus[1])] += 'W'
        escena[coords(self.gold[0], self.gold[1])] += 'G'
        for p in self.pits:
            escena[coords(p[0], p[1])] += 'P'
        if self.player[2] == 'N':
            pos = 'n'
        elif self.player[2] == 'O':
            pos = '<'
        elif self.player[2] == 'S':
            pos = 'v'
        elif self.player[2] == 'E':
            pos = '>'
        else:
            pos = 'O'

        escena[coords(self.player[0], self.player[1])] += pos

        s = ''
        for i in range(len(escena)):
            if i % 4 == 0:
                s += '\n------------------------\n'
            s += ' ' * (4 - len(escena[i])) + escena[i] + '|'
        return s

    def print(self):
        print('Wumpus:', self.wumpus)
        print('Oro:', self.gold)
        print('Pits:', self.pits)

    def avanzar(self, dir):
        estado = None
        if dir == 'E':
            if self.player[0] == 4:
                estado = "Pum me pegue"
            else:
                pos = self.player[0]
                pos += 1
                self.player = ((pos, self.player[1], dir))
        elif dir == 'O':
            if self.player[0] == 1:
                estado = "Pum me pegue"
            else:
                pos = self.player[0]
                pos -= 1
                self.player = ((pos, self.player[1], dir))
        elif dir == 'N':
            if self.player[1] == 4:
                estado = "Pum me pegue"
            else:
                pos = self.player[1]
                pos += 1
                self.player = ((self.player[0], pos, dir))
        elif dir == 'S':
            if self.player[1] == 1:
                estado = "Pum me pegue"
            else:
                pos = self.player[1]
                pos -= 1
                self.player = ((self.player[0], pos, dir))
        return estado

    def sense(self):
        if self.perdi():
            return 'Perdiste'
        ret = ''
        x, y, _ = self.player
        surroundings = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        wumpus_scent = False
        wind_scent = False
        brillo_scent = False

        for pos in surroundings:
            if pos == self.wumpus:
                wumpus_scent = True
            if pos in self.pits:
                wind_scent = True
        if x == self.gold[0] and y == self.gold[1]:
            brillo_scent = True

        if wumpus_scent:
            ret += "Olor "
        if wind_scent:
            ret += "Brisa "
        if brillo_scent:
            ret += "Brillo "
        if ret == '':
            ret = 'No siento nada'
        return ret

    def disparar(self):
        self.puntuacion -= 9
        if (self.player[2] == 'N' and self.player[1] < self.wumpus[1]) or \
           (self.player[2] == 'S' and self.player[1] > self.wumpus[1]) or \
           (self.player[2] == 'E' and self.player[0] < self.wumpus[0]) or \
           (self.player[2] == 'O' and self.player[0] > self.wumpus[0]):
            return ""
        else:
            return "Rugido"

    def perdi(self):
        if self.player[0] == self.wumpus[0] and self.player[1] == self.wumpus[1]:
            return True
        for pit in self.pits:
            if self.player[0] == pit[0] and self.player[1] == pit[1]:
                return True
        return False

    def accion(self, a, dir=None):
        self.puntuacion -= 1
        if a == 'Girar':
            self.player = (self.player[0], self.player[1], dir)
        elif a == 'Avanzar':
            estado = self.avanzar(self.player[2])
            if estado is not None:
                return estado
        elif a == 'Disparar':
            return self.disparar()
        elif a == 'Subir':
            if self.gold[2]:
                if self.player[0] == 1 and self.player[1] == 1:
                    self.puntuacion += 1000
                    return 'Puntuacion: ' + str(self.puntuacion)
        elif a == 'Recoger':
            if not self.gold[2] and self.player[0] == self.gold[0] and self.player[1] == self.gold[1]:
                self.gold[2] = True
                return 'Oro levantado exitosamente'
        print(self)
        return self.sense()

if __name__ == '__main__':
    Conexion()
