from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500
speed = 1.0
frozen = False
blinking = False
particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.color = [random.random(), random.random(), random.random()]
        self.visible = True

def draw_particles():
    glBegin(GL_POINTS)
    for p in particles:
        if p.visible:
            glColor3f(*p.color)
            glVertex2f(p.x, p.y)
    glEnd()

def update():
    global frozen
    if frozen:
        return  # If frozen, stop movement

    for p in particles:
        p.x += p.dx * speed  # Move horizontally
        p.y += p.dy * speed  # Move vertically

        # Bounce off window edges
        if p.x <= 0 or p.x >= W_Width:
            p.dx *= -1  # Reverse direction
        if p.y <= 0 or p.y >= W_Height:
            p.dy *= -1  # Reverse direction


def keyboardListener(key, x, y):
    global speed, frozen
    if key == b' ':
        frozen = not frozen
    glutPostRedisplay()

def special_key_Listener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        speed /= 1.5
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global blinking
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        particles.append(Particle(x, W_Height - y))
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking = not blinking
    glutPostRedisplay()

def blink_particles(value):
    if blinking:
        for p in particles:
            p.visible = not p.visible
        glutPostRedisplay()
    glutTimerFunc(500, blink_particles, 0)  #glutTimerFunc(milliseconds, callback, value)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_particles()
    glutSwapBuffers()

def animate(value):
    update()
    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)

def init():
    glClearColor(0, 0, 0, 1)
    glPointSize(5)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)

# Initialize GLUT
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Amazing Box")
init()

glutDisplayFunc(display)
glutIdleFunc(display)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(special_key_Listener)
glutTimerFunc(16, animate, 0)
glutTimerFunc(500, blink_particles, 0)

glutMainLoop()
