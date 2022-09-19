import pandas as pd
import itertools as IT
import matplotlib.pyplot as plt
import seaborn as sns
#from mpl_toolkits.basemap import Basemap
import numpy as np
from itertools import chain
from scipy import stats
from statsmodels.stats.multitest import multipletests

def draw_map(m, scale=0.5):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)
    
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')


### PARSE DATA 
otu_table_filtered=pd.read_csv('data/OTU_table_filtered.csv').set_index('OTU')
sums=pd.DataFrame(otu_table_filtered.sum(axis=0)).rename(columns={0:'RA'})
meta=pd.read_csv('data/Fungi_GSMc_sample_metadata.txt',sep='\t', encoding='cp437').set_index('plot')
sums=sums.merge(meta,left_index=True,right_index=True)
filtered=sums[(sums['RA']>0) & (sums['latitude']!='#VALUE!')]
sums=sums[sums['latitude']!='#VALUE!']

### PLOT MAP - see script map.py for improved version
#fig = plt.figure(figsize=(16, 12), edgecolor='w')
#m = Basemap(projection='cyl', resolution=None, llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, )
#m.scatter(list(sums['longitude'].astype(float)), list(sums['latitude'].astype(float)), latlon=True,color='black')
#m.scatter(list(filtered['longitude'].astype(float)), list(filtered['latitude'].astype(float)), latlon=True,color='red')
#draw_map(m)
#plt.savefig('map_GlobalMycobiome_Pcdetected.pdf')
#plt.close()
    
### CALCULATE ENRICHMENT WITH FISHER
sampling={b:[] for b in set(sums['biome'])} #[sums['biome'].str.contains('anthropogenic: ')]

for i in range(99999):
    if str(i)[-1]=='0':
        print(i)
    subset=sums.sample(n=len(filtered))
    for biome in sampling:
        sampling[biome].append(len(subset[subset['biome']==biome]))

df=[]
for biome in sampling:
    print(biome)
    sampling[biome].append(len(filtered[filtered['biome']==biome]))
    f=stats.fisher_exact(
        [[sampling[biome][-1], len(filtered)-sampling[biome][-1]],
        [sum(sampling[biome][:-1])/len(sampling[biome][:-1]), len(filtered)-sum(sampling[biome][:-1])/len(sampling[biome][:-1])]],
    alternative='two-sided')
    print(f)
    df.append({ 'biome':biome,
                'oddsratio':f[0],
                'p-value':f[1],
              })

df=pd.DataFrame(df).dropna()
df['adj. p-value']=multipletests(df['p-value'],alpha=0.05,method='fdr_bh')[1]
df.sort_values(by='adj. p-value').to_csv('results_fisher_2sided.csv')

    
    
    
