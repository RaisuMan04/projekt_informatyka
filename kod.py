import numpy as np
import sys
from math import *

o = object()

class Transformacje:  
    def __init__(self, model):
        """
        """
        if model == "wgs84":
            self.a = 6378137.0
            self.b = 6356752.31424518 
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "krasowski":
            self.a = 6378245.0
            self.b = 6356863.019
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) 
        self.ecc2 = (2 * self.flat - self.flat ** 2) 
        
    # jednostki
    jednostka = sys.argv[2]
    if jednostka == "bez":
        pass
    else:
        output = jednostka
        
    #z radianów na stopnie
    def rad2dms(x):
        sig = ' '
        if x<0:
            sig = '-'
            x = abs(x)
        x = x * 180 / pi
        d = int(x)
        m = int(60 * (x - d))
        s = (x - d - m/60) * 3600
        return(f'{sig}{d:3d}{chr(176)}{abs(m):2d}\'{abs(s):7.5f}\"')
        
    def xyz2plh(self, X, Y, Z, output = jednostka):
        """
        """
        r = sqrt(X**2 + Y**2)           
        p_0 = atan(Z / (r * (1 - self.ecc2)))    
        p = 0
        while abs(p_0 - p) > 0.000001/206265:    
            p_0 = p
            N = self.a / sqrt(1 - self.ecc2 * sin(p_0)**2)
            h = r / cos(p_0) - N
            p = atan((Z/r) * (((1 - self.ecc2 * N/(N + h))**(-1))))
        l = atan(Y/X)
        N = self.a / sqrt(1 - self.ecc2 * (sin(p))**2);
        h = r / cos(p) - N       
        if output == "dec_degree":
            return degrees(p), degrees(l), h 
        elif output == "dms":
            p = rad2dms(degrees(p))
            l = rad2dms(degrees(l))
            return p, l, h
        else:
            raise NotImplementedError(f"{output} - output format not defined")
            
    def plh2xyz(self, p, l, h):
        """
        """
        N = self.a / sqrt(1 - self.ecc2 * sin(p*pi/180)**2)
        X = (N + h) * np.cos(p*pi/180) * np.cos(l*pi/180)
        Y = (N + h) * np.cos(p*pi/180) * np.sin(l*pi/180)
        Z = ((N * (1 - self.ecc2)) + h) * np.sin(p*pi/180)
        return X, Y, Z
    
if __name__ == "__main__":
    # utworzenie obiektu
    geo = Transformacje(model = sys.argv[3])
    # dane XYZ geocentryczne
    plik = sys.argv[4]
    method = sys.argv[1]
    
    with open(plik, 'r') as t:
        text = t.readlines()
        dane = text[4:]
        wsp = []
        for linia in dane:
            elem = linia.replace(",", " ")
            x, y, z = elem.split()
            wsp.append([float(x), float(y), float(z)])
        wsp = np.array(wsp)
        X = wsp[:,0]
        Y = wsp[:,1]
        Z = wsp[:,2]
        wyniki = []
        for i in range(0, len(wsp)):
            phi, lam, h = geo.xyz2plh(X[i], Y[i], Z[i])
            wyniki.append([phi, lam, h])
        wyniki = np.array(wyniki)
        
    # gdy plik ze wsp zawiera wsp. XYZ
    if method == "xyz2plh":
        with open('raport_xyz2plh.txt', 'w') as p:
            p.write('      phi      |       lam      |  h [m]     \n')
            for phi, lam, h in wyniki:
                p.write(f'{phi:.12f}  {lam:.12f}  {h:.3f} \n')
    # gdy plik ze wsp zawiera wsp. PLH
            
    with open('raport_xyz2plh.txt', 'r') as l:
        text = l.readlines()
        dane = text[1:]
        wsp_1 = []
        for linia in dane:
            elem = linia.replace(",", " ")
            phi, lam, h = elem.split()
            wsp_1.append([float(phi), float(lam), float(h)])
        wsp_1 = np.array(wsp_1)
        Phi = wsp_1[:,0]
        Lam = wsp_1[:,1]
        H = wsp_1[:,2]
        wyniki2 = []
        for i in range(0, len(wsp_1)):
            X1, Y1, Z1 = geo.plh2xyz(Phi[i], Lam[i], H[i])
            wyniki2.append([X1, Y1, Z1])
        wyniki2 = np.array(wyniki2)
            
    with open('raport_plh2xyz.txt', 'w') as p:
        p.write('    X [m]   |    Y [m]   |    Z [m]    \n')
        for X, Y, Z in wyniki2:
            p.write(f'{X:.3f}, {Y:.3f}, {Z:.3f} \n')
      
print("Program został wykonany poprawnie :)")