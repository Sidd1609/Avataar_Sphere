import glfw
import math
from OpenGL.GL import *
from OpenGL.GLU import *


#Sphere parameters
initial_color = [0.65, 0.65, 0.65]
sphere_colors = [[initial_color for _ in range(6)] for _ in range(6)]
radius = 0.35
slices = 30 #For Smooth Rendering
stacks = 30 #For Smooth Rendering
changed_spheres = [ ] #To keep track of the sphere(s) that were clicked (with order)

#For Positioning the Spheres uniformly 
x_spacing = -2.5
y_spacing = -2.5
z_depth = -5.0

#Scaling factor 
far_value = 3.0 
near_value = -3.0


def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, slices, stacks)

def setup_lighting():
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    light_position = [5.0, 5.0, 5.0, 1.0]
    light_ambient = [0.25, 0.25, 0.25, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def setup_material(diffuse, specular, color):    
    material_ambient = [color[0], color[1], color[2], 1.0] 
    material_diffuse = [color[0] * diffuse, color[1] * diffuse, color[2] * diffuse, 1.0]
    material_specular = [color[0] * specular, color[1] * specular, color[2] * specular, 1.0]
    material_shininess = 100.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)


def calculate_sphere_normal(x, y, z, l, m, n, radius):
    #Vertext Normal at the Point Clicked on the Sphere
    normal_x = (x - l) / radius #Scaling it with [0,1] for reducing computation
    normal_y = (y - m) / radius
    normal_z = (z - n) / radius

    length = (normal_x**2 + normal_y**2 + normal_z**2)**0.5
    #Normalizing the vector
    normal_x /= length
    normal_y /= length
    normal_z /= length

    return normal_x, normal_y, normal_z

def is_within_sphere(row, col, winX, winY, winZ):
    sphere_center = (y_spacing + col * 1.0, x_spacing + row * 1.0, z_depth)
    
    model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    x, y, z = gluUnProject(winX, winY, winZ, model_view, projection, viewport)
    distance = math.sqrt((x - sphere_center[0])**2 + (y - sphere_center[1])**2)
    return distance <= radius

def mouse_button_callback(window, button, action, mods):
    global sphere_colors, selected_sphere
    global changed_spheres

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        z = z_depth
        viewport = glGetIntegerv(GL_VIEWPORT)
        winZ = glReadPixels(x, viewport[3] - int(y), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

        if winZ[0][0] < 1.0: 
            #Estimating which sphere the mouse click might by designing a grid like estimation.
            col = int(x // (viewport[2] / 6))
            row = int(y // (viewport[3] / 6))

            print("Selected Sphere @ in Grid -->", (row, col))

            if is_within_sphere(row, col, x, y, winZ):
                sphere_center = (y_spacing + col * 1.0, x_spacing + row * 1.0, z_depth)

                normal = calculate_sphere_normal(x, y, z, *sphere_center, radius)
                print("Normal @ point-> ", normal)

                #Estimating color of the sphere using the given formula  = (normal + 1) / 2 
                color = [(normal[0] + 1) / 2, (normal[1] + 1) / 2, (normal[2] + 1) / 2]
                print("Computing Color... -> ", color)

                #Indexing the right sphere for changing the color (managing shift in index--> bottom most left is 0,0 so changing that)
                row = abs(5-row)
                    
                sphere_colors[col][row] = color
                changed_spheres.append([col, row])

        else:
            print("Resetting Previous Selection! (First Change First Reset (FIFR))")
            sphere_colors[changed_spheres[0][0]][changed_spheres[0][1]] = initial_color
            changed_spheres = changed_spheres[1:]

    else:
        print("Click to register an event (Sphere-> change color & Outside Sphere-> Reset Previous Selection)")
    

def render(window):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(near_value, far_value, near_value, far_value, -10, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    for i in range(6):
        for j in range(6):
            glPushMatrix()
            glTranslatef(x_spacing + i, y_spacing + j, z_depth)

            diffuse_param = 1 - (i / 5.0) #This change translated the shades changed linearly from light to dark 
            specular_param = (j / 5.0) #This change translated the specular change linearly from shiny to rough surfaces

            setup_lighting()
            setup_material(diffuse_param, specular_param, sphere_colors[i][j])

            draw_sphere(radius, slices, stacks)

            glPopMatrix()

    glfw.swap_buffers(window)


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Avataar 6x6 Spheres", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback) 

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
