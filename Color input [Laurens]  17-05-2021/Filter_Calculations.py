from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops
import time
import os
import glob

import GUI_Buttons as GB
import GUI_Calculations as GC

# Settings values
conectivity, intensity, threshold = 1, 20, 48
layertreshold = 0.7  # Maybe 2 different needed (Normal and Stop layer)
finaltreshold = 0.9  # MUST BE LOWER THAN layertreshold
#currentlayer = 0 # First paint layer

if finaltreshold > layertreshold:
    finaltreshold = layertreshold


def overlap(imageA, imageB):
    # Making sure image is in Grayscale
    imageA = imageA.convert('L')
    imageB = imageB.convert('L')

    #   Alpha-blend the images
    buffer_blend = Image.blend(imageA, imageB, alpha=0.5)

    #   Operation to each pixel
    overlaped = buffer_blend.point(lambda i: (i == 255) * 255)

    return overlaped


def combine(imageA, imageB):
    # Making sure image is in Grayscale
    imageA = imageA.convert('1')
    imageB = imageB.convert('1')

    #   Alpha-blend the images
    combined = ImageChops.logical_or(imageA, imageB)

    return combined.convert('L')


def invert(image1):
    # Making sure image is in Grayscale
    img = image1.convert('L')

    # Inverting the images and maximizing all pixels
    imginvert = img.point(lambda i: (not i) * 255)
    return imginvert


def radius(image1, runs):
    # Making sure image is in Grayscale
    image1 = image1.convert('L')

    # Apply maximum filter
    filterApplied = image1
    for i in range(0, runs):
        filterApplied = filterApplied.filter(ImageFilter.MaxFilter())
        #print("Radius run: " + str(i + 1))

    return filterApplied



def mask(image1, colour, sens):
    # Split the red, green and blue bands from the Image
    multiBands = image1.split()

    # ERROR COULD ACCUR HERE IF THE IMAGE DOES NOT HAVE ENOUGH BANDS
    # Apply point operations that does thresholding on each color band
    redBand = multiBands[0].convert("L").point(
        lambda i: (i > (colour[0] - sens) and i < (colour[0] + sens)) * 255).convert('1')
    greenBand = multiBands[1].convert("L").point(
        lambda i: (i > (colour[1] - sens) and i < (colour[1] + sens)) * 255).convert('1')
    blueBand = multiBands[2].convert("L").point(
        lambda i: (i > (colour[2] - sens) and i < (colour[2] + sens)) * 255).convert('1')

    # Combining all alpha bands to one picture
    buffer = ImageChops.logical_and(redBand, greenBand)
    buffer = ImageChops.logical_and(buffer, blueBand)

    # Create a new image from the thresholded and combined red, green and blue brands (changing picture from Alpha to "RGB")
    buffer = buffer.convert('L')

    return buffer


def blur(image1, runs):
    # Making sure image is in Grayscale
    image1 = image1.convert('L')

    # Applying radius filter for better conectivity
    filterApplied = radius(image1, conectivity)

    # GaussianBlur with limit value
    for i in range(0, runs):
        blured = filterApplied.filter(ImageFilter.GaussianBlur(intensity))
        filterApplied = blured.point(lambda i: (i - threshold) * 255)

        #print("Blur run: " + str(i + 1))

    # Maximise brightness  (making sure all pictures are as expected)
    filterApplied = filterApplied.point(lambda i: i * 255)

    return filterApplied


# Temperarely to allow for working of script
def percentage(image1):
    return 0.7

def rgb_to_hsv(rgb):
    r,g,b = rgb
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100

    # Creating tuple from colours in 0-255 range
    hsv = h/360*255,s/100*255,v/100*255
    return hsv


def multimask(image, colourrgb, sens):
    # Converting rgb ranges to HSV ranges
    colourhsv = rgb_to_hsv(colourrgb)

    # Masking image for both colour ranges
    maskrgb = mask(image, colourrgb, sens)
    maskhsv = mask(image.convert("HSV"), colourhsv, sens)

    # Combining masks
    maskrgbhsv = overlap(maskrgb, maskhsv)

    # Peforming image operations for better mask
    maskrgbhsv = blur(maskrgbhsv, 1)
    maskrgbhsv = radius(maskrgbhsv, 1)

    return maskrgbhsv

def colorCalculator(filter_list):      ############################ Output Zone calculation

    #Show in window that calculation is started
    #print ("Started inside of colorcalculator function")

    # Show calculating text


    for key in filter_list:
        print(filter_list[key].rgbs)

    ########    Input from user interface    ########

    state = "layercolour"

    rgbs = []
    for item in filter_list.values():
        rgbs.append(item.rgbs)

    rgb = []
    cal = []
    for code in rgbs:
        rgb.append(code[:3])
        cal.append(code[3])

    print(rgb)
    print(cal)

    # Determine ammount of used layers #maybe layers until stop layer instead of total?
    StopL = len(filter_list)-2
    NoGoL = len(filter_list)-1

    # NEED TO KNOW WHAT LAYER IS STOP AND NOGO
    rgbstop, calstop = rgb[StopL], cal[StopL]
    rgbnogo, calnogo = rgb[NoGoL], cal[NoGoL]



    #Image used for calculaitons
    image = Image.open(GC.Auto_Image_Path)



    #####################################################
    #THIS SHOULD BE SOMEWHERE ELSE FOR MULTIPLE OPERATIONS#
    #AND SHOULD CHANGE FOR EACH TIME THE PROGRAM HAS RUNN#
    # First setup start values (these variables whill change over time [in the while loop])
    sideL = [0,0,0,0,0,0]
    side = 0
    FinishedSides = 0 # Finished Side counter
    TotalSides = 6



    ########################################################



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
        GoColour1 = multimask(image, RGBAct, CalAct)
        # GoColour1.show()

        # Previous colour mask
        GoColour2 = multimask(image, RGBPrev, CalPrev)
        # GoColour2.show()

        # STOP COLOUR MASK
        StopMask_W = multimask(image, rgbstop, calstop)
        StopMask_W = radius(StopMask_W, 1)
        StopMask = invert(StopMask_W)

        # NO GO COMPO
        CompoMask_W = multimask(image, rgbnogo, calnogo)
        CompoMask_W = radius(CompoMask_W, 1)
        CompoMask = invert(CompoMask_W)

        state = "combinemasks"


    # Combine all masks to final GO Zones
    if state == "combinemasks":
        GoColour = combine(GoColour1, GoColour2)

        # Black is no go so the image must be inverted beforehand
        # Only where all the NOGO zones show white is allowed to be sanded (NOT NO GO ZONES)
        NoGoMask = overlap(StopMask, CompoMask)

        # Combining not no go with go to make the final mask
        GoZones = overlap(GoColour, NoGoMask)
        GoZones.save("GOZONE.png", "PNG")
        # GoZones.show()

        state = "storedata"


    # Store all data needed in correct locations
    if state == "storedata":
        #what to save?
        state = "checksanding"


    # Check the final Go zone mask if sanding is needed
    # If no sanding is needed the active layer and side will be changed acordingly
    if state == "checksanding":
        # Check the percentage white in mask
        NoGopers = percentage(NoGoMask)
        Gopers = percentage(GoZones)

        if (Gopers < layertreshold and sideL[side] < StopL):
            continuenext = False
            # Check the image, will return the current layer, current side and completed sides

        # Check if this layer is done
        if (Gopers >= layertreshold and sideL[side] < StopL):
            # Setting the working layer to the next layer
            sideL[side] += 0

            # Setting value to continue to next layer after setting all variables
            continuenext = True

            # Resetting timer to stop
            FinishedSides = 0

        # Check if this is last layer and done
        if (NoGopers >= finaltreshold):
            FinishedSides += 1
            print("side completed, proceed to next side (Total in row finished:" + str(FinishedSides))
            continuenext = True





        # check if going to next side
        if (continuenext == True):
            # Change side variable
            side += 0

            # Loop the side value for six sides
            if (side == TotalSides):
                side = 0

            # Reset side change
            continuenext = False

            # Continue to next side
            print("Continued to next side")
            state = "nextside"
        else:
            print("Start Sanding")
            state = "sanding"

        if (FinishedSides >= TotalSides):
            print("Completed all sides")
            state = "finished"


    # Send command to the machine to make a picture and wait for said picture
    if state == "nextside":
        # send command to go to next side and make picture
        #wait for new image
        # when new image go back to checkcolour
        print("nextside")
        return GoZones


    # Waiting for sanding to be finished or until new image???
    if state == "sanding":
        print("sanding")
        return GoZones

    # All sides finished return to user interface
    if state == "finished":
        print("finished")
        GB.popup("This side is finished. The next side can be positioned")
        return GoZones

