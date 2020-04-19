from display import *
from matrix import *
from gmath import *
import random


# def scanline_convert(polygons, i, screen, zbuffer, color ):
#     p0 = polygons[i]
#     p1 = polygons[i + 1]
#     p2 = polygons[i + 2]
#     if (p0[1] > p1[1] and p0[1] > p2[1]):
#         top = p0
#         if(p1[1] > p2[1]):
#             mid = p1
#             bot = p2
#         else:
#             mid = p2
#             bot = p1
#     elif (p1[1] > p0[0] and p1[1] > p2[1]):
#         top = p1
#         if(p0[1] > p2[1]):
#             mid = p0
#             bot = p2
#         else:
#             mid = p2
#             bot = p0
#     else:
#         top = p2
#         if(p0[1] > p1[1]):
#             mid = p0
#             bot = p1
#         else:
#             mid = p1
#             bot = p0
#     x0 = int(bot[0])
#     x1 = int(bot[0])
#     y0 = int(bot[1])
#     dx0 = 0
#     dx1 = 0
#     dx1_1 = 0
#     if(top[1] - bot[1] != 0):
#         dx0 = int((top[0] - bot[0]) / (top[1] - bot[1]))
#     if(mid[1] - bot[1] != 0):
#         dx1 = int((mid[0] - bot[0]) / (mid[1] - bot[1]))
#     if(top[1] - mid[1] != 0):
#         dx1_1 = int((top[0] - mid[0]) / (top[1] - mid[1]))
#     y = y0
#     while (y < top[1]):
#         draw_line(int(x0), int(y), 0, int(x1), int(y), 0, screen, zbuffer, color)
#         x0 += dx0
#         x1 += dx1
#         y += 1
#         if y >= mid[1]:
#             dx1 = dx1_1
#             x1 = mid[0]
def scanline_convert(polygons, i, screen, zbuffer, color ):
    p1 = polygons[i]
    p2 = polygons[i+1]
    p3 = polygons[i+2]

    #find the top middle bottom points
    if(p1[1] >= p2[1] and p1[1] >= p3[1]):
        top = p1
        if(p2[1] > p3[1]):
            middle = p2
            bottom = p3
        else:
            middle = p3
            bottom = p2
    elif(p2[1] >= p1[1] and p2[1] >= p3[1]):
        top = p2
        if(p1[1] > p3[1]):
            middle = p1
            bottom = p3
        else:
            middle = p3
            bottom = p1
    else:
        top = p3
        if(p1[1] > p2[1]):
            middle = p1
            bottom = p2
        else:
            middle = p2
            bottom = p1
    #print([bottom[1], middle[1], top[1]])

    #initial setup
    x0 = bottom[0]
    x1 = bottom[0]
    z0 = bottom[2]
    z1 = bottom[2]
    y = int(bottom[1])
    #print([x0, x1, y])

    #find x slopes
    dx0 = (top[0]-bottom[0])/(top[1]-bottom[1])
    if(middle[1] - bottom[1] != 0):
        dx1 = (middle[0]-bottom[0])/(middle[1]-bottom[1])
    else:
        dx1 = None
    if(top[1] - middle[1] != 0):
        dx1_1 = (top[0]-middle[0])/(top[1]-middle[1])
    else:
        dx1_1 = None

    #find z slopes
    dz0 = (top[2]-bottom[2])/(top[1]-bottom[1])
    if(middle[1] - bottom[1] != 0):
        dz1 = (middle[2]-bottom[2])/(middle[1]-bottom[1])
    else:
        dz1 = None
    if(top[1] - middle[1] != 0):
        dz1_1 = (top[2]-middle[2])/(top[1]-middle[1])
    else:
        dz1_1 = None
    #print([dx0, dx1, dx1_1])
    color = [random.randint(0, 255), random.randint(0, 255),random.randint(0, 255)]
    # color = [0, random.randint(0, 255),0]


    while(y < middle[1]):
        #draw horizontal line
        #print([x0, x1])
        if((x1 <= top[0] or x1 <= middle[0] or x1 <= bottom[0]) and (x0 >= top[0] or x0 >= middle[0] or x0 >= bottom[0])):
            draw_scanline(screen, zbuffer, color, int(x0), int(x1), y, z0, z1)
        #move endpoints
        if(dx0 != None):
            x0 += dx0
        if(dx1 != None):
            x1 += dx1
        if(dz0 != None):
            z0 += dz0
        if(dz1 != None):
            z1 += dz1
        y += 1
    x1 = middle[0]
    z1 = middle[2]
    y = int(middle[1])
    dx1 = dx1_1
    dz1 = dz1_1
    while(y <= top[1]):
        #draw horizontal line
        #print([x0, x1])
        if((x1 <= top[0] or x1 <= middle[0] or x1 <= bottom[0]) and (x0 >= top[0] or x0 >= middle[0] or x0 >= bottom[0])):
            draw_scanline(screen, zbuffer, color, int(x0), int(x1), y, z0, z1)
        #move endpoints
        if(dx0 != None):
            x0 += dx0
        if(dx1 != None):
            x1 += dx1
        y += 1

def draw_scanline(screen, zbuffer, color, x0, x1, y, z0, z1):
    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        zt = z0
        x0 = x1
        z0 = z1
        x1 = xt
        z1 = zt

    x = x0
    z = z0
    if(x1 - x0 != 0):
        dz = (z1 - z0) / (x1 - x0)
    else:
        dz = None

    while(x <= x1):
        plot( screen, zbuffer, color, x, y, z )
        x += 1
        if(dz != None):
            z += dz


def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, color ):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return

    point = 0
    while point < len(polygons) - 2:

        normal = calculate_normal(polygons, point)[:]
        #print normal
        if normal[2] > 0:
            scanline_convert(polygons, point, screen, zbuffer, color)
            draw_line( int(polygons[point][0]),
                       int(polygons[point][1]),
                       polygons[point][2],
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       polygons[point+1][2],
                       screen, zbuffer, color)
            draw_line( int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       polygons[point+2][2],
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       polygons[point+1][2],
                       screen, zbuffer, color)
            draw_line( int(polygons[point][0]),
                       int(polygons[point][1]),
                       polygons[point][2],
                       int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       polygons[point+2][2],
                       screen, zbuffer, color)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        z1 = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        if(x1 - x0 != 0):
            d_z = (z1 - z0) / (x1 - x0)
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            d_z = (z1 - z0) / (y1 - y0)
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, 0 )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z+1 )
