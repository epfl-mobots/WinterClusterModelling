from processing_py import *
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import numpy as np

T_MIN_DRAW = 10
T_MAX_DRAW = 15
# SIZE_BEE = 5
# MAX_VAL = 100


# def get_hue(temp):
#     hue = 480-24.*temp#6000-480*temp#1800-120*temp##240 - 8*temp
#     return hue

# def draw_temp(app,hive,fig,ax):
#     step = 2
#     # grid_res = [step*app.width/hive.dims_temp[1],step*app.height/hive.dims_temp[0]]
#     # app.colorMode(HSB, 360, MAX_VAL, MAX_VAL)

#     temp_colors = (-5/3)*hive.tempField+(1/15)*np.ones_like(hive.tempField)
#     plt.matshow()

#     # for i in range(hive.dims_temp[0]//step):
#     #     for j in range(hive.dims_temp[1]//step):
#     #         x = (j-0.5)*grid_res[0]
#     #         y = app.height - (i+1-0.5)*grid_res[1]

#     #         hue = get_hue(hive.tempField[step*i,step*j])
#     #         app.fill(hue,MAX_VAL,MAX_VAL)
#     #         app.stroke(hue,MAX_VAL,MAX_VAL)
#     #         app.rect(x,y,grid_res[0],grid_res[1])


#     # app.stroke(0,0,0)
#     # app.fill(0,0,MAX_VAL)


# def draw_colony(app,hive,fig):
#     for b in hive.colony:
#         x_draw = b.j*app.width/hive.dims_b[0]
#         y_draw = app.height-b.i*app.height/hive.dims_b[1]
#         app.ellipse(x_draw,y_draw,SIZE_BEE,SIZE_BEE)
#     #app.text("Max T : "+str(hive.currTmax),700,700)
#     T = str(hive.Tmax[-1])
#     # app.text("Max T : "+T[0:5]+"C",700,700)
#     #app.redraw()

def update(hive,count=0):
    temp_colors = (-1/(T_MAX_DRAW-T_MIN_DRAW))*hive.tempField+(T_MAX_DRAW/(T_MAX_DRAW-T_MIN_DRAW))*np.ones_like(hive.tempField)
    plt.matshow(temp_colors,fignum=count,cmap='hsv',vmin=0,vmax=0.7,aspect='equal',interpolation='none',origin='lower')
    for b in hive.colony:
        plt.scatter(b.j*hive.g,b.i*hive.g,c='black',s=1)
    T = str(hive.Tmax[-1])
    plt.text(80,20,"Max T : "+T[0:5]+"C")
    plt.show()

