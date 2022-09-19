import os
import pandas as pd
SingleCopy=[fi.replace('.fa','') for fi in os.listdir('data/Single_Copy_Orthologue_Sequences')]
OGs=pd.read_csv('data/Orthogroups.tsv',sep='\t').set_index('Orthogroup')

with open('singleCopyTreesRenamed.all.nwk','w+') as outp:
    for og in SingleCopy:
        with open('data/Gene_Trees/'+og+'_tree.txt','r') as inp:
            tree=inp.read()
        for p in OGs.columns:
            tree=tree.replace(p+'_'+OGs.loc[og,p],p)
        outp.write(tree+'\n')
        

			
