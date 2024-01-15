from joblib import dump, load
import os
import numpy as np
from Bio import SeqIO
from glob import glob

# load all the classifiers
class_dict = {} 
for l in glob('*joblib'):
    p = load(l)
    class_dict[l] = p

#print('Type\tQuery\tDatabase\tASV\tSpecies\tScore')
#print('Type\tQuery\tDatabase\tASV\tSpecies')
print('\t'.join('Type    Query   Subject domain  phylum  class   order   family  genus   species OTU'.split()))
for f in glob('../*fa'):
    # load the entire file into memory so we can give all sequences to the classifiers at once
    seqs = [[x.description, str(x.seq)] for x in SeqIO.parse(f, 'fasta')]
    y, X = list(), list()
    for a in seqs:
        y.append(a[0])
        X.append(a[1])

    # iterate over all classifiers
    for ref in class_dict:
        pipeline = class_dict[ref]
        spec_prob = pipeline.predict_proba(X)
        spec_classes = pipeline.classes_

        for spec_probas, input_gene, label in zip(spec_prob, X, y):
            spec_prediction_label = spec_classes[np.argmax(spec_probas)]
            best_score = max(spec_probas)
            best_label = spec_prediction_label
            #gene_dict[best_label].append( (input_gene, label) )
            if float(best_score) < 0.97:
                best_label = 'NA'
            newll = ['NBC', os.path.basename(f), os.path.basename(ref).replace('_classifier.joblib',''), 'NA', 'NA', 'NA', 'NA', 'NA', best_label.split(' ')[0], best_label, label]
            #print('\t'.join(map(str, ['NBC', os.path.basename(f), os.path.basename(ref), label, best_label])))#, best_score])))
            print('\t'.join(newll))

