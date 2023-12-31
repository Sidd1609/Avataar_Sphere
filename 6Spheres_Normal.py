import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Sphere parameters
initial_color = [0.92, 0.93, 0.93]  # Initial color (Silver)
selected_color = [1.0, 0.0, 0.0]   # New color on click
sphere_colors = [[initial_color for _ in range(6)] for _ in range(6)]

radius = 0.3
slices = 30
stacks = 30

selected_sphere = None

def draw_sphere():
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, slices, stacks)

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    light_position = [5.0, 5.0, 5.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def setup_material(color):
    material_ambient = [color[0] * 0.19225, color[1] * 0.19225, color[2] * 0.19225, 1.0]
    material_diffuse = [color[0], color[1], color[2], 1.0]
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = 100.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def mouse_button_callback(window, button, action, mods):
    global sphere_colors, selected_sphere

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        viewport = glGetIntegerv(GL_VIEWPORT)
        winZ = glReadPixels(x, viewport[3] - int(y), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

        if winZ[0][0] < 1.0:
            col = int(x // (viewport[2] / 6))
            row = int(y // (viewport[3] / 6))
            row = 5-row
            selected_sphere = (row, col)
            sphere_colors[row][col] = selected_color
        else:
            # Clicked outside any sphere, reset the selection
            selected_sphere = None

def print_normal_at_clicked_point():
    global selected_sphere

    if selected_sphere is not None:
        row, col = selected_sphere
        x = -2.5 + col * 1.0
        y = -2.5 + row * 1.0
        z = -5.0

        # Calculate the normal vector
        length = (x**2 + y**2 + z**2)**0.5
        normal = [x / length, y / length, z / length]

def render(window):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)

    for i in range(6):
        for j in range(6):
            glPushMatrix()

            # Position each sphere in the grid
            glTranslatef(-2.5 + j * 1.0, -2.5 + i * 1.0, -5.0)

            # Rotate the spheres for better visibility
            glRotatef(45, 1, 1, 0)

            setup_lighting()
            setup_material(sphere_colors[i][j])

            draw_sphere()

            glPopMatrix()

    glfw.swap_buffers(window)
    print_normal_at_clicked_point()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Color Changing Spheres", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    glfw.set_mouse_button_callback(window, mouse_button_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
