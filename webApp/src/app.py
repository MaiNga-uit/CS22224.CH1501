# import the Flask class from the flask module
from flask import Flask, render_template, send_from_directory, request, json, jsonify, make_response, send_file
import io
import os
import logging
import cv2
import mimetypes
import numpy as np
import MySearchEngine as searcher
import ImageRetrieval as IR

# create the application object
app = Flask(__name__,
            static_url_path='', 
            static_folder='web',
            template_folder='web/template')

datasetDir = 'web/dataset'

# use decorators to link the function to a url
@app.route('/')
def home():
    return app.send_static_file('index.html')  # render a template

@app.route('/dataset/<string:imageId>')
def getImage(imageId):

    # /dataset/demo.jpg?x1=41&y1=61&x2=81&y2=61&size=160&thickness=1
    # Check query param to draw rect
    x1 = request.args.get("x1", 0, type=int)
    y1 = request.args.get("y1", 0, type=int)
    x2 = request.args.get("x2", 0, type=int)
    y2 = request.args.get("y2", 0, type=int)
    size = request.args.get("size", 0, type=int)
    thickness = request.args.get("thickness", 4, type=int)

    if x1 > 0 and y1 > 0 and \
        x2 > 0 and y2 > 0:

        logging.info("Get image: %s", f'x1={x1}&y1={y1}&x2={x2}&y2={y2}')
        imagePath = os.path.join(datasetDir, imageId)
        if os.path.isfile(imagePath):
            img = cv2.imread(imagePath)
            # img = image.load_img(imagePath, target_size=(450, 600))

            # Start coordinate
            startPoint = (x1, y1)
            # End coordinate
            endPoint = (x2, y2)

            # Yellow color in BGR 
            color = (0, 0, 255)

            # Draw a rectangle
            img = cv2.rectangle(img, startPoint, endPoint, color, thickness)
            
            # Get mime type and encode image
            contentType, _ = mimetypes.guess_type(imageId)
            _, imgEncoded = cv2.imencode('.jpg', img)

            # return image with rect
            return send_file(
                    io.BytesIO(imgEncoded),
                    attachment_filename = imageId,
                    mimetype = contentType)

    # return original image
    return send_from_directory(datasetDir, imageId)

@app.route('/api/datasets', methods=['GET'])
def listDataset():
    page = request.args.get('page', 0, type=int)
    if page <= 0:
        page = 1

    pageSize = 20  # define page size
    indexFrom = pageSize * (page - 1)
    indexTo = pageSize * page

    response = {
        'data': [],
        'hasNext': 0,
        'total': 0,
        'page': page,
        'indexFrom': indexFrom + 1, # Display begin from 1
        'indexTo': indexTo
    }

    dirs = os.listdir(datasetDir)
    response['total'] = len(dirs)
    
    if indexTo > len(dirs):
        response['indexTo'] = len(dirs)

    for count, filename in enumerate(dirs):
        if not os.path.isfile(os.path.join(datasetDir, filename)):
            continue

        if count <= indexFrom:
            continue
        if count > indexTo:
            response['hasNext'] = 1
            break

        response['data'].append(filename)
    
    json_data = json.dumps(response)
    # logging.info("Response = %s", json_data)
    return jsonify(response)
        

@app.route('/api/dosearch', methods=['GET'])
def doSearch():
    # id=oxc1_06_000427&x1=159&y1=357&x2=312&y2=368&width_on_page=600&height_on_page=450&use_qe=false
    imageId = request.args.get('id', '', type=str)
    x1 = request.args.get('x1', 0, type=int)
    y1 = request.args.get('y1', 0, type=int)
    x2 = request.args.get('x2', 0, type=int)
    y2 = request.args.get('y2', 0, type=int)
    widthOnPage = request.args.get('width_on_page', 0, type=int)
    heightOnPage = request.args.get('height_on_page', 0, type=int)
    
    queryByRegion = False
    if x1 > 0 and x2 > 0 and y1 > 0 and y2 > 0:
        queryByRegion = True

    searchInfo = {
       'imageId': imageId,
       'x1': x1,
       'y1': y1,
       'x2': x2,
       'y2': y2,
       'widthOnPage': widthOnPage,
       'heightOnPage': heightOnPage,
       'queryByRegion': queryByRegion
    }

    response = {
        'data': [],
    }

    imageLists = processDoSearch(searchInfo)
    response = {
        'searchImageInfo': {
            'id': imageId,
            'rect': f'x1={x1}&y1={y1}&x2={x2}&y2={y2}'
        },
        'results': imageLists
    }

    return jsonify(response)

def processDoSearch(searchInfo):
    logging.info("Search image info: %s", json.dumps(searchInfo))

    imgPath = os.path.join(datasetDir, searchInfo['imageId'])
    if searchInfo['queryByRegion'] == True:
        y1 = searchInfo['y1']
        y2 = searchInfo['y2']
        x1 = searchInfo['x1']
        x2 = searchInfo['x2']
        
        img = cv2.imread(imgPath)
        cropImg = img[y1:y2, x1:x2]
        imgPath = 'web/search/tmp_img.jpg' #+ searchInfo['imageId']
        cv2.imwrite(imgPath, cropImg)
        
    
    if os.path.isfile(imgPath):
        logging.info('Image Path: %s', imgPath)
        results = searcher.searchByImage(imgPath)
        imgResults = []
        for result in results:
            imgName = result[0].split('/')[-1]
            print(imgName)
            imgResults.append({'id': imgName})
    else:
        logging.info('Image Path: %s', imgPath)

    return imgResults

# start the server with the 'run()' method
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    app.run(debug=False, host='0.0.0.0', port=5000)
