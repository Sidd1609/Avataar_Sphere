import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)  # Set draw style to fill for solid spheres
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, slices, stacks)

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    light_position = [5.0, 5.0, 5.0, 1.0]
    light_ambient = [0.4, 0.4, 0.4, 1.0]  # Increase ambient for better visibility
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def setup_material(diffuse, specular, color):
    material_ambient = [color[0] * 0.19225, color[1] * 0.19225, color[2] * 0.19225, 1.0]
    material_diffuse = [color[0] * diffuse, color[1] * diffuse, color[2] * diffuse, 1.0]
    material_specular = [color[0] * specular, color[1] * specular, color[2] * specular, 1.0]
    material_shininess = 100.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def render(window):
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-3, 3, -3, 3, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    for i in range(6):
        for j in range(6):
            glPushMatrix()

            # Position each sphere with uniform spacing
            glTranslatef(-2.5 + i * 1.0, -2.5 + j * 1.0, -5.0)

            # Rotate the spheres for better visibility
            glRotatef(45, 1, 1, 0)

            # Linearly change the diffuse and specular parameters with reduced impact
            diffuse_param = 0.2 + (5 - i) / 7.0  # Adjust divisor for reduced impact
            specular_param = 0.2 + (5 - j) / 7.0  # Adjust divisor for reduced impact

            sphere_color = [0.92, 0.93, 0.93]  # RGB color of the sphere (Silver)

            setup_lighting()
            setup_material(diffuse_param, specular_param, sphere_color)

            draw_sphere(0.35, 30, 30)

            glPopMatrix()

    glfw.swap_buffers(window)

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(800, 600, "Visible Sphere Boundaries", None, None)
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
