from glob import glob
from Bio import SeqIO
import os
counter = 0
taxid_to_counter = {}
for l in glob('*fa'):
    base = os.path.basename(l)
    with open(base + '.csv', 'w') as out:
        out.write('name,sequence\n')
        for s in SeqIO.parse(l, 'fasta'):
            chunks, chunk_size = len(str(s.seq)), 101
            for i in range(0, chunks, chunk_size):
                piece = str(s.seq)[i:i+chunk_size]
                if len(piece) < 101:
                    # pad to 101
                    diff = 101 - len(piece)
                    piece += diff * 'N'
                out.write(f'{s.id},{piece}\n')
            #out.write(f'{str(s.seq)},{num}\n')
