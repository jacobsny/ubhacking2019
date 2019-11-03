import cv2
from syntax import check_syntax
import numpy as np
import base64
import io

                        
def processIMG(imgArr):
    # this function takes a PIL Image
    # passed to Google Cloud Vision API
    # processes OCR data
    # returns string in code formatting written
    """Detects document features in an image."""
    """Image is a base64 encoded string"""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image(content=base64.b64decode(imgArr))
    
    annotation = client.document_text_detection(image=image)

    # print(annotation)

    vertices = annotation.text_annotations[0].bounding_poly.vertices

    verticesArr = [[loc.x,loc.y] for loc in vertices]

    response = annotation.full_text_annotation.pages

    textArr = []
    def insertArr(word_dictionary):
        ylow = min(word_dictionary["boundingBox"],key=lambda vertex: vertex.y).y
        yup = max(word_dictionary["boundingBox"],key=lambda vertex: vertex.y).y
        if(len(textArr) > 0):
            for arr in textArr:
                for word1 in arr:
                  y2low = min(word1["boundingBox"],key=lambda vertex: vertex.y).y
                  y2up = max(word1["boundingBox"],key=lambda vertex: vertex.y).y
                  overlap = min([(y2up - y2low),(yup-ylow)]) * .66
                  if (yup <= y2up and yup > y2low):
                      if(yup - max(y2low,ylow) >= overlap):
                          arr.append(word_dictionary)
                          return
                  if(y2up < yup and y2up > ylow):
                      if(y2up - max(ylow,y2low) >= overlap):
                          arr.append(word_dictionary)
                          return
        textArr.append([word_dictionary])
        return

    for page in response:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    word_dict = {"word": word_text, "boundingBox": word.bounding_box.vertices}
                    insertArr(word_dict)
    # array will be formated so it is a 2d array of lines and inside each line are the words in the line
    for i in range(len(textArr)):
        textArr[i] = sorted(textArr[i], key=lambda x: min(x["boundingBox"], key=lambda vertex: vertex.x).x)
    textArr = sorted(textArr, key=lambda x: min(x[0]["boundingBox"], key=lambda vertex: vertex.y).y)
    # array should be sorted in paragraph order
    textStr = "\n".join([" ".join([wordStr["word"] for wordStr in arr]) for arr in textArr])
    print(textStr)
    return textStr, verticesArr
                    

def processSyntax(flags, string, img, verticesArr):
    # this function takes the formatted string from processIMG
    # each flag {"location": line#, "description": "string of what's wrong"}
    # it takes the flags where there are syntax errors
    # it outputs a numpy array of the original img with the
    # new text data and flags overlayed on the img
    arr = string.split("\n")
    for flag in flags:
        arr[flag["location"]-1] += ("// " + flag["description"])
    # byte array read to file
    # find predominent color in that polygon
    # fill the image with that predominent color
    # choose contrasting color to predominent color
    # put text in the center of that box left oriented
    # anything post // will be Red
    nparr = np.fromstring(base64.b64decode(img), np.float32)
    yrange = max(verticesArr, key=lambda x: x[1])[1] - min(verticesArr, key=lambda x: x[1])[1]
    xrange = max(verticesArr, key=lambda x: x[0])[0] - min(verticesArr, key=lambda x: x[0])[0]
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    pts = np.array(verticesArr,np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(image,[pts],(255,255,255))
    maxStr = max(arr)
    textSize = cv2.getTextSize(maxStr,cv2.FONT_HERSHEY_SIMPLEX,1,1)
    yscale = yrange / len(verticesArr) / textSize[0][1]
    xscale = xrange / textSize[0][0]
    print(xscale,yscale)
    newStr = "\n".join(arr)
    origin = [min(verticesArr,key=lambda x: x[0])[0],min(verticesArr,key=lambda x: x[1])[1]]
    yheight = yrange / len(verticesArr)
    count = 1
    for string in arr:
        image = cv2.putText(img=image,text=string,org=(origin[0],int(origin[1]+(yheight * count))),bottomLeftOrigin=False,fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=min(yscale,xscale)*1.25,color=(0,0,0))
        count += 1
    retval, buffer2 = cv2.imencode(".jpg",image)
    return base64.b64encode(buffer2)
    
    

def mainProcess(imgArr):
    # this is where the main will go
    # processIMG will be called on imgARR
    # half the returned data will go to John T
    # PIL img, text string, flags, and verticesArr will be passed to processSyntax
    # returned img will be sent to server
    string, verticesArr = processIMG(imgArr)
    flags = check_syntax(string)
    newImage = processSyntax(flags,string,imgArr, verticesArr)
    return newImage

if __name__ == "__main__":
    testImg = "/home/jacobsny/Downloads/OCR-detect-handwriting.png"
    with open(testImg, "rb") as imageFile:
        imgCode:bytes = (imageFile.read())
        b64Str = base64.b64encode(imgCode)
        # print(imgCode)
        img = mainProcess(b64Str)
        filename = "./test.jpg"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(img))
    
