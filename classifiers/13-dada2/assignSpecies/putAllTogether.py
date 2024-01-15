from glob import glob
with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\tConfidence\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    for l in glob('*Species.csv'):

        # make_12s_16s_simulated_reads_6-fakeGenes_GreenGenes_RESULTS_dada2_asv.fa_vs_c01_v03_HmmCutreformatted_for_species.fasta.Species.csv
        query, database = l.split('_vs_')
        database = database.replace('reformatted_for_species.fasta.Species.csv', '') + '.fasta'
        database = database.replace('_Taxonomies', '.fasta_Taxonomies')

        query_names_f = '../../' + query
        query_names = []
        with open(query_names_f) as fh:
            for line in fh:
                if line.startswith('>'):
                    name = line.rstrip().lstrip('>')
                    query_names.append(name)

        # "","Genus","Species"
        #"GAATGGTAAATTACGTAAGAAGCCTTGATTAAAAGAATGAACCAAGTAAACATTACCCAAATATCTTTGGTTGGGGCGACCGCGGGGTAAAACATAACCCCCGTGAGGAGCGAGGTATAAACCTTAAAACTACGAGCACCAGCTCTAAGTATCAAAACATTTGACCTTTAGATCCGGCATAGCCGATCAACGAACCG",NA,NA
        with open(l) as fh:
            fh.readline() # header
            for line,queryn in zip(fh, query_names):
                ll = line.rstrip().replace('"', '').split(',')
                asv = queryn
                seq, genus, species = ll
                if genus == 'NA':
                    # unassigned
                    newll = ['DADA2Spec', query, database, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', asv]#, score]
                else:
                    # assigned
                    if '/' in species:
                        # we treat the genus as LCA in cases where DADA2 has several hits
                        # example: Squalus formosus/japonicus/megalops/mitsukurii
                        all_tax_levels = ['NA', 'NA', 'NA', 'NA', 'NA', genus, 'NA']
                    else:
                        all_tax_levels = ['NA', 'NA', 'NA', 'NA', 'NA', genus, genus + ' ' + species]
                    assert '/' not in genus #just doublechecking...
                    newll = ['DADA2Spec', query, database] + all_tax_levels + [asv]#, score]
                out.write('\t'.join(newll) + '\n')

