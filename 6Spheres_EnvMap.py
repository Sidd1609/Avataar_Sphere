from PIL import Image
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_sphere(radius, slices, stacks):
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
    light_ambient = [1.0, 1.0, 1.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def load_texture(file_path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Set the texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Load and generate the texture
    image = Image.open(file_path).convert("RGBA")
    img_data = np.array(list(image.getdata()), np.uint8)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture

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
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-3, 3, -3, 3, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture("Swiss.JPG"))

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

    glDisable(GL_TEXTURE_2D)
    glfw.swap_buffers(window)


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(800, 600, "Spheres with Environment Map", None, None)
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
