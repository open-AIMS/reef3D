function [tri,xyz,inPoints]=terrain_metrics(filename, pointdens)
%% Read Point Cloud
delimiter = ' ';
% Format for each line of text:
formatSpec = '%f%f%f%f%f%f%f%f%f%[^\n\r]';
%Open the text file.
fileID = fopen(filename,'r');
% Read columns of data according to the format.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'TextType', 'string', 'EmptyValue', NaN,  'ReturnOnError', false);
% Close the text file.
fclose(fileID);
%%Create output variable
df = [dataArray{1:end-1}];
% Clear temporary variables
clearvars delimiter formatSpec fileID dataArray ans;

%% Generate mesh
xyz=df(:,1:3);
tri = delaunay(xyz(:,1),xyz(:,2));
%% create a boundary a quadrat locations where to measure structural complexity
x=xyz(:,1);
y=xyz(:,2);
sx=0.7; %proportion
sy=1; 
k=boundary(x,y,0.1);
bx= sx*x(k)+(1-sx)*mean(x(k));
by= sy*y(k)+(1-sy)*mean(y(k));
% create quadrat points where to sample strcutural complexity
inPoints = polygrid(bx, by,pointdens);
end
%% PLOT RESULTS
% trires=delaunay(inPoints(:, 1),inPoints(:,2));
% subplot(1,3,1), trisurf(tri,xyz(:,1),xyz(:,2),xyz(:,3)),...
%     shading interp, title('Bathymetry'), view(0,90),...
%     axis equal tight, colorbar
% 
% subplot(1,3,2),...
%     trisurf(trires,inPoints(:, 1),...
%     inPoints(:,2),rgsty), shading interp, title('Rugosity'),...
%     view(0,90), axis equal tight, colorbar
% 
% subplot(1,3,3),...
%     trisurf(trires,inPoints(:, 1),...
%     inPoints(:,2),rangez), shading interp, title('Range Heights (m)'),...
%     view(0,90), axis equal tight, colorbar