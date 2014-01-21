import turtle
import const
###########################################################
##
##                   DISPLAY
##
###########################################################


class BattleshipsGraphics:

    def __init__(self, gridSize):
        self._turtle = turtle.Turtle()
        self._screen = turtle.getscreen()
        self._screen.setup(width=1200, height=750, startx=None, starty=None)
        self._screen.register_shape(const.MISSED_GIF)
        self._screen.register_shape(const.HIT_GIF)
        self._screen.register_shape(const.WINNER_GIF)
        self._screen.register_shape(const.LOOSER_GIF)
        self._screen.bgpic(const.BOARD_BKG_GIF)
        self._turtle.speed(0)
        self._turtle.color("black")
        self.squareSize = 40
        self.gridSize = gridSize
        self._turtle.tracer(1, 0)
        self._turtle.goto(0, 0)
        self._turtle.showturtle()

    def setScreenSize(self, width, height):
        self._screen.setup(width=width, height=height,
                          startx=None, starty=None)

    def setSquareSize(self, squareSize):
        self.squareSize = squareSize

    # Draw a line from (x1, y1) to (x2, y2)
    def _drawLine(self, x1, y1, x2, y2):
        self._turtle.penup()
        self._turtle.goto(x1, y1)
        self._turtle.pendown()
        self._turtle.goto(x2, y2)
        self._turtle.penup()

    # Write a text at the specified location (x, y)
    def _writeText(self, s, x, y, font=("Arial", 16, "bold")):
        self._turtle.penup()  # Pull the pen up
        self._turtle.goto(x, y)
        self._turtle.pendown()  # Pull the pen down
        self._turtle.write(s, align='center', font=font)  # Write a string
        self._turtle.penup()

    # Draw a point at the specified location (x, y)
    def _drawPoint(self, x, y):
        self._turtle.penup()  # Pull the pen up
        self._turtle.goto(x, y)
        self._turtle.pendown()  # Pull the pen down
        self._turtle.begin_fill()  # Begin to fill color in a shape
        self._turtle.circle(3)
        self._turtle.end_fill()  # Fill the shape
        self._turtle.penup()

    # Draw a circle at centered at (x, y) with the specified radius
    def _fillCircle(self, x, y, radius):
        self._turtle.penup()  # Pull the pen up
        self._turtle.fill(True)
        self._turtle.goto(x, y - radius)
        self._turtle.pendown()  # Pull the pen down
        self._turtle.circle(radius)
        self._turtle.fill(False)
        self._turtle.penup()

    # Draw a rectangle at (x, y) with the specified width and height
    def _fillRectangle(self, x, y, width, height):
        self._turtle.penup()  # Pull the pen up
        self._turtle.fill(True)
        self._turtle.setheading(0)
        self._turtle.goto(x, y)
        self._turtle.pendown()  # Pull the pen down
        self._turtle.forward(width)
        self._turtle.right(90)
        self._turtle.forward(height)
        self._turtle.right(90)
        self._turtle.forward(width)
        self._turtle.right(90)
        self._turtle.forward(height)
        self._turtle.penup()  # Pull the pen up
        self._turtle.fill(False)
        self._turtle.setheading(0)
        self._turtle.penup()

    def clear(self):
        self._turtle.clear()

    def drawBoat(self, board, row, col):
        width = self._screen.window_width()
        height = self._screen.window_height()
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            left = -self.gridSize * self.squareSize - marginw
        else:
            left = marginw
        self._turtle.color("black", "darkgrey")
        self._fillRectangle(left + col * self.squareSize,
                            top - row * self.squareSize,
                            self.squareSize, self.squareSize)
        self._turtle.penup()

    def drawMiss(self, board, row, col):
        width = self._screen.window_width()
        height = self._screen.window_height()
        marginh = (height - self.squareSize * self.gridSize) / 2
        marginw = (width - 2 * self.squareSize * self.gridSize) / 4
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            left = -self.gridSize * self.squareSize - marginw
        else:
            left = marginw
        self._turtle.color("black", "blue")
        self._turtle.shape(const.MISSED_GIF)
        self._turtle.penup()
        self._turtle.goto(left + col * self.squareSize + self.squareSize / 2,
                         top - row * self.squareSize - self.squareSize / 2)
        self._turtle.pendown()
        self._turtle.stamp()
        self._turtle.shape("blank")
        self._turtle.penup()

    def drawHit(self, board, row, col):
        width = self._screen.window_width()
        height = self._screen.window_height()
        marginh = (height - self.squareSize * self.gridSize) / 2
        marginw = (width - 2 * self.squareSize * self.gridSize) / 4
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            left = -self.gridSize * self.squareSize - marginw
        else:
            left = marginw
        self._turtle.color("black", "red")
        self._turtle.shape(const.HIT_GIF)
        self._turtle.penup()
        self._turtle.goto(left + col * self.squareSize + self.squareSize / 2,
                         top - row * self.squareSize - self.squareSize / 2)
        self._turtle.pendown()
        self._turtle.stamp()
        self._turtle.shape("blank")
        self._turtle.penup()

    def drawPlayer(self, name, description, board):
        width = self._screen.window_width()
        height = self._screen.window_height()
        marginw = (width - 2 * self.squareSize * self.gridSize) / 4
        marginh = (height - self.squareSize * self.gridSize) / 2
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            center = -self.gridSize * self.squareSize / 2 - marginw
        else:
            center = self.gridSize * self.squareSize / 2 + marginw

        self._turtle.color("green", "green")
        self._writeText(name, center, bottom - 30)
        self._writeText(description, center, bottom - 80,
                        font=("Arial", 12, "normal"))
        self._turtle.penup()

    def drawWinner(self, board):
        width = self._screen.window_width()
        height = self._screen.window_height()
        marginh = (height - self.squareSize * self.gridSize) / 2
        marginw = (width - 2 * self.squareSize * self.gridSize) / 4
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        if board == 'left':
            win = -width / 4
            lost = width / 4
        else:
            win = width / 4
            lost = -width / 4

        self._turtle.shape(const.WINNER_GIF)
        self._turtle.penup()
        self._turtle.goto(win, 0)
        self._turtle.pendown()
        self._turtle.stamp()
        self._turtle.shape(const.LOOSER_GIF)
        self._turtle.penup()
        self._turtle.goto(lost, 0)
        self._turtle.pendown()
        self._turtle.stamp()
        self._turtle.shape("blank")
        self._turtle.penup()

    def drawScore(self, leftPlayerScore, rightPlayerScore):
        width = self._screen.window_width()
        height = self._screen.window_height()
        marginh = (height - self.squareSize * self.gridSize) / 2
        marginw = (width - 2 * self.squareSize * self.gridSize) / 4
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        self._turtle.color("green", "black")
        self._fillRectangle(-marginw / 2, 30, marginw, 40)
        self._writeText((str(leftPlayerScore) + " - " + str(rightPlayerScore)),
                        0, 0)
        self._turtle.penup()

    def drawBoards(self):
        width = self._screen.window_width()
        height = self._screen.window_height()
        squareSize = self.squareSize
        gridSize = self.gridSize
        marginh = (height - self.squareSize * self.gridSize)/2
        marginw = (width - 2 * self.squareSize * self.gridSize)/4
        middleh = -marginh / 3  # Vertical offset
        bottom = -self.squareSize * self.gridSize / 2 + middleh
        top = self.squareSize * self.gridSize / 2 + middleh

        self._turtle.color("cyan", "black")
        self._turtle.shape("blank")
        self._turtle.pensize(3)

        rowLabels = ['A', 'B', 'C', 'D', 'E', 'F',
                     'G', 'H', 'I', 'J', 'K', 'L']
        colLabels = ['1', '2', '3', '4', '5', '6',
                     '7', '8', '9', '10', '11', '12']

        ## drawing left board
        leftL = -gridSize * squareSize - marginw
        leftR = -marginw
        leftM = -squareSize * gridSize / 2 - marginw

        for row in range(0, 7):
            self._drawLine(leftL, top - row * squareSize,
                           leftM, top - row * squareSize)

        for row in range(6, 13):
            self._drawLine(leftL, top - row * squareSize,
                           leftR, top - row * squareSize)

        for col in range(0, 7):
            self._drawLine(leftL + col * squareSize, top,
                           leftL + col * squareSize, bottom)

        for col in range(6, 13):
            self._drawLine(leftL + col * squareSize, middleh,
                           leftL + col * squareSize, bottom)

        for row in range(1, 7):
            self._writeText(rowLabels[row - 1], leftL - squareSize / 2,
                            top - row * squareSize + squareSize / 5,
                            font=("Arial", 12, "normal"))

        for row in range(7, 13):
            self._writeText(rowLabels[row - 1], leftL - squareSize / 2,
                            top - row * squareSize + squareSize / 5,
                            font=("Arial", 12, "normal"))

        for col in range(1, 7):
            self._writeText(colLabels[col - 1],
                            leftL + col * squareSize - squareSize / 2,
                            top + squareSize / 3,
                            font=("Arial", 12, "normal"))

        for col in range(7, 13):
            self._writeText(colLabels[col - 1],
                            leftL + col * squareSize - squareSize / 2,
                            middleh + squareSize / 3,
                            font=("Arial", 12, "normal"))

        # Drawing right board
        rightL = marginw
        rightR = gridSize * squareSize + marginw
        rightM = squareSize * gridSize / 2 + marginw

        for row in range(0, 7):
            self._drawLine(rightL, top - row * squareSize,
                           rightM, top - row * squareSize)

        for row in range(6, 13):
            self._drawLine(rightL, top - row * squareSize,
                           rightR, top - row * squareSize)

        for col in range(0, 7):
            self._drawLine(rightL + col * squareSize, top,
                           rightL + col * squareSize, bottom)

        for col in range(6, 13):
            self._drawLine(rightL + col * squareSize, middleh,
                           rightL + col * squareSize, bottom)

        for row in range(1, 7):
            self._writeText(rowLabels[row - 1],
                            rightL - squareSize / 2,
                            top - row * squareSize + squareSize / 3,
                            font=("Arial", 12, "normal"))

        for row in range(7, 13):
            self._writeText(rowLabels[row - 1],
                            rightL - squareSize / 2,
                            top - row * squareSize + squareSize / 5,
                            font=("Arial", 12, "normal"))

        for col in range(1, 7):
            self._writeText(colLabels[col - 1],
                            rightL + col * squareSize - squareSize / 2,
                            top + squareSize / 3,
                            font=("Arial", 12, "normal"))

        for col in range(7, 13):
            self._writeText(colLabels[col - 1],
                            rightL + col * squareSize - squareSize / 2,
                            middleh + squareSize / 3,
                            font=("Arial", 12, "normal"))
        self._turtle.penup()

    def exitonclick():
        self._screen.exitonclick()
