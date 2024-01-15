print('accession\taccession.version\ttaxid\tgi')

my= '''242979  |       2923229 |
334900  |       3062207 |
882756  |       2923230 |
990565  |       3051909 |
1515630 |       1111465 |
1828424 |       2923232 |'''.split('\n')
transl = {}
for line in my:
    ll = line.split()
    old, new = ll[0], ll[2]
    transl[old]= new
for line in open('12s_v010_final.fasta.taxids.txt'):
    ll = line.split()
    if not ll[0].endswith('.1'):
        ll[0] += '.1'
    name = '.'.join(ll[0].split('.')[:-1])
    if ll[1] in transl:
        ll[1] = transl[ll[1]]
    print(f'{name}\t{ll[0]}\t{ll[1]}\t0')
    #print(f'{ll[0]}\t{ll[1]}')
