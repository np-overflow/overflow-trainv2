# Made By Addison Chua (https://github.com/NotAddison)
# SideNote : V2 uses an estimated center dot from the coordinates of the Bondary Boxes (BBox) to determine the number of people on each side (left & right)

import cv2 as cv 
from time import time
import random
from requests import post

URL = "https://overflow-robotics-api.herokuapp.com"

# --- ⚙ OpenCV Settings ⚙ ---
class CVDestinationProvider:

    def __init__(self, loopDuration, debug = False, mirror = True, header = True):

        self.threshold = 0.55        # Main threshold for obj detection [aka, sensitivity]
        self.toMirror = mirror      # Mirrors the projected frames (Use True if you're using a webcam & Left and right are mirrored)
        self.center_offset = 100     # Offset for center dot (Note To Self: Need to fix for better accuracy) [100 if close : 200 if far]

        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.6
        self.thickness = 2
        self.bbox_color = (255,169,0)
        self.text_colour = (0,255,0)

        self.header = header;                 # Display Heaader Toggle
        self.header_scale = 1                # Header Font Scale
        self.header_thickness = 2            # Header Font Thickness
        self.header_color = (255,255,255)    # Header Font Color

        self.debug = debug;                  # Show debugging stats
        self.debug_fontScale  = 0.5          # Show debugging stats
        self.debug_thickness = 1;            # Thickness of debugging text
        self.debug_Colour = (77, 40, 225)    # Colour of debugging text

        # Load Dependency Files
        config = r'Assets\Dependencies\coco-config.pbtxt'
        frozen_model = r'Assets\Dependencies\frozen_inference_graph.pb'

        # Read Pretrained Model
        self.model = cv.dnn_DetectionModel(frozen_model, config)
        
        # Model Setup
        self.model.setInputSize(320, 320)
        self.model.setInputScale(1.0/ 127.5)
        self.model.setInputMean((127.5, 127.5, 127.5))
        self.model.setInputSwapRB(True)
        
        # Labels
        self.lables = open('coco-labels.txt', 'r').read().rstrip('\n').split('\n')
        print(f">> Loaded {len(self.lables)} classes...")


        # // -- OpenCV Read Video (frames) --
        # VideoCapture(0)       : 0 = Default Camera
        # VideoCapture(1)       : 1 = External Camera
        # VideoCapture(addr)    : addr = Path to Video File
        self.video = cv.VideoCapture(0)

        ## Checks if camera opened successfully
        if not self.video.isOpened():
            self.video = cv.VideoCapture(0)
        if not self.video.isOpened():
            raise IOError("Cannot Open Video")

        ## Webcam Settings
        self.video.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

        self.loopduration = time() + loopDuration;

    def getNextDestination(self, destinations):   

        destination1 = random.choice(destinations)
        destination2 = random.choice(destinations)

        while destination1 == destination2:
            destination2 = random.choice(destinations)

        print(f"Dest 1: {destination1} | Dest 2: {destination2}")

        looptime = time() # Time Bookmark

        while time() < self.loopduration:
            count = 0
            left_count = 0
            right_count = 0
            ret,frame = self.video.read()

            if(self.toMirror):
                frame = cv.flip(frame, 1)

            roi_left = frame[0:1280, 0:640]
            classIndex, confidence, bbox = self.model.detect(frame, self.threshold)


            # print(classIndex)
            if(len(classIndex) != 0):
                for classIndex, confidence, bbox in zip(classIndex.flatten(), confidence.flatten(), bbox):
                    if (classIndex <= 80):
                        if(self.lables[classIndex-1] == 'person'):                                                           # Filter so it displays only People
                            count +=1
                            cv.rectangle(frame, bbox, self.bbox_color, self.thickness)                                           # Draw Bounding Box
                            cv.putText(frame, self.lables[classIndex-1], (bbox[0], bbox[1]), self.font, self.font_scale, self.text_colour, 1)    # Draw Labels

                            # Bbox Tracking postiton (Using center point of Bbox)
                            # 0-> left top corner, 1-> left bottom corner, 2-> right bottom corner, 3-> right top corner

                            width = bbox[2] - bbox[1]   # Right Bottom - Left Bottom
                            width_center_coord = int((bbox[0]+ (width/2)) + self.center_offset)

                            # print(f"Width : {width} : {bbox[0]} | ", f"Center: ({width_center_coord})")
                            
                            frame = cv.circle(frame, (width_center_coord, bbox[1]), 3, (255,255,255), self.thickness)

                            if (width_center_coord > 640):
                                right_count += 1
                            else:
                                left_count += 1

            # FPS Calculation & output
            fps = (1/(time() - looptime))
            looptime = time()

            # # Display OpenCV Video Result
            frame = cv.line(frame,(640,0),(640,1000),(255,255,255),7)   # Draw Center Line
            
            if(self.header):                                                                                                                     # Toggle Headers
                frame = cv.putText(frame, f'{destination1}', (220,60), self.font, self.header_scale, self.header_color, self.header_thickness, cv.LINE_AA)             # Display Left Header
                frame = cv.putText(frame, f'{destination2}', (920,60), self.font, self.header_scale, self.header_color, self.header_thickness, cv.LINE_AA)             # Display Right Header
                
            if(self.debug):                                                                                                                      # Toggle Debug
                frame = cv.putText(frame, 'Human Detection Demo', (20,610), self.font, self.font_scale, self.debug_Colour, 1, cv.LINE_AA)                  # Display Project Name
                frame = cv.putText(frame, 'Human Detection Demo', (20,610), self.font, self.font_scale, self.debug_Colour, 1, cv.LINE_AA)                  # Display Project Name (Duplicated for opacity bold)
                frame = cv.putText(frame, f'FPS: {fps}', (20,640), self.font, self.debug_fontScale, self.debug_Colour, 1, cv.LINE_AA)                      # Display FPS Count
                frame = cv.putText(frame, f'Left Count: {left_count}', (20,670), self.font, self.debug_fontScale, self.debug_Colour, 1, cv.LINE_AA)        # Display Left Count
                frame = cv.putText(frame, f'Right Count: {right_count}', (20,700), self.font, self.debug_fontScale, self.debug_Colour, 1, cv.LINE_AA)      # Display Right Count
                frame = cv.putText(frame, f'Timer: Xs', (1130,700), self.font, self.debug_fontScale, self.debug_Colour, 1, cv.LINE_AA)                     # Display Timer


            cv.imshow(f'Human Detection', frame)
            if cv.waitKey(1) == 27: 
                break 

        self.video.release()
        cv.destroyAllWindows()

        return destination1 if left_count > right_count else destination2 

provider = CVDestinationProvider(7) #Number is duration CV will run for
destination = provider.getNextDestination(["Jurong East", "Woodlands", "Bishan", "Botanic Gardens", "Buona Vista", "Clementi", "Haw Par Villa", "HarbourFront", "City Hall", "Orchard", "Serangoon", "Paya Lebar", "Changi", "Esplanade", "Marina Bay"])

print(destination)

postData = {'Destination' : destination}
print(post(URL, data = postData).text)