import operator
import time

import matplotlib.pyplot as plt

class Graph(object):
    def __init__(self,cost_matrix: list,rank: int):
        """
        :param cost_matrix:
        :param rank:rank of the cost matrix
        """
        self.matrix = cost_matrix;
        self.rank = rank
        self.pheromone = [[1/(rank*rank) for j in range(rank)] for i in range(rank)]

class ACO(object):
    def __init__(self, ant_count: int, generations: int, alpha: float, beta: float, rho: float, q: int, strategy: int, points):

        """
        :param ant_count:
        :param generations:
        :param alpha: relative importance of pheromone
        :param beta: relative information of heuristic information
        :param rho: pheromone residual coefficient
        :param q: pheromone intensity
        :param strategy: pheromone update strategy. 0-ant-cycle,1-ant-quality,2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy
        self.points = points

    def _update_pheromone(self,graph: Graph,ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j]*= self.rho;
                for ant in ants:
                    graph.pheromone[i][j]+= ant.pheromone_delta[i][j]

    def solve(self, graph: Graph):
        """
        :param graph:
        :return:
        """
        best_cost = float('inf');
        best_solution = []

        #ploting...
        #loading the plot
        x = []
        y = []
        for point in self.points:
            x.append(point[0])
            y.append(point[1])
        y = list(map(operator.sub, [max(y) for i in range(len(self.points))], y))

        # Set up plot
        plt.ion()
        figure, ax = plt.subplots()
        # Autoscale on unknown axis and known lims on the other
        ax.set_autoscaley_on(True)
        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)

        #starting generations
        for gen in range(self.generations):
            ants = [_Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                for i in range(graph.rank-1):
                    ant._select_next()
                ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]]
                ant.total_cost += graph.matrix[ant.tabu[0]][0]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = []+ant.tabu+[0]
                #update pheromone
                ant._update_pheromone_delta()
            self._update_pheromone(graph, ants)
            print('#{} ,cost: {}'.format(gen, best_cost))


            #ploting after a generation
            ax.clear()
            plt.plot(x, y, 'o')
            plt.plot(self.points[0][0],self.points[0][1],'-gD')

            for t in range(1, len(best_solution)):
                i = best_solution[t - 1]
                j = best_solution[t]
                plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

            figure.canvas.flush_events()
            figure.canvas.draw()
            time.sleep(0.1)

        return best_solution,best_cost

import random

class _Ant(object):
    def __init__(self,aco: ACO,graph: Graph):
        self.colony = aco
        self.graph = graph
        self.total_cost=0.0
        self.tabu = []
        self.pheromone_delta = [] #local increase of pheromone
        self.allowed = [i for i in range(graph.rank)] #nodes which are allowed for the next selection
        #heuristic information
        self.eta = [[0 if i == j else 1/graph.matrix[i][j] for j in range(graph.rank)] for i in range(graph.rank)]
        start = 0 #random.randint(0,graph.rank-1) #start from any node
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def _select_next(self):
        denominator = 0;
        for i in self.allowed:
            denominator+= self.graph.pheromone[self.current][i]**self.colony.alpha * self.eta[self.current][i]**self.colony.beta
        probabilities=[0 for i in range(self.graph.rank)] #probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i) #test if allowed list contains i
                probabilities[i]=self.graph.pheromone[self.current][i]**self.colony.alpha *\
                                 self.eta[self.current][i] ** self.colony.beta/denominator
            except ValueError:
                pass #do nothing

        #select next node by probability roulette
        selected=0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected

    def _update_pheromone_delta(self):
        self.pheromone_delta=[[0 for j in range(self.graph.rank)]for i in range(self.graph.rank)]
        for t in range(1,len(self.tabu)):
            i=self.tabu[t-1]
            j=self.tabu[t]
            if self.colony.update_strategy == 1: #ant-quality system
                self.pheromone_delta[i][j]=self.colony.Q
            if self.colony.update_strategy == 2:  #ant denisty system
                self.pheromone_delta[i][j] = self.colony.Q/self.graph.matrix[i][j]
            else: #ant-cycle system
                self.pheromone_delta[i][j] = self.colony.Q/self.total_cost