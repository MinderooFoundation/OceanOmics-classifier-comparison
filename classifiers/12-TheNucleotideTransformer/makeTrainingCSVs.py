from glob import glob
from Bio import SeqIO
import os
counter = 0
taxid_to_counter = {}
for l in glob('../*fasta'):
    base = os.path.basename(l)
    with open(base.replace('.fasta', '.csv'), 'w') as out, open(base.replace('.fasta', '_id_dict.csv'), 'w') as out2:
        if out.name != '16S_v04_final.csv_Taxonomies.CountedFams.txt_thirty_subset_9.csv':
            continue
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
            chunks, chunk_size = len(str(s.seq)), 101
            for i in range(0, chunks, chunk_size):
                piece = str(s.seq)[i:i+chunk_size]
                if len(piece) < 101:
                    # pad to 101
                    diff = 101 - len(piece)
                    piece += diff * 'N'
                out.write(f'{piece},{num}\n')
            #out.write(f'{str(s.seq)},{num}\n')
