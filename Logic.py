from lab_04.GA import GA


def run(probParam=None, generationParam=None):
    if probParam['option']==1:
        probParam['function'] = Quality
    else:
        probParam['function'] = QualitySE

    runGenerations(probParam, generationParam)


def runGenerations(probParam=None, generationParam=None):
    ga = GA(generationParam, probParam);
    ga.initialization()
    ga.evaluation()

    g = -1
    while (g < generationParam['noGen']):
        g += 1;
        # ga.oneGenerationRand()
        ga.oneGenerationElitism()
        #ga.oneGenerationSteedyState()

        print(str(g)+" "+str(ga.bestChromosome().fitness));

    cost =int(ga.bestChromosome().fitness);
    path = ga.bestChromosome().repres;
    strpath = '';

    if probParam['option']==1:
        path.insert(0, 0);
        for i in range(len(path)):
            strpath += str(path[i] + 1);
            if i != len(path) - 1:
                strpath += ','
        print(len(path))
    else:
        i=0
        t=1
        strpath+=str(probParam['startcity']+1)+',';
        while (path[i]!=probParam['endcity']):
            if path[i]!=probParam['startcity']:
                strpath+=str(path[i]+1)+','
                t+=1
            i+=1;
        t+=1
        strpath+=str(path[i]+1);
        print(t)

    print(strpath);
    print(cost)


def Quality(path, probParam):
    matirx = probParam['matrix'];
    fit = 0.0
    i = 0;
    for j in range(len(path)):
        fit += matirx[i][path[j]];
        i = path[j];
    fit += matirx[i][0];
    return fit


def QualitySE(path, probParam):
    matrix = probParam['matrix'];
    fit = 0.0
    i = probParam['startcity'];

    j = 0
    while (path[j] != probParam['endcity']):
        fit += matrix[i][path[j]]
        i = path[j];
        j+=1
    fit += matrix[i][probParam['endcity']]
    return fit

