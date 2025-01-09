BINF6309_Module9
================
Nick Wlodychak
2023-11-26

# Load Necessary Libraries and Data

Metagenomics is the study of broad microenviromental distribution of
bacteria or any genetic material in a given biome. We can do metagenomic
studies on the human gut or a soil sample on a rural farm.
`metagenomeSeq` is a novel normalization package in R that accounts for
under-sampling in a sample. metagenomeSeq is designed to determine
features that are differentially abundant between two or more groups of
multiple samples.

The code blocks in this .`rmd` are arranged to follow the tutorial
function from the `metagenomeSeq` vignette.

# Read in `BIOM` file and convert to a `MRexperiment` object

``` r
biom_file <- system.file("extdata", "min_sparse_otu_table.biom", package = "biomformat")
b <- read_biom(biom_file)
biom2MRexperiment(b)
```

    ## MRexperiment (storageMode: environment)
    ## assayData: 5 features, 6 samples 
    ##   element names: counts 
    ## protocolData: none
    ## phenoData: none
    ## featureData: none
    ## experimentData: use 'experimentData(object)'
    ## Annotation:

``` r
data("mouseData")
b <- MRexperiment2biom(mouseData)
write_biom(b, biom_file = "~/Desktop/otu_table.biom")
```

# Loading count data

This portion of the code sets the directory to store the data using the
`system.file` function, specifically referencing the “extdata” directory
within the “metagenomeSeq” package. The `loadMeta` function is used to
load count data from `CHK_NAME.otus.count.csv` located in the data
directory. The exact name of the file seems to be a placeholder
(CHK_NAME), which is typically replaced with the actual file name in
practical applications.

Using `dim(lung$counts)`, the dimensions of the count data are
determined. This helps us understand the size of the dataset being
worked with.

``` r
dataDirectory <- system.file("extdata", package = "metagenomeSeq")
lung = loadMeta(file.path(dataDirectory, "CHK_NAME.otus.count.csv"))
dim(lung$counts)
```

    ## [1] 1000   78

# Loading annotated taxonomy

The function `read.delim` is used to read a file containing taxonomy
data. The file is named `CHK_otus.taxonomy.csv`, located in the
previously defined `dataDirectory`.

The argument `stringsAsFactors = FALSE` ensures that string data in the
CSV file is read as plain text strings rather than being converted to
factors.

``` r
taxa = read.delim(file.path(dataDirectory, "CHK_otus.taxonomy.csv"),
stringsAsFactors = FALSE)
```

# Loading phenotype metadata

The `loadPhenoData` function is used to load phenotype metadata from
`CHK_clinical.csv`. We then use the match function is used to align the
names of the columns in `lung$counts` with the row names in the loaded
phenotype data (clin). This ensures the phenotype and meta data
correspond to one another. The phenotype data (clin) is reordered based
on the matching performed in the previous step.

``` r
clin = loadPhenoData(file.path(dataDirectory, "CHK_clinical.csv"), tran = TRUE)
ord = match(colnames(lung$counts), rownames(clin))
clin = clin[ord, ]
head(clin[1:2, ])
```

    ##                                          SampleType          SiteSampled
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2 Bronch2.PreWash Bronchoscope.Channel
    ## CHK_6467_E3B11_OW_V1V2                           OW           OralCavity
    ##                                     SmokingStatus
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2        Smoker
    ## CHK_6467_E3B11_OW_V1V2                     Smoker

# `MRexperiment` Object

`MRexperiment` takes a count matrix, `phenoData`, and `featureData` as
input. `phenotypeData` is created as an `AnnotatedDataFrame` from the
clinical data (`clin`). This structures the phenotype metadata for use
in the MRexperiment object.

`OTUdata` is created as another `AnnotatedDataFrame` from the taxonomy
data (`taxa`). This step formats the taxonomy data appropriately. The
`newMRexperiment` function is used to create the `MRexperiment` object
(obj). It combines the count matrix from `lung$counts`, the
`phenotypeData`, and the `featureData`. This object then represents a
complete dataset including count, phenotype, and taxonomy data.

We then display `phenotypeData`, `OTUdata`, and the newly created
`MRexperiment` object for initial inspection.

``` r
phenotypeData = AnnotatedDataFrame(clin)
OTUdata = AnnotatedDataFrame(taxa)
obj = newMRexperiment(lung$counts,phenoData=phenotypeData,featureData=OTUdata)
phenotypeData
```

    ## An object of class 'AnnotatedDataFrame'
    ##   rowNames: CHK_6467_E3B11_BRONCH2_PREWASH_V1V2 CHK_6467_E3B11_OW_V1V2
    ##     ... CHK_6467_E3B09_BAL_A_V1V2 (78 total)
    ##   varLabels: SampleType SiteSampled SmokingStatus
    ##   varMetadata: labelDescription

``` r
OTUdata
```

    ## An object of class 'AnnotatedDataFrame'
    ##   rowNames: 1 2 ... 1000 (1000 total)
    ##   varLabels: OTU Taxonomy ... strain (10 total)
    ##   varMetadata: labelDescription

``` r
obj
```

    ## MRexperiment (storageMode: environment)
    ## assayData: 1000 features, 78 samples 
    ##   element names: counts 
    ## protocolData: none
    ## phenoData
    ##   sampleNames: CHK_6467_E3B11_BRONCH2_PREWASH_V1V2
    ##     CHK_6467_E3B11_OW_V1V2 ... CHK_6467_E3B09_BAL_A_V1V2 (78 total)
    ##   varLabels: SampleType SiteSampled SmokingStatus
    ##   varMetadata: labelDescription
    ## featureData
    ##   featureNames: 1 2 ... 1000 (1000 total)
    ##   fvarLabels: OTU Taxonomy ... strain (10 total)
    ##   fvarMetadata: labelDescription
    ## experimentData: use 'experimentData(object)'
    ## Annotation:

# Loading relevant example datasets

The data function is used to load a dataset named `lungData`. After
loading, the `lungData` dataset is displayed and examined.

Here we use the data set **Human lung microbiome**.

The lung microbiome consists of respiratory flora sampled from six
healthy individuals. Three healthy nonsmokers and three healthy smokers.
The upper lung tracts were sampled by oral wash and oro-/nasopharyngeal
swabs. Samples were taken using two bronchoscopes, serial
bronchoalveolar lavage and lower airway protected brushes. (Paulson et
al. 2013)

Similarly, a dataset named `mouseData` is loaded using the data
function.

The mouse data set is **Humanized gnotobiotic mouse gut** \[2\].

Twelve germ-free adult male C57BL/6J mice were fed a low-fat, plant
polysaccharide-rich diet. Each mouse was gavaged with healthy adult
human fecal material. Following the fecal transplant, mice remained on
the low-fat, plant polysacchaaride-rich diet for four weeks, following
which a subset of 6 were switched to a high-fat and high-sugar diet for
eight weeks. Fecal samples for each mouse went through PCR amplification
of the bacterial 16S rRNA gene V2 region weekly. (Paulson et al. 2013)

These datasets, `lungData` and `mouseData`, are included as examples to
demonstrate the functionality of the `metagenomeSeq` package or for
comparison with the user’s own data. These serve as a turtorial to
compare experimental data sets and generate visual packages.

``` r
data(lungData)
lungData
```

    ## MRexperiment (storageMode: environment)
    ## assayData: 51891 features, 78 samples 
    ##   element names: counts 
    ## protocolData: none
    ## phenoData
    ##   sampleNames: CHK_6467_E3B11_BRONCH2_PREWASH_V1V2
    ##     CHK_6467_E3B11_OW_V1V2 ... CHK_6467_E3B09_BAL_A_V1V2 (78 total)
    ##   varLabels: SampleType SiteSampled SmokingStatus
    ##   varMetadata: labelDescription
    ## featureData
    ##   featureNames: 1 2 ... 51891 (51891 total)
    ##   fvarLabels: taxa
    ##   fvarMetadata: labelDescription
    ## experimentData: use 'experimentData(object)'
    ## Annotation:

``` r
data(mouseData)
mouseData
```

    ## MRexperiment (storageMode: environment)
    ## assayData: 10172 features, 139 samples 
    ##   element names: counts 
    ## protocolData: none
    ## phenoData
    ##   sampleNames: PM1:20080107 PM1:20080108 ... PM9:20080303 (139 total)
    ##   varLabels: mouseID date ... status (5 total)
    ##   varMetadata: labelDescription
    ## featureData
    ##   featureNames: Prevotellaceae:1 Lachnospiraceae:1 ...
    ##     Parabacteroides:956 (10172 total)
    ##   fvarLabels: superkingdom phylum ... OTU (7 total)
    ##   fvarMetadata: labelDescription
    ## experimentData: use 'experimentData(object)'
    ## Annotation:

# Useful commands to access `phenoData` and `pData` information

Functions like `phenoData(obj)` and `featureData(obj)` are used to
access phenotype and feature data within the `MRexperiment` object. The
`pData` and `fData` functions are utilized to inspect the first few
entries of the phenotype and feature data, respectively.

The portion of the code includes steps to filter and subset the data
based on certain criteria, like selecting features with a minimum number
of counts or samples with specific characteristics (e.g., smokers).

``` r
phenoData(obj)
```

    ## An object of class 'AnnotatedDataFrame'
    ##   sampleNames: CHK_6467_E3B11_BRONCH2_PREWASH_V1V2
    ##     CHK_6467_E3B11_OW_V1V2 ... CHK_6467_E3B09_BAL_A_V1V2 (78 total)
    ##   varLabels: SampleType SiteSampled SmokingStatus
    ##   varMetadata: labelDescription

``` r
head(pData(obj), 3)
```

    ##                                          SampleType          SiteSampled
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2 Bronch2.PreWash Bronchoscope.Channel
    ## CHK_6467_E3B11_OW_V1V2                           OW           OralCavity
    ## CHK_6467_E3B08_OW_V1V2                           OW           OralCavity
    ##                                     SmokingStatus
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2        Smoker
    ## CHK_6467_E3B11_OW_V1V2                     Smoker
    ## CHK_6467_E3B08_OW_V1V2                  NonSmoker

``` r
featureData(obj)
```

    ## An object of class 'AnnotatedDataFrame'
    ##   featureNames: 1 2 ... 1000 (1000 total)
    ##   varLabels: OTU Taxonomy ... strain (10 total)
    ##   varMetadata: labelDescription

``` r
head(fData(obj)[, -c(2, 10)], 3)
```

    ##   OTU superkingdom         phylum                  class             order
    ## 1   1     Bacteria Proteobacteria  Epsilonproteobacteria Campylobacterales
    ## 2   2         <NA>           <NA>                   <NA>              <NA>
    ## 3   3     Bacteria Actinobacteria Actinobacteria (class)   Actinomycetales
    ##               family         genus                  species
    ## 1 Campylobacteraceae Campylobacter     Campylobacter rectus
    ## 2               <NA>          <NA>                     <NA>
    ## 3   Actinomycetaceae   Actinomyces Actinomyces radicidentis

``` r
head(MRcounts(obj[, 1:2]))
```

    ##   CHK_6467_E3B11_BRONCH2_PREWASH_V1V2 CHK_6467_E3B11_OW_V1V2
    ## 1                                   0                      0
    ## 2                                   0                      0
    ## 3                                   0                      0
    ## 4                                   0                      0
    ## 5                                   0                      0
    ## 6                                   0                      0

``` r
featuresToKeep = which(rowSums(obj) >= 100)
samplesToKeep = which(pData(obj)$SmokingStatus == "Smoker")
obj_smokers = obj[featuresToKeep, samplesToKeep]
obj_smokers
```

    ## MRexperiment (storageMode: environment)
    ## assayData: 1 features, 33 samples 
    ##   element names: counts 
    ## protocolData: none
    ## phenoData
    ##   sampleNames: CHK_6467_E3B11_BRONCH2_PREWASH_V1V2
    ##     CHK_6467_E3B11_OW_V1V2 ... CHK_6467_E3B09_BAL_A_V1V2 (33 total)
    ##   varLabels: SampleType SiteSampled SmokingStatus
    ##   varMetadata: labelDescription
    ## featureData
    ##   featureNames: 570
    ##   fvarLabels: OTU Taxonomy ... strain (10 total)
    ##   fvarMetadata: labelDescription
    ## experimentData: use 'experimentData(object)'
    ## Annotation:

``` r
head(pData(obj_smokers), 3)
```

    ##                                          SampleType          SiteSampled
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2 Bronch2.PreWash Bronchoscope.Channel
    ## CHK_6467_E3B11_OW_V1V2                           OW           OralCavity
    ## CHK_6467_E3B11_BAL_A_V1V2                     BAL.A                 Lung
    ##                                     SmokingStatus
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2        Smoker
    ## CHK_6467_E3B11_OW_V1V2                     Smoker
    ## CHK_6467_E3B11_BAL_A_V1V2                  Smoker

``` r
head(normFactors(obj))
```

    ##                                     [,1]
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2   NA
    ## CHK_6467_E3B11_OW_V1V2                NA
    ## CHK_6467_E3B08_OW_V1V2                NA
    ## CHK_6467_E3B07_BAL_A_V1V2             NA
    ## CHK_6467_E3B11_BAL_A_V1V2             NA
    ## CHK_6467_E3B09_OP_V1V2                NA

``` r
normFactors(obj) <- rnorm(ncol(obj))
head(normFactors(obj))
```

    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2              CHK_6467_E3B11_OW_V1V2 
    ##                           0.1893954                           0.7057724 
    ##              CHK_6467_E3B08_OW_V1V2           CHK_6467_E3B07_BAL_A_V1V2 
    ##                           0.7085745                           0.5976035 
    ##           CHK_6467_E3B11_BAL_A_V1V2              CHK_6467_E3B09_OP_V1V2 
    ##                          -0.4671208                           1.5292341

``` r
head(libSize(obj))
```

    ##                                     [,1]
    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2    0
    ## CHK_6467_E3B11_OW_V1V2                16
    ## CHK_6467_E3B08_OW_V1V2                 1
    ## CHK_6467_E3B07_BAL_A_V1V2              2
    ## CHK_6467_E3B11_BAL_A_V1V2            118
    ## CHK_6467_E3B09_OP_V1V2                 5

``` r
libSize(obj) <- rnorm(ncol(obj))
head(libSize(obj))
```

    ## CHK_6467_E3B11_BRONCH2_PREWASH_V1V2              CHK_6467_E3B11_OW_V1V2 
    ##                           0.1322313                           1.1410630 
    ##              CHK_6467_E3B08_OW_V1V2           CHK_6467_E3B07_BAL_A_V1V2 
    ##                          -0.9370433                          -1.7019682 
    ##           CHK_6467_E3B11_BAL_A_V1V2              CHK_6467_E3B09_OP_V1V2 
    ##                           0.6882675                           1.3276561

``` r
filterData(mouseData, present = 10, depth = 1000)
```

    ## MRexperiment (storageMode: environment)
    ## assayData: 1057 features, 137 samples 
    ##   element names: counts 
    ## protocolData: none
    ## phenoData
    ##   sampleNames: PM1:20080108 PM1:20080114 ... PM9:20080303 (137 total)
    ##   varLabels: mouseID date ... status (5 total)
    ##   varMetadata: labelDescription
    ## featureData
    ##   featureNames: Erysipelotrichaceae:8 Lachnospiraceae:129 ...
    ##     Collinsella:34 (1057 total)
    ##   fvarLabels: superkingdom phylum ... OTU (7 total)
    ##   fvarMetadata: labelDescription
    ## experimentData: use 'experimentData(object)'
    ## Annotation:

``` r
newobj = mergeMRexperiments(mouseData, mouseData)
```

    ## MRexperiment 1 and 2 share sample ids; adding labels to sample ids.

# Normalization

Normalization in metagenomic analysis is essential to account for
varying depths of coverage across samples. Biasis introduced
experimentally, e.g from extraction of PCR must be taken into account to
ensure comparability . The **`cumNorm`** method calculates scaling
factors based on the sum of counts up to a certain quantile in each
sample.

These factors normalize the data, making the counts comparable across
samples by adjusting for different sequencing depths. **`wrenchNorm`**
offers an alternative normalization approach, such as grouping samples
by phenotypic characteristics, e.g diet in **`mouseData`**

``` r
data(lungData)
p = cumNormStatFast(lungData)
lungData = cumNorm(lungData, p = p)
condition = mouseData$diet
mouseData = wrenchNorm(mouseData, condition = condition)
```

    ## Warning: glm.fit: algorithm did not converge

    ## Warning: glm.fit: fitted probabilities numerically 0 or 1 occurred

    ## Warning: glm.fit: algorithm did not converge

    ## Warning: glm.fit: fitted probabilities numerically 0 or 1 occurred

    ## Warning: Partial NA coefficients for 8430 probe(s)

``` r
mat = MRcounts(lungData, norm = TRUE, log = TRUE)[1:5, 1:5]
exportMat(mat, file = file.path(dataDirectory, "tmp.tsv"))
exportStats(lungData[, 1:5], file = file.path(dataDirectory,
"tmp.tsv"))
```

    ## Default value being used.

``` r
head(read.csv(file = file.path(dataDirectory, "tmp.tsv"), sep = "\t"))
```

    ##                               Subject Scaling.factor Quantile.value
    ## 1 CHK_6467_E3B11_BRONCH2_PREWASH_V1V2             67              2
    ## 2              CHK_6467_E3B11_OW_V1V2           2475              1
    ## 3              CHK_6467_E3B08_OW_V1V2           2198              1
    ## 4           CHK_6467_E3B07_BAL_A_V1V2            836              1
    ## 5           CHK_6467_E3B11_BAL_A_V1V2           1008              1
    ##   Number.of.identified.features Library.size
    ## 1                            60          271
    ## 2                          3299         7863
    ## 3                          2994         8360
    ## 4                          1188         5249
    ## 5                          1098         3383

# Statistical Testing

One of the benefits of `metagenomeSeq` is its power to address
undersampling and detection of differentially abundant features (OTUs,
genes, etc). (Paulson et al. 2013) Once the data has been normalized,
statistical models can be applied to the data sets.

Here the data example uses `fitFeatureModel` for differential abundance
testing by comparing smoker's and non-smokers lung microbiome.

``` r
data(lungData)
lungData = lungData[, -which(is.na(pData(lungData)$SmokingStatus))]
lungData = filterData(lungData, present = 30, depth = 1)
lungData <- cumNorm(lungData, p = 0.5)
pd <- pData(lungData)
mod <- model.matrix(~1 + SmokingStatus, data = pd)
lungres1 = fitFeatureModel(lungData, mod)
head(MRcoefs(lungres1))
```

    ##           logFC        se      pvalues   adjPvalues
    ## 3465  -4.824949 0.5697511 0.000000e+00 0.000000e+00
    ## 35827 -4.304266 0.5445548 2.664535e-15 1.079137e-13
    ## 2817   2.320656 0.4324661 8.045793e-08 1.629273e-06
    ## 2735   2.260203 0.4331098 1.803341e-07 2.921412e-06
    ## 5411   1.748296 0.3092461 1.572921e-08 4.246888e-07
    ## 48745 -1.645805 0.3293117 5.801451e-07 7.831959e-06

<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-Knight_Vrbanac_Taylor_Aksenov_Callewaert_Debelius_Gonzalez_Kosciolek_McCall_McDonald_Melnik_Morton_Navas_Quinn_Sanders_Swafford_Thompson_Tripathi_Xu_Zaneveld_Zhu_Caporaso_Dorrestein_2018"
class="csl-entry">

Knight, Rob, Alison Vrbanac, Bryn C. Taylor, Alexander Aksenov, Chris
Callewaert, Justine Debelius, Antonio Gonzalez, et al. 2018. “Best
Practices for Analysing Microbiomes.” *Nature Reviews Microbiology* 16
(7): 410–22. <https://doi.org/10.1038/s41579-018-0029-9>.

</div>

<div id="ref-Paulson_Stine_Bravo_Pop_2013" class="csl-entry">

Paulson, Joseph N., O. Colin Stine, Héctor Corrada Bravo, and Mihai Pop.
2013. “Differential abundance analysis for microbial marker-gene
surveys.” *Nature methods* 10 (12): 1200–1202.
<https://doi.org/10.1038/nmeth.2658>.

</div>

<div id="ref-Quince_Walker_Simpson_Loman_Segata_2017" class="csl-entry">

Quince, Christopher, Alan W. Walker, Jared T. Simpson, Nicholas J.
Loman, and Nicola Segata. 2017. “Shotgun metagenomics, from sampling to
analysis.” *Nature biotechnology* 35 (9): 833–44.
<https://doi.org/10.1038/nbt.3935>.

</div>

</div>
