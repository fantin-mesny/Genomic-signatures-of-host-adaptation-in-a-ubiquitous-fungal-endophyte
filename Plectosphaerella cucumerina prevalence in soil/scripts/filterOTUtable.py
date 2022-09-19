import pandas as pd
blast=pd.read_csv('data/blast_curatedITS1_on_GSMc.tsv',sep='\t',header=None)
blast=list(blast[1])
otu=pd.read_csv('data/Fungi_GSMc_OTU_Table.txt',sep='\t').set_index('OTU')
otu[otu.index.isin(blast)].to_csv('data/OTU_table_filtered.csv')

