# CVtask
The task is to detect all the squares in the given image and replace all those squares with aruco markers. The ids of the aruco marker should match with the marker id of the coloured of the squares.


Approach:
1. Converted original image to gray scale
2. read all the aruco markers provided
3. Rotated all the aruco markers to get proper orientation and stored the markers in a list such that the markers can directly be accessed through their respective ids  
5. found the edges in original image using canny edge detector
6. found all the contours using findcontours function
7. transversed through all the contours and detected squares
8. rotated the aruco markers according to the angle of their respective squares
9. resized all the aruco markers so that they can be fitted in the squares
10. all the squares were converted to black color
11. after a series of operations the aruco markers were placed in a black image (having same size as that of the original image) such that they are in their correct places
12. The blackened square image and the aruco image with black background was ored to get the finaal result
13. The program also detects the arucos in the final image and puts its id and angle in the image
