# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 16:32:14 2017

@author: pfierens
"""
from os import listdir
from os.path import join, isdir
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import eigencalculator as ec

mypath      = 'att_faces/Fotos/'
onlydirs    = [f for f in listdir(mypath) if isdir(join(mypath, f))]

#image size
horsize     = 120
versize     = 160
areasize    = horsize*versize

#number of figures
personno    = 5
trnperper   = 6
tstperper   = 4
trnno       = personno*trnperper
tstno       = personno*tstperper

#TRAINING SET
images = np.zeros([trnno,areasize])
person = np.zeros([trnno,1])
imno = 0
per  = 0
trainingnames = {}
for dire in onlydirs:
    for k in range(1,trnperper+1):
        tstimage = plt.imread(mypath + dire + '/{}'.format(k) + '.pgm')
        images[imno,:] = (np.reshape(tstimage, [1, areasize]) - 127.5) / 127.5
        person[imno,0] = per
        imno += 1
    trainingnames[per] = dire
    per += 1

#TEST SET
imagetst  = np.zeros([tstno,areasize])
persontst = np.zeros([tstno,1])
imno = 0
per  = 0
for dire in onlydirs:
    for k in range(trnperper,10):
        tstimage = plt.imread(mypath + dire + '/{}'.format(k) + '.pgm')
        imagetst[imno,:]  = (np.reshape(tstimage, [1, areasize]) - 127.5) / 127.5
        persontst[imno,0] = per
        imno += 1
    per += 1

#KERNEL: polinomial de grado degree
degree = 2
K = (np.dot(images,images.T)/trnno+1)**degree
#K = (K + K.T)/2.0
        
#esta transformación es equivalente a centrar las imágenes originales...
unoM = np.ones([trnno,trnno])/trnno
K = K - np.dot(unoM,K) - np.dot(K,unoM) + np.dot(unoM,np.dot(K,unoM))


#Autovalores y autovectores
#w,alpha = ec.eigen_calc(K)
w,alpha = ec.eigen_calc(K, 0.01)
tst = np.dot(alpha, alpha.transpose())
W, A = np.linalg.eigh(K)
TST = np.dot(A, A.transpose())
lambdas = w/trnno
lambdas = w

#Los autovalores vienen en orden descendente. Lo cambio 
#lambdas = np.flipud(lambdas)
#alpha   = np.fliplr(alpha)

for col in range(alpha.shape[1]):
    alpha[:,col] = alpha[:,col]/np.sqrt(lambdas[col])

#pre-proyección
improypre   = np.dot(K.T,alpha)
unoML       = np.ones([tstno,trnno])/trnno
Ktest       = (np.dot(imagetst,images.T)/trnno+1)**degree
Ktest       = Ktest - np.dot(unoML,K) - np.dot(Ktest,unoM) + np.dot(unoML,np.dot(K,unoM))
imtstproypre= np.dot(Ktest,alpha)

#from sklearn.decomposition import KernelPCA

#kpca = KernelPCA(n_components = None, kernel='poly', degree=2, gamma = 1, coef0 = 0)
#kpca = KernelPCA(n_components = None, kernel='poly', degree=2)
#kpca.fit(images)

#improypre = kpca.transform(images)
#imtstproypre = kpca.transform(imagetst)

nmax = 30
accs = np.zeros([nmax,1])
clf = svm.LinearSVC()
for neigen in range(1,nmax):
    #Me quedo sólo con las primeras autocaras   
    #proyecto
    improy      = improypre[:,0:neigen]
    imtstproy   = imtstproypre[:,0:neigen]
        
    #SVM
    #entreno

    clf.fit(improy,person.ravel())
    accs[neigen] = clf.score(imtstproy,persontst.ravel())
    print('Precisión con {0} autocaras: {1} %\n'.format(neigen,accs[neigen]*100))

x=range(1,nmax+1)
y=(1-accs)*100

plt.plot(x, y, 'go--', linewidth=2, markersize=12)
plt.xlabel('Autocaras')
plt.ylabel('Error')
plt.title('KPCA')
plt.xticks(np.arange(0, nmax+0.001, step=nmax/10))
plt.yticks(np.arange(0, 100+0.001, step=10))
plt.grid(color='black', linestyle='-', linewidth=0.2)
plt.show()

# fig, axes = plt.subplots(1,1)
# axes.semilogy(range(nmax),)
# axes.set_xlabel('No. autocaras')
# axes.grid(which='Both')
# fig.suptitle('Error')
plt.show()

