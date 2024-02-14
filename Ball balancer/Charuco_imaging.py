import cv2 as cv
import numpy as np
import time
import os

# Board Parameters
ARUCO_DICT = cv.aruco.DICT_5X5_250 # 5 bit x 5 bit codes w/ hamming distance of 6, 250
SIZE = (8,8) # number of squares in (x,y)
SQUARE_LENGTH = 0.024 # meters
MARKER_LENGTH = 0.014 # meters
MARKER_RATIO = SQUARE_LENGTH/MARKER_LENGTH
IMAGE_SIZE = (800,800)
CALIBRATION_LOCATION = 'C:/Users/trist/OneDrive/Desktop/Projects/Ball balancer/CamCalibration'
CAM_MATRIX_PATH = 'C:/Users/trist\OneDrive/Desktop/Projects/Ball balancer/3camMatrix.npy'
DISTORTION_MATRIX_PATH = 'C:/Users/trist\OneDrive/Desktop/Projects/Ball balancer/3distMatrix.npy'
WINDOW_SIZE = (480, 640)
TRANSFORMED_SIZE = (480, 480)



def generateCharucoBoard():
    """
    creates a CharucoBoard PNG based off predefined parameters
    """
    dictionary = cv.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv.aruco.CharucoBoard(SIZE, SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    image = board.generateImage(IMAGE_SIZE)

    cv.imshow("charuco", image)
    np.save('charucoBoard.npy', board)
    #cv.imwrite('charucoBoard.png', image)

    # Press Q on keyboard to stop image display
    while True:

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
      


def saveCalibrationCameraParameters ():
    """
    Takes a folder of images and calculates the camera and distortion matrix. These get saved to a np array for later use
    """
    # Load the board parameters
    dictionary = cv.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv.aruco.CharucoBoard(SIZE, SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    params = cv.aruco.DetectorParameters()


    # Load the calibration images and saves the filepath to a list
    images = []
    for filename in os.listdir(CALIBRATION_LOCATION):
        if filename.endswith('.jpg'):
            image_path = os.path.join(CALIBRATION_LOCATION,filename).replace("\\", "/")
            images.append(image_path)

    
    

    all_charuco_corners = []
    all_charuco_ids = []

    # checks each image for charuco Patterns 
    for image_file in images:
        image = cv.imread(image_file)
        marker_corners, marker_ids, _ = cv.aruco.detectMarkers(image, dictionary, parameters = params)
        if len(marker_corners) > 0:
            charuco_retval, charuco_corners, charuco_ids = cv.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            if charuco_retval:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)
                


    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, image.shape[:2], None, None)

    
    np.save(CAM_MATRIX_PATH, camera_matrix)
    np.save(DISTORTION_MATRIX_PATH, dist_coeffs)
    print("Calibration complete and saved")


def drawCorners(image, dictionary, board, camMatrix, distMatrix):
    """
    takes in an image with a charuco board and locates the corners of the image and adds a marker.
    outputs an image with the coners drawn on.
    """
    x_size, y_size = SIZE
    charucoPoints3D = [(0,0,0), (x_size*SQUARE_LENGTH, 0, 0), (0, y_size*SQUARE_LENGTH, 0), (x_size*SQUARE_LENGTH, y_size*SQUARE_LENGTH, 0)]

    # find corners in supplied image and get pixle position and Ids
    corners, ids, _ = cv.aruco.detectMarkers(image, dictionary)
    if len(corners) > 0:
        charucoCorners = cv.aruco.interpolateCornersCharuco(corners, ids, image, board)
        #print("\n" + str(charucoCorners) + "\n")

        # unpacks the corners into cornerLocations and Ids and tries to draw boxes
        if charucoCorners is not None and len(charucoCorners) > 0:
            charucoCornerLocations =  charucoCorners[1]
            charucoIds = charucoCorners[2]

            # Estimates pose and draws in corners

            if charucoCornerLocations is not None and len(charucoCornerLocations) > 0 and len(charucoIds) >= 6:
                ret, rvec, tvec = cv.aruco.estimatePoseCharucoBoard(charucoCornerLocations, charucoIds, board, camMatrix, distMatrix, None, None, useExtrinsicGuess= False)
                cornerArray = []
                if ret:
                    for point_3d in charucoPoints3D:
                        point_2d, _ = cv.projectPoints(point_3d, rvec, tvec, camMatrix, distMatrix)
                        #print(point_2d[0][0])
                        cornerArray.append(tuple(point_2d[0][0]))
                    
                    cornerArray = np.array(cornerArray)
                    transformedImage = transformPerspective(image, cornerArray)
                    #print(image.shape)
                    return True, transformedImage
        
        return False, image


    return False, image

def transformPerspective(image, cornerList):
    """
    takes in the image, and returns a transformed image. The transformed image
    has the located corners moved to a specifed point in the returned image.
    """

    x_length, y_length = TRANSFORMED_SIZE

    destination = np.array([(0,0), (x_length,0), (0, y_length), (x_length, y_length)])
   
    transform, mask = cv.findHomography(cornerList, destination, cv.RANSAC, 5.0)
    transformedImage = cv.warpPerspective(image, transform, (x_length, y_length))

    return transformedImage


def get_circle_position(image):
    """
    takes in an image that has had a perspective transformation and ouputs the position of a circle in the image.
    the position is grabbed with a Hough circle transform. The output is a tuple with the x and y positions in pixels.
    """
    #circles = cv.HoughCircles(image,cv.HOUGH_GRADIENT_ALT, 0.5, 100, param1 = 100, param2 = 30, minRadius = 1, maxRadius = 30)

    """Add in a filter to ensure that only the ball we are after gets returned. just for robustness. It should check all
    the possible circles and eliminate those that are too small. Also needs the parameters tuned to ensure efficency. 
    """

    return None, None


def sharpenImage(image, kernel_size=(7,7), sigma=0.25, intensity=4):
    """
    Converts to gray and sharpens the image 
    """

    # Convert image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv.GaussianBlur(gray, kernel_size, sigma)
    
    # Subtract blurred image from original
    sharpened = cv.addWeighted(gray, 1.0 + intensity, blurred, -intensity, 0)
    
    return sharpened

def main():
    """
    opens the camera and undistorts the images
    """
    try:
        camMatrix = np.load(CAM_MATRIX_PATH)
        distMatrix = np.load(DISTORTION_MATRIX_PATH)
    except:
        print('Loading calibtration files failed')
        return
    
    # load the parameters for the Charuco Board
    dictionary = cv.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv.aruco.CharucoBoard(SIZE, SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    

    # Open 
    cam = cv.VideoCapture(0) # use 1 for web cam
    print(cam.isOpened())
    frame_count = 0
    start_time = cv.getTickCount()
    fps = 0

    # run camera Loop
    while True:
        ret, frame = cam.read()

        if ret:
            
            undistorted = cv.undistort(frame, camMatrix, distMatrix)
            #undistorted = cv.medianBlur(undistorted, 5)
            undistorted_gray = sharpenImage(undistorted)

            
            #cv.imshow('Distorted Image', frame)
            if cv.waitKey(1) & 0xFF == ord('q'): 
                break
            # if cv.waitKey(1) & 0xFF == ord('c'):
            #     frame_to_display = drawCorners(undistorted_gray, dictionary, board, charucoDetector)
            #     try:
            #         cv.imshow("with ids", frame_to_display)
            #     except:
            #         cv.imshow('Undistorted Image', undistorted_gray)
            # else:
                
            #     cv.imshow('Undistorted Image', undistorted_gray)

            #current_time = time.time()
            corner_ret, frame_to_display = drawCorners(undistorted_gray, dictionary, board, camMatrix, distMatrix)
            #print("frame to display time: "  + str(current_time - time.time()))
            try:
                if frame_to_display is not None:

                    #current_time = time.time()

                    if corner_ret:
                        current_x_pos, current_y_pos = get_circle_position(frame_to_display)

                    # put frame rate on the image
                    fps_text = f"FPS: {fps:.2f}"
                    cv.putText(frame_to_display, fps_text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv.imshow("with ids", frame_to_display)  
                    cv.imshow("unsharpened", cv.cvtColor(undistorted, cv.COLOR_BGR2GRAY))
                    #print("image display time: "  + str(current_time - time.time()))
            except:
                pass
        else:
            print("camera not active")

        #Frame rate display code
        
        # Increment frame count
        frame_count += 1

        # Calculate elapsed time since the start
        end_time = cv.getTickCount()
        elapsed_time = (end_time - start_time) / cv.getTickFrequency()

        # Calculate and display FPS every 30 frames
        if frame_count % 30 == 0:
            fps = frame_count / elapsed_time
            #print(f"FPS: {fps:.2f}")

    print("Camera Released")
    cam.release()
    cv.destroyAllWindows()



            

if __name__ == '__main__':
    main()
    #saveCalibrationCameraParameters()


