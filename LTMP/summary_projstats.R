library(ggplot2)
library(tidyverse)


rm(list=ls())

rap<-read.csv("Z:\\projects\\RAP\\project_summary.csv", stringsAsFactors = F)
rm<-read.csv("Z:\\projects\\RM\\project_summary.csv", stringsAsFactors = F)

rap.nscale<-rap %>% subset(SCALE_ERROR=="NULL")

df<-rbind(rap,rm)

df<-df %>% mutate_if(is.character, list(~na_if(., "NULL")))%>%
  mutate_at(vars(pALIGNED,SCALE_ERROR, MARKER_ERROR), as.numeric)%>%
  mutate(cal_year=as.numeric(substr(as.character(YEAR), 5,6))+2000)

hist(df$pALIGNED)
hist(df$SCALE_ERROR)
hist(df$MARKER_ERROR)

df.sum<-df%>%
  group_by(cal_year,REEFNAME,CAMPAIGN)%>%
  mutate(outlier=if_else(MARKER_ERROR>5,1,0))%>%
  summarise(DENSE_CLOUD=sum(STATUS=="2", na.rm=T),
            ALIGNED=sum(STATUS=="1", na.rm=T),
            DISABLED=sum(DISABLED=='yes', na.rm=T),
            pALIGNED=mean(pALIGNED, na.rm=T), 
            SCALE_ERROR=median(abs(SCALE_ERROR),na.rm=T),
            MARKER_ERROR=median(abs(MARKER_ERROR),na.rm=T),
            NO_SCALED=sum(SCALED=="NO"),
            NO_ALIGNED=sum(is.na(pALIGNED)),
            OUTLIERS=sum(outlier, na.rm=T),
            total=length(REEFNAME))
df.sum

df.outliers<-df%>%
  mutate(outlier=if_else(MARKER_ERROR>5,1,0))%>%
  filter(outlier==1)%>% select(REl_PATH)

write.csv(df, "C:\\Users/mgonzale/OneDrive - Australian Institute of Marine Science/projects/Appropriations/Task 003006/project_status.csv")
write.csv(df.sum, "C:\\Users/mgonzale/OneDrive - Australian Institute of Marine Science/projects/Appropriations/Task 003006/project_status_summary.csv")
