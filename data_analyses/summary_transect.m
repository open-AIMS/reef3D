function summary_transect(fpath,campose,script_path,outpath)
%%% Generate metrics of strucutral complex per transect

%% PARAMETERS (to modify)
%fpath='/Volumes/3d_ltmp/exports/pointsXYZ/OM/'; % path where point data is located
%campose='/Volumes/3d_ltmp/exports/cameras/OM/'
qsizes=[0.1,0.5]; % Window size vector for calculating sctructural complexity
pdens=0.3; %Distance (m) between points on which to evaluate structural complexity
addpath(genpath(script_path)) %functions path
% addpath('/Users/uqmgonz1/Documents/GitHub/reef3D/MatToolbox') %function paths
%outpath=('/Users/uqmgonz1/Dropbox/projects/3D_recruits/'); %directoriy where files will be saved

%% EXTRA PARAMETERS
f=dir(fpath);
f = f(~[f.isdir]);
%reef=struct('reefname',fName, 'qsize',qsizes);
%core_info = evalc('feature(''numcores'')');
%% set parallel workers
%nc=feature('numcores');
%mypool=parpool(6);

%% Calculate Structural complexity metrics per transect at different window sizes
for i=(1:length(f))
    namevar=strsplit(f(i).folder,'/');
    %%% Ignore the transects already processed
    if exist(fullfile(outpath,'structural_complexity', char(namevar(length(namevar))),f(i).name), 'file')==0
        sc_wrapper(f(i),pdens,qsizes, outpath, campose)
    end
end

end
