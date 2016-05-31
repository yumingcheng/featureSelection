#-*-coding:utf-8-*
import os
import sys
import math
from wordSeg import wordSeg

class OddsRatio:
    '''特征选择算法之(OddsRatio)'''
    def __init__(self):
        self.sumClass = 2 
        self.dicClassFre = dict().fromkeys([i for i in range(sumClass)],0)
        self.dicClassWord = dict([i,{}]for i in range(sumClass)) 
        self.wordAnalyse = {} #{'中国':[[10,20,10,18],[],[]]}
        self.wSeg = wordSeg()

    def addtrainingdatafilePos(self,dataPath):
        f = open(dataPath)
        for line in f:
            self.dicClassFre[0] += 1
            self.__updateDic(self.wSeg.tokenStrem(line),0)
        f.close()

    def addtrainingdatafileNeg(self,dataPath):
        f = open(dataPath)
        for line in f:
            self.dicClassFre[1] += 1
            self.__updateDic(self.wSeg.tokenStrem(line),1)
        f.close()


    def __updateDic(self,wordlist,classIndex):
        for word in wordlist:
            self.dicClassWord[classIndex][word] = 1
            if word not in self.wordAnalyse:
                self.wordAnalyse[word] = [0 for i in range(self.sumClass+1)]
            self.wordAnalyse[word][classIndex] += 1
            self.wordAnalyse[word][self.sumClass] += 1
            
    def __calculatePos(self,values):
        rdSum = 0.0
        numerator = (values[0]*1.0/self.dicClassFre[0])*(1 - values[1]*1.0/self.dicClassFre[1]);
        denominator = (values[1]*1.0/self.dicClassFre[1])*(1 - values[0]*1.0/self.dicClassFre[0]);
        if numerator == 0.0 :
           numerator = 3 
        elif denominator==0.0:
           denominator = 3 
        return math.log(numerator/denominator,2) 
    
    def __calculateNeg(self,values):
        rdSum = 0.0
        numerator = (values[1]*1.0/self.dicClassFre[1])*(1 - values[0]*1.0/self.dicClassFre[0]);
        denominator = (values[0]*1.0/self.dicClassFre[0])*(1 - values[1]*1.0/self.dicClassFre[1]);
        if numerator == 0.0 :
           numerator = 3 
        elif denominator==0.0:
           denominator = 3 
        return math.log(numerator/denominator,2) 


    def OutputTrainFilePos(self,filepath):
        endList = []
        for key,values in self.wordAnalyse.items():
            if values[-1] > 2 and key in self.dicClassWord[0]: 
#            if values[-1] > 2: 
                endList.append([key,self.__calculatePos(values),values])
        endList.sort(lambda x,y: cmp(x[1],y[1]),reverse=True)
        fout = open(filepath,"w")
        for attr in endList:
            fout.write(attr[0].encode('UTF-8')+"\t")
            fout.write(str(attr[1])+"\t"+str(attr[2])+"\n")
        fout.close()
        print self.dicClassFre
        return endList            

    def OutputTrainFileNeg(self,filepath):
        endList = []
        for key,values in self.wordAnalyse.items():
            if values[-1] > 2 and key in self.dicClassWord[1]: 
#            if values[-1] > 2: 
                endList.append([key,self.__calculateNeg(values),values])
        endList.sort(lambda x,y: cmp(x[1],y[1]),reverse=True)
        fout = open(filepath,"w")
        for attr in endList:
            fout.write(attr[0].encode('UTF-8')+"\t")
            fout.write(str(attr[1])+"\t"+str(attr[2])+"\n")
        fout.close()
        return endList            
                
if __name__ == "__main__":
    chi = OddsRatio()
    chi.addtrainingdatafilePos("./merge1.txt") # 添加正面数据
    chi.addtrainingdatafileNeg("./merge2.txt") # 添加负面数据
    chi.OutputTrainFilePos("./mo1.txt")             
    chi.OutputTrainFileNeg("./mo2.txt")

