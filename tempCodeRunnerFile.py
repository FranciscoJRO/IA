from typing import List
from queue import Queue

class Estado:
    cadena = ''

    def __init__(self, cadena):
        self.cadena = cadena

    def swap(self, p1, p2):
        hijo = list(self.cadena[:])
        if 0 <= p1 < len(hijo) and 0 <= p2 < len(hijo):
            aux = hijo[p1]
            hijo[p1] = hijo[p2]
            hijo[p2] = aux
            hijostring = "".join(hijo)
            h1 = Estado(hijostring)
            return h1
        else:
            return None  # Indicar que la operación de intercambio no es válida

    def __str__(self):
        return self.cadena[:3]+'\n'+self.cadena[3:6]+'\n'+self.cadena[6:9]+'\n'+self.cadena[9:]+'\n'

    def __eq__(self, other):
        return self.cadena == other.cadena

    def hijos(self) -> List['Estado']:
        i = 0
        ret = []
        for c in self.cadena:
            if c == '0':
                if i == 0 or i == 2 or i == 9 or i == 11:
                    if i == 0:
                        ret.extend([self.swap(0, 1), self.swap(0, 3)])
                    elif i == 2:
                        ret.extend([self.swap(2, 1), self.swap(2, 5)])
                    elif i == 9:
                        ret.extend([self.swap(9, 3), self.swap(9, 7)])
                    elif i == 11:
                        ret.extend([self.swap(11, 5), self.swap(11, 7)])
                elif i == 4 or i == 7:
                    ret.extend([self.swap(1, 4), self.swap(3, 4), self.swap(5, 4), self.swap(7, 4),
                                self.swap(4, 7), self.swap(6, 7), self.swap(8, 7), self.swap(10, 7)])
                else:
                    if i == 1:
                        ret.extend([self.swap(1, 0), self.swap(1, 2), self.swap(1, 4)])
                    elif i == 3:
                        ret.extend([self.swap(3, 0), self.swap(3, 4), self.swap(3, 6)])
                    elif i == 5:
                        ret.extend([self.swap(5, 2), self.swap(5, 4), self.swap(5, 8)])
                    elif i == 6:
                        ret.extend([self.swap(6, 3), self.swap(6, 7), self.swap(6, 9)])
                    elif i == 8:
                        ret.extend([self.swap(8, 5), self.swap(8, 7), self.swap(8, 11)])
                    elif i == 10:
                        ret.extend([self.swap(10, 9), self.swap(10, 7), self.swap(10, 11)])
            i += 1
        return ret

def bfs(e_inicial):
    por_visitar = []
    visitados = set()

    por_visitar.append((e_inicial, 0))
    e_final = Estado('1A435B067892')

    while por_visitar:
        e, padre = por_visitar.pop(0)
        if e == e_final:
            break
        if e.cadena not in visitados:
            visitados.add(e.cadena)
            for v in e.hijos():
                if v:
                    por_visitar.append((v, e.cadena))
    ruta = []
    padre = e.cadena
    while padre != '123456709A8B':
        ruta.append(padre)
        padre = visitados[padre]
    ruta.append(padre)
    return ruta

if __name__ == '__main__':
    e = Estado('123456709A8B')
    ruta = bfs(e)
    print(ruta)
