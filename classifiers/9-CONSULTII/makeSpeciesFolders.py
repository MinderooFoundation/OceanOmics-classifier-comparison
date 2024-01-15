from glob import glob
import os
from Bio import SeqIO

for l in glob('../*fasta'):
    if 'c01' in l: continue
    base = os.path.basename(l)
    outfolder = base + '_perSpecies'
    if not os.path.isdir(outfolder):
        os.mkdir(outfolder)

    for s in SeqIO.parse(l, 'fasta'):
        taxid = s.description.split(' ')[1]
        with open(outfolder + '/' + f'{taxid}.fasta' , 'a') as out:
            out.write(s.format('fasta'))
