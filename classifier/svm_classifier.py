from abc import ABC, abstractmethod
from os import listdir
from os.path import join, isdir

import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

import eigencalculator as ec


class SVMClassifier(ABC):

    def __init__(self, path_to_folders, image_height, image_width, number_of_people, testing_figures_per_person,
                 training_figures_per_person, total_figures_per_person, number_of_eigenvectors):

        # Initialize classifier variables
        self.path_to_folders = path_to_folders
        self.image_height = image_height
        self.image_width = image_width
        self.image_area = image_height * image_width
        self.number_of_people = number_of_people
        self.testing_figures_per_person = testing_figures_per_person
        self.testing_figures_total = testing_figures_per_person * number_of_people
        self.training_figures_per_person = training_figures_per_person
        self.training_figures_total = training_figures_per_person * number_of_people
        self.total_figures_per_person = total_figures_per_person
        self.number_of_eigenvectors = number_of_eigenvectors
        self.autofaces = None  # Will be set by PCA
        self.training_persons = None
        self.testing_persons = None
        self.training_images = None
        self.testing_images = None
        self.clf = None

    def plot_first_eigenface(self):
        eigen1 = (np.reshape(self.autofaces[0, :], [self.image_height, self.image_width])) * 255
        fig, axes = plt.subplots(1, 1)
        axes.imshow(eigen1, cmap='gray')
        fig.suptitle('Primera autocara')
        plt.show()

    def train_for_eigen_number(self, neigen):
        training_images_projection = self._get_training_images_projection(neigen)
        self.number_of_eigenvectors = neigen
        self.clf = svm.LinearSVC()
        self.clf.fit(training_images_projection, self.training_persons.ravel())

    def score(self):
        testing_images_projection = self._get_testing_images_projection()
        return self.clf.score(testing_images_projection, self.testing_persons.ravel())

    def plot_score_vs_eigen_number(self):
        nmax = self.autofaces.shape[1]
        accs = np.zeros([nmax, 1])
        for neigen in range(1, nmax):
            self.train_for_eigen_number(neigen)
            accs[neigen] = self.score()
            print('Precisión con {0} autocaras: {1} %\n'.format(neigen, accs[neigen] * 100))

        fig, axes = plt.subplots(1, 1)
        axes.semilogy(range(nmax), (1 - accs) * 100)
        axes.set_xlabel('No. autocaras')
        axes.grid(which='Both')
        fig.suptitle('Error')
        plt.show()

    def predict_for_image(self, path_to_image):
        image_array = self.build_image_array(path_to_image)
        proyected_image = self.get_image_projection(image_array)
        return self.clf.predict(proyected_image)

    @abstractmethod
    def get_image_projection(self, image_array):
        return NotImplementedError

    @abstractmethod
    def build_image_array(self, path_to_image):
        return NotImplementedError

    @abstractmethod
    def _get_testing_images_projection(self, neigen=None):
        return NotImplementedError

    @abstractmethod
    def _get_training_images_projection(self, neigen=None):
        return NotImplementedError


class SVMClassifierPCA(SVMClassifier):
    def __init__(self, path_to_folders, image_height, image_width, number_of_people, testing_figures_per_person,
                 training_figures_per_person, total_figures_per_person, number_of_eigenvectors):

        super().__init__(path_to_folders, image_height, image_width, number_of_people, testing_figures_per_person,
                         training_figures_per_person, total_figures_per_person, number_of_eigenvectors)

        # Build training set
        self.training_images = np.zeros([self.training_figures_total, self.image_area])
        self.training_persons = np.zeros([self.training_figures_total, 1])
        image_number = 0
        person = 0
        directories = [f for f in listdir(self.path_to_folders) if isdir(join(self.path_to_folders, f))]
        for dire in directories:
            if image_number >= self.training_figures_total:
                break
            for k in range(1, self.training_figures_per_person + 1):
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
            if image_number >= self.testing_figures_total:
                break
            for k in range(self.training_figures_per_person, 10):
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

    def _get_training_images_projection(self, neigen=None):
        if not neigen:
            neigen = self.number_of_eigenvectors
        B = self.autofaces[0:neigen, :]
        return np.dot(self.training_images, B.T)

    def _get_testing_images_projection(self, neigen=None):
        if not neigen:
            neigen = self.number_of_eigenvectors
        B = self.autofaces[0:neigen, :]
        return np.dot(self.testing_images, B.T)

    def build_image_array(self, path_to_image):
        array = np.zeros([self.image_area])
        a = plt.imread(path_to_image) / 255.0
        array[:] = np.reshape(a, [1, self.image_area])
        return array

    def get_image_projection(self, image_array):
        B = self.autofaces[0:self.number_of_eigenvectors, :]
        # proyecto
        return np.dot(image_array, B.T)

    def plot_mean_image(self):
        fig, axes = plt.subplots(1, 1)
        axes.imshow(np.reshape(self.mean_image, [self.image_height, self.image_width]) * 255, cmap='gray')
        fig.suptitle('Imagen media')
        plt.show()


class SVMClassifierKPCA(SVMClassifier):

    def build_training_and_testing_sets(self):
        pass

    def get_images_projection(self, neigen=None):
        if not neigen:
            neigen = self.number_of_eigenvectors

        return (
            self.training_images_preprojection[:, 0:neigen],
            self.testing_images_preprojection[:, 0:neigen]
                )

    def __init__(self, path_to_folders, image_height, image_width, number_of_people, testing_figures_per_person,
                 training_figures_per_person, total_figures_per_person, kernel_degree, number_of_eigenvectors):
        super().__init__(path_to_folders, image_height, image_width, number_of_people, testing_figures_per_person,
                         training_figures_per_person, total_figures_per_person, number_of_eigenvectors)
        self.kernel_degree = kernel_degree

    def principal_component_analysis(self):
        K = (np.dot(self.training_images,
                    self.training_images.T) / self.training_figures_total + 1) ** self.kernel_degree
        # K = (K + K.T)/2.0

        # esta transformación es equivalente a centrar las imágenes originales...
        unoM = np.ones([self.training_figures_total, self.training_figures_total]) / self.training_figures_total
        K = K - np.dot(unoM, K) - np.dot(K, unoM) + np.dot(unoM, np.dot(K, unoM))

        # Autovalores y autovectores
        w, alpha = ec.eigen_calc(K)
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

        # pre-proyección
        self.training_images_preprojection = np.dot(K.T, alpha)
        unoML = np.ones([self.testing_figures_total, self.training_figures_total]) / self.training_figures_total
        Ktest = (np.dot(self.testing_images,
                        self.training_images.T) / self.training_figures_total + 1) ** self.kernel_degree
        Ktest = Ktest - np.dot(unoML, K) - np.dot(Ktest, unoM) + np.dot(unoML, np.dot(K, unoM))
        self.testing_images_preprojection = np.dot(Ktest, alpha)
