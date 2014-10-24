from pylab import *
from math import *
import numpy as np
import scipy.io
import os
import sys

# Define input parameters

# case 0: sza 80, phi0 250
# case 1: sza 55, phi0 264
# case 2: sza 30, phi0 280
# case 3: sza 10, phi0 347
# case 4: sza 26, phi0 76
# case 5: sza 52, phi0 95
# case 6: sza 76, phi0 108

ncases = 3
cases = [0,1,2] #350nm,400nm,500nm

# viewing angle
va = np.linspace(0.0,pi/2,50,endpoint=True)
umu = - np.cos(va)

# azimuth angles
phi = np.linspace(0.0,360.0,180,endpoint=True)

# solar zenith angle
# sza = [80.,55.,30.,10.,26.,52.,76.]

# solar azimuth angle
# phi0 = [250.,264.,280.,347.,76.,95.,108.]

# wavelengths
lam = [350.,400.,500.]

# number of Stokescomponents
# nstokes = 4

# number of photons
# N = 1e5

# Initialize variables for radiance and standard deviation
I = np.zeros((len(va),len(phi),ncases))
Q = np.zeros((len(va),len(phi),ncases))
U = np.zeros((len(va),len(phi),ncases))
# V = np.zeros((len(va),len(phi),ncases))

x = np.zeros((len(va),len(phi)))
y = np.zeros((len(va),len(phi)))

# radiance = zeros((len(va), len(sza), len(phi), len(lam), nstokes, ncases))
# std = zeros((len(va), len(sza), len(phi), len(lam), nstokes, ncases))

# path to uvspec executable
# path = '../'

# run rt calculation
# run_rt = False
run_rt = True

if(run_rt):
	for case in cases:
		for iphi in range(len(phi)):
			for iumu in range(len(umu)):
				
				disp('run mystic: case %g phi %g umu %g'%(case,phi[iphi],va[iumu]*180.0/pi))
				tmp = open('mystic.inp').read()
				inp = open('mystic_run.inp','w')
				inp.write(tmp)
				inp.write('\n')
				inp.write('umu %g \n'%umu[iumu])
				inp.write('phi %g \n'%phi[iphi])

				# inp.write('albedo 0.2 \n') # Lambertian surface albedo of 0.2
				if case == 0:
					inp.write('wavelength %g \n'%lam[case])
				elif case == 1:
					inp.write('wavelength %g \n'%lam[case])
				elif case == 2:
					inp.write('wavelength %g \n'%lam[case])
				else:
					pass
				# if case == 0:
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# elif case == 1:
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# elif case == 2:
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# elif case == 3:   
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# elif case == 4:
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# elif case == 5:
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# elif case == 6:
				# 	inp.write('sza %g \n'%sza[case])
				# 	inp.write('phi0 %g \n'%phi0[case])
				# else:
				# 	pass

				inp.close()

				fin, fout = os.popen2('./uvspec < mystic_run.inp > test.out')

				os.wait()

				# wait Stokes vector and standard deviation into variables
				# I
				I[iumu,iphi,case] = loadtxt('mc.rad')[0,7]
				# Q
				Q[iumu,iphi,case] = loadtxt('mc.rad')[1,7]
				# U
				U[iumu,iphi,case] = loadtxt('mc.rad')[2,7]
				# V 
				# V[iumu,iphi,case] = loadtxt('mc.rad')[3,7]

	# save as mat file
	scipy.io.savemat('I.mat',{'I': I},oned_as='row')
	scipy.io.savemat('Q.mat',{'Q': Q},oned_as='row')
	scipy.io.savemat('U.mat',{'U': U},oned_as='row')

	np.save('I.npy',I)
	np.save('Q.npy',Q)
	np.save('U.npy',U)

	va.shape = (va.shape[0],1)
	phi.shape = (phi.shape[0],1)

	# degree to radius
	phi = phi*pi/180.0

	# coordinate of x, y
	x = np.dot(np.sin(va),np.cos(phi.T))
	y = np.dot(np.sin(va),np.sin(phi.T))

	# scipy.io.savemat('x.mat',{'x': x},oned_as='row')
	# scipy.io.savemat('y.mat',{'y': y},oned_as='row')

	np.save('x.npy',x)
	np.save('y.npy',y)

else:

	I = np.load('I.npy')
	Q = np.load('Q.npy')
	U = np.load('U.npy')

	x = np.load('x.npy')
	y = np.load('y.npy')
