function sc_wrapper(f, pdens, qsizes, outpath, campose)
    results=[];
    fname=fullfile(f.folder,f.name);
    [tri,xyz,inPoints]=terrain_metrics(fname, pdens, campose);
    for x=(1:length(qsizes))
        qs=qsizes(x);
        sprintf('Calculating terrain features for %s using %3.2fm quadrat size on %d points',f.name,qs,pdens)
        [rgsty,slope, aspect, ~, rangez, sdevz, rgstyXY, ~,~, concavity, meandevz, ~, ~, ~] = trisurfterrainfeats(tri, xyz, qs, inPoints);
        n=length(rgsty);
        qsize=repmat(qs,n,1);
        namevar=strsplit(f.folder,'/');
        reeftran=strsplit(f.name,'_');
        sitetran=sscanf(char(reeftran(2)),'Site%dTran%d.txt');
        reefname=repmat(char(reeftran(1)),n,1);
        site=repmat(sitetran(1),n,1);
        transect=repmat(sitetran(2),n,1);
        camp=repmat(char(namevar(length(namevar))),n,1);
        x=inPoints(:,1);
        y=inPoints(:,2);
        r=table(camp,reefname,site,transect,qsize,x,y,rgsty, slope, aspect, rangez, sdevz, rgstyXY, concavity, meandevz); 
        %% PLOT RESULTS
        sprintf('Creating plots for %s using %3.2fm quadrat size on %d points',f.name,qs,pdens)
        trires=delaunay(inPoints(:, 1),inPoints(:,2));
        h=figure('visible', 'off');
        subplot(1,3,1), trisurf(tri,xyz(:,1),xyz(:,2),xyz(:,3)),...
            shading interp, title('Bathymetry'), view(0,90),...
            axis equal tight,   colorbar
        subplot(1,3,2),...
            trisurf(trires,inPoints(:, 1),...
            inPoints(:,2),rgsty), shading interp, title('Rugosity'),...
            view(0,90), axis equal tight,  colorbar
        
        subplot(1,3,3),...
            trisurf(trires,inPoints(:, 1),...
            inPoints(:,2),rangez), shading interp, title('Range Heights (m)'),...
            view(0,90), axis equal tight, colorbar
        figname=strrep(char(f.name),'.txt',strcat('_q',num2str(qs,2),'.png'));
        %saveas(h,fullfile(outpath,'figs',char(namevar(length(namevar))),figname))
        parFigsave(fullfile(outpath,'figs',char(namevar(length(namevar))),figname),h)
        close(h);
        results=vertcat(results,r);
    end
    
    sprintf('Saving results for... %s',f.name)
    %writetable(results,fullfile(outpath,'structural_complexity', char(namevar(length(namevar))),f.name))
    parTablesave(results,fullfile(outpath,'structural_complexity', char(namevar(length(namevar))),f.name))
end 