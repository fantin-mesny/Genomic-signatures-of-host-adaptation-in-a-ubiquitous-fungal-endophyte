library(phylolm)
library(ape)

df <- read.csv('orthogroups.csv', row.names='X')
t<-read.tree('iqTree_phylogeny.nwk')
t_Pc<-drop.tip(t,c('P117','P30','P64')) # remove P. delsorboi and P. plurivora from tree

ara<-c()
for (c in names(df)){
	if (!(c %in% c("Arabidopsis"))){
		df[c][df[c]> 1] <- 1
		if (var(df[c]) != 0){
		GLM<-phyloglm(formula(paste(c,'~Arabidopsis',sep='')), data=df, phy=t_Pc)
		ara[c]<-summary(GLM)$coefficients[2,4]}
	}
}

print(ara)
fdr<-p.adjust(ara,method="fdr",n=length(ara))
print(fdr)

adf=data.frame(ara)
write.csv(cbind(adf,fdr),'orthogroups.phyloglm.out.csv')
for (i in fdr){
	if (i<0.05) { print(i)}
}
