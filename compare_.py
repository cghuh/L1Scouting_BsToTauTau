import copy, math, os
from numpy import array
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from array import array

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]

#ptbin = [0,1,2,3,4,5,6,7,8,9,10, 15, 20]
ptbin = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,6,7,8,9,10]


def applyHistStyle(h, i):
    print(h, i)
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(3)
    h.SetStats(False)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def comparisonPlots(hists, titles, isLog=False, pname='sync.pdf', isEff = False, isRatio=False, isLegend=False):

    display = DisplayManager(pname, isLog, isRatio, 0.42, 0.7)
    display.draw_legend = isLegend
    display.isEff = isEff
    
    display.Draw(hists, titles)


def sproducer(key, rootfile, name, ivar, addsel = '1'):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['nbin'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + ivar['sel'] + '&&' + addsel + ')'
        
    tree = rootfile.Get(ivar['tree'])

    print(ivar['var'] + ' >> ' + hist.GetName(), exp)
    
    tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(ivar['title'])
    hist.GetYaxis().SetTitle('a.u.')
    hist.GetYaxis().SetNdivisions(506)
        
    return copy.deepcopy(hist)


def sproducer_w(key, rootfile, name, ivar, addsel = '1'):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['nbin'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + ivar['sel'] + '&&' + addsel + ')/trk_pt'
        
    tree = rootfile.Get(ivar['tree'])

    print(ivar['var'] + ' >> ' + hist.GetName(), exp)
    
    tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(ivar['title'])
    hist.GetYaxis().SetTitle('a.u.')
    hist.GetYaxis().SetNdivisions(506)
        
    return copy.deepcopy(hist)



def effproducer(key, rootfile, name, ivar, addsel='1'):

    if ivar['isVar']:

        hist = TH2F('h_' + key + '_' + name, 
                    'h_' + key + '_' + name,
                    len(ptbin)-1, array('d', ptbin),
                    ivar['ynbin'], ivar['ymin'], ivar['ymax'])
    else:

        hist = TH2F('h_' + key + '_' + name, 
                    'h_' + key + '_' + name, 
                    ivar['xnbin'], ivar['xmin'], ivar['xmax'],
                    ivar['ynbin'], ivar['ymin'], ivar['ymax'])


    hist.Sumw2()
    exp = '(' + ivar['sel'] + '&&' + addsel + ')'
        
    tree = rootfile.Get(ivar['tree'])

#    print ivar['var'], 'effstr = ', effstr + ' >> ' + hist.GetName(), exp
    
    tree.Draw(ivar['yvar'] + ':' + ivar['xvar'] + ' >> ' + hist.GetName(), exp)
    
    hist.SetMaximum(ivar['ymax'])
    hist.SetMinimum(ivar['ymin'])
    hist.GetXaxis().SetTitle(ivar['xtitle'])
    hist.GetYaxis().SetTitle(ivar['ytitle'])
    return copy.deepcopy(hist)

    # hprof = hist.ProfileX()
    # hprof.SetMaximum(ivar['ymax'])
    # hprof.SetMinimum(ivar['ymin'])
    # hprof.GetXaxis().SetTitle(ivar['xtitle'])
    # hprof.GetYaxis().SetTitle(ivar['ytitle'])
    # hprof.GetYaxis().SetNdivisions(506)

    # if name.find('eff')!=-1:
    #     hprof.SetMaximum(1.2)
    #     hprof.SetMinimum(0)

    # if name.find('res')!=-1:

    #     hprof.SetMaximum(1.)
    #     hprof.SetMinimum(-1.)

    # return copy.deepcopy(hprof)




acc = 'abs(gen_eta) < 2.3'
drmatch = 'dr > 0 && dr < 0.02'
flag_t = 'trk_flag > 0.5'
flag_f = 'trk_flag < 0.5'
d0 = 'abs(trk_d0) < 0.2'
genmatch = 'abs(trk_matchtp_pdgid) == 211'
genfail = 'abs(trk_matchtp_pdgid) != 211'

vardict = {

    'pt_trk':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':flag_t},
    'eta_trk':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':flag_t},
    'phi_trk':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':flag_t},
    'd0_trk':{'tree':'tree', 'var':'trk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':flag_t},
    'z0_trk':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':flag_t},
    'nstub_trk':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':flag_t},
    'chi2dof_trk':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':flag_t},
    'chi2rphi_trk':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':flag_t},
    'chi2rz_trk':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':flag_t},
    'bendchi2_trk':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':flag_t},
    'fake_trk':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':flag_t},
    'pdgid_trk':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track pdgid", 'sel':flag_t},
    'pdgid_trk_zoom':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':800, 'xmin':-400, 'xmax':400, 'title':"track pdgid", 'sel':flag_t},
    'hitpattern_trk':{'tree':'tree', 'var':'trk_hitpattern', 'nbin':130, 'xmin':0, 'xmax':130, 'title':"track hitpattern", 'sel':flag_t},
    'MVA_trk':{'tree':'tree', 'var':'trk_MVA', 'nbin':100, 'xmin':0, 'xmax':1, 'title':"track MVA1", 'sel':flag_t},

    'pt_faketrk':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':flag_f},
    'eta_faketrk':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':flag_f},
    'phi_faketrk':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':flag_f},
    'd0_faketrk':{'tree':'tree', 'var':'trk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':flag_f},
    'z0_faketrk':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':flag_f},
    'nstub_faketrk':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':flag_f},
    'chi2dof_faketrk':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':flag_f},
    'chi2rphi_faketrk':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':flag_f},
    'chi2rz_faketrk':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':flag_f},
    'bendchi2_faketrk':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':flag_f},
    'fake_faketrk':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':flag_f},
    'pdgid_faketrk':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track pdgid", 'sel':flag_f},
    'pdgid_faketrk_zoom':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':800, 'xmin':-400, 'xmax':400, 'title':"track pdgid", 'sel':flag_f},
    'hitpattern_faketrk':{'tree':'tree', 'var':'trk_hitpattern', 'nbin':130, 'xmin':0, 'xmax':130, 'title':"track hitpattern", 'sel':flag_f},
    'MVA_faketrk':{'tree':'tree', 'var':'trk_MVA', 'nbin':100, 'xmin':0, 'xmax':1, 'title':"track MVA1", 'sel':flag_f},

    'pt_alltrk':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':'1'},
    'eta_alltrk':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':'1'},
    'phi_alltrk':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':'1'},
    'd0_alltrk':{'tree':'tree', 'var':'trk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':'1'},
    'z0_alltrk':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':'1'},
    'nstub_alltrk':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':'1'},
    'chi2dof_alltrk':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':'1'},
    'chi2rphi_alltrk':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':'1'},
    'chi2rz_alltrk':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':'1'},
    'bendchi2_alltrk':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':'1'},
    'all_faketrk':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':'1'},
    'pdgid_alltrk':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track pdgid", 'sel':'1'},
    'pdgid_alltrk_zoom':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':800, 'xmin':-400, 'xmax':400, 'title':"track pdgid", 'sel':'1'},
    'hitpattern_alltrk':{'tree':'tree', 'var':'trk_hitpattern', 'nbin':130, 'xmin':0, 'xmax':130, 'title':"track hitpattern", 'sel':'1'},
    'MVA_alltrk':{'tree':'tree', 'var':'trk_MVA', 'nbin':100, 'xmin':0, 'xmax':1, 'title':"track MVA1", 'sel':'1'},

    'pt_trk_genmatch':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':genmatch+'&&'+flag_t},
    'eta_trk_genmatch':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':genmatch+'&&'+flag_t},
    'phi_trk_genmatch':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':genmatch+'&&'+flag_t},
    'z0_trk_genmatch':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':genmatch+'&&'+flag_t},
    'nstub_trk_genmatch':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':genmatch+'&&'+flag_t},
    'chi2dof_trk_genmatch':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':genmatch+'&&'+flag_t},
    'chi2rphi_trk_genmatch':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':genmatch+'&&'+flag_t},
    'chi2rz_trk_genmatch':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':genmatch+'&&'+flag_t},
    'bendchi2_trk_genmatch':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':genmatch+'&&'+flag_t},
    'fake_trk_genmatch':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':genmatch+'&&'+flag_t},
    'pdgid_trk_genmatch':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track pdgid", 'sel':genmatch+'&&'+flag_t},
    'pdgid_trk_genmatch_zoom':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':800, 'xmin':-400, 'xmax':400, 'title':"track pdgid", 'sel':genmatch+'&&'+flag_t},
    'hitpattern_trk_genmatch':{'tree':'tree', 'var':'trk_hitpattern', 'nbin':130, 'xmin':0, 'xmax':130, 'title':"track hitpattern", 'sel':genmatch+'&&'+flag_t},

    'pt_faketrk_genmatch':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':genfail+'&&'+flag_f},
    'eta_faketrk_genmatch':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':genfail+'&&'+flag_f},
    'phi_faketrk_genmatch':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':genfail+'&&'+flag_f},
    'z0_faketrk_genmatch':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':genfail+'&&'+flag_f},
    'nstub_faketrk_genmatch':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':genfail+'&&'+flag_f},
    'chi2dof_faketrk_genmatch':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':genfail+'&&'+flag_f},
    'chi2rphi_faketrk_genmatch':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':genfail+'&&'+flag_f},
    'chi2rz_faketrk_genmatch':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':genfail+'&&'+flag_f},
    'bendchi2_faketrk_genmatch':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':genfail+'&&'+flag_f},
    'fake_faketrk_genmatch':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':genfail+'&&'+flag_f},
    'pdgid_faketrk_genmatch':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track pdgid", 'sel':genfail+'&&'+flag_f},
    'pdgid_faketrk_genmatch_zoom':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':800, 'xmin':-400, 'xmax':400, 'title':"track pdgid", 'sel':genfail+'&&'+flag_f},
    'hitpattern_faketrk_genmatch':{'tree':'tree', 'var':'trk_hitpattern', 'nbin':130, 'xmin':0, 'xmax':130, 'title':"track hitpattern", 'sel':genfail+'&&'+flag_f},
    }

order_of_keys = [
    # 'pt_trk', 'pt_faketrk', 'eta_trk', 'eta_faketrk', 'phi_trk', 'phi_faketrk', 
    # 'd0_trk', 'd0_faketrk', 
    # 'z0_trk', 'z0_faketrk', 'nstub_trk', 'nstub_faketrk', 'MVA_trk', 'MVA_faketrk',
    # 'chi2dof_trk', 'chi2dof_faketrk', 'chi2rphi_trk', 'chi2rphi_faketrk',
    # 'chi2rz_trk', 'chi2rz_faketrk', 'bendchi2_trk', 'bendchi2_faketrk',
    # 'fake_trk', 'fake_faketrk', 'pdgid_trk', 'pdgid_faketrk', 'pdgid_trk_zoom', 'pdgid_faketrk_zoom',
    # 'hitpattern_trk', 'hitpattern_faketrk',
    'pt_trk_genmatch', 'pt_faketrk_genmatch', 'eta_trk_genmatch', 'eta_faketrk_genmatch', 'phi_trk_genmatch', 'phi_faketrk_genmatch', 
    'z0_trk_genmatch', 'z0_faketrk_genmatch', 'nstub_trk_genmatch', 'nstub_faketrk_genmatch',
    'chi2dof_trk_genmatch', 'chi2dof_faketrk_genmatch', 'chi2rphi_trk_genmatch', 'chi2rphi_faketrk_genmatch',
    'chi2rz_trk_genmatch', 'chi2rz_faketrk_genmatch', 'bendchi2_trk_genmatch', 'bendchi2_faketrk_genmatch',
    'fake_trk_genmatch', 'fake_faketrk_genmatch', 'pdgid_trk_genmatch', 'pdgid_faketrk_genmatch', 'pdgid_trk_genmatch_zoom', 'pdgid_faketrk_genmatch_zoom',
    'hitpattern_trk_genmatch', 'hitpattern_faketrk_genmatch'
]

order_of_keys_z0 = [
    'z0_trk', 'z0_alltrk',
    'z0_trk', 'z0_alltrk',
]


effvardict = {
    'etaphi':{'tree':'tree', 'xvar':'trk_eta', 'yvar':'trk_phi', 'xnbin':100, 'xmin':-2.5, 'xmax':2.5, 'ynbin':100, 'ymin':-math.pi, 'ymax':math.pi, 'xtitle':'track eta', 'ytitle':"track phi", 'sel':'1', 'isVar':False},
    'm_etaphi':{'tree':'tree', 'xvar':'trk_eta', 'yvar':'trk_phi', 'xnbin':100, 'xmin':-2.5, 'xmax':2.5, 'ynbin':100, 'ymin':-math.pi, 'ymax':math.pi, 'xtitle':'track eta', 'ytitle':"track phi", 'sel':flag_t, 'isVar':False},
    #'eff':{'tree':'tree', 'xvar':'gen_pt', 'yvar':drmatch, 'xnbin':15, 'xmin':0, 'xmax':15, 'ynbin':2, 'ymin':-0.5, 'ymax':1.5, 'xtitle':'gen. pT (GeV)', 'ytitle':"TF matching eff.", 'sel':acc, 'isVar':False},
    #'res':{'tree':'tree', 'xvar':'gen_pt', 'yvar':'(trk_pt - gen_pt)/gen_pt', 'xnbin':15, 'xmin':0, 'xmax':15, 'ynbin':100, 'ymin':-1., 'ymax':6., 'xtitle':'gen. pT (GeV)', 'ytitle':"(TF - gen.)/gen.", 'sel':drmatch + '&&' + acc, 'isVar':False},
    
    #'eff_ta_match_dm10':{'tree':'ta_tree', 'xvar':'ta_gen_pt', 'yvar':'ta_iscontained==1', 'xnbin':20, 'xmin':0, 'xmax':20, 'ynbin':2, 'ymin':-0.5, 'ymax':1.5, 'xtitle':'gen. Tau vis. pT (GeV)', 'ytitle':"eff. single jet (DM10)", 'sel':'ta_ispfreco==1 && ta_gen_dm==10', 'isVar':True},
    }

ensureDir('Plots')
sfile = TFile('Myroot_0.root')

# for vkey, ivar in vardict.items():

#     hists = []
#     titles = []

#     print(vkey, ivar)

#     addsel = '1'

#     hist = sproducer('hist', sfile, vkey, ivar, addsel)

#     hists.append(copy.deepcopy(hist))
#     titles.append('match')

# #    if vkey.find('d0')!=-1:
# #
# #        hist = sproducer('hist', sfile, vkey, ivar, drmatch)
# #
# #        hists.append(copy.deepcopy(hist))
# #        titles.append('match')
# #
# #        hist = sproducer('hist', sfile, vkey, ivar, '!(' + drmatch +')')
# #
# #        hists.append(copy.deepcopy(hist))
# #        titles.append('non match')
        

    
#     for ii, ihist in enumerate(hists):
#         applyHistStyle(ihist, ii)
                                                                                                                                                                             
#         ihist.Scale(1./ihist.GetSumOfWeights())
#         ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)


#     comparisonPlots(hists, titles, False, 'Plots/' + vkey + '.png', False, False, False)
        
kk=0
for vkey in order_of_keys:
    ivar = vardict[vkey]

    if(kk%2==0):
        hists = []
        titles = []

    print(vkey, ivar)

    addsel = '1'

    hist = sproducer('hist', sfile, vkey, ivar, addsel)

    hists.append(copy.deepcopy(hist))
    if kk%2==0:
        titles.append('Gen matched track')
    else:
        titles.append('Not matched track')

    if kk%2==1:
        for ii, ihist in enumerate(hists):
            applyHistStyle(ihist, ii)
            ihist.Scale(1./ihist.GetSumOfWeights())
            ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)
            ihist.SetLineColor(ii%2+1)

        #comparisonPlots(hists, titles, False, 'Plots/' + vkey + '.png', False, False, True)
        comparisonPlots(hists, titles, True, 'Plots/' + vkey + '.png', False, False, True)
    kk+=1

kk=0
for vkey in order_of_keys_z0:
    ivar = vardict[vkey]

    if(kk%2==0):
        hists = []
        titles = []

    print(vkey, ivar)

    addsel = '1'

    if(kk>1):
        hist = sproducer_w('hist', sfile, vkey, ivar, addsel)
    else:
        hist = sproducer('hist', sfile, vkey, ivar, addsel)

    hists.append(copy.deepcopy(hist))
    if kk%2==0:
        titles.append('Gen matched track')
    else:
        titles.append('No selection track')

    if kk%2==1:
        for ii, ihist in enumerate(hists):
            applyHistStyle(ihist, ii)
            #ihist.Scale(1./ihist.GetSumOfWeights())
            ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)
            ihist.SetLineColor(ii%2+1)

        #comparisonPlots(hists, titles, False, 'Plots/' + vkey + '.png', False, False, True)
        if(kk<2):
            comparisonPlots(hists, titles, True, 'Plots/' + vkey + '.png', False, False, True)
        else:
            comparisonPlots(hists, titles, True, 'Plots/' + vkey + '_weight.png', False, False, True)

    kk+=1
        

kk=0
for vkey, ivar in effvardict.items():

    hists = []
    titles = []

    print(vkey, ivar)

    addsel = '1'

    hist = effproducer('hist', sfile, vkey, ivar, addsel)
    hists.append(copy.deepcopy(hist))
    if kk%2==0:
        titles.append('Gen matched track')
    else:
        titles.append('No selection track')

    #for ii, ihist in enumerate(hists):
    #    applyHistStyle(ihist, ii)
        
    comparisonPlots(hists, titles, False, 'Plots/' + vkey + '.png', True, False, False)
    kk+=1


