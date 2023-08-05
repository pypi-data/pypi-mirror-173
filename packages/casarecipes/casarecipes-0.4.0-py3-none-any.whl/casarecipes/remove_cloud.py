"""

Fit a constant tau component to the 4 ALMA WVR channels, 
then remove this from the 4 temperature measurements tsrc(0-3)

Based on rem_cloud.py by B. Dent version 12 Aug 2015, see ALMA CSV-3189


v2 was  Updated 18 Oct 2021. to improve processing of antennas with WVR calibration isses on single channels, eg DA64
    Also may run faster than previous, as the loops have been optmised
    Fix occasional instability in solution causing extra noise
v2.1 updated 13 Dec 2021. minor alterations (print statements, call to radians and log10 functions) to make compatible with Python 3
"""

import numpy as np
import pylab as pl
from matplotlib import pyplot
import scipy.optimize as opt
import os
import math
import time
import datetime
from casatasks import casalog
from casatools import ms as mstool
from casatools import table as tbtool

def rmc_func1(x,a,b,c):    
    return a*(x-b)**2+c

def rmc_weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weigts -- Numpy ndarrays with the same shape.
    """
    if sum(weights) > 0.0:
        average = np.average(values, weights=weights)
        variance = abs(np.average((values-average)**2, weights=weights))
    else:
        average = np.average(values)
        variance = abs(np.average((values-average)**2))
    return (average, math.sqrt(variance))

def nanmedian(f):
    fa = np.array(f)
    fan = fa[~np.isnan(fa)]
    return np.median(fan)

def nanstd(f):
    fa = np.array(f)
    fan = fa[~np.isnan(fa)]
    return np.std(fan)

def rmc_approxCalc(tsrc0, tsrc1, tsrc2, tsrc3,
                   m_el, Tamb, do_cal_offset, isam, verb):    
    m_el=math.radians(m_el)   # convert to radians
    mean_pwt=0.0; raw_mean_pwt=0.0

    if do_cal_offset:
        tau_offset = 0.1
    else:
        tau_offset = 0.0

    # correct for coupling to the sky, assuming T_loss=275K, eta_c=0.98
    eta_c=0.98
    T_loss=275.0

    tsrc0=(tsrc0-(1.0-eta_c)*T_loss)/eta_c
    tsrc1=(tsrc1-(1.0-eta_c)*T_loss)/eta_c
    tsrc2=(tsrc2-(1.0-eta_c)*T_loss)/eta_c
    tsrc3=(tsrc3-(1.0-eta_c)*T_loss)/eta_c

    #    m_az, m_el, m_ts= mc.actualAzEl()

    pw=[0.0,0.0,0.0,0.0];     pw_noc=[0.0,0.0,0.0,0.0]
    site="AOS"
    
    # set up fitting constants depending on the site:
    if site == "OSF":   # constants:
       tau0=[0.024,0.02,0.009,0.01]
       r=[1.205,0.402,0.177,0.116]
       # approximate physical temp of atmosphere:
       Tphys=267.0

    elif site == "AOS":  # constants:
       tau0=[0.027,0.02,0.010,0.01]
       r=[1.193,0.399,0.176,0.115]
       # approximate physical temp of atmosphere ,based on ambient temperature, Tamb, in centrigrade:
       Tphys=270.0 +Tamb

#       if Tphys<tsrc0 and tsrc0 < 300.0:
#           Tphys=tsrc0+1.0
#           if verb:
#               casalog.post('  fixed physical temperature to be tsrc0', 'INFO')

    tsrcn=np.zeros(4)
    teln=np.zeros(4)

    tel=[0.0,0.0,0.0,0.0]
    tz=[0.0,0.0,0.0,0.0]
    wt=[0.0,0.0,0.0,0.0]

    # calculate transmissions:
    tel[3]=(1.0-tsrc3/Tphys)
    tel[2]=(1.0-tsrc2/Tphys)
    tel[1]=(1.0-tsrc1/Tphys)
    tel[0]=(1.0-tsrc0/Tphys)

    if tsrc3 < 300.0:     # if greater, then probably on hot load, so dont set weights
      if verb:
          print('tsrc',tsrc0,tsrc1,tsrc2,tsrc3,'etatel',tel)
      for i in range(4):
            if tel[i]<0.0:
                tel[i]=1e-10
            wt[i] = (1.0-(abs(tel[i]-0.5)/0.50)**2.0)    # weights

            if wt[i] <0.:
                if verb: 
                    casalog.post( 'Found negative weight: '+str(wt), 'WARN')
                    casalog.post( '            tsrc 0-3:    '+str(tsrc0)+', '+str(tsrc1)+', '+str(tsrc2)+', '+str(tsrc3), 'WARN')
                    wt[i] = 0.
                    casalog.post( 'Setting it to zero: weights 0-3: '+str(wt), 'WARN')



      if verb:
        casalog.post( '  weights 0-3: '+str(wt), 'INFO')
        casalog.post( '  tsrc 0-3:    '+str(tsrc0)+', '+str(tsrc1)+', '+str(tsrc2)+', '+str(tsrc3), 'INFO')

      for i in range(4):
        pw[i]=-(pl.log(tel[i])+tau0[i])/r[i]

      rat31_1=pw[3]/pw[1]
      pwm=np.mean(pw)

      if pwm>5.0: wt[0]=0.0

      if pwm>0.5:   # only look for a wet cloud component if pwv>0.5mm (bit arbitrary cutof but probably ok)
        pwt=np.zeros(4)

        # now set increment factor for tauc depending on dekta T
        dt=pw[3]-pw[2]

        std_pwt_r=np.zeros(5)
        # find std for tauc=0.0000
        for i1 in range(4):
                pwt[i1]=-(pl.log(tel[i1])+tau0[i1])/r[i1]

        mean_pwt,std_pwt_0=rmc_weighted_avg_and_std(pwt, wt)   # get std of 4 v

        #  tauc_r is the maximum tau_continuum value to be used in the array for fitting
        tauc_r = 0.5
    
        # now create an array of tau's, up to tauc_r 
        narr = 50
        tau_arr=np.zeros(narr)
        std_arr=np.zeros(narr)
        fact = 10**(math.log10(1.0 + tauc_r) / float(narr))

        for it in range(narr):
            tau_arr[it] = fact**float(it) - 1.0 - tau_offset
            for i1 in range(4):
                pwt[i1]=-((pl.log(tel[i1])+tau0[i1])+tau_arr[it])/r[i1]
                if pwt[i1]<0.0:
                    iloop=False
            mean_pwt,std_arr[it]=rmc_weighted_avg_and_std(pwt, wt)

        # we now have the tau array. need to find std's and do a fit.
        # first check that 0'th element is not the smallest;
        # if it is, then no need to fit
        if std_arr[0]>(np.mean(std_arr[1:2])):
            # now find the minimum:
            mm=min(std_arr)
#            nmin=[ii for ii,jj in enumerate(std_arr) if jj==mm][0]
            nmin = np.argmin(std_arr)
            a2=tau_arr[nmin]
#            print '1st estimate',a2,nmin,'std:',std_arr[nmin-1],std_arr[nmin],std_arr[nmin+1]
            if verb:
                casalog.post('  First guess tauc, nmin: '+str(a2)+', '+str(nmin), 'INFO')
            a2_0 = a2

            # now do a fit to +-20 linear values around this point
            tau_arr_subset=[]; std_arr_subset=[]
            tau_lin_step = (tau_arr[nmin] - tau_arr[nmin-1]) / 30.0
            for isubset in range(-40,40):
                this_tau = tau_arr[nmin] + float(isubset)*tau_lin_step
                if this_tau > -tau_offset:
                    tau_arr_subset.append(this_tau)
                    for i1 in range(4):
                        pwt[i1]=-((pl.log(tel[i1])+tau0[i1])+this_tau)/r[i1]
                    if pwt[i1]<0.0:
                        iloop=False
                    this_mean_pwt,this_std=rmc_weighted_avg_and_std(pwt, wt)
                    std_arr_subset.append(this_std)
                
       # first estimate used for fitting
            for i1 in range(4):
                pwt[i1]=-((pl.log(tel[i1])+tau0[i1])+tau_arr[nmin])/r[i1]
            this_min_pwt,this_min_std=rmc_weighted_avg_and_std(pwt, wt)
            x0=np.array( [1.0,tau_arr[nmin],this_min_std])    # first guess
            if this_min_std < 1.0:
                try: 
                    a1,a2,a3=opt.curve_fit(rmc_func1,tau_arr_subset,std_arr_subset,x0)[0]
                except:
                    a2=tau_arr[nmin]
                    casalog.post('  Fitting failed, using approximation ' + str(tau_arr[nmin]), 'INFO')
                
            else:
                a2= np.nan #  tau_arr[nmin]
                casalog.post('  High discrepancy between WVR channels, setting tauc to ' + str(a2), 'INFO')

#            pwt_0 = np.zeros(4)
#            for i11 in range(4):
#                pwt_0[i11]=-((pl.log(tel[i11])+tau0[i11]))/r[i11]
#            print isam,pwt,pwt_0,this_min_std,a2,a2_0

            if verb:
                casalog.post('  Final fitted tauc: '+str(a2), 'INFO')

            tau_constant=a2
        else:
            tau_constant=0.0
            
        # re-estimate pwv, after removing additional tau_constant component.
        # (could add extra factor 1/(1-tau) in measured line abs. 
        # because it's absorbed by the continuum atmopheric abs ... 
        # although maybe not
        # if they are colocated - this needs some radiative transfer...)

        for i in range(4):
           pw_noc[i]=(-(pl.log(tel[i])+tau0[i]+tau_constant)/r[i])  # *(1./(1-tau_constant))

        # reverse-calculate the effective tsrcn(0-3) based on the new pwvs:
        for i in range(4):
            teln[i]=math.exp(-(pw_noc[i]*r[i]+tau0[i]))
            tsrcn[i]=Tphys*(1.0-teln[i])
            if np.isnan(tsrcn[i]) : tsrcn[i] = 0.0     # replace nan with 0.0

        if verb:
            casalog.post('  isam      : '+str(isam), 'INFO')
            casalog.post('  pw 0-3    : '+str(pw), 'INFO')
            casalog.post('  pw_noc 0-3: '+str(pw_noc), 'INFO')
            casalog.post('  tsrc 0-3  : '+str(tsrc0)+', '+str(tsrc1)+', '+str(tsrc2)+', '+str(tsrc3), 'INFO')
            casalog.post('  tsrcn 0-3 : '+str(tsrcn[0])+', '+str(tsrcn[1])+', '+str(tsrcn[2])+', '+str(tsrcn[3]), 'INFO')
 
        #  estimate weighted mean pwv, with and without cloud component:
        # first estimate
        ws=0.0
        for i in range(4):
            ws=ws+pw[i]*wt[i]
        pwv_los=ws/np.sum(wt)
        pwv_z=pwv_los*math.sin(m_el)

        # now remove moisture component
        ws=0.0
        for i in range(4):
            ws=ws+pw_noc[i]*wt[i]
        pwv_los_noc=ws/np.sum(wt)

        pwv_z_noc=pwv_los_noc*math.sin(m_el)

        # for i in range(4):
        #    pw[i]=pw[i]*math.sin(m_el)
      else: # pwv <= 0.5  
        tau_constant=0.0
        ws=0.0
        for i in range(4):
            ws=ws+pw[i]*wt[i]
        pwv_los=ws/np.sum(wt)
        pwv_z=pwv_los*math.sin(m_el)
        pwv_z_noc=pwv_z
    else:   # tsrc3>300
      tau_constant = np.nan
      ws=0.0
      for i in range(4):
          ws=ws+pw[i]*wt[i]
      pwv_los=ws/np.sum(wt)
      pwv_z=pwv_los*math.sin(m_el)
      pwv_z_noc=pwv_z
        
    return pwv_z,pwv_z_noc,tau_constant,tsrcn


def remove_cloud(vis=None, correct_ms=False, offsetstable='', verbose=False, doplot=False):
    """
    Parameters:
       vis - MS with WVR data included (imported ALMA data)
       correct_ms - do the corrections to the wvr data in the MS (default False)
       offsetstable - store processing results (Temp offsets) in this table (default '' = don't store) 
       verbose - control terminal output (default False) 
       doplot - generate diagnostic plots in subdirectory vis+'_remove_cloud_plots' (default False)
    Example:
       remove_cloud(vis='uid___A002_X....', True, 'myoffsets')
    """

    print('casa test version with boxcar smoothing   verbose=',verbose)
    casalog.post('*** Starting remove_cloud ***', 'INFO')

    if vis==None or type(vis)!=str:
        casalog.post('Invalid parameter vis.', 'SEVERE')
        return False

    if correct_ms:
        mst = mstool()
        mst.open(vis)
        myref = mst.asdmref()
        mst.close()
        if not myref=='':
            casalog.post('MS '+vis
                         +' was imported with option lazy=True, i.e. its DATA column is read-only.'
                         +'\nCannot proceed when option correct_ms==True.', 'SEVERE')
            return False

    if not type(offsetstable)==str: 
        casalog.post('Invalid parameter offsetstable.', 'SEVERE')
        return False

    if offsetstable!='' and  os.path.exists(offsetstable):
        casalog.post('Table '+offsetstable+' exits.', 'SEVERE')
        return False

    if correct_ms:   # either correct or dont correct ms file - need to set in advance
        casalog.post(' Will apply corrections to WVR data. MS will be modified.', 'INFO')

    plotdir=''
    if doplot:
        plotdir = vis+'_remove_cloud_plots'
        casalog.post(' Will (re-)create directory '+plotdir+' to store plots.', 'INFO')
        os.system('rm -rf '+plotdir+'; mkdir '+plotdir)

    mytb = tbtool()
    
    # get basic info
        
    mytb.open(vis+'/ANTENNA')
    nant=mytb.nrows()
    antnames=mytb.getcol('NAME')
    mytb.close()

    mytb.open(vis+'/PROCESSOR')
    nprocs=mytb.nrows()
    procs=mytb.getcol('SUB_TYPE')
    mytb.close()

    proc_id=-1
    for ipp in range(nprocs):
        if procs[ipp]=='ALMA_RADIOMETER':
            proc_id=ipp
            break
    if proc_id<0:
        casalog.post('MS contains no WVR data.', 'SEVERE')
        return False

    mytb.open(vis+'/WEATHER')
    Tamb=np.median(mytb.getcol('TEMPERATURE'))-273.1
    mytb.close()

    mytb.open(vis+'/POINTING')
    if(mytb.nrows()==0):
        mytb.close()
        casalog.post('Empty POINTING table. Please run on MS with intact POINTING table.', 'SEVERE')
        return False
    m_el=360.0*(np.median(mytb.getcol('DIRECTION')[1]))/(2.0*3.14)
    mytb.close()

    tbo = None
    dooffsets=False
    if offsetstable!='':
        try:
            os.system('echo "0 0 0 0 0 0" > mydummy.txt')
            ok = mytb.fromascii(offsetstable, sep=" ", columnnames=['TIME','ANTENNA','OFFSETS'], datatypes=['D', 'I', 'D4'], 
                                asciifile='mydummy.txt')
            mytb.close()
        except:
            os.system('rm -f mydummy.txt')
            casalog.post('Could not create table '+offsetstable, 'SEVERE')
            return False
        os.system('rm -f mydummy.txt')
        if not ok:
            casalog.post('Error creating table '+offsetstable, 'SEVERE')
            return False
        tbo = tbtool()
        tbo.open(offsetstable, nomodify=False)
        tbo.removerows([0])
        dooffsets=True

    if correct_ms:
        mytb.open(vis,nomodify=False)
    else:
        mytb.open(vis,nomodify=True)    # dont modify 

    tsrcn=np.zeros(4)
    # values for each ant
    pwv_ant=np.zeros(nant)
    pwv_std_ant=np.zeros(nant)
    tauc_ant=np.zeros(nant)
    tauc_std_ant=np.zeros(nant)

    for iant in range(nant):
#      if antnames[iant] == 'DV22':
        casalog.post('- Processing antenna#'+str(iant)+' ('+antnames[iant]+') ...', 'INFO')
        tb1=mytb.query("PROCESSOR_ID==%d && ANTENNA1==%d" % (proc_id,iant), sortlist='TIME')
        temp=tb1.getcol('DATA')
        nsamples=len(temp[0][0])
        pwvna=np.zeros(nsamples)
        pwvn_noca=np.zeros(nsamples)
        tau_con=np.zeros(nsamples)

        offsets=None
        rowtimes=None
        if dooffsets:
            rowtimes = tb1.getcol('TIME')
            offsets=np.zeros((4,nsamples))

        timestart = datetime.datetime.now()

        for isam in range(nsamples):
#        for isam in range(500,520):

            tsrc=[(temp[0][0][isam]).real, (temp[0][1][isam]).real, (temp[0][2][isam]).real, (temp[0][3][isam]).real]

            # got temps, now convert to pwv
            do_cal_offset = False
            pwvna[isam],pwvn_noca[isam],tau_con[isam],tsrcn=rmc_approxCalc(tsrc[0], tsrc[1], tsrc[2], tsrc[3], m_el, Tamb, do_cal_offset,
                                                                           isam, verbose)
            if dooffsets:
                for it in range(4):
                    offsets[it][isam]=tsrc[it] - tsrcn[it] # = old WVR value minus newly calculated one
 

            if correct_ms:
                # put the new tsrcn values for this sample & antenna into temp[0][0-3][isam]
                for it in range(4):
                    temp[0][it][isam]=tsrcn[it]

        timeend = datetime.datetime.now()

#  estimate fraction of samples which have real pwv and tau_con==0.0  (assumes these have offset issues)
        count_sam_problems = 0
        for isam in range(nsamples):
            if pwvna[isam] > 0.1 and tau_con[isam] == 0.0:
                count_sam_problems +=1
        tau_count_fraction= float(count_sam_problems)/float(nsamples)
#        print antnames[iant], tau_count_fraction
        if tau_count_fraction > 0.05:
            # approximately zero implying the WVR on this antenna may have a calibration offset
            # so re-run tau calculation with tau_offset

            casalog.post(antnames[iant] + ' Some continuum tau values (' + str(count_sam_problems) + ' samples) are less than 0.0 for this antenna. rerunning calculation with offset', 'WARN')


            for isam in range(nsamples):
#            for isam in range(500,520):
                tsrc=[(temp[0][0][isam]).real, (temp[0][1][isam]).real, (temp[0][2][isam]).real, (temp[0][3][isam]).real]
            # got temps, now convert to pwv

                do_cal_offset = True
                pwvna[isam],pwvn_noca[isam],tau_con[isam],tsrcn=rmc_approxCalc(tsrc[0], tsrc[1], tsrc[2], tsrc[3], m_el, Tamb, do_cal_offset,isam, verbose)
                
                if verbose:
                    print('sample',isam,pwvna[isam],pwvn_noca[isam])

                if dooffsets:
                    for it in range(4):
                        offsets[it][isam]=tsrc[it] - tsrcn[it] # = old WVR value minus newly calculated one

                if correct_ms:
                # put the new tsrcn values for this sample & antenna into temp[0][0-3][isam]
                    for it in range(4):
                        temp[0][it][isam]=tsrcn[it]

    # option to boxcar smooth the pwv samples and offsets table slightly
        ismooth = False
        if ismooth:
            print('boxcar smoothing pwvn_noca and offsets')
            pwvn_noca2 = np.zeros(len(pwvn_noca))
            offsets2=np.zeros((4,nsamples))
            for isam in range(1,(nsamples-1)):
                pwvn_noca2[isam] = np.mean([pwvn_noca[isam-1],pwvn_noca[isam+1],pwvn_noca[isam],pwvn_noca[isam]])
                if dooffsets:
                    for it in range(4):
                        offsets2[it][isam] = np.mean([offsets[it][isam-1],offsets[it][isam+1],offsets[it][isam],offsets[it][isam]])
            pwvn_noca = pwvn_noca2
            offsets = offsets2

        print(antnames[iant],' processed. time elapsed',(timeend-timestart))

        if dooffsets:
            casalog.post('   Writing the offset values for antenna '+str(iant)+' to '+offsetstable, 'INFO')
            startrow=tbo.nrows()
            tbo.addrows(nsamples)
            tbo.putcol('TIME', rowtimes, startrow)
            tbo.putcol('OFFSETS', offsets, startrow)
            ants = np.empty(nsamples)
            ants.fill(iant)
            tbo.putcol('ANTENNA', ants, startrow)
            

        if correct_ms:
            casalog.post('   Writing new values for antenna '+str(iant)+' to Main table of '+vis, 'INFO')
            tb1.putcol('DATA',temp)
        
        tb1.close()

        # now outputs to the screen the medians of the samples
        # this just removes crazy numbers, for rms estimate
        pwvna_m=nanmedian(pwvna)
        pwvn_noca_m=nanmedian(pwvn_noca)
        tau_constant_m=nanmedian(tau_con)
        for i in range(len(pwvna)):
            if abs(pwvna[i]-pwvna_m)>1.0:
                pwvna[i]=np.nan
            if abs(pwvn_noca[i]-pwvn_noca_m)>1.0:
                pwvn_noca[i]=np.nan
            if abs(tau_con[i]-tau_constant_m)>0.2:
                tau_con[i]=np.nan

        casalog.post('   Result for '+antnames[iant]+':', 'INFO')
        casalog.post('      PWV    : before, after '+str(nanmedian(pwvna))+', '+str(nanmedian(pwvn_noca)), 'INFO')
        casalog.post('      PWV rms: before, after '+str(nanstd(pwvna))+','+str(nanstd(pwvn_noca)), 'INFO')
        if not do_cal_offset:
            casalog.post('      tau_constant '+str(tau_constant_m)+'  rms '+str(nanstd(tau_con)), 'INFO')
        else:
            casalog.post('      tau_constant '+str(tau_constant_m)+'  rms '+str(nanstd(tau_con)) + ' with calibration offset applied' , 'INFO')

        pwv_ant[iant]=nanmedian(pwvn_noca)
        pwv_std_ant[iant]=nanstd(pwvn_noca)
        tauc_ant[iant]=tau_constant_m
        tauc_std_ant[iant]=nanstd(tau_con)

        if doplot:
            # plot before and after results
            tau_con_scaled=10*tau_con
            pl.ion()
            pyplot.clf()
            pyplot.plot(pwvna, color='blue')
            pyplot.plot(pwvn_noca, color='red')
            pyplot.plot(tau_con_scaled, color='green')
            ptitle = antnames[iant]+'  ('+str(iant)+')  '+vis
            if do_cal_offset:
                ptitle = ptitle + ' (cal offset)'
            pyplot.title(ptitle)
            pyplot.xlabel('Measurement Number')
            pyplot.ylabel('blue=PWV_before (mm), red=PWV_after (mm), green=10*tau_con')
            pyplot.draw()
            plotfil=plotdir+'/'+antnames[iant]+'.png'
            pyplot.savefig(plotfil)
            casalog.post('    Generated '+plotfil, 'INFO')
    #end for

    mytb.close()

    if dooffsets:
        pwv_noca_all=nanmedian(pwv_ant)
        pwv_std_all=nanmedian(pwv_std_ant)
        tauc_all=nanmedian(tauc_ant)
        tauc_std_all=nanmedian(tauc_std_ant)

        tbo.putkeyword('REFMS', vis)
        tbo.putkeyword('CREATION_UTC', time.asctime(time.gmtime()))
        tbo.putkeyword('PWV', pwv_noca_all)
        tbo.putkeyword('PWV_STDEV', pwv_std_all)
        tbo.putkeyword('TAUC', tauc_all)
        tbo.putkeyword('TAUC_STDEV', tauc_std_all)

        tbo.close()
        
        casalog.post(' Saved remove_cloud results to '+offsetstable, 'INFO')


    return True
  
