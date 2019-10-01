from classifier.svm_classifier import SVMClassifierPCA

classifier = SVMClassifierPCA(
    path_to_folders='att_faces/Fotos/',
    image_height=160,
    image_width=120,
    number_of_people=5,
    training_figures_per_person=9,
    total_figures_per_person=10
)

classifier.plot_mean_image()
for i in range(0,classifier.number_of_eigenvectors):
    classifier.plot_nth_eigenface(i)
classifier.plot_score_vs_eigen_number()

