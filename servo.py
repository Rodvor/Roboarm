class Servo:

    def __init__(self, name, port):

        # Naming etc.
        self.name = name
        self.port = port

        # Servo math properties
        self.hardware_max_angle = 270  # Servo hardware max in degrees
        self.pulse_range = [500, 2500]  # Servo pulse width
        self.angle_zero = 135  # Angle where servo is in position "zero". FROM HARDWARE NOT SOFTWARE range
        self.angle_range = [-135, 135]
        self.inverted = False

        # Servo variables
        self.angle = 0
        self.pulse = 1500  # Dependent on angle
        self.pulse_time = 10  # Time between each "pulse length unit"
        self.polynomial_terms = [0, 0, 0, 0]


    # Configure servo properties
    def config_angles(self, angle_zero, angle_range, hardware_max_angle, inverted):

        # Update values
        self.angle_zero = angle_zero
        self.angle_range = angle_range
        self.hardware_max_angle = hardware_max_angle
        self.inverted = inverted

        if angle_zero + angle_range[1] > hardware_max_angle:
            print(f"Warning: Servo '{self.name}' angle range exceeds hardware max angle")

        if angle_zero + angle_range[0] < 0:
            print(f"Warning: Servo '{self.name}' angle range exceeds hardware minimum angle")

        self.set_angle(0)




    def set_angle(self, angle):

        # Check that angle is not going over bounds
        max_angle = self.angle_range[1]
        min_angle = self.angle_range[0]

        if angle > max_angle:
            angle = max_angle
        
        if angle < min_angle:
            angle = min_angle

        # Set angle
        self.angle = angle

        # Update pulse
        self.update_pulse()

    def set_angular_velocity(self, angular_velocity, radians = True):

        # Calculate pulse_time rad/s -> ms/pulse_unit

        if angular_velocity == -1:
            self.pulse_time = 0
            return

        if radians:
          angular_velocity = 180/3.141592653 * angular_velocity

        # angular velocity is now °/s

        delta_pulse = self.pulse_range[1] - self.pulse_range[0]
        pulses_per_degree = delta_pulse / self.hardware_max_angle

        pulses_per_second = pulses_per_degree * angular_velocity
        milliseconds_per_pulse = 1 / pulses_per_second * 1000

        self.pulse_time = round(milliseconds_per_pulse)


    def move(self, angle, angular_velocity, radians = True):
        
        # Update angular velocity first
        self.set_angular_velocity(angular_velocity, radians)

        # Set angle
        self.set_angle(angle)

    def update_pulse(self):

        # Calculate width of pulse 500->2500 -> 2000
        delta_pulse = self.pulse_range[1] - self.pulse_range[0]

        # Calculate the angle where the servo is at from hardware 0
        hardware_angle = self.angle_zero + self.angle

        if self.inverted:
            self.pulse = round(self.pulse_range[1] - delta_pulse * hardware_angle/self.hardware_max_angle)
        else:
            self.pulse = round(self.pulse_range[0] + delta_pulse * hardware_angle/self.hardware_max_angle)
    
    def calculate_third_poly_terms(self, final_angle, max_time):

        # Used to precalculate third order polynomial terms such that they
        # don't have to be recalculated on every step
        self.max_time = max_time
        a0 = self.angle
        a1 = 0
        a2 = 3 / (max_time**2) * (final_angle - self.angle)
        a3 = -2 / (max_time**3) * (final_angle - self.angle)

        self.polynomial_terms = [a3, a2, a1, a0]
    

    def move_third_order(self, t):

        # Move according to third order polynomial
        # calculate_third_poly_terms must be ran before this

        if t >= self.max_time:
            t = self.max_time

        a3 = self.polynomial_terms[0]
        a2 = self.polynomial_terms[1]
        a1 = self.polynomial_terms[2]
        a0 = self.polynomial_terms[3]

        angle = a0 + a1*t + a2*(t**2) + a3*(t**3)

        self.move(angle, -1)



if __name__ == "__main__":
    my_servo = Servo("my_servo")
    my_servo.set_angular_velocity(0.05)
    print(my_servo.pulse_time)