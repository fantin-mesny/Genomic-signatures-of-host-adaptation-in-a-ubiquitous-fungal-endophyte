import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import distance
from scipy.cluster import hierarchy
import numpy as np
import sys
from scipy import stats
sys.setrecursionlimit(100000)


og=pd.read_csv('OrthoFinderResults/Orthogroups.GeneCount.tsv', sep='\t').drop(columns='Total').set_index('Orthogroup')
sc=list(pd.read_csv('OrthoFinderResults/Orthogroups_SingleCopyOrthologues.txt',header=None)[0])

order=list(pd.read_csv('metadata/order_in_species_tree.txt',header=None)[0])
og=og[order].T

og=og.drop(columns=sc) # keep only orthogroups shared by at least two strains
og[og>0]=1 # transform copy number into presence/absence (1/0) data


# orthogroup clustering
col_linkage = hierarchy.linkage(distance.pdist(og.T), method='average')
fclust=pd.DataFrame(hierarchy.fcluster(col_linkage, t=5,criterion='distance'))
fclust.index=og.columns

lut = dict(zip(fclust[0].unique(), sns.color_palette()))
row_colors = fclust[0].map(lut)
sns.clustermap(og,
               row_cluster=False,
               col_linkage=col_linkage,
               col_colors=row_colors,
               method="average",
               figsize=(25, 15),
               cmap='Greys')
plt.savefig('orthogroup_clustermap.png',dpi=400)


row_colors=pd.DataFrame(row_colors)
blue=list(row_colors[row_colors[0]==row_colors.loc['OG0009226',0]].index)
red=list(row_colors[row_colors[0]==row_colors.loc['OG0010970',0]].index)
cyan=list(row_colors[row_colors[0]==row_colors.loc['OG0011395',0]].index)
green=list(row_colors[row_colors[0]==row_colors.loc['OG0013021',0]].index)
main_clusters=[blue,red,cyan,green]
cluster_colors=['blue','red','cyan','green']
for c in main_clusters:
    with open('OGs_in_'+cluster_colors[main_clusters.index(c)]+'_cluster.csv','w+') as outp:
        for og in c:
            outp.write(og+'\n')


