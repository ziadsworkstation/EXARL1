%% ========================================================================
%%
% 
%  PRÁCTICA 3 (SOLUCIÓN): CLASIFICACIÓN DE FIGURAS POR FORMA, TAMAÑO Y COLOR
%  ========================================================================
%  Objetivo: a partir de una imagen con figuras geométricas (círculos,
%  triángulos y cuadrados) de distintos tamaños y colores, el programa
%  etiqueta cada figura con tres datos:
%
%%
% 
%     - FORMA:   C (círculo), T (triángulo), S (cuadrado)
%     - COLOR:   R (rojo), G (verde), B (azul)
%     - TAMAÑO:  1 (pequeño), 2 (mediano), 3 (grande) dentro de su forma
%
%%
% 
%  Ejemplo de etiqueta en pantalla: "CR1" = círculo rojo pequeño.
%
%%
% 
%  Esquema del algoritmo:
%    1) Convertir a gris y binarizar para separar figuras del fondo.
%    2) Limpiar con morfología y etiquetar cada figura (componentes conexas).
%    3) Clasificar la FORMA usando la circularidad.
%    4) Ordenar por área para asignar el TAMAÑO.
%    5) Leer el color del píxel central de cada figura.
%
%%
% 
%  IMPORTANTE: el programa supone que hay exactamente 9 figuras: 3 círculos,
%  3 triángulos y 3 cuadrados (3 tamaños de cada forma).
%  =========================================================================
%

clear all;   % Borra todas las variables del espacio de trabajo
close all    % Cierra todas las figuras abiertas

% --- 1) LECTURA Y PREPROCESADO -----------------------------------------
I = imread('imagen2.jpg');   % Imagen a color (matriz alto x ancho x 3: R,G,B)
imshow(I);                   % La mostramos: sobre ella escribiremos las etiquetas
hold on                      % Mantiene la imagen para dibujar texto encima

Igris=rgb2gray(I);           % Pasamos a escala de grises (1 solo canal)
figure, imshow(Igris);      % (línea de depuración: descomentar para ver el paso)

Igris2 = imadjust(Igris);    % Estiramos el contraste para facilitar la binarización
figure, imshow(Igris2);

% --- 2) BINARIZACIÓN Y LIMPIEZA ----------------------------------------
% Umbral fijo de 0.11 (en escala 0-1): todo lo que sea más claro que el 11 %
% pasa a blanco (figura) y el resto a negro (fondo).
% Inicialmente era 0.1, pero en la imagen 3 un píxel suelto superaba el
% umbral y se detectaba como un círculo (10 objetos en vez de 9).
bw = imbinarize(Igris2, 0.11);

se1 = strel('disk',1);       % Elemento estructurante: disco de radio 1 píxel
bw1 = imdilate(bw,se1);      % Dilatación: rellena pequeños huecos
bw2 = imerode(bw1,se1);      % Erosión: recupera el tamaño original
                             % (dilatación + erosión = operación de CIERRE)
figure, imshow(bw);

% --- 3) ETIQUETADO Y MEDICIÓN DE FIGURAS -------------------------------
% Componentes conexas con conectividad de 4 vecinos: cada figura blanca
% separada del resto se convierte en un objeto distinto.
cc = bwconncomp(bw2, 4);

% Calculamos todas las propiedades de cada objeto (área, centroide,
% circularidad, excentricidad...)
im_data = regionprops(cc, 'all');

N=length(im_data);                         % Número de figuras detectadas
circularidades=[im_data.Circularity];      % Vector con la circularidad de cada figura
excentricidades=[im_data.Eccentricity];    % (se calcula, pero no se usa después)
areas=[im_data.Area];                      % Vector con el área (en píxeles) de cada figura

% --- 4) CLASIFICACIÓN DE LA FORMA POR CIRCULARIDAD ---------------------
% Circularidad = 4π · Área / Perímetro²
% La circularidad vale 1 para un círculo perfecto y disminuye cuanto más
% "picuda" es la figura. Valores teóricos aproximados:
%     círculo ≈ 1   |   cuadrado ≈ 0.785   |   triángulo equilátero ≈ 0.605
% Se definen dos umbrales intermedios para separar las tres clases:
cuadTriang=0.74;   % Por debajo de este valor -> triángulo
circCuad=0.93;     % Por encima de este valor -> círculo
                   % Entre ambos             -> cuadrado

% Contadores para ir rellenando cada lista (círculos, triángulos, cuadrados)
ic=1;it=1;is=1;

for i=1:N                                  % Recorremos todas las figuras
    if circularidades(i)>circCuad
        tipo(i)='C';                       % Círculo
        circulos(ic,:)=[i areas(i)];       % Guardamos [nº de figura, área]
        ic=ic+1;
    elseif circularidades(i)<cuadTriang
        tipo(i)='T';                       % Triángulo
        triangulos(it,:)=[i areas(i)];
        it=it+1;
    else
        tipo(i)='S';                       % Cuadrado (S de "Square")
        cuadrados(is,:)=[i areas(i)];
        is=is+1;
    end
end

% --- 5) ASIGNACIÓN DEL TAMAÑO (1, 2 o 3) -------------------------------
% Dentro de cada forma, ordenamos las figuras de menor a mayor área
% (columna 2). Después de ordenar, la primera es la pequeña, la segunda la
% mediana y la tercera la grande.
    circulos=sortrows(circulos,2);
    triangulos=sortrows(triangulos,2);
    cuadrados=sortrows(cuadrados,2);

    % Lista de números de figura ordenados: círculos, luego triángulos,
    % luego cuadrados, y dentro de cada grupo de menor a mayor área
    tamanos=[circulos(:,1);triangulos(:,1);cuadrados(:,1)];

    % Emparejamos cada figura con su tamaño (1,2,3 repetido para cada forma)
    etiquetas=[tamanos [1;2;3;1;2;3;1;2;3]];

    % Reordenamos por número de figura para que la fila i corresponda a la
    % figura i. Así etiquetas(i,2) es el tamaño de la figura i.
    etiquetas=sortrows(etiquetas,1);

% --- 6) DETECCIÓN DEL COLOR Y ESCRITURA DE LA ETIQUETA -----------------
figure, imshow(I)

for i=1:N

    % Leemos el color RGB del píxel situado en el centro (centroide) de la
    % figura. Ojo: en una imagen, primero va la FILA (coordenada Y) y luego
    % la COLUMNA (coordenada X), por eso se usa Centroid(2) y luego Centroid(1).
    % Al no llevar punto y coma, también imprime los valores RGB por consola.
    colores(i,:)=I(round(im_data(i).Centroid(2)),round(im_data(i).Centroid(1)),:)

    % Decidimos el color según qué canal es más intenso (>200 de 255):
    if I(round(im_data(i).Centroid(2)),round(im_data(i).Centroid(1)),1)>200
        color(i)='R';          % Canal rojo alto -> rojo
    elseif I(round(im_data(i).Centroid(2)),round(im_data(i).Centroid(1)),2)>200
        color(i)='G';          % Canal verde alto -> verde
    else
        color(i)='B';          % En otro caso -> azul
    end

    % Escribimos sobre la imagen la etiqueta compuesta: forma + color + tamaño
    % Por ejemplo: 'T' + 'G' + '2' = "TG2" (triángulo verde mediano)
    text(im_data(i).Centroid(1),im_data(i).Centroid(2),[tipo(i) color(i) num2str(etiquetas(i,2))],'color','white','FontSize',14);
end