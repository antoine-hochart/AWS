from flask import Flask, request
from flask_cors import CORS
from binascii import a2b_base64
import boto3
import json

app = Flask(__name__)
CORS(app)

@app.route("/get_picture/", methods=['GET', 'POST'])
def getpicture():
    rdata = request.get_data()
    image_name = 'myImage.jpg'
    save_uri_as_jpeg(rdata, image_name)
    print("image saved as {}".format(image_name))
    # Upload in S3 bucket
    upload_to_S3(image_name)
    # Launch Reko detect faces...
    myjson = AWSdetect_faces(image_name)
    # Extract Json infos
    answer = get_features_from_json(myjson)
    return answer

@app.route("/analyze/", methods=['GET', 'POST'])
def happiness():
    answer = AWSmood()
    print(answer)
    return answer

def save_uri_as_jpeg(uri, imagename):
    imgData = str(uri)
    imgData64 = imgData[imgData.find(',') + 1:]
    binary_data = a2b_base64(imgData64)
    with open(imagename, 'wb') as fd:
        fd.write(binary_data)

def upload_to_S3(imagename):
    mys3 = boto3.resource('s3')
    mybucket = mys3.Bucket('image-for-mood-reko')
    myobject = mybucket.Object(imagename)
    # since filename is always the same, delete old one before adding new one
    myobject.delete()
    myobject.wait_until_not_exists()
    myobject.upload_file(imagename)
    myobject.wait_until_exists()
    print(imagename + " uploaded")

def AWSdetect_faces(imagename):
    reko = boto3.client('rekognition')
    response = reko.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': 'image-for-mood-reko',
                    'Name': imagename,
                    }
                },
            Attributes=[
                'ALL',
                ]
            )
    return response

def AWSmood():
    reko = boto3.client('rekognition')
    response = reko.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': 'image-for-mood-reko',
                    'Name': 'myImage.jpg',
                    }
                },
            Attributes=[
                'ALL',
                ]
            )
    facedetails = response['FaceDetails']
    if len(facedetails) > 0:
        emotion = facedetails[0]['Emotions'][0]
        emotion_type = emotion['Type']
        confidence = emotion['Confidence']
        mystr = "<kbd>YOU ARE " + emotion_type + " (AT " + "{:.1f}%)".format(confidence) + "</kbd>"
    else:
        mystr = "<kbd> NO EMOTIONS </kbd>"
    return mystr

def get_features_from_json(myjson):
    mystr = ""
    facedetails = myjson['FaceDetails']
    nbfaces = len(facedetails)
    notusedattributes = ['BoundingBox', 'Landmarks', 'Pose', 'Quality', 'Confidence', 'Emotions']
    if nbfaces == 1:
        face = facedetails[0]
        mystr += '<table class="table table-sm table-striped bg-light m-2">'
        for attribute, details in face.items():
            if attribute not in notusedattributes:
                mystr += '<tr>'
                if attribute == 'AgeRange':
                    mystr += "<td>{}</td><td>{:d}</td><td>{:d} yo</td>".format(attribute, details['Low'], details['High'])
                else:
                    mystr += "<td>{}</td><td>{}</td><td>{:.1f}</td>".format(
                            attribute, details['Value'], details['Confidence'])
                    mystr += "</tr>"
        mystr += "</table>"
    elif nbfaces > 1:
        mystr += "{} faces found on picture...\n".format(len(facedetails))
    else:
        mystr += "nobody on picture...\n"
    return mystr

if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)
