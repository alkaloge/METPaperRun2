cats = ['eeem','eeet','eemt','eett','mmem','mmet','mmmt','mmtt']
cats = ['mm']
#cats = ['mmmm']

# make lists of Mine and Mine events
OtherEvents, MineEvents = {}, {}
for cat in cats :
    OtherEvents[cat] = {}
    MineEvents[cat] = {}
'''
for line in open('sync_eeee.txt','r').readlines() :
    vals = line.split()
    print vals, '------->0 ', vals[0], ' pp', vals[1], int(vals[4]), float(vals[5]), float(vals[6])
'''
cat=cats[0]

fin='sync_{0:s}_1file.txt'.format(cat)
fin='SyncLepton2018_DYJetsToLL_LHEFilterPtZ-100To250_{0:s}.txt'.format(cat)
#for line in open('sync_eeee_allFiles_signal.txt','r').readlines() :
for line in open(fin,'r').readlines() :
    vals = line.split()
    if len(vals) < 2 : continue 
    #  run *      luminosityBlock *                event *          pt_pos_lead *          pt_pos_subl *          pt_neg_lead *          pt_neg_subl *
    LS, event, run =  int(vals[1]), int(vals[2]), int(vals[3])
    #cat, event,pt_1, pt_2, pt_3,pt_4 = cat, int(vals[4]), float(vals[5]), float(vals[6]),  float(vals[7]), float(vals[8])
    #cat, event,pt_1, pt_2 = cat, int(vals[4]), float(vals[5]), float(vals[6])
    LSrunEvent = "{0:d}:{1:d}:{2:d}".format(LS,event,run) 
    #LSrunEvent = "{0:.3f}:{1:.3f}".format(pt_1, pt_2) 
    OtherEvents[cat][LSrunEvent] = line 
    
for cat in cats :
    #for line in open('log_DCH_{0:s}_all_signal.txt'.format(cat),'r').readlines() :
    for line in open('zhh_{0:s}'.format(cat),'r').readlines() :
        vals = line.split()
        if len(vals) < 2 : continue 
        #cat, run, LS, event = vals[0], int(vals[1]), int(vals[2]), int(vals[3])
        LS, event, run = int(vals[1]), int(vals[2]), int(vals[3])
        #cat, event,pt_1, pt_2, pt_3,pt_4 = cat, int(vals[2]), float(vals[3]), float(vals[4]),  float(vals[5]), float(vals[6])
        #cat, event,pt_1, pt_2 = cat, int(vals[3]), float(vals[4]), float(vals[4])
        #LSrunEvent = "{0:.3f}:{1:.3f}".format(pt_1, pt_2) 
        LSrunEvent = "{0:d}:{1:d}:{2:d}".format(LS,event,run) 
        MineEvents[cat][LSrunEvent] = line 
        
    print MineEvents[cat][LSrunEvent][0]
    
# compare the lists
uniqueOther, uniqueMine = {}, {}
for cat in cats :
    uniqueOther[cat], uniqueMine[cat] = [], []
    for key in OtherEvents[cat].keys() :
        try : check = MineEvents[cat][key]
        except KeyError : uniqueOther[cat].append(OtherEvents[cat][key]) 
    for key in MineEvents[cat].keys() :
        try : check = OtherEvents[cat][key]
        except KeyError : uniqueMine[cat].append(MineEvents[cat][key])

    open('Otherunique_{0:s}.txt'.format(cat),'w').writelines(uniqueOther[cat])
    open('Mineunique_{0:s}.txt'.format(cat),'w').writelines(uniqueMine[cat])

# print summary
print(" Cat      nOther      nMine    nBoth   Otheronly   Mineonly") 
for cat in cats :
    nBoth = len(OtherEvents[cat]) - len(uniqueOther[cat])
    print("{0:s} {1:8d} {2:8d} {3:8d} {4:8d} {5:8d}".format(
        cat,len(OtherEvents[cat]),len(MineEvents[cat]), nBoth, len(uniqueOther[cat]), len(uniqueMine[cat])))
