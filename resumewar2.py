# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 08:09:18 2019

@author: Fer
"""

import numpy as np
from matplotlib import pyplot as plt
import skimage.measure as skm
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import facebook as fb
from pathlib import Path
import time

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
    
def recoloreo(M,atk,defe,colorarr):
    m = M-M*(labeled == props[-defe-1][1])
    m = m + (labeled == props[-defe-1][1])*colorarr[atk]
    return m

def suma_255(m1,m2):
    return m1+255*m2

def save_all(names,files):
    if len(names)!=len(files):
        raise ValueError('Los elementos deben tener la misma longitud')
    for i in range(len(names)):
        np.save(names[i],files[i])
    return 0

def replace(vec,chau,hola):
     vec[chau] = vec[hola]
     return vec
 
def three_times(f,a,b,c):
    return f(*a),f(*b),f(*c)
       
def hacer_imagen(mat):
    return Image.fromarray(mat).convert('L')
    
def gen_text(text,place,color):
    tw,th = draw.textsize(text,font = font)
    x0 = centroidy[place]-tw/2
    y0 = centroidx[place]-th/2
    draw.text((x0-1,y0),text,font = font,fill = "black")
    draw.text((x0+1,y0),text,font = font,fill = "black")
    draw.text((x0,y0+1),text,font = font,fill = "black")
    draw.text((x0,y0-1),text,font = font,fill = "black")
    draw.text((x0,y0),text,font = font, fill = color)
    return draw
#%%
img0 = Image.open('baires.png')
r0,g0,b0,what = img0.split()
rojo0 = np.array(r0)

#%%
imth = rojo0 < 159
labeled, N_objects = skm.label( imth, neighbors=8, return_num = True)
objects = skm.regionprops(labeled) 

props = [(object.area, object.label, object.centroid[0], object.centroid[1]) for object in objects]
props.sort(key=lambda x: x[0])

centroidx = np.zeros(len(props))
centroidy = np.zeros(len(props))
for i in range(len(props)):
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
font = ImageFont.truetype("arial.ttf",60)
#borders = np.load('borders.npy')
borders = np.load('fronteras.npy')
end = False
#%%
rojo2 = np.load('rojo.npy')
verde2 = np.load('verde.npy')
azul2 = np.load('azul.npy')
matr2 = np.load('matr.npy')
matb2 = np.load('matb.npy')
matg2 = np.load('matg.npy')
d2 = np.load('distancias.npy')
l2 = np.load('labels.npy')
i = 0

#%%
while not end:
    attack = np.random.randint(0,len(props))
    if np.any(l2[:] != l2[attack]):
        defender = np.argmin(d2[attack][:]) 
        for j in range(len(props)):
            if l2[j] == l2[attack]:#cambia la distancia del perdedor al ganador y sus aliados
                d2[defender][j] = lejos
                d2[j][defender] = lejos
            if l2[j] == l2[defender]:#cambia la distancia del perdedor a sus ex-aliados
                d2[defender][j] = distancias[defender][j]
                d2[j][defender] = distancias[j][defender]
        pre = len(np.unique(l2))
        lpre = l2[defender]
        matr2,matg2,matb2 = three_times(recoloreo,[matr2,attack,defender,rojo2],[matg2,attack,defender,verde2],[matb2,attack,defender,azul2])
        rojo2,verde2,azul2 = three_times(replace,[rojo2,defender,attack],[verde2,defender,attack],[azul2,defender,attack])
        we = save_all(['matr','matg','matb','rojo','verde','azul','labels','distancias'],[matr2,matg2,matb2,rojo2,verde2,azul2,l2,d2])
        borderr = (borders/(2**defender))%2 >= 1
        borderg, borderb = np.zeros(np.shape(r0)),np.zeros(np.shape(r0))
        for j in range(len(props)):
            if l2[j] == l2[attack]:
                borderg = borderg+((borders/(2**j))%2 >= 1)
        l2[defender] = l2[attack]
        posterior = len(np.unique(l2))
        for j in range(len(props)):
            if l2[j] == lpre:
                borderb = borderb+((borders/(2**j))%2 >= 1)
        borderg = (borderg==1)
        borderb = (borderb==1)
        borderg = (borderg-(borderg*borderr))==1
        borderb = (borderb-(borderg*borderb))==1
        borderb = (borderb-(borderr*borderb))==1
        matrp,matgp,matbp = three_times(suma_255,[matr2,borderr],[matg2,borderg],[matb2,borderb])
        r,g,b = three_times(hacer_imagen,[matrp],[matgp],[matbp])
        im = Image.merge("RGB", (r, g, b))
        draw = ImageDraw.Draw(im)
        draw = gen_text(labels[defender],defender,"red")
        draw = gen_text(l2[defender],attack,"green")
        if pre==posterior:
            exaliado = np.argwhere(l2 == lpre)[0][0]
            draw = gen_text(lpre,exaliado,"blue")
        im.save('imagen.png')  
        status_text = l2[attack]+' conquistó al barrio de '+labels[defender]
        if lpre != labels[defender]:
            status_text = status_text + ', previamente bajo el control de '+lpre
        if pre!= posterior:
            if posterior > 1:
                status_text = status_text +'. '+ lpre + ' ha sido completamente eliminado, quedan '+str(posterior)+' barrios.'
            else:
                status_text = status_text +'. '+ lpre + ' ha sido completamente eliminado, '+l2[0]+' es el barrio campeón de la Ciudad de Buenos Aires.'
        else:
            status_text = status_text+'.'
        upload(status_text, getAccessToken(), 'imagen.png')
        #print(l2[attack]+' conquisto a '+labels[defender]+' desde '+labels[attack])
        print(status_text)
        i = i+1
        time.sleep(60*60)
    else:
        end = True
        #print(i)
        print('gano '+l2[0])
