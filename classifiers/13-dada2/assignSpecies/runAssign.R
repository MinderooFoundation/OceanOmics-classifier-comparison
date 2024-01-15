library(dada2)
seq_files <- list.files('.', '*fasta$', full.names = TRUE)
for(training_fasta in seq_files) {
	base_t <- basename(training_fasta)
	for(s in list.files('../../', '*fa$', full.names = TRUE)){
		base_s <- basename(s)
		out <- paste0(base_s, '_vs_', base_t, '.Species.csv')
		seqs <- getSequences(s)
		spec <- assignSpecies(seqs, training_fasta, tryRC=TRUE, allowMultiple = TRUE)
		write.csv(as.data.frame(spec), out)
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
