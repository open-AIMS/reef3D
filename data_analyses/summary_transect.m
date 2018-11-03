function summary_transect(fpath,campose,script_path,outpath)
%%% Generate metrics of strucutral complex per transect

%% PARAMETERS (to modify)
%fpath='/Volumes/3d_ltmp/exports/pointsXYZ/OM/'; % path where point data is located
%campose='/Volumes/3d_ltmp/exports/cameras/OM/'
qsizes=[0.1,0.2,0.5]; % Window size vector for calculating sctructural complexity
pdens=0.2; %Number of point per m2 on which to calculate structural complexity
addpath(genpath(script_path)) %functions path
% addpath('/Users/uqmgonz1/Documents/GitHub/reef3D/MatToolbox') %function paths
%outpath=('/Users/uqmgonz1/Dropbox/projects/3D_recruits/'); %directoriy where files will be saved

%% EXTRA PARAMETERS
f=dir(fpath);
f = f(~[f.isdir]);
%reef=struct('reefname',fName, 'qsize',qsizes);
%core_info = evalc('feature(''numcores'')');
%% set parallel workers
% nc=feature('numcores');
% mypool=parpool(40);

%% Calculate Structural complexity metrics per transect at different window sizes
for i=(1)%:length(f))
    sc_wrapper(f(i),pdens,qsizes, outpath, campose)
end

end
