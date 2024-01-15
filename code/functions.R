source('code/helpers.R')

get_classifier_data <- function(file) {
  read.csv(file, sep = '\t', row.names = 1)
}

plot_dendrogram <- function(data) {
  data |> 
    dist() |> 
    hclust(method = 'ward.D2') |> 
    ggdendrogram(rotate = TRUE, theme_dendro = TRUE, labels = TRUE)
}


get_hits_data <- function(file) {
  read_tsv(file) |> 
    # give more descriptive names to Classifiers
    mutate(
            Type = str_replace(Type, '^NBC$', 'CustomNBC'),
            Type = str_replace(Type, '^BLAST$', 'BLAST97'),
            Type = str_replace(Type, '^MMSeqs2$', 'MMSeqs2_97'),
            # fix typo in Metabuli output I introduced
            Subject = str_replace(Subject, 'fasta_ref.fasta', 'fasta')
           )
}

get_truth_data <- function(file) {
  df <- read_tsv(file, col_names = c('Query', 'Subject', 'OTU', 'taxids', 'lca_taxid', 'long_lineage', 'short_lineage')) |> 
    separate(short_lineage, into = c('domain', 'phylum', 'class', 'order', 'family', 'genus', 'species'), sep = ';')
  df[df == ''] <- 'dropped'
  df
}
  
subsample_blast_thirty_hits <- function(data) {
  data |> 
    filter(Subject %in% c('16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_8.fasta', 
                          '12s_v010_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_8.fasta')) |> 
    filter(Query %in% c('make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa', 
                        'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa')) |> 
    filter( (Subject == '12s_v010_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_8.fasta' & 
               Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa') | 
              ( Subject == '16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_8.fasta' &
                  Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa'))
  
}

subsample_nbc_hits <- function(data) {
  data |> 
    filter(Subject %in% c('16S_v04_final.fasta', '12s_v010_final.fasta')) |> 
    filter(Query %in% c('make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa',
                        'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa')) |> 
    filter( (Subject == '12s_v010_final.fasta' &
               Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa') |
              (Subject == '16S_v04_final.fasta' &
                 Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa'))
}

subsample_nbc_hits_thirty <- function(data) {
  data |> 
    filter(Subject %in% c('16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_4.fasta',
                           '12s_v010_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_4.fasta')) |> 
    filter(Query %in% c('make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa',
                        'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa')) |> 
    filter( (Subject == '12s_v010_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_4.fasta' &
               Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa') |
              (Subject == '16S_v04_final.fasta_Taxonomies.CountedFams.txt_thirty_subset_4.fasta' &
                 Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa')) 
}

subsample_blast_hits <- function(data) {
  data |> 
    filter(Subject %in% c('16S_v04_final.fasta', '12s_v010_final.fasta')) |> 
    filter(Query %in% c('make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa', 
                        'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa')) |> 
    filter( (Subject == '12s_v010_final.fasta' & 
               Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa') | 
              ( Subject == '16S_v04_final.fasta' &
                  Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa'))
}

assess_correctness <- function(data, truth) {
  truth <- truth |> 
    select(Query, OTU, species, family) |> 
    mutate(species = na_if(species, 'dropped')) |>
    rename(True_Query = Query, True_OTU = OTU, True_species = species, True_family = family)
  
  filtered_data <- data |> 
    mutate(Type = str_replace(Type, '^BLAST$', 'BLAST97')) |>
    mutate(Type = str_replace(Type, '^MMSeqs2$', 'MMSeqs2_97')) |>
    filter(Subject %in% c('16S_v04_final.fasta', 
                          '12s_v010_final.fasta', 
                          'c01_v03_final.fasta')) |>
    filter(!Type %in% c('Kraken_0.2', 'Kraken_0.3', 'Kraken_0.4', 'Kraken_0.5', 'Kraken_0.6', 'Kraken_0.7', 'Kraken_0.8', 'Kraken_0.9')) |> 
    mutate(Type = str_replace(Type, 'Kraken', 'Kraken2')) |> 
    mutate(Subject = str_replace_all(Subject, pattern = '_ref.fasta', replacement=''),
           species = na_if(species, 'dropped')) |> 
    select(Type, Query, Subject, genus, family, species, OTU) |>
    left_join(truth, by=c('Query'= 'True_Query', 
                          'OTU' = 'True_OTU')) |>
    filter( ( Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' & Subject == '12s_v010_final.fasta') | 
              (  Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' & Subject == '16S_v04_final.fasta') |
              ( Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' & Subject == 'c01_v03_final.fasta') |
              ( Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' & Subject == '12s_v010_final.fasta') | 
              (  Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' & Subject == '16S_v04_final.fasta') |
              (Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' & Subject == 'c01_v03_final.fasta') | 
              ( Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' & Subject == '12s_v010_final.fasta') | 
              (  Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' & Subject == '16S_v04_final.fasta') |
              (Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' & Subject == 'c01_v03_final.fasta')) |> 
    mutate(CorrectSpecies = case_when(!is.na(species) & True_species == species ~ 'Correct species',
                                      !is.na(species) & True_species != species ~ 'Incorrect species',
                                      TRUE ~ NA))
  
  # you can test here using with(filtered_data, table(Query, Subject))   
  filtered_data
}

prepare_mean_median_f1_table <- function(filtered_data) {
  Counted_data <- filtered_data |> 
    mutate(all_asvs = case_when(Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 24,
                                Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 27,
                                Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 27,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 102,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 112,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 117,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ 99,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ 99,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ 99)) |>
    group_by(Type, Query, Subject, all_asvs) |>
    summarise(TP = sum(str_detect(CorrectSpecies, pattern = '^Correct species$'), na.rm=TRUE),
              FP = sum(str_detect(CorrectSpecies, pattern = 'Incorrect species'), na.rm=TRUE),
              TN = sum(str_detect(replace_na(CorrectSpecies,'NA'), pattern='NA') & is.na(True_species), na.rm=TRUE),
              FN = sum(is.na(species) & !is.na(True_species))) |> 
    mutate(sums = TP + FP + TN + FN)  |>
    mutate(missing = all_asvs - sums) |>
    mutate(FN = FN + missing) |> 
    select(-c(missing, sums))
  
  Counted_data |> 
    mutate(Precision = precision(TP, FP),
           Recall = recall(TP, FN),
           F1 = f1(Precision, Recall),
           F0.5 = f0.5(Precision, Recall),
           Accuracy = accuracy(TP, FP, FN, TN)) |> 
    ungroup()
}

make_median_f1_table <- function(filtered_data) {
  # this is Table 2
  Counted_data <- prepare_mean_median_f1_table(filtered_data)
  Counted_data |> 
    filter(! str_detect(Subject, '^c01')) |>  # TODO: DECIDE IF THIS IS FAIR
    select(Type, Precision, Recall, F1, F0.5, Accuracy) |> 
    pivot_longer(-Type, names_to = 'Measure') |> 
    group_by(Type, Measure) |> 
    summarise(median = median(value)) |> 
    pivot_wider(names_from = Measure, values_from = median) 
    
}

make_mean_f1_table <- function(filtered_data){
  Counted_data <- prepare_mean_median_f1_table(filtered_data)
  Counted_data |> 
    filter(! str_detect(Subject, '^c01')) |> 
    select(Type, Precision, Recall, F1, F0.5, Accuracy) |> 
    pivot_longer(-Type, names_to = 'Measure') |> 
    group_by(Type, Measure) |> 
    summarise(mean = mean(value)) |> 
    pivot_wider(names_from = Measure, values_from = mean) 
  
}

make_overview_f1_table <- function(filtered_data) {
  # make one table for everything, but pivot_wider the three genes
  Counted_data <- prepare_mean_median_f1_table(filtered_data)
  Counted_data |> 
    group_by(Type, Subject) |> 
    summarise(avg_acc = mean(Accuracy), 
              avg_prec = mean(Precision), 
              avg_rec = mean(Recall), 
              avg_f1 = mean(F1), 
              avg_f0.5 = mean(F0.5)) |> 
    mutate(across(where(is.numeric), \(x) round(x, 2))) |> 
    pivot_wider(names_from = Subject, values_from = c(avg_prec, avg_acc, avg_rec, avg_f1, avg_f0.5))
    
}

plot_overview_f1_table <- function(overview_f1_table) {
  # first, we get the top 3 and the bottom 3 classifiers
  

  classifier_levels <-   overview_f1_table |> 
    rename(Classifier = Type) |> 
    pivot_longer(-Classifier, names_to = 'Measure') |> 
    mutate(Measure = str_remove(Measure, 'avg_')) |> 
    separate(Measure, into=c('Measure', 'Database'), sep = '_', extra='merge') |>
    mutate(Database = case_when(Database == '12s_v010_final.fasta' ~ '12S',
                                Database ==  '16S_v04_final.fasta' ~ '16S',
                                TRUE ~ 'COI')) |>
    arrange(desc(value)) |> pull(Classifier) |> unique()
    
  overview_f1_table |> 
    rename(Classifier = Type) |> 
    pivot_longer(-Classifier, names_to = 'Measure') |> 
    mutate(Measure = str_remove(Measure, 'avg_')) |> 
    separate(Measure, into=c('Measure', 'Database'), sep = '_', extra='merge') |>
    mutate(Database = case_when(Database == '12s_v010_final.fasta' ~ '12S_Miya',
                                Database ==  '16S_v04_final.fasta' ~ '16S_Berry',
                                TRUE ~ 'COI_Leray')) |>
    mutate(Classifier = factor(Classifier, levels =classifier_levels)) |>
    filter(Measure %in% c('prec', 'acc')) |> 
    pivot_wider(names_from = Measure, values_from = value) |> 
    ggplot(aes(x=prec, y = acc, color=Classifier, shape=Classifier)) + 
    geom_point(size=3) + 
    scale_shape_manual(values=1:14) +
    ylab('Accuracy') + 
    xlab('Precision') + 
    facet_wrap(~Database) +
    ylim(c(0,1)) + 
    xlim(c(0,1)) +
    theme_minimal() +
    theme(panel.spacing = unit(2, "lines")) +
    # rotate xaxis labels
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

make_all_median_f1_tables <- function(filtered_data) {
  # this is Table 2, but split up into subtables for Supplementary Tables
  
  Counted_data <- filtered_data |> 
    mutate(all_asvs = case_when(Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 24,
                                Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 27,
                                Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 27,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 102,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 112,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 117,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ 99,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ 99,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ 99)) |>
    group_by(Type, Query, Subject, all_asvs) |>
    summarise(TP = sum(str_detect(CorrectSpecies, pattern = '^Correct species$'), na.rm=TRUE),
              FP = sum(str_detect(CorrectSpecies, pattern = 'Incorrect species'), na.rm=TRUE),
              TN = sum(str_detect(replace_na(CorrectSpecies,'NA'), pattern='NA') & is.na(True_species), na.rm=TRUE),
              FN = sum(is.na(species) & !is.na(True_species))) |> 
    mutate(sums = TP + FP + TN + FN)  |>
    mutate(missing = all_asvs - sums) |>
    mutate(FN = FN + missing) |> 
    select(-c(missing, sums))
  
  named_df_list <- Counted_data |> 
    mutate(Precision = precision(TP, FP),
           Recall = recall(TP, FN),
           F1 = f1(Precision, Recall),
           F0.5 = f0.5(Precision, Recall),
           Accuracy = accuracy(TP, FP, FN, TN)) |> 
    ungroup() |> 
    mutate(
      Query = case_when(
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ '100 Australian species'
      )
    ) |> 
    mutate(Subject = case_when(Subject == '12s_v010_final.fasta' ~ '12S',
                               Subject ==  '16S_v04_final.fasta' ~ '16S',
                               TRUE ~ 'COI')) |>
    select(Type,Query, Subject,  Precision, Recall, F1, F0.5, Accuracy) |> 
    pivot_longer(-c(Query, Subject, Type), names_to = 'Measure') |> 
    #unite('Pair', Query:Subject, remove = FALSE) |>  # Pair will be hte name of the sheet in the XLSX
    pivot_wider(names_from = Measure, values_from = value) |> 
    group_by(Query, Subject) |> 
    group_split()
  
  named_df_list
  
}

count_correctness <- function(filtered_data) {
  filtered_data |>
    separate(True_species,
             into = c('True_Genus', 'True_Epiteth'),
             remove = FALSE) |>
    mutate(species = na_if(species, 'dropped')) |>
    mutate(genus = na_if(genus, 'dropped')) |>
    
    mutate(
      CorrectSpecies = case_when(
        !is.na(species) &
          True_species == species ~ 'Correct species',
        !is.na(species) &
          True_species != species & True_Genus == genus ~ 'Correct genus, incorrect species',
        !is.na(species) &
          True_species != species & True_Genus != genus ~ 'Incorrect genus, incorrect species',
        !is.na(genus) &
          !is.na(True_Genus) &
          True_Genus == genus ~ 'Correct genus',
        !is.na(genus) &
          !is.na(True_Genus) &
          True_Genus != genus ~ 'Incorrect genus',
        !is.na(family) &
          True_family == family ~ 'Correct family',
        !is.na(family) &
          True_family != family ~ 'Incorrect family',
        TRUE ~ NA
      )
    ) |>
    group_by(Query, Type, Subject) |>
    count(CorrectSpecies) |>
    group_by(Query, Type, Subject) |>
    mutate(total = sum(n)) |>
    mutate(all_asvs = case_when(Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 24,
                                Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 27,
                                Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 27,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 102,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 112,
                                Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 117,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ 99,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ 99,
                                Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ 99)) |>
    mutate(missing = all_asvs - total) |>
    group_modify( ~ add_row(.x)) |>
    group_modify( ~ {
      .x |> mutate(
        new_col = max(missing, na.rm = TRUE),
        newcol2 = max(all_asvs, na.rm = TRUE)
      ) |>
        mutate(
          n = case_when(is.na(CorrectSpecies) & is.na(missing) ~ new_col,
                        TRUE ~ n),
          all_asvs = case_when(
            is.na(CorrectSpecies) & is.na(missing) ~ newcol2,
            TRUE ~ all_asvs
          )
        )
    }) |>
    mutate(perc = n / all_asvs * 100) |>
    mutate(CorrectSpecies = replace_na(CorrectSpecies, 'No hit')) |>
    mutate(
      Query = case_when(
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ '100 Australian species'
      )
    ) |> 
    mutate(Subject = case_when(Subject == '12s_v010_final.fasta' ~ '12S',
                               Subject == '16S_v04_final.fasta' ~ '16S',
                               TRUE ~ 'COI')) |> # TODO: CO1
    mutate(CorrectSpecies = factor(CorrectSpecies, rev(
      c(
        'Correct species',
        'Correct genus',
        'Correct genus, incorrect species',
        'Correct family',
        'Incorrect genus, incorrect species',
        'Incorrect genus',
        'Incorrect family',
        'No hit'
      )
    ))) |> 
    rename("Classifier" = Type) |> 
    group_modify ( ~ { .x |> tidyr::complete(CorrectSpecies, fill = list(n=0, total = max(.x$all_asvs), missing = NA, perc = 0)) } )    
}

plot_correctness <- function(counted_data) {

    cols <- c('Correct species' = "#009E73", 
            'Correct genus'="#56B4E9", 
            'Correct family' = "#0072B2", 
            'Incorrect family' = "#E69F00", 
            'Incorrect genus'="#F0E442", 
            'Correct genus, incorrect species'="#D55E00", 
            'Incorrect genus, incorrect species'="darkred", 
            'No hit'= "#D3D3D3")

  mymax <- function(perc){
    # the last element of the percentages 
    # is the 'Correct species' percentage
    perc[length(perc)]
  }
  
  counted_data |> 
    group_by(Classifier) |> 
    ggplot(aes(
      x = tidytext::reorder_within(x=Classifier, by=perc, 
                                   list(Subject, Query), 
                                   fun = mymax),
      fill = CorrectSpecies,
      y = perc
    )) +
    geom_col() +
    coord_flip() +
    theme_minimal() +
    ylab('Percentage') +
    xlab('Classifier') +
    scale_fill_manual(name = 'Outcome',
                      values = cols,
                      breaks = names(cols)) +
    tidytext::scale_x_reordered() +
    facet_wrap(~ Subject + Query, scales='free') + 
    theme(legend.position = 'bottom',
          plot.background = element_rect(
            fill = "white",
            colour = "white"
          ), 
          axis.text.y = element_text(size = 5))
}


get_stats_on_correctness <- function(counted_data){
  counted_data |> 
    ungroup() |> 
    group_by(Classifier, Subject) |> 
    filter(CorrectSpecies == 'Correct species') |> 
    summarise(average_correctness = mean(perc)) |> 
    arrange(average_correctness)
}

make_error_types_table <- function(correctness_table) {
  # need to know which errors are being made. Is it totally wrong species? wrong species, but correct genus?

  correctness_table |> 
    mutate(Subject = case_when(Subject == '12s_v010_final.fasta' ~ '12S',
                               Subject ==  '16S_v04_final.fasta' ~ '16S',
                               TRUE ~ 'COI')) |> # TODO: CO1
    separate(species, into = c('genus', 'epiteth')) |> 
    separate(True_species, into = c('True_genus', 'True_epiteth')) |> 
    mutate(CorrectGenus = case_when( True_genus == genus ~ 'Correct genus', 
                                     True_genus != genus ~ 'Incorrect genus',
                                     TRUE ~ NA)) |> 
    mutate(Outcome = case_when(CorrectSpecies == 'Correct species' & CorrectGenus == 'Correct genus' ~ 'Genus and species correct',
                            CorrectSpecies == 'Incorrect species' & CorrectGenus == 'Correct genus' ~ 'Genus correct, species wrong',
                            CorrectSpecies != 'Correct species' & CorrectGenus != 'Correct genus' ~ 'Genus and species wrong')) |> 
    mutate(Outcome = factor(Outcome, levels = c('Genus and species correct','Genus correct, species wrong', 'Genus and species wrong'))) |> 
    group_by(Type, Query, Subject, Outcome) |> 
    filter(!is.na(Outcome)) |> 
    count() |> 
    group_by(Type, Query, Subject) |> 
    mutate(totals = sum(n),
           Percentage = n/totals*100) |> 
    mutate(
      Query = case_when(
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
        Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ '100 Australian species'
      )
    ) 
}

make_error_types_figure <- function(error_types_table) {
  cols <- list('Genus and species correct' = "#009E73",
               'Genus correct, species wrong' = "#56B4E9",
               'Genus and species wrong' = "#D55E00")
  
  error_types_table |> 
    ggplot(aes(x = Type, y = Percentage, fill = Outcome))  + 
    geom_col() + 
    facet_wrap(~Subject + Query) + 
    coord_flip() +
    scale_fill_manual(values = cols) +
    xlab('Classifier') +
    theme_minimal() +
    theme(legend.position = 'bottom', 
          axis.text.y = element_text(size = 5),
          plot.background = element_rect(
            fill = "white",
            colour = "white"
        ))
}

make_big_table <- function(correctness_table) {

  # we make one table where we have all the species labels, one column per classifier
  outcome_spread <- correctness_table |> 
    select(-c(family, genus, CorrectSpecies)) |> 
    spread(Type, species) |> 
    # rename those outcome columns
    rename_at(vars(-Query, -Subject, -OTU, -True_species, -True_family), ~ paste0(., '_outcome'))
  
  # and another table where we have whether those labels are correct or not, again one column per classifier
  label_spread <- correctness_table |> 
    select(-c(species, family, genus)) |> 
    spread(Type, CorrectSpecies) |> 
    # rename those outcome columns
    rename_at(vars(-Query, -Subject, -OTU, -True_species, -True_family), ~ paste0(., '_label'))
  
  # now we chuck that together
  together <- cbind(label_spread, 
                    outcome_spread |> select(-c(Query, Subject, OTU, True_species, True_family))) |> 
    # sort the columns so label and outcome are together
    select(sort(tidyselect::peek_vars())) |> 
    # get my 'leading' columns back to the front
    relocate(c(OTU, Query, Subject, True_family, True_species))
  
  together |>  mutate(
    Query = case_when(
      Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_12S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
      Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_16S_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
      Query == 'make_12s_16s_simulated_reads_7-Lutjanids_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Lutjanidae',
      Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_12S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
      Query == 'make_12s_16s_simulated_reads_8-Rottnest_runEDNAFLOW_16S_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
      Query == 'make_12s_16s_simulated_reads_8-Rottnest_Mock_runEDNAFlow_CO1_RESULTS_dada2_asv.fa' ~ 'Wadjemup',
      Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_12S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
      Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_16S_Lulu_RESULTS_dada2_asv.fa' ~ '100 Australian species',
      Query == 'make_12s_16s_simulated_reads_5-BetterDatabaseARTSimulation_runEDNAFLOW_CO1_RESULTS_dada2_asv.fa' ~ '100 Australian species'
    )
  ) |> 
    mutate(Subject = case_when(Subject == '12s_v010_final.fasta' ~ '12S',
                               Subject ==  '16S_v04_final.fasta' ~ '16S',
                               TRUE ~ 'COI'))
}
