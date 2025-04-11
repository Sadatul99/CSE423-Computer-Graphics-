import sys
import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window dimensions
win_width, win_height = 800, 600

# Paddle configuration
paddle_w = 60
paddle_h = 20
paddle_y = 50

# Ball configuration
circle_size = 20

# Game variables
points = 0
fall_speed = 100
is_paused = False
is_game_over = False
prev_time = time.time()

# Initial positions
paddle_x = win_width // 2 - paddle_w // 2
circle_x = random.randint(50, win_width - 50)
circle_y = win_height
circle_shade = (1.0, 0.0, 1.0)

# ================= Utility Functions ===================

def detectZone(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy < 0:
            return 7
        elif dx < 0 and dy >= 0:
            return 3
        else:
            return 4
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx >= 0 and dy < 0:
            return 6
        elif dx < 0 and dy >= 0:
            return 2
        else:
            return 5

def toZone0(x, y, zone):
    trans = [
        (x, y), (y, x), (y, -x), (-x, y),
        (-x, -y), (-y, -x), (-y, x), (x, -y)
    ]
    return trans[zone]

def fromZone0(x, y, zone):
    trans = [
        (x, y), (y, x), (-y, x), (-x, y),
        (-x, -y), (-y, -x), (y, -x), (x, -y)
    ]
    return trans[zone]

def putPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def drawSegment(x1, y1, x2, y2):
    zone = detectZone(x1, y1, x2, y2)
    sx, sy = toZone0(x1, y1, zone)
    ex, ey = toZone0(x2, y2, zone)
    dx, dy = ex - sx, ey - sy
    d = 2 * dy - dx
    incrE, incrNE = 2 * dy, 2 * (dy - dx)
    x, y = sx, sy

    while x <= ex:
        px, py = fromZone0(x, y, zone)
        putPixel(px, py)
        if d > 0:
            y += 1
            d += incrNE
        else:
            d += incrE
        x += 1

# ================= Drawing Functions ===================

def renderBall(x, y):
    half = circle_size // 2
    drawSegment(x, y + half, x + half, y)
    drawSegment(x + half, y, x, y - half)
    drawSegment(x, y - half, x - half, y)
    drawSegment(x - half, y, x, y + half)

def renderPaddle():
    mid = paddle_w // 2
    glColor3f(1.0, 0.0, 0.0 if is_game_over else 1.0)
    drawSegment(paddle_x, paddle_y, paddle_x + mid, paddle_y + paddle_h)
    drawSegment(paddle_x + mid, paddle_y + paddle_h, paddle_x - mid, paddle_y + paddle_h)
    drawSegment(paddle_x - mid, paddle_y + paddle_h, paddle_x, paddle_y)

def renderControls():
    glColor3f(0.0, 1.0, 1.0)  # Restart button
    drawSegment(40, 570, 60, 590)
    drawSegment(60, 590, 60, 550)
    drawSegment(60, 550, 40, 570)

    glColor3f(1.0, 0.75, 0.0)  # Pause/Resume
    if is_paused:
        drawSegment(390, 550, 390, 590)
        drawSegment(410, 550, 410, 590)
    else:
        drawSegment(390, 550, 410, 570)
        drawSegment(410, 570, 390, 590)
        drawSegment(390, 590, 390, 550)

    glColor3f(1.0, 0.0, 0.0)  # Exit
    drawSegment(740, 550, 770, 590)
    drawSegment(770, 550, 740, 590)

def showText(x, y, string, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for ch in string:
        glutBitmapCharacter(font, ord(ch))

# ================= Game Logic ===================

def renderScene():
    global circle_y, circle_x, circle_shade, points, fall_speed, prev_time

    glClear(GL_COLOR_BUFFER_BIT)
    renderControls()
    renderPaddle()

    if not is_game_over:
        glColor3f(*circle_shade)
        renderBall(circle_x, int(circle_y))

    now = time.time()
    dt = now - prev_time

    if not is_paused and not is_game_over:
        circle_y -= fall_speed * dt
        if checkHit():
            points += 1
            if points % 2 == 0:
                fall_speed *= 1.25
            resetBall()
        elif circle_y < 0:
            triggerGameOver()

    prev_time = now

    # Display score
    glColor3f(1.0, 1.0, 0.0)
    showText(10, win_height - 90, f"Score: {points}")

    glutSwapBuffers()

def checkHit():
    paddle_box = (paddle_x, paddle_y, paddle_w, paddle_h)
    ball_box = (circle_x - 10, circle_y - 10, 20, 20)
    return (
        paddle_box[0] < ball_box[0] + ball_box[2] and
        paddle_box[0] + paddle_box[2] > ball_box[0] and
        paddle_box[1] < ball_box[1] + ball_box[3] and
        paddle_box[1] + paddle_box[3] > ball_box[1]
    )

def resetBall():
    global circle_x, circle_y, circle_shade
    circle_x = random.randint(50, win_width - 50)
    circle_y = win_height
    circle_shade = (random.random(), random.random(), random.random())

def triggerGameOver():
    global is_game_over
    is_game_over = True

def restartSession():
    global points, fall_speed, is_game_over, is_paused
    points = 0
    fall_speed = 100
    is_paused = False
    is_game_over = False
    resetBall()

# ================= Input Handlers ===================

def onKeyPress(key, x, y):
    if key == b'\x1b':  # ESC
        print("Closing. Final Score:", points)
        glutLeaveMainLoop()

def onArrowPress(key, x, y):
    global paddle_x
    if is_game_over or is_paused:
        return
    if key == GLUT_KEY_LEFT and paddle_x > 10:
        paddle_x -= 20
    elif key == GLUT_KEY_RIGHT and paddle_x < win_width - paddle_w - 10:
        paddle_x += 20

def onMouseClick(btn, state, mx, my):
    if btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        my = win_height - my
        if 40 < mx < 60 and 550 < my < 590:
            restartSession()
        elif 390 < mx < 420 and 550 < my < 590:
            global is_paused
            is_paused = not is_paused
        elif 740 < mx < 770 and 550 < my < 590:
            print("Closing. Final Score:", points)
            glutLeaveMainLoop()

# ================= Initialization ===================

def setupTimer(val):
    glutPostRedisplay()
    glutTimerFunc(16, setupTimer, 0)

def configureGL():
    glClearColor(0, 0, 0, 1)
    gluOrtho2D(0, win_width, 0, win_height)
    glPointSize(2)

def launchGame():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(win_width, win_height)
    glutCreateWindow(b"CG Lab 2 - Catch the Falling Circles")
    glutDisplayFunc(renderScene)
    glutKeyboardFunc(onKeyPress)
    glutSpecialFunc(onArrowPress)
    glutMouseFunc(onMouseClick)
    glutTimerFunc(0, setupTimer, 0)
    configureGL()
    glutMainLoop()

if __name__ == "__main__":
    launchGame()
