from glob import glob
with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\tConfidence\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    for l in glob('*95perc.csv'):
        # Feature ID      Taxon   Confidence
        # ASV_1   Unassigned      0.9646193887444457
        # ASV_1005        622424  0.865459965313474       cellular organisms;Eukaryota;Opisthokonta;Metazoa;Eumetazoa;Bilateria;Deuterostomia;Chordata;Craniata;Vertebrata;Gnathostomata;Teleostomi;Euteleostomi;Actinopterygii;Actinopteri;Neopterygii;Teleostei;Osteoglossocephalai;Clupeocephala;Euteleosteomorpha;Neoteleostei;Eurypterygia;Ctenosquamata;Acanthomorphata;Euacanthomorphacea;Percomorphaceae;Gobiaria;Gobiiformes;Gobioidei;Gobiidae;Gobiinae;Mahidolia;Mahidolia mystacina   Eukaryota;Chordata;Actinopteri;Gobiiformes;Gobiidae;Mahidolia;Mahidolia mystacina

        # make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa_vs_c01_v03_finalforTaxonomy.fasta_Taxonomies.CountedFams.txt_thirty_subset_9forTaxonomy.fasta.csv
        query, database = l.split('_vs_')
        database = database.replace('forTaxonomy.fasta', '.fasta').replace('.95perc.csv', '')

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
                seq, *all_tax_levels = ll
                # "ACGAAGGCAGACCATGTTAAGGACCCTTGAATAAAAGACTGAACTTAGTGGCCCCCTGTCCTGATGTCTTCGGTTGGGGCGACCATGGGGAAACAAACATCCCCCGTGCGGAATGGGAGGACCACCCCTTTCTTTCTCTTCCCTCTCCTCCCACAACTAAGAGCTACAGCTCTAACTAGCAGAACTTCTGACCATAAGTGATCCGGCAATGCCGATCAGCGGACCA","Eukaryota","Chordata","Actinopteri",NA,NA,NA,NA
                # assigned
                newll = ['DADA2Tax', query, database] + all_tax_levels + [asv]#, score]
                out.write('\t'.join(newll) + '\n')

#Type    Query   Subject domain  phylum  class   order   family  genus   species OTU
#Qiime2  make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa      12s_v010_final.fasta_Taxonomies.CountedFams.txt_fifty_subset_2.fasta    Eukaryota       Chordata        Actinopteri     Lutjaniformes   Lutjanidae      Pristipomoides  Pristipomoides filamentosus     ASV_3
    # Type    Query   Subject domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits Fake
    # BLAST   make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa 16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_7.fasta    Eukaryota       Chordata        Actinopteri     Syngnathiformes Syngnathidae    Phyllopteryx    Phyllopteryx taeniolatus        ASV_1   26      68

