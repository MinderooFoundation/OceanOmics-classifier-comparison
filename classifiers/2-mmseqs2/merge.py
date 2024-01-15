#Type    Query   Subject domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits   Fake

#BLAST   make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa    16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_7.fasta    Eukaryota       Chordata        Actinopteri     Syngnathiformes Syngnathidae    Phyllopteryx    Phyllopteryx taeniolatus        ASV_1   26      68

from glob import glob

with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\trank_level\tTaxid\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    taxlevel_index = {'domain':3, 'phylum':4, 'class':5, 'order':6, 'family':7, 'genus':8, 'species':9, 'no rank':100}
    for l in glob('*out_lca.tsv'):
        if '100perc' in l: continue
        # l = make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa_vs_16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_2.fasta_index_out_lca.tsv
        query, database = l.split('_vs_')
        database = database.replace('_index_out_lca.tsv', '')
        with open(l) as fh:
            for line in fh:
                ll = line.rstrip().split('\t')
                # ['ASV_383', '0', 'no rank', 'unclassified']
                # ['ASV_26', '75014', 'species', 'Acanthurus xanthopterus']
                asv = ll[0]
                taxlevel = ll[-2]
                label = ll[-1]
                taxid = ll[1]
                try:
                    position = taxlevel_index[taxlevel]
                except KeyError:
                    print(taxlevel, label)
                    position = 100
                newll = ['MMSeqs2', query, database, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', asv]#, taxlevel, taxid]
                if position != 100:
                    newll[position] = label
                out.write('\t'.join(newll) + '\n')
