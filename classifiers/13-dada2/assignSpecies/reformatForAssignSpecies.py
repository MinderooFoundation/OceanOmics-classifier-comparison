import os
from glob import glob
from Bio import SeqIO
'''(Required). The path to the reference fasta file, or an R connection. Can be compressed. This reference fasta file should be formatted so that the id lines correspond to the genus-species of the associated sequence:

    >SeqID genus species ACGAATGTGAAGTAA......'''
for g in glob('../../*fasta'):
    basename = os.path.basename(g).replace('.fasta','')
    with open(basename + 'reformatted_for_species.fasta', 'w') as out:
        for s in SeqIO.parse(g, 'fasta'):
            ss = s.description.split(' ')
            thisid = ss[0]
            thisgenus = ss[2]
            thisspecies = ss[3]
            genus_species = '%s %s'%(thisgenus, thisspecies)
            out.write('>%s %s\n'%(thisid, genus_species))
            out.write(str(s.seq) + '\n')


