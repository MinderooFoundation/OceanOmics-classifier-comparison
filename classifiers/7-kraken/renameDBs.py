from glob import glob
import os
for l in glob('../*fasta'):
    with open(os.path.basename(l) + '_kraken.fasta', 'w') as out:
        for line in open(l):
            if line.startswith('>'):
                ll = line.split(' ')
                out.write(ll[0] + '|kraken:taxid|' + ll[1] + '\n')
            else:
                out.write(line)

