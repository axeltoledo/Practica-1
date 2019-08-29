#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:48:17 2019

@author: alumnos
"""
import numpy as np
import matplotlib.pyplot as plt
from Cargar import cargar

#Archivos de datos para las corridas con distintos k
dir_salida1='C:/Users/axel/Desktop/circulacion/practica/practica 1/out_tmp/'
dir_salida2='C:/Users/axel/Desktop/circulacion/practica/practica 1/out_tmp2/'
dir_salida3='C:/Users/axel/Desktop/circulacion/practica/practica 1/out_tmp3/'
# valores de los contornos.

l=4000000 #tamaño de la cuenca 4000km
D=2000 #profundidad en metros
b=0.00000000001 #funcion beta
ro=1025 # densidad
tau=0.3 #esfuerzo del viento
U=((2*(np.pi)*tau)/(ro*D*b*l)) #velocidad U

# Defino las variables
# psi_temp= Funcion corriente para cada t
# vort_temp= vorticidad para cada t
# psiF=funcion corriente final (estacionario)
# vortF=vorticidad final (estacionaria)

# Para EPS=0.29
psi_temp1,vort_temp1,psiF1,vortF1,QG_diag1,QG_curlw1,X1,Y1,dx1,dy1=cargar(dir_salida1,4000,2000,200,100)
# Para EPS=0.75
psi_temp2,vort_temp2,psiF2,vortF2,QG_diag2,QG_curlw2,X2,Y2,dx2,dy2=cargar(dir_salida2,4000,2000,200,100)
# Para EPS=1.16
psi_temp3,vort_temp3,psiF3,vortF3,QG_diag3,QG_curlw3,X3,Y3,dx3,dy3=cargar(dir_salida3,4000,2000,200,100)

# Paso a dimensionar la funcion corriente y la vorticidad para cada corrida.
# Para EPS=0.29
psiF1_dim=psiF1*U*l
vortF1_dim=vortF1*(U/l)
# Para EPS=0.79
psiF2_dim=psiF2*U*l
vortF2_dim=vortF2*(U/l)
# Para EPS=1.29
psiF3_dim=psiF3*U*l
vortF3_dim=vortF3*(U/l)

# Diferencial de la funcion corriente dimensionado
Dif_psiF1_dim=np.diff(psiF1_dim,1,1)
Dif_psiF2_dim=np.diff(psiF2_dim,1,1)
Dif_psiF3_dim=np.diff(psiF3_dim,1,1)

# Defino los transportes meridionales.
M1=Dif_psiF1_dim*D #en long "23" canbia de signo
M2=Dif_psiF2_dim*D # Entre 46 y 49 cambia
M3=Dif_psiF3_dim*D # Entre 60 y 63

#Defino limites de las escalas para facilitar la comparacion
lim_func_corr=np.arange(-560000,80000,80000)
lim_transp=np.arange(-175,50,25)

# Plotear los graficos 
# 1) a) Esquema de energia cinetica en funcion del tiempo
plt.figure(1)
plt.title("Energia Cinetica vs Tiempo")
ax1=plt.subplot()
plt.plot(QG_diag1[:,0],QG_diag1[:,3],label="Energia Cinetica 1")
plt.plot(QG_diag2[:,0],QG_diag2[:,3],label="Energia Cinetica 2")
plt.plot(QG_diag3[:,0],QG_diag3[:,3],label="Energia Cinetica 3")
plt.xlabel("Tiempo")
plt.ylabel("Energia Cinética")
plt.tight_layout()
plt.legend()
plt.savefig('Energia Cinética.png')
plt.close()

# b) Graficos del campo de la funcion corriente y transporte meridional
plt.figure(2, figsize=(10,10))
ax1=plt.subplot(311)
plt.contourf(X1,Y1,psiF1_dim,lim_func_corr, cmap = 'YlGnBu')
plt.colorbar()
plt.title("Campos de función corriente")
ax2=plt.subplot(312)
plt.contourf(X1,Y1,psiF2_dim,lim_func_corr, cmap = 'YlGnBu')
plt.colorbar()
plt.ylabel("latitud (km)")
ax3=plt.subplot(313)
plt.contourf(X1,Y1,psiF3_dim,lim_func_corr, cmap = 'YlGnBu')
plt.xlabel("longitud (km)")
plt.colorbar()
plt.savefig('Campos de función corriente adimensionados.png')
plt.close()

plt.figure(3, figsize=(10,10))
ax1=plt.subplot(311)
plt.contourf(X1[0:199],Y1,M1/1000000,lim_transp, cmap='autumn')
plt.colorbar()
plt.title("Campos de transporte meridional")
ax2=plt.subplot(312)
plt.contourf(X1[0:199],Y1,M2/1000000,lim_transp, cmap='autumn')
plt.ylabel("latitud (km)")
plt.colorbar()
ax3=plt.subplot(313)
plt.contourf(X1[0:199],Y1,M3/1000000,lim_transp, cmap='autumn')
plt.xlabel("longitud (km)")
plt.colorbar()
plt.savefig('Campos de trasnporte meridional.png')
plt.close()

# c) Grafico de corte zonal del transporte meridional en latitud central de la cuenca
plt.figure(4, figsize=(10,10))
plt.title("Corte del transporte meridional zonal")
plt.subplot()
plt.plot(X1[0:199],M1[50,:]/1000000, label="Transporte 1")
plt.plot(X1[0:199],M2[50,:]/1000000, label="Transporte 2")
plt.plot(X1[0:199],M3[50,:]/1000000, label="Transporte 3")
plt.ylabel("Transporte meridional (Sv)")
plt.xlabel("Longitud (km)")
plt.legend()
plt.savefig('Grafico de corte zonal del transporte total.png')
plt.close()
# Grafico de vorticidad vs distancia en la latitud 50
plt.figure(5, figsize=(10,10))
plt.title('Corte de la vorticidad relativa zonal')
plt.subplot()
plt.plot(X1, vortF1_dim[50,:],'r', label='vorticidad relativa 1')
plt.plot(X1,vortF2_dim[50,:], label='vorticidad relativa 2')
plt.plot(X1,vortF3_dim[50,:],'g', label='vorticidad relativa 3')
plt.ylabel('Vorticidad relativa (1/seg)')
plt.xlabel('Longitud (km)')
plt.legend()
plt.savefig('Grafico de corte zonal de la vorticidad.png')
plt.close()
# 2) Transporte de corriente oeste y total
"""
Para cada corrida determine el ancho total por donde pasa la corriente de 
borde oeste a partir del cambio de signo del transporte meridional. Las longitudes
en las cuales cambian de signo los transportes son:
(todos calculados en la latitud central)
Corrida 1: Longitud 23 = X1=[23]= 462.311 Km del borde
Corrida 2: Longiutd 49 = X1=[49]= 984.924 Km del borde
Corrida 3: Longitud 63 = X1=[63]= 1266.331 Km del borde

"""
Trans_CBO_1=np.sum(M1[50,0:23]/1000000)#Transporte de la CBO corrida 1
Trans_CBO_2=np.sum(M2[50,0:49]/1000000)#Transporte de la CBO corrida 2
Trans_CBO_3=np.sum(M3[50,0:63]/1000000)#Transporte de la CBO corrida 3

Trans_Total_1=np.sum(M1[50,:]/1000000)#Transporte de la total corrida 1
Trans_Total_2=np.sum(M2[50,:]/1000000)#Transporte de la total corrida 2
Trans_Total_3=np.sum(M3[50,:]/1000000)#Transporte de la total corrida 3

"""
 Paso a determinar los terminos de la ecuacion del modelo de Stommel
en el caso estacionario, aunque ninguna de las 3 simulaciones me da 0
hay puntos que quedaron afuera ya que las variables no tienen las mismas
dimensiones.
rotor del viento: QG_curlw1 de la simulacion 1, aunque es igual para 
cada corrida ya que lo supusimos estacionario.

"""
# 4) Terminos del balance de la ecuacion de stommel adimencionados, organizados
# por cada corrida

D_Dx_psi=(np.diff(psiF1[1:99,0:199],1,1),np.diff(psiF2[1:99,0:199],1,1),np.diff(psiF3[1:99,0:199],1,1))
rotor_viento= QG_curlw1[1:99,0:198]#Los limites los puse asi para eliminar los 0
vort_rel=(vortF1[1:99,1:199],vortF2[1:99,1:199],vortF3[1:99,1:199])
# Calculo del balance para verificar la validez del mmismo 
# (si este da igual a 0), hicimos la misma cuenta 
# para las otras 2 corridas

Terminos_1= D_Dx_psi[0] - rotor_viento + 0.29*vort_rel[0]
#Terminos_2= D_Dx_psi[1] - rotor_viento + 0.79*vort_rel[1]
#Terminos_3= D_Dx_psi[1] - rotor_viento + 1.29*vort_rel[2]

# Grafico de un corte zonal de cada termino
plt.figure(6, figsize=(10,10))
plt.title('Corte Zonal de los términos del balance de Stommel')
plt.subplot()
plt.plot(X1[0:198],D_Dx_psi[1][50,:],'g', label='diferencial función corriente')
plt.plot(X1, QG_curlw1[50,0:200],'r', label='rotor del viento')
plt.plot(X1, 0.29*vortF1[50,:],'b',label='vorticidad relativa')
plt.ylabel('Valores de los terminos (adim)')
plt.xlabel('Longitud (km)')
plt.legend()
plt.savefig('Grafico del corte zonal de los terminos.png')
plt.close()






