# Integrating contact tracing data to enhance outbreak phylodynamic inference: a deep learning approach 

Ruopeng Xie1,2,\*, Dillon C. Adam1, Shu Hu1,2, Benjamin J. Cowling1,3, Olivier Gascuel4, Anna Zhukova5,\*, Vijaykrishna Dhanasekaran1,2,\*


1 School of Public Health, LKS Faculty of Medicine, The University of Hong Kong; Hong Kong S.A.R., China

2 HKU-Pasteur Research Pole, School of Public Health, LKS Faculty of Medicine, The University of Hong Kong; Hong Kong S.A.R., China

3 Laboratory of Data Discovery for Health, Hong Kong Science and Technology Park, New Territories, Hong Kong S.A.R., China

4 Institut de Systématique, Evolution, Biodiversité (ISYEB, UMR 7205 – CNRS, MNHN, SU, EPHE, UA), Muséum National d’Histoire Naturelle, 45 rue Buffon, 75005 - Paris, France

5 Bioinformatics and Biostatistics Hub, Institut Pasteur, Université Paris Cité, 75015 Paris, France

*Corresponding author

## Abstract
Phylodynamics is central to understanding infectious disease dynamics through the integration of genomic and epidemiological data. Despite advancements, including the application of deep learning to overcome computational limitations, significant challenges persist due to data inadequacies and statistical unidentifiability of key parameters. These issues are particularly pronounced in poorly resolved phylogenies, commonly observed in outbreaks such as SARS-CoV-2. In this study, we conducted a thorough evaluation of  PhyloDeep, a deep learning inference tool for phylodynamics, assessing its performance on poorly resolved phylogenies. Our findings reveal the limited predictive accuracy of PhyloDeep (and other state-of-the-art approaches) in these scenarios. However, models trained on poorly resolved, realistically simulated trees demonstrate improved predictive power, despite not being infallible, especially in scenarios with superspreading dynamics, whose parameters are challenging to capture accurately. Notably, we observe markedly improved performance through the integration of minimal contact tracing data, which refines poorly resolved trees. Applying this approach to a sample of SARS-CoV-2 sequences partially matched to contact tracing from Hong Kong yields informative estimates of superspreading potential, extending beyond the scope of contact tracing data alone. Our findings demonstrate the potential for enhancing phylodynamic analysis through complementary data integration, ultimately increasing the precision of epidemiological predictions crucial for public health decision making and outbreak control.