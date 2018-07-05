function [TP, RawPoints, Rot] = TransPoints(points, planeNorm)
% input: points cell contains postion, color, visibility in corresponding
% image views as image coordinates
% planeNorm is the plane normal direction respecting to world frame
% output: TP transformed points, RawPoints orignal pointss

NumOfPoints = max(size(points));

if iscell(points)
    RawPoints = zeros(3, NumOfPoints);   
    for k = 1:NumOfPoints
        RawPoints(:, k) = points{k}.position;
    end
else
    RawPoints = points;
end

Rot = vrrotvec2mat(vrrotvec(planeNorm, [0 0 1]'));
%Rot = vrrotvec2mat(vrrotvec([0 0 1]',planeNorm));

TP = Rot*RawPoints;

%figure(); plot3(RawPoints(1,:),RawPoints(2,:),RawPoints(3,:),'b.');axis equal;grid on
%figure(); plot3(TP(1,:),TP(2,:),TP(3,:),'b.');axis equal;grid on