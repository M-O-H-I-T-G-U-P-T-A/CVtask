import cv2 as cv
import numpy as np
import math
import cv2.aruco as aruco
import os

# keep all images in a folder in same directory and the program will take care of the rest
directory=os.getcwd()
path = directory+"/"+"images" 
names=os.listdir(path)
#print(names)

# Note images[0] contains the problem image i.e., CVtask,jpg
images=[]
for i in names:
    if(i[-3:]!="jpg"):
        continue
    p=cv.imread(path+"/"+i)
    images.append(p)

    
# functions for displaying images and removing them 
def do():
    cv.waitKey(0)
    cv.destroyAllWindows()

def show(s,name):
    cv.imshow(s,name)
    do()
# show("hi",images[0])

# imgo is the original image
imgo = images[0].copy()
imgo=cv.resize(imgo,(877,620))

img = cv.cvtColor(imgo, cv.COLOR_BGR2GRAY)
img=cv.cvtColor(img,cv.COLOR_GRAY2RGB)

# using canny edge detector to get edges and the optimum parameters were determined after experimenting with different values
img=cv.Canny(img,100,150)
# show("img",img)


# function to get distance between two points
def dis(v1,v2):
    x=v1[0]-v2[0]
    x=x**2
    y=v1[1]-v2[1]
    y=y**2
    d=x+y
    d=math.sqrt(d)
    d=int(d)
    return d


#function to get mid point of two given points
def cen(v1,v2):
    x=(v1[0]+v2[0])/2
    x=int(x)
    y=(v1[1]+v2[1])/2
    y=int(y)
    v=[x,y]
    return v


# funcction to find squares in a given image
def findsq(img):
    cpy=imgo.copy()
    cont, hier = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    print(len(cont))
#     test=np.zeros(img.shape,np.uint8)
    test=np.zeros([620,877,3],np.uint8)
#     test[:]=255
#     imp=test.copy()
    test1=None
    count=0
    for i in cont:
        if (cv.contourArea(i) < 100):
            continue
        p=cv.arcLength(i,True)


        
# the value 0.006 was found after experimenting with different values using trackbar:
# cv.namedWindow("approximation")
# cv.resizeWindow("approximation", img.shape)
# cv.createTrackbar("ep", 'approximation', 0, 255, any)
# image = imgo.copy()
# c = max(cont, key=cv.contourArea)
# p = cv.arcLength(c, True)
# while True:
#
#     image = imgo.copy()
#     ep = cv.getTrackbarPos("ep", "approximation")
#     ep = ep / 1000
#     j = 1
#     for i in cont:
#         if (cv.contourArea(i) < 100):
#             continue
#         p = cv.arcLength(i, True)
#         approx = cv.approxPolyDP(i, p * ep, True)
#         print("cont ", j, "=", len(approx))
#         j = j + 1
#         image = cv.drawContours(image, [approx], -1, (255, 0, 0), 2)
#         cv.imshow("approximation", image)
#         if cv.waitKey(0) & 0xFF == ord('q'):
#             break
#     if cv.waitKey(10) & 0xFF == ord('q'):
#         break
# # cv.imshow("approximation", image)
# # cv.waitKey(0)
# cv.destroyAllWindows()



        approx=cv.approxPolyDP(i, p * 0.006, True)
        v=[]
        for p in approx:
            q=p[0]
            q=list(q)
            v.append(q)
            test2=cv.circle(cpy,(q[0],q[1]),3,(0,0,255),-1)
        if(len(approx)!=4):
            continue
        x1=dis(v[0],v[1])
        x2=dis(v[1],v[2])
        x3=dis(v[2],v[3])
        x4=dis(v[3],v[0])
        x5=dis(v[0],v[2])
        x6=dis(v[1],v[3])
        c=cen(v[0],v[2])
        # c contains the centre of square
        if (abs(x1 - x2) <= 1 and abs(x2 - x3) <= 1 and abs(x3 - x4) <= 1 and abs(x4 - x1) <= 1 and abs(x5 - x6) <= 1):
            # drawing contours only if the contour is a square
            test=cv.drawContours(test, [i], -1, (255,255,255), -1) 
            test2=cv.circle(test2,(c[0],c[1]),3,(255,255,255),1)
            t=tuple(test2[c[1]][c[0]])
            t=d[t]
            st=str(t)
            test2=cv.putText(test2, st, (c[0], c[1]), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
#             putaruco() 
            count +=1
    #print("squares=",count)
    #show("cont",test)
#     show('Test2',test2)
    return test


# function to find endpoints of a square containing the square contour
def findendp(v):
    xmin=v[0][0]
    ymin=v[0][1]
    xmax=v[0][0]
    ymax=v[0][1]
    for i in v:
        xmin=min(xmin,i[0])
        ymin=min(ymin,i[1])
        xmax=max(xmax,i[0])
        ymax=max(ymax,i[1])
    a=[xmin,ymin]
    b=[xmax,ymax]
    c=[a,b]
    return c


# manipulating the images of the aruco markers given so as to make use of them according to our needs

# function to find aruco markers in a image
def findAruco(img1):
    img = img1.copy()
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_5X5_250')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv.aruco.detectMarkers(img, arucoDict, parameters=arucoParam)
    cx = 0
    cy = 0
    o = 0
    size=0
    v=[]
    for j in range(len(corners)):
        for c in corners[j]:
            v.append(list(c[0]))
            v.append(list(c[1]))
            v.append(list(c[2]))
            v.append(list(c[3]))
            cx = c[0][0] + c[2][0]
            cx = cx / 2
            cx = int(cx)
            cy = c[0][1] + c[2][1]
            cy = cy / 2
            cy = int(cy)
            mx = c[0][0] + c[3][0]
            mx = mx / 2
            my = c[0][1] + c[3][1]
            my = my / 2
            dy = cy - my
            dx = cx - mx
            a=list(c[0])
            b=list(c[1])
            size=dis(a,b)
            o = math.degrees(math.atan((dy / dx)))
            if (dx < 0 and dy > 0):
                o = o + 180
            elif (dx < 0 and dy <= 0):
                o = o + 180
            elif (dy < 0 and dx > 0):
                o = 360 + o
#             o = int(o)
        for d in corners[j]:
            k = 0
            for c in d:
                s = int(c[0])
                m = int(c[1])
#                 img1 = cv.circle(img1, (s, m), 4, (0 + 100 * k, 100 * k, 255 - 50 * k), -1)
                k += 1
#         st = str(ids[j])
#         img1 = cv.circle(img1, (cx, cy), 2, (255, 0, 0), 1)
#         img1 = cv.putText(img1, st, (cx + 10, cy + 10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#         st = str(o)
#         st = "o= " + st
#         img1 = cv.putText(img1, st, (cx - 10, cy - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (40, 30, 255), 3)
    ep=findendp(v)
    #print(size)
    return (o,[cx,cy],img1,ids,size,ep)


# function to align aruco images
def align1(image):
    o,c,image,id,s,epa=findAruco(image)
    (h,w)=image.shape[:2]
    M = cv.getRotationMatrix2D((c[0],c[1]), o, 1.0)
    rotated = cv.warpAffine(image, M, (w, h),borderValue=(255,255,255))
#     show("rotated",rotated)
#     rotate=findAruco(rotated)
#     show("rotated",rotated)
    return (id,rotated,c)


# putting aruco markers in a list so that they can be accessed according to their ids
arucos=[None]*5
for i in range(1,5):
    id,im,c=align1(images[i].copy())
    id=id[0][0]
    a=np.zeros((620,877,3),np.uint8)
    #print(c)
    a[:]=255
    #print(im.shape)
    a[15:606,143:734]=im.copy()
    arucos[id]=a.copy()

# function to align images according to angle feeded to it
def align(image,ori):
    o,c,image,id,s,ep=findAruco(image)
    (h,w)=image.shape[:2]
    M = cv.getRotationMatrix2D((c[0],c[1]), ori, 1.0)
    rotated = cv.warpAffine(image, M, (w, h),borderValue=(255,255,255))
#     rotated=imutils.rotate_bound(image,ori)
#     show("rotated",rotated)
#     rotate=findAruco(rotated)
#     show("rotated",rotated)

    return (s,rotated)


# rrar stands for rotate resize aruco
# this function rotates and resize arucos so that they can be fitted to the square they are meant for
def rrar(arid,o,s):
    size,image=align(arucos[arid],o-90)
    a=(s/size)
    b=image.shape
    x=int(b[0]*a)
    y=int(b[1]*a)
    image=cv.resize(image,(y,x))
    return image


# aru is a image on which we will place aruco markers such that the aruco markers occupy the positions of the squares present in the original image
aru=np.zeros((620,877,3),np.uint8)
aru[:]=255
#show("white",aru)



# function to put aruco markers aligning according to the squares of original image in aru
def putAruco(ang,id,sqs,r):
    global aru
    img=rrar(id,-ang,sqs)
    o,c,img1,ids,size,epa=findAruco(img)
    sizex=epa[1][0]-epa[0][0]+r[0][0]
    sizey=epa[1][1]-epa[0][1]+r[0][1]
    sizex=int(sizex)
    sizey=int(sizey)
    r[0][0]=int(r[0][0])
    r[0][1]=int(r[0][1])
    epa[0][0]=int(epa[0][0])
    epa[0][1]=int(epa[0][1])
    epa[1][0]=int(epa[1][0])
    epa[1][1]=int(epa[1][1])
    #print(r)
    #print(epa)
    #show("aru",aru)
    #print("r[0][0]=",r[0][0])
    #print("sizex=",sizex,"sizey=",sizey)
    roiimgo=aru[r[0][1]:sizey,r[0][0]:sizex]
    #print(roiimgo)
    roiaruco=img[epa[0][1]:epa[1][1],epa[0][0]:epa[1][0]]
    #show("roiaruco",roiaruco)
    #show("roi",roiimgo)
    #print(roiimgo.shape,roiaruco.shape)
    roi=cv.bitwise_and(roiimgo,roiaruco)
    aru[r[0][1]:sizey,r[0][0]:sizex]=roi
    #show("aru",aru)



# d is the dictionary of all the colour of squares and the aruco ids associated with them
d={(0,0,0):3,(210,222,228):4,(9,127,240):2,(79,209,146):1}
imp=None



# advanced version of findsq function which integrates all the function mentioned above
def findsq2(img):
    cpy=imgo.copy()
    cont, hier = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
#     print(len(cont))
    test=np.zeros([620,877,3],np.uint8)
    test1=None
    count=0
    for i in cont:
        if (cv.contourArea(i) < 100):
            continue
        p=cv.arcLength(i,True)
        approx=cv.approxPolyDP(i, p * 0.006, True)
        
        v=[]
        for p in approx:
            q=p[0]
            q=list(q)
            v.append(q)
            test2=cv.circle(cpy,(q[0],q[1]),3,(0,0,255),-1)
        if(len(approx)!=4):
            continue
        x1=dis(v[0],v[1])
        x2=dis(v[1],v[2])
        x3=dis(v[2],v[3])
        x4=dis(v[3],v[0])
        x5=dis(v[0],v[2])
        x6=dis(v[1],v[3])
        c=cen(v[0],v[2])
        dx=v[3][0]-v[2][0]
        dy=v[3][1]-v[2][1]
        if(dx!=0):
            ang = math.degrees(math.atan((dy / dx)))
        else:
            ang=90
            
        if (abs(x1 - x2) <= 5 and abs(x2 - x3) <= 5 and abs(x3 - x4) <= 5 and abs(x4 - x1) <= 5 and abs(x5 - x6) <= 5):
            test=cv.drawContours(test, [i], -1, (255, 255,255), -1)
            ep=findendp(v)
            test2=cv.circle(test2,(c[0],c[1]),3,(255,255,255),1)
            t=tuple(test2[c[1]][c[0]])
            t=d[t]
            st=str(t)
            test2=cv.putText(test2, st, (c[0], c[1]), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            putAruco(ang,t,x1,ep) 
            count +=1
    #print("squares=",count)
    return test

# sending the canny detected image to the findsq2 function
imp=findsq2(img)






cv.imshow("imp",imp)
cv.imshow("aru",aru)
a=imp.copy()
b=aru.copy()
c=cv.bitwise_and(a,b)
show("c",c)# c contains the aruco markers' white parts in a black background

impnot=cv.bitwise_not(imp)
impand=cv.bitwise_and(imgo,impnot)
# imp and contains the image in which all the squares are replaced by black boxes
show("impand",impand)
ans=cv.add(c,impand)
show("ans",ans)



# Saving the result image
n=eval(input("enter 1 to save the result image and 0 to exit"))
if(n==1):
    cv.imwrite(directory+"/result.jpg",ans)

