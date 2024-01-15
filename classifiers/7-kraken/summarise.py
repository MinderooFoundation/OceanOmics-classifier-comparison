from glob import glob
# Counts the numbers of classification levels

print('Cutoff\tInclusion\tSpecies\tFamilies\tUnclassified\tClassified')
for l in glob('*families'):
    cutoff = l.split('_')[0]
    try:
        this_exclusion = l.split('.txt')[1].split('_')[1]
    except:
        this_exclusion = 'zero'
    fams = [x.strip() for x in open(l).readlines()][0]
    species = [x.strip() for x in open(l.replace('families', 'species')).readlines()][0]
    unclass = [x.strip() for x in open(l.replace('families', 'unclassified')).readlines()][0]
    classif = [x.strip() for x in open(l.replace('families', 'classified')).readlines()][0]
    print('\t'.join(map(str, [cutoff, this_exclusion, species, fams, unclass, classif])))
