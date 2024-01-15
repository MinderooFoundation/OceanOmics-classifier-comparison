# A collection of smaller helper scripts

precision <- function(TP, FP) {
  if (TP + FP == 0) {
    # when a classifier returns garbage we get many errors
    return(0)
    }
  TP / (TP + FP )
}
recall <- function(TP, FN) {
  if (TP + FN == 0) {
    return(0)
  }
  TP / (TP + FN)
}
f1 <- function(precision, recall) {
  if(precision + recall == 0){
    return(0)
  }
  2*precision * recall / (precision + recall)
}
f0.5 <- function(precision, recall) {
  if(precision + recall == 0){
    return(0)
  }
  ((1 + 0.5^2) * precision * recall) / (0.5^2 * precision + recall)
}
accuracy <- function(TP, FP, FN, TN) {
  (TN + TP) / (TN + TP + FP + FN)
}

my_save_plot <- function(plot, name) {
  ggsave(filename = paste0('results/figures/', name, '.png'),
         plot = plot, dpi = 300, width = 10, height = (9/16)*10 )
  ggsave(filename = paste0('results/figures/', name, '.svg'),
         plot = plot, dpi = 300, width = 10, height = (9/16)*10 )
}

my_save_table <- function(table, name) {
  if(is.data.frame(table)) {
    # i'll round to two decimals
    table <- table |> mutate(across(where(is.numeric), \(x) round(x, 2)))
  } 
  writexl::write_xlsx(table, path = paste0('results/tables/', name, '.xlsx'))
}
