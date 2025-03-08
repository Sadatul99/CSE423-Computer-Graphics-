from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Global variables
rain_drops = [[random.randint(0, 500), random.randint(300, 500)] for _ in range(100)]
rain_direction = 0.0  # Straight down
background_color = [0.1, 0.1, 0.2]  # dark background

# Define colors for a more attractive house
house_color = [0.9, 0.7, 0.5]  
roof_color = [0.8, 0.4, 0.2]   
door_color = [0.5, 0.25, 0.15]  
window_color = [0.9, 0.9, 1.0]  
rain_color = [0.5, 0.5, 1.0]  
tree_trunk_color = [0.5, 0.3, 0.2]  
tree_leaves_color = [0.0, 0.6, 0.0] 


def draw_house():
    #  roof
    glColor3f(*roof_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(180, 320)
    glVertex2f(320, 320)
    glVertex2f(250, 420)
    glEnd() 
    
    #  walls
    glColor3f(*house_color)
    glBegin(GL_QUADS)
    glVertex2f(180, 200)
    glVertex2f(320, 200)
    glVertex2f(320, 320)
    glVertex2f(180, 320)
    glEnd() 
    
    #  door
    glColor3f(*door_color)
    glBegin(GL_QUADS)
    glVertex2f(230, 200)
    glVertex2f(270, 200)
    glVertex2f(270, 260)
    glVertex2f(230, 260)
    glEnd()
    
    # windows
    glColor3f(*window_color)
    glBegin(GL_QUADS)
    glVertex2f(190, 260)
    glVertex2f(220, 260)
    glVertex2f(220, 290)
    glVertex2f(190, 290)
    
    glVertex2f(280, 260)
    glVertex2f(310, 260)
    glVertex2f(310, 290)
    glVertex2f(280, 290)
    glEnd()
    
def draw_trees():
    positions = [80, 140, 360, 420]  # Four tree positions
    for x in positions:
        # Draw trunk
        glColor3f(*tree_trunk_color)
        glBegin(GL_QUADS)
        glVertex2f(x - 10, 200)
        glVertex2f(x + 10, 200)
        glVertex2f(x + 10, 250)
        glVertex2f(x - 10, 250)
        glEnd()
        
        # Draw leaves
        glColor3f(*tree_leaves_color)
        glBegin(GL_TRIANGLES)
        glVertex2f(x - 30, 250)
        glVertex2f(x + 30, 250)
        glVertex2f(x, 300)
        glEnd()

def draw_rain():
    glColor3f(*rain_color)
    glBegin(GL_LINES)
    for drop in rain_drops:
        glVertex2f(drop[0], drop[1])
        glVertex2f(drop[0] + rain_direction, drop[1] - 10)
    glEnd()

def update(value):
    global rain_drops
    for drop in rain_drops:
        drop[1] -= 10  # Slow rain falling speed
        drop[0] += rain_direction * 0.1
        if drop[1] < 0:
            drop[0], drop[1] = random.randint(0, 500), random.randint(300, 500)
    glutPostRedisplay()
    glutTimerFunc(50, update, 0)  # Timer function to slow down the update cycle  glutTimerFunc(milliseconds, callback, value)


def keyboard(key, x, y):
    global background_color, house_color, roof_color, door_color, window_color, rain_color
        
    # Day    
    if key == b'd':  
        background_color = [min(c + 0.1, 1.0) for c in background_color]
        house_color = [1.0, 0.8, 0.6]  
        roof_color = [0.9, 0.5, 0.3]
        door_color = [0.6, 0.3, 0.2]
        window_color = [1.0, 1.0, 1.0]
        rain_color = [0.3, 0.3, 0.8]
    # Night   
    elif key == b'n':  
        background_color = [max(c - 0.1, 0.0) for c in background_color]
        house_color = [0.9, 0.7, 0.5]  
        roof_color = [0.8, 0.4, 0.2]
        door_color = [0.5, 0.25, 0.15]
        window_color = [0.8, 0.8, 1.0]
        rain_color = [0.5, 0.5, 1.0]
    glutPostRedisplay()

def specialKey(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction -= 1
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 1
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    glClearColor(*background_color, 1.0) # Change background 
    
    draw_house()
    draw_trees()
    draw_rain()
    
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"House and Rain")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)  # For the day and night mode 
glutSpecialFunc(specialKey)   # To change rain direction

glutTimerFunc(50, update, 0)  # Start the timer function
glutMainLoop()
