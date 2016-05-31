#-*-coding:utf-8-*
import os
import sys
import math
from wordSeg import wordSeg

class CHI:
    '''特征选择算法之开方检验(CHI)'''
    def __init__(self,sumClass):
#        self.filename = filename
        self.sumClass = sumClass
        self.dicClassFre = dict().fromkeys([i for i in range(sumClass)],0)
        self.dicClassWord = dict([i,{}]for i in range(sumClass)) 
        self.wordAnalyse = {} #{'中国':[[10,20,10,18],[],[]]}
        self.wSeg = wordSeg()

    def addtrainingdatafile(self,dataPath,classIndex):
        print classIndex,dataPath
        f = open(dataPath)
        for line in f:
            self.dicClassFre[classIndex] += 1
            self.__updateDic(self.wSeg.tokenStrem(line),classIndex)

    def __updateDic(self,wordlist,classIndex):
        for word in wordlist:
            self.dicClassWord[classIndex][word] = 1
            if word not in self.wordAnalyse:
                self.wordAnalyse[word] = [[0,0,0,0,0] for i in range(self.sumClass)]
            for i in range(self.sumClass):
                if classIndex == i:
                    self.wordAnalyse[word][classIndex][0] += 1
                    self.wordAnalyse[word][classIndex][2] = self.dicClassFre[classIndex] - self.wordAnalyse[word][classIndex][0]
                else:
                    self.wordAnalyse[word][i][1] += 1
                
    def __calculate(self,A,B,C,D):
        sumAllDoc = (lambda info:sum(info.values()))(self.dicClassFre)
        numerator = sumAllDoc*pow((A*D - B*C),2)
        denominator = (A+C)*(A+B)*(B+D)*(C+D)
        return numerator/denominator

    def OutputTrainFile(self,filepath,classIndex):
        sumAllDoc = (lambda info:sum(info.values()))(self.dicClassFre)
        endList = []
        for key,values in self.wordAnalyse.items():
            if key in self.dicClassWord[classIndex]:
                A = values[classIndex][0]
                B = values[classIndex][1]
                C = self.dicClassFre[classIndex] - values[classIndex][0]
                self.wordAnalyse[key][classIndex][2]  = C
                D = sumAllDoc - A - B -C
                self.wordAnalyse[key][classIndex][3]  = D            
                endList.append([key,self.__calculate(A,B,C,D),values])
        endList.sort(lambda x,y: cmp(x[1],y[1]),reverse=True)
        fout = open(filepath,"w")
        for attr in  endList:
            fout.write(attr[0].encode('UTF-8')+"\t")
            fout.write(str(attr[1])+"\t"+str(attr[2])+"\n")
        fout.close()

#        for key,values in self.dicClassWord[classIndex].items():
#            print key.encode('UTF-8'),values
#        print "======================="

        return endList            
                
if __name__ == "__main__":
    chi = CHI(4)
    chi.addtrainingdatafile("./merge1.txt",0)
    chi.addtrainingdatafile("./merge2.txt",1)
    chi.addtrainingdatafile("./merge3.txt",2)
    chi.addtrainingdatafile("./merge4.txt",3)
    chi.OutputTrainFile("./m1.txt",0)
    chi.OutputTrainFile("./m2.txt",1)
    chi.OutputTrainFile("./m3.txt",2)
    chi.OutputTrainFile("./m4.txt",3)


