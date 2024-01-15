# iterate over all databases; make a custom job lib for every databaseG
# we will also do the upsampling; if taxonomic label appears < 10 times, upsample 10 times
from glob import glob
import sklearn
from Bio import SeqIO
import os
from sklearn.feature_extraction.text import HashingVectorizer
from imblearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, matthews_corrcoef, accuracy_score, cohen_kappa_score
#from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import RandomizedSearchCV#, HalvingGridSearchCV

import time
from joblib import dump

from collections import defaultdict

for f in glob('../*fasta'):

    if os.path.exists(os.path.basename(f) + '_classifier.joblib'):
        print(f'got {f} already')
        continue
    if 'c01' not in f:
        print(f'NOT skipping {f}')
        continue
    print(f'training {f}')
    if 'HmmCut' in f:
        print(f'skipping {f}')
        continue
    spec_dict = {}
    species_count = defaultdict(int)
    for s in SeqIO.parse(f, 'fasta'):
        sl = s.description.split(' ')

        thisid = sl[0].split('_')[-1]
        rest = sl[1:]
        found = False
        for index, i in enumerate(rest):
            if thisid in i:
                found = True
                break
        assert found
        species = ' '.join(rest[1:index])
        species_count[species] += 1
    
    X, y = [], []
    for s in SeqIO.parse(f, 'fasta'):
        sl = s.description.split(' ')
        thisid = sl[0].split('_')[-1]
        rest = sl[1:]
        found = False
        for index, i in enumerate(rest):
            if thisid in i:
                found = True
                break
        assert found
        species = ' '.join(rest[1:index])
        if species_count[species] < 10:
            X += 10*[str(s.seq)]
            y += 10*[species]
        else:
            X += [str(s.seq)]
            y += [species]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,
            stratify = y,
            shuffle = True,
            random_state = 42)

    steps = [('feat_ext', HashingVectorizer(analyzer='char_wb', n_features=4098, 
            ngram_range=(8,8), alternate_sign=False)),
            ('classify', MultinomialNB(alpha=0.001, fit_prior=False))]

    pipeline_raw = Pipeline(steps=steps)
    param_grid = {
        "feat_ext__ngram_range": [(i, i) for i in range(8, 46, 2)],
        #"feat_ext__n_features": [i for i in range(124, 8196, 500)],
        "classify__fit_prior": [True, False],
        "classify__alpha": [0.001, 0.01, 0.1],
    }

    search = RandomizedSearchCV(pipeline_raw, param_grid, n_jobs=15, verbose=1)
    #search = HalvingGridSearchCV(pipeline_raw, param_grid, verbose=1, min_resources = 10, max_resources=1000, n_jobs=100, aggressive_elimination  =True, factor=2)
    search.fit(X_train, y_train)
    pipeline = search.best_estimator_
    print('done!')
    #steps_dict = defaultdict(list)
    #for key in search.best_params_:
    #    pipelinestep, param = key.split('__')
    #    value = search.best_params_[key]
    #    steps_dict[pipelinestep] = {param:value}
    ## defaultdict(<class 'list'>, {'feat_ext': {'ngram_range': (30, 30)}, 'classify': {'alpha': 0.01}})
    #steps = [('feat_ext', HashingVectorizer(analyzer='char_wb', n_features=4098, **steps_dict['feat_ext'])),
    #        ('classify', MultinomialNB(**steps_dict['classify']))]
    #print(steps)
    #pipeline = Pipeline(steps=steps)
    #pipeline.fit(X_train, y_train)

    dump(pipeline, os.path.basename(f) + '_classifier.joblib')

