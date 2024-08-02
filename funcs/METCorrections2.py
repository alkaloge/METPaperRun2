from math import cos, sin, atan, sqrt, pi

def correctedMET2(uncormet, uncormet_phi, npv, runnb, isMC, yeara, isUL=False, ispuppi=False):
    #TheXYCorr_Met_MetPhi = (uncormet, uncormet_phi)
    
    if npv > 100:
        npv = 100
    year=str(yeara)
    runera = -1
    usemetv2 = False
    year = year.replace("postVFP", "nonAPV")
    year = year.replace("preVFP", "APV")
    
    if (isMC and year == "2016" and isUL) :  runera ="yUL2016MCnonAPV"
    elif(isMC and year == "2016APV" and isUL): runera = "yUL2016MCAPV"
    elif(isMC and year == "2016nonAPV" and isUL): runera = "yUL2016MCnonAPV"
    elif(isMC and year == "2017" and isUL) :runera = "yUL2017MC"
    elif(isMC and year == "2018" and isUL) :runera = "yUL2018MC"
    elif(not isMC and runnb >=315252 and runnb <=316995 and isUL): runera = "yUL2018A"
    elif(not isMC and runnb >=316998 and runnb <=319312 and isUL): runera = "yUL2018B"
    elif(not isMC and runnb >=319313 and runnb <=320393 and isUL): runera = "yUL2018C"
    elif(not isMC and runnb >=320394 and runnb <=325273 and isUL): runera = "yUL2018D"

    elif(not isMC and runnb >=297020 and runnb <=299329 and isUL):
      runera = "yUL2017B"
      usemetv2 =False
    elif(not isMC and runnb >=299337 and runnb <=302029 and isUL):
      runera = "yUL2017C"
      usemetv2 =False
    elif(not isMC and runnb >=302030 and runnb <=303434 and isUL):
      runera = "yUL2017D"
      usemetv2 =False
    elif(not isMC and runnb >=303435 and runnb <=304826 and isUL):
      runera = "yUL2017E"
      usemetv2 =False
    elif(not isMC and runnb >=304911 and runnb <=306462 and isUL):
      runera = "yUL2017F"
      usemetv2 =False

    elif(not isMC and runnb >=272007 and runnb <=275376 and isUL): runera = "yUL2016B"
    elif(not isMC and runnb >=275657 and runnb <=276283 and isUL): runera = "yUL2016C"
    elif(not isMC and runnb >=276315 and runnb <=276811 and isUL): runera = "yUL2016D"
    elif(not isMC and runnb >=276831 and runnb <=277420 and isUL): runera = "yUL2016E"
    elif(not isMC and ((runnb >=277772 and runnb <=278768) or runnb==278770) and isUL): runera = "yUL2016F"
    elif(not isMC and ((runnb >=278801 and runnb <=278808) or runnb==278769) and isUL): runera = "yUL2016Flate"
    elif(not isMC and runnb >=278820 and runnb <=280385 and isUL): runera = "yUL2016G"
    elif(not isMC and runnb >=280919 and runnb <=284044 and isUL): runera = "yUL2016H"

    else :   
      print 'failed, ============================================>', year, runera, isMC
      return [1, 1, 0.,0.]

    corrmet = uncormet
    corrmet_phi = uncormet_phi
    
    if usemetv2:
        corrmet, corrmet_phi = METXYCorr_Met_MetPhi_v2(uncormet, uncormet_phi, runera, npv)
    else:
        #print 'will correct for',  runera, corrmet, corrmet_phi
        if runera == "yUL2016B":
            corrmet *= 1.006
            corrmet_phi -= 0.005
        elif runera == "yUL2016G":
            corrmet *= 1.004
            corrmet_phi -= 0.015
        elif runera == "yUL2016H":
            corrmet *= 1.003
            corrmet_phi -= 0.025
        elif runera == "yUL2017B":
            if not isUL:
                corrmet *= (1.003 - 0.002 * npv)
                corrmet_phi -= (0.84 - 0.003 * npv)
            else:
                corrmet *= (1.006 - 0.002 * npv)
                corrmet_phi -= (0.76 - 0.01 * npv)
        elif runera == "yUL2017C":
            if not isUL:
                corrmet *= (1.004 - 0.002 * npv)
                corrmet_phi -= (1.34 - 0.006 * npv)
            else:
                corrmet *= (1.005 - 0.003 * npv)
                corrmet_phi -= (1.26 - 0.012 * npv)
        elif runera == "yUL2017D":
            if not isUL:
                corrmet *= (1.021 - 0.001 * npv)
                corrmet_phi -= (0.64 - 0.016 * npv)
            else:
                corrmet *= (1.015 - 0.001 * npv)
                corrmet_phi -= (0.65 - 0.018 * npv)
        elif runera == "yUL2017E":
            if not isUL:
                corrmet *= (1.01 - 0.001 * npv)
                corrmet_phi -= (1.19 - 0.016 * npv)
            else:
                corrmet *= (1.014 - 0.001 * npv)
                corrmet_phi -= (1.18 - 0.016 * npv)
        elif runera == "yUL2017F":
            if not isUL:
                corrmet *= (1.01 - 0.002 * npv)
                corrmet_phi -= (1.15 - 0.016 * npv)
            else:
                corrmet *= (1.02 - 0.003 * npv)
                corrmet_phi -= (1.12 - 0.019 * npv)
        elif runera == "yUL2018A":
            corrmet *= (1.003 - 0.002 * npv)
            corrmet_phi -= (0.63 - 0.03 * npv)
        elif runera == "yUL2018B":
            corrmet *= (1.006 - 0.002 * npv)
            corrmet_phi -= (0.65 - 0.02 * npv)
        elif runera == "yUL2018C":
            corrmet *= (1.01 - 0.001 * npv)
            corrmet_phi -= (0.7 - 0.025 * npv)
        elif runera == "yUL2018D":
            corrmet *= (1.009 - 0.001 * npv)
            corrmet_phi -= (0.75 - 0.025 * npv)
        elif runera == "yUL2018A":
            corrmet *= (1.010 - 0.002 * npv)
            corrmet_phi -= (0.74 - 0.03 * npv)
        elif runera == "yUL2018B":
            corrmet *= (1.011 - 0.002 * npv)
            corrmet_phi -= (0.75 - 0.03 * npv)
        elif runera == "yUL2018C":
            corrmet *= (1.012 - 0.001 * npv)
            corrmet_phi -= (0.74 - 0.03 * npv)
        elif runera == "yUL2018D":
            corrmet *= (1.012 - 0.001 * npv)
            corrmet_phi -= (0.76 - 0.03 * npv)
    
    return corrmet, corrmet_phi



