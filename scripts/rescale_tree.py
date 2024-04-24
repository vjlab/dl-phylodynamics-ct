import argparse
from ete3 import Tree

def rescale_tree(tre, sc_factor):
    """
    Modifies the input tree branches by dividing its length by given scaling factor.
    :param tre: ete3.Tree, tree to be modified
    :param sc_factor: float, scaling factor by which the tree branches will be modified
    :return: void, the original tree is modified
    """
    for node in tre.traverse():
        node.dist /= sc_factor


def main():
    parser = argparse.ArgumentParser(description='Rescale branches of a phylogenetic tree.')
    parser.add_argument('-i', '--input_tree', required=True, type=str, help='Input file path for the Newick tree')
    parser.add_argument('-o', '--output_tree', required=True, type=str, help='Output file path for the rescaled Newick tree')
    parser.add_argument('-s', '--scale_factor', required=True, type=float, help='Scaling factor to modify the tree branches')
    args = parser.parse_args()

    # Load the tree
    tree = Tree(args.input_tree)
    # Rescale the tree
    rescale_tree(tree, args.scale_factor)
    # Save the rescaled tree
    tree.write(outfile=args.output_tree)

if __name__ == "__main__":
    main()
