import unittest
from blosumak import cluster_distance_filter
from time import time
from Bio.SeqIO.FastaIO import SimpleFastaParser

class TestClusterDistanceFilter(unittest.TestCase):
    def test_basic_functionality(self):
        dummy = '/home/chubak/INSbttTARAAPEI-83.fa'
        
        with open(dummy, "r") as fr:
            seqs = list(SimpleFastaParser(fr))

        print(f'Operating on {len(seqs)} lines.')
        start = time()
        clusters = cluster_distance_filter(seqs)

        print(clusters)

        end = time()
        print(f'Total time: {end-start}')
        

if __name__ == '__main__':
    unittest.main()
