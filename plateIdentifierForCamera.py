import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import requests
import json

url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

cam = cv2.VideoCapture(0)

while True:
    _,img = cam.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
    
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
        
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    
    text = result[0][-2]
    
    try: 

        reg=text
        payload = "{\n\t\"registrationNumber\": \" "+reg+"\"\n}"

        headers = {
        'x-api-key': 'qOda9XogGja9uQ4yQAHh18tlOSHEXowg3w6ER7b8',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = payload)
        data = json.loads(response.text)
        #Info available: reggistrationNumber, taxStatus, taxDueDate,motStatus,make,yearOfManfacture,engineCapacity,
        #co2Emissions,fuelType,markedForExport,colour,typeApproval,revenueWeight,euroStatus,dateOfLastV5CIssued,motExpiryDate,wheelplan,monthOfFirstRegistration
        print(data)

        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=data["taxStatus"], org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        print(text)
    except:
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text="", org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        print(text)
    
    
    
    if cv2.waitKey(1)==ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
