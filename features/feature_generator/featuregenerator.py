import warnings
import pandas as pd
from encoding import encode_into_summary_statistics, encode_into_most_recent
from tree_utilities import *
#from Bio import Phylo

warnings.filterwarnings("ignore")



def featuregenerator(tree_file, epidemiological_parameters,encoding_method, **kvargs):
	
	# read epidemiological parameters
	epi_param = pd.read_csv(epidemiological_parameters)
	
	features = pd.DataFrame()
	
	with open(tree_file,'r') as f:
		filelines = f.readlines()
		row = 0
		for fileline in filelines:
			tree = read_tree_file(fileline)
			if encoding_method == "SUMSTATS":
				encoded_tree, rescale_factor = encode_into_summary_statistics(tree, epi_param.iloc[row,2])
				encoded_tree[len(encoded_tree.columns)] = rescale_factor
    			#encoded_tree, rescale_factor = encode_into_summary_statistics(tree, proba_sampling)
			elif encoding_method == "FULL":
				encoded_tree, rescale_factor = encode_into_most_recent(tree, epi_param.iloc[row,2])
    			#encoded_tree, rescale_factor = encode_into_most_recent(tree, proba_sampling)
			row = row + 1
			#print(encoded_tree)
			features = pd.concat([features,encoded_tree])
	
	return features
		


def main():

	import argparse

	parser = argparse.ArgumentParser(description="feature generator ",
                                     prog='featuregenerator')

	tree_group = parser.add_argument_group('tree-related arguments')
	tree_group.add_argument('-t', '--tree_file', help="input tree in newick format (must be rooted, without polytomies"
                                                      " and containing at least 50 tips).",
                            type=str, required=True)
	tree_group.add_argument('-p', '--epidemiological_parameters', help="input epidemiological parameter file in csv.gz format",
                            type=str, required=True)
	tree_group.add_argument('-e', '--encoding_method', help="SUMSTATS or FULL",
                            type=str, required=True)
	output_group = parser.add_argument_group('output')
	output_group.add_argument('-o', '--output', required=True, type=str, help="The name of the output file.")

	params = parser.parse_args()

	inference = featuregenerator(**vars(params))
	
	inference.to_csv(params.output,index=False)


if '__main__' == __name__:
    main()
