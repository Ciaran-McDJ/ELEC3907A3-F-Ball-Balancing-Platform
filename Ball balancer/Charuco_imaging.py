import cv2 as cv
import numpy as np
import os
from typing import Optional

"""
Module for Charuco imaging.

This module provides functions for generating and manipulating Charuco boards, saving camera calibration parameters, drawing corners on images, transforming perspective, sharpening images, and getting the position of a circle in an image.

"""


class Config:
    """
    The `Config` class represents the configuration parameters for the Charuco imaging application.

    Attributes:
    ARUCO_DICT (int): The ARUCO dictionary type.
    SIZE (tuple): The number of squares in the Charuco board.
    SQUARE_LENGTH (float): The length of each square in meters.
    MARKER_LENGTH (float): The length of each marker in meters.
    IMAGE_SIZE (tuple): The size of the generated Charuco board image.
    CALIBRATION_LOCATION (str): The location of the calibration images folder.
    CAM_MATRIX_PATH (str): The file path to save the camera matrix.
    DISTORTION_MATRIX_PATH (str): The file path to save the distortion matrix.
    TRANSFORMED_SIZE (tuple): The size of the transformed image.
    """
    ARUCO_DICT = cv.aruco.DICT_5X5_250  # ArUco dictionary to use
    SIZE = (8, 8)  # Size of the Charuco board
    SQUARE_LENGTH = 0.024  # Length of the squares in the Charuco board
    MARKER_LENGTH = 0.014  # Length of the markers in the Charuco board
    IMAGE_SIZE = (800, 800)  # Size of the image to generate
    CALIBRATION_LOCATION = 'C:/Users/trist/OneDrive/Desktop/Projects/ELEC3907A3-F-Ball-Balancing-Platform/Ball balancer/CamCalibration'  # Location of the calibration images
    CAM_MATRIX_PATH = 'C:/Users/trist\OneDrive/Desktop/Projects/ELEC3907A3-F-Ball-Balancing-Platform/Ball balancer/3camMatrix.npy'  # Path to save the camera matrix
    DISTORTION_MATRIX_PATH = 'C:/Users/trist\OneDrive/Desktop/Projects/ELEC3907A3-F-Ball-Balancing-Platform/Ball balancer/3distMatrix.npy' # Path to save the distortion matrix
    TRANSFORMED_SIZE = (480, 480)  # Size of the transformed image



def load_charuco_board() -> cv.aruco.CharucoBoard:
    """
    Load the Charuco board.

    Returns:
        cv.aruco.CharucoBoard: The loaded Charuco board.
    """
    dictionary = cv.aruco.getPredefinedDictionary(Config.ARUCO_DICT)
    return cv.aruco.CharucoBoard(Config.SIZE, Config.SQUARE_LENGTH, Config.MARKER_LENGTH, dictionary)


def generateCharucoBoard() -> None:
    """
    Generate a Charuco board image.
    """
    board = load_charuco_board()
    image = board.generateImage(Config.IMAGE_SIZE)

    cv.imshow("charuco", image)
    np.save('charucoBoard.npy', board)

    # Wait for the user to press 'q' to quit
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()


def saveCalibrationCameraParameters() -> None:
    """
    Save the camera calibration parameters.
    """

    dictionary = cv.aruco.getPredefinedDictionary(Config.ARUCO_DICT)
    board = load_charuco_board()
    params = cv.aruco.DetectorParameters()

    # Get a list of all the .jpg images in the calibration location
    images = [os.path.join(Config.CALIBRATION_LOCATION, filename) for filename in os.listdir(Config.CALIBRATION_LOCATION) if filename.endswith('.jpg')]

    all_charuco_corners = []
    all_charuco_ids = []

    # For each image, detect the markers and interpolate the Charuco corners
    for image_file in images:
        image = cv.imread(image_file)
        marker_corners, marker_ids, _ = cv.aruco.detectMarkers(image, dictionary, parameters=params)
        if len(marker_corners) > 0:
            charuco_retval, charuco_corners, charuco_ids = cv.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            if charuco_retval:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)

    # Calibrate the camera using the Charuco corners and ids
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, image.shape[:2], None, None)

    # Save the camera matrix and distortion coefficients
    np.save(Config.CAM_MATRIX_PATH, camera_matrix)
    np.save(Config.DISTORTION_MATRIX_PATH, dist_coeffs)
    print("Calibration complete and saved")


def drawCorners(image: np.ndarray, dictionary: cv.aruco.Dictionary, board: cv.aruco.CharucoBoard, camMatrix: np.ndarray, distMatrix: np.ndarray) -> tuple[bool, np.ndarray]:
    """
    Draw corners on an image.

    Args:
        image (np.ndarray): The input image.
        dictionary (cv.aruco.Dictionary): The ArUco dictionary.
        board (cv.aruco.CharucoBoard): The Charuco board.
        camMatrix (np.ndarray): The camera matrix.
        distMatrix (np.ndarray): The distortion matrix.

    Returns:
        Tuple[bool, np.ndarray]: A tuple containing a boolean indicating if the corners were successfully drawn and the resulting image.

    """
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

    # Estimate the pose of the Charuco board
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

def transformPerspective(image: np.ndarray, cornerList: np.ndarray) -> np.ndarray:
    """
    Transform the perspective of an image.

    Args:
        image (np.ndarray): The input image.
        cornerList (np.ndarray): The list of corners.

    Returns:
        np.ndarray: The transformed image.

    """

    x_length, y_length = Config.TRANSFORMED_SIZE
    destination = np.array([(0,0), (x_length,0), (0, y_length), (x_length, y_length)])
    transform, mask = cv.findHomography(cornerList, destination, cv.RANSAC, 5.0)
    return cv.warpPerspective(image, transform, (x_length, y_length))

def get_circle_position(image: np.ndarray, pixleSizeRatio: float) -> tuple[Optional[float], Optional[float]]:
    """
    Get the position of a circle in an image.

    Args:
        image (np.ndarray): The input image.

    Returns:
        Tuple[Optional[float], Optional[float]]: A tuple containing the x and y positions of the circle in meters, or None if the circle was not found.
    """
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, 200, param1=75, param2=40, minRadius=50, maxRadius=100)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            x_pos = x * pixleSizeRatio
            y_pos = y * pixleSizeRatio
            return x_pos, y_pos     
    return None, None

def sharpenImage(image: np.ndarray, kernel_size: tuple[int, int] = (7, 7), sigma: float = 0.25, intensity: int = 4) -> np.ndarray:
    """
    Sharpen an image.

    Args:
        image (np.ndarray): The input image.
        kernel_size (Tuple[int, int], optional): The size of the Gaussian kernel. Defaults to (7, 7).
        sigma (float, optional): The standard deviation of the Gaussian kernel. Defaults to 0.25.
        intensity (int, optional): The intensity of the sharpening effect. Defaults to 4.

    Returns:
        np.ndarray: The sharpened image.

    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    #blurred = cv.GaussianBlur(gray, kernel_size, sigma)
    #return cv.addWeighted(gray, 1.0 + intensity, blurred, -intensity, 0)
    return gray

def draw_center(image: np.ndarray, x: float, y: float) -> None:
    """
    Draw the center of the circle on an image.

    Args:
        image (np.ndarray): The input image.
        x (float): The x position of the circle.
        y (float): The y position of the circle.
    """
    if x is not None and y is not None:
        cv.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)


# Main function
def main() -> None:  # sourcery skip: do-not-use-bare-except
    """
    The main function.

    Raises:
        Exception: If loading calibration files fails.

    """
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
    #frame_count = 0
    #start_time = cv.getTickCount()
    #fps = 0
    pixleSizeRatio = (Config.SIZE[0]*Config.SQUARE_LENGTH) / Config.TRANSFORMED_SIZE[0]
    print(pixleSizeRatio)

    # Main loop
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
                        current_x_pos, current_y_pos = get_circle_position(frame_to_display,pixleSizeRatio)
                        print(current_x_pos, current_y_pos)


                    #cv.imshow("with ids", frame_to_display)  
            except:
                pass

    print("Camera Released")
    cam.release()
    cv.destroyAllWindows()

class Camera_Controller ():
    """
    implementation to control the collection of images from the camera and has functions to call
    """
    def __init__(self):
        self.camMatrix = np.load(Config.CAM_MATRIX_PATH)
        self.distMatrix = np.load(Config.DISTORTION_MATRIX_PATH)
        self.dictionary = cv.aruco.getPredefinedDictionary(Config.ARUCO_DICT)
        self.board = load_charuco_board()
        self.pixleSizeRatio = (Config.SIZE[0]*Config.SQUARE_LENGTH) / Config.TRANSFORMED_SIZE[0]
        self.cam = cv.VideoCapture(0)
        print(self.cam.isOpened())

    def __del__(self):
        self.cam.release()
        cv.destroyAllWindows()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.cam.release()
        cv.destroyAllWindows()


    def get_current_position(self):
        """
        this function returns the current position of the ball. It will take an image and return the balls
        x and y position in meters. 
        """
        frame = self.cam.read()
        undistorted = cv.undistort(frame, self.camMatrix, self.distMatrix)
        undistorted_gray = sharpenImage(undistorted)
        corner_ret, frame_to_display = drawCorners(undistorted_gray, self.dictionary, self.board, self.camMatrix, self.distMatrix)
        try:
            if frame_to_display is not None:
                if corner_ret:
                    current_x_pos, current_y_pos = get_circle_position(frame_to_display,self.pixleSizeRatio)
                    return (current_x_pos, current_y_pos)
                else:
                    return (None, None)
        except Exception:
            return (None, None)
        
    def display_image(self):
        """
        this function displays the image from the camera and tracks the ball position, Used for testing and demos
        """
        ret, frame = self.cam.read()
        if ret:
            undistorted = cv.undistort(frame, self.camMatrix, self.distMatrix)
            undistorted_gray = sharpenImage(undistorted)
            corner_ret, frame_to_display = drawCorners(undistorted_gray, self.dictionary, self.board, self.camMatrix, self.distMatrix)
            try:
                if frame_to_display is not None:
                    if corner_ret:
                        current_x_pos, current_y_pos = get_circle_position(frame_to_display,self.pixleSizeRatio)
                        draw_center(frame_to_display, current_x_pos, current_y_pos)
                        
                    cv.imshow("Camera View", frame_to_display)
            except:
                pass
        
        
    def release_camera(self):
        """
        this function releases the camera
        """
        self.cam.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    main()