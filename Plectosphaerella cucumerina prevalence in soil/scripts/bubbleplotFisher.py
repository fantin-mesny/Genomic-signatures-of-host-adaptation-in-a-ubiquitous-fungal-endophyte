import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


otu_table_filtered=pd.read_csv('data/OTU_table_filtered.csv').set_index('OTU')
sums=pd.DataFrame(otu_table_filtered.sum(axis=0)).rename(columns={0:'RA'})
meta=pd.read_csv('data/Fungi_GSMc_sample_metadata.txt',sep='\t', encoding='cp437').set_index('plot')
sums=sums.merge(meta,left_index=True,right_index=True)
filtered=sums[(sums['RA']>0) & (sums['latitude']!='#VALUE!')]
sums=sums[sums['latitude']!='#VALUE!']

fig2=[]
sums_biomes=sums['biome'].value_counts().to_dict()
filtered_biomes=filtered['biome'].value_counts().to_dict()
stats=pd.read_csv('results_fisher_2sided.csv').set_index('biome')
for biome in filtered_biomes:
    fig2.append({
        'biome':biome,
        'sample size':sums_biomes[biome],
        'percentage containing Pc':(filtered_biomes[biome]/sums_biomes[biome])*100,
        'adj. p-value':stats.loc[biome,'adj. p-value'],
        'odds ratio':stats.loc[biome,'oddsratio']
    })
fig2=pd.DataFrame(fig2).sort_values(by='percentage containing Pc',ascending=False).reset_index(drop=True)
for ind in fig2.index:
	if fig2.loc[ind,'adj. p-value']<0.001:
		fig2.loc[ind,'p-stars']='***'
	elif fig2.loc[ind,'adj. p-value']<0.01:
		fig2.loc[ind,'p-stars']='**'
	elif fig2.loc[ind,'adj. p-value']<0.05:
		fig2.loc[ind,'p-stars']='*'
	else:
		fig2.loc[ind,'p-stars']=' '

fig,ax=plt.subplots(1,1)#,figsize=(1,10))
sns.scatterplot(x=1,y='biome',size='sample size',hue='percentage containing Pc',data=fig2,palette='Greys',hue_norm=(-15,100),edgecolor=None,sizes=(2, 200))
for ind in fig2.index:
	if fig2.loc[ind,'odds ratio']<1:
		col='blue'
	else:
		col='red' 
	ax.text(1.005,ind,fig2.loc[ind,'p-stars'],va='center',ha='left',c=col)
plt.savefig('bubbleplot_biomes.pdf')

