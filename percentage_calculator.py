# -*- coding: utf-8 -*-

from PIL import Image

#Generate a random image 640x150 with many colours but no black or white
img = Image.open('GOZONE.png')

pixels = img.getdata()
go = len(list(filter(lambda i: i >= 200, pixels)))
total = len(list(filter(lambda i: i >= 0, pixels)))
percentage = (go/total)*100
print("There are %d bright pixels" % go)
print("The picture is %d percent bright" % percentage)


