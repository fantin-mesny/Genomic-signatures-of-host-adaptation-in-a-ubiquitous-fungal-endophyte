import pandas as pd
import os
#PLANT_DIR='/netscratch/dep_psl/grp_hacquard/Fantin/RNASEQ_HISAT2/mappings'
Dir='/netscratch/dep_psl/grp_hacquard/Fantin/plecto_rnaseq/mappings/'

l4df=[]
n=0
for sample in [f for f in os.listdir(Dir) if '.txt' in f and f!='.txt' and 'summary' not in f]:
	print(sample)
	n+=1
	df=pd.read_csv(Dir+'/'+sample,sep='\t',comment='#')
	df=df.set_index('Geneid').rename(columns={df.columns[-1]:'ReadCount'})
	df=df[df.index.str.contains('gene')]
	scalingFactor=sum(list(df['ReadCount']))/1000000.
	print(scalingFactor)
	df['RPM']=df['ReadCount']/scalingFactor
	df['RPKM']=df['RPM']/(df['Length']/1000)
	print(df['RPKM'])
	l4df.append(df[['RPKM']].rename(columns={'RPKM':'RPKM '+sample}))

df=pd.concat(l4df,axis=1)
df=df[sorted(list(df.columns))]
df.to_csv(Dir+'RPKMs.csv')


