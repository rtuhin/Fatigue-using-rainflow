# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 12:31:53 2014

@author: trakshit
"""
#from pandas import
import sys
import numpy as np

def halfcycles(ts, cycles, amp):
    n = len(ts)
    for i in xrange(n):
        if (i<n-1):
            xp = ts[i]
            xp1 = ts[i+1]
            #cycles.append(1.0)
            # assume all half cycles become full over time
            cycles.append(0.5)
            amp.append(abs(xp-xp1))
            #print xp, xp1, 'form a half cycle with range', abs(xp-xp1)
    # the last 2 points form a half cycle
            
    
def fullcycles(ts, cycles, amp):
    
    fullCyclesExist = True
    
    while (fullCyclesExist):
        # no of cycles    
        k = 0
        n = len(ts)
        indices = []        
        for i in xrange(1,n-2):
            xp = ts[i]
            xp1 = ts[i+1]
            xp2 = ts[i+2]
            #print i, xp, xp1, xp2
            if (xp1>=xp):
                if (xp2<=xp):
                    xm1 = ts[i-1]
                    if (xp1<=xm1):
                        #print 'here 1', i, xp, xp1, xp2, xm1
                        #print xp, xp1, 'form a closed cycle with range', abs(xp1-xp)
                        amp.append(abs(xp1-xp))
                        cycles.append(1)
                        indices.append(i)
                        indices.append(i+1)
                        k += 1

            else:
                if (xp2>=xp):
                    xm1 = ts[i-1]
                    if (xp1>=xm1):
                        #print 'here 2', i, xp, xp1, xp2, xm1
                        #print xp, xp1, 'form a closed cycle with range', abs(xp1-xp)
                        amp.append(abs(xp1-xp))
                        cycles.append(1)
                        indices.append(i)
                        indices.append(i+1)
                        k += 1

        ts = np.delete(ts,indices)
    
        if (k==0): fullCyclesExist = False
    #print ts
    return ts
    
def extremes(ts):
    temp =  []
    nts = len(ts)
    #temp.append(ts[0])
    for i in xrange(nts-2):
        xp = ts[i]
        xp1 = ts[i+1]
        xp2 = ts[i+2]
        if (xp==xp1):  xp1=1.000001*xp1
        if (xp2==xp1): xp1 = 1.000001*xp1
        slp1 = xp1-xp
        slp2 = xp2-xp1
        if (slp1*slp2<0):
            #print i+1,slp1*slp2
            temp.append(xp1)
            #print xp1
    #temp.append(ts[-1])
    return temp

#######################################################
#
#  Main program
#
#######################################################

if __name__ == "__main__":
    
    #inpFileName = sys.argv[1]
    SECONDS_IN_A_YEAR = 365.0*24.0*60.0*60.0
    scf = 1.0
    sref = 9.546
    nref = 1.0E6        
    slope = 3.0
    inpFileName = 'N73.dat'
    
    cycles = []
    amp = []
    dmg = 0.0


    #print inpFileName
    #inpFileName = 'pygen_e.inp'
    #
    time = []
    tst = []
    
    try:
        inpFile = open(inpFileName, "rb")
    except (IOError), e:
        print "Unable to open file", inpFileName,". Ending program.\n", e
        #raw_input("\n\nPress any key to exit.")
        sys.exit()
    
    inplines = inpFile.readlines()

    inpFile.close()
    
    for line in inplines:
        linedata = line.split();
        time.append(float(linedata[0]))
        tst.append(float(linedata[1]))
    
    print 'time[0]', time[0]
    print 'time[-1]', time[-1]
    print 'stress[0]', tst[0]
    print 'stress[-1]', tst[-1]


#    #s = 'Length of time series: %d, %0.2f, %d\n' % (elements[i], ang, len(tst))
#    #dbgfile.write(s)
#    s = ('%d, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f\n') % (elements[i], ang, np.average(tst), np.max(tst), np.min(tst), np.sqrt(np.mean(np.power(tst,2))))
#    #sumFile.write(s)
#    #print elements[i], ang.strip(), len(tst)
#    # get the extremes of the time history
    ext_tst = extremes(tst)
    n_ext = len(ext_tst)
    only_halves = fullcycles(ext_tst, cycles, amp)
    nfull = len(cycles)
#            
    halfcycles(only_halves, cycles, amp)
    nhalf = len(cycles) - nfull
#    s = ('%d, %0.2f, Extremes: %d, Full cycles: %0.2f, Half cycles: %0.2f\n') % (elements[i], ang, n_ext, nfull, nhalf)
#    outFile.write(s)
    scfAmp = np.multiply(scf, amp)
#    #scfAmp = amp
    nreftemp = np.power(np.divide(sref,scfAmp), slope)*nref
    dmgvector = np.divide(cycles,nreftemp)
#    # Annual Damage
    dmg = np.sum(dmgvector)*SECONDS_IN_A_YEAR/(time[-1]-time[0])
    print 'Annual Damage: ', dmg
    
    print 'Done!'
#        