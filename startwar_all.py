#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 12:23:39 2019

@author: Fer
"""

import numpy as np
import skimage.measure as skm
from PIL import Image
import pandas as pd

def distancia(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2+(y2-y1)**2)

def hex_to_rgb(hexa):
    return list(int(hexa.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def arrancar(lugar,condicion,valor,neighb = 8, pacman = False):
    img = Image.open(lugar+'.png')
    r0,g0,b0,what = img.split()
    rojo0 = np.array(r0)
    azul0 = np.array(b0)
    # Sacarle los puntitos qeu valen 255 y conectan los barrios
    
    #%%
    if lugar == 'partidoscaba' or lugar == 'partidossincaba':
        im1 = azul0 > 200
        im2 = rojo0 < 50
        imth = im1*im2
    elif condicion == '<':
        imth = rojo0 < valor
    elif condicion == '>':
        imth = rojo0 > valor
    else:
        raise ValueError('Condicion no valida, inserte < o >')
    labeled, N_objects = skm.label( imth, neighbors=neighb, return_num = True)
    objects = skm.regionprops(labeled) 
    
    props = [(object.area, object.label, object.centroid[0], object.centroid[1]) for object in objects]
    #props.sort(key=lambda x: x[0])
    #%%
    centroidx = np.zeros(len(props))
    centroidy = np.zeros(len(props))
    for i in range(len(props)):
        centroidx[i] = props[i][2]
        centroidy[i] = props[i][3]
        
    distancias = np.zeros((len(props),len(props)))
    for i in range(len(props)):
        for j in range(len(props)):
            if pacman:
                L,H = np.shape(imth)
                aes = np.zeros(9)
                aes[0] = distancia(centroidx[i],centroidy[i],centroidx[j],centroidy[j])
                aes[1] = distancia(centroidx[i],centroidy[i],centroidx[j] + L,centroidy[j])
                aes[2] = distancia(centroidx[i],centroidy[i],centroidx[j] - L,centroidy[j])
                aes[3] = distancia(centroidx[i],centroidy[i],centroidx[j],centroidy[j] + H)
                aes[4] = distancia(centroidx[i],centroidy[i],centroidx[j],centroidy[j] - H)
                aes[5] = distancia(centroidx[i],centroidy[i],centroidx[j] + L,centroidy[j] + H)
                aes[6] = distancia(centroidx[i],centroidy[i],centroidx[j] + L,centroidy[j] - H)
                aes[7] = distancia(centroidx[i],centroidy[i],centroidx[j] - L,centroidy[j] + H)
                aes[8] = distancia(centroidx[i],centroidy[i],centroidx[j] - L,centroidy[j] - H)
                distancias[i,j] = np.min(aes)
            else:
                distancias[i,j] = distancia(centroidx[i],centroidy[i],centroidx[j],centroidy[j])
        
    lejos = int(np.amax(distancias) + 100)
    
    for i in range(len(props)):
        distancias[i,i] = lejos
    
    if lugar == 'baires':
        #labels = ['Palermo', 'Villa Lugano', 'Villa Soldati', 'Flores', 'Barracas', 'Mataderos', 'Caballito', 'Villa Devoto', 'Belgrano', 'Nueva Pompeya', 'Villa Urquiza', 'Saavedra', 'Parque Avellaneda', 'Recoleta', 'Balvanera', 'Liniers', 'Almagro', 'Villa Riachuelo', 'Villa Crespo', 'Parque Chacabuco', 'Parque Patricios', 'Nuñez', 'Villa del Parque', 'Villa Pueyrredón', 'La Boca', 'Retiro', 'Chacarita', 'Monte Castro', 'Boedo', 'Villa Luro', 'Puerto Madero', 'Agronomía', 'Vélez Sarsfield', 'Floresta', 'Colegiales', 'Villa General Mitre', 'San Nicolás', 'Paternal', 'Constitución', 'Villa Santa Rita', 'Monserrat', 'San Cristóbal', 'Villa Ortúzar', 'Versalles', 'San Telmo', 'Coghlan', 'Villa Real', 'Parque Chas']
        labels = ['Núñez','Saavedra','Belgrano','Palermo','Coghlan','Villa Urquiza','Colegiales','Villa Pueyrredón','Recoleta','Villa Ortúzar','Parque Chas','Chacarita','Retiro','Villa Devoto','Villa Crespo','Agronomía','Paternal','Villa del Parque','Almagro','Balvanera','Puerto Madero','San Nicolás','Villa General Mitre','Caballito','Villa Santa Rita','Monserrat','Monte Castro','Villa Real','Flores','San Telmo','Floresta','Constitución','San Cristóbal','Boedo','Vélez Sarsfield','Versalles','Villa Luro','La Boca','Parque Chacabuco','Parque Patricios','Barracas','Liniers','Parque Avellaneda','Nueva Pompeya','Mataderos','Villa Soldati','Villa Lugano','Villa Riachuelo']
    if lugar == 'argentina':
        labels = ['Jujuy','Salta','Formosa','Chaco','Catamarca','Santiago del Estero','Misiones','Tucumán','Corrientes','La Rioja','Santa Fe','San Juan','Córdoba','Entre Ríos','San Luis','Mendoza','Buenos Aires','Capital Federal','La Pampa','Neuquén','Rio Negro','Chubut','Santa Cruz','Tierra del Fuego']
    if lugar == 'partidoscaba':
        labels = ['Escobar','Tigre','Pilar','San Fernando','Malvinas Argentinas','San Isidro','José C. Paz','Vicente López','San Martín','San Miguel','Moreno','General Rodríguez','Capital Federal','Tres de Febrero','Hurlingham','Morón','Ituzaingó','Avellaneda','La Matanza','Merlo','Lanús','Quilmes','Marcos Paz','Lomas de Zamora','Esteban Echeverría','Berazategui','Ezeiza','Almirante Brown','Florencio Varela','Ensenada','La Plata','Berisso','Presidente Perón','Cañuelas','San Vicente']
    if lugar == 'partidossincaba':
        labels = ['Escobar','Tigre','Pilar','San Fernando','Malvinas Argentinas','San Isidro','José C. Paz','Vicente López','San Martín','San Miguel','Moreno','General Rodríguez','Tres de Febrero','Hurlingham','Morón','Ituzaingó','Avellaneda','La Matanza','Merlo','Lanús','Quilmes','Marcos Paz','Lomas de Zamora','Esteban Echeverría','Berazategui','Ezeiza','Almirante Brown','Florencio Varela','Ensenada','La Plata','Berisso','Presidente Perón','Cañuelas','San Vicente']
  
    #%%
    borders = np.zeros((len(props),np.shape(rojo0)[0],np.shape(rojo0)[1]))
    for i in range(len(props)):
        cont = skm.find_contours(labeled == props[i][1],0.1,positive_orientation='high')[0]
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
              borders[i] = borders[i]+2*(labeled==props[j][1])
              borders[i] = (borders[i] == 1)
              
    #%%
    fronteras = np.zeros(np.shape(rojo0))
    for i in range(len(props)):
        fronteras = fronteras + 2**i*borders[i]  
    #%%
    if len(props) < 25:
        colors24 = ["#E61194B","#3CB44B","#FFE119","#4363D8","#F58231","#911EB4","#42D4F4","#F032E6","#BFEF45","#FABEBE","#469990","#E6BEFF","#9A6324","#FFFAC8","#800000","#AAFFC3","#808000","#FFD8B1","#000075","#A9A9A9","#FAFAFA","#FF0000","#00FF00","#0000FF"]
        rojo, verde, azul = [],[],[]
        for i in range(len(colors24)):
            rojo.append(hex_to_rgb(colors24[i])[0])
            verde.append(hex_to_rgb(colors24[i])[1])
            azul.append(hex_to_rgb(colors24[i])[2])
    elif len(props) < 63:
        col64 = np.array(pd.read_excel('col.xlsx'))
        rojo = col64[1:49,0]
        verde = col64[1:49,1]
        azul = col64[1:49,2]  
        
    elif len(props) < 268:
        colors269 = ["#000000","#FFFF00","#1CE6FF","#FF34FF","#FF4A46","#008941","#006FA6","#A30059","#FFDBE5","#7A4900","#0000A6","#63FFAC","#B79762","#004D43","#8FB0FF","#997D87","#5A0007","#809693","#FEFFE6","#1B4400","#4FC601","#3B5DFF","#4A3B53","#FF2F80","#61615A","#BA0900","#6B7900","#00C2A0","#FFAA92","#FF90C9","#B903AA","#D16100","#DDEFFF","#000035","#7B4F4B","#A1C299","#300018","#0AA6D8","#013349","#00846F","#372101","#FFB500","#C2FFED","#A079BF","#CC0744","#C0B9B2","#C2FF99","#001E09","#00489C","#6F0062","#0CBD66","#EEC3FF","#456D75","#B77B68","#7A87A1","#788D66","#885578","#FAD09F","#FF8A9A","#D157A0","#BEC459","#456648","#0086ED","#886F4C","#34362D","#B4A8BD","#00A6AA","#452C2C","#636375","#A3C8C9","#FF913F","#938A81","#575329","#00FECF","#B05B6F","#8CD0FF","#3B9700","#04F757","#C8A1A1","#1E6E00","#7900D7","#A77500","#6367A9","#A05837","#6B002C","#772600","#D790FF","#9B9700","#549E79","#FFF69F","#201625","#72418F","#BC23FF","#99ADC0","#3A2465","#922329","#5B4534","#FDE8DC","#404E55","#0089A3","#CB7E98","#A4E804","#324E72","#6A3A4C","#83AB58","#001C1E","#D1F7CE","#004B28","#C8D0F6","#A3A489","#806C66","#222800","#BF5650","#E83000","#66796D","#DA007C","#FF1A59","#8ADBB4","#1E0200","#5B4E51","#C895C5","#320033","#FF6832","#66E1D3","#CFCDAC","#D0AC94","#7ED379","#012C58","#7A7BFF","#D68E01","#353339","#78AFA1","#FEB2C6","#75797C","#837393","#943A4D","#B5F4FF","#D2DCD5","#9556BD","#6A714A","#001325","#02525F","#0AA3F7","#E98176","#DBD5DD","#5EBCD1","#3D4F44","#7E6405","#02684E","#962B75","#8D8546","#9695C5","#E773CE","#D86A78","#3E89BE","#CA834E","#518A87","#5B113C","#55813B","#E704C4","#00005F","#A97399","#4B8160","#59738A","#FF5DA7","#F7C9BF","#643127","#513A01","#6B94AA","#51A058","#A45B02","#1D1702","#E20027","#E7AB63","#4C6001","#9C6966","#64547B","#97979E","#006A66","#391406","#F4D749","#0045D2","#006C31","#DDB6D0","#7C6571","#9FB2A4","#00D891","#15A08A","#BC65E9","#FFFFFE","#C6DC99","#203B3C","#671190","#6B3A64","#F5E1FF","#FFA0F2","#CCAA35","#374527","#8BB400","#797868","#C6005A","#3B000A","#C86240","#29607C","#402334","#7D5A44","#CCB87C","#B88183","#AA5199","#B5D6C3","#A38469","#9F94F0","#A74571","#B894A6","#71BB8C","#00B433","#789EC9","#6D80BA","#953F00","#5EFF03","#E4FFFC","#1BE177","#BCB1E5","#76912F","#003109","#0060CD","#D20096","#895563","#29201D","#5B3213","#A76F42","#89412E","#1A3A2A","#494B5A","#A88C85","#F4ABAA","#A3F3AB","#00C6C8","#EA8B66","#958A9F","#BDC9D2","#9FA064","#BE4700","#658188","#83A485","#453C23","#47675D","#3A3F00","#061203","#DFFB71","#868E7E","#98D058","#6C8F7D","#D7BFC2","#3C3E6E","#D83D66","#2F5D9B","#6C5E46","#D25B88","#5B656C","#00B57F","#545C46","#866097","#365D25","#252F99","#00CCFF","#674E60","#FC009C","#92896B"]    
        rojo, verde, azul = [],[],[]
        for i in range(len(colors269)-1):
            rojo.append(hex_to_rgb(colors269[i+1])[0])
            verde.append(hex_to_rgb(colors269[i+1])[1])
            azul.append(hex_to_rgb(colors269[i+1])[2])
    else:
        raise ValueError('No alcanzan los colores')        
    #%%
     
    #%%
    """
    rojo = [255,0,255,51,128,128,128,0,255,0,0,0,0,0,128,0,64,128,198,128,0,255,255,240,0,128,255,128,64,0,255,128,64,166,128,0,0,0,255,240,0,128,255,220,128,128,64,192]
    verde = [128,64,0,51,128,128,255,255,255,0,64,255,128,255,0,64,128,64,89,0,128,128,128,240,0,128,255,128,0,128,128,0,0,68,255,128,0,255,0,0,147,0,128,170,128,64,0,192]
    azul = [0,64,255,51,255,64,128,128,0,160,128,0,0,255,0,0,128,64,187,128,128,192,128,240,128,192,128,0,0,64,255,64,64,219,0,255,64,64,128,0,172,255,64,67,128,0,128,192]
    """
    
    matr = np.zeros(np.shape(rojo0))
    matg = np.zeros(np.shape(rojo0))
    matb = np.zeros(np.shape(rojo0))
    for i in range(len(props)):
        matr = matr+(labeled == props[i][1])*rojo[i]
        matg = matg+(labeled == props[i][1])*verde[i]
        matb = matb+(labeled == props[i][1])*azul[i]
    #%%
    r = Image.fromarray(matr).convert('L')
    b = Image.fromarray(matb).convert('L')
    g = Image.fromarray(matg).convert('L')
    im = Image.merge("RGB", (r, g, b))
    #im.show()
    #%%i
    im.save(lugar+'start.png')
    np.save(lugar+'distanciastart',distancias)
    np.save(lugar+'labelstart',labels)
    np.save(lugar+'labels',labels)
    np.save(lugar+'distancias',distancias)
    np.save(lugar+'matr',matr)
    np.save(lugar+'matg',matg)
    np.save(lugar+'matb',matb)
    np.save(lugar+'rojo',rojo)
    np.save(lugar+'verde',verde)
    np.save(lugar+'azul',azul)
    np.save(lugar+'matrstart',matr)
    np.save(lugar+'matgstart',matg)
    np.save(lugar+'matbstart',matb)
    np.save(lugar+'rojostart',rojo)
    np.save(lugar+'verdestart',verde)
    np.save(lugar+'azulstart',azul)
    #np.save('borders',borders)
    np.save(lugar+'fronteras',fronteras)
    np.save(lugar+'centx',centroidx)
    np.save(lugar+'centy',centroidy)
    np.save(lugar+'props',props)
    np.save(lugar+'labeled',labeled)
    np.save(lugar+'counter',[0])