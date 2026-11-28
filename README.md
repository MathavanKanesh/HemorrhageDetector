Findings: 

From DinoV3PCA:
- Lots of overlap between the no hemorrhage and hemorrhage data points, suggesting that hemorrhage is not the main source of variance
- Both hemorrhage and no hemorrhage data points following the same horseshoe shape suggests one dominant underlying pattern shared by both classes rather than many distinct less dominant features 

From CosineSimilarityMatrix: 
Cosine similarity score measures how directionally similar 2 feature vectors for different (or same) classes of images
Applied this to hemorrhage images vs hemorrhage images, non hemorrhage vs non hemorrhage images, and hemorrhage vs non hemorrhage images
Found that: 
- Similarity matrix for no hemorrhage vs no hemorrhage images:
 [[1.         0.9722008  0.9778129  ... 0.991539   0.9914523  0.28266957]
 [0.9722008  0.9999998  0.9486872  ... 0.97531563 0.9827366  0.2915393 ]
 [0.9778129  0.9486872  0.99999976 ... 0.9777437  0.9729561  0.28740042]
 ...
 [0.991539   0.97531563 0.9777437  ... 0.9999999  0.988142   0.2624076 ]
 [0.9914523  0.9827366  0.9729561  ... 0.988142   1.0000002  0.26886177]
 [0.28266957 0.2915393  0.28740042 ... 0.2624076  0.26886177 0.9999998 ]]
Average similarity: 0.595368 --> suggests not very similar features overall despite all having no hemorrhage

- Similarity matrix for hemorrhage vs hemorrhage images:
 [[1.0000004  0.7810053  0.6877755  ... 0.6223943  0.69660807 0.6688279 ]
 [0.7810053  0.99999934 0.48986098 ... 0.8159708  0.81749755 0.43171096]
 [0.6877755  0.48986098 0.99999946 ... 0.455988   0.44674256 0.8547217 ]
 ...
 [0.6223943  0.8159708  0.455988   ... 1.0000004  0.8682745  0.34006315]
 [0.69660807 0.81749755 0.44674256 ... 0.8682745  1.0000002  0.3345424 ]
 [0.6688279  0.43171096 0.8547217  ... 0.34006315 0.3345424  0.99999994]]
Average Similarity: 0.6862356 --> Hemorrhage images demonstrated higher average feature similarity than non hemorrhage images. 

- Similarity matrix for no hemorrhage vs hemorrhage images:
[[0.5951803  0.3850598  0.7845176  ... 0.29127187 0.29173893 0.9293016 ]
 [0.5999316  0.406776   0.7728988  ... 0.3092819  0.30917233 0.8837026 ]
 [0.6082857  0.38407844 0.7877456  ... 0.28666192 0.29160702 0.9497515 ]
 ...
 [0.58319783 0.37591517 0.7672317  ... 0.28137606 0.28318307 0.9271998 ]
 [0.58409244 0.37683147 0.7659938  ... 0.2805596  0.28328034 0.9073928 ]
 [0.7688476  0.8915938  0.448966   ... 0.82234544 0.83426404 0.34722152]]
Average Similarity: 0.6306955 --> Relatively high cross class similarity. Odd that it is higher than non hemorrhage vs non hemorrhage images despite being across 2 different classes

Overall: From DinoV3PCA and CosineSimilarity: Dino's baseline is unable to extract meaningful patterns/features across hemorrhage and non hemorrhage images, or even same class images. 

Another check: 
Taking the feature average of each class (hemorrhage = 1 and hemorrhage = 0)
Came up with two matrices FeatureAverage0 and FeatureAverage1, where FeatureAverage0 is a 384 feature matrix that is the average of 856 non hemorrhage image features and FeatureAverage1 is a 384 feature matrix that is the average of 144 hemorrhage image features 
--> Applying cosine similarity to these 2 matrices gave a similarity score of 0.986. 
Limitation: Can't say much about this result. When averaging all feature vectors into one, it eliminates affect of individual images that might still contain useful differences 


