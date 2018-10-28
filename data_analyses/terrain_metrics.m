function [tri,xyz,inPoints]=terrain_metrics(filename, pointdens)
%% Read Point Cloud
% delimiter = ' ';
% % Format for each line of text:
% formatSpec = '%f%f%f%f%f%f%f%f%f%[^\n\r]';
% %Open the text file.
% fileID = fopen(filename,'r');
% % Read columns of data according to the format.
% dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'TextType', 'string', 'EmptyValue', NaN,  'ReturnOnError', false);
% % Close the text file.
% fclose(fileID);
% %%Create output variable
% df = [dataArray{1:end-1}];
% % Clear temporary variables
% clearvars delimiter formatSpec fileID dataArray ans;
p=pointCloud(filename);

%% Generate mesh
xyz=p.X;
tri = delaunay(p.X(:,1),p.X(:,2));
%% create a boundary a quadrat locations where to measure structural complexity
% xy=xyz(:,1:2);
% Selection window as 3-by-2 matrix: [minX maxX; minY maxY; minZ maxZ]
p.select('Limits',[p.lim.min(1)+0.1 p.lim.max(1)-0.1; p.lim.min(2)+0.1 p.lim.max(2)-0.1; p.lim.min(3) p.lim.max(3)]);
p.select('UniformSampling', pointdens);
inPoints=p.X(p.act,1:2);
% sx=0.7; %proportion
% sy=1; 
% k=boundary(x,y,0.1);
% bx= sx*x(k)+(1-sx)*mean(x(k));
% by= sy*y(k)+(1-sy)*mean(y(k));
% bx=mean(x);
% % create quadrat points where to sample strcutural complexity
% inPoints = polygrid(bx, by,pointdens);
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