import turtle
import const
###########################################################
##
##                   DISPLAY
##
###########################################################

class BattleshipsGraphics:

    def __init__(self, gridSize):
        self.turtle = turtle.Turtle()
        self.screen = turtle.getscreen()
        self.screen.setup(width = 1200, height = 750, startx = None, starty = None)
        self.screen.register_shape(const.MISSED_GIF)
        self.screen.register_shape(const.HIT_GIF)
        self.screen.register_shape(const.WINNER_GIF)
        self.screen.register_shape(const.LOOSER_GIF)
        self.screen.bgpic(const.BOARD_BKG_GIF)
        self.turtle.speed(0)
        self.turtle.color("black")
        self.squareSize = 40
        self.gridSize = gridSize
        self.turtle.tracer(1,0)
        self.turtle.goto(0,0)
        self.turtle.showturtle()

    def setScreenSize(self, width, height):
        self.screen.setup(width = width, height = height, startx = None, starty = None)

    def setSquareSize(self, squareSize):
        self.squareSize = squareSize

    # Draw a line from (x1, y1) to (x2, y2)
    def _drawLine(self, x1, y1, x2, y2):
        self.turtle.penup()
        self.turtle.goto(x1, y1)
        self.turtle.pendown()
        self.turtle.goto(x2, y2)
        self.turtle.penup()

    # Write a text at the specified location (x, y)
    def _writeText(self, s, x, y, font=("Arial", 16, "bold")):
        self.turtle.penup() # Pull the pen up
        self.turtle.goto(x, y)
        self.turtle.pendown() # Pull the pen down
        self.turtle.write(s, align = 'center', font = font) # Write a string
        self.turtle.penup()

    # Draw a point at the specified location (x, y)
    def _drawPoint(self, x, y):
        self.turtle.penup() # Pull the pen up
        self.turtle.goto(x, y)
        self.turtle.pendown() # Pull the pen down
        self.turtle.begin_fill() # Begin to fill color in a shape
        self.turtle.circle(3)
        self.turtle.end_fill() # Fill the shape
        self.turtle.penup()

    # Draw a circle at centered at (x, y) with the specified radius
    def _fillCircle(self, x, y, radius):
        self.turtle.penup() # Pull the pen up
        self.turtle.fill(True)
        self.turtle.goto(x, y - radius)
        self.turtle.pendown() # Pull the pen down
        self.turtle.circle(radius)
        self.turtle.fill(False)
        self.turtle.penup()

    # Draw a rectangle at (x, y) with the specified width and height
    def _fillRectangle(self, x, y, width, height):
        self.turtle.penup() # Pull the pen up
        self.turtle.fill(True)
        self.turtle.setheading(0)
        self.turtle.goto(x, y)
        self.turtle.pendown() # Pull the pen down
        self.turtle.forward(width)
        self.turtle.right(90)
        self.turtle.forward(height)
        self.turtle.right(90)
        self.turtle.forward(width)
        self.turtle.right(90)
        self.turtle.forward(height)
        self.turtle.penup() # Pull the pen up
        self.turtle.fill(False)
        self.turtle.setheading(0)
        self.turtle.penup()

    def drawBoat(self, board, row, col):
        width = self.screen.window_width()
        height = self.screen.window_height()
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            left = -self.gridSize * self.squareSize - marginw
        else:
            left = marginw
        self.turtle.color("black", "darkgrey")
        self._fillRectangle(left + col * self.squareSize, top - row * self.squareSize,
                      self.squareSize, self.squareSize)
        self.turtle.penup()

    def drawMiss(self, board, row, col):
        width = self.screen.window_width()
        height = self.screen.window_height()
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            left = -self.gridSize * self.squareSize - marginw
        else:
            left = marginw
        self.turtle.color("black", "blue")
        self.turtle.shape(const.MISSED_GIF)
        self.turtle.penup()
        self.turtle.goto(left + col * self.squareSize + self.squareSize / 2,
                   top - row * self.squareSize - self.squareSize / 2)
        self.turtle.pendown()
        self.turtle.stamp()
        self.turtle.shape("blank")
        self.turtle.penup()


    def drawHit(self, board, row, col):
        width = self.screen.window_width()
        height = self.screen.window_height()
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            left = -self.gridSize * self.squareSize - marginw
        else:
            left = marginw
        self.turtle.color("black", "red")
        self.turtle.shape(const.HIT_GIF)
        self.turtle.penup()
        self.turtle.goto(left + col * self.squareSize + self.squareSize / 2,
                    top - row * self.squareSize - self.squareSize / 2)
        self.turtle.pendown()
        self.turtle.stamp()
        self.turtle.shape("blank")
        self.turtle.penup()


    def drawPlayer(self, name, description, board):
        width = self.screen.window_width()
        height = self.screen.window_height()
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        marginh = (height - self.squareSize * self.gridSize)/2
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            center = -self.gridSize * self.squareSize / 2 - marginw
        else:
            center = self.gridSize * self.squareSize / 2 + marginw

        self.turtle.color("green", "green")
        self._writeText(name, center, bottom - 30)
        self._writeText(description, center, bottom - 80,
                  font=("Arial", 12, "normal"))
        self.turtle.penup()

    def drawWinner(self, board):
        width = self.screen.window_width()
        height = self.screen.window_height()
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            win = -width / 4
            lost = width / 4
        else:
            win = width / 4
            lost = -width / 4

        self.turtle.shape(const.WINNER_GIF)
        self.turtle.penup()
        self.turtle.goto(win, 0)
        self.turtle.pendown()
        self.turtle.stamp()
        self.turtle.shape(const.LOOSER_GIF)
        self.turtle.penup()
        self.turtle.goto(lost, 0)
        self.turtle.pendown()
        self.turtle.stamp()
        self.turtle.shape("blank")
        self.turtle.penup()


    def drawScore(self, leftPlayerScore, rightPlayerScore):
        width = self.screen.window_width()
        height = self.screen.window_height()
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh


        self.turtle.color("green", "black")
        self._fillRectangle(-marginw / 2, 30,
                      marginw , 40)
        self._writeText((str(leftPlayerScore) + " - " + str(rightPlayerScore)), 0, 0)
        self.turtle.penup()


    def drawBoards(self):
        width = self.screen.window_width()
        height = self.screen.window_height()
        squareSize = self.squareSize
        gridSize = self.gridSize
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3 ## vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        self.turtle.color("cyan", "black")
        self.turtle.shape("blank")
        self.turtle.pensize(3)

        rowLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        colLabels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        ## drawing left board
        leftL = -gridSize * squareSize - marginw
        leftR = - marginw
        leftM = -squareSize * gridSize / 2 - marginw

        for row in range(0,7):
            self._drawLine(leftL, top - row * squareSize,leftM, top - row * squareSize)

        for row in range(6, 13):
            self._drawLine(leftL, top - row * squareSize,leftR, top - row * squareSize)

        for col in range(0,7):
            self._drawLine(leftL + col * squareSize, top, leftL + col * squareSize, bottom)

        for col in range(6, 13):
            self._drawLine(leftL + col * squareSize, middleh, leftL + col * squareSize, bottom)

        for row in range(1,7):
            self._writeText(rowLabels[row-1],leftL-squareSize/2, top - row * squareSize + squareSize/5,font=("Arial", 12, "normal"))

        for row in range(7, 13):
            self._writeText(rowLabels[row-1], leftL-squareSize/2, top - row * squareSize + squareSize/5,font=("Arial", 12, "normal"))

        for col in range(1,7):
            self._writeText(colLabels[col-1], leftL + col * squareSize - squareSize/2, top + squareSize/3,font=("Arial", 12, "normal"))

        for col in range(7, 13):
            self._writeText(colLabels[col-1], leftL + col * squareSize - squareSize/2, middleh + squareSize/3,font=("Arial", 12, "normal"))


        ## drawing right board
        rightL = marginw
        rightR = gridSize * squareSize + marginw
        rightM = squareSize * gridSize / 2 + marginw

        for row in range(0,7):
            self._drawLine(rightL, top - row * squareSize, rightM, top - row * squareSize)

        for row in range(6, 13):
            self._drawLine(rightL, top - row * squareSize, rightR, top - row * squareSize)

        for col in range(0,7):
            self._drawLine(rightL + col * squareSize, top, rightL + col * squareSize, bottom)

        for col in range(6, 13):
            self._drawLine(rightL + col * squareSize, middleh, rightL + col * squareSize, bottom)

        for row in range(1,7):
            self._writeText(rowLabels[row-1],rightL-squareSize/2, top - row * squareSize + squareSize/3,font=("Arial", 12, "normal"))

        for row in range(7, 13):
            self._writeText(rowLabels[row-1], rightL-squareSize/2, top - row * squareSize + squareSize/5,font=("Arial", 12, "normal"))

        for col in range(1,7):
            self._writeText(colLabels[col-1], rightL + col * squareSize - squareSize/2, top + squareSize/3,font=("Arial", 12, "normal"))

        for col in range(7, 13):
            self._writeText(colLabels[col-1], rightL + col * squareSize - squareSize/2, middleh + squareSize/3,font=("Arial", 12, "normal"))
        self.turtle.penup()



