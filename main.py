from Lab_02.date import citeste_matrice
from lab_04.Logic import run,QualitySE
if __name__ == '__main__':
    fileName='berlin.in'
    matrix=citeste_matrice(fileName);
    n1=2;n2=4;
    probParam={'matrix':matrix,'noNodes':len(matrix),'startcity':n1-1,'endcity':n2-1};
    generationParam = {'popSize': 500, 'noGen': 1000};
    probParam['option']=1
    run(probParam,generationParam);
    probParam['option']=2
    if (fileName=="easy.in"):
        run(probParam,generationParam);
