# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 16:32:14 2017

@author: pfierens
"""
from os import listdir
from os.path import join, isdir
import numpy as np
import matplotlib.pyplot as plt
import eigencalculator as ec
import util
from sklearn import svm

mypath      = 'att_faces/orl_faces/'
onlydirs    = [f for f in listdir(mypath) if isdir(join(mypath, f))]

#image size
horsize     = 92
versize     = 112
areasize    = horsize*versize

#number of figures
personno    = 40
trnperper   = 6
tstperper   = 4
trnno       = personno*trnperper
tstno       = personno*tstperper

#TRAINING SET
images = np.zeros([trnno,areasize])
person = np.zeros([trnno,1])
imno = 0
per  = 0
for dire in onlydirs:
    for k in range(1,trnperper+1):
        a = plt.imread(mypath + dire + '/{}'.format(k) + '.pgm')/255.0
        images[imno,:] = np.reshape(a,[1,areasize])
        person[imno,0] = per
        imno += 1
    per += 1

#TEST SET
imagetst  = np.zeros([tstno,areasize])
persontst = np.zeros([tstno,1])
imno = 0
per  = 0
for dire in onlydirs:
    for k in range(trnperper,10):
        a = plt.imread(mypath + dire + '/{}'.format(k) + '.pgm')/255.0
        imagetst[imno,:]  = np.reshape(a,[1,areasize])
        persontst[imno,0] = per
        imno += 1
    per += 1


    
#CARA MEDIA
meanimage = np.mean(images,0)
fig, axes = plt.subplots(1,1)
axes.imshow(np.reshape(meanimage,[versize,horsize])*255,cmap='gray')
fig.suptitle('Imagen media')
plt.show()

#resto la media
images  = [images[k,:]-meanimage for k in range(images.shape[0])]
imagetst= [imagetst[k,:]-meanimage for k in range(imagetst.shape[0])]

#PCA
c = util.getSmallestDimensionC(images)
eigen_vec,eigen_val = ec.eigen_calc(c)

autofaces = util.getAllAutoFaces(eigen_vec,images)

#Primera autocara...
eigen1 = (np.reshape(autofaces[:,0],[versize,horsize]))*255
fig, axes = plt.subplots(1,1)
axes.imshow(eigen1,cmap='gray')
fig.suptitle('Primera autocara')
plt.show()

eigen2 = (np.reshape(autofaces[:,1],[versize,horsize]))*255
fig, axes = plt.subplots(1,1)
axes.imshow(eigen2,cmap='gray')
fig.suptitle('Segunda autocara')
plt.show()

eigen3 = (np.reshape(autofaces[:,2],[versize,horsize]))*255
fig, axes = plt.subplots(1,1)
axes.imshow(eigen3,cmap='gray')
fig.suptitle('Tercera autocara')
plt.show()


nmax = autofaces.shape[1]
accs = np.zeros([nmax,1])
for neigen in range(1,nmax):
    #Me quedo sólo con las primeras autocaras
    B = autofaces[:,0:neigen]
    #proyecto
    improy      = np.dot(images,B)
    imtstproy   = np.dot(imagetst,B)
        
    #SVM
    #entreno
    clf = svm.LinearSVC()
    clf.fit(improy,person.ravel())
    accs[neigen] = clf.score(imtstproy,persontst.ravel())
    print('Precisión con {0} autocaras: {1} %\n'.format(neigen,accs[neigen]*100))

fig, axes = plt.subplots(1,1)
axes.semilogy(range(nmax),(1-accs)*100)
axes.set_xlabel('No. autocaras')
axes.grid(which='Both')
fig.suptitle('Error')
plt.show()
