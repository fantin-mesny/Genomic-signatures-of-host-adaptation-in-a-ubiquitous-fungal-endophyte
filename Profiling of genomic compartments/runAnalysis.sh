# All assemblies were put in the folder 'assemblies' with name Pn.fasta (e.g. P1.fasta, P2.fasta,etc)

#1. Run all pairwise mappings between assemblies
bash scripts/pairwiseAlignments.sh
#2. Parse the SAM files and create a table, from which a network can be built
python scripts/samsToNetwork.py
##this script generated 'parsedSams_filtered10pc.csv', which we provide here
###this file was opened with Cytoscape to build the network, and cluster it with clusterMaker2
