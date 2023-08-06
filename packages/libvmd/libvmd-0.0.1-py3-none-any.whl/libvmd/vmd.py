# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:48:53 2022

LIBVMD: Python library for variational mode decomposition for both 1D and 2D

This code is originated from the MatLab code for vmd

Translated by Hyoseob Noh

See details in the definitions

"""

import numpy as np


def vmd(signal, alpha, K = 5, tau = 0.01, DC=True, init=1, tol=10**-6, N = 500):
    """
        -----------------------------------------------
    Original MATLAB code of D. Zosso was translated by Hyoseob Noh
    
    Dragomiretskiy, K., & Zosso, D. (2013). Variational mode decomposition. 
    IEEE transactions on signal processing, 62(3), 531-544.
    please check here for update reference: 
              http://dx.doi.org/10.1109/TSP.2013.2288675
              
    Dominique Zosso (2022). Variational Mode Decomposition 
    (https://www.mathworks.com/matlabcentral/fileexchange/44765-variational-mode-decomposition),
    MATLAB Central File Exchange. 
        -----------------------------------------------
    Unlike vmd2, mirror_extension option is default
        "mirror_extension: mirror padding of the input signal to reduce the boundary effect of FFT"
        
        
    signal: Input 2-D 
        
    alpha: Penalty factor
    
    tau: Lagrangian multiplier
    
    K: The number of modes
    
    DC: DC signal manipulation
        0: No manipulation
        1: Make the first mode's frequency zero
    
    init: center frequency initialization method
        0: Grid
        1: Random
        
    tol: Convergence tolerence

    N: Maximum iterations
        
    """


    # One dimensional original vmd
    
    # Period and sampling frequency of input signal
    save_T = len(signal)
    fs = 1/save_T
    
    # extend the signal by mirroring
    T = save_T
    
    halfT = int(T/2)
    
    f_mirror = np.zeros(T*2)
    
    f_mirror[:halfT] = signal[:halfT][::-1]
    f_mirror[halfT:(halfT+T)] = signal
    f_mirror[(halfT+T):] = signal[halfT:][::-1]
    f = f_mirror.copy()
    
    # Time Domain 0 to T (of mirrored signal)
    T = len(f)
    halfT = int(T/2)
    
    t = np.arange(1,T+1)/T
    
    # Spectral domain discretization
    freqs = t - 0.5 - 1/T
    
    # Maximum number of iterations (if not converged yet, then it won't anyway)
#    N = 500
    
    # For future generalizations: individual alpha for each mode
    Alpha = alpha*np.ones((1,K))
    
    f_hat = np.fft.fftshift(np.fft.fft(f))
    f_hat_plus = f_hat.copy()
    f_hat_plus[:halfT] = 0
    
    # matrix keeping track of every iterant // could be discarded for mem
    u_hat_plus = np.zeros((N, len(freqs), K),dtype = 'complex_')
    
    # Initialization of omega_k
    omega_plus = np.zeros((N, K))
    
    if init == 1:
        for i in range(K):
            omega_plus[0,i] = (0.5/K) * (i)
    
    elif init == 2:
        omega_plus[0,:] = np.sort(np.exp(np.log(fs) + (np.log(0.5)-np.log(fs))*np.random.rand(1,K)))
        
    else:
        omega_plus[0,:] = 0
        
    # if DC mode imposed, set its omega to 0
    if DC:
        omega_plus[0,0] = 0

    
    
    # start with empty dual variables
    lambda_hat = np.zeros((N, len(freqs)),dtype = 'complex_')
    
    # other init
    eps = np.spacing(1)
    uDiff = tol+eps # update step
    n = 0 # loop counter
    sum_uk = 0 # accumulator
    
    
    # =============================================================
    # Main loop for update
    
#    for jj in range(1):
    while (uDiff > tol) & (n < N-1):
        k = 0
        sum_uk = u_hat_plus[n,:,K-1] + sum_uk - u_hat_plus[n,:,0]
        
        # update spectrum of first mode through Wiener filter of residuals
        u_hat_plus[n+1,:,k] = (f_hat_plus - sum_uk - lambda_hat[n,:]/2)/(1+Alpha[0,k]*(freqs - omega_plus[n,k])**2)
        
        # update first omega if not held at 0
        if not DC:
#            omega_plus[n+1,k] = (np.matmul(freqs[halfT:T],(np.abs(u_hat_plus[n+1, halfT:T, k])**2).transpose()))/np.sum(np.abs(u_hat_plus[n+1,halfT:T,k])**2)
            omega_plus[n+1,k] = (np.vdot(freqs[halfT:T],(np.abs(u_hat_plus[n+1, halfT:T, k])**2)))/np.sum(np.abs(u_hat_plus[n+1,halfT:T,k])**2)
        
        for k in range(1,K):
            # accumulator
            sum_uk = u_hat_plus[n+1,:,k-1] + sum_uk - u_hat_plus[n,:,k];
            
            # mode spectrum
            u_hat_plus[n+1,:,k] = (f_hat_plus - sum_uk - lambda_hat[n,:]/2)/(1+Alpha[0,k]*(freqs - omega_plus[n,k])**2);
            
            # center frequencies
            omega_plus[n+1,k] = (np.matmul(freqs[halfT:T],(np.abs(u_hat_plus[n+1, halfT:T, k])**2).transpose()))/np.sum(np.abs(u_hat_plus[n+1,halfT:T,k])**2)
#            print( u_hat_plus[n+1,-1,k] )
        # Dual ascent
        lambda_hat[n+1,:] = lambda_hat[n,:] + tau*(np.sum(u_hat_plus[n+1,:,:],1) - f_hat_plus)
        
        # loop counter
        n = n+1;

        # converged yet?
        uDiff = eps;
        for i in range(K):
#            uDiff = uDiff + 1/T*(u_hat_plus[n,:,i]-u_hat_plus[n-1,:,i]).reshape(1,-1)@np.conj((u_hat_plus[n,:,i]-u_hat_plus[n-1,:,i])).reshape(-1,1)
            uDiff = uDiff + 1/T*np.vdot((u_hat_plus[n,:,i]-u_hat_plus[n-1,:,i]).conj(),(u_hat_plus[n,:,i]-u_hat_plus[n-1,:,i]))

        uDiff = np.abs(uDiff);
        
        
        
    # =============================================================
    # Post processing and clean up
    
    # discard empty space if converged early
    N = np.min([N,n])
    omega = omega_plus[:N+1,:]
    
    # Signal reconstruction
    u_hat = np.zeros((T, K),dtype = 'complex_')
    u_hat[halfT:T,:] = u_hat_plus[N,halfT:T,:]
    u_hat[halfT::-1,:][:-1] = np.conj(u_hat_plus[N,halfT:T,:])
    u_hat[0,:] = np.conj(u_hat[-1,:])

    u = np.zeros((K,len(t)),dtype = 'complex_')
                            
    for k in range(K):
        u[k,:]=np.real(np.fft.ifft(np.fft.ifftshift(u_hat[:,k])))

#    print(N)
    # remove mirror part
    u = u[:,int(T/4):3*int(T/4)]

    u_hat = np.zeros((halfT, K),dtype = 'complex_')
    for k in range(K):
        u_hat[:,k]=np.fft.fftshift(np.fft.fft(u[k,:])).transpose()

    return u, u_hat, omega


def vmd2(signal, alpha, K = 5, tau = 0.01,  DC=1, init=1, tol=10**-6, N = 3000, history_return = False, mirror_extension = False):
    """
        -----------------------------------------------
        -----------------------------------------------
    Original MATLAB code of D. Zosso was translated by Hyoseob Noh
    
    Dragomiretskiy, K., & Zosso, D. (2013). Variational mode decomposition. 
    IEEE transactions on signal processing, 62(3), 531-544.
    please check here for update reference: 
              http://dx.doi.org/10.1109/TSP.2013.2288675
              
    Dragomiretskiy, K., Zosso, D. (2015). Two-Dimensional Variational Mode Decomposition. 
    In: Tai, XC., Bae, E., Chan, T.F., Lysaker, M. (eds) 
    Energy Minimization Methods in Computer Vision and Pattern Recognition. EMMCVPR 2015. 
    Lecture Notes in Computer Science, vol 8932. Springer, Cham. 
            https://doi.org/10.1007/978-3-319-14612-6_15
            
    Dominique Zosso (2022). Two-dimensional Variational Mode Decomposition 
    (https://www.mathworks.com/matlabcentral/fileexchange/45918-two-dimensional-variational-mode-decomposition), 
    MATLAB Central File Exchange.
        -----------------------------------------------
        
    ----------
    Parameters
    ----------

    signal: Input 2-D 
        
    alpha: Penalty factor
    
    tau: Lagrangian multiplier
    
    K: The number of modes
    
    DC: DC signal manipulation
        0: No manipulation
        1: Make the first mode's frequency zero
    
    init: center frequency initialization method
        0: Grid
        1: Random
        
    tol: Convergence tolerence

    N: Maximum iterations
    
    history_return: Returning center frequency update history
    
    mirror_extension: mirror padding of the input signal to reduce the boundary effect of FFT
    """
    
    if mirror_extension:
        Hy0,Hx0 = signal.shape
        mirrored =np.lib.pad(signal,((0,Hy0),(0,Hy0)),'reflect')
#        mirrored =np.lib.pad(signal,((0,Hy0),(0,Hy0)))
        signal = np.roll(mirrored,(int(Hx0/2),int(Hy0/2)),axis=(0,1))
    
    # Resolution of image
    Hy,Hx = signal.shape
    X,Y = np.meshgrid(np.arange(1,Hx+1)/Hx, np.arange(1,Hy+1)/Hy)
        
    
    # Spectral Domain discretization
    fx = 1/Hx
    fy = 1/Hy
    freqs_1 = X - 0.5 - fx
    freqs_2 = Y - 0.5 - fy
    
    # For future generalizations: alpha might be individual for each mode
    Alpha = alpha* np.ones((K,1))
    
    # Construct f and f_hat
    f_hat = np.fft.fftshift(np.fft.fft2(signal))
    
    # Storage matrices for (Fourier) modes. All iterations are not recorded.
    u_hat = np.zeros((Hy,Hx,K),dtype = 'complex_')
    u_hat_old = u_hat.copy()
    sum_uk = 0


    # Storage matrices for (Fourier) Lagrange multiplier.
    mu_hat = np.zeros((Hy,Hx),dtype = 'complex_')
    
    # N iterations at most, 2 spatial coordinates, K clusters
    omega = np.zeros((N, 2, K))

    if init == 0:
        # spread omegas radially
         # if DC, keep first mode at 0,0
        if DC==1:
            maxK = K-1
        else:
            maxK = K
        
        for k in range( DC,DC + maxK) :
            omega[0,0,k] = 0.25*np.cos(np.pi*(k)/maxK)
            omega[0,1,k] = 0.25*np.sin(np.pi*(k)/maxK)

    elif init == 1:
        for k in range(K):
            omega[0,0,k] = np.random.rand()-1/2
            omega[0,1,k] = np.random.rand()/2
                
        # DC component (if expected)
        if DC == 1:
            omega[0,0,0] = 0
            omega[0,1,0] = 0
        
    
    eps = np.spacing(1)
    uDiff = tol+eps # update step
    omegaDiff = tol+eps
    n = 0

    while ((uDiff > tol) | (omegaDiff>tol)) & (n < N-1):

        # first things first
        k = 0
        
        # compute the halfplane mask for the 2D "analytic signal"
        HilbertMask = (np.sign(freqs_1*omega[n,0,k] + freqs_2*omega[n,1,k])+1)

        # update first mode accumulator
        sum_uk = u_hat[:,:,-1] + sum_uk - u_hat[:,:,k]

        # update first mode's spectrum through wiener filter (on half plane)
        u_hat[:,:,k] = ((f_hat - sum_uk - mu_hat[:,:]/2)*HilbertMask)/(1+Alpha[k]*((freqs_1 - omega[n,0,k])**2+(freqs_2 - omega[n,1,k])**2))

        if DC == 0:
            # omega[n+1,0,k] = np.sum(freqs_1*(np.abs(u_hat[:,:,k])**2))/np.sum(np.abs(u_hat[:,:,k])**2)
            # omega[n+1,1,k] = np.sum(freqs_2*(np.abs(u_hat[:,:,k])**2))/np.sum(np.abs(u_hat[:,:,k])**2)
            u_hat_sqabs = np.abs(u_hat[:,:,k])**2
            # omega[n+1,0,k] = np.sum(freqs_1*(u_hat_sqabs))/np.sum(u_hat_sqabs)
            # omega[n+1,1,k] = np.sum(freqs_2*(u_hat_sqabs))/np.sum(u_hat_sqabs)
            
            omega[n+1,0,k] = (freqs_1*(u_hat_sqabs)).sum()/u_hat_sqabs.sum()
            omega[n+1,1,k] = (freqs_2*(u_hat_sqabs)).sum()/u_hat_sqabs.sum()
        
        # keep omegas on same halfplane
            if omega[n+1,1,k] < 0:
                omega[n+1,:,k] = -omega[n+1,:,k]
           
       # recover full spectrum from analytic signal
        u_hat[:,:,k] = np.fft.fftshift(np.fft.fft2(np.real(np.fft.ifft2(np.fft.ifftshift(u_hat[:,:,k])))))

        # work on other modes
        for k in range(1,K):
            
            # recompute Hilbert mask
            HilbertMask = (np.sign(freqs_1*omega[n,0,k] + freqs_2*omega[n,1,k])+1)
            # update accumulator
            sum_uk = u_hat[:,:,k-1] + sum_uk - u_hat[:,:,k]
            
            # update signal spectrum
            u_hat[:,:,k] = ((f_hat - sum_uk - mu_hat[:,:]/2)*HilbertMask)/(1+Alpha[k]*((freqs_1 - omega[n,0,k])**2+(freqs_2 - omega[n,1,k])**2))
            
            # update signal frequencies
            # omega[n+1,0,k] = np.sum(freqs_1*(np.abs(u_hat[:,:,k])**2))/np.sum(np.sum(np.abs(u_hat[:,:,k])**2))
            # omega[n+1,1,k] = np.sum(freqs_2*(np.abs(u_hat[:,:,k])**2))/np.sum(np.sum(np.abs(u_hat[:,:,k])**2))
            u_hat_sqabs = np.abs(u_hat[:,:,k])**2
            # omega[n+1,0,k] = np.sum(freqs_1*(u_hat_sqabs))/np.sum(u_hat_sqabs)
            # omega[n+1,1,k] = np.sum(freqs_2*(u_hat_sqabs))/np.sum(u_hat_sqabs)
            
            omega[n+1,0,k] = (freqs_1*(u_hat_sqabs)).sum()/u_hat_sqabs.sum()
            omega[n+1,1,k] = (freqs_2*(u_hat_sqabs)).sum()/u_hat_sqabs.sum()
            
            # keep omegas on same halfplane
            if omega[n+1,1,k] < 0:
                omega[n+1,:,k] = -omega[n+1,:,k]
         
            
            # recover full spectrum from analytic signal
            u_hat[:,:,k] = np.fft.fftshift(np.fft.fft2(np.real(np.fft.ifft2(np.fft.ifftshift(u_hat[:,:,k])))))

        # Gradient ascent for augmented Lagrangian
        mu_hat[:,:] = mu_hat[:,:] + tau*(np.sum(u_hat,2) - f_hat)
        
        # increment iteration counter
        n = n+1;
        
        # convergence?
        uDiff = eps;
        omegaDiff = eps;
        
        for k in range(K):
            omegaDiff = omegaDiff + np.sum(np.abs(omega[n,:,:] - omega[n-1,:,:])**2)
            uDiff = uDiff + (1/(Hx*Hy)*(u_hat[:,:,k]-u_hat_old[:,:,k])*((u_hat[:,:,k]-u_hat_old[:,:,k])).conj()).sum()
        
        
        uDiff = np.abs(uDiff)
        u_hat_old[:,:,:] = u_hat[:,:,:]
        
    # Signal Reconstruction
    # Inverse Fourier Transform to compute (spatial) modes

    
    if mirror_extension:
        u = np.zeros((Hy0,Hx0,K))

        for k in range(K):
            ut = np.roll( np.real(np.fft.ifft2(np.fft.ifftshift(u_hat[:,:,k]))) ,(-int(Hy0/2),-int(Hx0/2)),axis=(0,1))
            u[:,:,k] = ut[:Hy0,:Hx0]
            
        if history_return:
            omega = omega[:n,:,:]
        
        else:
            omega = omega[n,:,:]
    else:
        u = np.zeros((Hy,Hx,K))
        for k in range(K):
            u[:,:,k] = np.real(np.fft.ifft2(np.fft.ifftshift(u_hat[:,:,k])))
            
        if history_return:
            omega = omega[:n,:,:]
        
        else:
            omega = omega[n,:,:]


    return u, u_hat, omega

