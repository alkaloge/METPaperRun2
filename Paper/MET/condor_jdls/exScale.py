import os

years = ["2018", "2017", "2016", "2016preVFP"]
years = ["2016", "2016preVFP"]
#years = ["2018", "2017"]
#years = ["2017"]
channels = ["Gjets"]
channels = ["MuMu", "ElEl"]

#channels = ["MuMu"]

modes = ["dynlo"]
njets = ["eq0", "eq1", "geq1", "incl"]

#njets = ["eq1", "geq1", "incl"]
#njets = ["incl"]



os.system("cp txt_Gjets_mc_sub/*_Gjets_npv*txt txt_Gjets_mc_sub/*_Gjets_vspt*txt txt_Gjets/")
channelDir = "Gjets_mc_sub"
extra = "cutbased_isocuttight"


for channel in channels:
    if 'Gjets' not in channel : channelDir= channel
    if 'Gjets' in channel : 
	modes =["Gjets"]
	os.system("cp graph_scale_vspt_Gjets.C graph_scale_vspt.C")

    if 'Gjets' not in channel : 
	os.system("cp graph_scale_vspt_DY.C graph_scale_vspt.C")
    for year in years:

        #if 'Gjets' in channel : njets = ["eq1", "geq1", "incl"]
        for mode in modes:
            for jet in njets:

                print year, channelDir, channel, mode, jet
                print "root -l -q -b 'graph_scale_vspt.C(\"_vspt_\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")'".format(year, channelDir, channel, mode, jet)
                os.system("root -l -q -b 'graph_scale_vspt.C(\"_vspt_\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")'".format(year, channelDir, channel, mode, jet))
                os.system("root -l -q -b 'graph_scale_npv.C(\"_npv_\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")'".format(year, channelDir, channel, mode, jet))

                #os.system("montage -tile 4x2 -geometry +10+5 -density 150 -resize 50% -quality 90 res_perp_*{}*{}_{}.pdf plots_res_perp_{}_{}_{}.pdf".format(year, channelDir, extra, year, channelDir, extra))                
                #os.system("montage -tile 4x2 -geometry +10+5 -density 150 -resize 50% -quality 90 scale_*{}*{}_{}.pdf plots_scale_{}_{}_{}.pdf".format(year, channelDir, extra, year, channelDir, extra))
                #os.system("montage -tile 4x2 -geometry +10+5 -density 150 -resize 50% -quality 90 res_par_*{}*{}_{}.pdf plots_res_par_{}_{}_{}.pdf".format(year, channelDir, extra, year, channelDir, extra))
        print "cp scale_{0}*_*_{1}_{2}.pdf res_p*_{0}*_njets*_*_{1}_{2}.pdf plots_*_{0}_{1}_{2}.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Scalesv4/".format(year, channelDir, extra)
        os.system("cp scale_{0}*_*_{1}_{2}.pdf res_p*_{0}*_njets*_*_{1}_{2}.pdf plots_*_{0}_{1}_{2}.pdf /publicweb/a/alkaloge/plots/MetStudiesPaper/Scalesv4/".format(year, channelDir, extra))


