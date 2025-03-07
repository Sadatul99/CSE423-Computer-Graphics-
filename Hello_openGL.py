from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

point_x=250
point_y=250
ball_size =5

def draw_points(x, y):
    glPointSize(20 ) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def animate():
    global point_x
    point_x+=0.02
    if point_x>500:
        point_x=150
    glutPostRedisplay()

def keyboardListen(key, x, y):
    if key ==b"d":
        global point_x
        point_x+=1
        glutPostRedisplay() 
        
    if  key ==b"w":
        global ball_size
        ball_size+=1   
        glutPostRedisplay()    
    


def iterate():
    glViewport(0, 0, 500, 500)  # This is vesel -->black part around the screen
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0) # Axis setup -->
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global point_x, point_y, ball_size
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    
    
    #call the draw methods here
    glPointSize(ball_size) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(point_x,point_y) #jekhane show korbe pixel
    glEnd()
    
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size (width, height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name

glutDisplayFunc(showScreen)
#glutIdleFunc(animate)
glutKeyboardFunc(keyboardListen)

glutMainLoop()