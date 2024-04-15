import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    """Removes any previous images from the image folder"""
    print("clean_folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")


while True:
    status = 0
    check, frame = video.read()

    # Convert the image to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Adds gaussian blur to remove noise from image
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    """Looks at difference between first stored (static) frame and subsequent
     frames to detect differences"""

    thresh_frame = cv2.threshold(delta_frame, 40, 255, cv2.THRESH_BINARY)[1]
    """Reassigns the colour of pixels of a value of 30 or more to 255, making
    them white to increase the contrast"""

    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    # Looks at the last 2 entries in the status list

    if status_list[0] == 1 and status_list[1] == 0:  # If first entry is 1 and
        # second is 0 it means something has left the image frame
        email_thread = Thread(target=send_email, args=(image_with_object,))
        """ Added a comma to show image_with_object is a Tuple. If this is
         not done it will result in an error and will not recognise the 
         argument."""

        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()
        """Starts email in a separate thread to ensure that there is not a
         delay between the capture and the email"""

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):  # binds a key to exit the window
        break

video.release()
clean_thread.start()