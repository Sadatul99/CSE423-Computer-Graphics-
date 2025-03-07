from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


W_Width, W_Height = 500, 500


points = []
speed = 0.002 
blink = False
frozen = False
last_blink_time = time.time()  
blink_state = True  

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = [random.random(), random.random(), random.random()]
        direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])  
        self.dx = direction[0] * speed
        self.dy = direction[1] * speed  #movement speed thik kore x y er dike
    
    def move(self):
        if frozen:
            return  # movement stop kre dey
        self.x += self.dx
        self.y += self.dy
        
        if self.x > 0.95 or self.x < -0.95:
            self.dx = -self.dx
        if self.y > 0.95 or self.y < -0.95: # jodi wall er kase chole jay thn direction reverse kre dey
            self.dy = -self.dy

    def draw(self):
        if blink and not blink_state:  
            glColor3f(0, 0, 0)  #pint gula invisible kre dey jodi blnkst fls hoy
        else:
            glColor3f(*self.color)  
        glPointSize(4)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

def draw_points():
    for p in points:
        p.draw() #draw cll kre each point er jnno

def keyboardListener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen  

def specialKeyListener(key, x, y):
    global speed
    if frozen:
        return  
    if key == GLUT_KEY_UP:
        speed += 0.0002
    elif key == GLUT_KEY_DOWN and speed > 0.0002:
        speed -= 0.0002  

    for p in points:

        p.dx = speed if p.dx > 0 else -speed
        p.dy = speed if p.dy > 0 else -speed

def mouseListener(button, state, x, y):
    global blink
    if frozen:
        return  
    if state == GLUT_DOWN: #mouse press hoise kina chck kre
        if button == GLUT_RIGHT_BUTTON:
        
            px = (x / W_Width) * 2 - 1
            py = 1 - (y / W_Height) * 2 #screen cordinate theke opengl cordinate a nia asha
            points.append(Point(px, py))  
        elif button == GLUT_LEFT_BUTTON:
            blink = not blink  

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_points()
    glutSwapBuffers()

def animate():
    global last_blink_time, blink_state

    if not frozen:
        for p in points:
            p.move()

    
        if blink and time.time() - last_blink_time > 0.5:
            blink_state = not blink_state  
            last_blink_time = time.time()  #blink er time cal

    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 1)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)  
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"OpenGL Interactive Box")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()