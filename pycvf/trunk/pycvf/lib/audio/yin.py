import math
import numpy


def interp_min(y,min_idx):
    """get a minimum value by parabolically interpolating three points"""
    #print y,min_idx
    Ai = numpy.matrix([ [ 0.5, -1, 0.5],[ -0.5 ,0 ,0.5],[ 0 ,1, 0]])
    #a_ = numpy.matrix([0.5, -1 ,0.5])
    #b_ = numpy.matrix([-0.5, 0, 0.5])
    y=numpy.matrix(y)
    a = Ai[0,:]*y.T
    b = Ai[1,:]*y.T
    c = Ai[2,:]*y.T
    x0 = -b/(2*a)
    y0 = a*pow(x0,2)+b*x0+c
    x0 = min_idx + x0
    return x0,y0

def find_f0_yin(x,f0_min = 60,f0_max = 2000,threshold = 0.1, tau_min_local = 0.8, tau_max_local = 1.2, r_local = 16):
    """
    FIND_F0_YIN  Find fundamental frequency using the YIN method

    F0 = FIND_F0_YIN(X)

    Find the fundamental frequency of signal X using the
    YIN method developed by de Cheveigne and Kawahara.

    tau_min_local = 0.8;  # search range for the local estimate
    tau_max_local = 1.2;  # search range for the local estimate
    r_local = 16;  # local context radius

    """
    # range limits for f0
    tau_min = int(math.floor(len(x)/f0_max))
    tau_max = int(math.ceil(len(x)/f0_min))

    # integration window size
    W = len(x)-tau_max;
    if W < 1:
        f0 = 0;
        raise Exception,'F0-YIN: Too short window'

    # initialization
    #
    dn_array = numpy.zeros((r_local, tau_max))
    #
    # initial energy
    E = pow(x,2).sum();

    #
    #Step 2: Difference function
    #
    # calculate the difference function
    #print "2"
    d = numpy.zeros(tau_max);
    for tau in range(tau_max):
        d[tau] = sum(pow((x[:W] - x[tau:W+tau]),2));

    #
    #
    # Step 3: Cumulative mean normalized difference function
    #print "3"
    dn = d/d.cumsum()/(numpy.arange(tau_max)+1);
    #
    # Step 4: Absolute threshold
    #
    # find the minima below the threshold
    #print "4"
    diff_dn = numpy.diff(dn)
    diff1 = diff_dn[tau_min-1:-1]
    diff2 = diff_dn[tau_min:]
    dn_range = dn[tau_min:-1]
    minima = map(lambda x,y,z: (x <= 0) and (y > 0) and (z <= threshold), diff1.flat, diff2.flat, dn_range.flat)
    #
    # get the first such minimum
    #
    #print "5"
    try:
        idx = minima.index(True) # argmax(minima);
        val=minima[idx]
    except:
        val=None
    # if not found, use the global minimum instead
    if val==None or (val==0):
        min_val, min_idx = min(dn_range);
        min_idx = min_idx + tau_min - 1;
    else:
        min_idx = idx + tau_min - 1;
        min_val = dn[min_idx]

    #
    #Step 5: Parabolic interpolation
    #
    min_idx_interp,min_val_interp = interp_min(dn[(min_idx-1):(min_idx+2)],min_idx);
    #
    # Step 6: Best local estimate not practical for short frames, so omitted
    #
    # final result:
    f0 = len(x)/min_idx_interp;
    return f0
