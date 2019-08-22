

clustTran=function(summaryfile, outdir,outname, clust_size){
  require(sp)
  require(rgdal)
  require(rgeos)
  require(dplyr)
  df<-read.table(summaryfile,
                 sep='\t', 
                 header = F,
                 stringsAsFactors = F,
                 col.names = c('fname','fpath','Latitude','Longitude'),
                 colClasses = c('character','character', 'character','character'),
                 na.strings='NULL',
                 dec=".",numerals = "no.loss", skipNul = T)
  df$Latitude=as.numeric(df$Latitude)
  df$Longitude=as.numeric(df$Longitude)
  df=df[!is.na(df$Latitude),]
  df=df[!is.na(df$Longitude),]
  
  
  df$dive=stringr::str_extract(string = df$fname, pattern = "D[0-9]")
  df$dive=as.factor(df$dive)
  
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
  c=lapply(chc, cutree, h=clust_size)
  df=lapply(t, data.frame)
  df=bind_rows(df, .id = "Dive")
  c=lapply(c, data.frame)
  c=bind_rows(c, .id = "Dive")
  names(c)[2]="cluster_id"
  df$cluster_id=c$cluster_id
  
  df=df %>% 
    group_by(cluster_id) %>% 
    filter(n() >= 50)
  
  for (i in unique(df$Dive)){
    write.csv2(df[df$Dive==i,],file=file.path(outdir,paste(outname, '_', i,'.csv')))
  }
  
}
clustTran(summaryfile="~/temp/20190527_Rugo/imlist.txt",outdir = '~/temp/20190527_Rugo/',outname = '20190527', clust_size = 20)





