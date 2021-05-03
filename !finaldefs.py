from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops
import time
import os

import numpy as np

########    Input from user interface    ########

# Process control user interface
state = "layercolour"

# Values
filter_list = {
    'filter0': (128, 128, 128, 20),
    'filter1': (128, 128, 128, 20),
    'filter2': (128, 128, 128, 20),
    'filter3': (128, 128, 128, 20),
    'filter4': (128, 128, 128, 20),
    'filter5': (128, 128, 128, 20) # composite layer
}

print()

rgbs = [list(i) for i in filter_list.values()]

rgb = []
cal = []
for code in rgbs:
    rgb.append(code[:3])
    cal.append(code[3])

print(rgb)
print(cal)

rgbstop, calstop = [24,30,30], 20
rgbnogo, calnogo = [129,123,1], 20

layertreshold = 0.8

# Images
image = Image.open(os.path.dirname(os.path.realpath(__file__)) + r"\Face 6.jpg").convert("RGB")
mask1 = Image.open(os.path.dirname(os.path.realpath(__file__)) + r"\background.png").convert("RGB")
mask2 = Image.open(os.path.dirname(os.path.realpath(__file__)) + r"\manual.png").convert("RGB")

# First setup start values
totalL = 0
sideL = [1,0,0,0,0,0]
side = 0
fs = 0

# Determine ammount of used layers
totalL = len(filter_list)

print ("Active layers:"+str(totalL))


########################################################


def overlap(imageA,imageB):     
    # Making sure image is in Grayscale   
    imageA = imageA.convert('L')    
    imageB = imageB.convert('L')

    #   Alpha-blend the images
    buffer_blend = Image.blend(imageA, imageB, alpha=0.5)    

    #   Operation to each pixel
    overlaped = buffer_blend.point(lambda i: (i==255) * 255)

    return overlaped


def combine(imageA,imageB):     
    # Making sure image is in Grayscale   
    imageA = imageA.convert('1')    
    imageB = imageB.convert('1')

    #   Alpha-blend the images
    combined = ImageChops.logical_or(imageA, imageB)    

    return combined.convert('L')


def invert(image1): 
    # Making sure image is in Grayscale   
    img = image1.convert('L')

    # Inverting the images
    imginvert = img.point(lambda i: (not i) * 255)
    return imginvert


def radius(image1,runs): 
    # Making sure image is in Grayscale   
    image1 = image1.convert('L')

    # Apply maximum filter
    filterApplied = image1
    for i in range(0, runs):
        filterApplied = filterApplied.filter(ImageFilter.MaxFilter())
        print("Radius run: "+str(i+1))

    return filterApplied

#not finished
def mask(image1,colour,sens):
    # Split the red, green and blue bands from the Image     
    multiBands      = image1.split()

    n1,n2,n3 = colour

    # ERROR COULD ACCUR HERE IF THE IMAGE DOES NOT HAVE ENOUGH BANDS  
    # Apply point operations that does thresholding on each color band
    redBand      = multiBands[0].point(lambda i: (i > (n1-sens) and i < (n1+sens)) * 255).convert('1')
    greenBand    = multiBands[1].point(lambda i: (i > (n2-sens) and i < (n2+sens)) * 255).convert('1')
    blueBand     = multiBands[2].point(lambda i: (i > (n3-sens) and i < (n3+sens)) * 255).convert('1')

    # Combining all alpha bands to one picture
    buffer = ImageChops.logical_and(redBand, greenBand)
    buffer = ImageChops.logical_and(buffer, blueBand)

    #buffer_merge = Image.merge("RGB", (redBand, greenBand, blueBand))
    # buffer10.show()

    # Create a new image from the thresholded and combined red, green and blue brands (changing picture from Alpha to "RGB")
    buffer = buffer.convert('L')
    buffer = Image.merge("RGB", (buffer, buffer, buffer))
    buffer = buffer.convert("L")

    return buffer

def blur(image1,runs,conectivity,intensity,threshold):
    # Making sure image is in Grayscale   
    image1 = image1.convert('L')

    # Applying radius filter for better conectivity
    filterApplied = radius(image1,conectivity)
    
    # GaussianBlur with limit value
    for i in range(0, runs):
        
        blured = filterApplied.filter(ImageFilter.GaussianBlur(intensity))
        filterApplied = blured.point(lambda i: (i - threshold)*255 )

        print("Blur run: "+str(i+1))

    # Maximise brightness  (making sure all pictures are as expected)
    filterApplied = filterApplied.point(lambda i: i*255 )

    return filterApplied

# Temperarely to allow for working of script
def percentage(image1):
    return 0.7

# Setting the active and previous GO Colours for sanding
def SetLayer(image1, comp):
    # Check current layer
    layerbuffer = sideL[side]

    # Check the percentage white in mask
    pers = percentage(image1)

    # Check if current layer is enough left (if not continue to next layer)
    if (pers >= layertreshold):
        
        # Check if last layer
        if (layerbuffer == totalL):
            # Count amount of final layers completed in a row
            comp += 1
           
            # CONTINUE TO NEXT SIDE
            gotonext = True
            print ("side completed, proceed to next side (Total in row finished:"+str(fs))
            return layerbuffer, gotonext, comp

        # Setting the working layer to the next layer    
        layerbuffer += 1        

        # Setting value to continue to next layer after setting all variables
        gotonext = True
        
        # Resetting timer to stop
        comp = 0
    else:
        gotonext = False

    return layerbuffer, gotonext, comp

########################################################

while fs <= 6:
    
    # Sets the colour for the current layer and side to be active
    if state == "layercolour":   
        RGBAct = rgb[sideL[side]]
        CalAct = cal[sideL[side]]

        # Check if there is a previous colour (if not 2 same masks are created)
        if sideL[side] == 0:
            RGBPrev = RGBAct
            CalPrev = CalAct
        else:           
            RGBPrev = rgb[sideL[side]-1]
            CalPrev = cal[sideL[side]-1]

        # Go to next state
        state = "createmasks"

        # Print some information about this mask
        print("Colour: "+str(RGBAct)+" calibration: "+str(CalAct))
        print("Current side: "+str(side))
        print("Current layer on side: "+str(sideL[side]))


    # Create all masks
    if state == "createmasks":
        # Current colour mask 
        # (WILL BE DEFENITION THAT DOES THE SAME THING FOR ALL COLOURSSPACES)
        GoColour1 = mask(image,RGBAct,CalAct)
        GoColour1 = blur(GoColour1,1,1,20,48)
        GoColour1 = radius(GoColour1,1)
        GoColour1.show()

        # Previous colour mask
        # (WILL BE DEFENITION THAT DOES THE SAME THING FOR ALL COLOURSSPACES)
        GoColour2 = mask(image,RGBPrev,CalPrev)
        GoColour2 = blur(GoColour2,1,1,20,48)
        GoColour2 = radius(GoColour2,0)
        #GoColour2.show()

        # STOP COLOUR MASK
        # (WILL BE DEFENITION THAT DOES THE SAME THING FOR ALL COLOURSSPACES)
        #thingies for that

        #NO GO TAPE MASK
        # (WILL BE DEFENITION THAT DOES THE SAME THING FOR ALL COLOURSSPACES)
        #thingies for that

        state = "combinemasks"


    # Combine all masks to final GO Zones
    if state == "combinemasks":

        GoColour = combine(GoColour1,GoColour2)
        GoColour = blur(GoColour,0,1,20,48)
        GoColour = radius(GoColour,0)
        #GoColour.show()

        FinalImg = overlap(image,mask1)
        FinalImg.save("GOZONE.png","PNG")
        #FinalImg.show()

        state = "checksanding"


    # Store all data needed in correct locations
    if state == "storedata":
        #what to save?
        state = "checksanding"


    # Check the final Go zone mask if sanding is needed
    # If no sanding is needed the active layer and side will be changed acordingly
    if state == "checksanding":
        # Check the image, will return the current layer, current side and completed sides
        sideL[side], continuenext, fs = SetLayer(FinalImg,fs)

        # check if going to next side
        if (continuenext == True):
            # Change side variable
            side = side + 1

            #Reset side change
            continuenext = False

            #Loop the side value for six sides
            if (side == 6):
                side = 0

            # Continue to next side
            print("Continued to next side")
            state = "nextside"
            
        else:
            print("checksanding")
            # Check if the machine is finished
            if fs == 6:
                state = "finished"
            else:        
                
                state = "sanding"


    # Send command to the machine to make a picture and wait for said picture
    if state == "nextside":
        # send command to go to next side and make picture
        #wait for new image
        # when new image go back to checkcolour
        print("nextside")


    # Waiting for sanding to be finished or until new image???
    if state == "sanding":
        print("sanding")
        break

    # All sides finished return to user interface
    if state == "finished":
        print("finished")


    # State of the program while user interface is active (user is changing values)
    if state == "preview":
        print("returning preview image to interface")

    #"program unresponsive" adding a 0.1 second delay 
    time.sleep(0.1)

    #Image.merge("HSV", (image.convert("L"), GoColour1, image.convert("L"))).show()
    #Image.merge("HSV", (image.convert("L"), GoColour2, image.convert("L"))).show()
    #Image.merge("HSV", (image.convert("L"), FinalImg, image.convert("L"))).show()


    #Image.merge("HSV", (image.convert("L"), GoColour1, image.convert("L"))).convert("RGB").save("./Tests/GOZONE_blur1_int20_radius50.png","PNG")
