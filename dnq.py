from matplotlib import pyplot as plt
from sympy import pi, atan2
from sympy.geometry import *
from util import *
from display import *

# Find rightmost point
def index_of_right_most_point(points):
    x_values = [point.x for point in points]
    max_x_values = max(x_values)
    max_x_values_idx = x_values.index(max_x_values)
    return max_x_values_idx


# Find leftmost point
def index_of_left_most_point(points):
    x_values = [point.x for point in points]
    min_x_values = min(x_values)
    min_x_values_idx = x_values.index(min_x_values)
    return min_x_values_idx

# Find upper tangent of two convex hulls
def get_upper_tangent(left_convex_hull, right_convex_hull):
    left_len = len(left_convex_hull)
    right_len = len(right_convex_hull)
    left_index = index_of_right_most_point(left_convex_hull)
    right_index = index_of_left_most_point(right_convex_hull)
    flag = True
    while flag:
        flag = False
        temp = left_convex_hull
        while temp:
            tangent = Segment(left_convex_hull[left_index],right_convex_hull[right_index])
            a,b,c = Line(tangent).coefficients
            temp_new = []
            for p in temp:
                if b != 0:
                    if b * (a * p.x + b * p.y + c) > 0:
                        temp_new.append(p)
                else:
                    if p.x == left_convex_hull[left_index].x:
                        if p.y > left_convex_hull[left_index].y:
                            temp_new.append(p)
            temp = temp_new
            if temp:
                left_index = (left_index-1) % left_len
                flag = True
        temp = right_convex_hull
        while temp:
            tangent = Segment(left_convex_hull[left_index],right_convex_hull[right_index])
            a,b,c = Line(tangent).coefficients
            temp_new = []
            for p in temp:
                if b != 0:
                    if (b*(a*p.x + b*p.y +c)) > 0:
                        temp_new.append(p)
                else:
                    if p.x == right_convex_hull[right_index].x:
                        if p.y < right_convex_hull[right_index].y:
                            temp_new.append(p)
            temp = temp_new
            if temp:
                right_index = (right_index+1) % right_len
                flag = True
    return tangent

# Find highest intersection point between the perpendicular bisector and edges of the voronoi diagram
def highest_intersection_point(line, voronoi_dict):
    result = None
    point_of_intersection = None
    for key, value in voronoi_dict.items():
        intersection = value.intersection(line)
        if intersection:
            if isinstance(intersection[0], Point2D):
                topmost_point = intersection[0]
            elif isinstance(intersection[0], Ray2D): 
                topmost_point = intersection[0].source
            elif isinstance(intersection[0], Segment2D):
                if (intersection[0].p1.y>intersection[0].p2.y or (intersection[0].p1.y==intersection[0].p2.y and intersection[0].p1.x<intersection[0].p2.x)):
                    topmost_point = intersection[0].p1 
                else:
                    topmost_point = intersection[0].p2
            else:
                continue
            if (result == None or (topmost_point.y>point_of_intersection.y or (topmost_point.x<point_of_intersection.x and (topmost_point.y==point_of_intersection.y)))):
                result = key
                point_of_intersection = topmost_point
    return result, point_of_intersection

# Check if point lies to the left of two intersecting lines
def left(bisecting_lines, point):
    if point.y >= bisecting_lines[0][1].source.y:
        start = 0
    elif point.y <= bisecting_lines[-1][1].source.y:
        start = -1
    else:
        start = 1
        end = len(bisecting_lines) - 1
        while(start<end):
            mid = int((start+end)/2)
            y_max = max(bisecting_lines[mid][1].p1.y, bisecting_lines[mid][1].p2.y)
            y_min = min(bisecting_lines[mid][1].p1.y, bisecting_lines[mid][1].p2.y)
            if(point.y <= y_max and point.y >= y_min):
                start = mid
                break
            elif (point.y > y_max):
                end = mid
            else:
                start = mid+1
    a,b,c = Line2D(bisecting_lines[start][1]).coefficients
    if a == 0:
        x_min = min(bisecting_lines[start][1].p1.x, bisecting_lines[start][1].p2.x)
        return point.x <= x_min
    else:
        x_on_line = (-c - b*point.y)/a
        return point.x <= x_on_line

# Merge voronoi diagrams
def merge(left_voronoi, right_voronoi, bisecting_lines):
    voronoi_dict = dict((each[0], each[1]) for each in bisecting_lines)
    flag = (len(bisecting_lines) == 1)
    for k, v in left_voronoi.items():
        if flag or (left(bisecting_lines, v.p1) and left(bisecting_lines, v.p2)):
            voronoi_dict[k] = v
    for k, v in right_voronoi.items():
        if flag or (not left(bisecting_lines, v.p1)) or (not left(bisecting_lines, v.p2)):
            voronoi_dict[k] = v
    return voronoi_dict

# Compute voronoi diagram
def vor(points):
    n = len(points)
    if n == 1:
        return {},[points[0],]
    if points[0].x == points[-1].x or n <= 2:
        return {(points[i], points[i+1]) : Segment(points[i], points[i+1]).perpendicular_bisector() for i in range(n-1)},[points[0], points[-1]]

    left_len = int(n/2)
    right_len = n - left_len
    left_voronoi, left_convex_hull = vor(points[:left_len])
    right_voronoi, right_convex_hull = vor(points[left_len:])
    tangent = get_upper_tangent(left_convex_hull,right_convex_hull)
    upper_tangent = tangent
    bisecting_line = tangent.perpendicular_bisector()
    # print(bisecting_line)
    if atan2(bisecting_line.direction.y,bisecting_line.direction.x) > 0:
        bisecting_line=Line2D(bisecting_line.p2,bisecting_line.p1)
    left_key, left_poi = highest_intersection_point(bisecting_line,left_voronoi)
    right_key, right_poi = highest_intersection_point(bisecting_line,right_voronoi)
    temp_poi=None
    left_poi_lines={}
    right_poi_lines={}
    bisecting_lines=[]
    while left_poi or right_poi:
        if left_poi and right_poi:
            if left_poi.y>right_poi.y or (left_poi.y==right_poi.y and left_poi.x<=right_poi.x):
                poi, intersection_key, intersection_line = left_poi,left_key,left_voronoi[left_key]
                del left_voronoi[left_key]
            else:
                poi, intersection_key, intersection_line = right_poi,right_key,right_voronoi[right_key]
                del right_voronoi[right_key]
        elif left_poi:
            poi, intersection_key, intersection_line = left_poi,left_key,left_voronoi[left_key]
            del left_voronoi[left_key]
        else:
            poi,intersection_key,intersection_line = right_poi,right_key,right_voronoi[right_key]
            del right_voronoi[right_key]

        if(poi != temp_poi):
            temp_poi = poi
            for k,v in left_poi_lines.items():
                left_voronoi[k] = v
            for k,v in right_poi_lines.items():
                right_voronoi[k] = v
            left_poi_lines.clear()
            right_poi_lines.clear()

        if isinstance(bisecting_line, Line2D):
            bisecting_lines.append(((tangent.p1,tangent.p2), Ray(poi,poi-bisecting_line.direction)))
        elif isinstance(Segment(poi,bisecting_line.source), Segment2D):
            bisecting_lines.append(((tangent.p1,tangent.p2), Segment(poi,bisecting_line.source)))

        l1 = Ray(poi, poi+intersection_line.direction)
        left_l1 = (atan2(l1.direction.y,l1.direction.x) - atan2(bisecting_line.direction.y,bisecting_line.direction.x))
        while left_l1 > pi:	
            left_l1 -= 2*pi
        while left_l1 <= -pi:	
            left_l1 += 2*pi
        left_l1 = (left_l1 <= 0)

        if left_l1 == (poi == left_poi):
            if isinstance(intersection_line,Segment2D):
                l1 = Segment(poi,intersection_line.p2)
        else:
            if isinstance(intersection_line,Line2D):
                l1 = Ray(poi,poi-intersection_line.direction)
            elif isinstance(intersection_line,Ray2D):
                l1 = Segment(poi,intersection_line.source)
            else:
                l1 = Segment(poi,intersection_line.p1)

        if poi == left_poi:
            if not isinstance(l1,Point2D):
                left_poi_lines[intersection_key]=l1
            tangent = Segment(intersection_key[0] if tangent.p1 == intersection_key[1] else intersection_key[1],tangent.p2)
        else:
            if not isinstance(l1,Point2D):
                right_poi_lines[intersection_key]=l1
            tangent = Segment(tangent.p1,intersection_key[0] if tangent.p2 == intersection_key[1] else intersection_key[1])
        bisecting_line = tangent.perpendicular_bisector()
        if atan2(bisecting_line.direction.y,bisecting_line.direction.x)<=0:
            bisecting_line = Ray(poi,poi+bisecting_line.direction)
        else:
            bisecting_line = Ray(poi,poi-bisecting_line.direction)

        left_key,left_poi = highest_intersection_point(bisecting_line,left_voronoi)
        right_key,right_poi = highest_intersection_point(bisecting_line,right_voronoi)
    
    # print(left_poi_lines)
    # print(right_poi_lines)
    for k, v in left_poi_lines.items():
        left_voronoi[k]=v
    for k,v in right_poi_lines.items():
        right_voronoi[k]=v

    bisecting_lines.append(((tangent.p1,tangent.p2),bisecting_line))
    voronoi_dict = merge(left_voronoi,right_voronoi,bisecting_lines)
    lower_tangent = tangent

    print(left_convex_hull)
    print(right_convex_hull)
    left_len = len(left_convex_hull)
    right_len = len(right_convex_hull)
    lcu = left_convex_hull.index(upper_tangent.p1)
    lcl = left_convex_hull.index(lower_tangent.p1)
    rcu = right_convex_hull.index(upper_tangent.p2)
    rcl = right_convex_hull.index(lower_tangent.p2)
    
    left_convex_hull = left_convex_hull[lcl:lcu+1] if lcu>=lcl else left_convex_hull[lcl:]+left_convex_hull[:lcu+1]
    right_convex_hull = right_convex_hull[rcu:rcl+1] if rcu<=rcl else right_convex_hull[rcu:]+right_convex_hull[:rcl+1]

    # print(voronoi_dict,left_convex_hull, right_convex_hull)
    return voronoi_dict, left_convex_hull+right_convex_hull

# Main function
def voronoi(points, bound):
    points.sort(key = lambda p: [p.x,p.y])
    voronoi_dict = vor(points)
    # print(voronoi_dict)
    display_dnq(voronoi_dict, points, bound)


# if __name__=="__main__":
# 	bound = 10
# 	points = [Point(1, 1), Point(2, 3), Point(5, 4), Point(3, 5), Point(4, 2)]
# 	voronoi_dict,convex_hull = voronoi(points)
# 	display(voronoi_dict, points, bound)
    