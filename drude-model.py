import numpy as np
import matplotlib.pyplot as plt

# NEED TO:
#   - Fix plot
#   - Add animation with mp4 output
#   - Add colision to electrons
#   - Activate or disable electron-electron forces and electron-nucleon forces

k = np.float64(8.99*10E9) # N.m²/C²
q = np.float64(1.6*10E-19) # C
me = np.float64(9.109E-31) # kg
dt = 0.01

class Electron:
    def __init__(self, id, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.id = id
        self.m = me
        self.q = -q  # Electron charge

    def update(self):	# need make it better
        self.ax = self.fx/self.m
        self.ay = self.fy/self.m
        self.x += self.vx * dt + 0.5*self.ax*dt**2
        self.y += self.vy * dt + 0.5*self.ay*dt**2
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def verify_limits(self, x_lim, y_lim):
        if abs(self.x) >= x_lim:
            self.x *= -1
        if abs(self.y) >= x_lim:
            self.y *= -1
            
    def type(self):
        return "Electron"
    
    def getForce(self, particles):
        self.fx = 0
        self.fy = 0
        for p in particles:
            if self.id != p.id:
                d = np.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
                fe = k*q*p.q/d**3
                self.fx += fe*(p.x - self.x)
                self.fy += fe*(p.y - self.y)

class Nucleon:
    def __init__(self, id, x, y, Z):
        # definir m e q com base no tipo de átomo, definir alguns tipos
        #print("{} created at ({}, {}) ".format(self.type(), x, y))
        self.Z = Z
        self.q = q*self.Z
        self.x = x
        self.y = y
        self.id = id

    def type(self):
        return "Nucleon"

class Mesh:
    def __init__(self, width, length, atom):
        self.atom = atom
        match atom:
            case "Al":
                self.Z = 13 # Protons
                self.lattice = 404.95E-12 # m
            case "Cu":
                self.Z = 29 # Protons
                self.lattice = 361.49E-12 # m
            case "Fe":
                self.Z = 26 # Protons
                self.lattice = 286.65E-12 # m
            case "Au":
                self.Z = 79 # Protons
                self.lattice = 407.82E-12 # m
        self.width = width
        self.length = length
        self.particles = []
        self.n_atoms = 10
    
    def getWidth(self):
        return self.width
    
    def getLength(self):
        return self.length

    def add(self, x):
        self.particles.append(x)

    def backgroundMesh(self):   # Add nucleons to mesh
        id=0
        for i in range(self.n_atoms+1):
            for j in range(self.n_atoms+1):
                self.add(Nucleon(id, i*self.width/self.n_atoms, j*self.length/self.n_atoms, self.Z))
                id += 1
    
    def show(self):
        global ax
        for p in self.particles:
            match p.type():
                case "Electron":
                    plt.plot(p.x, p.y, 'ob', markersize=5)
                case "Nucleon":
                    plt.plot(p.x, p.y, 'or', markersize=5)
        plt.show()

    def configurePlot(self):
        fig, ax = plt.subplots(1, figsize=(14,6))
        ax.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        ax.set_title("Drude Model Mesh")
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.length)
        ax.set_facecolor("black")

# MAIN CODE
mesh = Mesh(width=0.0005, length=0.001, atom="Cu")  # in meters
mesh.backgroundMesh()
mesh.add(Electron(41, mesh.getWidth()/3, mesh.getLength()/3, 0, 0))

ylim = mesh.getWidth()
xlim = mesh.getLength()

print([i.type() for i in mesh.particles])
for t in range(0, 10):
    mesh.configurePlot()
    for p in mesh.particles:
        if p.type() == "Electron":
            p.verify_limits(xlim, ylim)
            p.getForce(mesh.particles)
    for p in mesh.particles:
        if p.type() == "Electron":
            p.update()
    mesh.show()