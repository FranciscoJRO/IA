class Estado:
    cadena = ''
    def __init__(self, cadena):
        self.cadena = cadena
    def valida(self):
        pass
    def swap(self, p1, p2):
        hijo = list(self.cadena[:])
        aux = hijo[p1]
        hijo[p1] = hijo[p2]
        hijo[p2] = aux
        hijostring = "".join(hijo)
        h1 = Estado(hijostring)
        return h1
    def __str__(self):
        return self.cadena[:3]+'\n'+self.cadena[3:6]+'\n'+self.cadena[6:9]+'\n'+self.cadena[9:]+'\n'
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

def bfs(e_inicial):
    por_visitar = []
    visitados = {}

    por_visitar.append((e_inicial,0))
    e = e_inicial
    e_final = Estado('123456789AB0')
    while e != e_final:
        if not por_visitar:  # Verificar si por_visitar está vacío
            break
        e, padre = por_visitar.pop(0)
        if e.cadena not in visitados:
            visitados[e.cadena] = padre
            for v in e.hijos():
                por_visitar.append((v,e.cadena))
    ruta = []
    if e == e_final:  # Añadir solo si encontramos la solución
        padre = visitados[e.cadena]
        while padre != 0:
            ruta.append(padre)
            padre = visitados[padre]
    return ruta

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    e = Estado('1A435B067892')  # Estado inicial modificado
    ruta = bfs(e)
    print(ruta)
