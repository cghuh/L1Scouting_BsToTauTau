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
ofile = ROOT.TFile("output.root", "RECREATE")

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def Plots(hists, titles, isLog=False, pname='sync.pdf', isScale = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
    hists.SetMaximum(8)
    if isScale:
        hists.Scale(1./hists.GetSumOfWeights())
        hists.GetYaxis().SetRangeUser(1e-4,2)
    if isLog:
        c1.SetLogy()
    hists.Draw('ep')
    c1.Print(pname)
    ofile.cd()
    c1.Write()

def Plot2D(hists, titles, isLog=False, pname='sync.pdf', isEff = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
    ROOT.gPad.SetRightMargin(0.15)
    if isLog:
        c1.SetLogz()
    hists.Draw()
    c1.Print(pname)
    ofile.cd()
    c1.Write()

def comparisonPlot2D(hist1, hist2, titles, isLog=False, pname='sync.pdf', isEff = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
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
    ofile.cd()
    c1.Write()

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
    ofile.cd()
    c1.Write()

def comparison3Plots(hist1, hist2, hist3, isLog=False, pname='sync.pdf', isScale = False, isGen=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
    hist1.SetMaximum(8)
    if isLog:
        c1.SetLogy()
    if isScale:
        hist1.Scale(1./hist1.GetSumOfWeights())
        hist2.Scale(1./hist2.GetSumOfWeights())
        hist3.Scale(1./hist3.GetSumOfWeights())
        hist1.GetYaxis().SetRangeUser(1e-4,2)
    if "MVA" in str(hist1.GetName()):
        hist1.GetXaxis().SetRangeUser(0.98,1)
    hist3.SetLineColor(1)
    hist3.SetMarkerColor(1)
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.SetLineColor(4)
    hist1.SetMarkerColor(4)
    hist1.Draw('ep')
    hist2.Draw('epsame')
    hist3.Draw('epsame')
    if isLegend:
        leg = ROOT.TLegend(0.40, 0.68, 0.9, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.AddEntry(hist1, "BsToTauTau PU0", 'lp')
        leg.AddEntry(hist2, "BsToTauTau PU200", 'lp')
        leg.AddEntry(hist3, "MinBias", 'lp')
        leg.Draw()
    c1.Print(pname)
    ofile.cd()
    c1.Write()

h_0_trk_dR         = ROOT.TH1F("h_0_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_iso        = ROOT.TH1F("h_0_trk_iso",";min #Delta R_{TTracks}",100,0,2)
h_0_trk_pt         = ROOT.TH1F("h_0_trk_pt",";p_{T} [GeV]",100,0,20)
h_0_trk_eta        = ROOT.TH1F("h_0_trk_eta",";#eta",50,-2.5,2.5)
h_0_trk_phi        = ROOT.TH1F("h_0_trk_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_d0         = ROOT.TH1F("h_0_trk_d0",";d0",50,-2.5,2.5)
h_0_trk_z0         = ROOT.TH1F("h_0_trk_z0",";z0",160,-20,20)
h_0_trk_nstub      = ROOT.TH1F("h_0_trk_nstub",";nstub",8,2,10)
h_0_trk_chi2dof    = ROOT.TH1F("h_0_trk_chi2dof",";#chi^{2}/dof",100,0,20)
h_0_trk_chi2rphi   = ROOT.TH1F("h_0_trk_chi2rphi",";#chi^{2}rphi",100,0,20)
h_0_trk_chi2rz     = ROOT.TH1F("h_0_trk_chi2rz",";#chi^{2}rz",100,0,10)
h_0_trk_bendchi2   = ROOT.TH1F("h_0_trk_bendchi2",";bend #chi^{2}",100,0,10)
h_0_trk_hitpattern = ROOT.TH1F("h_0_trk_hitpattern",";hitpattern",130,0,130)
h_0_trk_MVA1       = ROOT.TH1F("h_0_trk_MVA1",";MVA1",1000,0,1)
h_0_trk_match_dR         = ROOT.TH1F("h_0_trk_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_match_iso        = ROOT.TH1F("h_0_trk_match_iso",";min #Delta R_{TTracks}",100,0,2)
h_0_trk_match_pt         = ROOT.TH1F("h_0_trk_match_pt",";p_{T} [GeV]",100,0,20)
h_0_trk_match_eta        = ROOT.TH1F("h_0_trk_match_eta",";#eta",50,-2.5,2.5)
h_0_trk_match_phi        = ROOT.TH1F("h_0_trk_match_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_match_d0         = ROOT.TH1F("h_0_trk_match_d0",";d0",50,-2.5,2.5)
h_0_trk_match_z0         = ROOT.TH1F("h_0_trk_match_z0",";z0",400,-20,20)
h_0_trk_match_nstub      = ROOT.TH1F("h_0_trk_match_nstub",";nstub",8,2,10)
h_0_trk_match_chi2dof    = ROOT.TH1F("h_0_trk_match_chi2dof",";#chi^{2}/dof",100,0,20)
h_0_trk_match_chi2rphi   = ROOT.TH1F("h_0_trk_match_chi2rphi",";#chi^{2}rphi",100,0,20)
h_0_trk_match_chi2rz     = ROOT.TH1F("h_0_trk_match_chi2rz",";#chi^{2}rz",100,0,10)
h_0_trk_match_bendchi2   = ROOT.TH1F("h_0_trk_match_bendchi2",";bend #chi^{2}",100,0,10)
h_0_trk_match_hitpattern = ROOT.TH1F("h_0_trk_match_hitpattern",";hitpattern",130,0,130)
h_0_trk_match_MVA1       = ROOT.TH1F("h_0_trk_match_MVA1",";MVA1",1000,0,1)
h_0_trk_z0_weight_match= ROOT.TH1F("h_0_trk_z0_weight_match",";z0",400,-1,1)
h_0_trk_z0_weight_all  = ROOT.TH1F("h_0_trk_z0_weight_all",";z0",400,-1,1)

h_0_trk_phi_eta       = ROOT.TH2F("h_0_trk_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_trk_match_phi_eta = ROOT.TH2F("h_0_trk_match_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_gen_phi_eta = ROOT.TH2F("h_0_trk_gen_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_0_trk_phi_eta_weight       = ROOT.TH2F("h_0_trk_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_trk_match_phi_eta_weight = ROOT.TH2F("h_0_trk_match_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_0_gen_z0         = ROOT.TH1F("h_0_gen_z0",";z0",400,-20,20)
h_0_diff_z0 = ROOT.TH1F("h_0_diff_z0",";Gen z0 - TTrack z0",200,-10,10)
h_0_diff_pt = ROOT.TH1F("h_0_diff_pt",";Gen p_{T} - TTrack p_{T}",100,-5,5)

h_200_trk_dR         = ROOT.TH1F("h_200_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_iso        = ROOT.TH1F("h_200_trk_iso",";min #Delta R_{TTracks}",100,0,2)
h_200_trk_pt         = ROOT.TH1F("h_200_trk_pt",";p_{T} [GeV]",100,0,20)
h_200_trk_eta        = ROOT.TH1F("h_200_trk_eta",";#eta",50,-2.5,2.5)
h_200_trk_phi        = ROOT.TH1F("h_200_trk_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_d0         = ROOT.TH1F("h_200_trk_d0",";d0",50,-2.5,2.5)
h_200_trk_z0         = ROOT.TH1F("h_200_trk_z0",";z0",160,-20,20)
h_200_trk_nstub      = ROOT.TH1F("h_200_trk_nstub",";nstub",8,2,10)
h_200_trk_chi2dof    = ROOT.TH1F("h_200_trk_chi2dof",";#chi^{2}/dof",100,0,20)
h_200_trk_chi2rphi   = ROOT.TH1F("h_200_trk_chi2rphi",";#chi^{2}rphi",100,0,20)
h_200_trk_chi2rz     = ROOT.TH1F("h_200_trk_chi2rz",";#chi^{2}rz",100,0,10)
h_200_trk_bendchi2   = ROOT.TH1F("h_200_trk_bendchi2",";bend #chi^{2}",100,0,10)
h_200_trk_hitpattern = ROOT.TH1F("h_200_trk_hitpattern",";hitpattern",130,0,130)
h_200_trk_MVA1       = ROOT.TH1F("h_200_trk_MVA1",";MVA1",1000,0,1)
h_200_trk_match_dR         = ROOT.TH1F("h_200_trk_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_match_iso        = ROOT.TH1F("h_200_trk_match_iso",";min #Delta R_{TTracks}",100,0,2)
h_200_trk_match_pt         = ROOT.TH1F("h_200_trk_match_pt",";p_{T} [GeV]",100,0,20)
h_200_trk_match_eta        = ROOT.TH1F("h_200_trk_match_eta",";#eta",50,-2.5,2.5)
h_200_trk_match_phi        = ROOT.TH1F("h_200_trk_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_match_d0         = ROOT.TH1F("h_200_trk_match_d0",";d0",50,-2.5,2.5)
h_200_trk_match_z0         = ROOT.TH1F("h_200_trk_match_z0",";z0",400,-20,20)
h_200_trk_match_nstub      = ROOT.TH1F("h_200_trk_match_nstub",";nstub",8,2,10)
h_200_trk_match_chi2dof    = ROOT.TH1F("h_200_trk_match_chi2dof",";#chi^{2}/dof",100,0,20)
h_200_trk_match_chi2rphi   = ROOT.TH1F("h_200_trk_match_chi2rphi",";#chi^{2}rphi",100,0,20)
h_200_trk_match_chi2rz     = ROOT.TH1F("h_200_trk_match_chi2rz",";#chi^{2}rz",100,0,10)
h_200_trk_match_bendchi2   = ROOT.TH1F("h_200_trk_match_bendchi2",";bend #chi^{2}",100,0,10)
h_200_trk_match_hitpattern = ROOT.TH1F("h_200_trk_match_hitpattern",";hitpattern",130,0,130)
h_200_trk_match_MVA1       = ROOT.TH1F("h_200_trk_match_MVA1",";MVA1",1000,0,1)

h_200_trk_z0_weight_match= ROOT.TH1F("h_200_trk_z0_weight_match",";z0",400,-0.1,0.1)
h_200_trk_z0_weight_all  = ROOT.TH1F("h_200_trk_z0_weight_all",";z0",400,-0.1,0.1)

h_200_trk_phi_eta       = ROOT.TH2F("h_200_trk_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_trk_match_phi_eta = ROOT.TH2F("h_200_trk_match_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_gen_phi_eta = ROOT.TH2F("h_200_trk_gen_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_200_trk_phi_eta_weight       = ROOT.TH2F("h_200_trk_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_trk_match_phi_eta_weight = ROOT.TH2F("h_200_trk_match_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_200_gen_z0         = ROOT.TH1F("h_200_gen_z0",";z0",400,-20,20)
h_200_diff_z0 = ROOT.TH1F("h_200_diff_z0",";Gen z0 - TTrack z0",200,-10,10)
h_200_diff_pt = ROOT.TH1F("h_200_diff_pt",";Gen p_{T} - TTrack p_{T}",100,-5,5)

h_MinBias_trk_dR         = ROOT.TH1F("h_MinBias_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_iso        = ROOT.TH1F("h_MinBias_trk_iso",";min #Delta R_{TTracks}",100,0,2)
h_MinBias_trk_pt         = ROOT.TH1F("h_MinBias_trk_pt",";p_{T} [GeV]",100,0,20)
h_MinBias_trk_eta        = ROOT.TH1F("h_MinBias_trk_eta",";#eta",50,-2.5,2.5)
h_MinBias_trk_phi        = ROOT.TH1F("h_MinBias_trk_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_d0         = ROOT.TH1F("h_MinBias_trk_d0",";d0",50,-2.5,2.5)
h_MinBias_trk_z0         = ROOT.TH1F("h_MinBias_trk_z0",";z0",160,-20,20)
h_MinBias_trk_nstub      = ROOT.TH1F("h_MinBias_trk_nstub",";nstub",8,2,10)
h_MinBias_trk_chi2dof    = ROOT.TH1F("h_MinBias_trk_chi2dof",";#chi^{2}/dof",100,0,20)
h_MinBias_trk_chi2rphi   = ROOT.TH1F("h_MinBias_trk_chi2rphi",";#chi^{2}rphi",100,0,20)
h_MinBias_trk_chi2rz     = ROOT.TH1F("h_MinBias_trk_chi2rz",";#chi^{2}rz",100,0,10)
h_MinBias_trk_bendchi2   = ROOT.TH1F("h_MinBias_trk_bendchi2",";bend #chi^{2}",100,0,10)
h_MinBias_trk_hitpattern = ROOT.TH1F("h_MinBias_trk_hitpattern",";hitpattern",130,0,130)
h_MinBias_trk_MVA1       = ROOT.TH1F("h_MinBias_trk_MVA1",";MVA1",5000,0,1)
h_MinBias_trk_match_dR         = ROOT.TH1F("h_MinBias_trk_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_match_iso        = ROOT.TH1F("h_MinBias_trk_match_iso",";min #Delta R_{TTracks}",100,0,2)
h_MinBias_trk_match_pt         = ROOT.TH1F("h_MinBias_trk_match_pt",";p_{T} [GeV]",100,0,20)
h_MinBias_trk_match_eta        = ROOT.TH1F("h_MinBias_trk_match_eta",";#eta",50,-2.5,2.5)
h_MinBias_trk_match_phi        = ROOT.TH1F("h_MinBias_trk_match_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_match_d0         = ROOT.TH1F("h_MinBias_trk_match_d0",";d0",50,-2.5,2.5)
h_MinBias_trk_match_z0         = ROOT.TH1F("h_MinBias_trk_match_z0",";z0",400,-20,20)
h_MinBias_trk_match_nstub      = ROOT.TH1F("h_MinBias_trk_match_nstub",";nstub",8,2,10)
h_MinBias_trk_match_chi2dof    = ROOT.TH1F("h_MinBias_trk_match_chi2dof",";#chi^{2}/dof",100,0,20)
h_MinBias_trk_match_chi2rphi   = ROOT.TH1F("h_MinBias_trk_match_chi2rphi",";#chi^{2}rphi",100,0,20)
h_MinBias_trk_match_chi2rz     = ROOT.TH1F("h_MinBias_trk_match_chi2rz",";#chi^{2}rz",100,0,10)
h_MinBias_trk_match_bendchi2   = ROOT.TH1F("h_MinBias_trk_match_bendchi2",";bend #chi^{2}",100,0,10)
h_MinBias_trk_match_hitpattern = ROOT.TH1F("h_MinBias_trk_match_hitpattern",";hitpattern",130,0,130)
h_MinBias_trk_match_MVA1       = ROOT.TH1F("h_MinBias_trk_match_MVA1",";MVA1",5000,0,1)

h_MinBias_trk_z0_weight_match= ROOT.TH1F("h_MinBias_trk_z0_weight_match",";z0",400,-0.1,0.1)
h_MinBias_trk_z0_weight_all  = ROOT.TH1F("h_MinBias_trk_z0_weight_all",";z0",400,-0.1,0.1)

h_MinBias_trk_phi_eta       = ROOT.TH2F("h_MinBias_trk_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_MinBias_trk_match_phi_eta = ROOT.TH2F("h_MinBias_trk_match_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_MinBias_gen_phi_eta = ROOT.TH2F("h_MinBias_trk_gen_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_MinBias_trk_phi_eta_weight       = ROOT.TH2F("h_MinBias_trk_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_MinBias_trk_match_phi_eta_weight = ROOT.TH2F("h_MinBias_trk_match_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_MinBias_gen_z0         = ROOT.TH1F("h_MinBias_gen_z0",";z0",400,-20,20)
h_MinBias_diff_z0 = ROOT.TH1F("h_MinBias_diff_z0",";Gen z0 - TTrack z0",200,-10,10)
h_MinBias_diff_pt = ROOT.TH1F("h_MinBias_diff_pt",";Gen p_{T} - TTrack p_{T}",100,-5,5)

cnt_acc = 0
cnt_acc_match = 0
    
nct=0

titles = []
titles.append('6pi TTrack')

start_time = time.time()
npu = 0
ensureDir('Plots'+str(npu)+'')
file = ROOT.TFile.Open('Tau3pi_PY8_PU'+ str(npu) + '_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')
tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
tree.SetBranchStatus('trk_*', 1)
Nevt = tree.GetEntries()
print('Total Number of events = ', Nevt)

for evt in range(Nevt):
    tree.GetEntry(evt)

    if evt%10000==0: 
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
            cnt1+=1
            h_0_trk_match_dR.Fill(dRmin)
            h_0_trk_match_iso.Fill(dRiso)
            h_0_trk_match_pt.Fill(tree.trk_pt[itrk])
            h_0_trk_match_eta.Fill(tree.trk_eta[itrk])
            h_0_trk_match_phi.Fill(tree.trk_phi[itrk])
            h_0_trk_match_d0.Fill(tree.trk_d0[itrk])
            h_0_trk_match_z0.Fill(tree.trk_z0[itrk])
            h_0_trk_match_nstub.Fill(tree.trk_nstub[itrk])
            h_0_trk_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_0_trk_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_0_trk_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_0_trk_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_0_trk_match_hitpattern.Fill(tree.trk_hitpattern[itrk])
            h_0_trk_match_MVA1.Fill(tree.trk_MVA1[itrk])
            if not npu == 'minBias':
                h_0_trk_z0_weight_match.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
                h_0_trk_match_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                h_0_trk_match_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
                h_0_gen_phi_eta.Fill(gen_eta, gen_phi)
                h_0_gen_z0.Fill(gen_z0)
                h_0_diff_z0.Fill(gen_z0-tree.trk_z0[itrk])
                h_0_diff_pt.Fill(gen_pt-tree.trk_pt[itrk])
        
        h_0_trk_dR.Fill(dRmin)
        h_0_trk_iso.Fill(dRiso)
        h_0_trk_pt.Fill(tree.trk_pt[itrk])
        h_0_trk_eta.Fill(tree.trk_eta[itrk])
        h_0_trk_phi.Fill(tree.trk_phi[itrk])
        h_0_trk_d0.Fill(tree.trk_d0[itrk])
        h_0_trk_z0.Fill(tree.trk_z0[itrk])
        h_0_trk_nstub.Fill(tree.trk_nstub[itrk])
        h_0_trk_chi2dof.Fill(tree.trk_chi2dof[itrk])
        h_0_trk_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
        h_0_trk_chi2rz.Fill(tree.trk_chi2rz[itrk])
        h_0_trk_bendchi2.Fill(tree.trk_bendchi2[itrk])
        h_0_trk_hitpattern.Fill(tree.trk_hitpattern[itrk])
        h_0_trk_MVA1.Fill(tree.trk_MVA1[itrk])
        if not npu == 'minBias':
            h_0_trk_z0_weight_all.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
            h_0_trk_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
            h_0_trk_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
            if cnt1 >= 6:
                break

    if not (npu == 'minBias'):
        Plot2D(h_0_trk_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_phi_eta.GetName() +str(evt)+'.png', False, False, False)
        Plot2D(h_0_trk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        Plot2D(h_0_trk_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
        Plot2D(h_0_trk_match_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot2D(h_0_trk_match_phi_eta, h_0_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlot2D(h_0_trk_match_phi_eta_weight, h_0_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlots(h_0_gen_z0, h_0_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_0_gen_z0.GetName() +str(evt)+ '.png', False, True, True)
        Plots(h_0_diff_pt, titles, False, 'Plots'+str(npu)+'/' + h_0_diff_pt.GetName() +str(evt)+ '.png', False, False, False)
        Plots(h_0_diff_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_diff_z0.GetName() +str(evt)+ '.png', False, False, False)
        h_0_trk_phi_eta.Reset()
        h_0_trk_match_phi_eta.Reset()
        h_0_trk_phi_eta_weight.Reset()
        h_0_trk_match_phi_eta_weight.Reset()
        h_0_gen_phi_eta.Reset()
        h_0_trk_z0_weight_all.Reset()
        h_0_gen_z0.Reset()
        h_0_trk_match_z0.Reset()
        h_0_diff_z0.Reset()
        h_0_diff_pt.Reset()

comparisonPlots(h_0_trk_dR, h_0_trk_match_dR, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_dR.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_iso, h_0_trk_match_iso, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_iso.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_pt, h_0_trk_match_pt, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_pt.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_eta, h_0_trk_match_eta, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_eta.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_phi, h_0_trk_match_phi, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_phi.GetName() + '.png', True, False, True)
if npu == 'minBias':
    comparisonPlots(h_0_trk_z0, h_0_trk_match_z0, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_z0.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_nstub, h_0_trk_match_nstub, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_nstub.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_chi2dof, h_0_trk_match_chi2dof, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_chi2dof.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_chi2rphi, h_0_trk_match_chi2rphi, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_chi2rphi.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_chi2rz, h_0_trk_match_chi2rz, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_chi2rz.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_bendchi2, h_0_trk_match_bendchi2, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_bendchi2.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_hitpattern, h_0_trk_match_hitpattern, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_hitpattern.GetName() + '.png', True, False, True)
comparisonPlots(h_0_trk_MVA1, h_0_trk_match_MVA1, True, 'Plots'+str(npu)+'/compare_' + h_0_trk_MVA1.GetName() + '.png', True, False, True)
        
print(nct)
file.Close()

nct=0
start_time = time.time()
npu = 200
ensureDir('Plots'+str(npu)+'')
file = ROOT.TFile.Open('Tau3pi_PY8_PU'+ str(npu) + '_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')
tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
tree.SetBranchStatus('trk_*', 1)
Nevt = tree.GetEntries()
print('Total Number of events = ', Nevt)

for evt in range(Nevt):
    tree.GetEntry(evt)

    if evt%10000==0: 
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
            cnt1+=1
            h_200_trk_match_dR.Fill(dRmin)
            h_200_trk_match_iso.Fill(dRiso)
            h_200_trk_match_pt.Fill(tree.trk_pt[itrk])
            h_200_trk_match_eta.Fill(tree.trk_eta[itrk])
            h_200_trk_match_phi.Fill(tree.trk_phi[itrk])
            h_200_trk_match_d0.Fill(tree.trk_d0[itrk])
            h_200_trk_match_z0.Fill(tree.trk_z0[itrk])
            h_200_trk_match_nstub.Fill(tree.trk_nstub[itrk])
            h_200_trk_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_200_trk_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_200_trk_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_200_trk_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_200_trk_match_hitpattern.Fill(tree.trk_hitpattern[itrk])
            h_200_trk_match_MVA1.Fill(tree.trk_MVA1[itrk])
            if not npu == 'minBias':
                h_200_trk_z0_weight_match.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
                h_200_trk_match_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                h_200_trk_match_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
                h_200_gen_phi_eta.Fill(gen_eta, gen_phi)
                h_200_gen_z0.Fill(gen_z0)
                h_200_diff_z0.Fill(gen_z0-tree.trk_z0[itrk])
                h_200_diff_pt.Fill(gen_pt-tree.trk_pt[itrk])
        
        h_200_trk_dR.Fill(dRmin)
        h_200_trk_iso.Fill(dRiso)
        h_200_trk_pt.Fill(tree.trk_pt[itrk])
        h_200_trk_eta.Fill(tree.trk_eta[itrk])
        h_200_trk_phi.Fill(tree.trk_phi[itrk])
        h_200_trk_d0.Fill(tree.trk_d0[itrk])
        h_200_trk_z0.Fill(tree.trk_z0[itrk])
        h_200_trk_nstub.Fill(tree.trk_nstub[itrk])
        h_200_trk_chi2dof.Fill(tree.trk_chi2dof[itrk])
        h_200_trk_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
        h_200_trk_chi2rz.Fill(tree.trk_chi2rz[itrk])
        h_200_trk_bendchi2.Fill(tree.trk_bendchi2[itrk])
        h_200_trk_hitpattern.Fill(tree.trk_hitpattern[itrk])
        h_200_trk_MVA1.Fill(tree.trk_MVA1[itrk])
        if not npu == 'minBias':
            h_200_trk_z0_weight_all.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
            h_200_trk_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
            h_200_trk_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
            if cnt1 >= 6:
                break

    if not (npu == 'minBias'):
        Plot2D(h_200_trk_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_phi_eta.GetName() +str(evt)+'.png', False, False, False)
        Plot2D(h_200_trk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        Plot2D(h_200_trk_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
        Plot2D(h_200_trk_match_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot2D(h_200_trk_match_phi_eta, h_200_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlot2D(h_200_trk_match_phi_eta_weight, h_200_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlots(h_200_gen_z0, h_200_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_200_gen_z0.GetName() +str(evt)+ '.png', False, True, True)
        Plots(h_200_diff_pt, titles, False, 'Plots'+str(npu)+'/' + h_200_diff_pt.GetName() +str(evt)+ '.png', False, False, False)
        Plots(h_200_diff_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_diff_z0.GetName() +str(evt)+ '.png', False, False, False)
        h_200_trk_phi_eta.Reset()
        h_200_trk_match_phi_eta.Reset()
        h_200_trk_phi_eta_weight.Reset()
        h_200_trk_match_phi_eta_weight.Reset()
        h_200_gen_phi_eta.Reset()
        h_200_trk_z0_weight_all.Reset()
        h_200_gen_z0.Reset()
        h_200_trk_match_z0.Reset()
        h_200_diff_z0.Reset()
        h_200_diff_pt.Reset()

comparisonPlots(h_200_trk_dR, h_200_trk_match_dR, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_dR.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_iso, h_200_trk_match_iso, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_iso.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_pt, h_200_trk_match_pt, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_pt.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_eta, h_200_trk_match_eta, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_eta.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_phi, h_200_trk_match_phi, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_phi.GetName() + '.png', True, False, True)
#comparisonPlots(h_200_trk_d0, h_200_trk_match_d0, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_d0.GetName() + '.png', True, False, True)
if npu == 'minBias':
    comparisonPlots(h_200_trk_z0, h_200_trk_match_z0, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_z0.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_nstub, h_200_trk_match_nstub, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_nstub.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_chi2dof, h_200_trk_match_chi2dof, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_chi2dof.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_chi2rphi, h_200_trk_match_chi2rphi, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_chi2rphi.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_chi2rz, h_200_trk_match_chi2rz, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_chi2rz.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_bendchi2, h_200_trk_match_bendchi2, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_bendchi2.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_hitpattern, h_200_trk_match_hitpattern, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_hitpattern.GetName() + '.png', True, False, True)
comparisonPlots(h_200_trk_MVA1, h_200_trk_match_MVA1, True, 'Plots'+str(npu)+'/compare_' + h_200_trk_MVA1.GetName() + '.png', True, False, True)
#comparisonPlots(hists, titles, False, 'Plots'+str(npu)+'/' + hists.GetName() + '.png', False, False, False)
        
print(nct)
file.Close()

nct=0
start_time = time.time()
npu = 'minBias'
ensureDir('Plots'+str(npu)+'')
file = ROOT.TFile.Open('MinBias_TuneCP5_14TeV-pythia8_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')
tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
tree.SetBranchStatus('trk_*', 1)
Nevt = tree.GetEntries()
print('Total Number of events = ', Nevt)

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
            cnt1+=1
            h_MinBias_trk_match_dR.Fill(dRmin)
            h_MinBias_trk_match_iso.Fill(dRiso)
            h_MinBias_trk_match_pt.Fill(tree.trk_pt[itrk])
            h_MinBias_trk_match_eta.Fill(tree.trk_eta[itrk])
            h_MinBias_trk_match_phi.Fill(tree.trk_phi[itrk])
            h_MinBias_trk_match_d0.Fill(tree.trk_d0[itrk])
            h_MinBias_trk_match_z0.Fill(tree.trk_z0[itrk])
            h_MinBias_trk_match_nstub.Fill(tree.trk_nstub[itrk])
            h_MinBias_trk_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_MinBias_trk_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_MinBias_trk_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_MinBias_trk_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_MinBias_trk_match_hitpattern.Fill(tree.trk_hitpattern[itrk])
            h_MinBias_trk_match_MVA1.Fill(tree.trk_MVA1[itrk])
            if not npu == 'minBias':
                h_MinBias_trk_z0_weight_match.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
                h_MinBias_trk_match_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                h_MinBias_trk_match_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
                h_MinBias_gen_phi_eta.Fill(gen_eta, gen_phi)
                h_MinBias_gen_z0.Fill(gen_z0)
                h_MinBias_diff_z0.Fill(gen_z0-tree.trk_z0[itrk])
                h_MinBias_diff_pt.Fill(gen_pt-tree.trk_pt[itrk])
        
        h_MinBias_trk_dR.Fill(dRmin)
        h_MinBias_trk_iso.Fill(dRiso)
        h_MinBias_trk_pt.Fill(tree.trk_pt[itrk])
        h_MinBias_trk_eta.Fill(tree.trk_eta[itrk])
        h_MinBias_trk_phi.Fill(tree.trk_phi[itrk])
        h_MinBias_trk_d0.Fill(tree.trk_d0[itrk])
        h_MinBias_trk_z0.Fill(tree.trk_z0[itrk])
        h_MinBias_trk_nstub.Fill(tree.trk_nstub[itrk])
        h_MinBias_trk_chi2dof.Fill(tree.trk_chi2dof[itrk])
        h_MinBias_trk_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
        h_MinBias_trk_chi2rz.Fill(tree.trk_chi2rz[itrk])
        h_MinBias_trk_bendchi2.Fill(tree.trk_bendchi2[itrk])
        h_MinBias_trk_hitpattern.Fill(tree.trk_hitpattern[itrk])
        h_MinBias_trk_MVA1.Fill(tree.trk_MVA1[itrk])
        if not npu == 'minBias':
            h_MinBias_trk_z0_weight_all.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
            h_MinBias_trk_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
            h_MinBias_trk_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
            if cnt1 >= 6:
                break

    if not (npu == 'minBias'):
        Plot2D(h_MinBias_trk_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_trk_phi_eta.GetName() +str(evt)+'.png', False, False, False)
        Plot2D(h_MinBias_trk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        Plot2D(h_MinBias_trk_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_trk_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
        Plot2D(h_MinBias_trk_match_phi_eta_weight, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_trk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot2D(h_MinBias_trk_match_phi_eta, h_MinBias_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlot2D(h_MinBias_trk_match_phi_eta_weight, h_MinBias_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_trk_match_phi_eta_weight.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlots(h_MinBias_gen_z0, h_MinBias_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_MinBias_gen_z0.GetName() +str(evt)+ '.png', False, True, True)
        Plots(h_MinBias_diff_pt, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_diff_pt.GetName() +str(evt)+ '.png', False, False, False)
        Plots(h_MinBias_diff_z0, titles, False, 'Plots'+str(npu)+'/' + h_MinBias_diff_z0.GetName() +str(evt)+ '.png', False, False, False)
        h_MinBias_trk_phi_eta.Reset()
        h_MinBias_trk_match_phi_eta.Reset()
        h_MinBias_trk_phi_eta_weight.Reset()
        h_MinBias_trk_match_phi_eta_weight.Reset()
        h_MinBias_gen_phi_eta.Reset()
        h_MinBias_trk_z0_weight_all.Reset()
        h_MinBias_gen_z0.Reset()
        h_MinBias_trk_match_z0.Reset()
        h_MinBias_diff_z0.Reset()
        h_MinBias_diff_pt.Reset()

comparisonPlots(h_MinBias_trk_dR, h_MinBias_trk_match_dR, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_dR.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_iso, h_MinBias_trk_match_iso, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_iso.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_pt, h_MinBias_trk_match_pt, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_pt.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_eta, h_MinBias_trk_match_eta, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_eta.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_phi, h_MinBias_trk_match_phi, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_phi.GetName() + '.png', True, False, True)
#comparisonPlots(h_MinBias_trk_d0, h_MinBias_trk_match_d0, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_d0.GetName() + '.png', True, False, True)
if npu == 'minBias':
    comparisonPlots(h_MinBias_trk_z0, h_MinBias_trk_match_z0, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_z0.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_nstub, h_MinBias_trk_match_nstub, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_nstub.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_chi2dof, h_MinBias_trk_match_chi2dof, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_chi2dof.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_chi2rphi, h_MinBias_trk_match_chi2rphi, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_chi2rphi.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_chi2rz, h_MinBias_trk_match_chi2rz, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_chi2rz.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_bendchi2, h_MinBias_trk_match_bendchi2, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_bendchi2.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_hitpattern, h_MinBias_trk_match_hitpattern, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_hitpattern.GetName() + '.png', True, False, True)
comparisonPlots(h_MinBias_trk_MVA1, h_MinBias_trk_match_MVA1, True, 'Plots'+str(npu)+'/compare_' + h_MinBias_trk_MVA1.GetName() + '.png', True, False, True)
#comparisonPlots(hists, titles, False, 'Plots'+str(npu)+'/' + hists.GetName() + '.png', False, False, False)
        
file.Close()

ensureDir('Plots_compare')
comparison3Plots(h_0_trk_match_dR, h_200_trk_match_dR, h_MinBias_trk_dR, True, 'Plots_compare/compares_'+h_0_trk_match_dR.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_iso, h_200_trk_match_iso, h_MinBias_trk_iso, True, 'Plots_compare/compares_'+h_0_trk_match_iso.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_pt, h_200_trk_match_pt, h_MinBias_trk_pt, True, 'Plots_compare/compares_'+h_0_trk_match_pt.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_eta, h_200_trk_match_eta, h_MinBias_trk_eta, True, 'Plots_compare/compares_'+h_0_trk_match_eta.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_phi, h_200_trk_match_phi, h_MinBias_trk_phi, True, 'Plots_compare/compares_'+h_0_trk_match_phi.GetName() + '.png', True, False, True)
#comparison3Plots(h_0_trk_match_z0, h_200_trk_match_z0, h_MinBias_trk_z0, True, 'Plots_compare/compares_'+h_0_trk_match_z0.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_nstub, h_200_trk_match_nstub, h_MinBias_trk_nstub, True, 'Plots_compare/compares_'+h_0_trk_match_nstub.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_chi2dof, h_200_trk_match_chi2dof, h_MinBias_trk_chi2dof, True, 'Plots_compare/compares_'+h_0_trk_match_chi2dof.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_chi2rphi, h_200_trk_match_chi2rphi, h_MinBias_trk_chi2rphi, True, 'Plots_compare/compares_'+h_0_trk_match_chi2rphi.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_chi2rz, h_200_trk_match_chi2rz, h_MinBias_trk_chi2rz, True, 'Plots_compare/compares_'+h_0_trk_match_chi2rz.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_bendchi2, h_200_trk_match_bendchi2, h_MinBias_trk_bendchi2, True, 'Plots_compare/compares_'+h_0_trk_match_bendchi2.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_hitpattern, h_200_trk_match_hitpattern, h_MinBias_trk_hitpattern, True, 'Plots_compare/compares_'+h_0_trk_match_hitpattern.GetName() + '.png', True, False, True)
comparison3Plots(h_0_trk_match_MVA1, h_200_trk_match_MVA1, h_MinBias_trk_MVA1, True, 'Plots_compare/compares_'+h_0_trk_match_MVA1.GetName() + '.png', True, False, True)

ofile.Close()