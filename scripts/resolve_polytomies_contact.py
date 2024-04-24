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



# Function to find the MRCA and modify the tree for a given cluster
def modify_tree_for_cluster(tree, cluster, one_mutation):
    # Find the MRCA for the current cluster
    mrca = tree.get_common_ancestor(cluster)
    
    # List to hold nodes that need to be re-attached
    reattach_nodes = []

    # Iterate through children of the MRCA
    for child in mrca.get_children():
        # Check if the child is a leaf and in the cluster
        if child.is_leaf() and child.name in cluster:
            reattach_nodes.append(child)
        # For internal nodes, check if one of leaves under this node are in the cluster
        elif not child.is_leaf():
            #print(child)
            for leaf in child.get_leaves():
                if leaf.name in cluster:
                    reattach_nodes.append(child)
                    break
    
    # Create a new parent node with a tiny branch length and attach the detached nodes to it
    if reattach_nodes:
        #dist = np.random.random(1)[0] * min(min(*[child.dist for child in reattach_nodes]),one_mutation)
        #dist = 0.05+ min(min(*[child.dist for child in reattach_nodes]),one_mutation)
        dist = 0
        new_parent = mrca.add_child(dist=dist)
        for node in reattach_nodes:
            mrca.remove_child(node)
            node = new_parent.add_child(node,dist=node.dist + dist)


if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_nwk', required=True, type=str,
                        help="Path to the input ML tree (needs to be rooted)")
    parser.add_argument('--contact_file', required=True, type=str,
                        help="Path to the contact tracing data")
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

    # In polytomy_counter we will keep stats on how many polytomies of each size there were in the tree
    polytomy_counter = Counter()
    # Go through the tree and resolve polytomies
    
    # Read the CSV file to get the clusters
    csv_file_path = params.contact_file

    with open(csv_file_path, 'r') as file:
        for line in file:
            cluster = line.strip().split(',')
            #print(cluster)
            modify_tree_for_cluster(tree, cluster, one_mutation)
    
    for n in tree.traverse('postorder'):
        n_children = len(n.children)
        #avoid internal node just has one child caused by modify_tree_for_cluster function
        if not n.is_leaf() and n_children == 1:
            child = n.children[0]
            parent = n.up
            if parent:
                parent.remove_child(n)
                parent.add_child(child, dist=child.dist+n.dist)
            else: #root
                child.detach()
                tree = child
                
        if n_children > 2:
            polytomy_counter[n_children] += 1
            # While we have more than 2 children,
            # let's keep randomly picking two of them and putting them together
            while len(n.children) > 2:
                child1, child2 = np.random.choice(n.children, 2, replace=False)
                # Detach the two children
                n.remove_child(child1)
                n.remove_child(child2)
                # Let's pick a length for the new branch,
                # which will be between 0 and min(1 mutation and lengths of child branches)
                #dist = np.random.random(1)[0] * min(child2.dist, child1.dist, one_mutation)
                dist = 0
                #dist = 0.05+ min(child2.dist, child1.dist, one_mutation)
                #print(min(child2.dist, child1.dist, one_mutation))
                # Create a new branch
                parent = n.add_child(dist=dist)
                # Let's reattach the two children to the newly created branch,
                # at distances = their initial distance minus the length of their newly created common branch
                child1 = parent.add_child(child1, dist=child1.dist + dist)
                child2 = parent.add_child(child2, dist=child2.dist + dist)
        # elif n.is_leaf() and n.dist == 0:
        #     #n.dist = np.random.random(1)[0] * one_mutation
        #     n.dist = 0

    # Print polytomy stats
    print('Resolved {} polytomies in a tree of {} tips: {}'
          .format(sum(polytomy_counter.values()), len(tree),
                  ', '.join('{} of {}'.format(v, k)
                            for (k, v) in sorted(polytomy_counter.items(), key=lambda _: -_[0]))))

    # Save the resolved tree  to the output file
    tree.write(outfile=params.out_nwk, format=5)

