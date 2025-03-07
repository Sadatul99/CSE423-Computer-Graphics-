from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Window dimensions
W_Width, W_Height = 500, 500

# Rain properties
rain_drops = [(random.randint(0, W_Width), random.randint(300, W_Height)) for _ in range(50)]  # Fewer raindrops
rain_direction = 0  # 0 for straight, negative for left bend, positive for right bend

# Background color (night: dark, day: bright)
bg_color = [0.0, 0.0, 0.0]


def draw_points(x, y):
    glBegin(GL_POINTS)
    
    glVertex2f(x, y)
    glEnd()


def draw_lines(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_tree(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glColor3f(0.3,0.2,0.7)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()    


def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glColor3f(1,0.5,0.3)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.6,0.2,0.6)
    glVertex2f(150,250)
    glVertex2f(350, 250)
    glVertex2f(250,350)
    glEnd()
def draw_ground():
    glPointSize(180)
    glColor3f(0.3,0.2,0.2)
    draw_points(50,50)
    draw_points(100,50)
    draw_points(200,50)
    draw_points(300,50)
    draw_points(400,50)
    draw_points(500,50)
    draw_points(50,100)
    draw_points(100,100)
    draw_points(200,100)
    draw_points(300,100)
    draw_points(400,100)
    draw_points(500,100)
    draw_points(50,150)
    draw_points(100,150)
    draw_points(200,150)
    draw_points(300,150)
    draw_points(400,150)
    draw_points(500,150)
def draw_gas():
    glColor3f(0.3,0.2,0.7)
    draw_tree(0,230,100,230,50,300)
    draw_tree(100,230,200,230,150,300)
    draw_tree(200,230,300,230,250,300)
    draw_tree(300,230,400,230,350,300)
    draw_tree(400,230,500,230,450,300)

    
    



def draw_house():
    glColor3f(1.0, 1.0, 1.0)
    # Base
    draw_triangle(175,150,325,150,250,200)
    draw_triangle(175,150,175,250,250,200)
    draw_triangle(325,150,325,250,250,200)
    draw_triangle(175,250,325,250,250,200)
    
    # Door (Middle of the house)
    glColor3f(1.0, 1.0, 1.0)
    draw_lines(230, 150, 230, 200)
    draw_lines(230, 200, 270, 200)
    draw_lines(270, 200, 270, 150)
    draw_lines(230, 150, 270, 150)
    
    # Left Window
    draw_lines(190, 180, 220, 180)
    draw_lines(220, 180, 220, 210)
    draw_lines(220, 210, 190, 210)
    draw_lines(190, 210, 190, 180)
    draw_lines(190, 195, 220, 195)
    draw_lines(205, 180, 205, 210)
    
    # Right Window
    draw_lines(280, 180, 310, 180)
    draw_lines(310, 180, 310, 210)
    draw_lines(310, 210, 280, 210)
    draw_lines(280, 210, 280, 180)
    draw_lines(280, 195, 310, 195)
    draw_lines(295, 180, 295, 210)


def draw_rain():
    glColor3f(0.6, 0.8, 0.9)
    for i in range(len(rain_drops)):
        x, y = rain_drops[i]
        draw_lines(x, y, x + rain_direction, y - 5)  # Shorter raindrop streaks


def keyboardListener(key, x, y):
    global bg_color
    step = 0.1
    if key == b'd':  # Gradually transition to day
        bg_color = [min(bg_color[0] + step, 1.0), min(bg_color[1] + step, 1.0), min(bg_color[2] + step, 1.0)]
    elif key == b'n':  # Gradually transition to night
        bg_color = [max(bg_color[0] - step, 0.0), max(bg_color[1] - step, 0.0), max(bg_color[2] - step, 0.0)]
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction -= 1
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 1
    glutPostRedisplay()


def animate():
    global rain_drops
    for i in range(len(rain_drops)):
        x, y = rain_drops[i]
        y -= 2  # Slower falling speed
        x += rain_direction * 0.1
        if y < 0:
            y = random.randint(300, W_Height)
            x = random.randint(0, W_Width)
        rain_drops[i] = (x, y)
    glutPostRedisplay()


def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(bg_color[0], bg_color[1], bg_color[2], 1.0)
    glLoadIdentity()
    draw_gas()
    draw_ground()

    draw_house()
    draw_rain()
    glutSwapBuffers()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"OpenGL House and Rain")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
iterate()
glutMainLoop()