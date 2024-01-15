from glob import glob
import os

from Bio import SeqIO

for l in glob('../*fa'):
    print(l)
    base = os.path.basename(l)
    with open(base + '.sub.fake.fq', 'w') as out:
        for s in SeqIO.parse(l, 'fasta'):
            #s.letter_annotations["phred_quality"] = [40] * len(s)

            chunks, chunk_size = len(str(s.seq)), 101
            for i in range(0, chunks, chunk_size):
                piece = s[i:i+chunk_size]
                piece.id = f'{piece.id}_{i}'
                if len(piece) < 101:
                    piece.seq += (101-len(piece)) * 'N'
                piece.letter_annotations['phred_quality'] = len(piece) * [40]
                out.write(piece.format('fastq'))
