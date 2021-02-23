import numpy as np
import os
from platform import platform
from glob import iglob

from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import  GlobalAveragePooling2D, Lambda
from tensorflow.keras.backend import l2_normalize
from tensorflow.keras.models import Model

# Use InceptionResNetV2 pre-trained model to classify the input image
classifier = InceptionResNetV2(include_top=True, weights='imagenet')

# For feature extraction, using the InceptionResNetV2 without the fully connected output layers
baseModel = InceptionResNetV2(include_top=False, weights='imagenet')

# Adding the GlobalAveragePooling layer after base model, it's used to reduce the dimentionality of the output
globalPoolingLayer = GlobalAveragePooling2D()(baseModel.output)

# Normalize the result of the GlobalPoolingLayer
normLambda = Lambda(lambda  x: l2_normalize(x,axis=1))(globalPoolingLayer)

# The input is the normal InceptionResNetV2 input of (n, 299, 299, 3) and the output is the normalised features of the norm layer
featureExtractor = Model(inputs=[baseModel.input], outputs=[normLambda])
featureExtractor.compile(optimizer='rmsprop', loss='mse')

# Load and pre-process the input image before inputing to the classifer
def loadAndProcessImage(imgPath):
    img = image.load_img(imgPath, target_size=(299, 299))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    
    return preprocess_input(img)

def predictImageCategory(imgPath):
    img = loadAndProcessImage(imgPath)

    predictResults = classifier.predict(img)
    decodedPredictResults = decode_predictions(predictResults)[0]

    return [decodedPredictResults[i][1] for i in range(0, len(decodedPredictResults))]

def extractImageFeature(imgPath):
    img = loadAndProcessImage(imgPath)
    feaVec = featureExtractor.predict(img)

    return feaVec.flatten()

def loadFeaturesByImgClasses(imgClasses):
    features = []
    for imgClass in imgClasses:
        featureFilePath = os.path.join('database/feature_by_category', imgClass + '.npz')
        if os.path.isfile(featureFilePath):
            print('Feature file path:', featureFilePath)
            loadedFeatureVectors = np.load(featureFilePath, allow_pickle=True)
            loadedFeatureVectors = list(loadedFeatureVectors['arr_0'])

            for vector in loadedFeatureVectors:
                if path2Name(vector[0]) in (path2Name(feature[0]) for feature in features):
                    continue
                features.append(vector)

    return features

def path2Name(img_path):
    return img_path.split('/')[-1]
