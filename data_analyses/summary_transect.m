%%% Generate metrics of strucutral complex per transect

%% PARAMETERS (to modify)
fpath='/net/138.7.48.21/3d_ltmp/exports/pointsXYZ/OM'; % path where point data is located
qsizes=[0.1,0.2,0.5]; % Window size vector for calculating sctructural complexity
pdens=50; %Number of point per m2 on which to calculate structural complexity
addpath('/export/home/l-p/mgonzale/Desktop/gits/reef3D/data_analyses/') %functions path
addpath('/export/home/l-p/mgonzale/Desktop/gits/reef3D/MatToolbox') %function paths
outpath=('/net/138.7.48.21/3d_ltmp/exports/'); %directoriy where files will be saved

%% EXTRA PARAMETERS
f=dir(fpath);
f = f(~[f.isdir]);
[fPath, fName] = fileparts(fpath);
%reef=struct('reefname',fName, 'qsize',qsizes);
%core_info = evalc('feature(''numcores'')');
%% set parallel workers
nc=feature('numcores');
mypool=parpool(40);

%% Calculate Structural complexity metrics per transect at different window sizes
parfor i=(2:length(f))
    sc_wrapper(f(i),pdens,qsizes, outpath, fName)
end

delete(mypool)