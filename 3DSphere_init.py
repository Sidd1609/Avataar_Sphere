import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)
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

def setup_material():
    material_ambient = [0.1, 0.1, 0.1, 1.0]
    material_diffuse = [0.6, 0.6, 0.6, 1.0]
    material_specular = [0.7, 0.7, 0.7, 1.0]
    material_shininess = 50.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def render(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glPushMatrix()

    # Place the sphere at the origin
    glTranslatef(0.0, 0.0, -3.0)

    # Rotate the sphere for better visibility
    glRotatef(45, 1, 1, 0)

    setup_lighting()
    setup_material()

    draw_sphere(1.0, 30, 30)

    glPopMatrix()

    glfw.swap_buffers(window)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "3D Sphere", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
