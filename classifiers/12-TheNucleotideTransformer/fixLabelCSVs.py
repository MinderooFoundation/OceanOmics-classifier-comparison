from glob import glob
from Bio import SeqIO
import os
counter = 0
taxid_to_counter = {}
for l in glob('*fa'):
    for x in glob(l + '*_vs_*'):
        with open(x + '_FIXED.csv', 'w') as out:
            base = os.path.basename(l)
            #with open(base + '.csv', 'w') as out:
                #out.write('sequence\n')
            print(l, x)
            seq_chunks = []
            for s in SeqIO.parse(l, 'fasta'):
                chunks, chunk_size = len(str(s.seq)), 101
                for i in range(0, chunks, chunk_size):
                    piece = str(s.seq)[i:i+chunk_size]
                    if len(piece) < 101:
                        # pad to 101
                        diff = 101 - len(piece)
                        piece += diff * 'N'
                    seq_chunks.append( (s.id, piece) )
            fh = open(x)
            out.write('ASV,' + fh.readline())
            for seq_c, line in zip(seq_chunks, fh):

                assert seq_c[1] == line.split(',')[1]
                #print(seq_c[0], line)
                out.write(f'{seq_c[0]},{line}')
