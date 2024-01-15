from glob import glob
from Bio import SeqIO
import math
from collections import defaultdict
import random
random.seed(42)

for l in glob('*Fams.txt'):

    with open(l.replace('CountedFams.','')) as fh:
        fam_to_taxids = defaultdict(set)
        for line in fh:
            # 334880  cellular organisms;Eukaryota;Opisthokonta;Metazoa;Eumetazoa;Bilateria;Deuterostomia;Chordata;Craniata;Vertebrata;Gnathostomata;Teleostomi;Euteleostomi;Actinopterygii;Actinopteri;Neopterygii;Teleostei;Osteoglossocephalai;Clupeocephala;Euteleosteomorpha;Neoteleostei;Eurypterygia;Ctenosquamata;Acanthomorphata;Euacanthomorphacea;Percomorphaceae;Eupercaria;Centrarchiformes;Terapontoidei;Oplegnathidae;Oplegnathus;Oplegnathus woodwardi  Eukaryota;Chordata;Actinopteri;Centrarchiformes;Oplegnathidae;Oplegnathus;Oplegnathus woodwardi
            ll = line.rstrip().split('\t')
            taxid = ll[0]
            fam = ll[-1].split(';')[-3]
            fam_to_taxids[fam].add(taxid)

    taxids_to_sequences = defaultdict(list)
    for s in SeqIO.parse(l.replace('_Taxonomies.CountedFams.txt',''), 'fasta'):
        description = s.description
        thistaxid = description.split(' ')[1]
        taxids_to_sequences[thistaxid].append(s)

    with open(l) as fh:
        fams = [x.strip().split() for x in fh]
        # remove empty fams
        fams = [x for x in fams if len(x) == 2]
        num_fams = len(fams)
        # now we make 30% exclusions and 50% exclusions; 10 each at random
        thirty_perc_fams = math.floor(0.3 * num_fams)
        print(thirty_perc_fams)
        fifty_perc_fams = math.floor(0.5 * num_fams)
        print(fifty_perc_fams)
        seventy_perc_fams = math.floor(0.7 * num_fams)

        for i in range(1,11):
            # new subset!
            with open(l + f'_fifty_subset_{i}.fasta', 'w') as out1,\
                    open(l + f'_fifty_subset_{i}.taxids.txt', 'w') as out1_tax,\
                    open(l + f'_thirty_subset_{i}.fasta', 'w') as out2,\
                    open(l + f'_thirty_subset_{i}.taxids.txt', 'w') as out2_tax,\
                    open(l + f'_seventy_subset_{i}.fasta', 'w') as out3,\
                    open(l + f'_seventy_subset_{i}.taxids.txt', 'w') as out3_tax:
                fifty_this_sample = random.sample(fams, fifty_perc_fams)
                thirty_this_sample = random.sample(fams, thirty_perc_fams)
                seventy_this_sample = random.sample(fams, seventy_perc_fams)
                counter = 0
                for fam in fifty_this_sample:
                    fam_name = fam[1]
                    taxids_to_get = fam_to_taxids[fam_name]
                    for t in taxids_to_get:
                        for s in taxids_to_sequences[t]:
                            out1.write(s.format('fasta'))
                            out1_tax.write(f'{s.id}\t{s.description.split(" ")[1]}\n')

                for fam in thirty_this_sample:
                    fam_name = fam[1]
                    taxids_to_get = fam_to_taxids[fam_name]
                    for t in taxids_to_get:
                        for s in taxids_to_sequences[t]:
                            out2.write(s.format('fasta'))
                            out2_tax.write(f'{s.id}\t{s.description.split(" ")[1]}\n')

                for fam in seventy_this_sample:
                    fam_name = fam[1]
                    taxids_to_get = fam_to_taxids[fam_name]
                    for t in taxids_to_get:
                        for s in taxids_to_sequences[t]:
                            out3.write(s.format('fasta'))
                            out3_tax.write(f'{s.id}\t{s.description.split(" ")[1]}\n')
