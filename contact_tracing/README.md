# Contact Tracing
Integration of contact tracing data into phylogenetic trees

## An example to refine the tree using 50% contact tracing data during simulations

Only integrate cluster information:
```bash
# extract tip dates and cluster information from Baseline Tree
python ../scripts/get_dates_cluster_time.py -i ../tree_simulations/trees/baseline_tree.nwk -p 0.5 -od contact_data/date.tsv -oc contact_data/contact_0.5.csv -t 0

#insert how many lines in the first row of dates file
sed -i '' "1s/^/$(wc -l < contact_data/date.tsv | awk '{$1=$1};1')\n/" contact_data/date.tsv

# resolve polytomies according to cluster information
python ../scripts/resolve_polytomies_contact.py --contact_file contact_data/contact_0.5.csv --in_nwk ../tree_simulations/trees/genetic_polytomous_tree.nwk --aln_len 1 --out_nwk refined_trees/genetic_resolved_tree.cluster.0.5.nwk

# rescale genetic distance tree
python ../scripts/rescale_tree.py -i refined_trees/genetic_resolved_tree.cluster.0.5.nwk -o refined_trees/genetic_resovled_rescale_tree.cluster.0.5.nwk -s 29903

# dating using LDS2
lsd2_mac -i refined_trees/genetic_resovled_rescale_tree.cluster.0.5.nwk -d contact_data/date.tsv -l -1 -s 29903 -w ../tree_simulations/trees/clock.txt -q 0.0004 -u 0.0001141552511 -U 0.0001141552511 -r l

# convert to nwk and rename
gotree reformat newick -f nexus -i refined_trees/genetic_resovled_rescale_tree.cluster.0.5.nwk.result.date.nexus -o refined_trees/dated_resovled_tree.cluster.0.5.nwk
```
Integrate cluster infromation and infection times:
```bash
# extract tip dates, cluster information and infection times from Baseline Tree
python ../scripts/get_dates_cluster_time.py -i ../tree_simulations/trees/baseline_tree.nwk -p 0.5 -od contact_data/date_ct_0.5.tsv -oc contact_data/contact_0.5.csv -t 1

#insert how many lines in the first row of dates file
sed -i '' "1s/^/$(wc -l < contact_data/date_ct_0.5.tsv | awk '{$1=$1};1')\n/" contact_data/date_ct_0.5.tsv

# resolve polytomies according to cluster information
python ../scripts/resolve_polytomies_contact.py --contact_file contact_data/contact_0.5.csv --in_nwk ../tree_simulations/trees/genetic_polytomous_tree.nwk --aln_len 1 --out_nwk refined_trees/genetic_resolved_tree.cluster.infection.0.5.nwk

# rescale genetic distance tree
python ../scripts/rescale_tree.py -i refined_trees/genetic_resolved_tree.cluster.infection.0.5.nwk -o refined_trees/genetic_resovled_rescale_tree.cluster.infection.0.5.nwk -s 29903

# dating using LDS2
lsd2_mac -i refined_trees/genetic_resovled_rescale_tree.cluster.infection.0.5.nwk -d contact_data/date_ct_0.5.tsv -l -1 -s 29903 -w ../tree_simulations/trees/clock.txt -q 0.0004 -u 0.0001141552511 -U 0.0001141552511 -r l

# convert to nwk and rename
gotree reformat newick -f nexus -i refined_trees/genetic_resovled_rescale_tree.cluster.infection.0.5.nwk.result.date.nexus -o refined_trees/dated_resovled_tree.cluster.infection.0.5.nwk
```