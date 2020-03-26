
##STRUCTURAL COMPLEXITY SUMMARY
#Concatenate Structural complexity files per transect/plot and summarise values 


rm(list=ls())
#LIBRARIES¥
library(dplyr)
library(ggplot2)
library(tidyverse)


##Rugosity data
# Read all rugosity files
# Define function
multmerge = function(mypath){
  filenames=list.files(path=mypath, recursive = TRUE,full.names=TRUE)
  datalist = lapply(filenames, function(x){read.csv(file=x,header=T)})
  df=bind_rows(datalist,.id="ID")
  return(df)
}

sc=multmerge("Z:\\exports\\structural_complexity\\OI") ##NOTe change this to desired folder

# Here transforme slope to degrees
sc$slopedeg <- (sc$slope * 180/pi)
sc <- sc[!is.na(sc$rgsty),]

# Define function to calculate the coefficient of variation (for rangez)
coefVar <- function(x){
  return(sd(x, na.rm = TRUE)/mean(x, na.rm = TRUE))
}
  
# Define function to calculate the 90th percentile for sdevz
cent90 <- function(x){
    quantile(x,0.90, na.rm = TRUE)
}


## CALCULATE SUMMARY METRICS FROM DIFFERENT MEASURES STRUCTURAL COMPLEXITY
#NOTE: ths is not the best approach becuase is lenghty (code-wise), but it works. 

sc_store <- sc

sc<-sc%>%
  filter(qsize==0.5)%>%
  select(-one_of("ID","qsize","x","y"))%>%
  group_by(camp,reefname,site,transect)%>%
  summarise_at(.vars = c("rgsty","slope","aspect","rangez","concavity"),.funs=list(median))

sc<-sc%>%
  rename(REEF_NAME=reefname, SITE_NO=site,TRANSECT_NO=transect,rgsty50=rgsty,slope50=slope,aspect50=aspect,rangez50=rangez,concavity50=concavity)
sc50medians <- sc


sc <- sc_store 

sc<-sc%>%
  filter(qsize==0.5)%>%
  select(-one_of("ID","qsize","x","y","sdevz","slope","aspect","rangez","concavity","meandevz"))%>%
  group_by(camp,reefname,site,transect)%>%
  summarise_at(.vars = c("rgsty"),.funs=list(sd))
sc<-sc%>%
  rename(REEF_NAME=reefname, SITE_NO=site,TRANSECT_NO=transect,rgsty50sd=rgsty)
sc50sds <- sc


sc <- sc_store

sc<-sc%>%
  filter(qsize==0.5)%>%
  select(-one_of("ID","qsize","x","y","rgsty","slope","aspect","rangez","concavity","sdevz"))%>%
  group_by(camp,reefname,site,transect)%>%
  summarise_at(.vars = c("meandevz"),.funs=list(max))
sc<-sc%>%
  rename(REEF_NAME=reefname, SITE_NO=site,TRANSECT_NO=transect,meandevz50=meandevz)
sc50maxs <- sc

sc <- sc_store

sc<-sc%>%
  filter(qsize==0.5)%>%
  select(-one_of("ID","qsize","x","y","rgsty","slope","aspect","rangez","concavity","meandevz"))%>%
  group_by(camp,reefname,site,transect)%>%
  summarise_at(.vars = c("sdevz"),.funs=list(cent90))
sc<-sc%>%
  rename(REEF_NAME=reefname, SITE_NO=site,TRANSECT_NO=transect,sdevz50=sdevz)
sc50cent90s <- sc

sc <- sc_store
  
sc<-sc%>%
  filter(qsize==0.5)%>%
  select(-one_of("ID","qsize","x","y","rgsty","slope","aspect","concavity","sdevz","meandevz"))%>%
  group_by(camp,reefname,site,transect)%>%
  summarise_at(.vars = c("rangez"),.funs=list(rangezCV50 = coefVar))
sc<-sc%>%
  rename(REEF_NAME=reefname, SITE_NO=site,TRANSECT_NO=transect)
sc50rangezCV <- sc

##MERGE DATAFRAMES
sc=list(sc50cent90s,sc50maxs,sc50medians,sc50rangezCV,sc50sds) %>% reduce(left_join, by =c("camp","REEF_NAME","SITE_NO","TRANSECT_NO"))

###SAVE as CSV
#write.csv(sc, path)