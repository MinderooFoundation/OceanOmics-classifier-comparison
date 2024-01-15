import os
from glob import glob
from Bio import SeqIO
'''(Required). The path to the reference fasta file, or an R connection. Can be compressed. This reference fasta file should be formatted so that the id lines correspond to the genus-species of the associated sequence:

    >SeqID genus species ACGAATGTGAAGTAA......'''
for g in glob('../../*fasta'):
    with open('TEMP_TAX.txt', 'w') as out:
        for s in SeqIO.parse(g, 'fasta'):
            genus_species = s.description.split(' ')[2:4]
            genus_species = ' '.join(genus_species)
            out.write(f'{genus_species}\n')


    os.popen('cat TEMP_TAX.txt | taxonkit name2taxid | taxonkit lineage -i 2 | taxonkit reformat -i 3 -f "{k};{p};{c};{o};{f};{g};{s}" > TEMP_LINEAGE.txt').read()

    base = os.path.basename(g).replace('.fasta','forTaxonomy.fasta')
    with open(base, 'w') as out:
        for seq, line in zip(SeqIO.parse(g, 'fasta'), open('TEMP_LINEAGE.txt')):
            out.write('>%s\n'%( line.rstrip().split('\t')[-1]))
            out.write('%s\n'%str(seq.seq))

