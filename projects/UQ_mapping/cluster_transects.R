library(sp)
library(rgdal)
require(rgeos)
require(dplyr)

clustTran=function(summaryfile, outputdir, clust_size){
  df<-read.csv("~/Dropbox/projects/UQ_Mapping/Rugosity/20190527/test_clusters.csv")
  df$dive=stringr::str_extract(string = df$Name, pattern = "D[0-9]")
  df$dive=as.factor(df$dive)
  
  df<-subset(df, select=-CLUSTER_ID)
  coordinates(df) <- ~Longitude+Latitude
  proj4string(df)=CRS("+proj=longlat +ellps=WGS84 +datum=WGS84")
  df=spTransform(df, CRS("+init=epsg:3112")) #project to GDA94 Australia Lambert
  
  t=split(df, df$dive)
  d=lapply(t, spDists)
  d=lapply(d, as.dist)
  
  #remove empty transects
  empty.t=lapply(d, length)
  empty.t=unlist(empty.t)
  empty.t=which(empty.t==0)
  if (length(empty.t)>0){
    d=d[-empty.t]
    t=t[-empty.t]
  }
  
  chc=lapply(d, hclust)
  chc.d100=lapply(chc, cutree, h=10)
  df=as.data.frame(df)
  df$clust_id=as.factor(as.data.frame(lapply(chc, cutree, h=10))[,1])
  
  df=df %>% 
    group_by(clust_id) %>% 
    filter(n() >= 100)
  
  dfl=split(df, df$dive)
  
            }





