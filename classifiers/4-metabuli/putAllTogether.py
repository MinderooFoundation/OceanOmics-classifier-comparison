from glob import glob
with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\tDNA_identity\tProtein_identity\tHamming_distance\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    for l in glob('*RESULTS/*fixed.tsv'):
        # make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa_vs_16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_6.fasta_ref.fasta_db_RESULTS/make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa_vs_16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_6.fasta_ref.fasta_db_RESULTS_classifications_fixed.tsv
        query, database = l.split('/')[0].split('_vs_')
        database = database.replace('_db_RESULTS','')
        # 0       ASV_1   0       225     0       0       0       no rank
        # 1       ASV_10  75042   201     0.283582        0.283582        0       species 75042:12        cellular organisms;Eukaryota;Opisthokonta;Metazoa;Eumetazoa;Bilateria;Deuterostomia;Chordata;Craniata;Vertebrata;Gnathostomata;Teleostomi;Euteleostomi;Actinopterygii;Actinopteri;Neopterygii;Teleostei;Osteoglossocephalai;Clupeocephala;Euteleosteomorpha;Neoteleostei;Eurypterygia;Ctenosquamata;Acanthomorphata;Euacanthomorphacea;Percomorphaceae;Eupercaria;Eupercaria incertae sedis;Siganidae;Siganus;Siganus canaliculatus     Eukaryota;Chordata;Actinopteri;;Siganidae;Siganus;Siganus canaliculatus
        with open(l) as fh:
            for line in fh:
                ll = line.rstrip().split('\t')
                asv = ll[1]
                taxid = ll[2]
                dna_ident = ll[4]
                prot_ident = ll[5]
                hamming_dist = ll[6]
                if ll[0] == '0' or ':' in ll[-1]:
                    # unassigned
                    newll = ['Metabuli', query, database, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', asv]#, dna_ident, prot_ident, hamming_dist]
                else:
                    # assigned
                    all_tax_levels = ll[-1].split(';')
                    all_tax_levels = ['NA' if x == '' else x for x in all_tax_levels]
                    newll = ['Metabuli', query, database] + all_tax_levels + [asv]# + [dna_ident, prot_ident, hamming_dist]
                    out.write('\t'.join(newll) + '\n')

    # Type    Query   Subject domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits Fake
    # BLAST   make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa 16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_7.fasta    Eukaryota       Chordata        Actinopteri     Syngnathiformes Syngnathidae    Phyllopteryx    Phyllopteryx taeniolatus        ASV_1   26      68

