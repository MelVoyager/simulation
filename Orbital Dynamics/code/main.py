import numpy as np
import argparse
from planet import *
from plot import plot

def earth_orbit(delta_t=100, method='euler_cromer'):
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 1]))
    rs, vs = planetsystem.simulate(365.243 * 86400, delta_t=delta_t, method=method)
    return rs, vs

def jupiter_orbit(delta_t=1000, method='euler_cromer'):
    planetsystem = Jupiter(r=np.array([1, 0]), v=np.array([0, 1]))
    rs, vs = planetsystem.simulate(4332.38 * 86400, delta_t=delta_t, method=method)
    return rs, vs

def p1_1():
    delta_t = 100
    rs, vs = earth_orbit(delta_t, 'euler')
    plot(rs, downsample=50000 // delta_t, save=None, title='Earth\'s orbit by Euler method')
    
def p1_2():
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 5]))
    delta_t = 10000
    rs, vs = planetsystem.simulate(t=1e11, delta_t=delta_t, method='euler_cromer', force='delta')
    plot(rs, downsample=10000, save=None, title='Earth\'s orbit under fine-tuning gravity')

def p1_3(coef=1):
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 2.5855e-6 * coef]))
    delta_t = int(1e7)
    rs, vs = planetsystem.simulate(t=5e13, delta_t=delta_t, method='euler_cromer', force='cube')
    plot(rs, downsample=10000, save=None, title='Earth\'s orbit under cubic gravity')

def p1_4():
    delta_t = 100
    rs, vs = earth_orbit(delta_t, 'euler_richardson')
    plot(rs, downsample=50000 // delta_t, save=None, title='Earth\'s orbit by Euler-Richardson method')
    
def p2_1():
    # Earth
    rs, vs = earth_orbit()
    distances = np.linalg.norm(rs, axis=1)
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    print(f"Max distance(Earth): {max_distance:.4e}, Min distance(Earth): {min_distance:.4e}, L2_Error={((max_distance - min_distance)/ max_distance * 100):.4e}%")
    
    # Jupiter
    rs, vs = jupiter_orbit()
    distances = np.linalg.norm(rs, axis=1)
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    print(f"Max distance(Jupiter): {max_distance:.4e}, Min distance(Jupiter): {min_distance:.4e}, L2_Error={((max_distance - min_distance)/ max_distance * 100):.4e}%")
    plot(rs, downsample=1000, save=None, title='Jupiter\'s orbit by Euler Cromer method')

def p2_2():
    def L2_Error(areas):
        differences = areas - areas.mean()
        return areas.mean(), np.linalg.norm(differences, ord=2) / np.linalg.norm(areas)
    
    # Earth
    delta_t = 1000
    rs, vs = earth_orbit(delta_t)
    areas = 0.5 * np.abs(rs[:-1, 0] * rs[1:, 1] - rs[1:, 0] * rs[:-1, 1])
    mean, L2 = L2_Error(areas)
    print(f"mean area per step(Earth): {mean:.4e}, L2_Error(Earth): {(L2 * 100):.4e}%")
    
    # Jupiter
    delta_t = 1000
    rs, vs = jupiter_orbit(delta_t)
    areas = 0.5 * np.abs(rs[:-1, 0] * rs[1:, 1] - rs[1:, 0] * rs[:-1, 1])
    mean, L2 = L2_Error(areas)
    print(f"mean area per step(Jupiter): {mean:.4e}, L2_Error(Jupiter): {(L2 * 100):.4e}%")


def p2_3():
    def kepler_third_law(rs, delta_t):
        # Calculate the distance between each point and the sun
        distances = np.linalg.norm(rs, axis=1)
        
        # Find the farthest and the closest distance
        r_max = np.max(distances)
        r_min = np.min(distances)
        
        # Calculate the semi-major axis a
        a = 0.5 * (r_max + r_min)
        
        # The period T is the total time, i.e. delta t multiplies the number of data points
        T = delta_t * len(rs)
        
        # Calculate a^3/T^2
        value = (a**3) / (T**2)
        
        return value
    
    # Earth
    delta_t = 1000
    rs, vs = earth_orbit(delta_t)
    v_earth = kepler_third_law(rs, delta_t)
    
    # Jupiter
    delta_t = 1000
    rs, vs = jupiter_orbit(delta_t)
    v_jupiter = kepler_third_law(rs, delta_t)
    print(f"A^3/T^2(Earth):{v_earth:.4e}, A^3/T^2(Jupiter):{v_jupiter:.4e}, relative_error={(np.abs(v_earth - v_jupiter) / v_jupiter * 100):.4e}%")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute function based on arguments.')
    parser.add_argument('a1', type=str, default='1', nargs='?', help='Problem number')
    parser.add_argument('a2', type=str, default='1', nargs='?', help='Question number')
    parser.add_argument('a3', type=str, default=None, nargs='?', help='Coefficient for p1_3')
    
    args = parser.parse_args()
    func_name = f'p{args.a1}_{args.a2}'
    
    try:
        # Use globals() to get the current global symbol table, and then execute the corresponding function
        if args.a3:
            globals()[func_name](float(args.a3))
        else:
            globals()[func_name]()
            
    except KeyError:
        print(f"Function {func_name} not found!")
        