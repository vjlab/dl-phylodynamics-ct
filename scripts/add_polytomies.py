#!/usr/bin/env python3

import sys
import argparse
import random

import numpy as np
import pandas as pd
from scipy.stats import linregress

from ete3 import Tree
from collections import Counter
from math import floor
import dendropy

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm
def choose_val(val_range):
    """
    returns a random value within given logten range
    :param val_range: str, format: 'min:max', if min>max, then negative values of both parameters are used
    :return: float, random logten value
    """
    try:
        min_val, max_val = val_range.split(";")
        min_val = float(min_val)
        max_val = float(max_val)
        if min_val > max_val:
            min_val = -min_val
            max_val = -max_val
    except ValueError:
        print("Choose_val: the argument must be a string of form 'x_min;x_max'")
    val = 10**((np.random.random()*(max_val-min_val))+min_val)
    return val


def rescale_tree(tre, sc_factor):
    """
    Modifies the input tree branches by dividing its length by given scaling factor
    :param tre: ete3.Tree, tre to be modified
    :param sc_factor: float, scaling factor by which the tree branches will be modified
    :return: void, the original tree is modified
    """
    for node in tre.traverse():
        node.dist = node.dist/sc_factor
    return None


def discretize_branch_lengths(tre, nb_sites):
    """
    Modifies the input tree branch lengths, proportionate to heuristically occurred mutations
    :param tre: ete3.Tree, tree to be modified
    :param mut_rate: float, mutation rate (mutation per site per year)
    :param nb_sites: int, number of sites in sequence
    :return: void, the original tree is modified
    """

    # Define the mean and standard deviation for the log-normal distribution
    mean_clock_rate = 0.0008   # mean of 0.001 subs/site/year
    sigma = 0.0004  # standard deviation of 0.03

    # Calculate the parameters for the underlying normal distribution
    # These calculations transform the mean and standard deviation of the log-normal distribution
    # to the mean (mu) and standard deviation (sigma) of the associated normal distribution
    mu = np.log(mean_clock_rate**2 / np.sqrt(mean_clock_rate**2 + sigma**2))
    sigma = np.sqrt(np.log(1 + (sigma**2 / mean_clock_rate**2)))

    # Create a log-normal distribution with the calculated parameters
    dist = lognorm(s=sigma, scale=np.exp(mu))

    for node in tre.traverse():
        orig_node_dist = node.dist
        node.dist = np.random.binomial(n=nb_sites, p=dist.rvs(1)[0]*orig_node_dist)  # keep it as number of mutations
        # node.dist = np.random.binomial(n=nb_sites, p=mut_rate * orig_node_dist) / nb_sites
    return None


def count_zero_length_branches(tre):
    """
    returns the number of zero length branches
    :param tre: ete3.Tree, tree on which the 0-length branches are counted
    :return: int, count
    """
    count = 0
    for node in tre.traverse():
        if node.dist == 0:
            count += 1
    return count


def write_output(tree, info, write_tree_flag, prefix):
    info_csv_filename = f"{prefix}_output.csv"
    #info.to_csv(path_or_buf=info_csv_filename, sep='\t', index=True, index_label='Index')

    if write_tree_flag == 1:
        newick_filename = f"{prefix}_output.nwk"  
        newick_str = tree.write(format=5)
        with open(newick_filename, "w") as out_tree_file:
            out_tree_file.write(newick_str)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a single tree')
    parser.add_argument('-t', '--tree', type=str, required=True, help='Path to the tree file on which we work')
    parser.add_argument('--write_trees', type=int, choices=[0, 1], default=0, help='Write down modified tree (1), or not (0)')
    parser.add_argument('--scale', type=str, required=True, choices=['day', 'week', 'year'], help='Discretization noise parameter, the timescale of the input tree: day, week or year')
    parser.add_argument('--seq_size', type=str, required=True, help='Discretization noise parameter: presumed sequence length [bp], in form: "min;max"')
    parser.add_argument('--prefix', type=str, help="Prefix for the output file name")

    # Load arguments
    args = parser.parse_args()
    tree = str(args.tree)
    prefix = args.prefix


    write_trees = int(args.write_trees)
    
    seq_length = int(args.seq_size)
    scale = str(args.scale).lower()
    try:
        if scale == "week":
            scale = 52.1429
        elif scale == "year":
            scale = 1
        elif scale == "day":
            scale = 365
    except ValueError:
        print("scale can only be set to year, week or day")

    # open and convert single tree
    with open(args.tree, mode="r") as curs:
        tree_data = curs.read().replace("\n", "")
    tr = Tree(tree_data + ";", format=1)

    # handle tree
    rescale_tree(tr, scale)
    discretize_branch_lengths(tre=tr, nb_sites=seq_length)

    # output info
    output_info = pd.DataFrame(index=[0], columns=["zero_length_branches", "total_branches"])
    output_info.loc[0, ['zero_length_branches']] = count_zero_length_branches(tr)
    output_info.loc[0, ['total_branches']] = 2*len(tr)-2

    # write output
    write_output(tr, output_info, args.write_trees,prefix)
