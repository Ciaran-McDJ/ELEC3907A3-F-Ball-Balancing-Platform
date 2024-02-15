import cv2 as cv
import numpy as np
import os

class Config:
    ARUCO_DICT = cv.aruco.DICT_5X5_250
    SIZE = (8, 8)
    SQUARE_LENGTH = 0.024
    MARKER_LENGTH = 0.014
    IMAGE_SIZE = (800, 800)
    CALIBRATION_LOCATION = 'C:/Users/trist/OneDrive/Desktop/Projects/ELEC3907A3-F-Ball-Balancing-Platform/Ball balancer/CamCalibration'
    CAM_MATRIX_PATH = 'C:/Users/trist/OneDrive/Desktop/Projects/ELEC3907A3-F-Ball-Balancing-Platform/Ball balancer/3camMatrix.npy'
    DISTORTION_MATRIX_PATH = 'C:/Users/trist/OneDrive/Desktop/Projects/ELEC3907A3-F-Ball-Balancing-Platform/Ball balancer/3distMatrix.npy'
    TRANSFORMED_SIZE = (480, 480)

def load_charuco_board():
    dictionary = cv.aruco.getPredefinedDictionary(Config.ARUCO_DICT)
    return cv.aruco.CharucoBoard(Config.SIZE, Config.SQUARE_LENGTH, Config.MARKER_LENGTH, dictionary)

def generateCharucoBoard():
    board = load_charuco_board()
    image = board.generateImage(Config.IMAGE_SIZE)

    cv.imshow("charuco", image)
    np.save('charucoBoard.npy', board)

    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def saveCalibrationCameraParameters():
    dictionary = cv.aruco.getPredefinedDictionary(Config.ARUCO_DICT)
    board = load_charuco_board()
    params = cv.aruco.DetectorParameters()

    images = [os.path.join(Config.CALIBRATION_LOCATION, filename) for filename in os.listdir(Config.CALIBRATION_LOCATION) if filename.endswith('.jpg')]

    all_charuco_corners = []
    all_charuco_ids = []

    for image_file in images:
        image = cv.imread(image_file)
        marker_corners, marker_ids, _ = cv.aruco.detectMarkers(image, dictionary, parameters=params)
        if len(marker_corners) > 0:
            charuco_retval, charuco_corners, charuco_ids = cv.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            if charuco_retval:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)

    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, image.shape[:2], None, None)

    np.save(Config.CAM_MATRIX_PATH, camera_matrix)
    np.save(Config.DISTORTION_MATRIX_PATH, dist_coeffs)
    print("Calibration complete and saved")

def drawCorners(image, dictionary, board, camMatrix, distMatrix):
    x_size, y_size = Config.SIZE
    charucoPoints3D = [(0,0,0), (x_size*Config.SQUARE_LENGTH, 0, 0), (0, y_size*Config.SQUARE_LENGTH, 0), (x_size*Config.SQUARE_LENGTH, y_size*Config.SQUARE_LENGTH, 0)]

    corners, ids, _ = cv.aruco.detectMarkers(image, dictionary)
    if len(corners) == 0:
        return False, image

    charucoCorners = cv.aruco.interpolateCornersCharuco(corners, ids, image, board)
    if charucoCorners is None or len(charucoCorners) == 0:
        return False, image

    charucoCornerLocations = charucoCorners[1]
    charucoIds = charucoCorners[2]

    if charucoCornerLocations is None or len(charucoCornerLocations) == 0 or len(charucoIds) < 6:
        return False, image

    ret, rvec, tvec = cv.aruco.estimatePoseCharucoBoard(charucoCornerLocations, charucoIds, board, camMatrix, distMatrix, None, None, useExtrinsicGuess=False)
    cornerArray = []
    if ret:
        for point_3d in charucoPoints3D:
            point_2d, _ = cv.projectPoints(point_3d, rvec, tvec, camMatrix, distMatrix)
            cornerArray.append(tuple(point_2d[0][0]))

        cornerArray = np.array(cornerArray)
        transformedImage = transformPerspective(image, cornerArray)
        return True, transformedImage

    return False, image

def transformPerspective(image, cornerList):
    x_length, y_length = Config.TRANSFORMED_SIZE
    destination = np.array([(0,0), (x_length,0), (0, y_length), (x_length, y_length)])
    transform, mask = cv.findHomography(cornerList, destination, cv.RANSAC, 5.0)
    transformedImage = cv.warpPerspective(image, transform, (x_length, y_length))
    return transformedImage

def get_circle_position(image):
    return None, None

def sharpenImage(image, kernel_size=(7,7), sigma=0.25, intensity=4):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, kernel_size, sigma)
    sharpened = cv.addWeighted(gray, 1.0 + intensity, blurred, -intensity, 0)
    return sharpened

def main():
    try:
        camMatrix = np.load(Config.CAM_MATRIX_PATH)
        distMatrix = np.load(Config.DISTORTION_MATRIX_PATH)
    except:
        print('Loading calibration files failed')
        return

    dictionary = cv.aruco.getPredefinedDictionary(Config.ARUCO_DICT)
    board = load_charuco_board()

    cam = cv.VideoCapture(0)
    print(cam.isOpened())
    frame_count = 0
    start_time = cv.getTickCount()
    fps = 0

    while True:
        ret, frame = cam.read()

        if ret:
            undistorted = cv.undistort(frame, camMatrix, distMatrix)
            undistorted_gray = sharpenImage(undistorted)

            if cv.waitKey(1) & 0xFF == ord('q'): 
                break

            corner_ret, frame_to_display = drawCorners(undistorted_gray, dictionary, board, camMatrix, distMatrix)
            try:
                if frame_to_display is not None:
                    if corner_ret:
                        current_x_pos, current_y_pos = get_circle_position(frame_to_display)

                    fps_text = f"FPS: {fps:.2f}"
                    cv.putText(frame_to_display, fps_text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv.imshow("with ids", frame_to_display)  
                    cv.imshow("unsharpened", cv.cvtColor(undistorted, cv.COLOR_BGR2GRAY))
            except:
                pass

        frame_count += 1
        end_time = cv.getTickCount()
        elapsed_time = (end_time - start_time) / cv.getTickFrequency()

        if frame_count % 30 == 0:
            fps = frame_count / elapsed_time

    print("Camera Released")
    cam.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
