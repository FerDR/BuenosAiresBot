#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 12:23:39 2019

@author: samantha
"""

import numpy as np
import skimage.measure as skm
from PIL import Image
import facebook as fb
from pathlib import Path

def distancia(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2+(y2-y1)**2)

def upload(message, access_token, img_path=None):
    graph = fb.GraphAPI(access_token)
    if img_path:
        post = graph.put_photo(image=open(img_path, 'rb'),
                               message=message)
    else:
        post = graph.put_object(parent_object='me',
                                connection_name='feed',
                                message=message)
    return post['post_id']
 
 
def getAccessToken(filename='access_token.txt'):
    return Path(filename).read_text().strip()

img = Image.open('baires.png')
r0,g0,b0,what = img.split()
rojo0 = np.array(r0)

# Sacarle los puntitos qeu valen 255 y conectan los barrios

#%%
imth = rojo0 < 159
labeled, N_objects = skm.label( imth, neighbors=8, return_num = True)
objects = skm.regionprops(labeled) 

props = [(object.area, object.label, object.centroid[0], object.centroid[1]) for object in objects]
props.sort(key=lambda x: x[0])
#%%
centroidx = np.zeros(48)
centroidy = np.zeros(48)
for i in range(48):
    centroidx[i] = props[-i-1][2]
    centroidy[i] = props[-i-1][3]
    
distancias = np.zeros((len(props),len(props)))
for i in range(len(props)):
    for j in range(len(props)):
        distancias[i,j] = distancia(centroidx[i],centroidy[i],centroidx[j],centroidy[j])

lejos = int(np.amax(distancias) + 100)
for i in range(len(props)):
    distancias[i,i] = lejos
labels = ['Palermo', 'Villa Lugano', 'Villa Soldati', 'Flores', 'Barracas', 'Mataderos', 'Caballito', 'Villa Devoto', 'Belgrano', 'Nueva Pompeya', 'Villa Urquiza', 'Saavedra', 'Parque Avellaneda', 'Recoleta', 'Balvanera', 'Liniers', 'Almagro', 'Villa Riachuelo', 'Villa Crespo', 'Parque Chacabuco', 'Parque Patricios', 'Nuñez', 'Villa del Parque', 'Villa Pueyrredón', 'La Boca', 'Retiro', 'Chacarita', 'Monte Castro', 'Boedo', 'Villa Luro', 'Puerto Madero', 'Agronomía', 'Vélez Sarsfield', 'Floresta', 'Colegiales', 'Villa General Mitre', 'San Nicolás', 'Paternal', 'Constitución', 'Villa Santa Rita', 'Monserrat', 'San Cristóbal', 'Villa Ortúzar', 'Versalles', 'San Telmo', 'Coghlan', 'Villa Real', 'Parque Chas']


#%%
borders = np.zeros((len(props),np.shape(rojo0)[0],np.shape(rojo0)[1]))
for i in range(len(props)):
    cont = skm.find_contours(labeled == props[-i-1][1],0.1,positive_orientation='high')[0]
    #cont = engordar_borde(cont)
    for j in range(len(cont)):
        borders[i,int(cont[j][0]),int(cont[j][1])] = True
    for k in range(20):
        cont = skm.find_contours(borders[i],0)[0]
        for l in range(len(cont)):
            borders[i,int(cont[l][0]),int(cont[l][1])] = True
#%%
vecinos = list(range(len(props)))
for i in range(len(props)):
    vecinos[i] = []
    for j in range(len(props)):
        if np.any((borders[i] + borders[j]) == 2):
            vecinos[i].append(j)
              
#%%
for i in range(len(props)):
    for j in vecinos[i]:
          borders[i] = borders[i]+2*(labeled==props[-1-j][1])
          borders[i] = (borders[i] == 1)
          
#%%
fronteras = np.zeros(np.shape(rojo0))
for i in range(len(props)):
    fronteras = fronteras + 2**i*borders[i]          
#%%
rojo = [255,0,255,51,128,128,128,0,255,0,0,0,0,0,128,0,64,128,198,128,0,255,255,240,0,128,255,128,64,0,255,128,64,166,128,0,0,0,255,240,0,128,255,220,128,128,64,192]
verde = [128,64,0,51,128,128,255,255,255,0,64,255,128,255,0,64,128,64,89,0,128,128,128,240,0,128,255,128,0,128,128,0,0,68,255,128,0,255,0,0,147,0,128,170,128,64,0,192]
azul = [0,64,255,51,255,64,128,128,0,160,128,0,0,255,0,0,128,64,187,128,128,192,128,240,128,192,128,0,0,64,255,64,64,219,0,255,64,64,128,0,172,255,64,67,128,0,128,192]

matr = np.zeros(np.shape(rojo0))
matg = np.zeros(np.shape(rojo0))
matb = np.zeros(np.shape(rojo0))
for i in range(len(props)):
    matr = matr+(labeled == props[-i-1][1])*rojo[i]
    matg = matg+(labeled == props[-i-1][1])*verde[i]
    matb = matb+(labeled == props[-i-1][1])*azul[i]
#%%
r = Image.fromarray(matr).convert('L')
b = Image.fromarray(matb).convert('L')
g = Image.fromarray(matg).convert('L')
im = Image.merge("RGB", (r, g, b))
#im.show()
#%%
im.save('start.png')
np.save('matr',matr)
np.save('matg',matg)
np.save('matb',matb)
np.save('rojo',rojo)
np.save('verde',verde)
np.save('azul',azul)
np.save('labels',labels)
np.save('distancias',distancias)
#np.save('borders',borders)
np.save('fronteras',fronteras)