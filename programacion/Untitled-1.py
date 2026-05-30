from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from stl import mesh

import tkinter as tk
import sys, os
import threading

from math import sin, cos


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def cargar(n):
    return mesh.Mesh.from_file(os.path.join(BASE_DIR, n))

base     = cargar('base.stl')
brazo1   = cargar('brazo 1.stl')
brazo1_h = cargar('brazo 1 horizontal.stl')
brazo2   = cargar('brazo 2.stl')
garra    = cargar('garra.stl')


rot_b1  = 0
rot_b1h = 0
rot_b2  = 0
rot_g   = 0


off_b1  = 10
off_b1h = 610
off_b2  = 600
off_g   = 310


scale = 0.03


cam_rot = 0

cam_x = 120
cam_y = 120
cam_z = 180


def draw(obj):

    glBegin(GL_TRIANGLES)

    for tri in obj.vectors:
        for v in tri:
            glVertex3f(v[0], v[1], v[2])

    glEnd()


def init():

    glEnable(GL_DEPTH_TEST)

    glClearColor(0.1, 0.1, 0.1, 1)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(45, 1.3, 0.1, 2000)

    glMatrixMode(GL_MODELVIEW)

# -------------------------------------------------
# ROBOT
# -------------------------------------------------
def robot():

    glPushMatrix()

    glScalef(scale, scale, scale)

    glTranslatef(-40, 0, -40)

    # ---------------- BASE ----------------

    glPushMatrix()

    glColor3f(0, 1, 0)

    draw(base)

    glPopMatrix()

    # ---------------- BRAZO 1 ----------------

    glTranslatef(40, off_b1, 40)

    glRotatef(rot_b1, 0, 1, 0)

    glPushMatrix()

    glColor3f(1, 1, 0)

    glTranslatef(-22.6, 0, -25.9)

    draw(brazo1)

    glPopMatrix()

    # ---------------- BRAZO 1 HORIZONTAL ----------------

    glTranslatef(0, off_b1h, 0)

    glRotatef(rot_b1h, 0, 0, 1)

    glPushMatrix()

    glColor3f(0.9, 0.5, 0.2)

    glTranslatef(-17.5, -17.5, -17.5)

    draw(brazo1_h)

    glPopMatrix()

    # ---------------- BRAZO 2 ----------------

    glTranslatef(off_b2, 0, 0)

    glRotatef(rot_b2, 1, 0, 0)

    glPushMatrix()

    glColor3f(1, 0, 1)

    glTranslatef(-22.6, 0, -25.9)

    draw(brazo2)

    glPopMatrix()

    # ---------------- GARRA ----------------

    glTranslatef(0, off_g, 0)

    glRotatef(rot_g, 0, 1, 0)

    glPushMatrix()

    glColor3f(0, 0, 1)

    glTranslatef(-25, 0, -25)

    draw(garra)

    glPopMatrix()

    glPopMatrix()


def display():

    global cam_rot
    global cam_x, cam_y, cam_z

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    # Rotacion orbital de camara
    rad = cam_rot * 3.1416 / 180

    eye_x = cam_x * cos(rad) - cam_z * sin(rad)
    eye_z = cam_x * sin(rad) + cam_z * cos(rad)

    gluLookAt(
        eye_x, cam_y, eye_z,
        0, 0, 0,
        0, 1, 0
    )

    robot()

    glutSwapBuffers()

    glutPostRedisplay()


def sliders():

    global rot_b1, rot_b1h, rot_b2, rot_g
    global off_b1, off_b1h, off_b2, off_g
    global scale
    global cam_rot
    global cam_x, cam_y, cam_z

    root = tk.Tk()

    root.title("Control Robot")


    def update(val):

        global rot_b1, rot_b1h, rot_b2, rot_g
        global off_b1, off_b1h, off_b2, off_g
        global scale
        global cam_rot

        rot_b1  = s1.get()
        rot_b1h = s2.get()
        rot_b2  = s3.get()
        rot_g   = s4.get()

        off_b1  = o1.get()
        off_b1h = o2.get()
        off_b2  = o3.get()
        off_g   = o4.get()

        scale = sc.get()

        cam_rot = cam.get()


    def home():

        global rot_b1, rot_b1h, rot_b2, rot_g
        global off_b1, off_b1h, off_b2, off_g
        global scale
        global cam_rot
        global cam_x, cam_y, cam_z

        rot_b1  = 0
        rot_b1h = 0
        rot_b2  = 0
        rot_g   = 0

        off_b1  = 10
        off_b1h = 610
        off_b2  = 600
        off_g   = 310

        scale = 0.03

        cam_rot = 0

        cam_x = 120
        cam_y = 120
        cam_z = 180

        s1.set(0)
        s2.set(0)
        s3.set(0)
        s4.set(0)

        o1.set(10)
        o2.set(610)
        o3.set(600)
        o4.set(310)

        sc.set(0.03)

        cam.set(0)


    def vista_frontal():

        global cam_x, cam_y, cam_z, cam_rot

        cam_x = 0
        cam_y = 120
        cam_z = 180
        cam_rot = 0

        cam.set(0)

    def vista_lateral():

        global cam_x, cam_y, cam_z, cam_rot

        cam_x = 180
        cam_y = 120
        cam_z = 0
        cam_rot = 0

        cam.set(0)

    def vista_superior():

        global cam_x, cam_y, cam_z, cam_rot

        cam_x = 0
        cam_y = 300
        cam_z = 1
        cam_rot = 0

        cam.set(0)

    def vista_iso1():

        global cam_x, cam_y, cam_z, cam_rot

        cam_x = 180
        cam_y = 140
        cam_z = 180
        cam_rot = 0

        cam.set(0)

    def vista_iso2():

        global cam_x, cam_y, cam_z, cam_rot

        cam_x = -180
        cam_y = 140
        cam_z = 180
        cam_rot = 0

        cam.set(0)


    s1 = tk.Scale(
        root,
        from_=-180,
        to=180,
        label="Brazo 1 (yaw)",
        orient="horizontal",
        command=update
    )

    s2 = tk.Scale(
        root,
        from_=-180,
        to=180,
        label="Brazo 1 Horizontal",
        orient="horizontal",
        command=update
    )

    s3 = tk.Scale(
        root,
        from_=-90,
        to=90,
        label="Brazo 2 (sube/baja)",
        orient="horizontal",
        command=update
    )

    s4 = tk.Scale(
        root,
        from_=-180,
        to=180,
        label="Garra",
        orient="horizontal",
        command=update
    )


    o1 = tk.Scale(
        root,
        from_=0,
        to=100,
        label="Offset B1",
        orient="horizontal",
        command=update
    )

    o2 = tk.Scale(
        root,
        from_=100,
        to=800,
        label="Offset B1H",
        orient="horizontal",
        command=update
    )

    o3 = tk.Scale(
        root,
        from_=100,
        to=800,
        label="Offset B2",
        orient="horizontal",
        command=update
    )

    o4 = tk.Scale(
        root,
        from_=50,
        to=500,
        label="Offset Garra",
        orient="horizontal",
        command=update
    )


    sc = tk.Scale(
        root,
        from_=0.005,
        to=0.075,
        resolution=0.001,
        label="Escala",
        orient="horizontal",
        command=update
    )


    cam = tk.Scale(
        root,
        from_=-180,
        to=180,
        label="Rotacion Camara",
        orient="horizontal",
        command=update
    )


    btn_home = tk.Button(
        root,
        text="HOME",
        command=home,
        bg="lightblue"
    )


    btn_front = tk.Button(
        root,
        text="Vista Frontal",
        command=vista_frontal
    )

    btn_side = tk.Button(
        root,
        text="Vista Lateral",
        command=vista_lateral
    )

    btn_top = tk.Button(
        root,
        text="Vista Superior",
        command=vista_superior
    )

    btn_iso1 = tk.Button(
        root,
        text="Isometrica 1",
        command=vista_iso1,
        bg="lightgreen"
    )

    btn_iso2 = tk.Button(
        root,
        text="Isometrica 2",
        command=vista_iso2,
        bg="lightgreen"
    )


    o1.set(10)
    o2.set(610)
    o3.set(600)
    o4.set(310)

    sc.set(0.03)

    cam.set(0)


    for w in [s1, s2, s3, s4,
              o1, o2, o3, o4,
              sc, cam]:

        w.pack(fill="x")

    btn_home.pack(fill="x")

    btn_front.pack(fill="x")
    btn_side.pack(fill="x")
    btn_top.pack(fill="x")

    btn_iso1.pack(fill="x")
    btn_iso2.pack(fill="x")

    root.mainloop()


def main():

    threading.Thread(
        target=sliders,
        daemon=True
    ).start()

    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH
    )

    glutInitWindowSize(900, 700)

    glutCreateWindow(b"Robot 3D Jerarquico")

    init()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()