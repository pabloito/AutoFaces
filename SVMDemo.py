from classifier.svm_classifier import svm_classifier_pca


svm_classifier_pca.train()
for name in svm_classifier_pca.person_map.values():
    for i in range(1, 11):
        prediction = svm_classifier_pca.predict_for_image(f'att_faces/Fotos/{name}/{i}.pgm')
        print(f'got {svm_classifier_pca.map_person(prediction[0])}, expected {name}')

score = svm_classifier_pca.score()
print(score)

