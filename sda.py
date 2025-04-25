from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, math, random

width, height = 800, 600
grid_size = 10
cell_size = 2

player_pos = [0.0, 0.0]
player_angle = 0.0
player_health = 100
invincible = False  # Cheat mode
one_shot_kill = False  # Cheat mode

bullets = []
enemies = [[random.uniform(-10, 10), random.uniform(-10, 10), 100] for _ in range(5)]  # 5 enemies

def init():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Follow player camera
    camX = player_pos[0] - 10 * math.sin(math.radians(player_angle))
    camZ = player_pos[1] + 10 * math.cos(math.radians(player_angle))
    gluLookAt(camX, 10, camZ, player_pos[0], 1.5, player_pos[1], 0, 1, 0)

    draw_grid()
    draw_boundaries()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_health_bar()

    glutSwapBuffers()

def draw_grid():
    for i in range(-grid_size, grid_size):
        for j in range(-grid_size, grid_size):
            glColor3f(0.9, 0.9, 1.0) if (i + j) % 2 == 0 else glColor3f(0.6, 0.3, 1.0)
            glBegin(GL_QUADS)
            glVertex3f(i * cell_size, 0, j * cell_size)
            glVertex3f((i + 1) * cell_size, 0, j * cell_size)
            glVertex3f((i + 1) * cell_size, 0, (j + 1) * cell_size)
            glVertex3f(i * cell_size, 0, (j + 1) * cell_size)
            glEnd()

def draw_boundaries():
    glColor3f(0.0, 1.0, 0.0)
    height = 5
    length = grid_size * 2 * cell_size

    def draw_wall(x1, z1, x2, z2):
        glBegin(GL_QUADS)
        glVertex3f(x1, 0, z1)
        glVertex3f(x2, 0, z2)
        glVertex3f(x2, height, z2)
        glVertex3f(x1, height, z1)
        glEnd()

    draw_wall(-length/2, -length/2, length/2, -length/2)
    draw_wall(-length/2, length/2, length/2, length/2)
    draw_wall(-length/2, -length/2, -length/2, length/2)
    draw_wall(length/2, -length/2, length/2, length/2)

def draw_bullets():
    glColor3f(1.0, 1.0, 0.0)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], 1.0, b[1])
        glutSolidCube(0.2)
        glPopMatrix()

def draw_enemies():
    for e in enemies:
        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)
        glTranslatef(e[0], 0.5, e[1])
        glutSolidSphere(0.5, 20, 20)
        glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0.0, player_pos[1])
    glRotatef(player_angle, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 1.5, 0.0)

    # Head
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, 1.0, 0)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    # Body
    glPushMatrix()
    glColor3f(0.3, 0.7, 0.3)
    glScalef(1.0, 2.0, 0.5)
    glutSolidCube(1.0)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0.0, 0.5, -1.0)
    glScalef(0.2, 0.2, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

def draw_health_bar():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Red health bar
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(10, height - 20)
    glVertex2f(10 + player_health * 2, height - 20)
    glVertex2f(10 + player_health * 2, height - 10)
    glVertex2f(10, height - 10)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def update(value):
    global bullets, enemies, player_health

    # Update bullets
    for b in bullets:
        rad = math.radians(b[2])
        b[0] += 0.5 * math.sin(rad)
        b[1] -= 0.5 * math.cos(rad)

    # Bullet-enemy collision
    new_enemies = []
    for e in enemies:
        hit = False
        for b in bullets:
            if math.hypot(e[0] - b[0], e[1] - b[1]) < 1.0:
                hit = True
                if not one_shot_kill:
                    e[2] -= 50
                else:
                    e[2] = 0
        if e[2] > 0:
            new_enemies.append(e)
    enemies[:] = new_enemies

    # Remove bullets that go out of bounds
    bullets[:] = [b for b in bullets if abs(b[0]) < 50 and abs(b[1]) < 50]

    # Simulate enemies damaging player if close
    for e in enemies:
        dist = math.hypot(e[0] - player_pos[0], e[1] - player_pos[1])
        if dist < 2.0 and not invincible:
            player_health = max(0, player_health - 1)

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global player_pos, player_angle, invincible, one_shot_kill
    speed = 0.5
    rad = math.radians(player_angle)

    if key == b'w':
        player_pos[0] += speed * math.sin(rad)
        player_pos[1] -= speed * math.cos(rad)
    elif key == b's':
        player_pos[0] -= speed * math.sin(rad)
        player_pos[1] += speed * math.cos(rad)
    elif key == b'a':
        player_angle += 5
    elif key == b'd':
        player_angle -= 5
    elif key == b'i':  # Toggle invincibility
        invincible = not invincible
    elif key == b'k':  # Toggle one-shot-kill
        one_shot_kill = not one_shot_kill

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rad = math.radians(player_angle)
        bx = player_pos[0] + math.sin(rad)
        bz = player_pos[1] - math.cos(rad)
        bullets.append([bx, bz, player_angle])

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Bullet Frenzy - Steps 5 to 9")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(16, update, 0)

    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
