
library(dada2)
seq_files <- list.files('.', '*fasta$', full.names = TRUE)
for(training_fasta in seq_files) {
	base_t <- basename(training_fasta)
	for(s in list.files('../../', '*fa$', full.names = TRUE)){
		base_s <- basename(s)
		out <- paste0(base_s, '_vs_', base_t, '.csv')
		out80 <- paste0(base_s, '_vs_', base_t, '.80perc.csv')
		out95 <- paste0(base_s, '_vs_', base_t, '.95perc.csv')
		seqs <- getSequences(s)
		taxa <- assignTaxonomy(seqs, training_fasta, multithread=50, tryRC=TRUE)
		write.csv(as.data.frame(taxa), out)
		taxa80 <-  assignTaxonomy(seqs, training_fasta, minBoot=80, multithread=50, tryRC=TRUE)
		write.csv(as.data.frame(taxa80), out80)
		taxa95 <-  assignTaxonomy(seqs, training_fasta, minBoot=95, multithread=50, tryRC=TRUE)
		write.csv(as.data.frame(taxa95), out95)
	}
}
#seqs <- getSequences('../LULU_curated_fasta_RS19_MiFish.fa')
#training_fasta <- '12S_fish_and_genomes.reformatted.noVagueSpecies.forAssignTaxonomy.fasta'
#taxa <- assignTaxonomy(seqs, training_fasta, multithread=50, tryRC=TRUE)
#taxa80 <-  assignTaxonomy(seqs, training_fasta, minBoot=80, multithread=50, tryRC=TRUE)
#write.csv(as.data.frame(taxa80), 'LULU_curated_fasta_RS19_MiFish.assignTaxonomy.Raw.csv')
#write.csv(as.data.frame(taxa80), 'LULU_curated_fasta_RS19_MiFish.assignTaxonomy.Bootstrap80.csv')
#
#seqs <- getSequences('../RS19_MiFish.fa')
#taxa <- assignTaxonomy(seqs, training_fasta, multithread=50, tryRC=TRUE)
#taxa80 <-  assignTaxonomy(seqs, training_fasta, minBoot=80, multithread=50, tryRC=TRUE)
#write.csv(as.data.frame(taxa80), 'RS19_MiFish.Raw.csv')
#write.csv(as.data.frame(taxa80), 'RS19_MiFish.Bootstrap80.csv')
