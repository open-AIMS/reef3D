function sc_wrapper(f, pdens, qsizes, outpath)
results=[];
    fname=fullfile(f.folder,f.name);
    [tri,xyz,inPoints]=terrain_metrics(fname, pdens);
    for x=(1:length(qsizes))
        qs=qsizes(x);
        sprintf('Calculating terrain features for %s using %3.2fm quadrat size on %d points',f.name,qs,pdens)
        [rgsty,slope, aspect, ~, rangez, sdevz, rgstyXY, ~,~, concavity, meandevz, ~, ~, ~] = trisurfterrainfeats(tri, xyz, qs, inPoints);
        n=length(rgsty);
        qsize=repmat(qs,n,1);
        namevar=strsplit(f.name,'_');
        reefname=repmat(namevar(1),n,1);
        sitetran=sscanf(char(namevar(2)),'Site%dTran%d.txt');
        site=repmat(sitetran(1),n,1);
        transect=repmat(sitetran(2),n,1);
        [~,camp]=fileparts(f.folder);
        camp=repmat(camp,n,1);
        r=table(camp,reefname,site,transect,qsize,rgsty, slope, aspect, rangez, sdevz, rgstyXY, concavity, meandevz); 
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
        saveas(h,fullfile(outpath,'figs',camp(1),figname))
        close(h);
        results=vertcat(results,r);
    end
    
    sprintf('Saving results for... %s',f.name)
    writetable(results,fullfile(outpath,'structural_complexity', camp(1),f.name))
end 