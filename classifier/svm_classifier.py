from abc import ABC, abstractmethod
from os import listdir
from os.path import join, isdir

import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

import eigencalculator as ec


class SVMClassifier(ABC):

    def __init__(self, path_to_folders, image_height, image_width, number_of_people, testing_figures_per_person,
                 total_figures_per_person):
        # Initialize classifier variables
        self.path_to_folders = path_to_folders
        self.image_height = image_height
        self.image_width = image_width
        self.image_area = image_height * image_width
        self.number_of_people = number_of_people
        self.testing_figures_per_person = testing_figures_per_person
        self.testing_figures_total = testing_figures_per_person * number_of_people
        self.training_figures_per_person = total_figures_per_person - testing_figures_per_person
        self.training_figures_total = self.training_figures_per_person * number_of_people
        self.total_figures_per_person = total_figures_per_person
        self.number_of_eigenvectors = self.training_figures_per_person * number_of_people
        self.autofaces = None  # Will be set by PCA
        self.training_persons = None
        self.testing_persons = None
        self.training_images = None
        self.testing_images = None
        self.clf = None
        self.person_map = {}

    def plot_nth_eigenface(self, n):
        eigen1 = (np.reshape(self.autofaces[n, :], [self.image_height, self.image_width])) * 255
        fig, axes = plt.subplots(1, 1)
        axes.imshow(eigen1, cmap='gray')
        fig.suptitle('Autocara #' + str(n))
        plt.show()

    def train(self, amount_of_eigenvectors):
        training_images_projection = self._get_training_images_projection(amount_of_eigenvectors)
        self.clf = svm.LinearSVC()
        self.clf.fit(training_images_projection, self.training_persons.ravel())

    def score(self):
        testing_images_projection = self._get_testing_images_projection()
        return self.clf.score(testing_images_projection, self.testing_persons.ravel())

    def predict_for_image(self, path_to_image, amount_of_eigenvectors):
        image_array = self.build_image_array(path_to_image)
        proyected_image = self.get_image_projection(image_array, amount_of_eigenvectors)
        # proyected_image = np.flip(proyected_image, 1)
        prediction = self.clf.predict(proyected_image)
        return prediction

    def map_person(self, number):
        return self.person_map.get(number)

    @abstractmethod
    def get_image_projection(self, image_array, amount_of_eigenvectors):
        return NotImplementedError

    @abstractmethod
    def build_image_array(self, path_to_image):
        return NotImplementedError

    @abstractmethod
    def _get_testing_images_projection(self):
        return NotImplementedError

    @abstractmethod
    def _get_training_images_projection(self, amount_of_eigenvectors):
        return NotImplementedError


class SVMClassifierPCA(SVMClassifier):
    def __init__(self, path_to_folders, image_height, image_width, number_of_people,
                 training_figures_per_person, total_figures_per_person):

        super().__init__(path_to_folders, image_height, image_width, number_of_people,
                         training_figures_per_person, total_figures_per_person)

        # Build training set
        self.training_images = np.zeros([self.training_figures_total, self.image_area])
        self.training_persons = np.zeros([self.training_figures_total, 1])
        image_number = 0
        person = 0
        directories = [f for f in listdir(self.path_to_folders) if isdir(join(self.path_to_folders, f))]
        for dire in directories:
            self.person_map.update({person: dire})
            if image_number >= self.training_figures_total:
                break
            for k in range(1, self.training_figures_per_person + 1):  # todo: creo que es sin el +1
                a = plt.imread(self.path_to_folders + dire + '/{}'.format(k) + '.pgm') / 255.0
                self.training_images[image_number, :] = np.reshape(a, [1, self.image_area])
                self.training_persons[image_number, 0] = person
                image_number += 1
            person += 1

        # Build testing set
        self.testing_images = np.zeros([self.testing_figures_total, self.image_area])
        self.testing_persons = np.zeros([self.testing_figures_total, 1])
        image_number = 0
        person = 0
        for dire in directories:
            self.person_map.update({person: dire})
            if image_number >= self.testing_figures_total:
                break
            for k in range(self.training_figures_per_person, 10):  # todo: creo que aca si es con el +1
                a = plt.imread(self.path_to_folders + dire + '/{}'.format(k) + '.pgm') / 255.0
                self.testing_images[image_number, :] = np.reshape(a, [1, self.image_area])
                self.testing_persons[image_number, 0] = person
                image_number += 1
            person += 1

        # Build the mean face of the database
        self.mean_image = np.mean(self.training_images, 0)

        # Standardize the sample (subtract the mean)
        self.training_images = [self.training_images[k, :] - self.mean_image for k in
                                range(self.training_images.shape[0])]
        self.testing_images = [self.testing_images[k, :] - self.mean_image for k in
                               range(self.testing_images.shape[0])]

        # Do PCA analysis and store autofaces
        images2 = np.asarray(self.training_images)
        # Calculate the covariance matrices for the training images
        C = images2.dot(images2.transpose())
        # Eigenvalues eigenvectors de C (La de menor dimension)
        L, VM = ec.eigen_calc(C)
        # Calcular las autocaras como en el Paper de Turk (pag 75)
        VM = np.dot(VM.transpose(), images2)
        for i in range(0, VM.shape[0]):
            VM[i, :] = VM[i, :] / np.linalg.norm(VM[i, :])
        self.autofaces = VM

    def _get_training_images_projection(self, amount_of_eigenvectors):
        B = self.autofaces[0:amount_of_eigenvectors, :]
        return np.dot(self.training_images, B.T)

    def _get_testing_images_projection(self):
        B = self.autofaces[0:self.number_of_eigenvectors, :]
        return np.dot(self.testing_images, B.T)

    def build_image_array(self, path_to_image):
        array = np.zeros([1, self.image_area])
        a = plt.imread(path_to_image) / 255.0
        array[0, :] = np.reshape(a, [1, self.image_area])
        array[0, :] = array[0, :] - self.mean_image
        return array

    def get_image_projection(self, image_array, amount_of_eigenvectors):
        B = self.autofaces[0:amount_of_eigenvectors, :]
        # proyecto
        return np.dot(image_array, B.T)

    def plot_mean_image(self):
        fig, axes = plt.subplots(1, 1)
        axes.imshow(np.reshape(self.mean_image, [self.image_height, self.image_width]) * 255, cmap='gray')
        fig.suptitle('Imagen media')
        plt.show()


class SVMClassifierKPCA(SVMClassifier):

    def __init__(self, path_to_folders, image_height, image_width, number_of_people, training_figures_per_person,
                 total_figures_per_person, kernel_degree):
        super().__init__(path_to_folders, image_height, image_width, number_of_people, training_figures_per_person,
                         total_figures_per_person)

        self.kernel_degree = kernel_degree

        # Build training set
        self.training_images = np.zeros([self.training_figures_total, self.image_area])
        self.training_persons = np.zeros([self.training_figures_total, 1])
        image_number = 0
        person = 0
        directories = [f for f in listdir(self.path_to_folders) if isdir(join(self.path_to_folders, f))]
        for dire in directories:
            self.person_map.update({person: dire})
            if image_number >= self.training_figures_total:
                break
            for k in range(1, self.training_figures_per_person + 1):  # todo: creo que es sin el +1
                a = plt.imread(self.path_to_folders + dire + '/{}'.format(k) + '.pgm')
                self.training_images[image_number, :] = (np.reshape(a, [1, self.image_area]) - 127.5) / 127.5
                self.training_persons[image_number, 0] = person
                image_number += 1
            person += 1

        # Build testing set
        self.testing_images = np.zeros([self.testing_figures_total, self.image_area])
        self.testing_persons = np.zeros([self.testing_figures_total, 1])
        image_number = 0
        person = 0
        for dire in directories:
            self.person_map.update({person: dire})
            if image_number >= self.testing_figures_total:
                break
            for k in range(self.training_figures_per_person, 10):  # todo: creo que aca si es con el +1
                a = plt.imread(self.path_to_folders + dire + '/{}'.format(k) + '.pgm')
                self.testing_images[image_number, :] = (np.reshape(a, [1, self.image_area]) - 127.5) / 127.5
                self.testing_persons[image_number, 0] = person
                image_number += 1
            person += 1

        # Do KPCA
        K = (np.dot(self.training_images,
                    self.training_images.T) / self.training_figures_total + 1) ** self.kernel_degree
        # K = (K + K.T)/2.0

        # esta transformación es equivalente a centrar las imágenes originales...
        unoM = np.ones([self.training_figures_total, self.training_figures_total]) / self.training_figures_total
        K = K - np.dot(unoM, K) - np.dot(K, unoM) + np.dot(unoM, np.dot(K, unoM))

        # Autovalores y autovectores
        w, alpha = ec.eigen_calc(K, 0.01)
        tst = np.dot(alpha, alpha.transpose())
        W, A = np.linalg.eigh(K)
        TST = np.dot(A, A.transpose())
        lambdas = w / self.training_figures_total
        lambdas = w

        # Los autovalores vienen en orden descendente. Lo cambio
        # lambdas = np.flipud(lambdas)
        # alpha   = np.fliplr(alpha)

        for col in range(alpha.shape[1]):
            alpha[:, col] = alpha[:, col] / np.sqrt(lambdas[col])
        self.K = K
        self.alpha = alpha
        self.unoM = unoM
        # pre-proyección
        self.training_images_preprojection = np.dot(K.T, alpha)
        unoML = np.ones([self.testing_figures_total, self.training_figures_total]) / self.training_figures_total
        Ktest = (np.dot(self.testing_images,
                        self.training_images.T) / self.training_figures_total + 1) ** self.kernel_degree
        Ktest = Ktest - np.dot(unoML, K) - np.dot(Ktest, unoM) + np.dot(unoML, np.dot(K, unoM))
        self.testing_images_preprojection = np.dot(Ktest, alpha)

    def get_image_projection(self, image_array, amount_of_eigenvectors):
        # preproyeccion de a
        unoML = np.ones([1, self.training_figures_total]) / self.training_figures_total
        Ktestimage = (np.dot(image_array,
                             self.training_images.T) / self.training_figures_total + 1) ** self.kernel_degree
        # Normalizo (esta en el paper de kpca for face recognition)
        Ktestimage = Ktestimage - np.dot(unoML, self.K) - np.dot(Ktestimage, self.unoM) + np.dot(unoML,
                                                                                            np.dot(self.K, self.unoM))
        aproypre = np.dot(Ktestimage, self.alpha)
        # proyeccion de a
        aproy = aproypre[:, 0: amount_of_eigenvectors]
        return aproy

    def build_image_array(self, path_to_image):
        a = plt.imread(path_to_image)
        return (np.reshape(a, [1, self.image_area]) - 127.5) / 127.5

    def _get_testing_images_projection(self):
        return self.testing_images_preprojection[:, 0:self.number_of_eigenvectors]

    def _get_training_images_projection(self, amount_of_eigenvectors):
        return self.training_images_preprojection[:, 0:amount_of_eigenvectors]


svm_classifier_pca = SVMClassifierPCA(
    path_to_folders='/home/francisco/itba/mna/tps/AutoFaces/att_faces/Fotos/',
    image_height=160,
    image_width=120,
    number_of_people=5,
    training_figures_per_person=6,
    total_figures_per_person=10,
)

svm_classifier_kpca = SVMClassifierKPCA(
    path_to_folders='/home/francisco/itba/mna/tps/AutoFaces/att_faces/Fotos/',
    image_height=160,
    image_width=120,
    number_of_people=5,
    training_figures_per_person=6,
    total_figures_per_person=10,
    kernel_degree=2
)
