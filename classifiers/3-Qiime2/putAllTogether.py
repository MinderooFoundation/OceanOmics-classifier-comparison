from glob import glob
with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\tConfidence\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    for l in glob('*RESULTS/*fixed.tsv'):
        # Feature ID      Taxon   Confidence
        # ASV_1   Unassigned      0.9646193887444457
        # ASV_1005        622424  0.865459965313474       cellular organisms;Eukaryota;Opisthokonta;Metazoa;Eumetazoa;Bilateria;Deuterostomia;Chordata;Craniata;Vertebrata;Gnathostomata;Teleostomi;Euteleostomi;Actinopterygii;Actinopteri;Neopterygii;Teleostei;Osteoglossocephalai;Clupeocephala;Euteleosteomorpha;Neoteleostei;Eurypterygia;Ctenosquamata;Acanthomorphata;Euacanthomorphacea;Percomorphaceae;Gobiaria;Gobiiformes;Gobioidei;Gobiidae;Gobiinae;Mahidolia;Mahidolia mystacina   Eukaryota;Chordata;Actinopteri;Gobiiformes;Gobiidae;Mahidolia;Mahidolia mystacina

        database, query = l.split('.qza_classifier')
        database = database.replace('_taxids.txt','')
        query = query.lstrip('.qza_').replace('.qza_classify_out.qza_RESULTS/taxonomy._fixed.tsv', '')
        with open(l) as fh:
            fh.readline() # header
            for line in fh:
                ll = line.rstrip().split('\t')
                asv = ll[0]
                score = ll[2]
                if ll[1] == 'Unassigned' or float(score) < 0.97:
                    # unassigned
                    newll = ['Qiime2', query, database, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', asv]#, score]
                else:
                    # assigned
                    all_tax_levels = ll[-1].split(';')
                    newll = ['Qiime2', query, database] + all_tax_levels + [asv]#, score]
                    out.write('\t'.join(newll) + '\n')

    # Type    Query   Subject domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits Fake
    # BLAST   make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa 16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_7.fasta    Eukaryota       Chordata        Actinopteri     Syngnathiformes Syngnathidae    Phyllopteryx    Phyllopteryx taeniolatus        ASV_1   26      68
