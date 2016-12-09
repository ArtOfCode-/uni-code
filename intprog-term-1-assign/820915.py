# Copyright (c) 2016 Owen Jenkins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from graphics import *

def main():
    workSize, colorNames = getInputs()
    win = GraphWin("Patchwork", workSize * 100, workSize * 100)
    drawPatchwork(workSize, colorNames, win)
    handleClicks(workSize, colorNames, win)
    
def getInputs():
    validSizes = [5, 7, 9]
    validColors = ["red", "green", "blue", "orange", "brown", "pink"]
    
    workSize = None
    while type(workSize) != int or workSize not in validSizes:
        print("Patchwork size should be one of 5, 7, or 9.")
        workSize = eval(input("Enter the size of the patchwork: "))
        
    colors = [None, None, None]
    for i in range(len(colors)):
        while True:
            print("Valid colours: ", ", ".join(validColors))
            colors[i] = input("Enter colour #{}: ".format(i + 1))
            if colors[i] in validColors:
                validColors.remove(colors[i])
                break
            
    return workSize, colors
    
def getLayout(size):
    # layouts describes the layout of the patchwork. Each possible size (5, 7,
    # or 9) has a key. The value is a list of lists: each sub-list describes
    # a horizontal line, and each list within describes a cell in terms of 
    # which patch is has and which color it's drawn in. The patch number is an
    # index to the drawing method in the patches array; the color number is an
    # index to the color in the colorNames array.
    # This looks messy, but it makes it easier to make changes than writing 
    # patterns in conditionals.
    layouts = {
        5: [
            [[0, 0], [1, 0], [0, 1], [1, 2], [0, 2]],
            [[0, 0], [1, 0], [0, 1], [1, 2], [0, 2]],
            [[0, 1], [1, 1], [0, 1], [1, 1], [0, 1]],
            [[0, 2], [1, 2], [0, 1], [1, 0], [0, 0]],
            [[0, 2], [1, 2], [0, 1], [1, 0], [0, 0]]
        ],
        7: [
            [[0, 0], [1, 0], [0, 0], [1, 1], [0, 2], [1, 2], [0, 2]],
            [[0, 0], [1, 0], [0, 0], [1, 1], [0, 2], [1, 2], [0, 2]],
            [[0, 0], [1, 0], [0, 0], [1, 1], [0, 2], [1, 2], [0, 2]],
            [[0, 1], [1, 1], [0, 1], [1, 1], [0, 1], [1, 1], [0, 1]],
            [[0, 2], [1, 2], [0, 2], [1, 1], [0, 0], [1, 0], [0, 0]],
            [[0, 2], [1, 2], [0, 2], [1, 1], [0, 0], [1, 0], [0, 0]],
            [[0, 2], [1, 2], [0, 2], [1, 1], [0, 0], [1, 0], [0, 0]]
        ],
        9: [
            [[0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [1, 2], [0, 2], [1, 2],
             [0, 2]],
            [[0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [1, 2], [0, 2], [1, 2],
             [0, 2]],
            [[0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [1, 2], [0, 2], [1, 2],
             [0, 2]],
            [[0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [1, 2], [0, 2], [1, 2],
             [0, 2]],
            [[0, 1], [1, 1], [0, 1], [1, 1], [0, 1], [1, 1], [0, 1], [1, 1],
             [0, 1]],
            [[0, 2], [1, 2], [0, 2], [1, 2], [0, 1], [1, 0], [0, 0], [1, 0],
             [0, 0]],
            [[0, 2], [1, 2], [0, 2], [1, 2], [0, 1], [1, 0], [0, 0], [1, 0],
             [0, 0]],
            [[0, 2], [1, 2], [0, 2], [1, 2], [0, 1], [1, 0], [0, 0], [1, 0],
             [0, 0]],
            [[0, 2], [1, 2], [0, 2], [1, 2], [0, 1], [1, 0], [0, 0], [1, 0],
             [0, 0]]
        ]
    }
    
    return layouts[size]
    
def drawPatchwork(workSize, colorNames, win):
    patches = [drawFirstPatch, drawSecondPatch]
    tileSize = 100
    
    selectedLayout = getLayout(workSize)
    dimension = workSize * tileSize

    for yPosition in range(0, dimension, tileSize):
        line = selectedLayout[yPosition // tileSize]
        for xPosition in range(0, dimension, tileSize):
            cell = line[xPosition // tileSize]
            
            methodIndex = cell[0]
            drawingMethod = patches[methodIndex]
            colorIndex = cell[1]
            color = colorNames[colorIndex]
            topLeft = Point(xPosition, yPosition)
            
            drawingMethod(win, topLeft, color)
        
    
def drawFirstPatch(win, topLeft, color):
    baseY = int(topLeft.getY())
    baseX = int(topLeft.getX())
    for y in range(baseY, baseY + 99, 33):
        for x in range(baseX, baseX + 100, 25):
            if y == baseY + 33:
                sailColor = 'white'
                hullColor = color
            else:
                sailColor = color
                hullColor = 'white'
            drawSingleBoat(win, x, y, sailColor, hullColor)
    
def drawSingleBoat(win, x, y, sailColor, hullColor):
    sailPoints = [Point(x + 13, y), Point(x + 25, y + 15), Point(x, y + 15)]
    sail = Polygon(sailPoints)
    sail.setFill(sailColor)
    sail.draw(win)
    
    mast = Line(Point(x + 13, y + 15), Point(x + 13, y + 20))
    mast.draw(win)
    
    hullPoints = [Point(x, y + 20), Point(x + 25, y + 20),
                  Point(x + 20, y + 25), Point(x + 5, y + 25)]
    hull = Polygon(hullPoints)
    hull.setFill(hullColor)
    hull.draw(win)
    
def drawSecondPatch(win, topLeft, color):
    baseX = int(topLeft.getX())
    baseY = int(topLeft.getY())
    
    for i in range(20, 100, 20):
        rect = Polygon(Point(baseX + i, baseY),
                       Point(baseX + 100, baseY + (100 - i)),
                       Point(baseX + (100 - i), baseY + 100),
                       Point(baseX, baseY + i))
        rect.setOutline(color)
        rect.draw(win)
        
    crossLines = [
        Line(Point(baseX, baseY), Point(baseX + 100, baseY + 100)),
        Line(Point(baseX, baseY + 100), Point(baseX + 100, baseY))
    ]
    for line in crossLines:
        line.setOutline(color)
        line.draw(win)
        
def handleClicks(workSize, colorNames, win):
    layout = getLayout(workSize)
    tileSize = 100
    drawingMethods = [drawFirstPatch, drawSecondPatch]
    
    while True:
        clickPoint = win.getMouse()
        tileXIndex = int(clickPoint.getX() // tileSize)
        tileYIndex = int(clickPoint.getY() // tileSize)
        tile = layout[tileYIndex][tileXIndex]
        
        currentColorIndex = tile[1]
        nextColorIndex = (currentColorIndex + 1) % len(colorNames)
        tile[1] = nextColorIndex
        
        methodIndex = tile[0]
        method = drawingMethods[methodIndex]
        topLeft = Point(tileXIndex * 100, tileYIndex * 100)
        color = colorNames[nextColorIndex]
        method(win, topLeft, color)
        
    
main()
