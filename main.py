from display import *
from draw import *
from parser_s import *
from matrix import *
import math

screen = new_screen()
zbuffer = new_zbuffer()
color = [ 0, 255, 0 ]
edges = []
polygons = []
t = new_matrix()
ident(t)
csystems = [ t ]


parse_file( 'backup', edges, polygons, csystems, screen, zbuffer, color )
