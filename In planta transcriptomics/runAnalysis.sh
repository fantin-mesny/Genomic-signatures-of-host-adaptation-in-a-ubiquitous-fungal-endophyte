#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>mapping.log 2>&1
CORENUM=48
MAIN_DIR="."
FILES_DIR=$MAIN_DIR/genomes # Arabidopsis and PcBMM genomes (fasta) and annotations (gtf) should be put in this folder
INDEX_DIR=$MAIN_DIR/genomes
MAPPING_DIR=$MAIN_DIR/mappings
READS_DIR=$MAIN_DIR/reads

##### DOWNLOAD AND SPLIT DATA #####
# reads fastq files from bioProject PRJNA614936 at NCBI 
cd $READS_DIR
curl -O -J https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos3/sra-pub-run-19/SRR11668192/SRR11668192.1 &
curl -O -J https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos3/sra-pub-run-21/SRR11668193/SRR11668193.1 &
curl -O -J https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos3/sra-pub-run-19/SRR11668194/SRR11668194.1 &
curl -O -J https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos3/sra-pub-run-19/SRR11668195/SRR11668195.1 &
wait 
fastq-dump SRR11668192.1 &
fastq-dump SRR11668193.1 &
fastq-dump SRR11668194.1 &
fastq-dump SRR11668195.1 &
wait
seqkit grep -inrp 'C9NA4ANXX:6' SRR11668192.1.fastq > PcBMM_16h_01.fq & #PcBMM 16h 01
seqkit grep -inrp 'C9NA4ANXX:8' SRR11668192.1.fastq > PcBMM_16h_02.fq & #PcBMM 16h 02
seqkit grep -inrp 'C9NA4ANXX:6' SRR11668193.1.fastq > PcBMM_10h_01.fq & #PcBMM 10h 01
seqkit grep -inrp 'C9NA4ANXX:8' SRR11668193.1.fastq > PcBMM_10h_02.fq & #PcBMM 10h 02
cd ../

##### BUILD HISAT INDEX #####
ls $FILES_DIR/*.gtf | while read line ; do hisat2_extract_splice_sites.py $line > $INDEX_DIR/$line.ss ; hisat2_extract_exons.py $line > $INDEX_DIR/$line.ex ; done

p1='Arabidopsis'
p2='PcBMM'
index="Arabidopsis_PcBMM"
cat $INDEX_DIR/$p1.gtf.ss $INDEX_DIR/$p2.gtf.ss > $INDEX_DIR/$index.ss
cat $INDEX_DIR/$p1.gtf.ex $INDEX_DIR/$p2.gtf.ex > $INDEX_DIR/$index.ex
hisat2-build -p 60 --ss $INDEX_DIR/$index.ss --exon $INDEX_DIR/$index.ex $FILES_DIR/$p1.fasta,$FILES_DIR/$p2.fasta $INDEX_DIR/$index

##### MAP READS ON INDEX #####

mkdir $MAPPING_DIR
reads=( 
    "$READS_DIR/PcBMM_10h_01.fq"
    "$READS_DIR/PcBMM_10h_02.fq"
    "$READS_DIR/PcBMM_16h_01.fq"
    "$READS_DIR/PcBMM_16h_02.fq"
)


for sample in "${reads[@]}"; do
    echo $sample
    s=$(python -c "print('$sample'.split('/')[-1])")
    hisat2 -p $CORENUM -x $INDEX_DIR/$index -U $sample -S $MAPPING_DIR/$s.sam
    samtools sort -@ $CORENUM -o $MAPPING_DIR/$s.bam $MAPPING_DIR/$s.sam
    samtools index $MAPPING_DIR/$s.bam
    featureCounts -T $CORENUM -a $FILES_DIR/$index.gtf -o $MAPPING_DIR/$s.txt $MAPPING_DIR/$s.sam
done

#### CALCULATE RPKMs #####
python GetRPKM.py

