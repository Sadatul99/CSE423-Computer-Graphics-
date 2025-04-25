from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Game settings
window_width = 800
window_height = 600
player_health = 100
player_score = 0
player_position = [0.0, 0.0, 0.0]  # x, y, z coordinates
player_velocity = [0.0, 0.0, 0.0]
player_turn_rate = 3.0
player_move_speed = 0.1
bullet_velocity = 0.2
bullet_radius = 0.05
enemy_velocity = 0.02
enemy_radius = 0.1
cheat_mode = False

# Game objects
bullets = []
enemies = []
player_turn_angle = 0

# Initialize player and enemy data
def init_game():
    global player_health, player_score, player_position, bullets, enemies
    player_health = 100
    player_score = 0
    player_position = [0.0, 0.0, 0.0]
    bullets = []
    enemies = [create_enemy() for _ in range(5)]

# Create an enemy at a random position
def create_enemy():
    return {
        'position': [random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0)],
        'velocity': [random.uniform(-enemy_velocity, enemy_velocity), random.uniform(-enemy_velocity, enemy_velocity), random.uniform(-enemy_velocity, enemy_velocity)],
        'health': 50
    }

# Function to draw a simple sphere (representing player, bullets, or enemies)
def draw_sphere(radius, color):
    slices = 10
    stacks = 10
    glPushMatrix()
    glColor3f(*color)
    glutSolidSphere(radius, slices, stacks)
    glPopMatrix()

# Handle user input (keyboard and mouse)
def handle_input(key, x, y):
    global player_velocity, player_turn_angle
    if key == b'w':
        player_velocity[2] = player_move_speed
    elif key == b's':
        player_velocity[2] = -player_move_speed
    elif key == b'a':
        player_turn_angle -= player_turn_rate
    elif key == b'd':
        player_turn_angle += player_turn_rate
    elif key == b' ':
        shoot_bullet()
    elif key == b'c':
        toggle_cheat_mode()

# Toggle cheat mode (e.g., invincibility, infinite ammo, etc.)
def toggle_cheat_mode():
    global cheat_mode
    cheat_mode = not cheat_mode
    if cheat_mode:
        print("Cheat Mode Activated: Invincibility ON.")
    else:
        print("Cheat Mode Deactivated.")

# Shoot a bullet
def shoot_bullet():
    global bullets
    bullet_position = list(player_position)
    bullet_direction = [math.cos(math.radians(player_turn_angle)), 0.0, math.sin(math.radians(player_turn_angle))]
    bullet = {'position': bullet_position, 'direction': bullet_direction}
    bullets.append(bullet)

# Update the positions of all game objects
def update_game():
    global player_position, bullets, enemies, player_health, player_score
    update_player_position()
    update_bullets()
    update_enemies()
    check_collisions()

# Update player position based on velocity and input
def update_player_position():
    global player_position
    player_position[0] += player_velocity[0]
    player_position[1] += player_velocity[1]
    player_position[2] += player_velocity[2]

# Update bullet positions and check for out-of-bounds
def update_bullets():
    global bullets
    for bullet in bullets[:]:
        bullet['position'][0] += bullet['direction'][0] * bullet_velocity
        bullet['position'][2] += bullet['direction'][2] * bullet_velocity
        if abs(bullet['position'][0]) > 10 or abs(bullet['position'][2]) > 10:
            bullets.remove(bullet)

# Update enemy positions
def update_enemies():
    global enemies
    for enemy in enemies:
        for i in range(3):
            enemy['position'][i] += enemy['velocity'][i]

# Check for bullet-enemy collisions
def check_collisions():
    global bullets, enemies, player_score, player_health
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet, enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                player_score += 10
                break
    for enemy in enemies[:]:
        if check_player_collision(enemy):
            player_health -= 10
            if player_health <= 0:
                print("Game Over!")
                init_game()

# Check if a bullet has collided with an enemy
def check_collision(bullet, enemy):
    distance = math.sqrt((bullet['position'][0] - enemy['position'][0]) ** 2 + (bullet['position'][2] - enemy['position'][2]) ** 2)
    return distance < bullet_radius + enemy_radius

# Check if an enemy has collided with the player
def check_player_collision(enemy):
    distance = math.sqrt((enemy['position'][0] - player_position[0]) ** 2 + (enemy['position'][2] - player_position[2]) ** 2)
    return distance < enemy_radius + bullet_radius

# Render the game objects (player, enemies, bullets)
def render_game():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Camera follows player
    gluLookAt(player_position[0], player_position[1] + 5, player_position[2] + 5, player_position[0], player_position[1], player_position[2], 0, 1, 0)

    # Draw player
    glPushMatrix()
    glTranslatef(player_position[0], player_position[1], player_position[2])
    draw_sphere(0.2, (0.0, 0.0, 1.0))  # Blue player
    glPopMatrix()

    # Draw enemies
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy['position'][0], enemy['position'][1], enemy['position'][2])
        draw_sphere(enemy_radius, (1.0, 0.0, 0.0))  # Red enemies
        glPopMatrix()

    # Draw bullets
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['position'][0], bullet['position'][1], bullet['position'][2])
        draw_sphere(bullet_radius, (0.0, 1.0, 0.0))  # Green bullets
        glPopMatrix()

    # Display score and health
    render_score_health()

    glutSwapBuffers()

# Render the score and health on screen
def render_score_health():
    glColor3f(1.0, 1.0, 1.0)
    glWindowPos2f(10, window_height - 30)
    stats = f"Score: {player_score}  Health: {player_health}"
    for ch in stats:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


# Main update loop
def main_loop():
    update_game()
    render_game()
    time.sleep(0.01)

# Set up OpenGL and start the game
def setup_game():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, window_width / window_height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    init_game()

# Main function to start the game
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"3D OpenGL Game")
    setup_game()
    glutDisplayFunc(render_game)
    glutIdleFunc(main_loop)
    glutKeyboardFunc(handle_input)
    glutMainLoop()

if __name__ == "__main__":
    main()
