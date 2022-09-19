import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs



otu_table_filtered=pd.read_csv('data/OTU_table_filtered.csv').set_index('OTU')
sums=pd.DataFrame(otu_table_filtered.sum(axis=0)).rename(columns={0:'RA'})

meta=pd.read_csv('data/Fungi_GSMc_sample_metadata.txt',sep='\t', encoding='cp437').set_index('plot')
sums=sums.merge(meta,left_index=True,right_index=True)
filtered=sums[(sums['RA']>0) & (sums['latitude']!='#VALUE!')]
sums=sums[sums['latitude']!='#VALUE!']

fig, axs = plt.subplots(nrows=1,ncols=2,subplot_kw={'projection': ccrs.PlateCarree()},figsize=(11,8.5),sharey=True)
axs[0].scatter(list(sums['longitude'].astype(float)), list(sums['latitude'].astype(float)),color='black',transform = ccrs.PlateCarree())
axs[0].coastlines()
axs[1].hist(list(sums['latitude'].astype(float)),orientation='horizontal',transform = ccrs.PlateCarree())
#plt.show()

plt.close()

for ind in sums.index:
	if ind in filtered.index:
		sums.loc[ind,'includes Pc']='Yes'
	else:
		sums.loc[ind,'includes Pc']='No'


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature

sums['latitude']=sums['latitude'].astype(float)
sums['longitude']=sums['longitude'].astype(float)

fig = plt.figure()
#gs = fig.add_gridspec(3, 3)
gs = fig.add_gridspec(2, 2,width_ratios=(5,1),height_ratios=(3,1))

#ax1 = fig.add_subplot(gs[0:2, 0:2], projection=ccrs.PlateCarree())
ax1 = fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree())
ax1.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='auto', color='k')
ax1.scatter(list(sums['longitude'].astype(float)), list(sums['latitude'].astype(float)),color='grey',s=3)#,transform = ccrs.PlateCarree())
ax1.scatter(list(filtered['longitude'].astype(float)), list(filtered['latitude'].astype(float)),color='red',s=3)#,transform = ccrs.PlateCarree())
#sns.scatterplot('longitude','latitude',data=sums,hue='includes Pc',palette={'Yes':'red','No':'grey'})
ax1.gridlines(color='lightgrey', linestyle='-', draw_labels=True)

#ax2 = fig.add_subplot(gs[2, 0:2])
ax2 = fig.add_subplot(gs[1, 0])
bins = np.linspace(-180, 180, 50)
#ax2.hist(list(sums['longitude'].astype(float)),bins=20,color='grey')
#ax2.hist(list(filtered['longitude'].astype(float)),bins=20,color='red')
#sns.histplot(list(sums['longitude'].astype(float)),ax=ax2,bins=bins,color='grey')
sns.histplot(sums, x='longitude',ax=ax2,bins=bins,hue='includes Pc',palette={'Yes':'red','No':'grey'},legend=None, multiple="stack")
ax2.set_yscale('log')

ax2.sharex(ax1)
ax2.set_xticks([180,100,60,0,-60,-120,-180])

#ax3 = fig.add_subplot(gs[0:2, 2:4])
ax3 = fig.add_subplot(gs[0, 1])
#ax3.sharey(ax1)
bins = np.linspace(-100, 100, 35)
#ax3.hist(list(sums['latitude'].astype(float)),bins=bins,color='grey',orientation='horizontal')
#ax3.hist(list(filtered['latitude'].astype(float)),bins=bins,color='red',orientation='horizontal')
#sns.histplot(y=list(sums['latitude'].astype(float)),ax=ax3,bins=bins,color='grey')
sns.histplot(sums, y='latitude',ax=ax3,bins=bins,hue='includes Pc',palette={'Yes':'red','No':'grey'},legend=None, multiple="stack")
ax3.sharey(ax1)
ax3.set_yticks([60,30,0,-30,-60])
ax3.set_xscale('log')
plt.savefig('map.pdf')
