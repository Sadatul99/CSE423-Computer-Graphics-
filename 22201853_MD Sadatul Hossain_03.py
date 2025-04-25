from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random

# Window dimensions
width, height = 800, 600

# Grid settings
grid_size = 10
cell_size = 2

# Game state
player_pos = [0.0, 0.0]     
player_angle = 0.0
bullets = []  
enemies = [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(5)]
player_health = 5
is_game_over = False

# Camera
camera_mode = 0       # 0 = third-person, 1 = first-person
camera_distance = 10.0
camera_height = 15.0
camera_angle_off = 0.0

spawn_timer = 0
spawn_interval = 100  # frames between spawns (adjust this for difficulty)

player_score = 0
missed_bullets = 0

cheat_mode     = False
auto_follow    = False

cheat_cooldown = 0
CHEAT_COOLDOWN_FRAMES = 30   # adjust to taste (30 frames ≈ 0.5 s at 60 Hz)

max_enemies = 5  # This will ensure that there are always 5 enemies at most.



def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)

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
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], 1.0, bullet[1])
        glutSolidCube(0.2)
        glPopMatrix()

def draw_health():
    glColor3f(1, 1, 1)
    def draw_text(x, y, text):
        glWindowPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    draw_text(10, height - 20, f"Health: {player_health}")
    draw_text(10, height - 40, f"Score: {player_score}")
    draw_text(10, height - 60, f"Missed Bullets: {missed_bullets}")


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0.0, player_pos[1])
    glRotatef(player_angle, 0.0, 1.0, 0.0)

    if is_game_over:
        glRotatef(90, 0.0, 0.0, 1.0)

    glTranslatef(0.0, 1.5, 0.0)

    # Head
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0.0, 1.25, 0.0)  
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    # Body
    glPushMatrix()
    glColor3f(0.3, 0.7, 0.3)
    glScalef(1.0, 2.0, 0.5)
    glutSolidCube(1.0)
    glPopMatrix()

    # Arms
    for xOff in (-0.75, 0.75):
        glPushMatrix()
        glColor3f(1.0, 0.8, 0.6)
        glTranslatef(xOff, 1.0, 0.0)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.2, 0.2, 1.0, 12, 12)
        glPopMatrix()

    # Legs
    for xOff in (-0.3, 0.3):
        glPushMatrix()
        glColor3f(0.2, 0.2, 1.0)
        glTranslatef(xOff, -1.0, 0.0)
        glScalef(0.3, 1.5, 0.3)
        glutSolidCube(1.0)
        glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0.0, 0.5, 1.0)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glScalef(0.2, 0.2, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

def draw_enemies():
    for e in enemies:
        glPushMatrix()
        glTranslatef(e[0], 0.5, e[1])  # Position at ground level

        # Draw body
        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)  # Red
        glutSolidSphere(0.5, 20, 20)
        glPopMatrix()

        # Draw head (offset vertically)
        glPushMatrix()
        glColor3f(0.8, 0.6, 0.6)  # Light pinkish head
        glTranslatef(0.0, 0.6, 0.0)  # Slightly above the body
        glutSolidSphere(0.3, 20, 20)
        glPopMatrix()

        glPopMatrix()


def is_player_hit(enemy, threshold=1.0):
    dx = player_pos[0] - enemy[0]
    dz = player_pos[1] - enemy[1]
    return math.hypot(dx, dz) < threshold

def check_collision(b, e, threshold=1.0):
    dx = b[0] - e[0]
    dz = b[1] - e[1]
    return math.hypot(dx, dz) < threshold

def update(value):
    global bullets, enemies, player_health, is_game_over, spawn_timer
    global player_score, missed_bullets, player_angle
    global cheat_mode, cheat_cooldown  # <<--- added
    global max_enemies  # <<--- added

    if is_game_over:
        # Game over, check if 'r' key was pressed to restart
        return  # Prevent any further updates if game is over

    # Cheat‐mode auto‐fire + spin
    if cheat_mode:
        # 1) rotate the player continuously
        player_angle = (player_angle + 1) % 360

        # 2) only fire if our cooldown has expired
        if cheat_cooldown == 0:
            for e in enemies:
                dx = e[0] - player_pos[0]
                dz = e[1] - player_pos[1]
                angle_to_e = (math.degrees(math.atan2(dx, dz)) + 360) % 360
                diff = ((angle_to_e - player_angle + 180) % 360) - 180
                if abs(diff) < 5:  # within your 5° firing cone
                    rad = math.radians(player_angle)
                    bx = player_pos[0] + math.sin(rad)
                    bz = player_pos[1] + math.cos(rad)
                    bullets.append([bx, bz, player_angle])
                    print("Player bullet fired")  # Print when a bullet is fired
                    cheat_cooldown = 5  # reduced cooldown to 5 frames
                    break  # done with this frame’s auto‐fire

    # Decrease cooldown
    if cheat_cooldown > 0:
        cheat_cooldown -= 1

    # Move bullets
    bullet_speed = 0.2
    enemy_speed = 0.005

    for b in bullets:
        rad = math.radians(b[2])
        b[0] += bullet_speed * math.sin(rad)
        b[1] += bullet_speed * math.cos(rad)

    # Move enemies
    for e in enemies:
        dx = player_pos[0] - e[0]
        dz = player_pos[1] - e[1]
        dist = math.hypot(dx, dz)
        if dist > 0.001:
            e[0] += enemy_speed * dx / dist
            e[1] += enemy_speed * dz / dist

    # Handle bullet–enemy collisions
    new_enemies = []
    for e in enemies:
        if any(check_collision(b, e) for b in bullets):
            player_score += 1
            print(f"Enemy hit! Score now {player_score}")
        else:
            new_enemies.append(e)
    enemies = new_enemies

    # Count & remove out‐of‐bounds bullets
    out_of_bounds = [b for b in bullets if abs(b[0]) >= 50 or abs(b[1]) >= 50]
    missed_bullets += len(out_of_bounds)
    if len(out_of_bounds) > 0:
        print(f"Bullet missed: {missed_bullets}")  # Print when a bullet misses
    bullets[:] = [b for b in bullets if abs(b[0]) < 50 and abs(b[1]) < 50]

    # Enemy–player collision
    for e in enemies[:]:
        if is_player_hit(e):
            player_health -= 1
            enemies.remove(e)
            print(f"Player hit! Health now {player_health}")
            break

    if player_health <= 0:
        is_game_over = True
        print("GAME OVER")  # Print game over when health reaches 0

    # Enemy spawn
    # Ensure the number of enemies is always constant (max_enemies)
    if len(enemies) < max_enemies:
        # Only spawn if the number of enemies is less than max_enemies
        enemies.append([random.uniform(-10, 10), random.uniform(-10, 10)])

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)







    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    rad = math.radians(player_angle + camera_angle_off)

    if camera_mode == 0:
        # Third-person camera: top-down view
        cam_x = player_pos[0] - camera_distance * math.sin(rad)
        cam_z = player_pos[1] - camera_distance * math.cos(rad)
        cam_y = camera_height  # Set camera height to look from above
        gluLookAt(cam_x, cam_y, cam_z,
                  player_pos[0], 1.0, player_pos[1],
                  0, 1, 0)
    else:
        # First-person camera with slightly raised and forward position
        eye_offset = 0.6  # How high the eyes are
        forward_offset = 0.8  # Slightly forward from player center

        cam_x = player_pos[0] + forward_offset * math.sin(rad)
        cam_z = player_pos[1] + forward_offset * math.cos(rad)
        cam_y = 1.5 + eye_offset

        # Auto-follow camera logic for cheat mode (only in first-person mode)
        if cheat_mode and auto_follow and enemies:
            # Aim at the closest enemy
            e = min(enemies, key=lambda e: (e[0]-player_pos[0])**2 + (e[1]-player_pos[1])**2)
            dx, dz = e[0] - player_pos[0], e[1] - player_pos[1]
            rad_e = math.atan2(dx, dz)
            look_x = player_pos[0] + math.sin(rad_e)
            look_z = player_pos[1] + math.cos(rad_e)
            look_y = cam_y
        else:
            # Regular first-person camera look direction
            look_x = cam_x + math.sin(rad)
            look_z = cam_z + math.cos(rad)
            look_y = cam_y  # Looking straight

        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 1, 0)

    draw_grid()
    draw_boundaries()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_health()

    glutSwapBuffers()


    
def reset_game():
    global player_pos, player_health, enemies, bullets, is_game_over
    global camera_height, player_score, missed_bullets, spawn_timer

    player_pos = [0.0, 0.0]
    player_health = 5
    bullets.clear()
    enemies = [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(5)]
    player_score = 0
    missed_bullets = 0
    spawn_timer = 0
    is_game_over = False
    camera_height = 15.0

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  # ✅ Restart update loop



def keyboard(key, x, y):
    global player_pos, player_angle, cheat_mode, auto_follow

    speed = 0.5
    angle_rad = math.radians(player_angle)

    if key == b'w':  # Move forward
        player_pos[0] += speed * math.sin(angle_rad)
        player_pos[1] += speed * math.cos(angle_rad)
    elif key == b's':  # Move backward
        player_pos[0] -= speed * math.sin(angle_rad)
        player_pos[1] -= speed * math.cos(angle_rad)
    elif key == b'a':  # Rotate left
        player_angle += 5  # Increase the angle to rotate left
    elif key == b'd':  # Rotate right
        player_angle -= 5  # Decrease the angle to rotate right
        
    elif key == b'r':  # Restart the game
        reset_game()
    elif key == b'c':  # Toggle cheat mode
        cheat_mode = not cheat_mode
        print(f"Cheat mode {'enabled' if cheat_mode else 'disabled'}")
    elif key == b'v' and cheat_mode:  # Toggle auto-follow, only if cheat is ON
        auto_follow = not auto_follow
        print(f"Auto-follow {'enabled' if auto_follow else 'disabled'}")

    glutPostRedisplay()



def specialKeyListener(key, x, y):
    global camera_height, camera_angle_off

    if key == GLUT_KEY_UP:
        camera_height += 1.0
    elif key == GLUT_KEY_DOWN:
        camera_height = max(1.0, camera_height - 1.0)
    elif key == GLUT_KEY_LEFT:
        camera_angle_off -= 5.0
    elif key == GLUT_KEY_RIGHT:
        camera_angle_off += 5.0

    glutPostRedisplay()

def mouse(button, state, x, y):
    global bullets, camera_mode
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON and not is_game_over:
            rad = math.radians(player_angle)
            bx = player_pos[0] + math.sin(rad)
            bz = player_pos[1] + math.cos(rad)
            bullets.append([bx, bz, player_angle])
            print("Player bullet fired")
        elif button == GLUT_RIGHT_BUTTON:
            camera_mode = 1 - camera_mode
            print("Camera toggled:", "First Person" if camera_mode else "Third Person")

        glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Bullet Frenzy")
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutSpecialFunc(specialKeyListener)
    glutTimerFunc(16, update, 0)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
