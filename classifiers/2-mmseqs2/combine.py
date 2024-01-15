from glob import glob

for l in glob('*lca.tsv'):
    if 'c01' in l: continue
    print(l)
