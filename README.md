# Deep learning of SARS-CoV-2 outbreak phylodynamics with contact tracing data

Ruopeng Xie1,2,\*, Dillon C. Adam1, Shu Hu1,2, Benjamin J. Cowling1,3, Olivier Gascuel4, Anna Zhukova5,\*, Vijaykrishna Dhanasekaran1,2,\*


1 School of Public Health, LKS Faculty of Medicine, The University of Hong Kong; Hong Kong S.A.R., China

2 HKU-Pasteur Research Pole, School of Public Health, LKS Faculty of Medicine, The University of Hong Kong; Hong Kong S.A.R., China

3 Laboratory of Data Discovery for Health, Hong Kong Science and Technology Park, New Territories, Hong Kong S.A.R., China

4 Institut de Systématique, Evolution, Biodiversité (ISYEB, UMR 7205 – CNRS, MNHN, SU, EPHE, UA), Muséum National d’Histoire Naturelle, 45 rue Buffon, 75005 - Paris, France

5 Bioinformatics and Biostatistics Hub, Institut Pasteur, Université Paris Cité, 75015 Paris, France

*Corresponding author

## Abstract
Deep learning has emerged as a powerful tool for phylodynamic analysis, addressing common computational limitations affecting existing methods. However, notable disparities exist between simulated phylogenetic trees used for training existing deep learning models and those derived from real-world sequence data, necessitating a thorough examination of their practicality. We conducted a comprehensive evaluation of model performance by assessing an existing deep learning inference tool for phylodynamics, PhyloDeep, against realistic phylogenetic trees characterized from SARS-CoV-2. Our study reveals the poor predictive accuracy of PhyloDeep models trained on simulated trees when applied to realistic data. Conversely, models trained on realistic trees demonstrate improved predictions, despite not being infallible, especially in scenarios where superspreading dynamics are challenging to capture accurately. Consequently, we find markedly improved performance through the integration of minimal contact tracing data. Applying this approach to a sample of SARS-CoV-2 sequences partially matched to contact tracing from Hong Kong yields informative estimates of SARS-CoV-2 superspreading potential beyond the scope of contact tracing data alone. Our findings demonstrate the potential for enhancing deep learning phylodynamic models processing low resolution trees through complementary data integration, ultimately increasing the precision of epidemiological predictions crucial for public health decision making and outbreak control.