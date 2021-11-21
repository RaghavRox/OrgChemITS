import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pylsd import lsd
 

def process_lines(image_src):
    img = cv2.imread(image_src)
    img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    thresh1 = cv2.bitwise_not(thresh1)

    lines = lsd(gray, scale=0.5)
    lines = [x[:-1] for x in lines]
    for i in range(len(lines)):
        lines[i] = [int(x) for x in lines[i]]

    _lines = []
    for _line in lines:
        _lines.append([(_line[0], _line[1]), (_line[2], _line[3])])

    # sort
    _lines_x = []
    _lines_y = []
    for line_i in _lines:
        orientation_i = math.atan2(
            (line_i[0][1]-line_i[1][1]), (line_i[0][0]-line_i[1][0]))
        if (abs(math.degrees(orientation_i)) > 45) and abs(math.degrees(orientation_i)) < (90+45):
            _lines_y.append(line_i)
        else:
            _lines_x.append(line_i)

    _lines_x = sorted(_lines_x, key=lambda _line: _line[0][0])
    _lines_y = sorted(_lines_y, key=lambda _line: _line[0][1])

    merged_lines_x = merge_lines_pipeline_2(_lines_x)
    merged_lines_y = merge_lines_pipeline_2(_lines_y)

    merged_lines_all = []
    merged_lines_all.extend(merged_lines_x)
    merged_lines_all.extend(merged_lines_y)

    
    merged_lines_all = [x for x in merged_lines_all if is_short_line(x, 30)]    
# joining paralell lines
    extra_lines = []
    tresh = 30
    for i in range(len(merged_lines_all)):
        for j in range(i):
            if i != j:
                if not is_short_line([merged_lines_all[i][0]]+[merged_lines_all[j][0]], tresh) and not is_short_line([merged_lines_all[i][1]]+[merged_lines_all[j][1]], tresh):
                    extra_lines.append(merged_lines_all[i])
                    extra_lines.append(merged_lines_all[j])
                    new_first_point = (int((merged_lines_all[i][0][0]+merged_lines_all[j][0][0])/2), int(
                        (merged_lines_all[i][0][1]+merged_lines_all[j][0][1])/2))
                    new_second_point = (int((merged_lines_all[i][1][0]+merged_lines_all[j][1][0])/2), int(
                        (merged_lines_all[i][1][1]+merged_lines_all[j][1][1])/2))
                    merged_lines_all.append(
                        [new_first_point, new_second_point])

    for line in extra_lines:
        try:
            merged_lines_all.remove(line)
        except:
            pass
    ####
    # Removing / joiing nearby points
    for i in range(len(merged_lines_all)):
        for j in range(i):
            if i != j:
                for p in range(2):
                    for q in range(2):

                        if not is_short_line([merged_lines_all[i][p]]+[merged_lines_all[j][q]], 50):
                            new_cord = joining_points(
                                merged_lines_all[i][p], merged_lines_all[j][q])
                            merged_lines_all[i][p] = new_cord
                            merged_lines_all[j][q] = new_cord
    ####
    
    
    # Splitting Lines

    ####
    
    
    
    new_img = np.zeros((600, 800, 3), dtype = "uint8")
    new_img[:,:] = (255,255,255)  
    for line in merged_lines_all:
        cv2.line(new_img, (line[0][0], line[0][1]),
                 (line[1][0], line[1][1]), (0, 0, 255), 1)
    new_name=image_src.split('.jpg')[0]+"_converted.jpg"
    cv2.imwrite(new_name, new_img)
    """cv2.imshow('prediction/lines_lines.jpg', img)
    cv2.imshow('prediction/merged_lines.jpg', img_merged_lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    return [new_name ,[list(x[0]+x[1]) for x in merged_lines_all]]
     


def joining_points(cord1, cord2):
    return (int((cord1[0]+cord2[0])/2), int((cord1[1]+cord2[1])/2))


def is_short_line(cords, limit):
    (x1, y1), (x2, y2) = cords
    return math.hypot(x2-x1, y2-y1) > limit


def merge_lines_pipeline_2(lines):
    super_lines_final = []
    super_lines = []
    min_distance_to_merge = 11
    min_angle_to_merge = 11

    for line in lines:
        create_new_group = True
        group_updated = False

        for group in super_lines:
            for line2 in group:
                if get_distance(line2, line) < min_distance_to_merge:
                    # check the angle between lines
                    orientation_i = math.atan2(
                        (line[0][1]-line[1][1]), (line[0][0]-line[1][0]))
                    orientation_j = math.atan2(
                        (line2[0][1]-line2[1][1]), (line2[0][0]-line2[1][0]))

                    if int(abs(abs(math.degrees(orientation_i)) - abs(math.degrees(orientation_j)))) < min_angle_to_merge:

                        group.append(line)

                        create_new_group = False
                        group_updated = True
                        break

            if group_updated:
                break

        if (create_new_group):
            new_group = []
            new_group.append(line)

            for idx, line2 in enumerate(lines):
                # check the distance between lines
                if get_distance(line2, line) < min_distance_to_merge:
                    # check the angle between lines
                    orientation_i = math.atan2(
                        (line[0][1]-line[1][1]), (line[0][0]-line[1][0]))
                    orientation_j = math.atan2(
                        (line2[0][1]-line2[1][1]), (line2[0][0]-line2[1][0]))

                    if int(abs(abs(math.degrees(orientation_i)) - abs(math.degrees(orientation_j)))) < min_angle_to_merge:

                        new_group.append(line2)

                        # remove line from lines list

            # append new group
            super_lines.append(new_group)

    for group in super_lines:
        super_lines_final.append(merge_lines_segments1(group))

    return super_lines_final


def merge_lines_segments1(lines, use_log=False):
    if(len(lines) == 1):
        return lines[0]

    line_i = lines[0]

    # orientation
    orientation_i = math.atan2(
        (line_i[0][1]-line_i[1][1]), (line_i[0][0]-line_i[1][0]))

    points = []
    for line in lines:
        points.append(line[0])
        points.append(line[1])

    if (abs(math.degrees(orientation_i)) > 45) and abs(math.degrees(orientation_i)) < (90+45):

        # sort by y
        points = sorted(points, key=lambda point: point[1])

        if use_log:
            print("use y")
    else:

        # sort by x
        points = sorted(points, key=lambda point: point[0])

        if use_log:
            print("use x")

    return [points[0], points[len(points)-1]]


def lines_close(line1, line2):
    dist1 = math.hypot(line1[0][0] - line2[0][0], line1[0][0] - line2[0][1])
    dist2 = math.hypot(line1[0][2] - line2[0][0], line1[0][3] - line2[0][1])
    dist3 = math.hypot(line1[0][0] - line2[0][2], line1[0][0] - line2[0][3])
    dist4 = math.hypot(line1[0][2] - line2[0][2], line1[0][3] - line2[0][3])

    return (min(dist1, dist2, dist3, dist4) < 5)


def lineMagnitude(x1, y1, x2, y2):
    return  math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


def DistancePointLine(px, py, x1, y1, x2, y2):
    LineMag = lineMagnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):

        ix = lineMagnitude(px, py, x1, y1)
        iy = lineMagnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = lineMagnitude(px, py, ix, iy)

    return DistancePointLine


def get_distance(line1, line2):
    dist1 = DistancePointLine(line1[0][0], line1[0][1],
                              line2[0][0], line2[0][1], line2[1][0], line2[1][1])
    dist2 = DistancePointLine(line1[1][0], line1[1][1],
                              line2[0][0], line2[0][1], line2[1][0], line2[1][1])
    dist3 = DistancePointLine(line2[0][0], line2[0][1],
                              line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    dist4 = DistancePointLine(line2[1][0], line2[1][1],
                              line1[0][0], line1[0][1], line1[1][0], line1[1][1])

    return min(dist1, dist2, dist3, dist4)


print(process_lines("test47.jpg"))