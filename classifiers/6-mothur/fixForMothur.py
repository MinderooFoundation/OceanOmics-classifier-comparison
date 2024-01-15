from glob import glob
for x in glob('*taxids.txt'):
    with open(x) as f, open(x.rstrip('.txt') + 'mothur.txt', 'w') as out:
        for line in f:
            ll = line.rstrip().split('\t')
            ll = [ll[0], ll[2].replace(' ','_') + ";"] 
            out.write('\t'.join(ll) + '\n')
