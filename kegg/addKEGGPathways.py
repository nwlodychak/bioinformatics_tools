import argparse
import requests
import csv
import pandas as pd
import copy

def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Your script description (often top line of script's DocString; eg. Duplicate word n times)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Create a sequential argument (eg. it has to come in the order defined)
    parser.add_argument('-i', '--infile', # name of the argument, we will later use args.word to get this user input
                        metavar='INFILE', # shorthand to represent the input value
                        help='Input Blast Alignment File.', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default='Hello', # default option if no input is given by the user
                        required=True # whether this input must be given by the user, could also be True
                        )
    # Create a flagged argument (eg. input comes after a short "-i" or long "--input" form flag)
    parser.add_argument('-e', '--evalue', # name of the argument, we will later use args.number to get this user input
                        metavar='EVALUE', # shorthand to represent the input value
                        help='Significance value to filter for.', # message to the user, it goes into the help menu
                        type=float, # type of input expected, could also be int or float
                        default=1, # default option if no input is given by the user
                        required=False # whether this input must be given by the user, could also be True
                        )
    parser.add_argument('-O', '--outfile', # name of the argument, we will later use args.number to get this user input
                        metavar='OUTFILE', # shorthand to represent the input value
                        help='Output file to generate. Must be a csv format', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default='KEGGResults.csv', # default option if no input is given by the user
                        required=False # whether this input must be given by the user, could also be True
                        )


    return(parser.parse_args())

def getUniProtFromBlast(blast_line, threshold):
    """Return UniProt ID from the BLAST line if the evalue is below the threshold.

    Returns False if evalue is above threshold.
    """
    cleaned_line = blast_line.strip()
    blast_fields = cleaned_line.split("\t")
    if float(blast_fields[7]) < float(threshold):
        return(blast_fields[1])
    else:
        return(False)

def loadKeggPathways(): 
    """Return dictionary of key=pathID, value=pathway name from http://rest.kegg.jp/list/pathway/ko 

    Example: keggPathways["path:ko00564"] = "Glycerophospholipid metabolism"
    """
    keggPathways = {}
    result = requests.get('https://rest.kegg.jp/list/pathway/ko')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
        fields = str_entry.split("\t")
        keggPathways[fields[0]] = fields[1]
    return(keggPathways)

def getKeggGenes(uniprotID):
    """Return a list of KEGG organism:gene pairs for a provided UniProtID."""
    keggGenes = []
    result = requests.get(f'https://rest.kegg.jp/conv/genes/uniprot:{uniprotID}')
    if result.status_code == 200 and result.text.strip() != '':
        for entry in result.iter_lines():
            str_entry = entry.decode(result.encoding)
            fields = str_entry.split("\t")
            keggGenes.append(fields[1])
    else:
        keggGenes.append('{KEGG_GENE_NOT_FOUND}')
    return keggGenes
    
def getKeggOrthology(keggGenes):
    """Return a list of KEGG Orthology:gene pairs with a provided Kegg ID"""
    KeggOrthology = []
    result = requests.get(f'https://rest.kegg.jp/link/ko/{keggGenes}')
    if result.status_code == 200 and result.text.strip() != '':
        for entry in result.iter_lines():
            str_entry = entry.decode(result.encoding)
            fields = str_entry.split("\t")
            KeggOrthology.append(fields[1])
    else:
        print(f"Error querying KEGG API for Kegg Gene: {keggGenes}")
        KeggOrthology.append('{KO_NOT_FOUND}')
    return KeggOrthology

def getKeggPathIDs(KeggOrthology):
    """Return a list of KEGG PathIDs:KeggOrthology pairs for a provided Kegg Orthology ID."""
    KeggPathIDs = []
    result = requests.get(f'https://rest.kegg.jp/link/pathway/{KeggOrthology}')
    if result.status_code == 200 and result.text.strip() != '':
        for entry in result.iter_lines():
            str_entry = entry.decode(result.encoding)
            fields = str_entry.split("\t")
            KeggPathIDs.append(fields[1])
    else:
        print(f"Error querying KEGG API for Kegg Orthology: {KeggOrthology}")
        KeggPathIDs.append('{PATHWAY_ID_NOT_FOUND}')
    return KeggPathIDs

def search_pathway(ko_number, pathway):
    result = None
    for line in pathway:
        line = line.strip().split('\t')
        if line[0] == ko_number:
            result = line[1]
            break
    return result
    
if __name__ == "__main__":
    list_lines = []
    args = get_args()
    pathways = loadKeggPathways()
    with open(args.infile, 'r', newline='') as file:
        count = 0
        for line in file:
            uniprot = str(getUniProtFromBlast(line, args.evalue)).strip()
            if uniprot != False:
                keggGenes = getKeggGenes(uniprot)
                if keggGenes[0] != '{KEGG_GENE_NOT_FOUND}':
                    KeggOrthology = getKeggOrthology(str(keggGenes[0]))

                    if KeggOrthology[0] != '{KO_NOT_FOUND}':
                        KeggPathIDs = getKeggPathIDs(str(KeggOrthology[0]).strip())
                    else:
                        KeggPathIDs = ['{PATHWAY_ID_NOT_FOUND}']
                else: 
                    KeggOrthology = ['{KO_NOT_FOUND}']
                    KeggPathIDs = ['{PATHWAY_ID_NOT_FOUND}']

                cleaned_line = line.strip().split('\t')
                cleaned_line.append(keggGenes[0])
                cleaned_line.append(KeggOrthology[0])
                cleaned_line.append("{PATH_ID}")
                cleaned_line.append("{PATH_NAME}")
                if KeggPathIDs[0] != '{PATHWAY_ID_NOT_FOUND}':
                    for id in KeggPathIDs:
                        if "path:ko" in id:
                            pathway_name = pathways.get(id.split(':')[1])
                            new_line = copy.copy(cleaned_line)
                            new_line[-1] = pathway_name
                            new_line[-2] = id
                            list_lines.append(new_line)
                        else:
                            pass
                    else:
                       pass
            else:
                pass

            df=pd.DataFrame(list_lines)
            df.to_csv(args.outfile, index=False)
