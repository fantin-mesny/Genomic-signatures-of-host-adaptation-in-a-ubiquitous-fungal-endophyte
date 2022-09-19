import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

glm=pd.read_csv('orthogroups.phyloglm.out.csv').set_index('Unnamed: 0')
glm=glm[glm['fdr']<0.05]
og=pd.read_csv('orthogroups.csv').set_index('Unnamed: 0')
og[og>1]=1
order=list(pd.read_csv('order_in_iqTree.txt',header=None)[0])
order_map={o:order.index(o) for o in order}
og['order']=og.index.map(order_map)
og=og.sort_values(by='order',ascending=True).drop(columns='order')

og['Arabidopsis']=og['Arabidopsis'].astype(int)
for c in list(glm.index):
	#og[og['Arabidopsis']=='True'][c]
	print(c,sum(og[og['Arabidopsis']==0][c]),sum(og[og['Arabidopsis']>0][c]))



og=og[list(glm.index)]
print(og)
fig,ax=plt.subplots(1,1,figsize=(10,7))
sns.heatmap(ax=ax,data=og,cmap='Greys',cbar=None)
plt.savefig('ath_phyloGLM_genefamilies.pdf')
