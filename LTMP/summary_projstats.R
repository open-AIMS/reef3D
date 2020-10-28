library(ggplot2)
library(tidyverse)


rm(list=ls())

rap<-read.csv("Z:\\projects\\RAP\\project_summary.csv", stringsAsFactors = F)
rm<-read.csv("Z:\\projects\\RM\\project_summary.csv", stringsAsFactors = F)

rap.nscale<-rap %>% subset(SCALE_ERROR=="NULL")

df<-rbind(rap,rm)

df<-df %>% mutate_if(is.character, list(~na_if(., "NULL")))%>%
  mutate_at(vars(pALIGNED,SCALE_ERROR, MARKER_ERROR), as.numeric)

hist(df$pALIGNED)
hist(df$SCALE_ERROR)
hist(df$MARKER_ERROR)

df.sum<-df%>%
  group_by(YEAR,CAMPAIGN)%>%
  mutate(outlier=if_else(MARKER_ERROR>5,1,0))%>%
  summarise(pALIGNED=mean(pALIGNED, na.rm=T), 
            SCALE_ERROR=median(SCALE_ERROR,na.rm=T),
            MARKER_ERROR=median(MARKER_ERROR,na.rm=T),
            NO_SCALED=sum(SCALED=="NO"),
            NO_ALIGNED=sum(ALIGNED==0),
            OUTLIERS=sum(outlier, na.rm=T),
            total=length(REEFNAME))
df.sum

df.outliers<-df%>%
  mutate(outlier=if_else(MARKER_ERROR>5,1,0))%>%
  filter(outlier==1)%>% select(REl_PATH)

write.csv(df, "C:\\Users/mgonzale/OneDrive - Australian Institute of Marine Science/projects/Appropriations/Task 003006/project_status.csv")
write.csv(df.sum, "C:\\Users/mgonzale/OneDrive - Australian Institute of Marine Science/projects/Appropriations/Task 003006/project_status_summary.csv")
