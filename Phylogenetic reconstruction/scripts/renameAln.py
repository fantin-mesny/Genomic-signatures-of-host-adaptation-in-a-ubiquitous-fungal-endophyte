import os
Dir='singleCopyPhylogeny/'
oDir='singleCopyPhylogeny_renamed/'
for fi in os.listdir(Dir):
	with open(Dir+fi,'r') as inp:
		with open(oDir+fi+'.renamed','w+') as outp:
			for line in inp:
				if '>' in line:
					outp.write('>'+line.split('|')[1]+'\n')
				else:
					outp.write(line)
