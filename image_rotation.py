import cv2
from math import sin, cos, radians, ceil
import numpy as np

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def print(self):
        print(f"{self.x} , {self.y}")

class BoundingBox:
    def __init__(self):
        self.minCorner = Point()
        self.maxCorner = Point()
        self.valid = False
    
    def add(self, p : Point):
        if not self.valid:
            self.minCorner = Point(p.x, p.y)
            self.maxCorner = Point(p.x, p.y)
            self.valid = True
        else:
            if p.x < self.minCorner.x:
                self.minCorner.x = p.x
            
            if p.y < self.minCorner.y:
                self.minCorner.y = p.y

            if p.x > self.maxCorner.x:
                self.maxCorner.x = p.x
            
            if p.y > self.maxCorner.y:
                self.maxCorner.y = p.y
    
    def print(self):
        print(f"box: {self.minCorner.print()}, {self.maxCorner.print()}")

def rotate_point(point : Point, center : Point, deg : float):
    rad = radians(deg)

    result = Point()

    result.x = center.x + (center.x - point.x)*cos(rad) + (center.y - point.y)*sin(rad)
    result.y = center.y + (center.x - point.x)*sin(rad) - (center.y - point.y)*cos(rad)

    return result

def check_boundary(value : int, min_value : int, max_value : int):
    if value < min_value:
        return False
    elif value > max_value:
        return False
    
    return True

def rotation_image(filename : str, rotation_name : str, deg : float):
    input_image = cv2.imread(filename)
    (h, w) = input_image.shape[:2]

    bbox = BoundingBox()
    center = Point(w//2, h//2)
    center.print()
    bbox.add(rotate_point(Point(0,0), center, deg))
    bbox.add(rotate_point(Point(w,0), center, deg))
    bbox.add(rotate_point(Point(w,h), center, deg))
    bbox.add(rotate_point(Point(0,h), center, deg))

    new_w = ceil(bbox.maxCorner.x - bbox.minCorner.x)
    new_h = ceil(bbox.maxCorner.y - bbox.minCorner.y)

    output_image = np.zeros((new_h + 1, new_w + 1, 3), dtype = np.uint8)

    print((new_h, new_w, 3))

    center = Point(w//2, h//2)
    for row in range(new_h):
        for col in range(new_w):
            p = Point(col + bbox.minCorner.x, row + bbox.minCorner.y)
            new_p = rotate_point(p, center, deg)
            if check_boundary(int(new_p.x), 0, w-1) and check_boundary(int(new_p.y), 0, h-1):
                old_row = int(new_p.x)
                old_col = int(new_p.y)
                k = input_image[old_col, w - 1 - old_row]
                output_image[row, col] = k
            else:
                 output_image[row, col] = [255//2, 255//2, 255//2]
    
    cv2.imwrite(rotation_name, output_image)

