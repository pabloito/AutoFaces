from classifier.svm_classifier import svm_classifier_pca, svm_classifier_kpca


# svm_classifier_pca.train()
# hits = 0
# total = 0
# for name in svm_classifier_pca.person_map.values():
#     for i in range(1, 11):
#         prediction = svm_classifier_pca.predict_for_image(f'/home/francisco/itba/mna/tps/AutoFaces/att_faces/Fotos/pablo/4.pgm')
#         if svm_classifier_pca.map_person(prediction[0]) == name:
#             hits += 1
#         total += 1


svm_classifier_kpca.train(10)
print(f'kpca precition {svm_classifier_kpca.score()}')
hits = 0
total = 0
for name in svm_classifier_kpca.person_map.values():
    for i in range(1, 11):
        prediction = svm_classifier_kpca.predict_for_image(f'/home/francisco/itba/mna/tps/AutoFaces/att_faces/Fotos/{name}/{i}.pgm', 10)
        if svm_classifier_kpca.map_person(prediction[0]) == name:
            hits += 1
        total += 1

print(f'hits over total: {hits/total}')
