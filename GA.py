from random import randint,random

from lab_04.Chromosome import Chromosome


class GA:
    def __init__(self, param=None, probParam=None):
        self.__param = param;
        self.__probParam = probParam;
        self.__population = []

    @property
    def population(self):
        return self.__population;

    def initialization(self):
        for i in range(self.__param['popSize']):
            c = Chromosome(self.__probParam);
            self.__population.append(c);

    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__probParam['function'](c.repres, self.__probParam)

    def selection(self):
        pos1 = randint(0, self.__param['popSize'] - 1)
        pos2 = randint(0, self.__param['popSize'] - 1)
        if self.__population[pos1].fitness < self.__population[pos2].fitness:
            return pos1
        else:
            return pos2

    def roulette_wheel_pop(self,probabilities):
        r=random();
        for i in range(len(probabilities)):
            if r<=probabilities[i]:
                return i

    def bestChromosome(self):
        best = self.__population[0];
        for c in self.__population:
            if c.fitness < best.fitness:
                best = c
        return best

    def worstChromosome(self):
        best = self.__population[0];
        for c in self.__population:
            if c.fitness > best.fitness:
                best = c
        return best

    def oneGenerationElitism(self):
        newPop = [self.bestChromosome()];
        probabilities=self.get_probability_list();
        #print(probabilities)
        #print(self.roulette_wheel_pop(probabilities))
        for i in range(self.__param['popSize'] - 1):
            p1 = self.__population[self.roulette_wheel_pop(probabilities)];
            p2 = self.__population[self.roulette_wheel_pop(probabilities)];
            offspring = p1.crossover(p2);
            offspring.mutation();
            newPop.append(offspring);
        self.__population = newPop;
        self.evaluation();

    def oneGenerationSteedyState(self):
        for i in range(self.__param['popSize']):
            p1 = self.__population[self.selection()];
            p2 = self.__population[self.selection()];
            offspring = p1.crossover(p2);
            offspring.mutation();
            offspring.fitness = self.__probParam['function'](offspring.repres, self.__probParam);
            worst = self.worstChromosome();
            if (offspring.fitness < worst.fitness):
                worst = offspring
            self.__population[i] = worst

    def oneGenerationRand(self):
        newPop = []
        for i in range(self.__param['popSize']):
            p1 = self.__population[self.selection()];
            p2 = self.__population[self.selection()];
            off = p1.crossover(p2)
            off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def get_probability_list(self):
        fitness = [self.__population[i].fitness for i in range(len(self.__population))];
        total_fit=float(sum(fitness))
        relative_fitness=[1-f/total_fit for f in fitness]
        probabilities = [sum(relative_fitness[:i+1])
                         for i in range(len(relative_fitness))];
        return probabilities