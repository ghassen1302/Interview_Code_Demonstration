'''
    File name         : objTracking.py
    Description       : Main file for object tracking
    Author            : Rahmad Sadli
    Date created      : 20/02/2020
    Python Version    : 3.7
'''

import cv2
from Detector import detect
from KalmanFilter import KalmanFilter
import matplotlib.pyplot as plt

def main():

    # Create opencv video capture object
    VideoCap = cv2.VideoCapture(0)

    #Variable used to control the speed of reading the video
    ControlSpeedVar = 100  #Lowest: 1 - Highest:100

    HiSpeed = 100

    #Create KalmanFilter object KF
    #KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)

    KF = KalmanFilter(0.1, 1, 1, 1, 0.1,0.1)

    debugMode=1
    predicted_x=[]
    predicted_y=[]
    estimated_x=[]
    estimated_y=[]
    measured_x=[]
    measured_y=[]
    try:
        while(True):
            # Read frame
            ret, frame = VideoCap.read()

            # Detect object
            centers = detect(frame,debugMode)

            # If centroids are detected then track them
            if (len(centers) > 0):

                # Draw the detected circle
                cv2.circle(frame, (int(centers[0][0]), int(centers[0][1])), 10, (0, 191, 255), 2)
                measured_x.append(int(centers[0][0]))
                measured_y.append(int(centers[0][1]))
                
                # Predict
                (x, y) = KF.predict()
                predicted_x.append(x.item((0, 0)))
                predicted_y.append(y.item((0, 0)))
                
                # Draw a rectangle as the predicted object position
                cv2.rectangle(frame, (x - 15, y - 15), (x + 15, y + 15), (255, 0, 0), 2)

                # Update
                (x1, y1) = KF.update(centers[0])
                estimated_x.append(x1.item((0, 0)))
                estimated_y.append(y1.item((0, 0)))

                # Draw a rectangle as the estimated object position
                cv2.rectangle(frame, (x1 - 15, y1 - 15), (x1 + 15, y1 + 15), (0, 0, 255), 2)

                cv2.putText(frame, "Estimated Position", (x1 + 15, y1 + 10), 0, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, "Predicted Position", (x + 15, y), 0, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, "Measured Position", (centers[0][0] + 15, centers[0][1] - 15), 0, 0.5, (0,191,255), 2)

            cv2.imshow('image', frame)

            if cv2.waitKey(2) & 0xFF == ord('q'):
                VideoCap.release()
                cv2.destroyAllWindows()
                break

            cv2.waitKey(HiSpeed-ControlSpeedVar+1)
    except:
        pass
    plt.figure()
    plt.plot(measured_x,measured_y,'b',label='measured')
    plt.plot(predicted_x,predicted_y,'g',label='predicted')
    plt.plot(estimated_x,estimated_y,'r',label='estimated')
    plt.legend(loc=2)
    plt.title("Variation de la position de l’objet suivi")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


if __name__ == "__main__":
    # execute main
    main()