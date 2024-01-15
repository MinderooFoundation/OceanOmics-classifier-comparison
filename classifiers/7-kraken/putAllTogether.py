#Type    Query   Subject domain  phylum  class   order   family  genus   species OTU     numberOfUnq_BlastHits   Fake
# 
# BLAST   make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa    16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_7.fasta    Eukaryota       Chordata        Actinopteri     Syngnathiformes Syngnathidae    Phyllopteryx    Phyllopteryx taeniolatus        ASV_1   26      68

from glob import glob
def filter_zeroes(number):
    if number.startswith('0:'):
        return False
    return True

with open('all_results.tsv', 'w') as out:
    #out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\tTaxonomy_hits\tOverall_hits\tKraken_confidence\n')
    out.write('Type\tQuery\tSubject\tdomain\tphylum\tclass\torder\tfamily\tgenus\tspecies\tOTU\n')
    for l in glob('make*fixed.tsv'):
        # make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa_0.9_16S_v04_HmmCut.fasta_db_out_fixed.tsv
        query, database = l.split('.fa_')
        query += '.fa'

        dl = database.split('_')
        cutoff = dl[0]
        database = '_'.join(dl[1:]).split('_db_out')[0]

        for line in open(l):
            ll = line.rstrip().split('\t')
            # 0:15 123369:4 123366:2 0:113
            # U       ASV_1   0       197     0:48 458026:5 1489872:1 0:3 181402:5 0:101
            hits = ll[4]
            hits = list(filter(filter_zeroes, hits.split()))
            num_hits = len(hits)
            distinct_hits = sum(map(int, [l.split(':')[1] for l in hits]))
            newll = [f'Kraken_{cutoff}', query, database]
            if len(ll) == 5:
                # no hits
                newll += 7*['NA']
            else:
                # hits
                best_ranks = ll[-1].split(';')
                best_ranks = ['NA' if not x else x for x in best_ranks]
                newll += best_ranks
            asv_name = ll[1]
            newll += map(str, [asv_name])#, distinct_hits, num_hits, cutoff])
            out.write('\t'.join(newll)+'\n')
