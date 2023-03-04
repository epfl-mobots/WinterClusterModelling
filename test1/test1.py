import numpy as np
import random

import requests
from processing_py import *

class Boid:
    def __init__(self,x,y):
        self.position = np.array([x,y],dtype=float)
        self.acceleration = np.array([0,0], dtype=float)
        #speed = random.random()*2*np.pi
        self.velocity = np.array([random.random(), random.random()])

        self.r = 2.0
        self.maxSpeed = 2.0
        self.maxForce = 0.03

    def run(self, boids:np.ndarray):
        self.flock(boids)
        self.update()
        self.borders()
        self.render()
    
    def applyForce(self, force:np.ndarray):
        self.acceleration += force
    
    def flock(self, boids:np.ndarray):
        self.applyForce(1.5*self.separate(boids))
        self.applyForce(1.0*self.align(boids))
        self.applyForce(1.0*self.cohesion(boids))

    def update(self):
        self.velocity += self.acceleration
        np.clip(self.velocity, -self.maxSpeed, self.maxSpeed)
        self.position += self.velocity
        self.acceleration = 0

    def seek(self, target:np.ndarray):
        desired = target-self.position
        desired = (self.maxSpeed/np.linalg.norm(desired))*desired

        steer = desired-self.velocity
        return steer
    
    def render(self):
        theta = np.arctan2(self.velocity[1], self.velocity[0])

        app.fill(200, 100)
        app.stroke(255)
        app.pushMatrix()
        app.translate(self.position[0], self.position[1])
        app.rotate(theta)
        # app.beginShape(TRIANGLES)
        # app.vertex(0, -self.r*2)
        # app.vertex(-self.r, self.r*2)
        # app.vertex(self.r, self.r*2)
        app.triangle(0, -self.r*2, -self.r, self.r*2, self.r, self.r*2)
        #app.endShape()
        app.popMatrix()

    def borders(self):
        if (self.position[0] < -self.r):
            self.position[0] = app.width+self.r

        if (self.position[1] < -self.r):
            self.position[1] = app.height+self.r

        if (self.position[0] > app.width+self.r):
            self.position[0] = -self.r

        if (self.position[1] > app.height+self.r):
            self.position[1] = -self.r
    
    def separate(self, boids:np.ndarray):
        desiredSep = 4#25.0
        steer = np.array([0,0],dtype=float)
        count = 0

        for other in boids:
            d = np.linalg.norm(self.position-other.position)
            
            if (d>0) and (d<desiredSep):
                diff = self.position-other.position
                diff = (1/(d*np.linalg.norm(diff)))*diff
                steer += diff
                count += 1
        
        if count>0:
            steer = (1/count)*steer
        
        if(np.linalg.norm(steer)>0):
            steer = (self.maxSpeed/np.linalg.norm(steer))*steer
            steer -= self.velocity
            np.clip(steer, -self.maxForce, self.maxForce)

        return steer
    
    def align(self, boids:np.ndarray):
        neighDist = 50
        sum = np.array([0,0], dtype=float)
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position-other.position)

            if (d>0) and (d<neighDist):
                sum += other.velocity
                count += 1
        
        if count>0:
            sum = (1/count)*sum
            sum = (self.maxSpeed/np.linalg.norm(sum))*sum
            steer = sum-self.velocity
            np.clip(steer, -self.maxForce, self.maxForce)
            return steer

        else:
            return np.array([0,0])
        
    def cohesion(self, boids:np.ndarray):
        neighDist = 50
        sum = np.array([0,0], dtype=float)
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position-other.position)

            if (d>0) and (d<neighDist):
                sum += other.position
                count += 1
        
        if count>0:
            sum = (1/count)*sum
            return self.seek(sum)

        else:
            return np.array([0,0])


class Flock:
    def __init__(self):
        self.nb = 0
        self.boids = []

    def run(self):
        for b in self.boids:
            b.run(np.array(self.boids))
    
    def addBoid(self, b):
        self.boids.append(b)


flock = Flock()
app = App(1280,720)
for i in range(150):
        flock.addBoid(Boid(app.width/2, app.height/2))

while(True):
    app.background(0.5,0.5,0.5)
    flock.run()
    # for b in flock.boids:
    #     b.render()
    app.redraw()