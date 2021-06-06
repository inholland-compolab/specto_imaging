import cv2
import os
mainfolder = r"C:\Image stitching test\images"
mainoutput = r"C:\Image stitching test\output"
myfolders = os.listdir(mainfolder)
print(myfolders)

for folder in myfolders:
    path = mainfolder+'/'+folder
    images = []
    myList = os.listdir(path)
    for imgN in myList:
        curImg = cv2.imread(f'{path}/{imgN}')
        images.append(curImg)
        sticher = cv2.Stitcher.create()
        (status,results) = sticher.stitch(images)
        if (status == cv2.Stitcher_OK):
            print('Stitching succesful')
            cv2.imshow(folder,results)
            cv2.waitKey(1)
        else:
            print("Stitching failed")
cv2.waitKey(0)
