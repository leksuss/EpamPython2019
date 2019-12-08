"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной
Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)
"""


class Graph:
    def __new__(cls, E):
        if not len(E):
            return {}
        return object.__new__(cls)

    def __init__(self, E):
        self.E = E
        self.queue = None
        self.visited = {k: False for k in self.E.keys()}
        self.vertex = next(iter(self.E))

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue is None:
            self.queue = [self.vertex]
            self.visited[self.vertex] = True
        if len(self.queue):
            for child_vertex in self.E[self.queue[0]]:
                if not self.visited[child_vertex]:
                    self.visited[child_vertex] = True
                    self.queue.append(child_vertex)
            return self.queue.pop(0)
        else:
            raise StopIteration


E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}

graph = Graph(E)

for i in graph:
    print(i)
