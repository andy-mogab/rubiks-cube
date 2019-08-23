import numpy as np

class Face:
    def __init__(self, arr2d = np.array([[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]])):
        self.arr2dim = np.array(arr2d)        
    def get3top(self):
        temp = [-1,-1,-1]
        for i in range(3):
            temp[i] = self.arr2dim[0][i]
        return temp    
    def get3right(self):
        temp = [-1,-1,-1]
        for i in range(3):
            temp[i] = self.arr2dim[i][2]
        return temp
    def get3bot(self):
        temp = [-1,-1,-1]
        for i in range(3):
            temp[i] = self.arr2dim[2][2-i]
        return temp
    def get3left(self):
        temp = [-1,-1,-1]
        for i in range(3):
            temp[i] = self.arr2dim[2-i][0]
        return temp    
    def set3top(self, new3):
        for i in range(3):
            self.arr2dim[0][i] = new3[i]           
    def set3right(self, new3):
        for i in range(3):
            self.arr2dim[i][2] = new3[i]            
    def set3bot(self, new3):
        for i in range(3):
            self.arr2dim[2][2-i] = new3[i]            
    def set3left(self, new3):
        for i in range(3):
            self.arr2dim[2-i][0] = new3[i]    
    def getArr(self):
        return self.arr2dim   
    def getFaceColor(self):
        return self.arr2dim[1][1]   
    def getTile(self, x, y):
        return self.arr2dim[x][y]
    def rotateR(self):
        temp = np.copy(self.arr2dim)
        for i in range(3):
            for j in range(3):
                self.arr2dim[i][j] = temp[2-j][i]
    def rotateL(self):
        temp = np.copy(self.arr2dim)
        for i in range(3):
            for j in range(3):
                self.arr2dim[i][j] = temp[j][2-i]
    def printF(self):
        print(self.arr2dim)
        
class Piece: 
    def __init__(self, f1 = Face(), f2 = Face(), f3 = Face()):
        self.face1 = f1
        self.face2 = f2
        self.face3 = f3
    def getFace1(self):
        return self.face1
    def getFace2(self):
        return self.face2
    def getFace3(self):
        return self.face3
    def getFColor(self, num): 
        if num == 1:
            return self.face1.getFaceColor()
        elif num == 2:
            return self.face2.getFaceColor()
        else:
            return self.face3.getFaceColor()
    def getFName(self, num):
        color_int = self.getFColor(num)
        if color_int == 0:
            color = "Red"
        elif color_int == 1:
            color = "Green"
        elif color_int == 2:
            color = "Orange"
        elif color_int == 3:
            color = "Blue"
        elif color_int == 4:
            color = "Yellow"
        else:
            color = "White"
        return color
    
    def getArrPColor(self):
        ptemp = [0,0,0]
        if self.face3.getTile(1,1) == -1: 
            ptemp[2] = -1
            if self.face1.getFaceColor() == 0: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,1)
                    ptemp[1] = self.face2.getTile(1,0)
                elif self.face2.getFaceColor() == 3:
                    ptemp[0] = self.face1.getTile(1,0)
                    ptemp[1] = self.face2.getTile(1,2)
                elif self.face2.getFaceColor() == 1:
                    ptemp[0] = self.face1.getTile(1,2)
                    ptemp[1] = self.face2.getTile(1,0)
                else:
                    ptemp[0] = self.face1.getTile(2,1)
                    ptemp[1] = self.face2.getTile(1,0)
            elif self.face1.getFaceColor() == 1: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,1)
                    ptemp[1] = self.face2.getTile(2,1)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(1,0)
                    ptemp[1] = self.face2.getTile(1,2)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(1,2)
                    ptemp[1] = self.face2.getTile(1,0)
                else:
                    ptemp[0] = self.face1.getTile(2,1)
                    ptemp[1] = self.face2.getTile(0,1)
            elif self.face1.getFaceColor() == 2: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,1)
                    ptemp[1] = self.face2.getTile(1,2)
                elif self.face2.getFaceColor() == 1:
                    ptemp[0] = self.face1.getTile(1,0)
                    ptemp[1] = self.face2.getTile(1,2)
                elif self.face2.getFaceColor() == 3:
                    ptemp[0] = self.face1.getTile(1,2)
                    ptemp[1] = self.face2.getTile(1,0)
                else:
                    ptemp[0] = self.face1.getTile(2,1)
                    ptemp[1] = self.face2.getTile(1,2)
            elif self.face1.getFaceColor() == 3: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,1)
                    ptemp[1] = self.face2.getTile(0,1)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(1,0)
                    ptemp[1] = self.face2.getTile(1,2)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(1,2)
                    ptemp[1] = self.face2.getTile(1,0)
                else:
                    ptemp[0] = self.face1.getTile(2,1)
                    ptemp[1] = self.face2.getTile(2,1)
            elif self.face1.getFaceColor() == 4: 
                if self.face2.getFaceColor() == 3:
                    ptemp[0] = self.face1.getTile(0,1)
                    ptemp[1] = self.face2.getTile(0,1)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(1,0)
                    ptemp[1] = self.face2.getTile(0,1)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(1,2)
                    ptemp[1] = self.face2.getTile(0,1)
                else:
                    ptemp[0] = self.face1.getTile(2,1)
                    ptemp[1] = self.face2.getTile(0,1)
            else: 
                if self.face2.getFaceColor() == 1:
                    ptemp[0] = self.face1.getTile(0,1)
                    ptemp[1] = self.face2.getTile(2,1)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(1,0)
                    ptemp[1] = self.face2.getTile(2,1)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(1,2)
                    ptemp[1] = self.face2.getTile(2,1)
                else:
                    ptemp[0] = self.face1.getTile(2,1)
                    ptemp[1] = self.face2.getTile(2,1)
        else: #meaning piece is a corner piece (has 3 faces) 
            if self.face1.getFaceColor() == 0: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,0)
                    ptemp[1] = self.face2.getTile(0,0)
                    ptemp[2] = self.face3.getTile(0,2)
                elif self.face2.getFaceColor() == 1:
                    ptemp[0] = self.face1.getTile(0,2)
                    ptemp[1] = self.face2.getTile(0,0)
                    ptemp[2] = self.face3.getTile(2,0)
                elif self.face2.getFaceColor() == 3:
                    ptemp[0] = self.face1.getTile(2,0)
                    ptemp[1] = self.face2.getTile(2,2)
                    ptemp[2] = self.face3.getTile(2,0)
                else:
                    ptemp[0] = self.face1.getTile(2,2)
                    ptemp[1] = self.face2.getTile(0,0)
                    ptemp[2] = self.face3.getTile(2,0)
            elif self.face1.getFaceColor() == 1: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,0)
                    ptemp[1] = self.face2.getTile(2,0)
                    ptemp[2] = self.face3.getTile(0,2)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(0,2)
                    ptemp[1] = self.face2.getTile(0,0)
                    ptemp[2] = self.face3.getTile(2,2)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(2,0)
                    ptemp[1] = self.face2.getTile(2,2)
                    ptemp[2] = self.face3.getTile(0,0)
                else:
                    ptemp[0] = self.face1.getTile(2,2)
                    ptemp[1] = self.face2.getTile(0,2)
                    ptemp[2] = self.face3.getTile(2,0)
            elif self.face1.getFaceColor() == 2: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,0)
                    ptemp[1] = self.face2.getTile(2,2)
                    ptemp[2] = self.face3.getTile(0,2)
                elif self.face2.getFaceColor() == 3:
                    ptemp[0] = self.face1.getTile(0,2)
                    ptemp[1] = self.face2.getTile(0,0)
                    ptemp[2] = self.face3.getTile(0,2)
                elif self.face2.getFaceColor() == 1:
                    ptemp[0] = self.face1.getTile(2,0)
                    ptemp[1] = self.face2.getTile(2,2)
                    ptemp[2] = self.face3.getTile(0,2)
                else:
                    ptemp[0] = self.face1.getTile(2,2)
                    ptemp[1] = self.face2.getTile(2,2)
                    ptemp[2] = self.face3.getTile(2,0)
            elif self.face1.getFaceColor() == 3: 
                if self.face2.getFaceColor() == 4:
                    ptemp[0] = self.face1.getTile(0,0)
                    ptemp[1] = self.face2.getTile(0,2)
                    ptemp[2] = self.face3.getTile(0,2)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(0,2)
                    ptemp[1] = self.face2.getTile(0,0)
                    ptemp[2] = self.face3.getTile(0,0)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(2,0)
                    ptemp[1] = self.face2.getTile(2,2)
                    ptemp[2] = self.face3.getTile(2,2)
                else:
                    ptemp[0] = self.face1.getTile(2,2)
                    ptemp[1] = self.face2.getTile(2,0)
                    ptemp[2] = self.face3.getTile(2,0)
            elif self.face1.getFaceColor() == 4: 
                if self.face2.getFaceColor() == 3:
                    ptemp[0] = self.face1.getTile(0,0)
                    ptemp[1] = self.face2.getTile(0,2)
                    ptemp[2] = self.face3.getTile(0,0)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(0,2)
                    ptemp[1] = self.face2.getTile(0,2)
                    ptemp[2] = self.face3.getTile(0,0)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(2,0)
                    ptemp[1] = self.face2.getTile(0,2)
                    ptemp[2] = self.face3.getTile(0,0)
                else:
                    ptemp[0] = self.face1.getTile(2,2)
                    ptemp[1] = self.face2.getTile(0,2)
                    ptemp[2] = self.face3.getTile(0,0)
            else: 
                if self.face2.getFaceColor() == 1:
                    ptemp[0] = self.face1.getTile(0,0)
                    ptemp[1] = self.face2.getTile(2,0)
                    ptemp[2] = self.face3.getTile(2,2)
                elif self.face2.getFaceColor() == 2:
                    ptemp[0] = self.face1.getTile(0,2)
                    ptemp[1] = self.face2.getTile(2,0)
                    ptemp[2] = self.face3.getTile(2,2)
                elif self.face2.getFaceColor() == 0:
                    ptemp[0] = self.face1.getTile(2,0)
                    ptemp[1] = self.face2.getTile(2,0)
                    ptemp[2] = self.face3.getTile(2,2)
                else:
                    ptemp[0] = self.face1.getTile(2,2)
                    ptemp[1] = self.face2.getTile(2,0)
                    ptemp[2] = self.face3.getTile(2,2)
        return ptemp

class Cube:
    def __init__(self, r = Face(), g = Face(), o = Face(), b = Face(),\
                 y = Face(), w = Face()):
        self.Red = r
        self.Green = g
        self.Orange = o
        self.Blue = b
        self.Yellow = y
        self.White = w
        self.arrOfMoves = []
        self.arrCond = []
        self.arrSolution = []
        
    def solveCube(self):
        self.yellowCross()
        self.yellowCorners()
        self.middlelayer()
        self.bottomcross()
        self.bottomcross2()
        self.bottomcorners()
        self.laststep()
        return self.retcondensedmoves()
        
    def getFace(self, facenum):
        if facenum == 0:
            return self.Red
        elif facenum == 1:
            return self.Green
        elif facenum == 2:
            return self.Orange
        elif facenum == 3:
            return self.Blue
        elif facenum == 4:
            return self.Yellow
        else:
            return self.White
    def getFaceString(self, facenum):
        if facenum == 0:
            return "Red"
        elif facenum == 1:
            return "Green"
        elif facenum == 2:
            return "Orange"
        elif facenum == 3:
            return "Blue"
        elif facenum == 4:
            return "Yellow"
        else:
            return "White"
    def addmove(self, str):
        self.arrOfMoves.append(str)
    def rotateFaceR(self, f):
        if f.getFaceColor() == 0:
            temp = self.Yellow.get3left()
            self.Red.rotateR()
            self.Yellow.set3left(self.Blue.get3right())
            self.Blue.set3right(self.White.get3left())
            self.White.set3left(self.Green.get3left())
            self.Green.set3left(temp)
        elif f.getFaceColor() == 1:
            temp = self.Yellow.get3bot()
            self.Green.rotateR()
            self.Yellow.set3bot(self.Red.get3right())
            self.Red.set3right(self.White.get3top())
            self.White.set3top(self.Orange.get3left())
            self.Orange.set3left(temp)
        elif f.getFaceColor() == 2:
            temp = self.Yellow.get3right()
            self.Orange.rotateR()
            self.Yellow.set3right(self.Green.get3right())
            self.Green.set3right(self.White.get3right())
            self.White.set3right(self.Blue.get3left())
            self.Blue.set3left(temp)
        elif f.getFaceColor() == 3:
            temp = self.Yellow.get3top()
            self.Blue.rotateR()
            self.Yellow.set3top(self.Orange.get3right())
            self.Orange.set3right(self.White.get3bot())
            self.White.set3bot(self.Red.get3left())
            self.Red.set3left(temp)
        elif f.getFaceColor() == 4:
            temp = self.Blue.get3top()
            self.Yellow.rotateR()
            self.Blue.set3top(self.Red.get3top())
            self.Red.set3top(self.Green.get3top())
            self.Green.set3top(self.Orange.get3top())
            self.Orange.set3top(temp)
        else:
            temp = self.Green.get3bot()
            self.White.rotateR()
            self.Green.set3bot(self.Red.get3bot())
            self.Red.set3bot(self.Blue.get3bot())
            self.Blue.set3bot(self.Orange.get3bot())
            self.Orange.set3bot(temp)
    def rotateFaceL(self, f):
        if f.getFaceColor() == 0:
            temp = self.Yellow.get3left()
            self.Red.rotateL()
            self.Yellow.set3left(self.Green.get3left())
            self.Green.set3left(self.White.get3left())
            self.White.set3left(self.Blue.get3right())
            self.Blue.set3right(temp)
        elif f.getFaceColor() == 1:
            temp = self.Yellow.get3bot()
            self.Green.rotateL()
            self.Yellow.set3bot(self.Orange.get3left())
            self.Orange.set3left(self.White.get3top())
            self.White.set3top(self.Red.get3right())
            self.Red.set3right(temp)
        elif f.getFaceColor() == 2:
            temp = self.Yellow.get3right()
            self.Orange.rotateL()
            self.Yellow.set3right(self.Blue.get3left())
            self.Blue.set3left(self.White.get3right())
            self.White.set3right(self.Green.get3right())
            self.Green.set3right(temp)
        elif f.getFaceColor() == 3:
            temp = self.Yellow.get3top()
            self.Blue.rotateL()
            self.Yellow.set3top(self.Red.get3left())
            self.Red.set3left(self.White.get3bot())
            self.White.set3bot(self.Orange.get3right())
            self.Orange.set3right(temp)
        elif f.getFaceColor() == 4:
            temp = self.Blue.get3top()
            self.Yellow.rotateL()
            self.Blue.set3top(self.Orange.get3top())
            self.Orange.set3top(self.Green.get3top())
            self.Green.set3top(self.Red.get3top())
            self.Red.set3top(temp)
        else:
            temp = self.Green.get3bot()
            self.White.rotateL()
            self.Green.set3bot(self.Orange.get3bot())
            self.Orange.set3bot(self.Blue.get3bot())
            self.Blue.set3bot(self.Red.get3bot())
            self.Red.set3bot(temp)
    def returnPiece(self, f, i, j): #returns a piece at a given index on a given Face
        if (i+j)%2 == 1: #if index corresponds to a side piece
            if f.getFaceColor() == 0:
                if i == 0 and j == 1:
                    p = Piece(f, self.Yellow)
                elif i == 1 and j == 0:
                    p = Piece(f, self.Blue)
                elif i == 1 and j == 2:
                    p = Piece(f, self.Green)
                else:
                    p = Piece(f, self.White)
            elif f.getFaceColor() == 1:
                if i == 0 and j == 1:
                    p = Piece(f, self.Yellow)
                elif i == 1 and j == 0:
                    p = Piece(f, self.Red)
                elif i == 1 and j == 2:
                    p = Piece(f, self.Orange)
                else:
                    p = Piece(f, self.White)
            elif f.getFaceColor() == 2:
                if i == 0 and j == 1:
                    p = Piece(f, self.Yellow)
                elif i == 1 and j == 0:
                    p = Piece(f, self.Green)
                elif i == 1 and j == 2:
                    p = Piece(f, self.Blue)
                else:
                    p = Piece(f, self.White)
            elif f.getFaceColor() == 3:
                if i == 0 and j == 1:
                    p = Piece(f, self.Yellow)
                elif i == 1 and j == 0:
                    p = Piece(f, self.Orange)
                elif i == 1 and j == 2:
                    p = Piece(f, self.Red)
                else:
                    p = Piece(f, self.White)
            elif f.getFaceColor() == 4:
                if i == 0 and j == 1:
                    p = Piece(f, self.Blue)
                elif i == 1 and j == 0:
                    p = Piece(f, self.Red)
                elif i == 1 and j == 2:
                    p = Piece(f, self.Orange)
                else:
                    p = Piece(f, self.Green)
            else:
                if i == 0 and j == 1:
                    p = Piece(f, self.Green)
                elif i == 1 and j == 0:
                    p = Piece(f, self.Red)
                elif i == 1 and j == 2:
                    p = Piece(f, self.Orange)
                else:
                    p = Piece(f, self.Blue)
        else: #corner piece
            if f.getFaceColor() == 0:
                if i == 0 and j == 0:
                    p = Piece(f, self.Yellow, self.Blue)
                elif i == 0 and j == 2:
                    p = Piece(f, self.Green, self.Yellow)
                elif i == 2 and j == 0:
                    p = Piece(f, self.Blue, self.White)
                else:
                    p = Piece(f, self.White, self.Green)
            elif f.getFaceColor() == 1:
                if i == 0 and j == 0:
                    p = Piece(f, self.Yellow, self.Red)
                elif i == 0 and j == 2:
                    p = Piece(f, self.Orange, self.Yellow)
                elif i == 2 and j == 0:
                    p = Piece(f, self.Red, self.White)
                else:
                    p = Piece(f, self.White, self.Orange)
            elif f.getFaceColor() == 2:
                if i == 0 and j == 0:
                    p = Piece(f, self.Yellow, self.Green)
                elif i == 0 and j == 2:
                    p = Piece(f, self.Blue, self.Yellow)
                elif i == 2 and j == 0:
                    p = Piece(f, self.Green, self.White)
                else:
                    p = Piece(f, self.White, self.Blue)
            elif f.getFaceColor() == 3:
                if i == 0 and j == 0:
                    p = Piece(f, self.Yellow, self.Orange)
                elif i == 0 and j == 2:
                    p = Piece(f, self.Red, self.Yellow)
                elif i == 2 and j == 0:
                    p = Piece(f, self.Orange, self.White)
                else:
                    p = Piece(f, self.White, self.Red)
            elif f.getFaceColor() == 4:
                if i == 0 and j == 0:
                    p = Piece(f, self.Blue, self.Red)
                elif i == 0 and j == 2:
                    p = Piece(f, self.Orange, self.Blue)
                elif i == 2 and j == 0:
                    p = Piece(f, self.Red, self.Green)
                else:
                    p = Piece(f, self.Green, self.Orange)
            else:
                if i == 0 and j == 0:
                    p = Piece(f, self.Green, self.Red)
                elif i == 0 and j == 2:
                    p = Piece(f, self.Orange, self.Green)
                elif i == 2 and j == 0:
                    p = Piece(f, self.Red, self.Blue)
                else:
                    p = Piece(f, self.Blue, self.Orange)
        return p
    def sideP_arr(self):
        piece_arr = []
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if (j+k)%2 != 0: #meaning side piece
                        piece_arr.append(self.returnPiece(self.getFace(i), j, k))
        return piece_arr
    def cornerP_arr(self):
        piece_arr = []
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if (j+k)%2 == 0 and j != 1: #meaning corner piece (j!=1 to exclude center)
                        piece_arr.append(self.returnPiece(self.getFace(i), j, k))
        return piece_arr
    def begin_ycross(self, faceval):
        piece_arr = self.sideP_arr()
        for i in range(len(piece_arr)):
            x = piece_arr[i].getArrPColor()[0]
            y = piece_arr[i].getArrPColor()[1]
            if x == faceval and y == 4:
                correctpiece = piece_arr[i]
        if faceval == 0:
            c = 1; d = 0
        elif faceval == 1:
            c = 2; d = 1
        elif faceval == 2:
            c = 1; d = 2
        else:
            c = 0; d = 1
        while (self.getFace(faceval).getTile(0,1) != faceval or self.Yellow.getTile(c,d) != 4)\
                and (self.getFace(faceval).getTile(0,1) != 4 or self.Yellow.getTile(c,d) != faceval):
            if correctpiece.getFColor(1) == faceval or correctpiece.getFColor(2) == faceval:
                self.rotateFaceR(self.getFace(faceval))
                self.addmove(self.getFaceString(faceval) + " right")
            elif correctpiece.getFColor(1) == 5 or correctpiece.getFColor(2) == 5:
                self.rotateFaceR(self.White)
                self.addmove("White right")
            elif correctpiece.getFColor(1) == 4:
                if faceval == 0:
                    self.rotateFaceR(self.Yellow)
                    self.addmove("Yellow right")              
                elif (correctpiece.getFColor(2)+1)%4 == faceval:
                    self.rotateFaceR(correctpiece.getFace2())
                    self.addmove(correctpiece.getFName(2) + " right")
                else:
                    self.rotateFaceL(correctpiece.getFace2())
                    self.addmove(correctpiece.getFName(2) + " left")
            elif correctpiece.getFColor(2) == 4:
                if faceval == 0:
                    self.rotateFaceR(self.Yellow)
                    self.addmove("Yellow right")

                elif (correctpiece.getFColor(1)+1)%4 == faceval:
                    self.rotateFaceR(correctpiece.getFace1())
                    self.addmove(correctpiece.getFName(1) + " right")
                else:
                    self.rotateFaceL(correctpiece.getFace1())
                    self.addmove(correctpiece.getFName(1) + " left")          
            else:
                a = (faceval+1)%4
                b = (faceval+2)%4
                if correctpiece.getFColor(1) == a or correctpiece.getFColor(2) == a:
                    self.rotateFaceL(self.getFace(b))
                    self.addmove(self.getFaceString(b) + " left")
                    self.rotateFaceR(self.White)
                    self.addmove("White right")
                    self.rotateFaceR(self.getFace(b))
                    self.addmove(self.getFaceString(b) + " right")
                else:
                    self.rotateFaceR(self.getFace(b))
                    self.addmove(self.getFaceString(b) + " right")
                    self.rotateFaceR(self.White)
                    self.addmove("White right")
                    self.rotateFaceL(self.getFace(b))
                    self.addmove(self.getFaceString(b) + " left")
            piece_arr = self.sideP_arr()
            for i in range(len(piece_arr)):
                x = piece_arr[i].getArrPColor()[0]
                y = piece_arr[i].getArrPColor()[1]
                if x == faceval and y == 4:
                    correctpiece = piece_arr[i]
        if self.getFace(faceval).getTile(0,1) == 4 and self.Yellow.getTile(c,d) == faceval:
            if faceval == 0:
                e = 3
            else:
                e = faceval - 1
            self.rotateFaceL(self.getFace(faceval))
            self.addmove(self.getFaceString(faceval) + " left")
            self.rotateFaceL(self.getFace(faceval))
            self.addmove(self.getFaceString(faceval) + " left")
            self.rotateFaceL(self.White)
            self.addmove("White left")
            self.rotateFaceL(self.getFace(e))
            self.addmove(self.getFaceString(e) + " left")
            self.rotateFaceR(self.getFace(faceval))
            self.addmove(self.getFaceString(faceval) + " right")
            self.rotateFaceR(self.getFace(e))
            self.addmove(self.getFaceString(e) + " right")
    def yellowCross(self):
        self.begin_ycross(0)
        self.begin_ycross(1)
        self.begin_ycross(2)
        self.begin_ycross(3)
    def yellowCorners(self):
        p1 = Piece(self.Yellow, self.Red, self.Green)
        p2 = Piece(self.Yellow, self.Green, self.Orange)
        p3 = Piece(self.Yellow, self.Orange, self.Blue)
        p4 = Piece(self.Yellow, self.Blue, self.Red)
        p5 = Piece(self.Red, self.White, self.Green)
        p6 = Piece(self.Green, self.White, self.Orange)
        p7 = Piece(self.Orange, self.White, self.Blue)
        p8 = Piece(self.Blue, self.White, self.Red)
        orig_PieceArr = [p1,p2,p3,p4,p5,p6,p7,p8]
        numreps = 0
        for i in range(4):
            a = orig_PieceArr[i].getFColor(1)
            b = orig_PieceArr[i].getFColor(2)
            c = orig_PieceArr[i].getFColor(3)
            d = orig_PieceArr[i].getArrPColor()[0]
            e = orig_PieceArr[i].getArrPColor()[1]
            f = orig_PieceArr[i].getArrPColor()[2]
            u = orig_PieceArr[i+4].getFColor(1)
            v = orig_PieceArr[i+4].getFColor(2)
            w = orig_PieceArr[i+4].getFColor(3)
            while a != d or b != e or c != f:
                cp_arr = self.cornerP_arr()
                for cp in cp_arr:
                    x = cp.getArrPColor()[0]
                    y = cp.getArrPColor()[1]
                    z = cp.getArrPColor()[2]
                    if x == a and y == b and z == c:
                        correctpiece = cp
                g1 = correctpiece.getFColor(1)
                g2 = correctpiece.getFColor(2)
                g3 = correctpiece.getFColor(3)
                if ((g1 == a or g2 == a or g3 == a) and (g1 == b or g2 == b or g3 == b)\
                    and (g1 == c or g2 == c or g3 == c)) or ((g1 == u or g2 == u or g3 == u)\
                    and (g1 == v or g2 == v or g3 == v) and (g1 == w or g2 == w or g3 == w)):
                    self.rotateFaceL(orig_PieceArr[i].getFace3())
                    self.rotateFaceL(self.White)
                    self.rotateFaceR(orig_PieceArr[i].getFace3())
                    self.rotateFaceR(self.White)
                    numreps += 1
                elif g1 == 5 or g2 == 5 or g3 == 5:
                    self.rotateFaceR(self.White)
                    self.addmove("White right")
                else:
                    if g1 == 4:
                        facetoturn = g3
                    elif g2 == 4:
                        facetoturn = g1
                    else:
                        facetoturn = g2
                    self.rotateFaceL(self.getFace(facetoturn))
                    self.addmove(self.getFaceString(facetoturn) + " left")
                    self.rotateFaceL(self.White)
                    self.addmove("White left")
                    self.rotateFaceR(self.getFace(facetoturn))
                    self.addmove(self.getFaceString(facetoturn) + " right")
                    self.rotateFaceR(self.White)
                    self.addmove("White right")
                p1 = Piece(self.Yellow, self.Red, self.Green)
                p2 = Piece(self.Yellow, self.Green, self.Orange)
                p3 = Piece(self.Yellow, self.Orange, self.Blue)
                p4 = Piece(self.Yellow, self.Blue, self.Red)
                p5 = Piece(self.Red, self.White, self.Green)
                p6 = Piece(self.Green, self.White, self.Orange)
                p7 = Piece(self.Orange, self.White, self.Blue)
                p8 = Piece(self.Blue, self.White, self.Red)
                orig_PieceArr = [p1,p2,p3,p4,p5,p6,p7,p8]
                d = orig_PieceArr[i].getArrPColor()[0]
                e = orig_PieceArr[i].getArrPColor()[1]
                f = orig_PieceArr[i].getArrPColor()[2]    
            if numreps > 3:
                for repcount in range(numreps):
                    self.rotateFaceL(self.White)
                    self.rotateFaceL(orig_PieceArr[i].getFace3())
                    self.rotateFaceR(self.White)
                    self.rotateFaceR(orig_PieceArr[i].getFace3())
                for repcount2 in range(6-numreps):
                    self.rotateFaceR(orig_PieceArr[i].getFace2())
                    self.addmove(self.getFaceString(orig_PieceArr[i].getFColor(2)) + " right")
                    self.rotateFaceR(self.White)
                    self.addmove("White right")
                    self.rotateFaceL(orig_PieceArr[i].getFace2())
                    self.addmove(self.getFaceString(orig_PieceArr[i].getFColor(2)) + " left")
                    self.rotateFaceL(self.White)
                    self.addmove("White left")
            else:
                for r in range(numreps):
                    self.addmove(self.getFaceString(orig_PieceArr[i].getFColor(3)) + " left")
                    self.addmove("White left")
                    self.addmove(self.getFaceString(orig_PieceArr[i].getFColor(3)) + " right")
                    self.addmove("White right")
            numreps = 0
    def checkmiddlelayer(self):
        count = 0
        for i in range(4):
            if self.getFace(i).getTile(1,0) == (i) and self.getFace(i).getTile(1,2) == (i):
                count += 1
        if count == 4:
            return True
        else:
            return False
    def middlelayer(self):
        counter = 0
        while self.checkmiddlelayer() == False:
            for i in range(4):
                sideP = self.returnPiece(self.getFace(i), 1, 2)
                a = sideP.getFColor(1)
                b = sideP.getFColor(2)
                if a != sideP.getArrPColor()[0] or b != sideP.getArrPColor()[1]:
                    sidepieces = self.sideP_arr()
                    for sp in sidepieces:
                        x = sp.getArrPColor()[0]
                        y = sp.getArrPColor()[1]
                        if x == a and y == b:
                            correctpiece = sp
                    if correctpiece.getFColor(1) == 5 or correctpiece.getFColor(2) == 5:
                        while correctpiece.getFColor(2) != b and correctpiece.getFColor(1) != a:
                            self.rotateFaceR(self.White)
                            self.addmove("White right")
                            sidepieces = self.sideP_arr()
                            for sp in sidepieces:
                                x = sp.getArrPColor()[0]
                                y = sp.getArrPColor()[1]
                                if x == a and y == b:
                                    correctpiece = sp
                        if correctpiece.getFColor(1) == 5:
                            self.rotateFaceR(self.White)
                            self.addmove("White right")
                            self.rotateFaceR(sideP.getFace1())
                            self.addmove(sideP.getFName(1) + " right")
                            self.rotateFaceL(self.White)
                            self.addmove("White left")
                            self.rotateFaceL(sideP.getFace1())
                            self.addmove(sideP.getFName(1) + " left")
                            self.rotateFaceL(self.White)
                            self.addmove("White left")
                            self.rotateFaceL(sideP.getFace2())
                            self.addmove(sideP.getFName(2) + " left")
                            self.rotateFaceR(self.White)
                            self.addmove("White right")
                            self.rotateFaceR(sideP.getFace2())
                            self.addmove(sideP.getFName(2) + " right")
                        else:
                            self.rotateFaceL(self.White)
                            self.addmove("White left")
                            self.rotateFaceL(sideP.getFace2())
                            self.addmove(sideP.getFName(2) + " left")
                            self.rotateFaceR(self.White)
                            self.addmove("White right")
                            self.rotateFaceR(sideP.getFace2())
                            self.addmove(sideP.getFName(2) + " right")
                            self.rotateFaceR(self.White)
                            self.addmove("White right")
                            self.rotateFaceR(sideP.getFace1())
                            self.addmove(sideP.getFName(1) + " right")
                            self.rotateFaceL(self.White)
                            self.addmove("White left")
                            self.rotateFaceL(sideP.getFace1())
                            self.addmove(sideP.getFName(1) + " left")
            counter += 1
            if counter > 3:
                c = 0; q = 0
                while q <= 3 and c == 0:
                    sideP = self.returnPiece(self.getFace(q), 1, 2)
                    a = sideP.getFColor(1)
                    b = sideP.getFColor(2)
                    if (a == sideP.getArrPColor()[1] and b == sideP.getArrPColor()[0])\
                        or (a != sideP.getArrPColor()[0] or b != sideP.getArrPColor()[1]):
                        self.rotateFaceR(self.White)
                        self.addmove("White right")
                        self.rotateFaceR(sideP.getFace1())
                        self.addmove(sideP.getFName(1) + " right")
                        self.rotateFaceL(self.White)
                        self.addmove("White left")
                        self.rotateFaceL(sideP.getFace1())
                        self.addmove(sideP.getFName(1) + " left")
                        self.rotateFaceL(self.White)
                        self.addmove("White left")
                        self.rotateFaceL(sideP.getFace2())
                        self.addmove(sideP.getFName(2) + " left")
                        self.rotateFaceR(self.White)
                        self.addmove("White right")
                        self.rotateFaceR(sideP.getFace2())
                        self.addmove(sideP.getFName(2) + " right")
                        c = 1
                    q += 1
                counter = 0
    def bottomcross(self):
        while self.White.getTile(0,1) != 5 or self.White.getTile(1,0) != 5\
            or self.White.getTile(1,2) != 5 or self.White.getTile(2,1) != 5:
            if (self.White.getTile(0,1) == 5 and self.White.getTile(2,1) == 5)\
                or (self.White.getTile(1,0) == 5 and self.White.getTile(1,2) == 5):
                for i in range(4):
                    if self.getFace(i).getTile(2,1) == 5:
                        x = i
                z = (x+3)%4
                self.rotateFaceR(self.getFace(x))
                self.addmove(self.getFaceString(x) + " right")
                self.rotateFaceR(self.getFace(z))
                self.addmove(self.getFaceString(z) + " right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.getFace(z))
                self.addmove(self.getFaceString(z) + " left")
                self.rotateFaceL(self.White)
                self.addmove("White left")
                self.rotateFaceL(self.getFace(x))
                self.addmove(self.getFaceString(x) + " left")
            elif self.White.getTile(0,1) != 5 and self.White.getTile(1,0) != 5\
                and self.White.getTile(1,2) != 5 and self.White.getTile(2,1) != 5:
                self.rotateFaceR(self.Green)
                self.addmove("Green right")
                self.rotateFaceR(self.Red)
                self.addmove("Red right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.Red)
                self.addmove("Red left")
                self.rotateFaceL(self.White)
                self.addmove("White left")
                self.rotateFaceL(self.Green)
                self.addmove("Green left")
            else:
                for j in range(4):
                    if self.getFace(j).getTile(2,1) == 5\
                        and self.getFace((j+1)%4).getTile(2,1) == 5:
                        y = j
                nextface = (y+1)%4
                self.rotateFaceR(self.getFace(nextface))
                self.addmove(self.getFaceString(nextface) + " right")
                self.rotateFaceR(self.getFace(y))
                self.addmove(self.getFaceString(y) + " right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.getFace(y))
                self.addmove(self.getFaceString(y) + " left")
                self.rotateFaceL(self.White)
                self.addmove("White left")
                self.rotateFaceL(self.getFace(nextface))
                self.addmove(self.getFaceString(nextface) + " left")
    def bottomcross2(self):
        while self.Red.getTile(2,1) != 0:
            self.rotateFaceR(self.White)
            self.addmove("White right")
        if self.Red.getTile(2,1) != 0 or self.Green.getTile(2,1) != 1\
            or self.Orange.getTile(2,1) != 2 or self.Blue.getTile(2,1) != 3:
            while self.Blue.getTile(2,1) != 3:
                self.rotateFaceR(self.Blue)
                self.addmove("Blue right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.Blue)
                self.addmove("Blue left")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceR(self.Blue)
                self.addmove("Blue right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.Blue)
                self.addmove("Blue left")
            if self.Green.getTile(2,1) != 1:
                self.rotateFaceR(self.Red)
                self.addmove("Red right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.Red)
                self.addmove("Red left")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceR(self.Red)
                self.addmove("Red right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.Red)
                self.addmove("Red left")
            if self.Green.getTile(2,1) != 1:
                self.rotateFaceR(self.White)
                self.addmove("White right")
    def bottomcorners(self):
        correctpiece = Piece()
        i = 0
        while correctpiece.getFace1().getArr()[1][1] == -1:
            p = self.returnPiece(self.getFace(i),2,2)
            a = p.getFColor(1); b = p.getFColor(2); c = p.getFColor(3)
            d1 = p.getArrPColor()[0]; d2 = p.getArrPColor()[1]; d3 = p.getArrPColor()[2]
            if (d1 == a or d1 == b or d1 == c) and (d2 == a or d2 == b or d2 ==c)\
                and (d3 == a or d3 == b or d3 == c):
                correctpiece = p
                break
            i+= 1
            if i > 3:
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceR(self.Red)
                self.addmove("Red right")
                self.rotateFaceL(self.White)
                self.addmove("White left")
                self.rotateFaceL(self.Orange)
                self.addmove("Orange left")
                self.rotateFaceR(self.White)
                self.addmove("White right")
                self.rotateFaceL(self.Red)
                self.addmove("Red left")
                self.rotateFaceL(self.White)
                self.addmove("White left")
                self.rotateFaceR(self.Orange)
                self.addmove("Orange right")
                i = 0
        nextcpiece = self.returnPiece(self.getFace(correctpiece.getFColor(3)),2,2)
        x = nextcpiece.getFColor(1)
        y = nextcpiece.getFColor(2)
        z = nextcpiece.getFColor(3)
        w1 = nextcpiece.getArrPColor()[0]
        w2 = nextcpiece.getArrPColor()[1]
        w3 = nextcpiece.getArrPColor()[2]
        while (w1 != x and w1 != y and w1 != z) or (w2 != x and w2 != y and w2 != z)\
            or (w3 != x and w3 != y and w3 != z):
            self.rotateFaceR(self.White)
            self.addmove("White right")
            self.rotateFaceR(correctpiece.getFace1())
            self.addmove(correctpiece.getFName(1) + " right")
            self.rotateFaceL(self.White)
            self.addmove("White left")
            self.rotateFaceL(nextcpiece.getFace3())
            self.addmove(nextcpiece.getFName(3) + " left")
            self.rotateFaceR(self.White)
            self.addmove("White right")
            self.rotateFaceL(correctpiece.getFace1())
            self.addmove(correctpiece.getFName(1) + " left")
            self.rotateFaceL(self.White)
            self.addmove("White left")
            self.rotateFaceR(nextcpiece.getFace3())
            self.addmove(nextcpiece.getFName(3) + " right")
            nextcpiece = self.returnPiece(self.getFace(correctpiece.getFColor(3)),2,2)
            w1 = nextcpiece.getArrPColor()[0]
            w2 = nextcpiece.getArrPColor()[1]
            w3 = nextcpiece.getArrPColor()[2]
    def laststep(self):
        p = Piece(self.White, self.Green, self.Red)
        while p.getArrPColor()[0] != 5 or p.getArrPColor()[1] != 1 or p.getArrPColor()[2] != 0:
            self.rotateFaceL(self.Red)
            self.addmove("Red left")
            self.rotateFaceL(self.Yellow)
            self.addmove("Yellow left")
            self.rotateFaceR(self.Red)
            self.addmove("Red right")
            self.rotateFaceR(self.Yellow)
            self.addmove("Yellow right")
            p = Piece(self.White, self.Green, self.Red)
        self.rotateFaceR(self.White)
        self.addmove("White right")
        p = Piece(self.White, self.Green, self.Red)
        while p.getArrPColor()[0] != 5 or p.getArrPColor()[1] != 0 or p.getArrPColor()[2] != 3:
            self.rotateFaceL(self.Red)
            self.addmove("Red left")
            self.rotateFaceL(self.Yellow)
            self.addmove("Yellow left")
            self.rotateFaceR(self.Red)
            self.addmove("Red right")
            self.rotateFaceR(self.Yellow)
            self.addmove("Yellow right")
            p = Piece(self.White, self.Green, self.Red)
        self.rotateFaceR(self.White)
        self.addmove("White right")
        p = Piece(self.White, self.Green, self.Red)
        while p.getArrPColor()[0] != 5 or p.getArrPColor()[1] != 3 or p.getArrPColor()[2] != 2:
            self.rotateFaceL(self.Red)
            self.addmove("Red left")
            self.rotateFaceL(self.Yellow)
            self.addmove("Yellow left")
            self.rotateFaceR(self.Red)
            self.addmove("Red right")
            self.rotateFaceR(self.Yellow)
            self.addmove("Yellow right")
            p = Piece(self.White, self.Green, self.Red)
        self.rotateFaceR(self.White)
        self.addmove("White right")
        p = Piece(self.White, self.Green, self.Red)   
        while p.getArrPColor()[0] != 5 or p.getArrPColor()[1] != 2 or p.getArrPColor()[2] != 1:
            self.rotateFaceL(self.Red)
            self.addmove("Red left")
            self.rotateFaceL(self.Yellow)
            self.addmove("Yellow left")
            self.rotateFaceR(self.Red)
            self.addmove("Red right")
            self.rotateFaceR(self.Yellow)
            self.addmove("Yellow right")
            p = Piece(self.White, self.Green, self.Red)
        while self.Green.getTile(2,0) != 1:
            self.rotateFaceR(self.White)
            self.addmove("White right")
    def printmoves(self):
       for i in range(len(self.arrOfMoves)):
           print (i+1, self.arrOfMoves[i])
    def retcondensedmoves(self):
        arr = self.arrOfMoves[:]
        prior = 0
        while prior != len(arr):
            prior = len(arr)
            i = 0; k = 0
            while i < (len(arr)-2):
                if arr[i] == arr[i+1] and arr[i] == arr[i+2]:
                    loc = arr[i].find(" ")
                    temp = arr[i][:loc]
                    if arr[i].find("right") != -1:
                        temp += " left"
                    else:
                        temp += " right"
                    arr.pop(i)
                    arr.pop(i)
                    arr.pop(i)
                    arr.insert(i, temp)
                    if i > 1:
                        i -= 2
                else:
                    i += 1
            while k < (len(arr) - 1):
                locator = arr[k].find(" ")
                if arr[k] != arr[k+1] and arr[k][:locator] == arr[k+1][:locator]:
                    arr.pop(k)
                    arr.pop(k)
                    if k > 0:
                        k -= 1
                else:
                    k += 1
        return arr
    def printcondensedmoves(self):
        condmoves = self.retcondensedmoves()
        for m in range(len(condmoves)):
            print(m+1, condmoves[m]) 






        
