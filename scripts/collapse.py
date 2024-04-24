from collections import Counter

import numpy as np
from ete3 import Tree


def collapse_zero_branches(tree, threshold):
    n_collapsed = 0
    for n in list(tree.traverse('postorder')):
        children = list(n.children)
        for child in children:
            if child.dist < threshold and not child.is_leaf():
                    n.remove_child(child)
                    for grandchild in child.children:
                        n.add_child(grandchild, dist=grandchild.dist + child.dist)
                    n_collapsed += 1
    print('Collapsed {} internal branches shorter than {}'.format(n_collapsed, threshold))


if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_nwk', required=True, type=str,
                        help="Path to the input ML tree (needs to be rooted)")
    parser.add_argument('--aln_len', required=True, type=int,
                        help="Length of the alignment that was used to reconstruct the ML tree")
    parser.add_argument('--out_nwk', required=True, type=str,
                        help="Path to the output tree with polytomies resolved")
    params = parser.parse_args()

    # Read the input tree
    tree = Tree(params.in_nwk)

    # Calculate one mutation per sequence length
    one_mutation = 1 / params.aln_len

    # Let's collapse all the branches that have less than 1/2 of a mutation on them,
    # as they are non-informative
    collapse_zero_branches(tree, one_mutation / 2)

    # Save the resolved tree  to the output file
    tree.write(outfile=params.out_nwk, format=5)

    # #also give a name for root
    # tree.name = "root"

    # # Create a new tree with a single node named "root"
    # new_root = Tree(name="root")

    # # Attach the original tree to the new root
    # new_root.add_child(tree)

    # # Save the new tree with the new root
    # new_root.write(outfile=params.out_nwk, format=1)  # format=1 includes internal node names

    #tree.write(outfile=params.out_nwk, format=1)

