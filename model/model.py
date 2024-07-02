import copy

from database.DAO import DAO
import networkx as nx
from geopy import distance


class Model:
    def __init__(self):
        self._bestdTot = 0
        self._bestComp = []
        self.idMap = {}
        self.graph = nx.Graph()

    def getYears(self):
        return DAO.getYears()

    def getShapes(self, year):
        return DAO.getShapes(year)

    def getGraphDetails(self):
        result = [f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi."]
        for node in self.graph:
            score = 0
            for v in self.graph.neighbors(node):
                score += self.graph[node][v]['weight']
            result.append(f"Nodo {node.id}, somma pesi sugli archi: {score}")
        return result

    def get_nodes(self):
        return self.graph.nodes

    def buildGraph(self, year, shape):
        self.graph.clear()
        nodes = DAO.getStates()
        self.graph.add_nodes_from(nodes)
        for node in self.graph.nodes:
            self.idMap[node.id] = node
        edges = DAO.getEdges(year, shape, self.idMap)
        for edge in edges:
            if self.graph.has_edge(edge.state1, edge.state2):
                pass
            else:
                self.graph.add_edge(edge.state1, edge.state2, weight=edge.weight)
        return True

    def getPath(self):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = []
        for node in self.graph.nodes:
            parziale.append(node)
            self._ricorsionev2(parziale)
            parziale.pop()
        return self._bestComp

    def _ricorsionev2(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache
        if self._getScore(parziale) > self._bestdTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        listaVicini = []
        # per ogni vicino dell'ultimo nodo del percorso:
        for v in self.graph.neighbors(parziale[-1]):
            edgeV = self.graph[parziale[-1]][v]["weight"]  # peso arco che mando in ricorsione
            listaVicini.append((v, edgeV))
        if len(parziale) == 1:
            for v1 in listaVicini:
                # per ogni vicino trovato, se il nodo non è nella soluzione parziale, e il peso del suo predecessore è maggiore del suo
                if v1[0] not in parziale:
                    parziale.append(v1[0])  # aggiungo il nodo, faccio la ricorsione e poi la return, perchè gli altri sono sicuro peggiori ( lista ordinata )
                    self._ricorsionev2(parziale)
                    parziale.pop()
        else:
            for v1 in listaVicini:
                # per ogni vicino trovato, se il nodo non è nella soluzione parziale, e il peso del suo predecessore è maggiore del suo
                if (v1[0] not in parziale and
                        self.graph[parziale[-2]][parziale[-1]]["weight"] < v1[1]):
                    parziale.append(v1[0])  # aggiungo il nodo, faccio la ricorsione e poi la return, perchè gli altri sono sicuro peggiori ( lista ordinata )
                    self._ricorsionev2(parziale)
                    parziale.pop()

    def _getScore(self, nodes):
        score = 0
        for i in range(0, len(nodes)-1):
            score += distance.geodesic((nodes[i].Lat, nodes[i].Lng), (nodes[i+1].Lat, nodes[i+1].Lng)).km
        return score

    def getPathDetails(self):
        result = []
        for i in range(0, len(self._bestComp) - 1):
            result.append((self._bestComp[i], self._bestComp[i+1], self.graph[self._bestComp[i]][self._bestComp[i+1]]['weight'], self._getScore([self._bestComp[i], self._bestComp[i+1]])))
        return result

