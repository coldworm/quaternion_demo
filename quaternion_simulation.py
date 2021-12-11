from tkinter import *
import matplotlib.pyplot as plot
import random
import math

Version = '1.0'


def euler_to_quaternion(pitch, yaw, roll):
    c1 = math.cos(pitch / 2)
    c2 = math.cos(yaw / 2)
    c3 = math.cos(roll / 2)
    s1 = math.sin(pitch / 2)
    s2 = math.sin(yaw / 2)
    s3 = math.sin(roll / 2)
    w = c1 * c2 * c3 - s1 * s2 * s3
    x = c1 * c2 * s3 + s1 * s2 * c3
    y = s1 * c2 * c3 + c1 * s2 * s3
    z = c1 * s2 * c3 - s1 * c2 * s3
    return [x, y, z, w]


def quaternion_to_matrix(q):
    xx = q[0] * q[0]
    xy = q[0] * q[1]
    xz = q[0] * q[2]
    xw = q[0] * q[3]
    yy = q[1] * q[1]
    yz = q[1] * q[2]
    yw = q[1] * q[3]
    zz = q[2] * q[2]
    zw = q[2] * q[3]
    ww = q[3] * q[3]

    m00 = xx-yy-zz+ww
    m01 = 2 * (xy - zw)
    m02 = 2 * (xz + yw)

    m10 = 2 * (xy + zw)
    m11 = 1 - 2 * (xx + zz)
    m12 = 2 * (yz - xw)

    m20 = 2 * (xz - yw)
    m21 = 2 * (yz + xw)
    m22 = 1 - 2 * (xx + yy)
    return [[m00, m01, m02], [m10, m11, m12], [m20, m21, m22]]


class MyWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title('Quaternion simulation' + Version)
        self.window.geometry('300x500')

        Label(self.window, text='Pitch').grid(row=0, column=0, stick="we", padx=5, pady=5)
        Label(self.window, text='Yaw').grid(row=1, column=0, stick="we", padx=5, pady=5)
        Label(self.window, text='Roll').grid(row=2, column=0, stick="we", padx=5, pady=5)

        self.pitch_value = StringVar()
        self.pitch_value.set(0)
        pitch_scale = Scale(self.window,
                            from_=-3.14, to=3.14, resolution=0.02,
                            length=200,
                            variable=self.pitch_value,
                            orient=HORIZONTAL,
                            command=self.scale_resize)
        pitch_scale.grid(row=0, column=1, stick="we", padx=5, pady=5)

        self.yaw_value = StringVar()
        self.yaw_value.set(0)
        yaw_scale = Scale(self.window,
                          from_=-3.14, to=3.14, resolution=0.02,
                          length=200,
                          variable=self.yaw_value,
                          orient=HORIZONTAL,
                          command=self.scale_resize)
        yaw_scale.grid(row=1, column=1, stick="we", padx=5, pady=5)

        self.roll_value = StringVar()
        self.roll_value.set(0)
        roll_scale = Scale(self.window,
                           from_=-3.14, to=3.14, resolution=0.02,
                           length=200,
                           variable=self.roll_value,
                           orient=HORIZONTAL,
                           command=self.scale_resize)
        roll_scale.grid(row=2, column=1, stick="we", padx=5, pady=5)

        self.bt_reset = Button(self.window, text="复位", bg='#008B8B', width=5, command=self.reset) \
            .grid(row=3, column=1, columnspan=2, stick="w", padx=5, pady=5)

        self.lab_info = StringVar()
        self.lab_info.set('Start')
        Message(self.window, textvariable=self.lab_info, bg="white", width=450).place(relx=.05, rely=.45, anchor="nw")

        self.ax = plot.subplot(projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        # plot points
        self.p_o = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
        self.ax.scatter(self.p_o[0][0], self.p_o[0][1], self.p_o[0][2], s=10, c='r')
        self.ax.scatter(self.p_o[1][0], self.p_o[1][1], self.p_o[1][2], s=10, c='r')
        self.ax.scatter(self.p_o[2][0], self.p_o[2][1], self.p_o[2][2], s=10, c='g')
        self.ax.scatter(self.p_o[3][0], self.p_o[3][1], self.p_o[3][2], s=10, c='g')
        self.ax.scatter(self.p_o[4][0], self.p_o[4][1], self.p_o[4][2], s=10, c='b')
        self.ax.scatter(self.p_o[5][0], self.p_o[5][1], self.p_o[5][2], s=10, c='b')
        # plot lines
        l_x = [self.p_o[2], self.p_o[4], self.p_o[3], self.p_o[5], self.p_o[2]]
        l_x2 = [[r[col] for r in l_x] for col in range(len(l_x[0]))]
        l_y = [self.p_o[0], self.p_o[4], self.p_o[1], self.p_o[5], self.p_o[0]]
        l_y2 = [[r[col] for r in l_y] for col in range(len(l_y[0]))]
        l_z = [self.p_o[0], self.p_o[2], self.p_o[1], self.p_o[3], self.p_o[0]]
        l_z2 = [[r[col] for r in l_z] for col in range(len(l_z[0]))]
        self.ax.plot(l_x2[0], l_x2[1], l_x2[2], c='c')
        self.ax.plot(l_y2[0], l_y2[1], l_y2[2], c='c')
        self.ax.plot(l_z2[0], l_z2[1], l_z2[2], c='c')

        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_zlim(-1.1, 1.1)
        plot.show()
        self.window.mainloop()

    def reset(self):
        self.roll_value.set(0)
        self.pitch_value.set(0)
        self.yaw_value.set(0)
        self.scale_resize("")

    def scale_resize(self, text):
        roll = float(self.roll_value.get())
        pitch = float(self.pitch_value.get())
        yaw = float(self.yaw_value.get())
        q = euler_to_quaternion(pitch, yaw, roll)
        m = quaternion_to_matrix(q)
        p_n = [[0 for col in range(3)] for row in range(6)]
        for i in range(6):
            for j in range(3):
                p_n[i][j] = m[j][0]*self.p_o[i][0] + m[j][1]*self.p_o[i][1] + m[j][2]*self.p_o[i][2]

        info = "Quaternion\n%1.4f %1.4f %1.4f %1.4f\n" % (q[0], q[1], q[2], q[3])
        info = info + "Matrix\n%1.4f %1.4f %1.4f\n%1.4f %1.4f %1.4f\n%1.4f %1.4f %1.4f\n" % \
               (m[0][0], m[0][1], m[0][2], m[1][0], m[1][1], m[1][2], m[2][0], m[2][1], m[2][2])
        info = info + "Points:"
        for i in range(6):
            info = info + "\n%1.4f %1.4f %1.4f" % (p_n[i][0], p_n[i][1], p_n[i][2])
        self.lab_info.set(info)
        # print(info)

        plot.cla()
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        # plot points
        self.ax.scatter(p_n[0][0], p_n[0][1], p_n[0][2], s=10, c='r')
        self.ax.scatter(p_n[1][0], p_n[1][1], p_n[1][2], s=10, c='r')
        self.ax.scatter(p_n[2][0], p_n[2][1], p_n[2][2], s=10, c='g')
        self.ax.scatter(p_n[3][0], p_n[3][1], p_n[3][2], s=10, c='g')
        self.ax.scatter(p_n[4][0], p_n[4][1], p_n[4][2], s=10, c='b')
        self.ax.scatter(p_n[5][0], p_n[5][1], p_n[5][2], s=10, c='b')
        # plot lines
        l_x = [p_n[2], p_n[4], p_n[3], p_n[5], p_n[2]]
        l_x2 = [[r[col] for r in l_x] for col in range(len(l_x[0]))]
        l_y = [p_n[0], p_n[4], p_n[1], p_n[5], p_n[0]]
        l_y2 = [[r[col] for r in l_y] for col in range(len(l_y[0]))]
        l_z = [p_n[0], p_n[2], p_n[1], p_n[3], p_n[0]]
        l_z2 = [[r[col] for r in l_z] for col in range(len(l_z[0]))]
        self.ax.plot(l_x2[0], l_x2[1], l_x2[2], c='c')
        self.ax.plot(l_y2[0], l_y2[1], l_y2[2], c='c')
        self.ax.plot(l_z2[0], l_z2[1], l_z2[2], c='c')
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_zlim(-1.1, 1.1)
        plot.draw()


if __name__ == '__main__':
    w = MyWindow()
