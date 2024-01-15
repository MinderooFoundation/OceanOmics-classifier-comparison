from glob import glob
import os
from collections import defaultdict

with open('all_together.csv', 'w') as out1:
    for x in glob('*FIXED.csv'):
        query, subject = x.split('_vs_')
        print(query, subject)
        fh = open(x)
        header = fh.readline()
        asv_dict = defaultdict(list)
        with open('TEMP.txt', 'w') as out:
            for line in fh:
                ll = line.rstrip().split(',')
                asv = ll[0]
                asv_dict[asv].append(ll)
            for a in asv_dict:
                # [['ASV_1', '0', 'ACCAAGGCAGACCATGTTAAACACCCCAAAACAAAGGACCAAACCAAATGACCCCTGCCCTAATGTCTTTGGTTGGGGCGACCGCGGGGAAACACAAAACC', '40502', '0.19451705'], ['ASV_1', '1', 'CCCACGTGGAACGAGAACACCTCCTCTCACAACCAAGAGCTCCCGCTCTAATAAACAGAAATTCTGACCAATAAGATCCGGCAAGGCCGATCAACGGACCG', '40502', '0.4789651']]
                # find the highest score for this piece
                biggest_sc = 0
                for x in asv_dict[a]:
                    if float(x[-1]) > biggest_sc:
                        biggest_sc = float(x[-1])
                        biggest_taxid = x[3]
                #print(a, biggest_sc, biggest_taxid)
                out.write(f'{a}\t{biggest_sc}\t{biggest_taxid}\n')
        os.popen('taxonkit --data-dir . lineage -i 3 TEMP.txt | taxonkit reformat --data-dir . -i 4 > TEMP_LINEAGE.txt').read()
        break

        # Type    Query   Subject domain  phylum  class   order   family  genus   species OTU
        #Metabuli        KWest_16S_PooledTrue.fa 12s_v010_final.fasta_ref.fasta  Eukaryota       Chordata        Actinopteri     NA      Siganidae       Siganus Siganus canaliculatus   ASV_10
