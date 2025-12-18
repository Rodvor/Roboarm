import sympy as np
from sympy import pi
from sympy import sqrt, sin, cos, tan, asin, acos, atan, atan2

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

        previous = np.Matrix([[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        for n in range(len(angles)):
            previous = previous * self.links[n].tf(angles[n])

        if self.has_tool and len(angles) == self.n_variables:
            previous = previous * self.tool_link.tf(0)

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
        q2 = -acos((r ** 2 + wz ** 2 + d1 ** 2 - d2 ** 2) / (2*sqrt(r ** 2 + wz ** 2)*d1)) - atan2(wz, r)
        q3 = pi/2 - acos((d2 ** 2 + d1 ** 2 - (r ** 2 + wz ** 2)) / (2*d2*d1))

        link1, link2, link3, link4, link5, link6 = self.links[0], self.links[1], self.links[2], self.links[3], self.links[4], self.links[5]

        R60 = target[:3, :3]
        T30 = link1.tf(q1) * link2.tf(q2) * link3.tf(q3)
        R30 = T30[:3, :3]

        R63 = R30.T * R60


        q4 = np.symbols('q4')
        q5 = np.symbols('q5')
        q6 = np.symbols('q6')

        T43 = link4.tf(q4)
        R43 = T43[:3, :3]

        R64_q4 = R43.T * R63

        T54 = link5.tf(q5)
        T65 = link6.tf(q6)
        T64 = T54 * T65
        R64_q56 = T64[:3, :3]

        # Solve q4

        func = R64_q4[1, 2]

        q4_solved = np.solve(func, q4)
        q4_solved = min(q4_solved, key=lambda v: abs(v.evalf()))

        # Solve q5

        R64_numeric = R64_q4.subs(q4, q4_solved)
        func = R64_q56[0, 2]
        value = R64_numeric[0, 2]

        q5_solved = np.solve(func - value, q5)
        q5_solved = min(q5_solved, key=lambda v: abs(v.evalf()))

        # Solve q6

        func = R64_q56[1, 0]
        value = R64_numeric[1, 0]

        q6_solved = np.solve(func - value, q6)
        q6_solved = min(q6_solved, key=lambda v: abs(v.evalf()))


        return np.Matrix([q1, q2, q3, q4_solved, q5_solved, q6_solved])


class Link:

    # Make a link with a rotational joint

    def __init__(self, alpha, a, d):
        self.alpha = alpha
        self.a = a
        self.d = d
    

    def tf(self, theta):

        # Get the transformation matrix of link

        r1 = [cos(theta), -sin(theta), 0, self.a]
        r2 = [sin(theta)*cos(self.alpha), cos(theta)*cos(self.alpha), -sin(self.alpha), -sin(self.alpha)*self.d]
        r3 = [sin(theta)*sin(self.alpha), cos(theta)*sin(self.alpha), cos(self.alpha), cos(self.alpha)*self.d]
        r4 = [0, 0, 0, 1]

        matrix = np.Matrix([r1, r2, r3, r4])

        return matrix


def get_coordinates(matrix):

    # Convert 4x4 matrix into cartesian coordinates and orientation
    
    angle = matrix[0:3, 2]
    coords = matrix[0:3, 3]

    return np.Matrix.vstack(coords, angle)


def cartesian_to_matrix(coords: list):
    
    # Convert x, y, z, alpha, beta, gamma -> 4x4 matrix

    x, y, z, alpha, beta, gamma = np.symbols('x y z alpha beta gamma')

    Rz = np.Matrix([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma),  np.cos(gamma), 0],
        [0,              0,             1]
    ])

    Ry = np.Matrix([
        [ np.cos(beta), 0, np.sin(beta)],
        [ 0,            1, 0           ],
        [-np.sin(beta), 0, np.cos(beta)]
    ])

    Rx = np.Matrix([
        [1, 0,             0            ],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha),  np.cos(alpha)]
    ])

    R = Rz * Ry * Rx

    T = np.Matrix([
    [R[0,0], R[0,1], R[0,2], x],
    [R[1,0], R[1,1], R[1,2], y],
    [R[2,0], R[2,1], R[2,2], z],
    [0,      0,      0,      1]
    ])


    subs_dict = {
        x: coords[0],
        y: coords[1],
        z: coords[2],
        alpha: coords[3],
        beta: coords[4],
        gamma: coords[5]
    }

    T_numeric = T.subs(subs_dict).evalf()

    return T_numeric

def convert_to_servo_data(angle_matrix):

    # Converts list or matrix 1x6 into angle data dict in degrees.
    servo_data = {"base": (angle_matrix[0] * 180/pi).evalf(10),
                "shoulder": (angle_matrix[1] * 180/pi).evalf(10) + 90,
                "elbow": (angle_matrix[2] * 180/pi).evalf(10) + 90,
                "forearm": (angle_matrix[3] * 180/pi).evalf(10),
                "wrist": (angle_matrix[4] * 180/pi).evalf(10),
                "end_effector_base": (angle_matrix[5] * 180/pi).evalf(10)
                }
    
    return servo_data

def my_robot():

    d1 = 385
    d2 = 380
    tool = 80

    my_robot = Robot()
    my_robot.add_link(Link(0,     0,  0))
    my_robot.add_link(Link(-pi/2, 0,  0))
    my_robot.add_link(Link(0,     d1, 0))

    my_robot.add_link(Link(-pi/2, 0,  d2))
    my_robot.add_link(Link(pi/2,  0,  0))
    my_robot.add_link(Link(-pi/2, 0,  0))

    my_robot.add_tool(tool)

    return my_robot



def main():

    robot = my_robot()

    coordinates = cartesian_to_matrix([400, 0, -200, 0, 0, 0])
    q = robot.ikine(coordinates)
    print(convert_to_servo_data(q.evalf(10)))

    #q = np.Matrix([0.2782, 0.1511, 0.1790, -0.0611, -0.0043, 0])

    fkine_q = robot.fkine(q)
    new_q = robot.ikine(fkine_q)

    print(f"Input angles:                    {q.evalf(5)}")
    print(f"Very cool cartesian coordinates: {get_coordinates(fkine_q.evalf(5))}")
    print(f"Hopefully same as input angles:  {new_q.evalf(5)}")


if __name__ == "__main__": 
    main()
