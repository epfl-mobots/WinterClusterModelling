from processing_py import *
from matplotlib.colors import hsv_to_rgb

SIZE_BEE = 5

def init_world(app):
    app.background(0,0,0)

def get_color(temp):
    hue = 0
    return hsv_to_rgb([hue,1,1])

def init_temp(app,hive):
    grid_res = [app.width/hive.temp.dims[1],app.height/hive.temp.dims[0]]

    for i in range(hive.temp.dims[0]):
        for j in range(hive.temp.dims[1]):
            color = get_color(hive.temp.field[i,j])
            x = j*grid_res[0]
            y = app.height - i*grid_res[1]
            app.fill(color)
            app.rect(x,y,grid_res[0],grid_res[1])



def init_colony(app,hive):
    for b in hive.colony:
        x_draw = b.x*app.width/hive.dims_b[0]
        y_draw = b.y*app.height/hive.dims_b[1]
        app.ellipse(x_draw,y_draw,SIZE_BEE,SIZE_BEE)
    app.redraw()

def update(app):
    return