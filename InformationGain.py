#-*-coding:utf-8-*
import os
import sys
import math
from wordSeg import wordSeg

class InformationGain:
    '''特征选择算法之信息增益(InformationGain)'''
    def __init__(self,sumClass):
        self.sumClass = sumClass
        self.dicClass = dict().fromkeys([i for i in range(sumClass)],0)
        self.wordAnalyse = {} #{'中国':[[10,20,10,18],[],[]]}
        self.wSeg = wordSeg()

    def addtrainingdatafile(self,dataPath,classIndex):
        print classIndex,dataPath
        f = open(dataPath)
        for line in f:
            self.dicClass[classIndex] += 1
            self.__updateDic(self.wSeg.tokenStrem(line),classIndex)

    def __updateDic(self,wordlist,classIndex):
        for word in wordlist:
            if word not in self.wordAnalyse:
                self.wordAnalyse[word] = [0 for i in range(self.sumClass+1)]
            self.wordAnalyse[word][classIndex] += 1
            self.wordAnalyse[word][self.sumClass] += 1
            
    def __calculateFirst(self):
        sumAllDoc = (lambda info:sum(info.values()))(self.dicClass)
        rFirst = 0.0
        for i in range(self.sumClass):
            rFirst += self.dicClass[i]*1.0/sumAllDoc*math.log(self.dicClass[i]*1.0/sumAllDoc,2)
        return rFirst*-1.0

    def __calculate(self,values):
        dSumPt = 0.0;
        __dSumPt = 0.0;
        sumAllDoc = (lambda info:sum(info.values()))(self.dicClass)
        pt = values[-1]
        __pt = sumAllDoc - pt
        for i in range(len(values)-1):
            if values[i] != 0:
                dSumPt += values[i]*1.0/pt*math.log(values[i]*1.0/pt,2) 
                __dSumPt += (self.dicClass[i]-values[i])*1.0/__pt*math.log((self.dicClass[i]-values[i])*1.0/__pt,2) 

        return  (pt*1.0/sumAllDoc * dSumPt + __pt*1.0/sumAllDoc*__dSumPt)

    def OutputTrainFile(self,filepath,classIndex):
        endList = []
        firstSum = self.__calculateFirst()
        for key,values in self.wordAnalyse.items():
            if values[-1] > 2: 
                endList.append([key,self.__calculate(values)+firstSum,values])
        endList.sort(lambda x,y: cmp(x[1],y[1]),reverse=True)
        fout = open(filepath,"w")
        for attr in endList:
            fout.write(attr[0].encode('UTF-8')+"\t")
            fout.write(str(attr[1])+"\t"+str(attr[2])+"\n")
        fout.close()
        print self.dicClass
#        for key,values in self.wordAnalyse.items():
#            print key,values

        return endList            
                
if __name__ == "__main__":
    chi = InformationGain(4)
    chi.addtrainingdatafile("./merge1.txt",0)
    chi.addtrainingdatafile("./merge2.txt",1)
    chi.addtrainingdatafile("./merge3.txt",2)
    chi.addtrainingdatafile("./merge4.txt",3)
    chi.OutputTrainFile("./m.txt",0)

