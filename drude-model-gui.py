import numpy as np
import tkinter as tk
import random

# NEED TO:
#   - Fix plot
#   - Add animation with mp4 output
#   - Add colision to electrons
#   - Activate or disable electron-electron forces and electron-nucleon forces

k = np.float64(8.99*10E9) # N.m²/C²
q = np.float64(1.6*10E-19) # C
me = np.float64(9.109E-31) # kg
dt = 0.01
limit_distance = 2

#creates the window
root = tk.Tk()
root.title("Drude Model")
root.resizable(False,False)
width = 800
length = 400
canvas = tk.Canvas(root, width = width, height = length)
canvas.pack()
canvas.config(bg="black")

class Electron:
    def __init__(self, id, x, y, vx, vy, color="blue"):
        self.shape = canvas.create_oval(x-2, y-2, x+2, y+2, fill = color) 
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.id = id
        self.m = me
        self.q = -q  # Electron charge
        self.fx = 0
        self.fy = 0

    def update(self):	# need make it better
        self.ax = self.fx/self.m
        self.ay = self.fy/self.m
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt + 0.5*self.ax*dt**2
        self.y += self.vy * dt + 0.5*self.ay*dt**2
        canvas.move(self.shape, self.vx*dt, self.vy*dt)

    def verify_limits(self):
        x_lim = width ; y_lim = length
        if abs(self.x) >= x_lim:
            self.vx *= -1
        if abs(self.y) >= y_lim:
            self.vy *= -1
    
    def collide(self):
        global particles
        for p in particles:
            if p.type() == "Nucleon":
                d = np.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
                if d <= limit_distance: # Considering it pontual for now because of bugs
                    self.vx*=-1
                    self.vy*=-1
                    '''v_e = np.sqrt(self.vx**2 + self.vy**2)
                    r_n = np.sqrt(p.x**2 + p.y**2)
                    print("d: ", d)
                    print("v_e: ", v_e)
                    print("r_n: ", r_n)
                    alphax = (self.vx/v_e) - (p.x/r_n)
                    alphay = (self.vy/v_e) - (p.y/r_n)
                    self.vx = alphax * (v_e)
                    self.vy = alphay * (v_e)'''
            
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
    def __init__(self, id, x, y, Z, color="red"):
        self.shape = canvas.create_oval(x-2, y-2, x+2, y+2, fill = color) 
        self.Z = Z
        self.q = q*self.Z
        self.x = x
        self.y = y
        self.id = id

    def type(self):
        return "Nucleon"
    
    def update(self):
        pass
    
    def collide(self):
        pass
    
    def verify_limits(self):
        pass

class Mesh:
    def __init__(self, width, length, atom):
        global particles
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
        particles = []
        self.n_atoms = 10
    
    def getWidth(self):
        return self.width
    
    def getLength(self):
        return self.length

    def add(self, x):
        global particles
        particles.append(x)

    def backgroundMesh(self):   # Add nucleons to mesh
        id=0
        for i in range(self.n_atoms+1):
            for j in range(self.n_atoms+1):
                self.add(Nucleon(id, i*self.width/self.n_atoms, j*self.length/self.n_atoms, self.Z))
                id += 1
    
    def show(self): # Draws particles
        global particles
        for p in particles:
            match p.type():
                case "Electron":
                    plt.plot(p.x, p.y, 'ob', markersize=5)
                case "Nucleon":
                    plt.plot(p.x, p.y, 'or', markersize=5)
        

def setup():
    global mesh, width, lenght
    mesh = Mesh(width=width, length=length, atom="Cu")
    mesh.backgroundMesh()
    mesh.add(Electron(41, 10, length/2, random.randint(0,50), random.randint(-50, 50)))    

def main():
    [i.verify_limits() for i in particles]
    [i.update() for i in particles]
    [j.collide() for j in particles]
    canvas.after(int(1000*dt), main)
    

setup()
main()
root.mainloop()
