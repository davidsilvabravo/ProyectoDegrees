class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    # constructor de la pila
    def __init__(self):
        self.frontier = [] # lista vacía

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
    # Este método está diseñado para verificar si un estado está presente en la frontera (frontier)
    # La frontera es típicamente una colección de nodos que aún no se han explorado, en algoritmos de búsqueda
    # devuelve true o false
        return any(node.state == state for node in self.frontier)

    def empty(self):
    # devuelve true o false
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1] # obtiene el último nodo de la pila, y lo asigna a node
            self.frontier = self.frontier[:-1] # elimina el último nodo de la pila
            return node # devuelve el nodo eliminado


class QueueFrontier(StackFrontier):
# hereda de StackFrontier

    def remove(self):
    # remove sobreescrito, para que el nodo que se elimine sea el primero de la cola
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] # obtiene el primer nodo de la cola, y lo asigna a node
            self.frontier = self.frontier[1:] # elimina el primer nodo de la cola
            return node # devuelve el nodo eliminado
