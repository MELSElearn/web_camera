from flask import Flask, render_template, request
import numpy as np
import cv2
from base64 import b64decode, b64encode
from cvzone.HandTrackingModule import HandDetector

app = Flask(__name__)

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    #print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    #print(add)
    #print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]

    return myPointsNew

def rectContour(contours):
    #check if the contour is rectangle shape by checking is the
    #given contours provide 4 point of edges
    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    #print(len(rectCon))
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx

def splitBoxes(img):
    rows = np.vsplit(img,5) #verticle split
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,5) #horizontal split
        for box in cols:
            boxes.append(box)
    return boxes

def drawGrid(img,questions=5,choices=5):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)

    return img

def showAnswers(img,myIndex,grading,ans,questions=5,choices=5):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    
    for x in range(0,questions):
        myAns= myIndex[x]
        cX = (myAns * secW) + secW // 2
        cY = (x * secH) + secH // 2
        if grading[x]==1:
            myColor = (0,255,0)
            #cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
            cv2.circle(img,(cX,cY),50,myColor,cv2.FILLED)
        else:
            myColor = (0,0,255)
            #cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
            cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)

            # CORRECT ANSWER
            myColor = (0, 255, 0)
            correctAns = ans[x]
            cv2.circle(img,((correctAns * secW)+secW//2, (x * secH)+secH//2),
            20,myColor,cv2.FILLED)
    
    return img

@app.route('/', methods=['GET','POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', user_image = '')
    else:
        txt64 = request.form['txt64']
        encoded_data = txt64.split(',')[1]
        encoded_data = b64decode(encoded_data)
        nparr = np.frombuffer(encoded_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detector = HandDetector(detectionCon=0.8, maxHands=2)
        hands, img = detector.findHands(img)
        totalfingers=0
        if hands:
            fingers = detector.fingersUp(hands[0])
            totalfingers = fingers.count(1)
        
        cv2.putText(img,f'{int(totalfingers)}',(50,70), cv2.FONT_HERSHEY_PLAIN,5,(250,0,0),5)
            
        _, im_arr = cv2.imencode('.png', img)
        im_bytes = im_arr.tobytes()
        im_b64 = b64encode(im_bytes).decode("utf-8")

        return render_template('index.html', user_image = im_b64)
    
@app.route("/api/info", methods=['GET','POST'])
def api_info():
    txt64 = request.form.get("todo")
    encoded_data = txt64.split(',')[1]
    encoded_data = b64decode(encoded_data)
    nparr = np.frombuffer(encoded_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    hands, img = detector.findHands(img)
    totalfingers=0
    if hands:
        fingers = detector.fingersUp(hands[0])
        totalfingers = fingers.count(1)
    cv2.putText(img,f'{int(totalfingers)}',(50,70), cv2.FONT_HERSHEY_PLAIN,5,(250,0,0),5)
    _, im_arr = cv2.imencode('.png', img)
    im_bytes = im_arr.tobytes()
    im_b64 = b64encode(im_bytes).decode("utf-8")
    return im_b64
