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

    display = DisplayManager(pname, isLog, isRatio, 0.6, 0.7)
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
    
    hprof = hist.ProfileX()
    hprof.SetMaximum(ivar['ymax'])
    hprof.SetMinimum(ivar['ymin'])
    hprof.GetXaxis().SetTitle(ivar['xtitle'])
    hprof.GetYaxis().SetTitle(ivar['ytitle'])
    hprof.GetYaxis().SetNdivisions(506)

    if name.find('eff')!=-1:
        hprof.SetMaximum(1.2)
        hprof.SetMinimum(0)

    if name.find('res')!=-1:

        hprof.SetMaximum(1.)
        hprof.SetMinimum(-1.)

    return copy.deepcopy(hprof)




acc = 'abs(gen_eta) < 2.3'
drmatch = 'dr > 0 && dr < 0.02'

vardict = {
    'ntrk':{'tree':'tree', 'var':'gen_ntrk', 'nbin':30, 'xmin':0, 'xmax':30., 'title':"# of tracks", 'sel':'1'},
    'pt_gen':{'tree':'tree', 'var':'gen_pt', 'nbin':50, 'xmin':0, 'xmax':10, 'title':"gen. pT (GeV)", 'sel':'1'},
    'eta_gen':{'tree':'tree', 'var':'gen_eta', 'nbin':50, 'xmin':-7, 'xmax':7, 'title':"gen. eta", 'sel':'1'},
    'phi_gen':{'tree':'tree', 'var':'gen_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"gen. phi", 'sel':'1'},
    'z0_gen':{'tree':'tree', 'var':'gen_z0', 'nbin':100, 'xmin':-50, 'xmax':50, 'title':"gen. z0", 'sel':'1'},

    'pt_trk':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':'1'},
    'eta_trk':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':'1'},
    'phi_trk':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':'1'},
    'd0_trk':{'tree':'tree', 'var':'trk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':'1'},
    'z0_trk':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':'1'},
    'nstub_trk':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':'1'},
    'chi2dof_trk':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':'1'},
    'chi2rphi_trk':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':'1'},
    'chi2rz_trk':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':'1'},
    'bendchi2_trk':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':'1'},
    'fake_trk':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':'1'},
    'pdgid_trk':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track fake", 'sel':'1'},


    'pt_faketrk':{'tree':'tree', 'var':'faketrk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':'1'},
    'eta_faketrk':{'tree':'tree', 'var':'faketrk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':'1'},
    'phi_faketrk':{'tree':'tree', 'var':'faketrk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':'1'},
    'd0_faketrk':{'tree':'tree', 'var':'faketrk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':'1'},
    'z0_faketrk':{'tree':'tree', 'var':'faketrk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':'1'},
    'nstub_faketrk':{'tree':'tree', 'var':'faketrk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':'1'},
    'chi2dof_faketrk':{'tree':'tree', 'var':'faketrk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':'1'},
    'chi2rphi_faketrk':{'tree':'tree', 'var':'faketrk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':'1'},
    'chi2rz_faketrk':{'tree':'tree', 'var':'faketrk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':'1'},
    'bendchi2_faketrk':{'tree':'tree', 'var':'faketrk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':'1'},
    'fake_faketrk':{'tree':'tree', 'var':'faketrk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':'1'},
    'pdgid_faketrk':{'tree':'tree', 'var':'faketrk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track fake", 'sel':'1'},

    #'pt_res':{'tree':'tree', 'var':'(trk_pt - gen_pt)/gen_pt', 'nbin':50, 'xmin':-0.1, 'xmax':0.1, 'title':"pT resolution", 'sel':drmatch + '&&' + acc},
    #'z0_res':{'tree':'tree', 'var':'trk_z0 - gen_z0', 'nbin':50, 'xmin':-1., 'xmax':1., 'title':"z0 resolution", 'sel':drmatch + '&&' + acc},

    }

var2dict = {
    'pt_trk':{'tree':'tree', 'var':'trk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':'1'},
    'pt_faketrk':{'tree':'tree', 'var':'faketrk_pt', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track pT (GeV)", 'sel':'1'},
    'eta_trk':{'tree':'tree', 'var':'trk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':'1'},
    'eta_faketrk':{'tree':'tree', 'var':'faketrk_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track eta", 'sel':'1'},
    'phi_trk':{'tree':'tree', 'var':'trk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':'1'},
    'phi_faketrk':{'tree':'tree', 'var':'faketrk_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':"track phi", 'sel':'1'},
    'd0_trk':{'tree':'tree', 'var':'trk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':'1'},
    'd0_faketrk':{'tree':'tree', 'var':'faketrk_d0', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':"track d0", 'sel':'1'},
    'z0_trk':{'tree':'tree', 'var':'trk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':'1'},
    'z0_faketrk':{'tree':'tree', 'var':'faketrk_z0', 'nbin':40, 'xmin':-20, 'xmax':20, 'title':"track z0", 'sel':'1'},
    'nstub_trk':{'tree':'tree', 'var':'trk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':'1'},
    'nstub_faketrk':{'tree':'tree', 'var':'faketrk_nstub', 'nbin':7, 'xmin':0, 'xmax':7, 'title':"track nstub", 'sel':'1'},
    'chi2dof_trk':{'tree':'tree', 'var':'trk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':'1'},
    'chi2dof_faketrk':{'tree':'tree', 'var':'faketrk_chi2dof', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2/dof", 'sel':'1'},
    'chi2rphi_trk':{'tree':'tree', 'var':'trk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':'1'},
    'chi2rphi_faketrk':{'tree':'tree', 'var':'faketrk_chi2rphi', 'nbin':100, 'xmin':0, 'xmax':50, 'title':"track #chi^2rphi", 'sel':'1'},
    'chi2rz_trk':{'tree':'tree', 'var':'trk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':'1'},
    'chi2rz_faketrk':{'tree':'tree', 'var':'faketrk_chi2rz', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track #chi^2rz", 'sel':'1'},
    'bendchi2_trk':{'tree':'tree', 'var':'trk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':'1'},
    'bendchi2_faketrk':{'tree':'tree', 'var':'faketrk_bendchi2', 'nbin':100, 'xmin':0, 'xmax':20, 'title':"track bend #chi^2", 'sel':'1'},
    'fake_trk':{'tree':'tree', 'var':'trk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':'1'},
    'fake_faketrk':{'tree':'tree', 'var':'faketrk_fake', 'nbin':2, 'xmin':0, 'xmax':2, 'title':"track fake", 'sel':'1'},
    'pdgid_trk':{'tree':'tree', 'var':'trk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track fake", 'sel':'1'},
    'pdgid_faketrk':{'tree':'tree', 'var':'faketrk_matchtp_pdgid', 'nbin':6800, 'xmin':-3400, 'xmax':3400, 'title':"track fake", 'sel':'1'},
    }



effvardict = {
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
for vkey, ivar in var2dict.items():

    if(kk%2==0):
        hists = []
        titles = []

    print(vkey, ivar)

    addsel = '1'

    hist = sproducer('hist', sfile, vkey, ivar, addsel)

    hists.append(copy.deepcopy(hist))
    titles.append('match')

    if kk%2==1:
        for ii, ihist in enumerate(hists):
            applyHistStyle(ihist, ii)
            ihist.Scale(1./ihist.GetSumOfWeights())
            ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)
            ihist.SetLineColor(ii%2+1)

        comparisonPlots(hists, titles, False, 'Plots/' + vkey + '.png', False, False, False)
    kk+=1
        

for vkey, ivar in effvardict.items():

    hists = []
    titles = []

    print(vkey, ivar)

#    sfile = TFile('output_B2DstarTauNu_20180502/Myroot.root')

    addsel = '1'

#    if ivar['tree']=='ta_tree':
#        addsel = 'ta_jtype==0'

    
    hist = effproducer('hist', sfile, vkey, ivar, addsel)
    hists.append(copy.deepcopy(hist))
    titles.append('ak4chs')

    for ii, ihist in enumerate(hists):
        applyHistStyle(ihist, ii)
        
    comparisonPlots(hists, titles, False, 'Plots/' + vkey + '.pdf', True, False, False)


