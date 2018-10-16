%%% Generate metrics of strucutral complex per transect

%% LOAD PARAMETERS
fpath='/net/138.7.48.21/3d_ltmp/exports/pointsXYZ/OM';
f=dir(fpath);
f = f(~[f.isdir]);
[fPath, fName] = fileparts(fpath);
qsizes=[0.1,0.2];
pdens=5;
addpath('/export/home/l-p/mgonzale/Desktop/gits/reef3D/data_analyses/')
addpath('/export/home/l-p/mgonzale/Desktop/gits/reef3D/MatToolbox')
outpath=('/net/138.7.48.21/3d_ltmp/exports/structural_complexity/OM');
reef=struct('reefname',fName, 'qsize',qsizes);
core_info = evalc('feature(''numcores'')');
%% set parallel workers
parpool(30)

results=[];
%% Calculate Structural complexity metrics per transect at different window sizes
parfor i=(2:4)
    sc_wrapper(f(i),pdens,qsizes)
end