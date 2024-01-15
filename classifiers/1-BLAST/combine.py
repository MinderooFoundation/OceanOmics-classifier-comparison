from glob import glob

#print('Type\tQuery\tSubject\t' + '\t'.join('''domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits   Fake '''.split()))
print('Type\tQuery\tSubject\t' + '\t'.join('''domain  phylum  class   order   family  genus   species OTU'''.split()))
for l in glob('*LCA.tsv'):
    if l.startswith('100'): continue
    query, subject = l.split('_vs_')
    subject = subject.replace('_out_LCA.tsv','')
    with open(l) as fh:
        header = fh.readline()
        for line in fh:
            ll = line.rstrip().split('\t')
            # ignore the last two columns
            print('\t'.join(['BLAST', query, subject]) + '\t' + '\t'.join(ll[:-2]))
