from processing_py import *
from matplotlib.colors import hsv_to_rgb

SIZE_BEE = 5
MAX_VAL = 100

def init_world(app):
    app.background(0,0,0)

def get_hue(temp):
    hue = 480-24*temp#6000-480*temp#1800-120*temp##240 - 8*temp
    return hue

def init_temp(app,hive):
    step = 2
    grid_res = [step*app.width/hive.dims_temp[1],step*app.height/hive.dims_temp[0]]
    app.colorMode(HSB, 360, MAX_VAL, MAX_VAL)

    for i in range(hive.dims_temp[0]//step):
        for j in range(hive.dims_temp[1]//step):
            x = (j-0.5)*grid_res[0]
            y = app.height - (i+1-0.5)*grid_res[1]

            hue = get_hue(hive.tempField[step*i,step*j])
            app.fill(hue,MAX_VAL,MAX_VAL)
            app.stroke(hue,MAX_VAL,MAX_VAL)
            app.rect(x,y,grid_res[0],grid_res[1])


    app.stroke(0,0,0)
    app.fill(0,0,MAX_VAL)

# def init_temp_old(app,hive):
#     step = 1
#     grid_res = [step*app.width/hive.dims_temp[1],step*app.height/hive.dims_temp[0]]
#     app.colorMode(HSB, 360, MAX_VAL, MAX_VAL)

    # i = 3
    # j = 3
    # x = j*grid_res[0]
    # y = app.height - i*grid_res[1]

    # hue = get_hue(hive.temp.field[i,j])
    # print(hue)
    # app.fill(hue,MAX_VAL,MAX_VAL)
    # app.rect(x,y,20,20)
    # app.fill(0,0,MAX_VAL)

#     for i in range(hive.dims_temp[0]//step):
#         for j in range(hive.dims_temp[1]//step):
#             x = j*grid_res[0]
#             y = app.height - (i+1)*grid_res[1]

#             hue = get_hue(hive.tempField[step*i,step*j])
#             app.fill(hue,MAX_VAL,MAX_VAL)
#             app.stroke(hue,MAX_VAL,MAX_VAL)
#             app.rect(x,y,grid_res[0],grid_res[1])


#     app.stroke(0,0,0)
#     app.fill(0,0,MAX_VAL)

def init_colony(app,hive):
    for b in hive.colony:
        x_draw = b.j*app.width/hive.dims_b[0]
        y_draw = app.height-b.i*app.height/hive.dims_b[1]
        app.ellipse(x_draw,y_draw,SIZE_BEE,SIZE_BEE)
    #app.text("Max T : "+str(hive.currTmax),700,700)
    T = str(hive.Tmax[-1])
    app.text("Max T : "+T[0:5]+"C",700,700)
    app.redraw()

def update(app,hive):
    init_temp(app,hive)
    init_colony(app,hive)
    T = str(hive.Tmax[-1])
    app.text("Max T : "+T[0:5]+"C",700,700)

