#!/usr/bin/env Rscript
# de.R
library(tximport, warn.conflicts = FALSE, quietly=TRUE)
library(readr, warn.conflicts = FALSE, quietly=TRUE)
library(DESeq2, warn.conflicts = FALSE, quietly=TRUE)
library(dplyr, warn.conflicts = FALSE, quietly=TRUE)
library(knitr)


# Define constants
# Note: parent directory must be in the top level of the module. e.g. ../module04-nwlodychak
PARENTDIR <- "/home/wlodychak.s/BINF6309/module04-nwlodychak"
TESTING <- FALSE # Change to FALSE if using entire Samples set
RESULTS_DIR <- file.path(PARENTDIR, "results")
AIPTASIA_DIR <- file.path(PARENTDIR, "AiptasiaMiSeq")
ANNOTATION_DIR <- file.path(PARENTDIR, "Annotation")


# True script begins
tx2gene <- read.csv(file.path(RESULTS_DIR, "tx2gene.csv"))
head(tx2gene)


if (TESTING) {
  # for testing purposes - alternative samples table
  testing_samples <- data.frame(Sample = c("Aip02", "Aip02", "Aip02", "Aip02"),
                                Menthol = c("Control", "Control", "Menthol", "Menthol"),
                                Vibrio = c("Control", "Vibrio", "Control", "Vibrio"))
  head(testing_samples)
  print("***Running test with Aip02 only***")
  samples <- testing_samples
} else {
  samples <- read.csv(file.path(AIPTASIA_DIR, "Samples.csv"), header=TRUE)
  kable(head(samples))
}


files <- file.path(RESULTS_DIR, "quant", samples$Sample, "quant.sf")
txi <- tximport(files, type="salmon", tx2gene=tx2gene)

dds <- DESeqDataSetFromTximport(txi, colData = samples, 
                                design = ~ Menthol + Vibrio)

dds$Vibrio <- relevel(dds$Vibrio, ref = "Control")
dds$Menthol <- relevel(dds$Menthol, ref = "Control")
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]
dds <- DESeq(dds)


padj <- .05
minLog2FoldChange <- .5
dfAll <- data.frame()
# Get all DE results except Intercept, and "flatten" into a single file.
for (result in resultsNames(dds)){
  if(result != 'Intercept'){
    res <- results(dds, alpha=.05, name=result)
    dfRes <- as.data.frame(res)
    dfRes <- subset(subset(dfRes, select=c(log2FoldChange, padj)))
    dfRes$Factor <- result
    dfRes$ko <- rownames(dfRes)
    dfAll <- rbind(dfAll, dfRes)
  }
}
rownames(dfAll) <- NULL
kable(head(dfAll))
write.csv(dfAll, file=file.path(RESULTS_DIR, "dfAll.csv"))


# Filter for padj < 0.05
dfFiltered <- subset(dfAll, padj < 0.05)

dfPathways <- read.table(file.path(ANNOTATION_DIR, "path.txt"),
                      header=FALSE,
                      sep="\t",
                      col.names=c("ko", "path"))
kable(head(dfPathways))
dfKo <- read.table(file.path(ANNOTATION_DIR, "ko"),
                    header=FALSE,
                    sep="\t",
                    col.names=c("path", "description"))
kable(head(dfKo))
# Merge with path.txt and ko information
dfMerged <- dfFiltered %>%  left_join(dfPathways, by="ko") %>%  left_join(dfKo, by="path")
# Selecting the specified columns
dfFinal <- dfMerged %>% select(ko, path, description, log2FoldChange, padj, Factor)
# Write the final data to deAnnotated.
write.csv(dfFinal, file.path(RESULTS_DIR, "deAnnotated.csv"), row.names=FALSE)
kable(head(dfFinal))

# end of de.R script
