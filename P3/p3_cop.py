def sysCall_init():
    sim = require('sim')
    global car1_handle, car2_handle, m1, m2, Fm1, Fm2, b1, b2, k, car_length, dt, pos1, vel1, pos2, vel2, collision_occurred
    
    # Get object handles
    car1_handle = sim.getObject('/Car1')
    car2_handle = sim.getObject('/Car2')
    
    # Parameters
    m1, m2 = 2.0, 1.0       # masses
    Fm1, Fm2 = 2.0, 3.0     # motor forces
    b1, b2 = 0.5, 0.3        # friction coefficients
    k = 1000.0               # spring constant
    car_length = 0.5        # car length
    dt = sim.getSimulationTimeStep()
    
    # Initial conditions
    pos1, pos2 = 3.0, 0.0   # initial positions
    vel1, vel2 = 0.0, 0.0    # initial velocities
    collision_occurred = False
    
    # Set initial positions in CoppeliaSim
    sim.setObjectPosition(car1_handle, -1, [pos1, 0, 0])
    sim.setObjectPosition(car2_handle, -1, [pos2, 0, 0])

def calculate_forces(pos1, vel1, pos2, vel2):
    global collision_occurred, Fm1, Fm2, b1, b2, k, car_length
    
    # Check for collision
    distance = pos1 - pos2
    if not collision_occurred and distance <= car_length:
        collision_occurred = True
        Fm1, Fm2 = 0, 0  # Turn off motors after collision
    
    # Calculate forces
    if collision_occurred:
        overlap = max(0, car_length - distance)
        F_spring = k * overlap
        F1 = -b1*vel1 + F_spring
        F2 = -b2*vel2 - F_spring
    else:
        F1 = Fm1 - b1*vel1
        F2 = Fm2 - b2*vel2
    
    return F1, F2

def sysCall_actuation():
    global pos1, vel1, pos2, vel2, collision_occurred
    
    dt = sim.getSimulationTimeStep()
    
    # Calculate forces
    F1, F2 = calculate_forces(pos1, vel1, pos2, vel2)
    
    # Calculate accelerations
    accel1 = F1 / m1
    accel2 = F2 / m2
    
    # Euler integration
    vel1 += dt * accel1
    vel2 += dt * accel2
    pos1 += dt * vel1
    pos2 += dt * vel2
    
    # Update positions in CoppeliaSim
    sim.setObjectPosition(car1_handle, -1, [pos1, 0, 0])
    sim.setObjectPosition(car2_handle, -1, [pos2, 0, 0])

def sysCall_sensing():
    # You could add sensor readings here if needed
    pass

def sysCall_cleanup():
    # Cleanup code if needed
    pass