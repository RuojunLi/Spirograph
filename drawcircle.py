import math,turtle,random, argparse

def drawcircle_turtle(x,y,r):
    """
    (x,y):the big circel center
    (x+r,y): the pen point position
    """
    # move turtle to the pen position
    turtle.up();
    turtle.setpos(x+r,y)
    turtle.down()
    #Start drawing the small circle
    for i in range(0,365,5):
        rad = math.radians(i)
        turtle.setpos(x+r*math.cos(rad),y+r*math.sin(rad))

# A class draw the Spirograph
class Spiro:
    #constructor
    def __init__(self,xc,yc,col,R,r,l):
        """
        R: Radius of large circel
        r: Radius f small circel
        (xc,yc): center of the small circle
        """
        #create the turtle object
        self.t = turtle.Turtle()
        # set the cursor shape
        self.t.shape('turtle')
        # step degree
        self.step = 5
        # set complete flag
        self.completeflag = False
        # set parameters
        self.setparams(xc,yc,col,R,r,l)
        # initialize the drawing
        self.restart()


    def setparams(self,xc,yc,col,R,r,l):
        # the spiro graph parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        # GCD of r and R
        gcdR = math.gcd(self.r,self.R)
        self.nRot = int(self.r/gcdR)
        self.k = self.r/self.R
        self.t.color(*col)
        #Current Angle
        self.a = 0


    def restart(self):
        # set flag
        self.completeflag = False
        # open turtle
        self.t.showturtle()
        # go to the first pen point
        self.t.up()
        R,k,l,a = self.R, self.k, self.l, self.a
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc+x,self.yc+y)
        self.t.down()

    def draw(self):
        R, k, l = self.R, self.k, self.l
        a = 0.0
        for i in range(0,360*self.nRot+1,self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()

    def update(self):
        if self.completeflag:
            return
        self.a +=self.step
        # draw a step
        R,k,l = self.R,self.k,self.l
        a = math.radians(self.a)
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a>=360*self.nRot:
            self.hideturtle()
            self.completeflag = True

    def clear(self):
        self.t.clear()


# A class for animating spirographs
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # timer value in milliseconds
        self.deltaT = 10
        # get window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create spiro objects
        self.spiros = []
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams()
            # set spiro params
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.deltaT)

    # restart sprio drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set spiro params
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    # generate random parameters
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height) // 2)
        r = random.randint(10, 9 * R // 10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)

    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed ones
            if spiro.completeflag:
                nComplete += 1
        # if all spiros are complete, restart
        if nComplete == len(self.spiros):
            self.restart()
        # call timer
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle on/off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


# save spiros to image
def saveDrawing():
    # hide turtle
    turtle.hideturtle()
    fileName = 'spiro-test'
    print('saving drawing to %s.eps/png' % fileName)
    # get tkinter canvas
    canvas = turtle.getcanvas()
    # save postscipt image
    canvas.postscript(file=fileName + '.eps')
    # show turtle
    turtle.showturtle()


# main() function
def main():
    # use sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr ="""This program draws spirographs using the Turtle module. 
    When run with no arguments, this program draws random spirographs.

    Terminology:
    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r.
    """
    parser = argparse.ArgumentParser(description=descStr)

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")
    params = [300, 100, 0.9]
    # parse args
    args = parser.parse_args()

    # set to 80% screen width
    turtle.setup(width=0.8)

    # set cursor shape
    turtle.shape('turtle')

    # set title
    turtle.title("Spirographs!")
    # add key handler for saving images
    turtle.onkey(saveDrawing, "s")
    # start listening
    turtle.listen()

    # hide main turtle cursor
    turtle.hideturtle()
    # checks args and draw
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw spirograph with given parameters
        # black by default
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create animator object
        spiroAnim = SpiroAnimator(4)
        # add key handler to toggle turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # add key handler to restart animation
        turtle.onkey(spiroAnim.restart, "space")

    # start turtle main loop
    turtle.mainloop()


# call main
if __name__ == '__main__':
    main()

col = (1.0, 1.0, 1.0)
