import requests
import cv2
import numpy 
  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.1.2:8080/shot.jpg"

vid = cv2.VideoCapture(1)

# While loop to continuously fetching data from the Url
while True:
    #img_resp = requests.get(url)
    #img_arr = numpy.array(bytearray(img_resp.content), dtype=numpy.uint8)
    #img = cv2.imdecode(img_arr, -1)
    ret, frame = vid.read()
    img=frame
    #img=cv2.resize(frame, (800, 500))
    img=img[200:,250:]
    cv2.imshow("cam", img)
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()