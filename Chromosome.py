from random import randint
def generateRandomPermutation(n):
    perm=[i+1 for i in range(n)];
    pos1=randint(0,n-1);
    pos2=randint(0,n-1);
    perm[pos1],perm[pos2]=perm[pos2],perm[pos1]
    return perm

class Chromosome:
    def __init__(self,probParam=None):
        self.__probParam=probParam;
        self.__fitness=0.0;
        self.__repr=generateRandomPermutation(self.__probParam['noNodes']-1)

        if (self.__probParam['option']==2):
            pos=randint(0,self.__probParam['noNodes']);
            self.__repr.insert(pos,0);
    @property
    def repres(self):
        return self.__repr

    @property
    def fitness(self):
        return self.__fitness

    @repres.setter
    def repres(self,l=[]):
        self.__repr=l

    @fitness.setter
    def fitness(self,fit=0):
        self.__fitness=fit

    def __str__(self):
        return "fit:"+str(self.__fitness)+" repres:"+str(self.__repr);

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__fitness==other.__fitness and self.__repr==other.__repr;

    def crossover(self,c):
        #num=[randint(0,1) for i in range(len(self.__repr))]
        #offspring.__repr=[self.__repr[i] if (num[i]) else c.__repres[i] for i in range(len(self.__repr))];

        pos1=randint(0,self.__probParam['noNodes']-1)
        pos2=randint(0,self.__probParam['noNodes']-1)
        if (pos2<pos1):
            pos1,pos2=pos2,pos1
        k=0
        newrepres=self.__repr[pos1:pos2]
        for el in c.__repr[pos2:]+c.__repr[:pos2]:
            if (el not in newrepres):
                if(len(newrepres)<self.__probParam['noNodes']-pos1):
                    newrepres.append(el)
                else:
                    newrepres.insert(k,el)
                    k+=1;

        offspring=Chromosome(self.__probParam);
        offspring.repres=newrepres;
        return offspring

    def mutation(self):
        #pos=randint(0,len(self.__repr));
        #self.__repr[pos]=randint(0,self.__probParam['']);

        pos1=randint(0,self.__probParam['noNodes']-2)
        pos2=randint(0,self.__probParam['noNodes']-2)
        if (pos2<pos1):
            pos1,pos2=pos2,pos1
        el=self.__repr[pos2]
        del self.__repr[pos2]
        self.__repr.insert(pos1+1,el)

    def testcrosover():
        # seed(5)
        problParam = {'noNodes': 10}
        c1 = Chromosome(problParam)
        c2 = Chromosome(problParam)
        print('parent1: ', c1)
        print('parent2: ', c2)
        off = c1.crossover(c2)
        print('offspring: ', off)

    def testmutation():
        problParam = {'noNodes': 10}
        c1 = Chromosome(problParam)
        print('before mutation: ', c1)
        c1.mutation()
        print('after mutation: ', c1)
