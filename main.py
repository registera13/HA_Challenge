import numpy as np
import pandas as pd
import os


class FileIO(object):
    def __init__(self, dataDir=None):
        self.dataDir = dataDir
        self.tsvFiles = None
        pass

    def listDataFromDir(self):
        self.tsvFiles = [f for f in os.listdir(self.dataDir) if f.endswith('.tsv')]
        return self.tsvFiles

    def convertToPanda(self):
        for files in self.tsvFiles:
            pd.read_csv(files, sep='\t', lineterminator='\r')


class Hg19(object):
    def __init__(self, exon=None, genes=None):
        self.exon = pd.read_csv('Data Files/hg19_exon_locations.tsv', sep='\t', header=None)
        self.genes = pd.read_csv('Data Files/hg19_genes.tsv', sep='\t', header=None)

    def sort_gene(self,ref):

        if 2 and 3 in range(3, 9):
            print(" %s is in the range")
        else:
            print("The number is outside the given range.")
        return


    def sort_exon(self,df):
        for index, row in df.iterrows():

            if row[1] and row[2] in range():


if __name__ == "__main__":
    data = pd.read_csv('Data Files/hg5_min_6_min_7.bed', sep='\t', header=None)
    test=Hg19()
    test.sort_exon(data)



