import time
import heapq

class Estado:
    cadena = ''

    def __init__(self, cadena, g=0):
        self.cadena = cadena
        self.g = g  # Costo acumulado desde el nodo inicial

    def swap(self, p1, p2):
        hijo = list(self.cadena[:])
        aux = hijo[p1]
        hijo[p1] = hijo[p2]
        hijo[p2] = aux
        hijostring = "".join(hijo)
        h1 = Estado(hijostring)
        return h1

    def __str__(self):
        return self.cadena[:3] + '\n' + self.cadena[3:6] + '\n' + self.cadena[6:9] + '\n' + self.cadena[9:] + '\n'

    def __eq__(self, other):
        return self.cadena == other.cadena

    def __lt__(self, other):
        return self.g < other.g

    def manhattan_distance(self, goal_state):
        distance = 0
        for i in range(12):
            if self.cadena[i] != goal_state.cadena[i] and self.cadena[i] != 'A':
                index_goal = goal_state.cadena.index(self.cadena[i])
                x1, y1 = i // 3, i % 3
                x2, y2 = index_goal // 3, index_goal % 3
                distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    def f(self, goal_state):
        return self.g + self.manhattan_distance(goal_state)

    def hijos(self):
        i = 0
        ret = []
        for c in self.cadena:
            if c == '0':
                if i == 0:
                    ret = [self.swap(0, 1), self.swap(0, 3)]
                elif i == 1:
                    ret = [self.swap(1, 0), self.swap(1, 2), self.swap(1, 4)]
                elif i == 2:
                    ret = [self.swap(2, 1), self.swap(2, 5)]
                elif i == 3:
                    ret = [self.swap(3, 0), self.swap(3, 4), self.swap(3, 6)]
                elif i == 4:
                    ret = [self.swap(4, 1), self.swap(4, 3), self.swap(4, 5), self.swap(4, 7)]
                elif i == 5:
                    ret = [self.swap(5, 2), self.swap(5, 4), self.swap(5, 8)]
                elif i == 6:
                    ret = [self.swap(6, 3), self.swap(6, 7), self.swap(6, 9)]
                elif i == 7:
                    ret = [self.swap(7, 4), self.swap(7, 6), self.swap(7, 8), self.swap(7, 10)]
                elif i == 8:
                    ret = [self.swap(8, 5), self.swap(8, 7), self.swap(8, 11)]
                elif i == 9:
                    ret = [self.swap(9, 6), self.swap(9, 10)]
                elif i == 10:
                    ret = [self.swap(10, 7), self.swap(10, 9), self.swap(10, 11)]
                elif i == 11:
                    ret = [self.swap(11, 8), self.swap(11, 10)]
            i += 1
        return ret

def a_star(e_inicial, e_final):
    visitados = set()
    heap = []
    heapq.heappush(heap, (e_inicial.f(e_final), e_inicial))

    while heap:
        _, estado_actual = heapq.heappop(heap)

        if estado_actual == e_final:
            return estado_actual

        if estado_actual.cadena in visitados:
            continue

        visitados.add(estado_actual.cadena)

        for hijo in estado_actual.hijos():
            if hijo.cadena not in visitados:
                hijo.g = estado_actual.g + 1
                heapq.heappush(heap, (hijo.f(e_final), hijo))

    return None

if __name__ == '__main__':
    start_time = time.time()

    e_inicial = Estado('1A435B067892')  # Estado inicial modificado
    e_final = Estado('123456789AB0')
    resultado = a_star(e_inicial, e_final)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Tiempo de ejecución:", execution_time, "segundos")

    if resultado:
        print(resultado)
    else:
        print("No se encontró solución.")
