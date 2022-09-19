import os
import pandas as pd
from itertools import groupby

def aligned(cigar_string):
    """
    modified from https://stackoverflow.com/questions/39710796/infer-the-length-of-a-sequence-using-the-cigar
    """
    read_consuming_ops = ("M", "I", "H","S", "=", "X")
    len_contig = 0
    len_clips = 0
    cig_iter = groupby(cigar_string, lambda chr: chr.isdigit())
    for _, length_digits in cig_iter:
        length = int(''.join(length_digits))
        op = next(next(cig_iter)[1])
        if op in read_consuming_ops:
            len_contig += length
            if op in ["S","H"]:
                len_clips+=length
    len_aligned=len_contig-len_clips
    return [len_aligned, len_contig, len_aligned/len_contig]


Dir='mappings'
df=[]
n=0
for sam in os.listdir(Dir):
	if '.sam' in sam:
		try:
			mapped=[]
			with open(Dir+'/'+sam,'r') as inp:
				for line in inp:
					if line[0]!='@':
						sline=line.split('\t')
						cigar=sline[5]
						if cigar!='*': #mapped
							al_data=aligned(cigar)
							df.append({'genome_qry':sam.split('_')[1].replace('.sam',''),'contig_qry':sline[0],'genome_ref':sam.split('_')[0], 'contig_ref':sline[2],'len_qryAligned':al_data[0],'len_qryContig':al_data[1],'percentage_qryContig':al_data[2]})
		except:
			print(sam)
	n+=1
	print("Completed: "+str(round((n/4692)*100,2))+"%")
	df=pd.DataFrame(df)
	df=pd.DataFrame(df.groupby(['genome_qry','genome_ref','contig_qry','contig_ref']).sum()).reset_index(drop=False)
	df['qry']=df['genome_qry']+'|'+df['contig_qry']
	df['ref']=df['genome_ref']+'|'+df['contig_ref']
#df.to_csv('parsedSams_unfiltered.csv')
#df[df['percentage_qryContig']>0.01].to_csv('parsedSams_filtered1pc.csv')
df[df['percentage_qryContig']>0.1].to_csv('parsedSams_filtered10pc.csv')
