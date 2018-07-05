%%% Generate metrics of strucutral complex per transect

%% LOAD PARAMETERS
fpath='/Users/uqmgonz1/Dropbox/projects/3D_recruits/data/points/feather_v26';
f=dir(fpath);
f = f(~[f.isdir]);
[fPath, fName] = fileparts(fpath);
qsizes=[0.1,0.2,0.5];
pdens=50;
addpath('/Users/uqmgonz1/Dropbox/3D_reconstructions/scripts/matlab_ACFR_QUT/')
addpath('/Users/uqmgonz1/Dropbox/projects/3D_recruits/scripts')
outpath=('/Users/uqmgonz1/Dropbox/projects/3D_recruits/data/structural_complexity');
reef=struct('reefname',fName, 'qsize',qsizes);
core_info = evalc('feature(''numcores'')');
%% set parallel workers
% parpool(4)

results=[];
%% Calculate Structural complexity metrics per transect at different window sizes
for i=(2:length(f))
    results=[];
    fname=fullfile(f(i).folder,f(i).name);
    [tri,xyz,inPoints]=terrain_metrics(fname, pdens);
    for x=(1:length(qsizes))
        qs=qsizes(x);
        [rgsty,slope, aspect, ~, rangez, sdevz, rgstyXY, ~,~, concavity, meandevz, ~, ~, ~] = trisurfterrainfeats(tri, xyz, qs, inPoints);
        n=length(rgsty);
        qsize=repmat(qs,n,1);
        namevar=strsplit(f(i).name,'_');
        reefname=repmat(namevar(1),n,1);
        visit=repmat(sscanf(char(namevar(2)),'v%d'),n,1);
        site=repmat(sscanf(char(namevar(3)),'s%d'),n,1);
        transect=repmat(sscanf(char(namevar(4)),'t%d.txt'),n,1);
        r=table(visit,reefname,site,transect,qsize,rgsty, slope, aspect, rangez, sdevz, rgstyXY, concavity, meandevz); 
        %% PLOT RESULTS
        trires=delaunay(inPoints(:, 1),inPoints(:,2));
        h=figure('visible', 'off');
        subplot(1,3,1), trisurf(tri,xyz(:,1),xyz(:,2),xyz(:,3)),...
            shading interp, title('Bathymetry'), view(0,90),...
            axis equal tight,  colorbar
        subplot(1,3,2),...
            trisurf(trires,inPoints(:, 1),...
            inPoints(:,2),rgsty), shading interp, title('Rugosity'),...
            view(0,90), axis equal tight, colorbar
        
        subplot(1,3,3),...
            trisurf(trires,inPoints(:, 1),...
            inPoints(:,2),rangez), shading interp, title('Range Heights (m)'),...
            view(0,90), axis equal tight, colorbar
        figname=strrep(char(f(i).name),'.txt',strcat('_q',num2str(qs,2),'.png'));
        saveas(h,fullfile('/Users/uqmgonz1/Dropbox/projects/3D_recruits/fig/structural_complexity',figname))
        close(h);
        results=vertcat(results,r);
    end
    writetable(results,fullfile(outpath,f(i).name))
end