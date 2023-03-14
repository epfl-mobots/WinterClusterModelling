from processing_py import *
from matplotlib.colors import hsv_to_rgb

SIZE_BEE = 5
MAX_VAL = 100

def init_world(app):
    app.background(0,0,0)

def get_hue(temp):
    hue = 240 - 8*temp
    return hue

def init_temp(app,hive):
    step = 1
    grid_res = [step*app.width/hive.temp.dims[1],step*app.height/hive.temp.dims[0]]
    app.colorMode(HSB, 360, MAX_VAL, MAX_VAL)

    # i = 3
    # j = 3
    # x = j*grid_res[0]
    # y = app.height - i*grid_res[1]

    # hue = get_hue(hive.temp.field[i,j])
    # print(hue)
    # app.fill(hue,MAX_VAL,MAX_VAL)
    # app.rect(x,y,20,20)
    # app.fill(0,0,MAX_VAL)

    for i in range(hive.temp.dims[0]//step):
        for j in range(hive.temp.dims[1]//step):
            x = j*grid_res[0]
            y = app.height - (i+1)*grid_res[1]

            hue = get_hue(hive.temp.field[step*i,step*j])
            app.fill(hue,MAX_VAL,MAX_VAL)
            app.stroke(hue,MAX_VAL,MAX_VAL)
            app.rect(x,y,grid_res[0],grid_res[1])

    app.stroke(0,0,0)
    app.fill(0,0,MAX_VAL)


def init_colony(app,hive):
    for b in hive.colony:
        x_draw = b.x*app.width/hive.dims_b[0]
        y_draw = b.y*app.height/hive.dims_b[1]
        app.ellipse(x_draw,y_draw,SIZE_BEE,SIZE_BEE)
    app.redraw()

def update(app):
    return