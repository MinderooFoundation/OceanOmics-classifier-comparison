from glob import glob
with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\tScore\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    for l in glob('*/*wang.taxonomy'):

        
        query, database  = l.split('.fa_')
        # make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa_16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_9.fasta/make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fasta_mothur_taxidsmothur.wang.tax.summary
        database = database.split('/')[0]
        query = query + '.fa'
        with open(l) as fh:
            # ASV_4   cellular_organisms(100);Eukaryota(100);Opisthokonta(100);Metazoa(100);Eumetazoa(100);Bilateria(100);Deuterostomia(100);Chordata(100);Craniata(100);Vertebrata(100);Gnathostomata(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);Gnathostomata_unclassified(100);
            # ASV_15  cellular_organisms(100);Eukaryota(100);Opisthokonta(100);Metazoa(100);Eumetazoa(100);Bilateria(100);Deuterostomia(100);Chordata(100);Craniata(100);Vertebrata(100);Gnathostomata(100);Teleostomi(100);Euteleostomi(100);Actinopterygii(100);Actinopteri(100);Neopterygii(100);Teleostei(100);Osteoglossocephalai(100);Clupeocephala(100);Euteleosteomorpha(100);Neoteleostei(100);Eurypterygia(100);Ctenosquamata(100);Acanthomorphata(100);Euacanthomorphacea(100);Percomorphaceae(100);Syngnathiaria(100);Syngnathiformes(100);Mulloidea(100);Mullidae(100);Parupeneus(100);Parupeneus_chrysopleuron(100);Parupeneus_chrysopleuron_unclassified(100);Parupeneus_chrysopleuron_unclassified(100);Parupeneus_chrysopleuron_unclassified(100);
            for line in fh:
                ll = line.rstrip().split('\t')
                asv = ll[0]
                lowest_thing = ll[1].split(';')[-2].replace('_unclassified','')
                lowest_thing, score = lowest_thing.split('(')
                score = score.replace(')','')
                if '_' in lowest_thing:
                    # species-level hit
                    for element in ll[1].split(';'):
                        if 'dae(' in element:
                            family = element.split('(')[0]
                            break
                    lowest_thing = lowest_thing.replace('_',' ')
                    genus = lowest_thing.split(' ')[0]
                    newll = ['Mothur', query, database, 'NA', 'NA', 'NA', 'NA', family, genus, lowest_thing, asv]#, score]
                else:
                    newll = ['Mothur', query, database, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', asv]#, 'NA']
                out.write('\t'.join(newll) + '\n')
