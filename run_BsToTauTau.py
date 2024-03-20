import os, math, sys
import time
#from ROOT import TFile, TH1F, gROOT, TTree, Double, TChain, TLorentzVector, TVector3
#import numpy as num

from distutils.ccompiler import gen_lib_options
#from TreeProducerBcJpsiTauNu import *
from DeltaR import returndR
import copy
import random
#import numpy as np
from ROOT import *
import ROOT
from DisplayManager import DisplayManager

from officialStyle import officialStyle

ROOT.gROOT.SetBatch(True)
officialStyle(gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

#npu = 200
npu = 'minBias'
#arg = sys.argv[1]

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def Plots(hists, titles, isLog=False, pname='sync.pdf', isScale = False, isRatio=False, isLegend=False):
    c1 = TCanvas("c1","",900,900)
    hists.SetMaximum(8)
    if isScale:
        hists.Scale(1./hists.GetSumOfWeights())
        hists.GetYaxis().SetRangeUser(1e-4,2)
    if isLog:
        c1.SetLogy()
    hists.Draw('ep')
    c1.Print(pname)

def Plot2D(hists, titles, isLog=False, pname='sync.pdf', isEff = False, isRatio=False, isLegend=False):
    c1 = TCanvas("c1","",900,900)
    ROOT.gPad.SetRightMargin(0.15)
    if isLog:
        c1.SetLogz()
    hists.Draw()
    c1.Print(pname)

def comparisonPlot2D(hist1, hist2, titles, isLog=False, pname='sync.pdf', isEff = False, isRatio=False, isLegend=False):
    c1 = TCanvas("c1","",900,900)
    #ROOT.gPad.SetRightMargin(0.15)
    if isLog:
        c1.SetLogz()
    hist1.SetMarkerSize(1)
    hist2.SetMarkerSize(1.5)
    hist2.SetMarkerColor(2)
    #hist1.GetXaxis().SetRangeUser(-2.5,2.5)
    #hist1.GetYaxis().SetRangeUser(-math.pi,math.pi)
    hist2.Draw()
    hist1.Draw('same')
    if isLegend:
        leg = ROOT.TLegend(0.75, 0.85, 0.9, 0.97)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.AddEntry(hist1, "TTrack", 'p')
        leg.AddEntry(hist2, "Gen #pi", 'p')
        leg.Draw()
    c1.Print(pname)

def comparisonPlots(hist1, hist2, isLog=False, pname='sync.pdf', isScale = False, isGen=False, isLegend=False):
    c1 = TCanvas("c1","",700,700)
    hist1.SetMaximum(8)
    if isLog:
        c1.SetLogy()
    if isScale:
        hist1.Scale(1./hist1.GetSumOfWeights())
        hist2.Scale(1./hist2.GetSumOfWeights())
        hist1.GetYaxis().SetRangeUser(1e-4,2)
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.Draw('ep')
    hist2.Draw('epsame')
    if isLegend:
        leg = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        if isGen:
            leg.AddEntry(hist1, "Gen", 'lp')
            leg.AddEntry(hist2, "TTrack", 'lp')
        else:
            leg.AddEntry(hist1, "Total", 'lp')
            leg.AddEntry(hist2, "Gen Matching", 'lp')
        leg.Draw()

    c1.Print(pname)

#from optparse import OptionParser, OptionValueError
#usage = "usage: python runTauDisplay_BsTauTau.py"
#parser = OptionParser(usage)

#parser.add_option("-o", "--out", default='Myroot.root', type="string", help="output filename", dest="out")

#(options, args) = parser.parse_args()


ensureDir('Plots'+str(npu)+'')

#output='Myroot_' + str(npu) + '.root'

#out = TreeProducerBcJpsiTauNu(output, 'mc')

if(npu == 'minBias'):
    #file = ROOT.TFile.Open('/eos/cms/store/group/phys_bphys/ytakahas/l1p2/125X_cc7/MinBias_TuneCP5_14TeV-pythia8_GTT_20240217/MinBias_TuneCP5_14TeV-pythia8_GTT.root')
    #file = ROOT.TFile.Open('/eos/cms/store/group/phys_bphys/ytakahas/l1p2/125X_cc7/MinBias_TuneCP5_14TeV-pythia8_GTT_20240217/MinBias_TuneCP5_14TeV-pythia8.batch1.job'+str(arg)+'_GTT.root')
    file = ROOT.TFile.Open('MinBias_TuneCP5_14TeV-pythia8_GTT.root')
else:
    file = ROOT.TFile.Open('Tau3pi_PY8_PU'+ str(npu) + '_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')


tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
#tree.SetBranchStatus('trk_*', 1)
tree.SetBranchStatus('trk_*', 1)

Nevt = tree.GetEntries()

print('Total Number of events = ', Nevt)
evtid = 0

htrk_dR         = ROOT.TH1F("htrk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
htrk_iso        = ROOT.TH1F("htrk_iso",";min #Delta R_{TTracks}",100,0,2)
htrk_pt         = ROOT.TH1F("htrk_pt",";pT [GeV]",100,0,20)
htrk_eta        = ROOT.TH1F("htrk_eta",";eta",50,-2.5,2.5)
htrk_phi        = ROOT.TH1F("htrk_phi",";phi",50,-math.pi,math.pi)
htrk_d0         = ROOT.TH1F("htrk_d0",";d0",50,-2.5,2.5)
htrk_z0         = ROOT.TH1F("htrk_z0",";z0",160,-20,20)
htrk_nstub      = ROOT.TH1F("htrk_nstub",";nstub",8,2,10)
htrk_chi2dof    = ROOT.TH1F("htrk_chi2dof",";{#chi}^{2}/dof",100,0,50)
htrk_chi2rphi   = ROOT.TH1F("htrk_chi2rphi",";{#chi}^{2}rphi",100,0,50)
htrk_chi2rz     = ROOT.TH1F("htrk_chi2rz",";{#chi}^{2}rz",100,0,20)
htrk_bendchi2   = ROOT.TH1F("htrk_bendchi2",";bend {#chi}^{2}",100,0,20)
htrk_hitpattern = ROOT.TH1F("htrk_hitpattern",";hitpattern",130,0,130)
htrk_MVA1       = ROOT.TH1F("htrk_MVA1",";MVA1",100,0,1)
#htrk_ = ROOT.TH1F("htrk_",";",100,0,20)
htrk_match_dR         = ROOT.TH1F("htrk_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
htrk_match_iso        = ROOT.TH1F("htrk_match_iso",";min #Delta R_{TTracks}",100,0,2)
htrk_match_pt         = ROOT.TH1F("htrk_match_pt",";pT [GeV]",100,0,20)
htrk_match_eta        = ROOT.TH1F("htrk_match_eta",";eta",50,-2.5,2.5)
htrk_match_phi        = ROOT.TH1F("htrk_match_phi",";phi",50,-math.pi,math.pi)
htrk_match_d0         = ROOT.TH1F("htrk_match_d0",";d0",50,-2.5,2.5)
htrk_match_z0         = ROOT.TH1F("htrk_match_z0",";z0",400,-20,20)
htrk_match_nstub      = ROOT.TH1F("htrk_match_nstub",";nstub",8,2,10)
htrk_match_chi2dof    = ROOT.TH1F("htrk_match_chi2dof",";#chi^{2}/dof",100,0,50)
htrk_match_chi2rphi   = ROOT.TH1F("htrk_match_chi2rphi",";#chi^{2}rphi",100,0,50)
htrk_match_chi2rz     = ROOT.TH1F("htrk_match_chi2rz",";#chi^{2}rz",100,0,20)
htrk_match_bendchi2   = ROOT.TH1F("htrk_match_bendchi2",";bend #chi^{2}",100,0,20)
htrk_match_hitpattern = ROOT.TH1F("htrk_match_hitpattern",";hitpattern",130,0,130)
htrk_match_MVA1       = ROOT.TH1F("htrk_match_MVA1",";MVA1",100,0,1)

if npu == 0:
    htrk_nTTrack    = ROOT.TH1F("htrk_nTTrack",";N_{TTrack}",19,1,20)
    htrk_match_nTTrack    = ROOT.TH1F("htrk_match_nTTrack",";N_{TTrack}",19,1,20)
else:
    htrk_nTTrack    = ROOT.TH1F("htrk_nTTrack",";N_{TTrack}",209,1,210)
    htrk_match_nTTrack    = ROOT.TH1F("htrk_match_nTTrack",";N_{TTrack}",209,1,210)

if npu == 0:
    htrk_z0_weight_match= ROOT.TH1F("htrk_z0_weight_match",";z0",400,-1,1)
    htrk_z0_weight_all  = ROOT.TH1F("htrk_z0_weight_all",";z0",400,-1,1)
else:
    htrk_z0_weight_match= ROOT.TH1F("htrk_z0_weight_match",";z0",400,-0.1,0.1)
    htrk_z0_weight_all  = ROOT.TH1F("htrk_z0_weight_all",";z0",400,-0.1,0.1)
# htrk_z0_match       = ROOT.TH1F("htrk_z0_match",";z0",40,-2,2)
# htrk_z0_all         = ROOT.TH1F("htrk_z0_all",";z0",40,-2,2)

htrk_phi_eta       = ROOT.TH2F("htrk_phi_eta",";eta;phi",100,-2.5,2.5,100,-math.pi,math.pi)
htrk_match_phi_eta = ROOT.TH2F("htrk_match_phi_eta",";eta;phi",100,-2.5,2.5,100,-math.pi,math.pi)
hgen_phi_eta = ROOT.TH2F("htrk_gen_phi_eta",";eta;phi",100,-2.5,2.5,100,-math.pi,math.pi)

htrk_phi_eta_weight       = ROOT.TH2F("htrk_phi_eta_weight",";eta;phi",100,-2.5,2.5,100,-math.pi,math.pi)
htrk_match_phi_eta_weight = ROOT.TH2F("htrk_match_phi_eta_weight",";eta;phi",100,-2.5,2.5,100,-math.pi,math.pi)

hgen_z0         = ROOT.TH1F("hgen_z0",";z0",400,-20,20)
hdiff_z0 = ROOT.TH1F("hdiff_z0",";Gen z0 - TTrack z0",200,-10,10)
hdiff_pt = ROOT.TH1F("hdiff_pt",";Gen p_{T} - TTrack p_{T}",100,-5,5)

cnt_acc = 0
cnt_acc_match = 0
    
count1=0
count2=0
nct=0

titles = []
titles.append('6pi TTrack')

start_time = time.time()

Nevt = 1000
for evt in range(Nevt):
    tree.GetEntry(evt)

    if evt%100==0: 
        time_elapsed = time.time() - start_time
        print('{0:.2f}'.format(float(evt)/float(Nevt)*100.), '% processed ', '{0:.2f}'.format(float(evt)/float(time_elapsed)), 'Hz')

    flag_acc = True
    flag_match = True
    npi = 0
    if not npu == 'minBias':
        for igen in range(len(tree.gen_pt)):
            if (tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                npi += 1
        if (npi == 6):
            nct += 1
        elif not (npu == 'minBias'):
            continue
    
    sumpt=0
    cnt1=0
    cnt2=0
    for itrk in range(len(tree.trk_pt)):
        dRmin = 999.
        dRiso = 999.
        flag=-1
        for igen in range(len(tree.gen_pt)):
            if (tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
                if dR < dRmin:
                    dRmin = dR
                    gen_pt = tree.gen_pt[igen]
                    gen_eta = tree.gen_eta[igen]
                    gen_phi = tree.gen_phi[igen]
                    gen_z0 = tree.gen_z0[igen]

        for jtrk in range(len(tree.trk_pt)):
            sumpt += tree.trk_pt[jtrk] 
            if itrk == jtrk:
                continue
            dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
            if dR < dRiso:
                dRiso = dR

        cnt2+=1
        if dRmin < 0.02:
            flag = 1
            count1+=1
            cnt1+=1
            htrk_match_dR.Fill(dRmin)
            htrk_match_iso.Fill(dRiso)
            htrk_match_pt.Fill(tree.trk_pt[itrk])
            htrk_match_eta.Fill(tree.trk_eta[itrk])
            htrk_match_phi.Fill(tree.trk_phi[itrk])
            htrk_match_d0.Fill(tree.trk_d0[itrk])
            htrk_match_z0.Fill(tree.trk_z0[itrk])
            htrk_match_nstub.Fill(tree.trk_nstub[itrk])
            htrk_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
            htrk_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            htrk_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
            htrk_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
            htrk_match_hitpattern.Fill(tree.trk_hitpattern[itrk])
            htrk_match_MVA1.Fill(tree.trk_MVA1[itrk])
            if not npu == 'minBias':
                htrk_z0_weight_match.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
                htrk_match_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                htrk_match_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
                hgen_phi_eta.Fill(gen_eta, gen_phi)
                hgen_z0.Fill(gen_z0)
                hdiff_z0.Fill(gen_z0-tree.trk_z0[itrk])
                hdiff_pt.Fill(gen_pt-tree.trk_pt[itrk])
        elif dRmin == 999:
            flag=-1
        else:
            flag=0
            count2+=1
        
        htrk_dR.Fill(dRmin)
        htrk_iso.Fill(dRiso)
        htrk_pt.Fill(tree.trk_pt[itrk])
        htrk_eta.Fill(tree.trk_eta[itrk])
        htrk_phi.Fill(tree.trk_phi[itrk])
        htrk_d0.Fill(tree.trk_d0[itrk])
        htrk_z0.Fill(tree.trk_z0[itrk])
        htrk_nstub.Fill(tree.trk_nstub[itrk])
        htrk_chi2dof.Fill(tree.trk_chi2dof[itrk])
        htrk_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
        htrk_chi2rz.Fill(tree.trk_chi2rz[itrk])
        htrk_bendchi2.Fill(tree.trk_bendchi2[itrk])
        htrk_hitpattern.Fill(tree.trk_hitpattern[itrk])
        htrk_MVA1.Fill(tree.trk_MVA1[itrk])
        if not npu == 'minBias':
            htrk_z0_weight_all.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
            htrk_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
            htrk_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)

        #if cnt1 >= 6:
        #    break

    #Plot2D(htrk_phi_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_phi_eta.GetName() +str(evt)+'.png', False, False, False)
    #Plot2D(htrk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
    #Plot2D(htrk_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + htrk_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
    #Plot2D(htrk_match_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + htrk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
    if not (npu == 'minBias'):
        comparisonPlot2D(htrk_match_phi_eta, hgen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlot2D(htrk_match_phi_eta_weight, hgen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlots(hgen_z0, htrk_match_z0, False, 'Plots'+str(npu)+'/compare_' + hgen_z0.GetName() +str(evt)+ '.png', False, True, True)
        Plots(hdiff_pt, titles, False, 'Plots'+str(npu)+'/' + hdiff_pt.GetName() +str(evt)+ '.png', False, False, False)
        Plots(hdiff_z0, titles, False, 'Plots'+str(npu)+'/' + hdiff_z0.GetName() +str(evt)+ '.png', False, False, False)
        htrk_phi_eta.Reset()
        htrk_match_phi_eta.Reset()
        htrk_phi_eta_weight.Reset()
        htrk_match_phi_eta_weight.Reset()
        hgen_phi_eta.Reset()
        htrk_z0_weight_all.Reset()
        hgen_z0.Reset()
        htrk_match_z0.Reset()
        hdiff_z0.Reset()
        hdiff_pt.Reset()

    htrk_nTTrack.Fill(len(tree.trk_pt))
    htrk_match_nTTrack.Fill(cnt1)

# Plots(htrk_dR, titles, False, 'Plots'+str(npu)+'/' + htrk_dR.GetName() + '.png', False, False, False)
# Plots(htrk_iso, titles, False, 'Plots'+str(npu)+'/' + htrk_iso.GetName() + '.png', False, False, False)
# Plots(htrk_pt, titles, False, 'Plots'+str(npu)+'/' + htrk_pt.GetName() + '.png', False, False, False)
# Plots(htrk_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_eta.GetName() + '.png', False, False, False)
# Plots(htrk_phi, titles, False, 'Plots'+str(npu)+'/' + htrk_phi.GetName() + '.png', False, False, False)
# #Plots(htrk_d0, titles, False, 'Plots'+str(npu)+'/' + htrk_d0.GetName() + '.png', False, False, False)
# Plots(htrk_z0, titles, False, 'Plots'+str(npu)+'/' + htrk_z0.GetName() + '.png', False, False, False)
# Plots(htrk_nstub, titles, False, 'Plots'+str(npu)+'/' + htrk_nstub.GetName() + '.png', False, False, False)
# Plots(htrk_chi2dof, titles, False, 'Plots'+str(npu)+'/' + htrk_chi2dof.GetName() + '.png', False, False, False)
# Plots(htrk_chi2rphi, titles, False, 'Plots'+str(npu)+'/' + htrk_chi2rphi.GetName() + '.png', False, False, False)
# Plots(htrk_chi2rz, titles, False, 'Plots'+str(npu)+'/' + htrk_chi2rz.GetName() + '.png', False, False, False)
# Plots(htrk_bendchi2, titles, False, 'Plots'+str(npu)+'/' + htrk_bendchi2.GetName() + '.png', False, False, False)
# Plots(htrk_hitpattern, titles, False, 'Plots'+str(npu)+'/' + htrk_hitpattern.GetName() + '.png', False, False, False)
# Plots(htrk_MVA1, titles, False, 'Plots'+str(npu)+'/' + htrk_MVA1.GetName() + '.png', False, False, False)
# Plots(htrk_nTTrack, titles, False, 'Plots'+str(npu)+'/' + htrk_nTTrack.GetName() + '.png', False, False, False)

comparisonPlots(htrk_dR, htrk_match_dR, True, 'Plots'+str(npu)+'/compare_' + htrk_dR.GetName() + '.png', True, False, True)
comparisonPlots(htrk_iso, htrk_match_iso, True, 'Plots'+str(npu)+'/compare_' + htrk_iso.GetName() + '.png', True, False, True)
comparisonPlots(htrk_pt, htrk_match_pt, True, 'Plots'+str(npu)+'/compare_' + htrk_pt.GetName() + '.png', True, False, True)
comparisonPlots(htrk_eta, htrk_match_eta, True, 'Plots'+str(npu)+'/compare_' + htrk_eta.GetName() + '.png', True, False, True)
comparisonPlots(htrk_phi, htrk_match_phi, True, 'Plots'+str(npu)+'/compare_' + htrk_phi.GetName() + '.png', True, False, True)
#comparisonPlots(htrk_d0, htrk_match_d0, True, 'Plots'+str(npu)+'/compare_' + htrk_d0.GetName() + '.png', True, False, True)
if npu == 'minBias':
    comparisonPlots(htrk_z0, htrk_match_z0, True, 'Plots'+str(npu)+'/compare_' + htrk_z0.GetName() + '.png', True, False, True)
comparisonPlots(htrk_nstub, htrk_match_nstub, True, 'Plots'+str(npu)+'/compare_' + htrk_nstub.GetName() + '.png', True, False, True)
comparisonPlots(htrk_chi2dof, htrk_match_chi2dof, True, 'Plots'+str(npu)+'/compare_' + htrk_chi2dof.GetName() + '.png', True, False, True)
comparisonPlots(htrk_chi2rphi, htrk_match_chi2rphi, True, 'Plots'+str(npu)+'/compare_' + htrk_chi2rphi.GetName() + '.png', True, False, True)
comparisonPlots(htrk_chi2rz, htrk_match_chi2rz, True, 'Plots'+str(npu)+'/compare_' + htrk_chi2rz.GetName() + '.png', True, False, True)
comparisonPlots(htrk_bendchi2, htrk_match_bendchi2, True, 'Plots'+str(npu)+'/compare_' + htrk_bendchi2.GetName() + '.png', True, False, True)
comparisonPlots(htrk_hitpattern, htrk_match_hitpattern, True, 'Plots'+str(npu)+'/compare_' + htrk_hitpattern.GetName() + '.png', True, False, True)
comparisonPlots(htrk_MVA1, htrk_match_MVA1, True, 'Plots'+str(npu)+'/compare_' + htrk_MVA1.GetName() + '.png', True, False, True)
comparisonPlots(htrk_nTTrack, htrk_match_nTTrack, True, 'Plots'+str(npu)+'/compare_' + htrk_nTTrack.GetName() + '.png', True, False, True)
#comparisonPlots(hists, titles, False, 'Plots'+str(npu)+'/' + hists.GetName() + '.png', False, False, False)
        

#Plot2D(htrk_phi_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_phi_eta.GetName() + '.png', False, False, False)
#Plot2D(htrk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + htrk_match_phi_eta.GetName() + '.png', False, False, False)
#Plot2D(htrk_phi_eta_weight, titles, True, 'Plots'+str(npu)+'/' + htrk_phi_eta_weight.GetName() + '.png', False, False, False)
#Plot2D(htrk_match_phi_eta_weight, titles, True, 'Plots'+str(npu)+'/' + htrk_match_phi_eta_weight.GetName() + '.png', False, False, False)

print(nct)
print(count1, 'matched ', count2, 'not matched')
#print(Nevt, 'evt processed.', cnt_acc, 'evt has detector acc. (', float(cnt_acc/Nevt), ')' )
#print(Nevt, 'evt processed.', cnt_acc_match, 'evt has detector acc. and matching (', float(cnt_acc_match/Nevt), ')' )

#out.endJob()
