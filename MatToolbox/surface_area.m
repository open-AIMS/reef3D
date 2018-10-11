function h_quadrat = surface_area(TP, gridres)

res = gridres;
points = TP;
%ratio = 0.1;

% NumOfPoints = max(size(TP));
% NumSelPoints = round(NumOfPoints*ratio);
% SelPoints = ones(NumSelPoints, 1);

points(1, :) = points(1, :) - min(points(1, :));
points(2, :) = points(2, :) - min(points(2, :));
points(3, :) = points(3, :) - min(points(3, :));

% %temp_points = points;
% for k = 1:NumSelPoints
%     [SelPoints(k, 1), idx] = min(points(3, :));
%     points(:, idx) = [];
% end
% h_min = mean(SelPoints);
%clear temp_points

minx = min(points(1, :));
miny = min(points(2, :));
%minz = min(points(3, :));

maxx = max(points(1, :));
maxy = max(points(2, :));
%maxz = max(points(3, :));

stepx = (maxx - minx)/res;
resy = ceil((maxy - miny)/stepx);
stepy = (maxy - miny)/resy;

h_quadrat = zeros(res, resy);

for ii = 1:res
    % using logic indexing to improve the efficiency
    grid_idx = points(1,:) > minx + (ii-1)*stepx & points(1,:) <= minx + ii*stepx;
    temp = points(:, grid_idx);
    for jj = 1:resy
        grid_idx = temp(2,:) > miny + (jj-1)*stepy & temp(2,:) <= miny + jj*stepy;
        test = temp(:, grid_idx);
        Num = floor(size(test, 2)/2);
        if Num > 0
            D = zeros(Num, 1);
            for k = 1:Num
                [~, maxid] = max(test(3, :));
                [~, minid] = min(test(3, :));
                D1 = pdist(test(:,[maxid,minid])');
                D2 = pdist(test(1:2,[maxid,minid])');
                if acos(D2/D1) < pi/3
                    D(k, 1) = D1/D2;
                end
                test(:,[maxid,minid]) = [];
            end
            h_quadrat(ii, jj) = mean(D(D ~= 0));
            if isnan(h_quadrat(ii, jj))
                h_quadrat(ii, jj) = 0;
            end
        end
    end
end
% figure()
% h_quadrat = medfilt2(h_quadrat);
% imagesc(h_quadrat, [1, max(h_quadrat(:))])
% axis equal
% colorbar