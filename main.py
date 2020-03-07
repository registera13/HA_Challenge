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
        self.exon = exon
        self.genes = genes

    def read_data(self):
        self.exon = pd.read_csv('Data Files/hg19_exon_locations.tsv', sep='\t', header=None)
        self.genes = pd.read_csv('Data Files/hg19_genes.tsv', sep='\t', header=None)

    def sort_gene(self):
        start
        pass

    def sort_exon(self):
        pass


if __name__ == "__main__":
    hr19 = Hg19()
    hr19.read_data()





