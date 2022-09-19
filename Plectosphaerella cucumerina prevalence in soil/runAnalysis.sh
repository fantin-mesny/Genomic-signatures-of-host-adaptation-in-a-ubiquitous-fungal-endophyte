# Files from the Global Mycobiome Dataset must be downloaded and put in the 'data' folder
# Are needed: (1) Fungi_GSMc_OTUs_fasta.fasta, (2) Fungi_GSMc_OTU_Table.txt, (3) Fungi_GSMc_sample_metadata.txt
# These files can be downloaded from: https://doi.org/10.15156/BIO/2263453

# The file curated_its1_Pcucumerina.fasta is in the data folder 
# It was obtained by extracting the ITS1 from curated ITS1-5.8S-ITS2 sequences of species P. cucumerina, see study https://doi.org/10.1016/j.simyco.2018.10.005


#1. Link curated ITS1 sequence to barcode from Global Soil Mycobiome data set
blastn -query data/curated_its1_Pcucumerina.fasta -subject data/Fungi_GSMc_OTUs_fasta.fasta -perc_identity 100 -outfmt 6 > data/blast_curatedITS1_on_GSMc.tsv
#2. Filter the Global Soil Mycobiome OTU table to only keep P. cucumerina ASVs
python scripts/filterOTUtable.py
#3. Plot map
python scripts/map.py
#4. Run enrichment test
python scripts/fisher.py
#5. Plot results of the fisher test
python scripts/bubbleplotFisher.py

