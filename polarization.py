#!/usr/bin/env python
# encoding: utf-8
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from math import pi,sin,cos,sqrt
import numpy as np
import scipy.io
import sys
import os
# Define input parameters

# case 0: Clear atmosphere with land surface (Lambertian)
# case 1: Clear atmosphere with ocean surface
# case 2: Aerosol (desert)
# case 3: Water cloud (optical thickness 2)

# 4 different cases
ncases = 4
cases  = [0,1,2,3]

# viewing angles
va  = np.linspace(0.0,pi/2,50,endpoint=True)
umu = - np.cos(va)

# azimuth angles
phi = np.linspace(0.0,360.0,200,endpoint=True)

# wavelengths
# lam = [350.,400.,450.]

# number of photons
# N = 1e5

# run rt calculation
run_rt = True

# draw the data
# run_rt = False

# Initialize varibles for radiance and standard deviation
I = np.zeros((len(va),len(phi),ncases))
Q = np.zeros((len(va),len(phi),ncases))
U = np.zeros((len(va),len(phi),ncases))
V = np.zeros((len(va),len(phi),ncases))

x = np.zeros((len(va),len(phi)))
y = np.zeros((len(va),len(phi)))

if(run_rt):
    for case in cases:
        for iphi in range(len(phi)):
            for iumu in range(len(umu)):
                print('run mystic: case %g phi %g umu %g' % (case,phi[iphi],va[iumu]*180.0/pi))
                tmp = open('mystic.inp').read()
                inp = open('mystic_run.inp','w')
                inp.write(tmp)
                inp.write('umu %g \n' % umu[iumu])
                inp.write('phi %g \n' % phi[iphi])

                if case == 0:
                    inp.write('albedo 0.2 \n') # Lambertian surface albedo of 0.2
                elif case == 1:
                    inp.write('bpdf_tsang_u10 2 \n') # BRDF for ocean, wind speed 2
                elif case == 2:
                    inp.write('aerosol_default \n')
                    inp.write('aerosol_species_file desert \n') # OPAC desert aerosol
                    inp.write('mc_vroom on \n') # switch on variance reduction for spiky phase functions
                elif case == 3:
                    inp.write('wc_file ../examples/WC.DAT \n')
                    inp.write('wc_properties mie \n')
                    inp.write('wc_properties_interpolate \n')
                    inp.write('wc_set_tau 2 \n') # cloud optical thickness 2
                    inp.write('mc_vroom on \n') # switch on variance reduction for spiky phase functions
                else:
                    pass

                inp.close()

                # can also use module subprocess.Popen() instead
                # child = subprocess.Popen('./uvspec < mystic_run.inp > test.out', shell=True)
                # child.wait()
                fin,fout = os.popen2('./uvspec < mystic_run.inp > test.out')
                os.wait()

                # wait Stokes vector and standard deviation into variables
                # I
                I[iumu,iphi,case] = np.loadtxt('mc.rad')[0,7]
                # Q
                Q[iumu,iphi,case] = np.loadtxt('mc.rad')[1,7]
                # U
                U[iumu,iphi,case] = np.loadtxt('mc.rad')[2,7]
                # V
                V[iumu,iphi,case] = np.loadtxt('mc.rad')[3,7]

    # save as mat file
    scipy.io.savemat('I.mat',{'I':I},oned_as='row')
    scipy.io.savemat('Q.mat',{'Q':Q},oned_as='row')
    scipy.io.savemat('U.mat',{'U':U},oned_as='row')
    scipy.io.savemat('V.mat',{'V':V},oned_as='row')

    # save as numpy file
    np.save('I.npy',I)
    np.save('Q.npy',Q)
    np.save('U.npy',U)
    np.save('V.npy',V)

    va.shape  = (va.shape[0],1)
    phi.shape = (phi.shape[0],1)

    # degree to radius
    phi = phi*pi/180.0

    # coordinate of x,y
    x = np.dot(np.sin(va),np.cos(phi.T))
    y = np.dot(np.sin(va),np.sin(phi.T))

    scipy.io.savemat('x.mat',{'x':x},oned_as='row')
    scipy.io.savemat('y.mat',{'y':y},oned_as='row')

    np.save('x.npy',x)
    np.save('y.npy',y)

else:
    # an example
    # load and draw the data
    I = np.load('I.npy')
    Q = np.load('Q.npy')
    U = np.load('U.npy')
    V = np.load('V.npy')

    x = np.load('x.npy')
    y = np.load('y.npy')

    # location of the sun
    phi0 = 3*pi/2 # azimuth angle (east)
    sza  = pi/3 # solar zenith angle

    xs = sin(sza)*cos(phi0)
    ys = sin(sza)*sin(phi0)

    ######################################################
    # for directly sphere mapping r=1
    # the equation for this sphere is
    # x^2 + y^2 = 1
    # the equation for (0,0) and (xs,ys) is
    # y = (ys/xs)*xs
    ######################################################

    # get the intersection points of the above equations
    meridian_x = np.zeros(2)
    meridian_y = np.zeros(2)

    meridian_x[0] = xs/(sqrt(xs**2 + ys**2))
    meridian_x[1] = - meridian_x[0]

    meridian_y[0] = ys/(sqrt(xs**2 + ys**2))
    meridian_y[1] = - meridian_y[0]

    # set the font
    font = {
            'family': 'Times New Roman',
            'size'  : 16
            }
    matplotlib.rc('font',**font)

    # Lambertian surface albedo of 0.2
    # ratio * I/Q/U/V
    ratio = 10**2
    I_exp = ratio*I[:,:,0]
    Q_exp = ratio*Q[:,:,0]
    U_exp = ratio*U[:,:,0]
    V_exp = ratio*V[:,:,0]

    # degree of polarization
    dop = np.sqrt(Q_exp**2 + U_exp**2)/I_exp
    # angle of polarization
    aop = 0.5*np.arctan2(U_exp,Q_exp)
    aop = np.rad2deg(aop)

    fig = plt.figure(num='distribution of I',facecolor='white')
    plt.clf()
    plt.pcolormesh(x,y,I_exp,shading='flat',cmap=cm.rainbow)
    plt.plot(meridian_x,meridian_y,'w-',xs,ys,'wo',linewidth=2,markersize=8)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('I.png')

    fig = plt.figure(num='distribution of Q',facecolor='white')
    plt.clf()
    plt.pcolormesh(x,y,Q_exp,shading='flat',cmap=cm.rainbow)
    plt.plot(meridian_x,meridian_y,'w-',xs,ys,'wo',linewidth=2,markersize=8)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('Q.png')

    fig = plt.figure(num='distribution of U',facecolor='white')
    plt.clf()
    plt.pcolormesh(x,y,U_exp,shading='flat',cmap=cm.rainbow)
    plt.plot(meridian_x,meridian_y,'w-',xs,ys,'wo',linewidth=2,markersize=8)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('U.png')

    fig = plt.figure(num='degree of polarizaiton',facecolor='white')
    plt.clf()
    plt.pcolormesh(x,y,dop,shading='flat',cmap=cm.jet)
    plt.plot(meridian_x,meridian_y,'w-',xs,ys,'wo',linewidth=2,markersize=8)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('dop.png')

    fig = plt.figure(num='angle of polarizaiton',facecolor='white')
    plt.clf()
    plt.pcolormesh(x,y,aop,shading='flat',cmap=cm.jet)
    plt.plot(meridian_x,meridian_y,'w-',xs,ys,'wo',linewidth=2,markersize=8)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('aop.png')

    plt.show()



