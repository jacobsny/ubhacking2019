def main():
    # this is where the main will go
    # I need to have a function that takes in the image data as a 2d array
    # that function will then use the google cloud api and will pass the image through OCR
    # The OCR will return Google's custom format
    # I will then post process that format into a properly formated text file with tabs and all
    # I will pass the text file as a string to John's Piece of BackEnd
    # John's BackEnd will return the a list of flags that the syntax checker gave us for that text file
    # I will then take the text file and the flags and will format them into a canvas
    # this canvas will then be overlayed on the actual image from the display.
    # the goal is to keep this live but if it's a take a photo and it then just overlays the photo
    # that will most likely be acceptable
