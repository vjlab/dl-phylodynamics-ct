import argparse
import pandas as pd
from ete3 import Tree
import random

def calculate_distances(input_file,percentage):
    # Load the tree from the file
    tree = Tree(input_file)

    # Calculate distances for each leaf to the root and store in a list
    tips = []
    int_nodes = []
    tips_name = []

    for node in tree.traverse("levelorder"):

        CIs = 1/365 #1 day
        distance_to_root = 2000+node.get_distance(tree) / 365  # Dividing each distance by 365

        if node.is_leaf():
            tips.append([node.name, distance_to_root])
            tips_name.append(node.name)
        elif not node.is_leaf():
            leaves = [leaf.name for leaf in node.iter_leaves()]
            #int_nodes.append(['mrca('+",".join(leaves)+')',distance_to_root])
            int_nodes.append(['mrca('+",".join(leaves)+')','b('+str(distance_to_root-CIs)+','+str(distance_to_root+CIs)+')'])

    #randomly pick p percentage 
    num_to_select = int(len(int_nodes) * percentage)
    int_nodes = random.sample(int_nodes, num_to_select)

    #make sure set the tmrca of root
    tips.insert(0, ['mrca('+",".join(tips_name)+')','b('+str(2000-CIs)+','+str(2000+CIs)+')'])
    #tips.insert(0, ['mrca('+",".join(tips_name)+')','b('+str(2000)+','+str(2000.02)+')'])
    
    return int_nodes,tips

def save_to_csv(int_nodes, tips, output_date, output_contact, write_type):
    
    if write_type == 0:
        df = pd.DataFrame(tips) #only for cluster info
    else:
        df = pd.DataFrame(tips+int_nodes)
    
    df.to_csv(output_date, index=False, header=False, sep='\t')

    df_int = pd.DataFrame(int_nodes)
    if not df_int.empty:
        df_contact = df_int.iloc[:, 0].str.replace('mrca', '',regex=False).str.replace('(', '',regex=False).str.replace(')', '',regex=False)
    else:
        df_contact = pd.DataFrame()
    df_contact.to_csv(output_contact, index=False, header=False, sep='\t')


def main():
    parser = argparse.ArgumentParser(description="Calculate distances from each leaf to the root of a phylogenetic tree and save to a CSV file.")
    
    parser.add_argument('-i', '--input', required=True, type=str, help='Input Newick tree file path')
    parser.add_argument('-od', '--output_date', required=True, type=str, help='Date output CSV file path')
    parser.add_argument('-oc', '--output_contact', required=True, type=str, help='Contact output CSV file path')
    parser.add_argument('-p', '--percentage', required=True, type=float, help='The percentage of data from the cluster is being extracted')
    parser.add_argument('-t', '--write_type', type=int, choices=[0, 1], default=0, help='Record dates for both tips and internal nodes (1), or for tips only (0)')

    args = parser.parse_args()

    # Calculate distances
    int_nodes, tips = calculate_distances(args.input,args.percentage)

    # Save to CSV
    save_to_csv(int_nodes, tips, args.output_date, args.output_contact, args.write_type)

if __name__ == "__main__":
    main()
