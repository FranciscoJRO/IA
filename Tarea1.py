import time

class Estado:
    cadena = ''

    def __init__(self, cadena):
        self.cadena = cadena

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


def bfs(e_inicial, e_final):
    por_visitar_inicial = [(e_inicial, 0)]
    por_visitar_final = [(e_final, 11)]
    visitados_inicial = {}
    visitados_final = {}

    while por_visitar_inicial and por_visitar_final:
        if bfs_visit(visitados_inicial, por_visitar_inicial, visitados_final):
            ruta = reconstruct_path(visitados_inicial, visitados_final)
            if ruta is not None:
                return ruta
        if bfs_visit(visitados_final, por_visitar_final, visitados_inicial):
            ruta = reconstruct_path(visitados_inicial, visitados_final)
            if ruta is not None:
                return ruta

    return None


def bfs_visit(visitados, por_visitar, otro_visitados):
    e, padre = por_visitar.pop(0)
    if e.cadena in visitados:
        return False
    visitados[e.cadena] = padre
    for v in e.hijos():
        if v.cadena in otro_visitados:
            return True
        por_visitar.append((v, e.cadena))
    return False


def reconstruct_path(visitados_inicial, visitados_final):
    ruta_inicial = []
    ruta_final = []
    for key in visitados_inicial.keys():
        if key in visitados_final:
            padre = visitados_inicial[key]
            while padre != 0:
                ruta_inicial.append(padre)
                padre = visitados_inicial[padre]
            padre = visitados_final[key]
            while padre != 11:
                ruta_final.append(padre)
                padre = visitados_final[padre]
            return ruta_inicial[::-1] + ruta_final  # Invertir la lista antes de retornarla
    return None

if __name__ == '__main__':
    start_time = time.time()

    e_inicial = Estado('035142A768B9')  # Estado inicial modificado
    e_final = Estado('123456789AB0')
    ruta = bfs(e_inicial, e_final)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Tiempo de ejecución:", execution_time, "segundos")

    print(ruta)
