import cv2
import syntax.check_syntax
import numpy as np

                        
def processIMG(imgArr):
    # this function takes a PIL Image
    # passed to Google Cloud Vision API
    # processes OCR data
    # returns string in code formatting written
    """Detects document features in an image."""
    """Image is a base64 encoded string"""
    annotation = client.document_text_detection(image=image)

    vertices = annotation.text_annotation[0]["boundingPoly"]["vertices"]

    verticesArr = [[loc["x"],loc["y"]] for loc in vertices]

    response = annotation.full_text_annotation.pages

    textArr = []
    def insertArr(word_dictionary):
        ylow = min(word_dictionary["boundingBox"],key=lambda vertex: vertex["y"])["y"]
        yup = max(word_dictionary["boundingBox"],key=lambda vertex: vertex["y"])["y"]
        if(len(textArr) > 0):
            for arr in textArr:
                for word1 in arr:
                  y2low = min(word1["boundingBox"],key=lambda vertex: vertex["y"])["y"]
                  y2up = max(word1["boundingBox"],key=lambda vertex: vertex["y"])["y"]
                  overlap = min([(y2up - y2low),(yup-ylow)]) * .66
                  print([ylow,yup],[y2low,y2up], overlap)
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
        for block in page["blocks"]:
            for paragraph in block["paragraphs"]:
                for word in paragraph["words"]:
                  word_text = ''.join([symbol["text"] for symbol in word["symbols"]])
                  word_dict = {"word": word_text, "boundingBox": word["boundingBox"]["vertices"]}
                  insertArr(word_dict)
    # array will be formated so it is a 2d array of lines and inside each line are the words in the line
    for i in range(len(textArr)):
        textArr[i] = sorted(textArr[i], key=lambda x: min(x["boundingBox"], key=lambda vertex: vertex["x"])["x"])
        print(textArr)
    textArr = sorted(textArr, key=lambda x: min(x[0]["boundingBox"], key=lambda vertex: vertex["y"])["y"])
    # array should be sorted in paragraph order
    textStr = "\n".join([" ".join([wordStr["word"] for wordStr in arr]) for arr in textArr])
    return textStr, verticesArr
                    

def processSyntax(flags, string, img, verticesArr):
    # this function takes the formatted string from processIMG
    # each flag {"location": line#, "description": "string of what's wrong"}
    # it takes the flags where there are syntax errors
    # it outputs a numpy array of the original img with the
    # new text data and flags overlayed on the img
    arr = string.split("\n")
    for flag in flags:
        arr[flag["location"]].append("// " + flag["description"])
    # byte array read to file
    # find predominent color in that polygon
    # fill the image with that predominent color
    # choose contrasting color to predominent color
    # put text in the center of that box left oriented
    # anything post // will be Red
    image = cv2.imdecode(img)
    pts = np.array(verticesArr,np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(image,[pts],(255,255,255))
    newStr = "\n".join(arr)
    origin = [min(verticesArr,key=lambda x: x[0])[0],min(verticesArr,key=lambda x: x[1])[1]]
    image = cv2.putText(img=image,text=newStr,org=(origin[0],origin[1]),bottomLeftOrigin=False)
    retval, buffer2 = cv2.imencode(".jpg",image)
    return base64.b64encode(buffer2)
    
    

def main(imgArr):
    # this is where the main will go
    # processIMG will be called on imgARR
    # half the returned data will go to John T
    # PIL img, text string, flags, and verticesArr will be passed to processSyntax
    # returned img will be sent to server
    string, verticesArr = processImg(imgArr)
    flags = check_syntax(string)
    newImage = processSyntax(flags,string,imgArr, verticesArr)
    return newImage
