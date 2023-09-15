import math, sys, optparse, array, time, copy, glob, os, os.path

year=['2017', '2018']
var=['allpuppi', 'allmet']
#var=['boson_pt']
mc=['NLO', 'WNjets44']
channels=['MuMu', 'ElEl']

for v in var:
    for ch in channels:
        for m in mc:
            for y in year:
                fiLe='/publicweb/a/alkaloge/plots/MetStudies/{1:s}_{0:s}_doQCD0_WIncl{2:s}_QCDHT_nLepEq1_njetsGt0_BtagL_WTmassGt80_T1_v2_Log_{3:s}.pdff'.format(str(y), str(v), str(m), str(ch))
		cf = os.path.isfile(fiLe)
                if not cf : 
                    #print 'does not exist', fiLe
		    print '. exx {0:s}  {1:s} 0 WIncl{2:s}_QCDHT_nLepEq1_njetsGt0_BtagL_WTmassGt80_T1_v2 {3:s} &>log{0:s}{1:s}{2:s}{3:s}&'.format(str(y), str(v), str(m), str(ch))



