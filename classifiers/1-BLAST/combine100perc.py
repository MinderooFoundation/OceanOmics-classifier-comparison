from glob import glob

#print('Type\tQuery\tSubject\t' + '\t'.join('''domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits   Fake '''.split()))
print('Type\tQuery\tSubject\t' + '\t'.join('''domain  phylum  class   order   family  genus   species OTU'''.split()))
for l in glob('100*LCA.tsv'):
    query, subject = l.split('_vs_')
    subject = subject.replace('_out_LCA.tsv','')
    query = query.replace('100perc_', '')
    with open(l) as fh:
        header = fh.readline()
        for line in fh:
            ll = line.rstrip().split('\t')
            # ignore the last two columns
            print('\t'.join(['BLAST100', query, subject]) + '\t' + '\t'.join(ll[:-2]))
