%% Practica 3 INPS - Interaccio amb Visio
% Deteccio de figures geometriques (Cercle, Triangle, Quadrat), del seu
% color (Vermell, Verd, Blau) i de la seva mida (1 petita, 2 mitjana,
% 3 gran) sobre una imatge de fons negre.
%
% Etiqueta = <forma><color><mida>, p.ex. 'SG2' = quadrat verd mitja.
%
% Basat en ejemploVision.m (Atenea).

clear all;
close all;

%% Seleccio de la imatge
% Es pot canviar el nom del fitxer o deixar que l'usuari el triï.
[fitxer, carpeta] = uigetfile({'*.jpg;*.png;*.bmp;*.tif', 'Imatges'}, ...
                              'Tria una imatge', 'imatges/figures1.jpg');
if isequal(fitxer, 0)
    fitxer  = 'figures1.jpg';
    carpeta = 'imatges';
end
I = imread(fullfile(carpeta, fitxer));

figure, imshow(I), title('Imatge original');

%% Separacio per colors
% Les figures son R, G o B purs: un canal alt i els altres dos baixos.
% Llindars amplis per tolerar la compressio JPEG.
R = I(:,:,1);
G = I(:,:,2);
B = I(:,:,3);

mascares = { R > 128 & G < 100 & B < 100, ...   % Vermell
             G > 128 & R < 100 & B < 100, ...   % Verd
             B > 128 & R < 100 & G < 100 };     % Blau
lletraColor = 'RGB';

%% Deteccio de figures
% Per cada figura guardem: forma, color, area i centroide.
figures = struct('forma', {}, 'color', {}, 'area', {}, 'centroide', {});

for c = 1:3
    bw = mascares{c};
    bw = bwareaopen(bw, 50);          % eliminar soroll (punts petits)
    bw = imfill(bw, 'holes');         % omplir forats
    se = strel('disk', 1);
    bw = imdilate(imerode(bw, se), se);   % obertura: suavitzar vores

    cc    = bwconncomp(bw, 8);
    props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid', 'Perimeter');

    for k = 1:numel(props)
        % Extent = area / area de la bounding box
        %   quadrat  ~ 1
        %   cercle   ~ pi/4 = 0.785
        %   triangle ~ 0.5
        bb     = props(k).BoundingBox;
        extent = props(k).Area / (bb(3) * bb(4));

        if extent > 0.9
            forma = 'S';
        elseif extent > 0.65
            forma = 'C';
        else
            forma = 'T';
        end

        figures(end+1) = struct('forma', forma, ...
                                'color', lletraColor(c), ...
                                'area',  props(k).Area, ...
                                'centroide', props(k).Centroid); %#ok<SAGROW>
    end
end

%% Mida (opcional): ordenar per area dins de cada tipus de figura
% De cada forma n'hi ha tres (una de cada color) de mides diferents:
% la mes petita es 1, la mitjana 2 i la gran 3.
mida = zeros(1, numel(figures));
for f = 'CTS'
    idx = find([figures.forma] == f);
    [~, ordre] = sort([figures(idx).area]);
    mida(idx(ordre)) = 1:numel(idx);
end

%% Resultat: etiquetes sobre la imatge
figure, imshow(I), title('Figures detectades');
axis on;
hold on;
fprintf('\n%-8s %-8s %-8s %-8s %s\n', 'Etiqueta', 'Forma', 'Color', 'Mida', 'Centroide (x, y)');
for k = 1:numel(figures)
    etiqueta = sprintf('%c%c%d', figures(k).forma, figures(k).color, mida(k));
    cx = figures(k).centroide(1);
    cy = figures(k).centroide(2);
    text(cx, cy, etiqueta, 'Color', 'white', 'FontSize', 12, ...
         'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    fprintf('%-8s %-8c %-8c %-8d (%.0f, %.0f)\n', etiqueta, ...
            figures(k).forma, figures(k).color, mida(k), cx, cy);
end
hold off;
