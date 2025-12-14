import numpy as np
from numpy import pi
from math import sqrt, sin, cos, tan, asin, acos, atan, atan2

class Robot:

    def __init__(self):
        self.links = []
        self.n_variables = 0
        self.has_tool = False
        self.tool_length = 0
        self.tool_link = None
    
    def add_link(self, link):

        self.links.append(link)
        self.n_variables += 1
    
    def fkine(self, angles):

        if len(angles) > self.n_variables:
            print("Error in fkine: Too many variables")
            return None

        previous = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        for n in range(len(angles)):
            
            previous = np.dot(previous, self.links[n].tf(angles[n]))

        if self.has_tool and len(angles) == self.n_variables:
            previous = np.dot(previous, self.tool_link.tf(0))

        return previous
    
    def add_tool(self, length):

        self.tool_link = Link(0, 0, length)
        self.has_tool = True
        self.tool_length = length


    def ikine(self, target):

        if self.n_variables != 6:
            return

        d1 = self.links[2].a
        d2 = self.links[3].d

        wrist = target[0:3, 3] - self.tool_length * target[0:3, 2]
        wx = wrist[0]
        wy = wrist[1]
        wz = wrist[2]

        r = sqrt(wx ** 2 + wy ** 2)

        q1 = atan2(wy, wx)
        q2 = -acos((r ** 2 + wz ** 2 + d1 ** 2 - d2 ** 2) / (2*sqrt(r ** 2 + wz ** 2)*d1)) - atan2(wz, r);
        q3 = pi/2 - acos((d2 ** 2 + d1 ** 2 - (r ** 2 + wz ** 2)) / (2*d2*d1));

        T63 = self.fkine([q1,q2,q3])
        R63 = T63[0:3, 0:3]

        # Get link objects for joint 4, 5, 6
        link4, link5, link6 = self.links[3], self.links[4], self.links[5]

        # Compute transformations
        T43 = link4.tf(0)  # t4 will be variable later
        R43 = T43[:3, :3]

        # R64 depends on q4
        # For numeric solving, we’ll scan or iteratively solve for t4
        # Example placeholder:
        R64_q4 = R43.T @ R63

        # Transformations for q5, q6
        T54 = link5.tf(0)
        T65 = link6.tf(0)
        T64 = T54 @ T65
        R64_q56 = T64[:3, :3]

        # For demonstration, compute q4, q5, q6 numerically from R matrices
        # (Replace this with your actual numeric rotation values)
        q4 = atan2(R64_q4[1, 2], R64_q4[0, 2])
        q5 = atan2(np.sqrt(R64_q4[0, 2]**2 + R64_q4[1, 2]**2), R64_q4[2, 2])
        q6 = atan2(R64_q4[2, 1], -R64_q4[2, 0])

        return np.array([q1, q2, q3, q4, q5, q6])


class Link:

    def __init__(self, alpha, a, d):
        self.alpha = alpha
        self.a = a
        self.d = d
    

    def tf(self, theta):

        r1 = [cos(theta), -sin(theta), 0, self.a]
        r2 = [sin(theta)*cos(self.alpha), cos(theta)*cos(self.alpha), -sin(self.alpha), -sin(self.alpha)*self.d]
        r3 = [sin(theta)*sin(self.alpha), cos(theta)*sin(self.alpha), cos(self.alpha), cos(self.alpha)*self.d]
        r4 = [0, 0, 0, 1]

        matrix = np.array([r1, r2, r3, r4])

        return matrix

def get_coordinates(matrix):
    
    angle = matrix[0:3, 2]
    coords = matrix[0:3, 3]

    return np.concatenate((coords, angle))


def main():

    d1 = 31
    d2 = 31
    tool = 7.5

    my_robot = Robot()
    my_robot.add_link(Link(0,     0,  0))
    my_robot.add_link(Link(-pi/2, 0,  0))
    my_robot.add_link(Link(0,     d1, 0))

    my_robot.add_link(Link(-pi/2, 0,  d2))
    my_robot.add_link(Link(pi/2,  0,  0))
    my_robot.add_link(Link(-pi/2, 0,  0))

    my_robot.add_tool(tool)

    q = np.array([1.5, -2, 0.5, -0.2, 1.3, 2])

    fkine_q = my_robot.fkine(q)
    new_q = my_robot.ikine(fkine_q)
    new_fkine = my_robot.fkine(new_q)

    print(get_coordinates(fkine_q))
    print(get_coordinates(new_fkine))


if __name__ == "__main__": 
    main()