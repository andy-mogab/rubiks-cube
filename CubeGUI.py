from Rubiks_Cube import Cube, Face
import math
import random
import numpy as np
import tkinter as Tk
from operator import itemgetter

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
        
    def rotateOtherAxis(self, angle, matrix):
        """Rotates the points about the new axis shifted for better view by the baseangle"""
        rad = angle * math.pi / 180
        sina = math.sin(rad)
        sinaover2 = math.sin(rad/2)
        v = np.array([self.x,self.y,self.z])
        M = np.eye(3) + (sina*matrix) + (2*sinaover2*sinaover2*np.matmul(matrix,matrix))
        pts = np.matmul(M,v)
        return Point3D(pts[0],pts[1],pts[2])
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)

class Sticker:
    def __init__(self, pointlist):
        self.stickerv = pointlist

class FaceStickers:
    def __init__(self, stickerArr2dim):
        self.stickerArr2d = stickerArr2dim
    
class CubeGUI:
    def __init__(self, master, win_width = 640, win_height = 480):
        self.master = master

        self.win_width = win_width
        self.win_height = win_height
        self.canvas = Tk.Canvas(self.master, width = self.win_width, height = self.win_height)
        self.canvas.pack()
        self.helv14 = Tk.font.Font(family='Helvetica', size=14, weight=Tk.font.BOLD)
        self.helv32 = Tk.font.Font(family='Helvetica', size=32, weight=Tk.font.BOLD)
        self.button1 = Tk.Button(self.master, text="Solve Cube", fg="red",command=self.solveC)
        self.button1.configure(width = 100, activebackground = "#33B5E5", font = self.helv14, relief = Tk.RAISED)
        self.button1.pack()
        self.button2 = Tk.Button(self.master, text="Randomize", fg="red", font = self.helv14, command=self.randomize)
        self.button2.configure(width = 100, activebackground = "#33B5E5", relief = Tk.RAISED) 
        self.button2.place(relx=.5, rely = 0.02, anchor="c")
        self.isSolved = False
        self.CubeRotMidSolve = 0
        self.doneRot = True
        self.doneTurn = True
        self.cube = Cube(Face([[0,0,0],[0,0,0],[0,0,0]]), Face([[1,1,1],[1,1,1],[1,1,1]]),
                         Face([[2,2,2],[2,2,2],[2,2,2]]), Face([[3,3,3],[3,3,3],[3,3,3]]),
                         Face([[4,4,4],[4,4,4],[4,4,4]]), Face([[5,5,5],[5,5,5],[5,5,5]]))
        self.bindKeys()
        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
            ]
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(2,6,7,3)]
        self.FSArr = [FaceStickers(self.faceStickersOrig(0)), FaceStickers(self.faceStickersOrig(1)),
                      FaceStickers(self.faceStickersOrig(2)), FaceStickers(self.faceStickersOrig(3)),
                      FaceStickers(self.faceStickersOrig(4)), FaceStickers(self.faceStickersOrig(5))]
        
        self.colors = ["red","green","orange","blue","yellow","white"]
        self.baseangle_x = -25 
        self.baseangle_y = 45
        self.angle = 0
        
        self.alt_axis_projs = self.makeMatrixes()
        self.M1 = self.alt_axis_projs[0]
        self.M2 = self.alt_axis_projs[1]
        self.M3 = self.alt_axis_projs[2]
        
        self.drawCube(0)
        
    def bindKeys(self):
        self.master.bind('<Up>', lambda event: self.rotateCube(event, num = 1))
        self.master.bind('<Down>', lambda event: self.rotateCube(event, num = -1))
        self.master.bind('<Left>', lambda event: self.rotateCube(event, num = 2))
        self.master.bind('<Right>', lambda event: self.rotateCube(event, num = -2))
        self.master.bind('<Shift-Left>', lambda event: self.rotateCube(event, num = 3))
        self.master.bind('<Shift-Right>', lambda event: self.rotateCube(event, num = -3))
        self.master.bind('r', lambda event: self.rotateF(event, facenum = 0, direx = 1))
        self.master.bind('R', lambda event: self.rotateF(event, facenum = 0, direx = -1))
        self.master.bind('g', lambda event: self.rotateF(event, facenum = 1, direx = 1))
        self.master.bind('G', lambda event: self.rotateF(event, facenum = 1, direx = -1))
        self.master.bind('o', lambda event: self.rotateF(event, facenum = 2, direx = 1))
        self.master.bind('O', lambda event: self.rotateF(event, facenum = 2, direx = -1))
        self.master.bind('b', lambda event: self.rotateF(event, facenum = 3, direx = 1))
        self.master.bind('B', lambda event: self.rotateF(event, facenum = 3, direx = -1))
        self.master.bind('y', lambda event: self.rotateF(event, facenum = 4, direx = 1))
        self.master.bind('Y', lambda event: self.rotateF(event, facenum = 4, direx = -1))
        self.master.bind('w', lambda event: self.rotateF(event, facenum = 5, direx = 1))
        self.master.bind('W', lambda event: self.rotateF(event, facenum = 5, direx = -1))
        
    def unbindFaceKeys(self):
        self.master.unbind('r')
        self.master.unbind('R')
        self.master.unbind('g')
        self.master.unbind('G')
        self.master.unbind('o')
        self.master.unbind('O')
        self.master.unbind('b')
        self.master.unbind('B')
        self.master.unbind('y')
        self.master.unbind('Y')
        self.master.unbind('w')
        self.master.unbind('W')
    
    def changebindCubeRotKeys(self):
        self.master.unbind('<Up>')
        self.master.unbind('<Down>')
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')
        self.master.unbind('<Shift-Left>')
        self.master.unbind('<Shift-Right>')
        
        self.master.bind('<Up>', lambda event: self.userInputMidSolve(event, num = 1))
        self.master.bind('<Down>', lambda event: self.userInputMidSolve(event, num = -1))
        self.master.bind('<Left>', lambda event: self.userInputMidSolve(event, num = 2))
        self.master.bind('<Right>', lambda event: self.userInputMidSolve(event, num = -2))
        self.master.bind('<Shift-Left>', lambda event: self.userInputMidSolve(event, num = 3))
        self.master.bind('<Shift-Right>', lambda event: self.userInputMidSolve(event, num = -3)) 
        
    def randomize(self):
        """Randomizes the Cube"""
        tempC = Cube(Face([[0,0,0],[0,0,0],[0,0,0]]), Face([[1,1,1],[1,1,1],[1,1,1]]),
                     Face([[2,2,2],[2,2,2],[2,2,2]]), Face([[3,3,3],[3,3,3],[3,3,3]]),
                     Face([[4,4,4],[4,4,4],[4,4,4]]), Face([[5,5,5],[5,5,5],[5,5,5]]))
        scrambleArr = [[random.randint(0,5), random.randint(0,1)] for i in range(20)]
        for x in scrambleArr:
            if x[1] == 0:
                tempC.rotateFaceL(tempC.getFace(x[0]))
            else:
                tempC.rotateFaceR(tempC.getFace(x[0]))
        self.cube = Cube(Face(tempC.getFace(0).arr2dim),
                         Face(tempC.getFace(1).arr2dim),
                         Face(tempC.getFace(2).arr2dim),
                         Face(tempC.getFace(3).arr2dim),
                         Face(tempC.getFace(4).arr2dim),
                         Face(tempC.getFace(5).arr2dim))
        self.drawCube(0)
        
    def solveC(self):
        """Solves the Cube using Rubiks_Cube.py"""
        self.unbindFaceKeys()
        self.changebindCubeRotKeys()
        tempC = Cube(Face(np.copy(self.cube.getFace(0).arr2dim)),
                     Face(np.copy(self.cube.getFace(1).arr2dim)),
                     Face(np.copy(self.cube.getFace(2).arr2dim)),
                     Face(np.copy(self.cube.getFace(3).arr2dim)),
                     Face(np.copy(self.cube.getFace(4).arr2dim)),
                     Face(np.copy(self.cube.getFace(5).arr2dim)))
        arrStr = tempC.solveCube()
        arrSol = []
        for num, s in enumerate(arrStr, 1):
            print(num, s)
            loc = s.find(" ")
            t1 = s[:loc]
            t2 = s[loc+1:]
            if t1 == "Red":
                color = 0
            elif t1 == "Green":
                color = 1
            elif t1 == "Orange":
                color = 2
            elif t1 == "Blue":
                color = 3
            elif t1 == "Yellow":
                color = 4
            else:
                color = 5
            if t2 == "right":
                drx = 1
            else:
                drx = -1
            arrSol.append([color,drx])
        self.displaySol(arrSol,0, len(arrSol))
       
    def userInputMidSolve(self, ev, num):
        self.CubeRotMidSolve = num
        
    def displaySol(self, arrsol, index, length):
        if index < length:
            if self.doneRot == True and self.doneTurn == True:
                if self.CubeRotMidSolve != 0:
                    self.runturn(self.CubeRotMidSolve)
                    self.CubeRotMidSolve = 0
                else:
                    self.rotateFClockwise(arrsol[index][0],arrsol[index][1])
                    index += 1
            self.master.after(400, self.displaySol, arrsol, index, length)  
        else:
            self.bindKeys()
            self.isSolved = True
            self.winner()
            
    def winner(self):
        self.buttonwin = Tk.Button(self.master, text="You Win! Click to Restart", fg="red",command=self.restart)
        self.buttonwin.configure(width = 100, activebackground = "#33B5E5", font = self.helv14, relief = Tk.RAISED)
        self.buttonwin.place(relx=.5, rely = 0.5, anchor="c")      

    def restart(self):
        self.cube = Cube(Face([[0,0,0],[0,0,0],[0,0,0]]), Face([[1,1,1],[1,1,1],[1,1,1]]),
                         Face([[2,2,2],[2,2,2],[2,2,2]]), Face([[3,3,3],[3,3,3],[3,3,3]]),
                         Face([[4,4,4],[4,4,4],[4,4,4]]), Face([[5,5,5],[5,5,5],[5,5,5]]))
        self.canvas.delete("all")
        self.buttonwin.destroy()
        self.drawCube(0)
           
    def diff(self,p1,p2):
        d1 = p1.x - p2.x
        d2 = p1.y - p2.y
        d3 = p1.z - p2.z
        return np.array([d1,d2,d3])
    
    def makeMatrixes(self):
        """Makes matrix that will be used as other rotation axis"""
        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i].rotateY(self.baseangle_y).rotateX(self.baseangle_x)
        
        for face in self.FSArr:
            for i in range(3):
                for j in range(3):
                    for k in range(4):
                        face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                            .rotateY(self.baseangle_y).rotateX(self.baseangle_x)
            
        v0v3 = self.diff(self.vertices[3], self.vertices[0])
        v0v1 = self.diff(self.vertices[1], self.vertices[0])
        v0v4 = self.diff(self.vertices[4], self.vertices[0])
        self.vec1 = np.cross(v0v4,v0v3); self.vec2 = np.cross(v0v4,v0v1); self.vec3 = np.cross(v0v3,v0v1)
        mag1 = np.linalg.norm(self.vec1); mag2 = np.linalg.norm(self.vec2); mag3 = np.linalg.norm(self.vec3)
        unit1 = self.vec1/mag1; unit2 = self.vec2/mag2; unit3 = self.vec3/mag3;
        W1 = np.array([[0,-unit1[2],unit1[1]],[unit1[2],0,-unit1[0]],[-unit1[1],unit1[0],0]])
        W2 = np.array([[0,-unit2[2],unit2[1]],[unit2[2],0,-unit2[0]],[-unit2[1],unit2[0],0]])
        W3 = np.array([[0,-unit3[2],unit3[1]],[unit3[2],0,-unit3[0]],[-unit3[1],unit3[0],0]])
        return [W1, W2, W3]
    
    def faceStickersOrig(self, facenum):
        """Initializing the Face Stickers depending on the Face"""
        if facenum == 0:
            vlist = [Point3D(-1,1,-1), Point3D(-1./3,1,-1), 
                     Point3D(1./3,1,-1), Point3D(1,1,-1),
                     Point3D(-1,1./3,-1), Point3D(-1./3,1./3,-1),
                     Point3D(1./3,1./3,-1), Point3D(1,1./3,-1),
                     Point3D(-1,-1./3,-1), Point3D(-1./3,-1./3,-1),
                     Point3D(1./3,-1./3,-1), Point3D(1,-1./3,-1),
                     Point3D(-1,-1,-1), Point3D(-1./3,-1,-1),
                     Point3D(1./3,-1,-1), Point3D(1,-1,-1)]
         
        elif facenum == 1:
            vlist = [Point3D(1,1,-1), Point3D(1,1,-1./3), 
                     Point3D(1,1,1./3), Point3D(1,1,1),
                     Point3D(1,1./3,-1), Point3D(1,1./3,-1./3),
                     Point3D(1,1./3,1./3), Point3D(1,1./3,1),
                     Point3D(1,-1./3,-1), Point3D(1,-1./3,-1./3),
                     Point3D(1,-1./3,1./3), Point3D(1,-1./3,1),
                     Point3D(1,-1,-1), Point3D(1,-1,-1./3),
                     Point3D(1,-1,1./3), Point3D(1,-1,1)]
        
        elif facenum == 2:
            vlist = [Point3D(1,1,1), Point3D(1./3,1,1), 
                     Point3D(-1./3,1,1), Point3D(-1,1,1),
                     Point3D(1,1./3,1), Point3D(1./3,1./3,1),
                     Point3D(-1./3,1./3,1), Point3D(-1,1./3,1),
                     Point3D(1,-1./3,1), Point3D(1./3,-1./3,1),
                     Point3D(-1./3,-1./3,1), Point3D(-1,-1./3,1),
                     Point3D(1,-1,1), Point3D(1./3,-1,1),
                     Point3D(-1./3,-1,1), Point3D(-1,-1,1)]
            
        elif facenum == 3:
            vlist = [Point3D(-1,1,1), Point3D(-1,1,1./3), 
                     Point3D(-1,1,-1./3), Point3D(-1,1,-1),
                     Point3D(-1,1./3,1), Point3D(-1,1./3,1./3),
                     Point3D(-1,1./3,-1./3), Point3D(-1,1./3,-1),
                     Point3D(-1,-1./3,1), Point3D(-1,-1./3,1./3),
                     Point3D(-1,-1./3,-1./3), Point3D(-1,-1./3,-1),
                     Point3D(-1,-1,1), Point3D(-1,-1,1./3),
                     Point3D(-1,-1,-1./3), Point3D(-1,-1,-1)]
            
        elif facenum == 4:
            vlist = [Point3D(-1,1,-1), Point3D(-1,1,-1./3), 
                     Point3D(-1,1,1./3), Point3D(-1,1,1),
                     Point3D(-1./3,1,-1), Point3D(-1./3,1,-1./3),
                     Point3D(-1./3,1,1./3), Point3D(-1./3,1,1),
                     Point3D(1./3,1,-1), Point3D(1./3,1,-1./3),
                     Point3D(1./3,1,1./3), Point3D(1./3,1,1),
                     Point3D(1,1,-1), Point3D(1,1,-1./3),
                     Point3D(1,1,1./3), Point3D(1,1,1)]
        else:
            vlist = [Point3D(1,-1,-1), Point3D(1,-1,-1./3), 
                     Point3D(1,-1,1./3), Point3D(1,-1,1),
                     Point3D(1./3,-1,-1), Point3D(1./3,-1,-1./3),
                     Point3D(1./3,-1,1./3), Point3D(1./3,-1,1),
                     Point3D(-1./3,-1,-1), Point3D(-1./3,-1,-1./3),
                     Point3D(-1./3,-1,1./3), Point3D(-1./3,-1,1),
                     Point3D(-1,-1,-1), Point3D(-1,-1,-1./3),
                     Point3D(-1,-1,1./3), Point3D(-1,-1,1)]
       
        topStickers = [Sticker([vlist[0],vlist[1],vlist[5],vlist[4]]),
                       Sticker([vlist[1],vlist[2],vlist[6],vlist[5]]),
                       Sticker([vlist[3],vlist[7],vlist[6],vlist[2]])]            
        midStickers = [Sticker([vlist[8],vlist[4],vlist[5],vlist[9]]),
                       Sticker([vlist[5],vlist[6],vlist[10],vlist[9]]),
                       Sticker([vlist[7],vlist[11],vlist[10],vlist[6]])]            
        botStickers = [Sticker([vlist[12],vlist[8],vlist[9],vlist[13]]),
                       Sticker([vlist[14],vlist[13],vlist[9],vlist[10]]),
                       Sticker([vlist[15],vlist[14],vlist[10],vlist[11]])]
        
        return [topStickers, midStickers, botStickers]
  
     
    def runturn(self, direction):
        """Initiates a Cube turn"""
        self.doneTurn = False
        if self.angle <= 90:
            self.drawCube(direction)
            self.angle += 3
            self.master.after(10, self.runturn, direction)
        else:
            self.doneTurn = True
            self.angle = 0
            for i in range(len(self.vertices)):
                    if direction == 1:
                        self.vertices[i] = self.vertices[i].rotateOtherAxis(90, self.M1)
                    elif direction == -1:
                        self.vertices[i] = self.vertices[i].rotateOtherAxis(-90, self.M1)
                    elif direction == 2:
                        self.vertices[i] = self.vertices[i].rotateOtherAxis(90, self.M2)
                    elif direction == -2:
                        self.vertices[i] = self.vertices[i].rotateOtherAxis(-90, self.M2)
                    elif direction == 3:
                        self.vertices[i] = self.vertices[i].rotateOtherAxis(90, self.M3)
                    else:
                        self.vertices[i] = self.vertices[i].rotateOtherAxis(-90, self.M3)
             
            for face in self.FSArr:
                for i in range(3):
                    for j in range(3):
                        for k in range(4):
                            if direction == 1:
                                face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                                    .rotateOtherAxis(90, self.M1)               
                            elif direction == -1:
                                face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                                    .rotateOtherAxis(-90, self.M1)               
                            elif direction == 2:                
                                face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                                    .rotateOtherAxis(90, self.M2)
                            elif direction == -2:               
                                face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                                    .rotateOtherAxis(-90, self.M2) 
                            elif direction == 3:
                                face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                                    .rotateOtherAxis(90, self.M3) 
                            else:
                                face.stickerArr2d[i][j].stickerv[k] = face.stickerArr2d[i][j].stickerv[k]\
                                    .rotateOtherAxis(-90, self.M3) 
   
    def rotateCube(self, ev, num):
        self.runturn(num)
        
    def rotateF(self, ev, facenum, direx):
        self.rotateFClockwise(facenum,direx)
        
    def rotateFClockwise(self, facenum, direx):
        x = self.faces[facenum][0]
        y = self.faces[facenum][1]
        z = self.faces[facenum][3]
        facevec = np.cross(self.diff(self.vertices[y], self.vertices[x]),
                           self.diff(self.vertices[z], self.vertices[x]))
        facevec = [round(elem, 2) for elem in facevec]
        vec1R = [round(elem, 2) for elem in self.vec1]
        vec2R = [round(elem, 2) for elem in self.vec2]
        vec3R = [round(elem, 2) for elem in self.vec3]
        if (facevec[0] == vec1R[0] and facevec[1] == vec1R[1] and facevec[2] == vec1R[2]) or\
            (-facevec[0] == vec1R[0] and -facevec[1] == vec1R[1] and -facevec[2] == vec1R[2]):
            axis = self.M1
            if facevec[0] == vec1R[0] and facevec[1] == vec1R[1] and facevec[2] == vec1R[2]:
                anglesign = 1
            else:
                anglesign = -1
        elif (facevec[0] == vec2R[0] and facevec[1] == vec2R[1] and facevec[2] == vec2R[2]) or\
                (-facevec[0] == vec2R[0] and -facevec[1] == vec2R[1] and -facevec[2] == vec2R[2]):
            axis = self.M2
            if facevec[0] == vec2R[0] and facevec[1] == vec2R[1] and facevec[2] == vec2R[2]:
                anglesign = 1
            else:
                anglesign = -1
        else:
            axis = self.M3
            if facevec[0] == vec3R[0] and facevec[1] == vec3R[1] and facevec[2] == vec3R[2]:
                anglesign = 1
            else:
                anglesign = -1
        
        self.runrotation(facenum, axis, anglesign, direx)
        
        
    def runrotation(self, facenum, axis, anglesign, direction):
        """Initiates a Face Rotation"""
        self.doneRot = False
        if self.angle <= 90:
            self.drawFRotationClockwise(facenum, axis, anglesign, direction)
            self.angle += 3
            self.master.after(10, self.runrotation, facenum, axis, anglesign, direction)
        else:
            self.doneRot = True
            self.angle = 0
            if direction == 1:
                self.cube.rotateFaceR(self.cube.getFace(facenum))
            else:
                self.cube.rotateFaceL(self.cube.getFace(facenum))
       
    def getOppFace(self, facenum):
        if facenum == 0:
            oppface = 2
        elif facenum == 1:
            oppface = 3
        elif facenum == 2:
            oppface = 0
        elif facenum == 3:
            oppface = 1
        elif facenum == 4:
            oppface = 5
        else:
            oppface = 4
        return oppface
    
    def getStationaryIndexDict(self, facenum):
        if facenum == 0:
            indexvals_dict = {1:[[i,j+1] for i in range(3) for j in range(2)], # block of right 6
                              2:[[i,j] for i in range(3) for j in range(3)], #block of all
                              3:[[i,j] for i in range(3) for j in range(2)], #block of left 6
                              4:[[i,j+1] for i in range(3) for j in range(2)],
                              5:[[i,j+1] for i in range(3) for j in range(2)]}
        elif facenum == 1:
            indexvals_dict = {0:[[i,j] for i in range(3) for j in range(2)],
                              2:[[i,j+1] for i in range(3) for j in range(2)],
                              3:[[i,j] for i in range(3) for j in range(3)],
                              4:[[i,j] for i in range(2) for j in range(3)], #block of top 6
                              5:[[i+1,j] for i in range(2) for j in range(3)]} #block of bottom 6
        elif facenum == 2:
            indexvals_dict = {0:[[i,j] for i in range(3) for j in range(3)],
                              1:[[i,j] for i in range(3) for j in range(2)],
                              3:[[i,j+1] for i in range(3) for j in range(2)],
                              4:[[i,j] for i in range(3) for j in range(2)],
                              5:[[i,j] for i in range(3) for j in range(2)]}
        elif facenum == 3:
            indexvals_dict = {0:[[i,j+1] for i in range(3) for j in range(2)],
                              1:[[i,j] for i in range(3) for j in range(3)],
                              2:[[i,j] for i in range(3) for j in range(2)],
                              4:[[i+1,j] for i in range(2) for j in range(3)],
                              5:[[i,j] for i in range(2) for j in range(3)]}
        elif facenum == 4:
            indexvals_dict = {0:[[i+1,j] for i in range(2) for j in range(3)],
                              1:[[i+1,j] for i in range(2) for j in range(3)],
                              2:[[i+1,j] for i in range(2) for j in range(3)],
                              3:[[i+1,j] for i in range(2) for j in range(3)],
                              5:[[i,j] for i in range(3) for j in range(3)]}
        else:
            indexvals_dict = {0:[[i,j] for i in range(2) for j in range(3)],
                              1:[[i,j] for i in range(2) for j in range(3)],
                              2:[[i,j] for i in range(2) for j in range(3)],
                              3:[[i,j] for i in range(2) for j in range(3)],
                              4:[[i,j] for i in range(3) for j in range(3)]}
        return indexvals_dict
    
    def getRotationalIndexDict(self, facenum):
        if facenum == 0:
            indexvalsRot_dict = {0:[[i,j] for i in range(3) for j in range(3)], 
                                 1:[[i,j] for i in range(3) for j in range(1)], 
                                 3:[[i,j+2] for i in range(3) for j in range(1)], 
                                 4:[[i,j] for i in range(3) for j in range(1)],
                                 5:[[i,j] for i in range(3) for j in range(1)]}
        elif facenum == 1:
            indexvalsRot_dict = {0:[[i,j+2] for i in range(3) for j in range(1)], #right 3
                                 1:[[i,j] for i in range(3) for j in range(3)], #all
                                 2:[[i,j] for i in range(3) for j in range(1)], #left 3 
                                 4:[[i+2,j] for i in range(1) for j in range(3)], #bottom 3
                                 5:[[i,j] for i in range(1) for j in range(3)]} #top 3   
        elif facenum == 2:
            indexvalsRot_dict = {1:[[i,j+2] for i in range(3) for j in range(1)], 
                                 2:[[i,j] for i in range(3) for j in range(3)], 
                                 3:[[i,j] for i in range(3) for j in range(1)], 
                                 4:[[i,j+2] for i in range(3) for j in range(1)],
                                 5:[[i,j+2] for i in range(3) for j in range(1)]}
        elif facenum == 3:
            indexvalsRot_dict = {0:[[i,j] for i in range(3) for j in range(1)], 
                                 2:[[i,j+2] for i in range(3) for j in range(1)] , 
                                 3:[[i,j] for i in range(3) for j in range(3)], 
                                 4:[[i,j] for i in range(1) for j in range(3)],
                                 5:[[i+2,j] for i in range(1) for j in range(3)]}
        elif facenum == 4:
            indexvalsRot_dict = {0:[[i,j] for i in range(1) for j in range(3)], 
                                 1:[[i,j] for i in range(1) for j in range(3)], 
                                 2:[[i,j] for i in range(1) for j in range(3)], 
                                 3:[[i,j] for i in range(1) for j in range(3)],
                                 4:[[i,j] for i in range(3) for j in range(3)]}
        else:
            indexvalsRot_dict = {0:[[i+2,j] for i in range(1) for j in range(3)], 
                                 1:[[i+2,j] for i in range(1) for j in range(3)], 
                                 2:[[i+2,j] for i in range(1) for j in range(3)], 
                                 3:[[i+2,j] for i in range(1) for j in range(3)],
                                 5:[[i,j] for i in range(3) for j in range(3)]}
        return indexvalsRot_dict
    
    def getBlackFList(self, facenum):
        """For displaying the Black on the inside of the Cube when rotating faces"""
        if facenum == 0:
            blackF = [self.FSArr[3].stickerArr2d[0][1].stickerv[1],
                      self.FSArr[1].stickerArr2d[0][1].stickerv[0],
                      self.FSArr[1].stickerArr2d[2][1].stickerv[1],
                      self.FSArr[3].stickerArr2d[2][1].stickerv[0]]
        elif facenum == 1:
            blackF = [self.FSArr[0].stickerArr2d[0][1].stickerv[1],
                      self.FSArr[2].stickerArr2d[0][1].stickerv[0],
                      self.FSArr[2].stickerArr2d[2][1].stickerv[1],
                      self.FSArr[0].stickerArr2d[2][1].stickerv[0]]
            
        elif facenum == 2:
            blackF = [self.FSArr[1].stickerArr2d[0][1].stickerv[1],
                      self.FSArr[3].stickerArr2d[0][1].stickerv[0],
                      self.FSArr[3].stickerArr2d[2][1].stickerv[1],
                      self.FSArr[1].stickerArr2d[2][1].stickerv[0]]
            
        elif facenum == 3:
            blackF = [self.FSArr[2].stickerArr2d[0][1].stickerv[1],
                      self.FSArr[0].stickerArr2d[0][1].stickerv[0],
                      self.FSArr[0].stickerArr2d[2][1].stickerv[1],
                      self.FSArr[2].stickerArr2d[2][1].stickerv[0]]
            
        elif facenum == 4:
            blackF = [self.FSArr[0].stickerArr2d[1][0].stickerv[1],
                      self.FSArr[2].stickerArr2d[1][2].stickerv[0],
                      self.FSArr[2].stickerArr2d[1][0].stickerv[1],
                      self.FSArr[0].stickerArr2d[1][2].stickerv[0]]
            
        else:
            blackF = [self.FSArr[0].stickerArr2d[1][2].stickerv[1],
                      self.FSArr[2].stickerArr2d[1][0].stickerv[0],
                      self.FSArr[2].stickerArr2d[1][2].stickerv[1],
                      self.FSArr[0].stickerArr2d[1][0].stickerv[0]]
        return blackF
        
    def drawFRotationClockwise(self, facenum, axis, anglesign, direction):
        """displaying the Face Rotation"""
        self.canvas.delete("all")  
        t = []
        verticesandblack = self.vertices[:]
        for vert in self.getBlackFList(facenum):
            verticesandblack.append(vert)
        for v in verticesandblack:   
            p = v.project(self.win_width, self.win_height, 400, 5)
            t.append(p)
        facesandblack = self.faces[:]
        facesandblack.append((8,9,10,11))
        avg_z = []
        for i in range(len(facesandblack)):
            if i != facenum:
                z = (t[facesandblack[i][0]].z + t[facesandblack[i][1]].z + t[facesandblack[i][2]].z\
                     + t[facesandblack[i][3]].z) / 4.0
                avg_z.append([i,z]) 
        t2 = []
        for v in verticesandblack:
            r = v.rotateOtherAxis(self.angle * anglesign * direction, axis)
            p = r.project(self.win_width, self.win_height, 400, 5)
            t2.append(p)
        d = {}
        for i in range(len(self.faces)):
            if i != facenum and i != self.getOppFace(facenum):
                l = []
                for a in self.getRotationalIndexDict(facenum)[i]:
                    j = self.FSArr[i].stickerArr2d[a[0]][a[1]].stickerv
                    for k in j:
                        r = k.rotateOtherAxis(self.angle * anglesign * direction, axis)
                        p = r.project(self.win_width, self.win_height, 400, 5)
                        l.append(p.z)
                d[i] = l
        avg_z2 = []
        for i in range(len(facesandblack)):
            if i != self.getOppFace(facenum):
                if i == facenum or i == 6:
                    z = (t2[facesandblack[i][0]].z + t2[facesandblack[i][1]].z\
                         + t2[facesandblack[i][2]].z + t2[facesandblack[i][3]].z) / 4.0
                else:
                    z = sum(d[i])/ 12.0
                avg_z2.append([i,z])
        if axis is self.M1 or axis is self.M2:
            if anglesign == 1:
                self.displayTwoThirdsCube(facenum, avg_z)
                self.displayOneThirdCubeRot(facenum, avg_z2, axis, anglesign, direction)
            else:
                self.displayOneThirdCubeRot(facenum, avg_z2, axis, anglesign, direction)
                self.displayTwoThirdsCube(facenum, avg_z)
        else:
            if anglesign == 1:
                self.displayOneThirdCubeRot(facenum, avg_z2, axis, anglesign, direction)
                self.displayTwoThirdsCube(facenum, avg_z)
            else:
                self.displayTwoThirdsCube(facenum, avg_z)
                self.displayOneThirdCubeRot(facenum, avg_z2, axis, anglesign, direction)
    
    def displayTwoThirdsCube(self, facenum, avg_z):
        """displaying the stationary part of cube during a rotation"""
        for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
            if tmp[0] == 6:
                stkr = []
                for k in range(4):
                    r = self.getBlackFList(facenum)[k]
                    p = r.project(self.win_width, self.win_height, 400, 5)
                    stkr.append(p)
                blacklist = [(stkr[0].x, stkr[0].y), (stkr[1].x, stkr[1].y),
                             (stkr[1].x, stkr[1].y), (stkr[2].x, stkr[2].y),
                             (stkr[2].x, stkr[2].y), (stkr[3].x, stkr[3].y),
                             (stkr[3].x, stkr[3].y), (stkr[0].x, stkr[0].y)]
                self.canvas.create_polygon(blacklist, fill = "black", outline = "black")
            else:
                stickerface = self.FSArr[tmp[0]]
                arrindvals = self.getStationaryIndexDict(facenum)[tmp[0]]
                for x in arrindvals:
                    stkr = []
                    col = self.colors[self.cube.getFace(tmp[0]).getTile(x[0],x[1])]
                    for k in range(4):
                        r = stickerface.stickerArr2d[x[0]][x[1]].stickerv[k]
                        p = r.project(self.win_width, self.win_height, 400, 5)
                        stkr.append(p)
                    plist = [(stkr[0].x, stkr[0].y), (stkr[1].x, stkr[1].y),
                             (stkr[1].x, stkr[1].y), (stkr[2].x, stkr[2].y),
                             (stkr[2].x, stkr[2].y), (stkr[3].x, stkr[3].y),
                             (stkr[3].x, stkr[3].y), (stkr[0].x, stkr[0].y)]
                    self.canvas.create_polygon(plist, fill = col, outline = "black")
    
    def displayOneThirdCubeRot(self, facenum, avg_z, axis, anglesign, direction):
        """displaying the rotating layer of the cube"""
        for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
            if tmp[0] == 6: 
                stkr = []
                for k in range(4):
                    r = self.getBlackFList(facenum)[k].rotateOtherAxis(self.angle * anglesign * direction, axis)
                    p = r.project(self.win_width, self.win_height, 400, 5)
                    stkr.append(p)
                blacklist = [(stkr[0].x, stkr[0].y), (stkr[1].x, stkr[1].y),
                             (stkr[1].x, stkr[1].y), (stkr[2].x, stkr[2].y),
                             (stkr[2].x, stkr[2].y), (stkr[3].x, stkr[3].y),
                             (stkr[3].x, stkr[3].y), (stkr[0].x, stkr[0].y)]
                self.canvas.create_polygon(blacklist, fill = "black", outline = "black")
            else:
                stickerface = self.FSArr[tmp[0]]
                arrindvals = self.getRotationalIndexDict(facenum)[tmp[0]]
                for x in arrindvals:
                    stkr = []
                    col = self.colors[self.cube.getFace(tmp[0]).getTile(x[0],x[1])]
                    for k in range(4):
                        r = stickerface.stickerArr2d[x[0]][x[1]].stickerv[k]\
                            .rotateOtherAxis(self.angle * anglesign * direction, axis)
                        p = r.project(self.win_width, self.win_height, 400, 5)
                        stkr.append(p)    
                    plist = [(stkr[0].x, stkr[0].y), (stkr[1].x, stkr[1].y),
                             (stkr[1].x, stkr[1].y), (stkr[2].x, stkr[2].y),
                             (stkr[2].x, stkr[2].y), (stkr[3].x, stkr[3].y),
                             (stkr[3].x, stkr[3].y), (stkr[0].x, stkr[0].y)]
                    self.canvas.create_polygon(plist, fill = col, outline = "black")
           
    def drawCube(self, numdir):
        """Draws the cube at a stationary state"""
        self.canvas.delete("all")
        t = []   
        for v in self.vertices:
            if numdir == 1:
                r = v.rotateOtherAxis(self.angle, self.M1)               
            elif numdir == -1:
                r = v.rotateOtherAxis(-self.angle, self.M1)              
            elif numdir == 2:                
                r = v.rotateOtherAxis(self.angle, self.M2)
            elif numdir == -2:               
                r = v.rotateOtherAxis(-self.angle, self.M2)
            elif numdir == 3:
                r = v.rotateOtherAxis(self.angle, self.M3)
            elif numdir == -3:
                r = v.rotateOtherAxis(-self.angle, self.M3)
            else:
                r = v  
            p = r.project(self.win_width, self.win_height, 400, 5)
            t.append(p)
        avg_z = []
        i = 0
        for f in self.faces:
            z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
            avg_z.append([i,z])
            i = i + 1
        for tmp in sorted(avg_z,key=itemgetter(1),reverse=True): 
            face = tmp[0]
            for i in range(3):
                for j in range(3):
                    stkr = []
                    col = self.colors[self.cube.getFace(face).getTile(i,j)]
                    for k in range(4):
                        if numdir == 1:
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]\
                                .rotateOtherAxis(self.angle, self.M1)               
                        elif numdir == -1:
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]\
                                .rotateOtherAxis(-self.angle, self.M1)              
                        elif numdir == 2:                
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]\
                                .rotateOtherAxis(self.angle, self.M2)
                        elif numdir == -2:               
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]\
                                .rotateOtherAxis(-self.angle, self.M2)
                        elif numdir == 3:
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]\
                                .rotateOtherAxis(self.angle, self.M3)
                        elif numdir == -3:
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]\
                                .rotateOtherAxis(-self.angle, self.M3)
                        else:
                            r = self.FSArr[face].stickerArr2d[i][j].stickerv[k]
                        
                        p = r.project(self.win_width, self.win_height, 400, 5)
                        stkr.append(p)
                        
                    plist = [(stkr[0].x, stkr[0].y), (stkr[1].x, stkr[1].y),
                             (stkr[1].x, stkr[1].y), (stkr[2].x, stkr[2].y),
                             (stkr[2].x, stkr[2].y), (stkr[3].x, stkr[3].y),
                             (stkr[3].x, stkr[3].y), (stkr[0].x, stkr[0].y)]
                    self.canvas.create_polygon(plist, fill = col, outline = "black")                           
                                       

if __name__ == "__main__":
    root = Tk.Tk()
    gui = CubeGUI(root)
    root.mainloop()
    
