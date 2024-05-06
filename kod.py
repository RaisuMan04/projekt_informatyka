import numpy as np
import sys
from math import *

o = object()

class Transformacje:
    
    def __init__(self, model: str = "wgs84"):
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
            self.b = 6378102.119674574
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) 
        self.ecc2 = (2 * self.flat - self.flat ** 2) 
        
    def xyz2plh(self, X, Y, Z, output = "dec_degree"):
        """
        """
        r = sqrt(X**2 + Y**2)           
        lat_prev = atan(Z / (r * (1 - self.ecc2)))    
        lat = 0
        while abs(lat_prev - lat) > 0.000001/206265:    
            lat_prev = lat
            N = self.a / sqrt(1 - self.ecc2 * sin(lat_prev)**2)
            h = r / cos(lat_prev) - N
            lat = atan((Z/r) * (((1 - self.ecc2 * N/(N + h))**(-1))))
        lon = atan(Y/X)
        N = self.a / sqrt(1 - self.ecc2 * (sin(lat))**2);
        h = r / cos(lat) - N       
        if output == "dec_degree":
            return degrees(lat), degrees(lon), h 
        elif output == "dms":
            lat = rad2dms(degrees(lat))
            lon = rad2dms(degrees(lon))
            return f"{lat[0]:02d}:{lat[1]:02d}:{lat[2]:.2f}", f"{lon[0]:02d}:{lon[1]:02d}:{lon[2]:.2f}", f"{h:.3f}"
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
    geo = Transformacje(model = "wgs84")
    # dane XYZ geocentryczne
    with open('wsp_inp.txt', 'r') as t:
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
            
    with open('raport_xyz2plh.txt', 'w') as p:
        p.write('      phi      |       lam      |  h [m]     \n')
        for phi, lam, h in wyniki:
            p.write(f'{phi:.12f}  {lam:.12f}  {h:.3f} \n')
            
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