%% ========================================================================
%  EJEMPLOS DE VISIÓN ARTIFICIAL CON MATLAB (Image Processing Toolbox)
%  ========================================================================
%  Este script contiene dos ejemplos independientes:
%    - Ejemplo 1: mejora del contraste mediante ecualización del histograma.
%    - Ejemplo 2: segmentación y medición de objetos (granos de arroz).
%
%  Cada ejemplo está en una "sección" (empieza con %%). Se puede ejecutar
%  sección por sección con Ctrl+Enter para ver el resultado de cada paso.
%  Las imágenes 'pout.tif' y 'rice.png' vienen incluidas con MATLAB.
% =========================================================================

clear all;   % Borra todas las variables del espacio de trabajo
close all    % Cierra todas las figuras abiertas

%% ========================================================================
%  EJEMPLO 1: ECUALIZACIÓN DEL HISTOGRAMA (mejora de contraste)
%  ========================================================================
%  Idea: una imagen con poco contraste tiene sus niveles de gris
%  concentrados en un rango estrecho. La ecualización reparte esos niveles
%  por todo el rango disponible (0-255) y hace que la imagen se vea con
%  más contraste.

% Leemos la imagen y la guardamos en la variable I.
% Es una imagen en escala de grises: una matriz donde cada elemento es
% un píxel con un valor de 0 (negro) a 255 (blanco).
I = imread('pout.tif');
imshow(I);                 % Mostramos la imagen original

% Histograma: cuántos píxeles hay de cada nivel de gris.
% Se observará que está concentrado en una zona pequeña (poco contraste).
figure, imhist(I)

% Ecualizamos el histograma para redistribuir los niveles de gris
I2 = histeq(I);
figure, imshow(I2)         % Imagen con el contraste mejorado

% El nuevo histograma está mucho más repartido a lo largo de todo el rango
figure, imhist(I2)

% Guardamos la imagen resultante en un archivo PNG
imwrite (I2, 'pout2.png');

%% ========================================================================
%  EJEMPLO 2: SEGMENTACIÓN Y MEDICIÓN DE OBJETOS (granos de arroz)
%  ========================================================================
%  Objetivo: detectar cada grano de arroz de la imagen, contornearlo y
%  encontrar cuál es el más pequeño y cuál el más grande (por área).
%
%  Pasos habituales en visión artificial:
%    1) Preprocesado  ->  2) Binarización  ->  3) Limpieza (morfología)
%    ->  4) Etiquetado de objetos  ->  5) Medición de propiedades

%close all

% --- 1) PREPROCESADO ---------------------------------------------------
I = imread('rice.png');    % Leemos la imagen (escala de grises)
figure, imshow(I);         % Imagen original

% imadjust estira el contraste: reasigna los niveles de gris para que
% ocupen todo el rango disponible
I3 = imadjust(I);
figure, imshow(I3);

% --- 2) BINARIZACIÓN ---------------------------------------------------
% graythresh calcula automáticamente el umbral óptimo (método de Otsu).
% Devuelve un valor entre 0 y 1.
level = graythresh(I3);

% Convertimos a imagen binaria: los píxeles por encima del umbral pasan a
% 1 (blanco = objeto) y el resto a 0 (negro = fondo).
% Nota: im2bw está obsoleta en versiones recientes de MATLAB; la función
% actual equivalente es imbinarize(I3, level).
bw = im2bw(I3,level);
figure, imshow(bw);

% --- 3) LIMPIEZA (operaciones morfológicas) ----------------------------
% Eliminamos los objetos pequeños (ruido) con menos de 50 píxeles
bw1 = bwareaopen(bw, 50);
figure, imshow(bw1)

% Rellenamos los agujeros que quedan dentro de los granos
bw2 = imfill(bw1,'holes');
figure, imshow(bw2)

% Elemento estructurante: la "forma" con la que se recorre la imagen en
% las operaciones morfológicas. Aquí, un disco de radio 1 píxel.
se1 = strel('disk',1);

% Erosión: "adelgaza" los objetos. Elimina píxeles sueltos y separa
% granos que estaban muy juntos.
bw3 = imerode(bw2,se1);
figure, imshow(bw3);

% Dilatación: "engorda" los objetos para recuperar su tamaño original.
% Erosión + dilatación seguidas = operación de APERTURA.
bw4 = imdilate(bw3,se1);
figure, imshow(bw4);

% --- 4) CONTORNOS Y ETIQUETADO DE OBJETOS ------------------------------
% bwboundaries devuelve el contorno de cada objeto como una lista de
% coordenadas (fila, columna). boundaries{k} es el contorno del objeto k.
boundaries = bwboundaries(bw4);

% Mostramos la imagen original para dibujar los contornos encima
figure, imshow(I);

hold on;   % Mantiene lo ya dibujado para añadir más elementos encima
for k=1:size(boundaries,1),    % Recorremos todos los objetos detectados
   b = boundaries{k};          % Coordenadas del contorno del objeto k
   % b(:,2) son las columnas (eje X) y b(:,1) las filas (eje Y)
   plot(b(:,2),b(:,1),'g','LineWidth',1);   % Contorno en verde
end

% Componentes conexas: agrupa los píxeles blancos que están conectados,
% de forma que cada grano es un objeto distinto. El 4 indica conectividad
% de 4 vecinos (arriba, abajo, izquierda, derecha).
cc = bwconncomp(bw4, 4);

% --- 5) MEDICIÓN DE PROPIEDADES ----------------------------------------
% regionprops calcula propiedades de cada objeto (área, centroide,
% perímetro, orientación...). Con 'all' se calculan todas.
arrozdata = regionprops(cc, 'all');%'all'

% Extraemos el área (nº de píxeles) de cada grano en un vector
arroz_areas=[arrozdata.Area];

% Grano más pequeño: min devuelve el valor mínimo y su posición (índice)
[min_area, i_min] = min(arroz_areas);
% Marcamos su centro (centroide) con una cruz roja
plot(arrozdata(i_min).Centroid(1),arrozdata(i_min).Centroid(2),'r+');

% Grano más grande: mismo procedimiento con max
[max_area, i_max] = max(arroz_areas);
plot(arrozdata(i_max).Centroid(1),arrozdata(i_max).Centroid(2),'r+');

% Creamos una imagen binaria vacía (todo a 0) del mismo tamaño y
% activamos solo los píxeles del grano más pequeño y del más grande
arroz = false(size(bw4));
arroz(cc.PixelIdxList{i_min}) = true;
arroz(cc.PixelIdxList{i_max}) = true;
figure, imshow(arroz);   % Se ven únicamente esos dos granos

% Escribimos el valor del área junto a cada grano marcado.
% Nota: text se dibuja sobre la figura activa, que ahora es la de 'arroz'.
% Si se quiere ver el texto sobre la imagen original con los contornos,
% hay que ejecutar estas líneas antes del figure, imshow(arroz) anterior.
text(arrozdata(i_max).Centroid(1),arrozdata(i_max).Centroid(2),num2str(arroz_areas(i_max)),'color','red');
text(arrozdata(i_min).Centroid(1),arrozdata(i_min).Centroid(2),num2str(arroz_areas(i_min)),'color','red');
