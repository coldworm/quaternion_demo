# Simulation of 3D rotation by quaternion
# Copyright (C) <2020>  <coldworm>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import matplotlib.pyplot as plot
import math

scale = 1


class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def normalize(self):
        l = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l
        self.w = self.w / l

    def __mul__(self, q):
        q_n = Quaternion()
        q_n.x = q.w * self.x - q.z * self.y + q.y * self.z + q.x * self.w
        q_n.y = q.z * self.x + q.w * self.y - q.x * self.z + q.y * self.w
        q_n.z = -q.y * self.x + q.x * self.y + q.w * self.z + q.z * self.w
        q_n.w = -q.x * self.x - q.y * self.y - q.z * self.z + q.w * self.w
        return q_n


class Conversion:
    @staticmethod
    def angle_to_quaternion(x=0, y=0, z=1, angle=0):
        l = math.sqrt(x * x + y * y + z * z)
        x = x / l
        y = y / l
        z = z / l
        q = Quaternion()
        rad = angle / 180.0 * math.pi
        s = math.sin(rad / 2)
        q.x = x * s
        q.y = y * s
        q.z = z * s
        q.w = math.cos(rad / 2)
        return q

    @staticmethod
    def quat_to_matrix(q):
        m = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        sqw = q.w * q.w
        sqx = q.x * q.x
        sqy = q.y * q.y
        sqz = q.z * q.z

        # invs(inverse square length) is only required if quaternion is not already normalised
        invs = 1 / (sqx + sqy + sqz + sqw)
        m[0][0] = (sqx - sqy - sqz + sqw) * invs  # since sqw + sqx + sqy + sqz = 1 / invs * invs
        m[1][1] = (-sqx + sqy - sqz + sqw) * invs
        m[2][2] = (-sqx - sqy + sqz + sqw) * invs

        tmp1 = q.x * q.y
        tmp2 = q.z * q.w
        m[1][0] = 2.0 * (tmp1 + tmp2) * invs
        m[0][1] = 2.0 * (tmp1 - tmp2) * invs

        tmp1 = q.x * q.z;
        tmp2 = q.y * q.w;
        m[2][0] = 2.0 * (tmp1 - tmp2) * invs
        m[0][2] = 2.0 * (tmp1 + tmp2) * invs
        tmp1 = q.y * q.z;
        tmp2 = q.x * q.w;
        m[2][1] = 2.0 * (tmp1 + tmp2) * invs
        m[1][2] = 2.0 * (tmp1 - tmp2) * invs
        return m

    @staticmethod
    def vector_rightotation(v, m):
        v_n = [None] * 3
        for i in range(0, 3):
            v_n[i] = m[i][0] * v[0] + m[i][1] * v[1] + m[i][2] * v[2]
        return v_n;


if __name__ == '__main__':
    # points for X Y Z axis
    x_axis = [0, 1, 0, 0, 0, 0]
    y_axis = [0, 0, 0, 1, 0, 0]
    z_axis = [0, 0, 0, 0, 0, 1]

    # points for original arrow
    x_right_org = [i * scale for i in [0, 1 / 6, 1 / 6, 1 / 3, 0]]
    y_right_org = [i * scale for i in [0, 0, 0, 0, 0]]
    z_right_org = [i * scale for i in [0, 0, 2 / 3, 2 / 3, 1]]
    x_left_org = [i * scale for i in [0, -1 / 3, -1 / 6, -1 / 6, 0]]
    y_left_org = [i * scale for i in [0, 0, 0, 0, 0]]
    z_left_org = [i * scale for i in [1, 2 / 3, 2 / 3, 0, 0]]

    fig = plot.figure(1)
    ax = fig.gca(projection='3d')
    ax.plot(x_axis, y_axis, z_axis, c='r', linestyle='--')
    # show original arrow
    ax.plot(x_right_org, y_right_org, z_right_org, c='b', linestyle='--')
    ax.plot(x_left_org, y_left_org, z_left_org, c='y', linestyle='--')
    # set X Y Z axis label
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    x_right_new = [None] * 5
    y_right_new = [None] * 5
    z_right_new = [None] * 5
    x_left_new = [None] * 5
    y_left_new = [None] * 5
    z_left_new = [None] * 5
    q = Conversion.angle_to_quaternion(1, 0, 0, 90)  # rotation angle
    # q2 = Conversion.angle_to_quaternion(0, 1, 0, 90)
    # q = q*q2
    m = Conversion.quat_to_matrix(q)
    # calculate points of new arrow
    for i in range(0, 5):
        v_org = [x_right_org[i], y_right_org[i], z_right_org[i]]
        v_new = Conversion.vector_rightotation(v_org, m)
        x_right_new[i] = v_new[0]
        y_right_new[i] = v_new[1]
        z_right_new[i] = v_new[2]

        v_org = [x_left_org[i], y_left_org[i], z_left_org[i]]
        v_new = Conversion.vector_rightotation(v_org, m)
        x_left_new[i] = v_new[0]
        y_left_new[i] = v_new[1]
        z_left_new[i] = v_new[2]
    # show new arrow
    ax.plot(x_right_new, y_right_new, z_right_new, c='b', linestyle='-')
    ax.plot(x_left_new, y_left_new, z_left_new, c='y', linestyle='-')
    plot.show()
