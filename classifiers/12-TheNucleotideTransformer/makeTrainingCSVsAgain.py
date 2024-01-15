from glob import glob
from collections import defaultdict
from Bio import SeqIO
import os
for l in glob('*fasta'):
    base = os.path.basename(l)
    with open(base.replace('.fasta', '.csv'), 'w') as out, open(base.replace('.fasta', '_id_dict.csv'), 'w') as out2:
        counter = 0
        taxid_to_counter = {}
        #if out.name != '16S_v04_final.csv_Taxonomies.CountedFams.txt_thirty_subset_9.csv':
        #    continue
        # first, we have to count the 'rare' sequences
        taxid_counter = defaultdict(int)
        for s in SeqIO.parse(l, 'fasta'):
            taxid = s.description.split(' ')[1]
            taxid_counter[taxid] += 1
        

        out.write('sequence,label\n')
        for s in SeqIO.parse(l, 'fasta'):
            taxid = s.description.split(' ')[1]
            if taxid not in taxid_to_counter:
                num = counter
                taxid_to_counter[taxid] = num
                out2.write(f'{taxid}\t{num}\n')
                counter += 1
            else:
                num = taxid_to_counter[taxid]
            #if num > 500:
            #    break
            # have to break this up into pieces of length 100
            
            # if this taxid appears < 10 times, do the following
            # ten times
            if taxid_counter[taxid] < 10:
                repeats = 9
            else:
                repeats = 1
            repeat_counter = 0
            while repeat_counter < repeats:
                chunks, chunk_size = len(str(s.seq)), 101
                for i in range(0, chunks, chunk_size):
                    piece = str(s.seq)[i:i+chunk_size]
                    if len(piece) < 101:
                        # pad to 101
                        diff = 101 - len(piece)
                        piece += diff * 'N'
                    out.write(f'{piece},{num}\n')
                repeat_counter += 1
            #out.write(f'{str(s.seq)},{num}\n')
