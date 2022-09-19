
#Untar the single copy orthologue sequences, obtained from orthology prediction with OrthoFinder
tar -xzvf data/Single_Copy_Orthologue_Sequences.tar.gz

#### IQ-TREE and RAxML-NG 

# 1. Align all sequences in each single copy orthogroup
mkdir singleCopyPhylogeny
cd data/Single_Copy_Orthologue_Sequences/
ls * | while read line ; do mafft --auto --thread 40 $line > ../../singleCopyPhylogeny/$line.aln ; done
cd ../../

#2. Rename protein ID to strain ID in each fasta file
mkdir singleCopyPhylogeny_renamed/
python scripts/renameAln.py

#3. Trim alignments to remove low quality regions
mkdir singleCopyPhylogeny_trimal/
ls singleCopyPhylogeny_renamed/* | while read line ; do trimal -in $line -out singleCopyPhylogeny_trimal/$(python -c "print('$line'.replace('singleCopyPhylogeny_renamed/',''))") ; done

#4. Run iq-tree
iqtree -T AUTO -m TEST -s singleCopyPhylogeny_trimal/ --seqtype AA > iq_trimal.log
### log file tells us that ModelFinder found JTT+F+I+G4 to be the best maximum-likelihood model

#5. Concatenate alignments with AMAS, to obtain a single file for RAxML-NG
python AMAS.py concat -i singleCopyPhylogeny_trimal/* -f fasta -d aa -p singleCopyPhylogeny_trimal_amas_partitions.txt -t singleCopyPhylogeny_trimal_amas_concatenated.out -u fasta

#6. Run RAxML-NG
raxml-ng --msa singleCopyPhylogeny_trimal_amas_concatenated.out --model JTT+F+I+G4

#### ASTRAL

#1. Untar the Gene Trees calculated by OrthoFinder, and the orthogroup table as well
tar -xzvf data/Gene_Trees.tar.gz
tar -xzvf data/Orthogroups.tar.gz

#2. Filter the Gene Trees (to keep single copy orthologoes) and rename protein ID into strain ID in each
python scripts/renameInTrees.py

#3. run Astral
java -jar astral.5.7.1.jar --input singleCopyTreesRenamed.all.nwk --output singleCopyTreesRenamed_astral > astralOnSingleCopyTrees.log &

#### STAG
# phylogeny computed by OrthoFinder, when running Orthology Prediction on protein fasta files
