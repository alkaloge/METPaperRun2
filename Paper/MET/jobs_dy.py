#!/usr/bin/env python

import os

allsyst = ["Nominal", "JESUp", "JESDown", "JERUp", "JERDown", "UnclusteredUp", "UnclusteredDown"]
samples = ["data", "dy", "dynlo", "top", "ew"]
channels = ["MuMu", "ElEl"]
years = ["2016preVFP", "2016postVFP", "2017"]
years = ["2018", "2017"]
extra = ''
vars = ["METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGood_T1Smear_pt"]
vars = ["METCorGood_T1Smear_pt"]
dosend = "1"
moremem = "0"
jetcut = "njetsgt0"
btag = "nbtagl_10bins"
veto = "1"

for sy in allsyst:
    dosend = "1"
    for yr in years:
        dosend = "1"
        for ss in samples:
            if ss == "ewk" and yr == "2016postVFP":
                moremem = "1"
            ss = f"{ss}_{jetcut}_{btag}_hitslt{veto}{extra}"
            for ch in channels:
                for vr in vars:
                    if sy == "Nominal":
                        sy = ""
                    os.system(f"cp job_template Jobs_dy/jobb_{yr}_{vr}{sy}_{ss}_{ch}.sh")
                    os.system(f"echo python dy_met_distribution.py -y {yr} -v {vr}{sy} -q 0 -e {ss} -c {ch} -l no >> Jobs_dy/jobb_{yr}_{vr}{sy}_{ss}_{ch}.sh")
                    os.system(f"cp jdl_template Jobs_dy/jobb_{yr}_{vr}{sy}_{ss}_{ch}.jdl")
                    yrr = yr
                    if "preVFP" in yrr:
                        yrr = "2016preVFP"
                    os.system(f'sed -i \'s/EXECHERE/jobb_{yr}_{vr}{sy}_{ss}_{ch}.sh/g\' Jobs_dy/jobb_{yr}_{vr}{sy}_{ss}_{ch}.jdl')
                    os.system(f'sed -i \'s/YEARHERE/{yrr}/g\' Jobs_dy/jobb_{yr}_{vr}{sy}_{ss}_{ch}.jdl')
                    os.system(f"echo \"cp plotS*root ../../.\" >> Jobs_dy/jobb_{yr}_{vr}{sy}_{ss}_{ch}.sh")

for sy in allsyst:
    for yr in years:
        for ss in samples:
            ss = f"{ss}_{jetcut}_{btag}_hitslt{veto}{extra}"
            for ch in channels:
                for vr in vars:
                    if sy == "Nominal":
                     
                        sy = ""
                    if not os.path.isfile(f"Jobs_dy/plotS_{yr}_{ss}_{vr}{sy}_{ch}.root"):
                        print(f"this is not there... Jobs_dy/plotS_{yr}_{ss}_{vr}{sy}_{ch}.root")
                        os.chdir("Jobs_dy")
                        os.system(f"condor_submit jobb_{yr}_{vr}{sy}_{ss}_{ch}.jdl")
                        os.chdir("..")
                    else:
                        print(f"Jobs_dy/plotS_{yr}_{ss}_{vr}{sy}_{ch}.root")



