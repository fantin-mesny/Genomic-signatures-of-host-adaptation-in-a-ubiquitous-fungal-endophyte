library(phylolm)
library(ape)

df <- read.csv('genomic_compartments.csv', row.names='X')
#df<-as.numeric(df$lifestyle)
t<-read.tree('iqTree_phylogeny.nwk')
t_Pc<-drop.tip(t,c('P117','P30','P64')) # remove P. delsorboi and P. plurivora from tree

ara<-c()
bra<-c()
for (c in names(df)){
	if (!(c %in% c("X1.0","X2.0","X3.0","X4.0","X5.0","X6.0","Continent","HostFamily","HostGroup","Brassicaceae","Arabidopsis"))){
		print(c)
		GLM<-phyloglm(formula(paste(c,'~Arabidopsis',sep='')), data=df, phy=t_Pc)
		ara[c]<-summary(GLM)$coefficients[2,4]
		#GLM<-phyloglm(formula(paste(c,'~Brassicaceae',sep='')), data=df, phy=t_Pc)
		#bra[c]<-summary(GLM)$coefficients[2,4]
	}
}

print(ara)
fdr<-p.adjust(ara,method="fdr",n=length(ara))
print(fdr)
adf=data.frame(ara)
write.csv(cbind(adf,fdr),'compartments.phyloglm.out.csv')
for (i in fdr){
	print(i<0.05)
}

