import cv2


from geomutils import centroid

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)

class Detector:

    def __init__(self, cameraid: int, aruco_dict = ARUCO_DICT):
        self.cam = cv2.VideoCapture(cameraid)
        self.aruco_dict = aruco_dict

    def get_markers(self):
        ret, frame = self.cam.read()
        frame = frame[64:-64]
        corners, ids, rejected = cv2.aruco.detectMarkers(frame, self.aruco_dict)
        if len(corners) > 0:
            return frame, [{
                "id": int(id_),
                "p": centroid(list(corner.flatten())),
                "corners": list(corner.flatten())}
                    for (id_, corner) in zip(ids, corners)
                ]
        else:
            return frame, []

    def cleanup(self):
        self.cam.release()
