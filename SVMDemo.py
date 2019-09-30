from classifier.svm_classifier import SVMClassifierPCA

classifier = SVMClassifierPCA(
    path_to_folders='att_faces/orl_faces/',
    image_height=112,
    image_width=92,
    number_of_people=40,
    training_figures_per_person=6,
    testing_figures_per_person=4,
    total_figures_per_person=10
)

classifier.plot_mean_image()

