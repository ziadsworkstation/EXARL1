clear all;
close all
%Ejemplo1
%% 
I = imread('pout.tif');
imshow(I);
figure, imhist(I)
I2 = histeq(I);
figure, imshow(I2)
figure, imhist(I2)
imwrite (I2, 'pout2.png');

%% 
%Ejemplo2
close all
I = imread('rice.png');
figure, imshow(I);
I3 = imadjust(I);
figure, imshow(I3);
level = graythresh(I3);
bw = im2bw(I3,level);
figure, imshow(bw);
bw1 = bwareaopen(bw, 50);
figure, imshow(bw1)
bw2 = imfill(bw1,'holes');
figure, imshow(bw2)

se1 = strel('disk',1);
bw3 = imerode(bw2,se1);
figure, imshow(bw3);
bw4 = imdilate(bw3,se1);
figure, imshow(bw4);

boundaries = bwboundaries(bw4);

figure, imshow(I);

hold on;
for k=1:size(boundaries,1),
   b = boundaries{k};
   plot(b(:,2),b(:,1),'g','LineWidth',1);
end

cc = bwconncomp(bw4, 4);

arrozdata = regionprops(cc, 'all');%'all'
arroz_areas=[arrozdata.Area];
[min_area, i_min] = min(arroz_areas);
plot(arrozdata(i_min).Centroid(1),arrozdata(i_min).Centroid(2),'r+');

[max_area, i_max] = max(arroz_areas);
plot(arrozdata(i_max).Centroid(1),arrozdata(i_max).Centroid(2),'r+');


arroz = false(size(bw4));
arroz(cc.PixelIdxList{i_min}) = true;
arroz(cc.PixelIdxList{i_max}) = true;
figure, imshow(arroz);

text(arrozdata(i_max).Centroid(1),arrozdata(i_max).Centroid(2),num2str(arroz_areas(i_max)),'color','red');
text(arrozdata(i_min).Centroid(1),arrozdata(i_min).Centroid(2),num2str(arroz_areas(i_min)),'color','red');
