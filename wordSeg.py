#-*-coding:utf-8-*
import os
import sys

class wordSeg:
    '''简易分词'''
    def __init__(self,dicpath='./webdict_with_freq.txt'):
        self.wordDic = {}
        self.__addWordDic(dicpath)        

    def __addWordDic(self,dicpath):
        f = open(dicpath)
        for line in f:
            line =  line.replace('\n',"")
            analyse = line.split()
#            print '%s/%s'%(analyse[0],analyse[1])
            if analyse[0].decode('UTF-8') in self.wordDic:
                continue
            else :
                self.wordDic[analyse[0].decode('UTF-8')] = int(analyse[1])

    def tokenStrem(self,Sententce):
#        print self.wordDic
        extDocument = [] 
        try:
#            document = Sententce.decode('UTF-8','ignore')
            document = Sententce.decode('UTF-8',)
        except:
            return []
        length = len(document)
        curIndex = 0 
        j = 0
        while curIndex < length:
            endIndex = 1
            maxIndex = 1
            while endIndex < 8 and endIndex+curIndex <= length:
                tempString = document[curIndex:curIndex+endIndex]
                if (tempString in self.wordDic) and (len(tempString) is not 1):
#                    print "{%s}"%(extDocument)
                    extDocument.append(tempString)
                    if endIndex > maxIndex:
                        maxIndex = endIndex
                endIndex += 1
            curIndex += maxIndex
        extDocument = list(set(extDocument))
        return extDocument 
        
if __name__  == "__main__":
    wordSeg = wordSeg()
    for word in  wordSeg.tokenStrem("腌法腌制品腌法腌制品"):
        print '%s '%(word),

