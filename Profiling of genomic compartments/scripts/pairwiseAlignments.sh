#!/bin/bash

export PATH="/netscratch/dep_psl/grp_hacquard/Fantin/miniconda3/bin:$PATH"

pathAssembly='assemblies'
pathMappings='mappings'

fungi=( #list of the 69 P. cucumerina short names
    'P47'
    'P40'
    'P49'
    'P23'
    'P9'
    'P65'
    'P22'
    'P20'
    'P7'
    'P46'
    'P2'
    'P8'
    'P31'
    'P1'
    'P13'
    'P50'
    'P3'
    'P12'
    'P11'
    'P10'
    'P21'
    'P56'
    'P54'
    'P67'
    'P60'
    'P59'
    'P62'
    'P58'
    'P57'
    'P55'
    'P6'
    'P32'
    'P33'
    'P63'
    'P61'
    'P66'
    'P42'
    'P612'
    'P421'
    'P43'
    'P19'
    'P68'
    'P18'
    'P51'
    'P35'
    'P340'
    'P25'
    'P5'
    'P34'
    'P17'
    'P4'
    'P38'
    'P36'
    'P39'
    'P455'
    'P29'
    'P24'
    'P14'
    'P41'
    'P27'
    'P26'
    'P16'
    'P45'
    'P44'
    'P28'
    'P48'
    'P143'
    'P52'
    'P15'
)

for f1 in "${fungi[@]}"; do
    for f2 in "${fungi[@]}"; do
        if [ "$f1" == "$f2" ]; then
            echo ' '
        else
            pair=$f1\_$f2
            echo $pair
            minimap2 -t 40 -ax asm5 --eqx $pathAssembly/$f1.fasta $pathAssembly/$f2.fasta > $pathMappings/$pair.sam
        fi
    done
done







