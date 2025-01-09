/*
========================================================================================
    IMPORT MODULES
========================================================================================
*/

include { filter_reads }                  from '../modules/filter_reads/main.nf'
include { umi_extraction }                from '../modules/umi_extraction/main.nf'
include { umi_clustering }                from '../modules/umi_clustering/main.nf'
include { call_consensus }                from '../modules/call_consensus/main.nf'
include { gather_stats }                  from '../modules/gather_stats/main.nf'

/*
