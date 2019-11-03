import cv2

                        
def processIMG(imgArr):
    # this function takes a PIL Image
    # passed to Google Cloud Vision API
    # processes OCR data
    # returns string in code formatting written
    """Detects document features in an image."""
    """Image is a base64 encoded string"""

    response = client.document_text_detection(image=image)

    textArr = []
    def insertArr(word_dictionary):
        ylow = min(word_dictionary.boundingBox,key=lambda vertex: vertex.y)
        yup = max(word_dictionary.boundingBox,key=lambda vertex: vertex.y)
        if(len(textArr) > 0):
            for arr in textArr:
                for word1 in arr:
                    y2low = min(word1.boundingBox,key=lambda vertex: vertex.y)
                    y2up = max(word1.boundingBox,key=lambda vertex: vertex.y)
                    overlap = min([(y2up - y2low),(yup-ylow)]) * .66
                    if(yup =< y2up && yup > y2low):
                        if(yup - max(y2low,yup) >= overlap):
                            arr.append(word_dictionary)
                            return
                    if(y2up < yup && y2up > ylow):
                        if(y2up - max(ylow,y2up)):
                            arr.append(word_dictionary)
                            return
        textArr.append([word_dictionary])
        return

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    word_dict = {"word": word_text, "boundingBox": word.boundingBox.vertices}
                    insertArr(word_dict)
    # array will be formated so it is a 2d array of lines and inside each line are the words in the line
                    
                    

def processSyntax(flags, string, img):
    # this function takes the formatted string from processIMG
    # it takes the flags where there are syntax errors
    # it outputs a numpy array of the original img with the
    # new text data and flags overlayed on the img

def main(imgArr):
    # this is where the main will go
    # processIMG will be called on imgARR
    # returned data will go to John T
    # PIL img, text string, and flags will be passed to processSyntax
    # returned img will be sent to server
