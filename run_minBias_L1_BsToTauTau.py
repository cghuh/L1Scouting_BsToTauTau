import os, math, sys
import time
from DeltaR import returndR
import copy
import random
from ROOT import *
import ROOT
import argparse

from officialStyle import officialStyle

ROOT.gROOT.SetBatch(True)
officialStyle(gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def Plots(hists, titles, isLog=False, pname='sync.pdf', isScale = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
    #hists.SetMaximum(8)
    if isScale:
        hists.Scale(1./hists.GetSumOfWeights())
        hists.GetYaxis().SetRangeUser(1e-4,2)
    if isLog:
        c1.SetLogy()
    hists.Draw('ep')
    c1.Print(pname)
    #ofile.cd()
    #c1.Write()

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
    #ofile.cd()
    #c1.Write()

def comparisonPlot2D(hist1, hist2, titles, isLog=False, pname='sync.pdf', isGen = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
    #ROOT.gPad.SetRightMargin(0.15)
    if isLog:
        c1.SetLogz()
    hist1.SetMarkerSize(1)
    hist2.SetMarkerSize(1)
    if isGen == True:
        hist1.SetMarkerSize(1.5)
    hist1.SetMarkerColor(1)
    hist2.SetMarkerColor(2)
    hist1.Draw()
    hist2.Draw('same')
    if isLegend:
        leg = ROOT.TLegend(0.65, 0.90, 0.9, 0.97)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        if isGen == True:
            leg.AddEntry(hist1, "TTrack", 'p')
            leg.AddEntry(hist2, "Gen #pi", 'p')
        else:
            leg.AddEntry(hist1, "Total", 'p')
            leg.AddEntry(hist2, "Gen Matched", 'p')
        leg.Draw()
    c1.Print(pname)
    #ofile.cd()
    #c1.Write()

def comparisonPlots2D(hist1, hist2, hist3, titles, isLog=False, pname='sync.pdf', isGen = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",700,700)
    #ROOT.gPad.SetRightMargin(0.15)
    if isLog:
        c1.SetLogz()
    hist1.SetMarkerSize(0.9)
    hist2.SetMarkerSize(3.0)
    hist3.SetMarkerSize(3.0)
    hist2.SetMarkerStyle(29)
    hist3.SetMarkerStyle(29)
    if isGen == True:
        hist1.SetMarkerSize(1.5)
    hist1.SetMarkerColor(1)
    hist2.SetMarkerColor(2)
    hist3.SetMarkerColor(4)
    hist1.Draw()
    hist2.Draw('same')
    hist3.Draw('same')
    if isLegend:
        leg = ROOT.TLegend(0.65, 0.87, 0.9, 0.97)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.AddEntry(hist1, "Total", 'p')
        leg.AddEntry(hist2, "#pi^{+} Matched", 'p')
        leg.AddEntry(hist3, "#pi^{-} Matched", 'p')
        leg.Draw()
    c1.Print(pname)
    #ofile.cd()
    #c1.Write()
    hist1.SetMarkerSize(1)
    hist2.SetMarkerSize(1)
    hist3.SetMarkerSize(1)
    hist2.SetMarkerStyle(1)
    hist3.SetMarkerStyle(1)

def comparisonPlot3D(hist1, hist2, hist3, titles, isLog=False, pname='sync.pdf', isGen = False, isRatio=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = TCanvas(cname,"",1400,700)
    #c1.GetView().RotateView(30, 115)
    c1.SetPhi(20)
    c1.SetTheta(20)
    #ROOT.gPad.SetRightMargin(0.15)
    hist1.GetZaxis().SetNdivisions(506)
    hist1.GetZaxis().SetTitleOffset(0.8)
    hist1.SetMarkerSize(0.9)
    hist2.SetMarkerSize(3.0)
    hist3.SetMarkerSize(3.0)
    hist2.SetMarkerStyle(29)
    hist3.SetMarkerStyle(29)
    hist1.SetMarkerColor(1)
    hist2.SetMarkerColor(2)
    hist3.SetMarkerColor(4)
    hist1.Draw()
    hist2.Draw('same')
    hist3.Draw('same')
    if isLegend:
        leg = ROOT.TLegend(0.65, 0.86, 0.9, 0.97)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.AddEntry(hist1, "Total", 'p')
        leg.AddEntry(hist2, "#pi^{+} Matched", 'p')
        leg.AddEntry(hist3, "#pi^{-} Matched", 'p')
        leg.Draw()
    c1.Print(pname)
    #ofile.cd()
    #c1.Write()
    hist1.SetMarkerSize(1)
    hist2.SetMarkerSize(1)
    hist3.SetMarkerSize(1)
    hist2.SetMarkerStyle(1)
    hist3.SetMarkerStyle(1)

def comparisonPlots(hist1, hist2, isLog=False, pname='sync.pdf', isScale = False, isGen=False, isLegend=False):
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
        hist1.GetYaxis().SetRangeUser(1e-4,2)
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.SetLineColor(1)
    hist1.SetMarkerColor(1)
    hist1.Draw('ep')
    hist2.Draw('epsame')
    if isLegend:
        leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
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
            leg.AddEntry(hist2, "Gen Matched", 'lp')
        leg.Draw()

    c1.Print(pname)
    #ofile.cd()
    #c1.Write()

def comparison3Plots(hist1, hist2, hist3, isLog=False, pname='sync.pdf', isScale = False, isPipm=False, isLegend=False):
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
        hist3.GetYaxis().SetRangeUser(1e-4,2)
    if "MVA" in str(hist1.GetName()):
        hist3.GetXaxis().SetRangeUser(0.98,1)
    hist3.SetLineColor(1)
    hist3.SetMarkerColor(1)
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.SetLineColor(4)
    hist1.SetMarkerColor(4)
    hist3.Draw('ep')
    hist2.Draw('epsame')
    hist1.Draw('epsame')
    if isLegend:
        leg = ROOT.TLegend(0.40, 0.68, 0.9, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        if isPipm:
            leg.AddEntry(hist3, "Total", 'p')
            leg.AddEntry(hist2, "#pi^{+} Matched", 'p')
            leg.AddEntry(hist1, "#pi^{-} Matched", 'p')
        else:
            leg.AddEntry(hist1, "BsToTauTau PU0", 'lp')
            leg.AddEntry(hist2, "BsToTauTau PU200", 'lp')
            leg.AddEntry(hist3, "MinBias", 'lp')
        leg.Draw()
    c1.Print(pname)
    #ofile.cd()
    #c1.Write()

h_MinBias_trk_dR         = ROOT.TH1F("h_MinBias_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_iso        = ROOT.TH1F("h_MinBias_trk_iso",";min #Delta R_{TTracks}",100,0,2)
h_MinBias_trk_pt         = ROOT.TH1F("h_MinBias_trk_pt",";p_{T} [GeV]",100,0,20)
h_MinBias_trk_eta        = ROOT.TH1F("h_MinBias_trk_eta",";#eta",50,-2.5,2.5)
h_MinBias_trk_phi        = ROOT.TH1F("h_MinBias_trk_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_d0         = ROOT.TH1F("h_MinBias_trk_d0",";d0",50,-2.5,2.5)
h_MinBias_trk_z0         = ROOT.TH1F("h_MinBias_trk_z0",";z",300,-15,15)
h_MinBias_trk_nstub      = ROOT.TH1F("h_MinBias_trk_nstub",";nstub",8,2,10)
h_MinBias_trk_chi2dof    = ROOT.TH1F("h_MinBias_trk_chi2dof",";#chi^{2}/dof",100,0,20)
h_MinBias_trk_chi2rphi   = ROOT.TH1F("h_MinBias_trk_chi2rphi",";#chi^{2}rphi",100,0,20)
h_MinBias_trk_chi2rz     = ROOT.TH1F("h_MinBias_trk_chi2rz",";#chi^{2}rz",100,0,10)
h_MinBias_trk_bendchi2   = ROOT.TH1F("h_MinBias_trk_bendchi2",";bend #chi^{2}",100,0,10)
h_MinBias_trk_hitpattern = ROOT.TH1F("h_MinBias_trk_hitpattern",";hitpattern",130,0,130)
h_MinBias_trk_MVA1       = ROOT.TH1F("h_MinBias_trk_MVA1",";MVA1",5000,0,1)

cnt_acc = 0
cnt_acc_match = 0
    
nct=0

titles = []
titles.append('6pi TTrack')

start_time = time.time()


nct=0
start_time = time.time()
npu = 'minBias'
ensureDir('Plots'+str(npu)+'')
file = ROOT.TFile.Open('/eos/user/c/chuh/l1p2/MinBias_TuneCP5_14TeV-pythia8_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')
tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
tree.SetBranchStatus('trk_*', 1)
Nevt = tree.GetEntries()
print('Total Number of events = ', Nevt)

#Nevt = 10000
for evt in range(Nevt):
    tree.GetEntry(evt)

    if evt%1000==0: 
        time_elapsed = time.time() - start_time
        print('{0:.2f}'.format(float(evt)/float(Nevt)*100.), '% processed ', '{0:.2f}'.format(float(evt)/float(time_elapsed)), 'Hz')

    sumpt=0
    cnt1=0
    cnt2=0
    for itrk in range(len(tree.trk_pt)):
        dRmin = 999.
        dRiso = 999.
        flag=-1
        for jtrk in range(len(tree.trk_pt)):
            sumpt += tree.trk_pt[jtrk] 
            if itrk == jtrk:
                continue
            dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
            if dR < dRiso:
                dRiso = dR

        cnt2+=1
        
        #h_MinBias_trk_dR.Fill(dRmin)
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
file.Close()

ofile = ROOT.TFile("output.root", "RECREATE")
#h_MinBias_trk_dR.Write()
h_MinBias_trk_iso.Write()
h_MinBias_trk_pt.Write()
h_MinBias_trk_eta.Write()
h_MinBias_trk_phi.Write()
h_MinBias_trk_d0.Write()
h_MinBias_trk_nstub.Write()
h_MinBias_trk_chi2dof.Write()
h_MinBias_trk_chi2rphi.Write()
h_MinBias_trk_chi2rz.Write()
h_MinBias_trk_bendchi2.Write()
h_MinBias_trk_MVA1.Write()

ofile.Close()
