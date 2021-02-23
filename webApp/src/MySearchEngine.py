import ImageRetrieval as IR
import logging
from scipy.spatial import distance

def searchByImage(imagePath):
    imageClasses = IR.predictImageCategory(imagePath)
    
    imageFeature = IR.extractImageFeature(imagePath)
    imgClassesFeature = []
    imgClassesFeature = IR.loadFeaturesByImgClasses(imageClasses)

    if not imgClassesFeature:
        print('No matching images found!')

    imgClassesFeature.sort(key=lambda feaVec: distance.cosine(feaVec[1], imageFeature))
    if len(imgClassesFeature) > 20:
        return imgClassesFeature[:20]

    return imgClassesFeature
