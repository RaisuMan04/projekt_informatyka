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
        
    # PODAWANIE JEDNOSTKI
    jednostka = sys.argv[2]
    if jednostka == "dec_degree" or jednostka == "dms" or jednostka == "bez_jednostki":
        pass
    else:
        raise NotImplementedError(f"Jednostka '{jednostka}' to jednostka nieobługiwana albo nieprawidłowa")
        
    # RAD - DMS
    def rad2dms(self, x):
        sig = ' '
        if x<0:
            sig = '-'
            x = abs(x)
        x = x * 180 / pi
        d = int(x)
        m = int(60 * (x - d))
        s = (x - d - m/60) * 3600
        return(f'{sig}{d:3d}{chr(176)}{abs(m):2d}\'{abs(s):7.5f}\"')
    
    # DMS - RAD
    def dms2rad(self, d, m, s):
        kat_rad = (d + m/60 + s/3600) * pi/180
        return(kat_rad)
        
    # XYZ - PLH
    def xyz2plh(self, X, Y, Z):
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
        return p, l, h
    
    # PLH - XYZ      
    def plh2xyz(self, p, l, h):
        """
        """
        N = self.a / sqrt(1 - self.ecc2 * sin(p)**2)
        X = (N + h) * np.cos(p) * np.cos(l)
        Y = (N + h) * np.cos(p) * np.sin(l)
        Z = ((N * (1 - self.ecc2)) + h) * np.sin(p)
        return X, Y, Z
    
    # XYZ - NEUp
    def neup(self, p, l, h, X2, Y2, Z2):
        R = np.array([[-np.sin(p)*np.cos(l), -np.sin(p), np.cos(p)*np.cos(l)],
                      [-np.sin(p)*np.sin(l), np.cos(l), np.cos(p)*np.sin(l)],
                      [np.cos(p), 0, np.sin(p)]])
        X1, Y1, Z1 = self.plh2xyz(p, l, h)
        dx = np.array([X1, Y1, Z1]) - np.array([X2, Y2, Z2])
        dX = R @ dx
        return(dX)
        
    # XYZ - GK
    
    # pierwszy wertykał - wzór na N
    def Np(self, p):
        N = self.a / np.sqrt(1 - self.ecc2 * sin(p)**2)
        return(N)

    # sigma
    def sigma(self, p):
        A0 = 1 - (self.ecc2 / 4) -((3 * self.ecc2 ** 2) / 64) -((5 * self.ecc2 ** 3) / 256)
        A2 = (3 / 8) * (self.ecc2 + (self.ecc2 ** 2) / 4 + (15 * self.ecc2 ** 3) / 128)
        A4 = (15 / 256) * (self.ecc2 ** 2 + (3 * self.ecc2 ** 3) / 4)
        A6 = (35 * self.ecc2 ** 3) / 3072
        sigma = self.a * ((A0 * p) - (A2 * sin(2*p)) + (A4 * sin(4*p)) - (A6 * sin(6*p)))
        return(sigma)

    # PL - XY GK
    def pl2xygk(self, p, l, l_0):
        b2 = (self.a ** 2) * (1 - self.ecc2)
        ep2 = (self.a ** 2 - b2) / b2
        dl = l - l_0
        t = tan(p)
        n2 = ep2 * (cos(p) ** 2)
        N = self.Np(p)
        s = self.sigma(p)
        x_gk = s + ((dl ** 2 / 2) * N * sin(p) * cos(p) * (1 + (((dl ** 2)/12) * (cos(p) ** 2) * (5 - t **2 + 9 * n2 + 4 * n2 ** 2)) + (((dl ** 4) / 360) * (cos(p) ** 4 ) * (61 -58 * (t ** 2) + t ** 4 + 270 * n2 -330 * n2 * (t ** 2)))))
        y_gk = dl * N * cos(p) * (1 + (((dl ** 2)/6) * (cos(p) ** 2) * (1 - t ** 2 + n2)) + (((dl ** 4 ) / 120) * (cos(p) ** 4) * (5 -18 * t ** 2 + t ** 4 + 14 * n2 -58 * n2 * t **2))) 
        return(x_gk, y_gk)
    
    # południk zerowy i numer strefy w układzie 2000
    def strefy2000(self, l):
        l_0 = 0
        n = 0
        if l > self.dms2rad(13, 30, 0) and l < self.dms2rad(16, 30, 0):
            l_0 += self.dms2rad(15, 0, 0)
            n += 5
        if l > self.dms2rad(16, 30, 0) and l < self.dms2rad(19, 30, 0): 
            l_0 += self.dms2rad(18, 0, 0)
            n += 6
        if l > self.dms2rad(19, 30, 0) and l < self.dms2rad(22, 30, 0): 
            l_0 += self.dms2rad(21, 0, 0)
            n += 7
        if l > self.dms2rad(22, 30, 0) and l < self.dms2rad(25, 30, 0): 
            l_0 += self.dms2rad(24, 0, 0)
            n += 8
        return(l_0, n)
    
    # GK - 2000
    def xy_2000(self, x_gk, y_gk, n):
        m = 0.999923
        x = x_gk * m
        y = y_gk * m + n * 1000000 + 500000
        return(x, y)
    
    # GK - 1992
    def xy_1992(self, x_gk, y_gk):
        m = 0.9993 
        x = x_gk * m - 5300000
        y = y_gk * m + 500000
        return(x, y)

# wywołanie       
if __name__ == "__main__":
    # utworzenie obiektu
    geo = Transformacje(model = sys.argv[3])
    # dane XYZ geocentryczne
    plik = sys.argv[4]
    method = sys.argv[1]
    
    # Mamy współrzędne XYZ, chcemy PLH
    with open(plik, 'r') as t:
        text = t.readlines()
        dane = text[4:]
        wsp = []
        if method == "xyz2plh" or method == "xyz2neu":
            for linia in dane:
                elem = linia.replace(",", " ")
                x, y, z = elem.split()
                wsp.append([float(x), float(y), float(z)])
            wsp = np.array(wsp)
            X = wsp[:,0]
            Y = wsp[:,1]
            Z = wsp[:,2]
            wyniki1 = []
            for i in range(0, len(wsp)):
                phi, lam, h = geo.xyz2plh(X[i], Y[i], Z[i])
                wyniki1.append([phi, lam, h])
            wyniki1 = np.array(wyniki1)
            
        # Mamy współrzędne PLH, chcemy XYZ/chcemy skorzystać ze wsp do GK        
        elif method == "plh2xyz" or method == "pl2xygk2000" or method == "pl2xygk1992":
            wsp_plh = []
            for linia in dane:
                elem = linia.replace(",", " ")
                phi, lam, h = elem.split()
                wsp_plh.append([float(phi), float(lam), float(h)])
            wsp_plh = np.array(wsp_plh)
            Phi = wsp_plh[:,0]
            Lam = wsp_plh[:,1]
            H = wsp_plh[:,2]
            if method == "plh2xyz":
                wyniki2 = []
                for i in range(0, len(wsp_plh)):
                    X1, Y1, Z1 = geo.plh2xyz(Phi[i]*pi/180, Lam[i]*pi/180, H[i])
                    wyniki2.append([X1, Y1, Z1])
                wyniki2 = np.array(wyniki2)
            else: # w tym momencie zostawiamy wsp by z nich skorzystać do GK
                pass
        
    # gdy plik ze wsp zawiera wsp. XYZ
    if method == "xyz2plh":
        with open('raport_xyz2plh.txt', 'w') as p:
            jednostka = sys.argv[2]
            if jednostka == "dec_degree":
                p.write('      phi      |       lam      |  h [m]     \n')
                for phi, lam, h in wyniki1:
                        phi = degrees(phi)
                        lam = degrees(lam)
                        p.write(f'{phi:.12f}  {lam:.12f}  {h:.3f} \n')
            elif jednostka == "dms":
                p.write('        phi       |       lam       |  h [m]     \n')
                for phi, lam, h in wyniki1:
                    phi = geo.rad2dms(phi)
                    lam = geo.rad2dms(lam)
                    p.write(f'{phi} {lam}   {h:.3f} \n')
                
    # gdy plik ze wsp zawiera wsp. PLH
    elif method == "plh2xyz":
        with open('raport_plh2xyz.txt', 'w') as p:
            p.write('    X [m]   |    Y [m]   |    Z [m]    \n')
            for X, Y, Z in wyniki2:
                p.write(f'{X:.3f} {Y:.3f} {Z:.3f} \n')
                
    # Mamy współrzędne PLH, chcemy mieć XY 2000            
    elif method == "pl2xygk2000":
        wyniki3 = []
        for phi, lam, h in wsp_plh:
            lam_0, n = geo.strefy2000(lam*pi/180)
            x, y = geo.pl2xygk(phi*pi/180, lam*pi/180, lam_0)
            x_2000, y_2000 = geo.xy_2000(x, y, n)
            wyniki3.append([x_2000, y_2000])
        wyniki3 = np.array(wyniki3)
        with open('raport_pl2xygk2000.txt', 'w') as r:
            r.write('       X [m]     |       Y[m]    \n')
            for x, y in wyniki3:
                r.write(f'{x:.9f} {y:.9f} \n')
        
    # Mamy współrzędne PLH, chcemy mieć XY 1992            
    elif method == "pl2xygk1992":
        wyniki4 = []
        for phi, lam, h in wsp_plh:
            lam_0 = geo.dms2rad(19, 0, 0)
            x, y = geo.pl2xygk(phi*pi/180, lam*pi/180, lam_0)
            x_1992, y_1992 = geo.xy_1992(x, y)
            wyniki4.append([x_1992, y_1992])
        wyniki4 = np.array(wyniki4)
        with open('raport_pl2xygk1992.txt', 'w') as r:
            r.write('      X [m]     |      Y [m]    \n')
            for x, y in wyniki4:
                r.write(f'{x:.9f} {y:.9f} \n')
         
    # Mamy współrzędne PLH, chcemy mieć wektor NEU
    elif method == "xyz2neu":
        wyniki5 = []
        wsp_a = input("Podaj współrzędne XYZ punktu początkowego wektora przestrzennego: ")
        elem = wsp_a.replace(", ", " ")
        X2, Y2, Z2 = elem.split()
        X2, Y2, Z2 = float(X2), float(Y2), float(Z2)
        for phi, lam, h in wyniki1:
            dX = geo.neup(phi, lam, h, X2, Y2, Z2)
            wyniki5.append(dX)
        wyniki5 = np.array(wyniki5)
        with open('raport_xyz2neu.txt', 'w') as k:
            k.write('  N [m]  |   E [m]  |   U [m] \n')
            for dx in wyniki5:
                n = dx[0]
                e = dx[1]
                u = dx[2]
                k.write(f'{n:^10.4f} {e:^10.4f} {u:^10.4f} \n')
              
print("Program został wykonany poprawnie :)")