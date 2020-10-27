library(ggplot2)
library(tidyverse)


rm(list=ls())

rap<-read.csv("Z:\\projects\\RAP\\201920\\project_summary.csv", stringsAsFactors = F)

rap.nscale<-rap %>% subset(SCALE_ERROR=="NULL")

rap<-rap %>% mutate_if(is.character, list(~na_if(., "NULL")))%>%
  mutate_at(vars(SCALE_ERROR, MARKER_ERROR), as.numeric)

hist(rap$pALIGNED)
hist(rap$SCALE_ERROR)
hist(rap$MARKER_ERROR)

rap.sum<-rap%>%
  group_by(YEAR,CAMPAIGN)%>%
  mutate(outlier=if_else(MARKER_ERROR>5,1,0))%>%
  summarise(pALIGNED=mean(pALIGNED, na.rm=T), 
            SCALE_ERROR=median(SCALE_ERROR,na.rm=T),
            MARKER_ERROR=median(MARKER_ERROR,na.rm=T),
            NO_SCALED=sum(SCALED=="NO"),
            NO_ALIGNED=sum(ALIGNED==0),
            OUTLIERS=sum(outlier, na.rm=T),
            total=)
rap.sum
            