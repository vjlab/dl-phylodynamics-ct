# Tree Simulations
Simulations of phylogenetic trees

## 'Ideal' Tree (Baseline Tree)

The following command lines simulate a tree with 200-1000 tips under BDSS model using [treesimulator](https://github.com/evolbioinfo/treesimulator), with R<sub>0</sub>=3.43, X<sub>ss</sub>=28.77, f<sub>ss</sub>=0.24, infectious period=6.70, sampling proportion=0.36, and saves it to a file trees/baseline_tree.nwk, while saving the parameters to a comma-separated file trees/parameters.csv

```bash
R=3.43
x=28.77
f=0.24
ip=6.70
p=0.36
        
psi=`bc -l <<< "1/$ip"`
fx=`bc -l <<< $f*$x`
la=`bc -l <<< "$R/$ip"`
bss=`bc -l <<< "$la*$fx/($fx+1-$f)"`
bns=`bc -l <<< "$bss/$x"`
bnn=`bc -l <<< "$la-$bss"`
bsn=`bc -l <<< "$bnn*$x"`

generate_bdss --min_tips 200 --max_tips 1000 \
--la_nn $bnn \
--la_ns $bns \
--la_sn $bsn \
--la_ss $bss \
--psi $psi \
--p $p \
--nwk trees/baseline_tree.nwk \
--log trees/parameters.csv
```

## Genetic Baseline Tree
Baseline Tree are transformed into Genetic Baseline tree, with branch lengths determined by a binomial process, B (n=sequence length, p=evolutionary rate × branch length of time-scaled trees).
```bash
python ../scripts/add_polytomies.py -t trees/baseline_tree.nwk --write_trees 1 --scale day --seq_size 29903 --prefix trees/genetic_baseline_tree

mv trees/genetic_baseline_tree_output.nwk trees/genetic_baseline_tree.nwk
```

## Dated Baseline Tree
Dating Genetic Baseline Tree using [LSD2](https://github.com/tothuhien/lsd2) with a minimal branch length of one hour
```bash
# get tip dates from Baseline Tree
python ../scripts/get_dates_cluster_time.py -i trees/baseline_tree.nwk -p 0 -od trees/date.tsv -oc ../contact_tracing/contact_data/contact_0.csv -t 0

#insert how many lines in the first row of dates file
sed -i '' "1s/^/$(wc -l < trees/date.tsv | awk '{$1=$1};1')\n/" trees/date.tsv

# rescale genetic distance tree
python ../scripts/rescale_tree.py -i trees/genetic_baseline_tree.nwk -o trees/genetic_baseline_rescale_tree.nwk -s 29903

# dating using LDS2
lsd2_mac -i trees/genetic_baseline_rescale_tree.nwk -d trees/date.tsv -l -1 -s 29903 -w trees/clock.txt -q 0.0004 -u 0.0001141552511 -U 0.0001141552511 -r l

# convert to nwk and rename
gotree reformat newick -f nexus -i trees/genetic_baseline_rescale_tree.nwk.result.date.nexus -o trees/dated_baseline_tree.nwk
```

## Genetic Polytomous Tree
In Genetic Baseline tree, branches representing zero mutation are collapsed to form Genetic Polytomous Tree
```bash
python ../scripts/collapse.py --in_nwk trees/genetic_baseline_tree.nwk --out_nwk trees/genetic_polytomous_tree.nwk --aln_len 1
```

## Dated Polytomous Tree
Dating Genetic Polytomous Tree using [LSD2](https://github.com/tothuhien/lsd2) with a minimal branch length of one hour
```bash
# rescale genetic distance tree
python ../scripts/rescale_tree.py -i trees/genetic_polytomous_tree.nwk -o trees/genetic_polytomous_rescale_tree.nwk -s 29903

# dating using LDS2
lsd2_mac -i trees/genetic_polytomous_rescale_tree.nwk -d trees/date.tsv -l -1 -s 29903 -w trees/clock.txt -q 0.0004 -u 0.0001141552511 -U 0.0001141552511 -r l

# convert to nwk and rename
gotree reformat newick -f nexus -i trees/genetic_polytomous_rescale_tree.nwk.result.date.nexus -o trees/dated_polytomous_tree.nwk
```

## Genetic Resovled Tree
Resolve polytomies by randomly coalescing two offspring until binary trees
```bash
python ../scripts/resolve_polytomies_contact.py --contact_file ../contact_tracing/contact_data/contact_0.csv --in_nwk trees/genetic_polytomous_tree.nwk --aln_len 1 --out_nwk trees/genetic_resolved_tree.nwk
```

## Dated Resolved Tree
Dating Genetic Resolved Tree using [LSD2](https://github.com/tothuhien/lsd2) with a minimal branch length of one hour
```bash
# rescale genetic distance tree
python ../scripts/rescale_tree.py -i trees/genetic_resolved_tree.nwk -o trees/genetic_resovled_rescale_tree.nwk -s 29903

# dating using LDS2
lsd2_mac -i trees/genetic_resovled_rescale_tree.nwk -d trees/date.tsv -l -1 -s 29903 -w trees/clock.txt -q 0.0004 -u 0.0001141552511 -U 0.0001141552511 -r l

# convert to nwk and rename
gotree reformat newick -f nexus -i trees/genetic_resovled_rescale_tree.nwk.result.date.nexus -o trees/dated_resovled_tree.nwk
```

## Examples of seven types of phylogenetic trees used in simulations
![Fig.1](dl-phylodynamics-ct/tree_simulations/tree_simulation.png)