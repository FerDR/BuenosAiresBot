#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 12:23:39 2019

@author: samantha
"""

import numpy as np
from matplotlib import pyplot as plt
import skimage.measure as skm
from PIL import Image
import urllib3
import requests
import facebook as fb
from bs4 import BeautifulSoup
from PIL import Image
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
"""
l = rojo.shape[0]
mat = np.zeros((l,l))
#areas = np.zeros((l,l,len(props)))
plt.ion()
plt.figure()
for i in range(len(props)):
    #areas[:,:,i] = ( labeled == props[-i][1] )
    #mat = mat + (i+10)*areas[:,:,i]
    mat = mat + (i+10)*( labeled == props[-i][1] )
    plt.imshow(mat)
    plt.title(i)
    plt.pause(0.5)
    print(i)
#plt.imshow(mat, cmap='tab20')
"""
#%%
centroidx = np.zeros(48)
centroidy = np.zeros(48)
for i in range(48):
    centroidx[i] = props[-i-1][2]
    centroidy[i] = props[-i-1][3]
    
distancias = np.zeros((48,48))
for i in range(48):
    for j in range(48):
        distancias[i,j] = distancia(centroidx[i],centroidy[i],centroidx[j],centroidy[j])

for i in range(48):
    distancias[i,i] = 3000
labels = ['Palermo', 'Villa Lugano', 'Villa Soldati', 'Flores', 'Barracas', 'Mataderos', 'Caballito', 'Villa Devoto', 'Belgrano', 'Nueva Pompeya', 'Villa Urquiza', 'Saavedra', 'Parque Avellaneda', 'Recoleta', 'Balvanera', 'Liniers', 'Almagro', 'Villa Riachuelo', 'Villa Crespo', 'Parque Chacabuco', 'Parque Patricios', 'Nuñez', 'Villa del Parque', 'Villa Pueyrredón', 'La Boca', 'Retiro', 'Chacarita', 'Monte Castro', 'Boedo', 'Villa Luro', 'Puerto Madero', 'Agronomía', 'Vélez Sarsfield', 'Floresta', 'Colegiales', 'Villa General Mitre', 'San Nicolás', 'Paternal', 'Constitución', 'Santa Rita', 'Monserrat', 'San Cristóbal', 'Villa Ortúzar', 'Versalles', 'San Telmo', 'Coghlan', 'Villa Real', 'Parque Chas']
rojo = [255,0,255,51,128,128,128,0,255,0,0,0,0,0,128,0,64,128,198,128,0,255,255,240,0,128,255,128,64,0,255,128,64,166,128,0,0,0,255,255,0,128,255,220,128,128,64,192]
verde = [128,64,0,51,128,128,255,255,255,0,64,255,128,255,0,64,128,64,89,0,128,128,128,240,0,128,255,128,0,128,128,0,0,68,255,128,0,255,0,0,147,0,128,170,128,64,0,192]
azul = [0,64,255,51,255,64,128,128,0,160,128,0,0,255,0,0,128,64,187,128,128,192,128,240,128,192,128,0,0,64,255,64,64,219,0,255,64,64,128,0,172,255,64,67,128,0,128,192]

matr = np.zeros((2400,2400))
matg = np.zeros((2400,2400))
matb = np.zeros((2400,2400))
for i in range(48):
    matr = matr+(labeled == props[-i-1][1])*rojo[i]
    matg = matg+(labeled == props[-i-1][1])*verde[i]
    matb = matb+(labeled == props[-i-1][1])*azul[i]
"""
r = Image.fromarray(matr).convert('L')
b = Image.fromarray(matb).convert('L')
g = Image.fromarray(matg).convert('L')
im = Image.merge("RGB", (r, g, b))
im.show()
im.save('start.png')
"""
#%%
rojo2 = np.copy(rojo)
verde2 = np.copy(verde)
azul2 = np.copy(azul)
matr2 = np.copy(matr)
matb2 = np.copy(matb)
matg2 = np.copy(matg)
d2 = np.copy(distancias)
l2 = np.copy(labels)
end = False
i = 0

while i < 1:
    attack = np.random.randint(0,48)
    if np.any(l2[:] != l2[attack]):
        defender = np.argmin(d2[attack][:])
        
        for j in range(48):
            if l2[j] == l2[attack]:
                d2[defender][j] = 3000
                d2[j][defender] = 3000
            if l2[j] == l2[defender]:
                d2[defender][j] = distancias[defender][j]
                d2[j][defender] = distancias[j][defender]
        pre = len(np.unique(l2))
        lpre = l2[defender]
        l2[defender] = l2[attack]
        posterior = len(np.unique(l2))
        #desde aca es para hacer la imagen, comentar para mayor velocidad
        matr2 = matr2-matr2*(labeled == props[-defender-1][1])
        matr2 = matr2 + (labeled == props[-defender-1][1])*rojo2[attack]
        matg2 = matg2-matg2*(labeled == props[-defender-1][1])
        matg2 = matg2 + (labeled == props[-defender-1][1])*verde2[attack]
        matb2 = matb2-matb2*(labeled == props[-defender-1][1])
        matb2 = matb2 + (labeled == props[-defender-1][1])*azul2[attack]
        rojo2[defender] = rojo2[attack]
        verde2[defender] = verde2[attack]
        azul2[defender] = azul2[attack]
        r = Image.fromarray(matr2).convert('L')
        g = Image.fromarray(matg2).convert('L')
        b = Image.fromarray(matb2).convert('L')
        im = Image.merge("RGB", (r, g, b))
        im.save('./run3/'+str(i)+'.png')
        #aca termina lo de la imagen
  
        status_text = l2[attack]+' conquistó al barrio de '+labels[defender]
        if lpre != labels[defender]:
            status_text = status_text + ', previamente bajo el control de '+lpre
        if pre!= posterior:
            status_text = status_text +'. '+ lpre + ' ha sido completamente eliminado, quedan '+str(posterior)+' barrios.'
        else:
            status_text = status_text+'.'
        upload(status_text, getAccessToken(), './run3/'+str(i)+'.png')
        #print(l2[attack]+' conquisto a '+labels[defender]+' desde '+labels[attack])
        print(status_text)
        i = i+1
    else:
        end = True
        #print(i)
        print('gano '+l2[0])

#%%
"""
turnos = []
winners = []
for k in range(10000):
    rojo2 = np.copy(rojo)
    verde2 = np.copy(verde)
    azul2 = np.copy(azul)
    matr2 = np.copy(matr)
    matb2 = np.copy(matb)
    matg2 = np.copy(matg)
    d2 = np.copy(distancias)
    l2 = np.copy(labels)
    end = False
    i = 0
    
    while not end:
        attack = np.random.randint(0,48)
        if np.any(l2[:] != l2[attack]):
            defender = np.argmin(d2[attack][:])
            for j in range(48):
                if l2[j] == l2[attack]:
                    d2[defender][j] = 3000
                    d2[j][defender] = 3000
                if l2[j] == l2[defender]:
                    d2[defender][j] = distancias[defender][j]
                    d2[j][defender] = distancias[j][defender]
            l2[defender] = l2[attack]
            i = i+1
            #print(l2[attack]+' conquisto a '+labels[defender]+' desde '+labels[attack])
            
        else:
            end = True
            #print(i)
            turnos.append(i)
            winners.append(l2[0])
            if int(k/100)!=int((k-1)/100):
                print(str(int(k/100))+"%")
            #print('gano '+l2[0])
            #ti.append(time.time()-t)
            
#%%
winnum = []
for i in range(len(winners)):
    for j in range(len(labels)):
        if winners[i]==labels[j]:
            winnum.append(j)
"""