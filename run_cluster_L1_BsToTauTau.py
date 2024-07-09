import os, math, sys
import time
from DeltaR import returndR
import copy
import random
from ROOT import *
import ROOT
import argparse
import numpy as np
from sklearn.cluster import DBSCAN

from officialStyle import officialStyle

ROOT.gROOT.SetBatch(True)
officialStyle(gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Custom spherical distance function for DBSCAN
def spherical_distance(point1, point2):
    delta_eta = point1[0] - point2[0]
    delta_phi = math.fmod(point1[1] - point2[1] + 3*math.pi, 2*math.pi) - math.pi
    delta_z = point1[2] - point2[2]
    return np.sqrt(delta_eta**2 + delta_phi**2 + delta_z**2)

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
    if hist2.Integral()+hist3.Integral() == 6:
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

def create_lorentz_vector(pt, eta, phi):
    vec = ROOT.TLorentzVector()
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    mass = 0.13957
    E = math.sqrt(px**2 + py**2 + pz**2 + mass**2)
    vec.SetPxPyPzE(px, py, pz, E)
    return vec

h_0_trk_dR         = ROOT.TH1F("h_0_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_iso        = ROOT.TH1F("h_0_trk_iso",";min #Delta R_{TTracks}",100,0,1)
h_0_trk_pt         = ROOT.TH1F("h_0_trk_pt",";p_{T} [GeV]",400,0,20)
h_0_trk_eta        = ROOT.TH1F("h_0_trk_eta",";#eta",250,2.5,2.5)
h_0_trk_phi        = ROOT.TH1F("h_0_trk_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_d0         = ROOT.TH1F("h_0_trk_d0",";d0",200,-1,1)
h_0_trk_z0         = ROOT.TH1F("h_0_trk_z0",";z",300,-15,15)
h_0_trk_nstub      = ROOT.TH1F("h_0_trk_nstub",";nstub",8,2,10)
h_0_trk_chi2dof    = ROOT.TH1F("h_0_trk_chi2dof",";#chi^{2}/dof",400,0,20)
h_0_trk_chi2rphi   = ROOT.TH1F("h_0_trk_chi2rphi",";#chi^{2}rphi",400,0,20)
h_0_trk_chi2rz     = ROOT.TH1F("h_0_trk_chi2rz",";#chi^{2}rz",200,0,10)
h_0_trk_bendchi2   = ROOT.TH1F("h_0_trk_bendchi2",";bend #chi^{2}",200,0,10)
h_0_trk_hitpattern = ROOT.TH1F("h_0_trk_hitpattern",";hitpattern",130,0,130)
h_0_trk_MVA1       = ROOT.TH1F("h_0_trk_MVA1",";MVA1",5000,0,1)
h_0_trk_match_dR         = ROOT.TH1F("h_0_trk_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_match_iso        = ROOT.TH1F("h_0_trk_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_0_trk_match_pt         = ROOT.TH1F("h_0_trk_match_pt",";p_{T} [GeV]",400,0,20)
h_0_trk_match_eta        = ROOT.TH1F("h_0_trk_match_eta",";#eta",250,2.5,2.5)
h_0_trk_match_phi        = ROOT.TH1F("h_0_trk_match_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_match_d0         = ROOT.TH1F("h_0_trk_match_d0",";d0",200,-1,1)
h_0_trk_match_z0         = ROOT.TH1F("h_0_trk_match_z0",";z",300,-15,15)
h_0_trk_match_nstub      = ROOT.TH1F("h_0_trk_match_nstub",";nstub",8,2,10)
h_0_trk_match_chi2dof    = ROOT.TH1F("h_0_trk_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_0_trk_match_chi2rphi   = ROOT.TH1F("h_0_trk_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_0_trk_match_chi2rz     = ROOT.TH1F("h_0_trk_match_chi2rz",";#chi^{2}rz",200,0,10)
h_0_trk_match_bendchi2   = ROOT.TH1F("h_0_trk_match_bendchi2",";bend #chi^{2}",200,0,10)
h_0_trk_match_hitpattern = ROOT.TH1F("h_0_trk_match_hitpattern",";hitpattern",130,0,130)
h_0_trk_match_MVA1       = ROOT.TH1F("h_0_trk_match_MVA1",";MVA1",5000,0,1)
h_0_trk_z0_weight_match= ROOT.TH1F("h_0_trk_z0_weight_match",";z",400,-1,1)
h_0_trk_z0_weight_all  = ROOT.TH1F("h_0_trk_z0_weight_all",";z",400,-1,1)
h_0_trk_pion_plus = ROOT.TH1F("h_0_trk_pion_plus",";mass",500,0,10)
h_0_trk_pion_minus = ROOT.TH1F("h_0_trk_pion_minus",";mass",500,0,10)
h_0_trk_Bs = ROOT.TH1F("h_0_trk_Bs",";mass",500,0,10)

h_0_trk_cut1_match_dR         = ROOT.TH1F("h_0_trk_cut1_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_cut1_match_iso        = ROOT.TH1F("h_0_trk_cut1_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_0_trk_cut1_match_pt         = ROOT.TH1F("h_0_trk_cut1_match_pt",";p_{T} [GeV]",400,0,20)
h_0_trk_cut1_match_eta        = ROOT.TH1F("h_0_trk_cut1_match_eta",";#eta",250,2.5,2.5)
h_0_trk_cut1_match_phi        = ROOT.TH1F("h_0_trk_cut1_match_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_cut1_match_d0         = ROOT.TH1F("h_0_trk_cut1_match_d0",";d0",200,-1,1)
h_0_trk_cut1_match_chi2dof    = ROOT.TH1F("h_0_trk_cut1_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_0_trk_cut1_match_chi2rphi   = ROOT.TH1F("h_0_trk_cut1_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_0_trk_cut1_match_chi2rz     = ROOT.TH1F("h_0_trk_cut1_match_chi2rz",";#chi^{2}rz",200,0,10)
h_0_trk_cut1_match_bendchi2   = ROOT.TH1F("h_0_trk_cut1_match_bendchi2",";bend #chi^{2}",200,0,10)
h_0_trk_cut1_match_MVA1       = ROOT.TH1F("h_0_trk_cut1_match_MVA1",";MVA1",5000,0,1)
h_0_trk_cut1_pion_plus        = ROOT.TH1F("h_0_trk_cut1_pion_plus",";mass",500,0,10)
h_0_trk_cut1_pion_minus       = ROOT.TH1F("h_0_trk_cut1_pion_minus",";mass",500,0,10)
h_0_trk_cut1_Bs               = ROOT.TH1F("h_0_trk_cut1_Bs",";mass",500,0,10)
h_0_trk_cut2_match_dR         = ROOT.TH1F("h_0_trk_cut2_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_cut2_match_iso        = ROOT.TH1F("h_0_trk_cut2_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_0_trk_cut2_match_pt         = ROOT.TH1F("h_0_trk_cut2_match_pt",";p_{T} [GeV]",400,0,20)
h_0_trk_cut2_match_eta        = ROOT.TH1F("h_0_trk_cut2_match_eta",";#eta",250,2.5,2.5)
h_0_trk_cut2_match_phi        = ROOT.TH1F("h_0_trk_cut2_match_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_cut2_match_d0         = ROOT.TH1F("h_0_trk_cut2_match_d0",";d0",200,-1,1)
h_0_trk_cut2_match_chi2dof    = ROOT.TH1F("h_0_trk_cut2_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_0_trk_cut2_match_chi2rphi   = ROOT.TH1F("h_0_trk_cut2_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_0_trk_cut2_match_chi2rz     = ROOT.TH1F("h_0_trk_cut2_match_chi2rz",";#chi^{2}rz",200,0,10)
h_0_trk_cut2_match_bendchi2   = ROOT.TH1F("h_0_trk_cut2_match_bendchi2",";bend #chi^{2}",200,0,10)
h_0_trk_cut2_match_MVA1       = ROOT.TH1F("h_0_trk_cut2_match_MVA1",";MVA1",5000,0,1)
h_0_trk_cut2_pion_plus        = ROOT.TH1F("h_0_trk_cut2_pion_plus",";mass",500,0,10)
h_0_trk_cut2_pion_minus       = ROOT.TH1F("h_0_trk_cut2_pion_minus",";mass",500,0,10)
h_0_trk_cut2_Bs               = ROOT.TH1F("h_0_trk_cut2_Bs",";mass",500,0,10)
h_0_trk_cut3_match_dR         = ROOT.TH1F("h_0_trk_cut3_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_cut3_match_iso        = ROOT.TH1F("h_0_trk_cut3_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_0_trk_cut3_match_pt         = ROOT.TH1F("h_0_trk_cut3_match_pt",";p_{T} [GeV]",400,0,20)
h_0_trk_cut3_match_eta        = ROOT.TH1F("h_0_trk_cut3_match_eta",";#eta",250,2.5,2.5)
h_0_trk_cut3_match_phi        = ROOT.TH1F("h_0_trk_cut3_match_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_cut3_match_d0         = ROOT.TH1F("h_0_trk_cut3_match_d0",";d0",200,-1,1)
h_0_trk_cut3_match_chi2dof    = ROOT.TH1F("h_0_trk_cut3_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_0_trk_cut3_match_chi2rphi   = ROOT.TH1F("h_0_trk_cut3_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_0_trk_cut3_match_chi2rz     = ROOT.TH1F("h_0_trk_cut3_match_chi2rz",";#chi^{2}rz",200,0,10)
h_0_trk_cut3_match_bendchi2   = ROOT.TH1F("h_0_trk_cut3_match_bendchi2",";bend #chi^{2}",200,0,10)
h_0_trk_cut3_match_MVA1       = ROOT.TH1F("h_0_trk_cut3_match_MVA1",";MVA1",5000,0,1)
h_0_trk_cut3_pion_plus        = ROOT.TH1F("h_0_trk_cut3_pion_plus",";mass",500,0,10)
h_0_trk_cut3_pion_minus       = ROOT.TH1F("h_0_trk_cut3_pion_minus",";mass",500,0,10)
h_0_trk_cut3_Bs               = ROOT.TH1F("h_0_trk_cut3_Bs",";mass",500,0,10)
h_0_trk_cut4_match_dR         = ROOT.TH1F("h_0_trk_cut4_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_0_trk_cut4_match_iso        = ROOT.TH1F("h_0_trk_cut4_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_0_trk_cut4_match_pt         = ROOT.TH1F("h_0_trk_cut4_match_pt",";p_{T} [GeV]",400,0,20)
h_0_trk_cut4_match_eta        = ROOT.TH1F("h_0_trk_cut4_match_eta",";#eta",250,2.5,2.5)
h_0_trk_cut4_match_phi        = ROOT.TH1F("h_0_trk_cut4_match_phi",";#phi",50,-math.pi,math.pi)
h_0_trk_cut4_match_d0         = ROOT.TH1F("h_0_trk_cut4_match_d0",";d0",200,-1,1)
h_0_trk_cut4_match_chi2dof    = ROOT.TH1F("h_0_trk_cut4_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_0_trk_cut4_match_chi2rphi   = ROOT.TH1F("h_0_trk_cut4_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_0_trk_cut4_match_chi2rz     = ROOT.TH1F("h_0_trk_cut4_match_chi2rz",";#chi^{2}rz",200,0,10)
h_0_trk_cut4_match_bendchi2   = ROOT.TH1F("h_0_trk_cut4_match_bendchi2",";bend #chi^{2}",200,0,10)
h_0_trk_cut4_match_MVA1       = ROOT.TH1F("h_0_trk_cut4_match_MVA1",";MVA1",5000,0,1)
h_0_trk_cut4_pion_plus        = ROOT.TH1F("h_0_trk_cut4_pion_plus",";mass",500,0,10)
h_0_trk_cut4_pion_minus       = ROOT.TH1F("h_0_trk_cut4_pion_minus",";mass",500,0,10)
h_0_trk_cut4_Bs               = ROOT.TH1F("h_0_trk_cut4_Bs",";mass",500,0,10)

h_0_trk_match_ntrk            = ROOT.TH1F("h_0_trk_match_ntrk",";N_{TTrack}",100,0,300)
h_0_trk_cut1_match_ntrk       = ROOT.TH1F("h_0_trk_cut1_match_ntrk",";N_{TTrack}",100,0,300)
h_0_trk_cut2_match_ntrk       = ROOT.TH1F("h_0_trk_cut2_match_ntrk",";N_{TTrack}",100,0,300)
h_0_trk_cut3_match_ntrk       = ROOT.TH1F("h_0_trk_cut3_match_ntrk",";N_{TTrack}",100,0,300)
h_0_trk_cut4_match_ntrk       = ROOT.TH1F("h_0_trk_cut4_match_ntrk",";N_{TTrack}",100,0,300)
h_200_trk_match_ntrk          = ROOT.TH1F("h_200_trk_match_ntrk",";N_{TTrack}",100,0,300)
h_200_trk_cut1_match_ntrk     = ROOT.TH1F("h_200_trk_cut1_match_ntrk",";N_{TTrack}",100,0,300)
h_200_trk_cut2_match_ntrk     = ROOT.TH1F("h_200_trk_cut2_match_ntrk",";N_{TTrack}",100,0,300)
h_200_trk_cut3_match_ntrk     = ROOT.TH1F("h_200_trk_cut3_match_ntrk",";N_{TTrack}",100,0,300)
h_200_trk_cut4_match_ntrk     = ROOT.TH1F("h_200_trk_cut4_match_ntrk",";N_{TTrack}",100,0,300)
h_MinBias_trk_match_ntrk      = ROOT.TH1F("h_MinBias_trk_match_ntrk",";N_{TTrack}",100,0,300)
h_MinBias_trk_cut1_match_ntrk = ROOT.TH1F("h_MinBias_trk_cut1_match_ntrk",";N_{TTrack}",100,0,300)
h_MinBias_trk_cut2_match_ntrk = ROOT.TH1F("h_MinBias_trk_cut2_match_ntrk",";N_{TTrack}",100,0,300)
h_MinBias_trk_cut3_match_ntrk = ROOT.TH1F("h_MinBias_trk_cut3_match_ntrk",";N_{TTrack}",100,0,300)
h_MinBias_trk_cut4_match_ntrk = ROOT.TH1F("h_MinBias_trk_cut4_match_ntrk",";N_{TTrack}",100,0,300)

h_0_trk_phi_eta       = ROOT.TH2F("h_0_trk_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_trk_match_phi_eta = ROOT.TH2F("h_0_trk_match_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_trk_match_1_phi_eta = ROOT.TH2F("h_0_trk_match_1_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_trk_match_2_phi_eta = ROOT.TH2F("h_0_trk_match_2_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_gen_phi_eta = ROOT.TH2F("h_0_trk_gen_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_0_trk_phi_eta_weight       = ROOT.TH2F("h_0_trk_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_0_trk_match_phi_eta_weight = ROOT.TH2F("h_0_trk_match_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_0_gen_z0         = ROOT.TH1F("h_0_gen_z0",";z",300,-15,15)
h_0_diff_z0 = ROOT.TH1F("h_0_diff_z0",";Gen z0 - TTrack z0",200,-10,10)
h_0_diff_pt = ROOT.TH1F("h_0_diff_pt",";Gen p_{T} - TTrack p_{T}",100,-5,5)

h_0_trk_phi_eta_z0 = ROOT.TH3F("h_0_trk_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_match_1_phi_eta_z0 = ROOT.TH3F("h_0_trk_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_match_2_phi_eta_z0 = ROOT.TH3F("h_0_trk_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_match_1_z0         = ROOT.TH1F("h_0_trk_match_1_z0",";z",300,-15,15)
h_0_trk_match_2_z0         = ROOT.TH1F("h_0_trk_match_2_z0",";z",300,-15,15)

h_0_trk_cut1_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut1_match_1_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut1_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut1_match_2_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut1_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut2_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut2_match_1_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut2_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut2_match_2_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut2_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut3_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut3_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut3_match_1_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut3_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut3_match_2_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut3_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut4_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut4_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut4_match_1_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut4_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_0_trk_cut4_match_2_phi_eta_z0 = ROOT.TH3F("h_0_trk_cut4_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut1_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut1_match_1_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut1_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut1_match_2_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut1_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut2_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut2_match_1_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut2_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut2_match_2_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut2_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut3_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut3_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut3_match_1_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut3_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut3_match_2_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut3_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut4_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut4_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut4_match_1_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut4_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_cut4_match_2_phi_eta_z0 = ROOT.TH3F("h_200_trk_cut4_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)

h_200_trk_dR         = ROOT.TH1F("h_200_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_iso        = ROOT.TH1F("h_200_trk_iso",";min #Delta R_{TTracks}",100,0,1)
h_200_trk_pt         = ROOT.TH1F("h_200_trk_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_eta        = ROOT.TH1F("h_200_trk_eta",";#eta",250,2.5,2.5)
h_200_trk_phi        = ROOT.TH1F("h_200_trk_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_d0         = ROOT.TH1F("h_200_trk_d0",";d0",200,-1,1)
h_200_trk_z0         = ROOT.TH1F("h_200_trk_z0",";z",300,-15,15)
h_200_trk_nstub      = ROOT.TH1F("h_200_trk_nstub",";nstub",8,2,10)
h_200_trk_chi2dof    = ROOT.TH1F("h_200_trk_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_chi2rphi   = ROOT.TH1F("h_200_trk_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_chi2rz     = ROOT.TH1F("h_200_trk_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_bendchi2   = ROOT.TH1F("h_200_trk_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_hitpattern = ROOT.TH1F("h_200_trk_hitpattern",";hitpattern",130,0,130)
h_200_trk_MVA1       = ROOT.TH1F("h_200_trk_MVA1",";MVA1",5000,0,1)
h_200_trk_match_dR         = ROOT.TH1F("h_200_trk_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_match_iso        = ROOT.TH1F("h_200_trk_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_200_trk_match_pt         = ROOT.TH1F("h_200_trk_match_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_match_eta        = ROOT.TH1F("h_200_trk_match_eta",";#eta",250,2.5,2.5)
h_200_trk_match_phi        = ROOT.TH1F("h_200_trk_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_match_d0         = ROOT.TH1F("h_200_trk_match_d0",";d0",200,-1,1)
h_200_trk_match_z0         = ROOT.TH1F("h_200_trk_match_z0",";z",300,-15,15)
h_200_trk_match_nstub      = ROOT.TH1F("h_200_trk_match_nstub",";nstub",8,2,10)
h_200_trk_match_chi2dof    = ROOT.TH1F("h_200_trk_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_match_chi2rphi   = ROOT.TH1F("h_200_trk_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_match_chi2rz     = ROOT.TH1F("h_200_trk_match_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_match_bendchi2   = ROOT.TH1F("h_200_trk_match_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_match_hitpattern = ROOT.TH1F("h_200_trk_match_hitpattern",";hitpattern",130,0,130)
h_200_trk_match_MVA1       = ROOT.TH1F("h_200_trk_match_MVA1",";MVA1",5000,0,1)
h_200_trk_pion_plus = ROOT.TH1F("h_200_trk_pion_plus",";mass",500,0,10)
h_200_trk_pion_minus = ROOT.TH1F("h_200_trk_pion_minus",";mass",500,0,10)
h_200_trk_Bs = ROOT.TH1F("h_200_trk_Bs",";mass",500,0,10)

h_200_trk_cut1_match_dR         = ROOT.TH1F("h_200_trk_cut1_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_cut1_match_iso        = ROOT.TH1F("h_200_trk_cut1_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_200_trk_cut1_match_pt         = ROOT.TH1F("h_200_trk_cut1_match_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_cut1_match_eta        = ROOT.TH1F("h_200_trk_cut1_match_eta",";#eta",250,2.5,2.5)
h_200_trk_cut1_match_phi        = ROOT.TH1F("h_200_trk_cut1_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_cut1_match_d0         = ROOT.TH1F("h_200_trk_cut1_match_d0",";d0",200,-1,1)
h_200_trk_cut1_match_chi2dof    = ROOT.TH1F("h_200_trk_cut1_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_cut1_match_chi2rphi   = ROOT.TH1F("h_200_trk_cut1_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_cut1_match_chi2rz     = ROOT.TH1F("h_200_trk_cut1_match_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_cut1_match_bendchi2   = ROOT.TH1F("h_200_trk_cut1_match_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_cut1_match_MVA1       = ROOT.TH1F("h_200_trk_cut1_match_MVA1",";MVA1",5000,0,1)
h_200_trk_cut1_pion_plus        = ROOT.TH1F("h_200_trk_cut1_pion_plus",";mass",500,0,10)
h_200_trk_cut1_pion_minus       = ROOT.TH1F("h_200_trk_cut1_pion_minus",";mass",500,0,10)
h_200_trk_cut1_Bs               = ROOT.TH1F("h_200_trk_cut1_Bs",";mass",500,0,10)
h_200_trk_cut2_match_dR         = ROOT.TH1F("h_200_trk_cut2_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_cut2_match_iso        = ROOT.TH1F("h_200_trk_cut2_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_200_trk_cut2_match_pt         = ROOT.TH1F("h_200_trk_cut2_match_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_cut2_match_eta        = ROOT.TH1F("h_200_trk_cut2_match_eta",";#eta",250,2.5,2.5)
h_200_trk_cut2_match_phi        = ROOT.TH1F("h_200_trk_cut2_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_cut2_match_d0         = ROOT.TH1F("h_200_trk_cut2_match_d0",";d0",200,-1,1)
h_200_trk_cut2_match_chi2dof    = ROOT.TH1F("h_200_trk_cut2_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_cut2_match_chi2rphi   = ROOT.TH1F("h_200_trk_cut2_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_cut2_match_chi2rz     = ROOT.TH1F("h_200_trk_cut2_match_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_cut2_match_bendchi2   = ROOT.TH1F("h_200_trk_cut2_match_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_cut2_match_MVA1       = ROOT.TH1F("h_200_trk_cut2_match_MVA1",";MVA1",5000,0,1)
h_200_trk_cut2_pion_plus        = ROOT.TH1F("h_200_trk_cut2_pion_plus",";mass",500,0,10)
h_200_trk_cut2_pion_minus       = ROOT.TH1F("h_200_trk_cut2_pion_minus",";mass",500,0,10)
h_200_trk_cut2_Bs               = ROOT.TH1F("h_200_trk_cut2_Bs",";mass",500,0,10)
h_200_trk_cut3_match_dR         = ROOT.TH1F("h_200_trk_cut3_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_cut3_match_iso        = ROOT.TH1F("h_200_trk_cut3_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_200_trk_cut3_match_pt         = ROOT.TH1F("h_200_trk_cut3_match_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_cut3_match_eta        = ROOT.TH1F("h_200_trk_cut3_match_eta",";#eta",250,2.5,2.5)
h_200_trk_cut3_match_phi        = ROOT.TH1F("h_200_trk_cut3_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_cut3_match_d0         = ROOT.TH1F("h_200_trk_cut3_match_d0",";d0",200,-1,1)
h_200_trk_cut3_match_chi2dof    = ROOT.TH1F("h_200_trk_cut3_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_cut3_match_chi2rphi   = ROOT.TH1F("h_200_trk_cut3_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_cut3_match_chi2rz     = ROOT.TH1F("h_200_trk_cut3_match_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_cut3_match_bendchi2   = ROOT.TH1F("h_200_trk_cut3_match_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_cut3_match_MVA1       = ROOT.TH1F("h_200_trk_cut3_match_MVA1",";MVA1",5000,0,1)
h_200_trk_cut3_pion_plus        = ROOT.TH1F("h_200_trk_cut3_pion_plus",";mass",500,0,10)
h_200_trk_cut3_pion_minus       = ROOT.TH1F("h_200_trk_cut3_pion_minus",";mass",500,0,10)
h_200_trk_cut3_Bs               = ROOT.TH1F("h_200_trk_cut3_Bs",";mass",500,0,10)
h_200_trk_cut4_match_dR         = ROOT.TH1F("h_200_trk_cut4_match_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_200_trk_cut4_match_iso        = ROOT.TH1F("h_200_trk_cut4_match_iso",";min #Delta R_{TTracks}",100,0,1)
h_200_trk_cut4_match_pt         = ROOT.TH1F("h_200_trk_cut4_match_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_cut4_match_eta        = ROOT.TH1F("h_200_trk_cut4_match_eta",";#eta",250,2.5,2.5)
h_200_trk_cut4_match_phi        = ROOT.TH1F("h_200_trk_cut4_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_cut4_match_d0         = ROOT.TH1F("h_200_trk_cut4_match_d0",";d0",200,-1,1)
h_200_trk_cut4_match_chi2dof    = ROOT.TH1F("h_200_trk_cut4_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_cut4_match_chi2rphi   = ROOT.TH1F("h_200_trk_cut4_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_cut4_match_chi2rz     = ROOT.TH1F("h_200_trk_cut4_match_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_cut4_match_bendchi2   = ROOT.TH1F("h_200_trk_cut4_match_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_cut4_match_MVA1       = ROOT.TH1F("h_200_trk_cut4_match_MVA1",";MVA1",5000,0,1)
h_200_trk_cut4_pion_plus        = ROOT.TH1F("h_200_trk_cut4_pion_plus",";mass",500,0,10)
h_200_trk_cut4_pion_minus       = ROOT.TH1F("h_200_trk_cut4_pion_minus",";mass",500,0,10)
h_200_trk_cut4_Bs               = ROOT.TH1F("h_200_trk_cut4_Bs",";mass",500,0,10)

h_200_trk_z0_weight_match= ROOT.TH1F("h_200_trk_z0_weight_match",";z",400,-0.1,0.1)
h_200_trk_z0_weight_all  = ROOT.TH1F("h_200_trk_z0_weight_all",";z",400,-0.1,0.1)

h_200_trk_phi_eta       = ROOT.TH2F("h_200_trk_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_trk_match_phi_eta = ROOT.TH2F("h_200_trk_match_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_trk_match_1_phi_eta = ROOT.TH2F("h_200_trk_match_1_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_trk_match_2_phi_eta = ROOT.TH2F("h_200_trk_match_2_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_gen_phi_eta = ROOT.TH2F("h_200_trk_gen_phi_eta",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_200_trk_phi_eta_weight       = ROOT.TH2F("h_200_trk_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)
h_200_trk_match_phi_eta_weight = ROOT.TH2F("h_200_trk_match_phi_eta_weight",";#eta;#phi",100,-2.5,2.5,100,-math.pi,math.pi)

h_200_gen_z0         = ROOT.TH1F("h_200_gen_z0",";z",300,-15,15)
h_200_diff_z0 = ROOT.TH1F("h_200_diff_z0",";Gen z0 - TTrack z0",200,-10,10)
h_200_diff_pt = ROOT.TH1F("h_200_diff_pt",";Gen p_{T} - TTrack p_{T}",100,-5,5)

h_200_trk_phi_eta_z0 = ROOT.TH3F("h_200_trk_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_match_1_phi_eta_z0 = ROOT.TH3F("h_200_trk_match_1_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_match_2_phi_eta_z0 = ROOT.TH3F("h_200_trk_match_2_phi_eta_z0", ";z;#phi;#eta",300,-15,15,100,-math.pi,math.pi,100,-2.5,2.5)
h_200_trk_match_1_z0         = ROOT.TH1F("h_200_trk_match_1_z0",";z",300,-15,15)
h_200_trk_match_2_z0         = ROOT.TH1F("h_200_trk_match_2_z0",";z",300,-15,15)

h_200_ntrack = ROOT.TH1F("h_200_ntrack",";N_{track}",40,0,400)

h_MinBias_trk_dR         = ROOT.TH1F("h_MinBias_trk_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_iso        = ROOT.TH1F("h_MinBias_trk_iso",";min #Delta R_{TTracks}",100,0,1)
h_MinBias_trk_pt         = ROOT.TH1F("h_MinBias_trk_pt",";p_{T} [GeV]",400,0,20)
h_MinBias_trk_eta        = ROOT.TH1F("h_MinBias_trk_eta",";#eta",250,2.5,2.5)
h_MinBias_trk_phi        = ROOT.TH1F("h_MinBias_trk_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_d0         = ROOT.TH1F("h_MinBias_trk_d0",";d0",200,-1,1)
h_MinBias_trk_z0         = ROOT.TH1F("h_MinBias_trk_z0",";z",300,-15,15)
h_MinBias_trk_nstub      = ROOT.TH1F("h_MinBias_trk_nstub",";nstub",8,2,10)
h_MinBias_trk_chi2dof    = ROOT.TH1F("h_MinBias_trk_chi2dof",";#chi^{2}/dof",400,0,20)
h_MinBias_trk_chi2rphi   = ROOT.TH1F("h_MinBias_trk_chi2rphi",";#chi^{2}rphi",400,0,20)
h_MinBias_trk_chi2rz     = ROOT.TH1F("h_MinBias_trk_chi2rz",";#chi^{2}rz",200,0,10)
h_MinBias_trk_bendchi2   = ROOT.TH1F("h_MinBias_trk_bendchi2",";bend #chi^{2}",200,0,10)
h_MinBias_trk_hitpattern = ROOT.TH1F("h_MinBias_trk_hitpattern",";hitpattern",130,0,130)
h_MinBias_trk_MVA1       = ROOT.TH1F("h_MinBias_trk_MVA1",";MVA1",5000,0,1)

h_MinBias_trk_cut1_dR         = ROOT.TH1F("h_MinBias_trk_cut1_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_cut1_iso        = ROOT.TH1F("h_MinBias_trk_cut1_iso",";min #Delta R_{TTracks}",100,0,1)
h_MinBias_trk_cut1_pt         = ROOT.TH1F("h_MinBias_trk_cut1_pt",";p_{T} [GeV]",400,0,20)
h_MinBias_trk_cut1_eta        = ROOT.TH1F("h_MinBias_trk_cut1_eta",";#eta",250,2.5,2.5)
h_MinBias_trk_cut1_phi        = ROOT.TH1F("h_MinBias_trk_cut1_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_cut1_d0         = ROOT.TH1F("h_MinBias_trk_cut1_d0",";d0",200,-1,1)
h_MinBias_trk_cut1_chi2dof    = ROOT.TH1F("h_MinBias_trk_cut1_chi2dof",";#chi^{2}/dof",400,0,20)
h_MinBias_trk_cut1_chi2rphi   = ROOT.TH1F("h_MinBias_trk_cut1_chi2rphi",";#chi^{2}rphi",400,0,20)
h_MinBias_trk_cut1_chi2rz     = ROOT.TH1F("h_MinBias_trk_cut1_chi2rz",";#chi^{2}rz",200,0,10)
h_MinBias_trk_cut1_bendchi2   = ROOT.TH1F("h_MinBias_trk_cut1_bendchi2",";bend #chi^{2}",200,0,10)
h_MinBias_trk_cut1_MVA1       = ROOT.TH1F("h_MinBias_trk_cut1_MVA1",";MVA1",5000,0,1)
h_MinBias_trk_cut2_dR         = ROOT.TH1F("h_MinBias_trk_cut2_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_cut2_iso        = ROOT.TH1F("h_MinBias_trk_cut2_iso",";min #Delta R_{TTracks}",100,0,1)
h_MinBias_trk_cut2_pt         = ROOT.TH1F("h_MinBias_trk_cut2_pt",";p_{T} [GeV]",400,0,20)
h_MinBias_trk_cut2_eta        = ROOT.TH1F("h_MinBias_trk_cut2_eta",";#eta",250,2.5,2.5)
h_MinBias_trk_cut2_phi        = ROOT.TH1F("h_MinBias_trk_cut2_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_cut2_d0         = ROOT.TH1F("h_MinBias_trk_cut2_d0",";d0",200,-1,1)
h_MinBias_trk_cut2_chi2dof    = ROOT.TH1F("h_MinBias_trk_cut2_chi2dof",";#chi^{2}/dof",400,0,20)
h_MinBias_trk_cut2_chi2rphi   = ROOT.TH1F("h_MinBias_trk_cut2_chi2rphi",";#chi^{2}rphi",400,0,20)
h_MinBias_trk_cut2_chi2rz     = ROOT.TH1F("h_MinBias_trk_cut2_chi2rz",";#chi^{2}rz",200,0,10)
h_MinBias_trk_cut2_bendchi2   = ROOT.TH1F("h_MinBias_trk_cut2_bendchi2",";bend #chi^{2}",200,0,10)
h_MinBias_trk_cut2_MVA1       = ROOT.TH1F("h_MinBias_trk_cut2_MVA1",";MVA1",5000,0,1)
h_MinBias_trk_cut3_dR         = ROOT.TH1F("h_MinBias_trk_cut3_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_cut3_iso        = ROOT.TH1F("h_MinBias_trk_cut3_iso",";min #Delta R_{TTracks}",100,0,1)
h_MinBias_trk_cut3_pt         = ROOT.TH1F("h_MinBias_trk_cut3_pt",";p_{T} [GeV]",400,0,20)
h_MinBias_trk_cut3_eta        = ROOT.TH1F("h_MinBias_trk_cut3_eta",";#eta",250,2.5,2.5)
h_MinBias_trk_cut3_phi        = ROOT.TH1F("h_MinBias_trk_cut3_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_cut3_d0         = ROOT.TH1F("h_MinBias_trk_cut3_d0",";d0",200,-1,1)
h_MinBias_trk_cut3_chi2dof    = ROOT.TH1F("h_MinBias_trk_cut3_chi2dof",";#chi^{2}/dof",400,0,20)
h_MinBias_trk_cut3_chi2rphi   = ROOT.TH1F("h_MinBias_trk_cut3_chi2rphi",";#chi^{2}rphi",400,0,20)
h_MinBias_trk_cut3_chi2rz     = ROOT.TH1F("h_MinBias_trk_cut3_chi2rz",";#chi^{2}rz",200,0,10)
h_MinBias_trk_cut3_bendchi2   = ROOT.TH1F("h_MinBias_trk_cut3_bendchi2",";bend #chi^{2}",200,0,10)
h_MinBias_trk_cut3_MVA1       = ROOT.TH1F("h_MinBias_trk_cut3_MVA1",";MVA1",5000,0,1)
h_MinBias_trk_cut4_dR         = ROOT.TH1F("h_MinBias_trk_cut4_dr",";min #Delta R_{gen, TTrack}",100,0,0.5)
h_MinBias_trk_cut4_iso        = ROOT.TH1F("h_MinBias_trk_cut4_iso",";min #Delta R_{TTracks}",100,0,1)
h_MinBias_trk_cut4_pt         = ROOT.TH1F("h_MinBias_trk_cut4_pt",";p_{T} [GeV]",400,0,20)
h_MinBias_trk_cut4_eta        = ROOT.TH1F("h_MinBias_trk_cut4_eta",";#eta",250,2.5,2.5)
h_MinBias_trk_cut4_phi        = ROOT.TH1F("h_MinBias_trk_cut4_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_cut4_d0         = ROOT.TH1F("h_MinBias_trk_cut4_d0",";d0",200,-1,1)
h_MinBias_trk_cut4_chi2dof    = ROOT.TH1F("h_MinBias_trk_cut4_chi2dof",";#chi^{2}/dof",400,0,20)
h_MinBias_trk_cut4_chi2rphi   = ROOT.TH1F("h_MinBias_trk_cut4_chi2rphi",";#chi^{2}rphi",400,0,20)
h_MinBias_trk_cut4_chi2rz     = ROOT.TH1F("h_MinBias_trk_cut4_chi2rz",";#chi^{2}rz",200,0,10)
h_MinBias_trk_cut4_bendchi2   = ROOT.TH1F("h_MinBias_trk_cut4_bendchi2",";bend #chi^{2}",200,0,10)
h_MinBias_trk_cut4_MVA1       = ROOT.TH1F("h_MinBias_trk_cut4_MVA1",";MVA1",5000,0,1)

nct=0

titles = []
titles.append('6pi TTrack')

start_time = time.time()
npu = 0
ensureDir('Plots'+str(npu)+'')
parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name')
parser.add_argument('pnevt_PU0', type=int, help='number of preivous event for PU0')
parser.add_argument('pnevt_PU200', type=int, help='number of preivous event for PU200')
args = parser.parse_args()

ofile = ROOT.TFile("output.root", "RECREATE")

if not args.fname == 'minBias':
    file_list = ['/eos/cms/store/user/chuh/l1p2/PU0/Tau3pi_PY8_PU0_GTT_'+args.fname+'.root']
    tree = ROOT.TChain("L1TrackNtuple/eventTree")
    for file_name in file_list:
        tree.Add(file_name)
    Nevt = tree.GetEntries()

    print('Total Number of events = ', Nevt)

    evt = args.pnevt_PU0-1
    for entry in tree:

        evt+=1
        if (evt-args.pnevt_PU0)%5000==0: 
            time_elapsed = time.time() - start_time
            print('{0:.2f}'.format(float(evt-args.pnevt_PU0)/float(Nevt)*100.), '% processed ', '{0:.2f}'.format(float(evt-args.pnevt_PU0)/float(time_elapsed)), 'Hz')

        npi = 0
        for igen in range(len(tree.gen_pt)):
            if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                npi += 1
        if (npi == 6):
            nct += 1
        elif not (npu == 'minBias'):
            continue
        
        sumpt=0
        cnt1=0
        cnt2=0
        cntp=0
        cntm=0
        pip = []
        pim = []
        pip_cut1 = []
        pim_cut1 = []
        pip_cut2 = []
        pim_cut2 = []
        pip_cut3 = []
        pim_cut3 = []
        pip_cut4 = []
        pim_cut4 = []
        ntrk0 = 0
        ntrk1 = 0
        ntrk2 = 0
        ntrk3 = 0
        ntrk4 = 0
        data = []
        flag = True

        for itrk in range(len(tree.trk_pt)):
            dRmin = 999.
            dRiso = 999
            ntrk0+=1

            if tree.trk_MVA1[itrk] < 0.997 : 
                ntrk1+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2: 
                ntrk2+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.3: 
                ntrk3+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.2: 
                ntrk4+=1

            for igen in range(len(tree.gen_pt)):
                if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                    dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                        gen_mpdgid = tree.gen_mpdgid[igen]
            if dRmin < 0.02:
                if gen_mpdgid > 0:
                    cntp+=1
                elif gen_mpdgid < 0:
                    cntm+=1
        if cntp != 3 or cntm != 3: continue

        for itrk in range(len(tree.trk_pt)):
            dRmin = 999.
            dRiso = 999.
            for igen in range(len(tree.gen_pt)):
                if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                    dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                        gen_pt = tree.gen_pt[igen]
                        gen_eta = tree.gen_eta[igen]
                        gen_phi = tree.gen_phi[igen]
                        gen_z0 = tree.gen_z0[igen]
                        gen_mpdgid = tree.gen_mpdgid[igen]

            for jtrk in range(len(tree.trk_pt)):
                sumpt += tree.trk_pt[jtrk] 
                if itrk == jtrk:
                    continue
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
                if dR < dRiso:
                    dRiso = dR
            #     if tree.trk_MVA1[jtrk] < 0.997 and abs(tree.trk_eta[jtrk]) < 2 and flag:
            #         tmp = [tree.trk_z0[jtrk],tree.trk_phi[jtrk],tree.trk_eta[jtrk]]
            #         data.append(tmp)

            # if flag:
            #     dbscan = DBSCAN(eps=0.3, min_samples=3, metric=spherical_distance)
            #     dbscan.fit(data)
            #     labels = dbscan.labels_
            #     clustered_data_0p3 = np.hstack((data, labels.reshape(-1, 1)))
            #     for point in clustered_data_0p3:
            #         if not int(point[3] == -1):
            #             print(f"Point: {point[:3]}, Cluster: {int(point[3])}")
            #     dbscan = DBSCAN(eps=0.2, min_samples=3, metric=spherical_distance)
            #     dbscan.fit(data)
            #     labels = dbscan.labels_
            #     clustered_data_0p2 = np.hstack((data, labels.reshape(-1, 1)))
            #     for point in clustered_data_0p2:
            #         if not int(point[3] == -1):
            #             print(f"Point: {point[:3]}, Cluster: {int(point[3])}")

            flag = False
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
            h_0_trk_z0_weight_all.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
            h_0_trk_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
            h_0_trk_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
            h_0_trk_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])

            if tree.trk_MVA1[itrk] < 0.997 : 
                h_0_trk_cut1_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2: 
                h_0_trk_cut2_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.3: 
                h_0_trk_cut3_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.2: 
                h_0_trk_cut4_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            cnt2+=1

            if dRmin < 0.02:
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
                h_0_trk_z0_weight_match.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
                h_0_trk_match_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
                h_0_trk_match_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                if gen_mpdgid > 0:
                    h_0_trk_match_1_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                    h_0_trk_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    h_0_trk_match_1_z0.Fill(tree.trk_z0[itrk])
                    pip.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_0_trk_match_2_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                    h_0_trk_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    h_0_trk_match_2_z0.Fill(tree.trk_z0[itrk])
                    pim.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                h_0_gen_phi_eta.Fill(gen_eta, gen_phi)
                h_0_gen_z0.Fill(gen_z0)
                h_0_diff_z0.Fill(gen_z0-tree.trk_z0[itrk])
                h_0_diff_pt.Fill(gen_pt-tree.trk_pt[itrk])

                if not tree.trk_MVA1[itrk] < 0.997: continue
                h_0_trk_cut1_match_dR.Fill(dRmin)
                h_0_trk_cut1_match_iso.Fill(dRiso)
                h_0_trk_cut1_match_pt.Fill(tree.trk_pt[itrk])
                h_0_trk_cut1_match_eta.Fill(tree.trk_eta[itrk])
                h_0_trk_cut1_match_phi.Fill(tree.trk_phi[itrk])
                h_0_trk_cut1_match_d0.Fill(tree.trk_d0[itrk])
                h_0_trk_cut1_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_0_trk_cut1_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_0_trk_cut1_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_0_trk_cut1_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_0_trk_cut1_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_0_trk_cut1_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut1.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_0_trk_cut1_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut1.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                if not abs(tree.trk_eta[itrk]) < 2 : continue
                h_0_trk_cut2_match_dR.Fill(dRmin)
                h_0_trk_cut2_match_iso.Fill(dRiso)
                h_0_trk_cut2_match_pt.Fill(tree.trk_pt[itrk])
                h_0_trk_cut2_match_eta.Fill(tree.trk_eta[itrk])
                h_0_trk_cut2_match_phi.Fill(tree.trk_phi[itrk])
                h_0_trk_cut2_match_d0.Fill(tree.trk_d0[itrk])
                h_0_trk_cut2_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_0_trk_cut2_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_0_trk_cut2_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_0_trk_cut2_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_0_trk_cut2_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_0_trk_cut2_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut2.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_0_trk_cut2_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut2.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                if not dRiso < 0.3: continue
                h_0_trk_cut3_match_dR.Fill(dRmin)
                h_0_trk_cut3_match_iso.Fill(dRiso)
                h_0_trk_cut3_match_pt.Fill(tree.trk_pt[itrk])
                h_0_trk_cut3_match_eta.Fill(tree.trk_eta[itrk])
                h_0_trk_cut3_match_phi.Fill(tree.trk_phi[itrk])
                h_0_trk_cut3_match_d0.Fill(tree.trk_d0[itrk])
                h_0_trk_cut3_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_0_trk_cut3_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_0_trk_cut3_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_0_trk_cut3_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_0_trk_cut3_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_0_trk_cut3_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut3.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_0_trk_cut3_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut3.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                if not dRiso < 0.2: continue
                h_0_trk_cut4_match_dR.Fill(dRmin)
                h_0_trk_cut4_match_iso.Fill(dRiso)
                h_0_trk_cut4_match_pt.Fill(tree.trk_pt[itrk])
                h_0_trk_cut4_match_eta.Fill(tree.trk_eta[itrk])
                h_0_trk_cut4_match_phi.Fill(tree.trk_phi[itrk])
                h_0_trk_cut4_match_d0.Fill(tree.trk_d0[itrk])
                h_0_trk_cut4_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_0_trk_cut4_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_0_trk_cut4_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_0_trk_cut4_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_0_trk_cut4_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_0_trk_cut4_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut4.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_0_trk_cut4_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut4.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
            
            if cnt1 >= 6:
                break

        Plot2D(h_0_trk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot2D(h_0_trk_match_phi_eta, h_0_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_match_phi_eta.GetName() +str(evt)+ '.png', True, False, True)
        comparisonPlots(h_0_trk_z0, h_0_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_0_trk_z0.GetName() +str(evt)+ '.png', False, False, True)

        comparisonPlots2D(h_0_trk_phi_eta, h_0_trk_match_1_phi_eta, h_0_trk_match_2_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_0_trk_phi_eta_z0, h_0_trk_match_1_phi_eta_z0, h_0_trk_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparison3Plots(h_0_trk_match_1_z0, h_0_trk_match_2_z0, h_0_trk_z0, False, 'Plots'+str(npu)+'/'+h_0_trk_match_z0.GetName() +str(evt)+ '.png', False, True, True)
        comparisonPlot3D(h_0_trk_cut1_phi_eta_z0, h_0_trk_cut1_match_1_phi_eta_z0, h_0_trk_cut1_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_cut1_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_0_trk_cut2_phi_eta_z0, h_0_trk_cut2_match_1_phi_eta_z0, h_0_trk_cut2_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_cut2_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_0_trk_cut3_phi_eta_z0, h_0_trk_cut3_match_1_phi_eta_z0, h_0_trk_cut3_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_cut3_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_0_trk_cut4_phi_eta_z0, h_0_trk_cut4_match_1_phi_eta_z0, h_0_trk_cut4_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_trk_cut4_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)

        comparisonPlots(h_0_gen_z0, h_0_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_0_gen_z0.GetName() +str(evt)+ '.png', False, True, True)
        Plots(h_0_diff_pt, titles, False, 'Plots'+str(npu)+'/' + h_0_diff_pt.GetName() +str(evt)+ '.png', False, False, False)
        Plots(h_0_diff_z0, titles, False, 'Plots'+str(npu)+'/' + h_0_diff_z0.GetName() +str(evt)+ '.png', False, False, False)
        h_0_trk_phi_eta.Reset()
        h_0_trk_match_phi_eta.Reset()
        h_0_trk_phi_eta_weight.Reset()
        h_0_trk_match_phi_eta_weight.Reset()
        h_0_gen_phi_eta.Reset()
        h_0_trk_z0.Reset()
        h_0_trk_z0_weight_all.Reset()
        h_0_gen_z0.Reset()
        h_0_trk_match_z0.Reset()
        h_0_diff_z0.Reset()
        h_0_diff_pt.Reset()
        h_0_trk_phi_eta_z0.Reset()
        h_0_trk_match_1_phi_eta.Reset()
        h_0_trk_match_2_phi_eta.Reset()
        h_0_trk_match_1_phi_eta_z0.Reset()
        h_0_trk_match_2_phi_eta_z0.Reset()
        h_0_trk_match_1_z0.Reset()
        h_0_trk_match_2_z0.Reset()
        h_0_trk_cut1_phi_eta_z0.Reset()
        h_0_trk_cut1_match_1_phi_eta_z0.Reset()
        h_0_trk_cut1_match_2_phi_eta_z0.Reset()
        h_0_trk_cut2_phi_eta_z0.Reset()
        h_0_trk_cut2_match_1_phi_eta_z0.Reset()
        h_0_trk_cut2_match_2_phi_eta_z0.Reset()
        h_0_trk_cut3_phi_eta_z0.Reset()
        h_0_trk_cut3_match_1_phi_eta_z0.Reset()
        h_0_trk_cut3_match_2_phi_eta_z0.Reset()
        h_0_trk_cut4_phi_eta_z0.Reset()
        h_0_trk_cut4_match_1_phi_eta_z0.Reset()
        h_0_trk_cut4_match_2_phi_eta_z0.Reset()

        pion_p = pip[0]+pip[1]+pip[2]
        pion_m = pim[0]+pim[1]+pim[2]
        Bs = pion_p + pion_m
        h_0_trk_pion_plus.Fill(pion_p.M())
        h_0_trk_pion_minus.Fill(pion_m.M())
        h_0_trk_Bs.Fill(Bs.M())
        if len(pip_cut1) > 2 and len(pim_cut1) > 2:
            pion_p = pip_cut1[0]+pip_cut1[1]+pip_cut1[2]
            pion_m = pim_cut1[0]+pim_cut1[1]+pim_cut1[2]
            Bs = pion_p + pion_m
            h_0_trk_cut1_pion_plus.Fill(pion_p.M())
            h_0_trk_cut1_pion_minus.Fill(pion_m.M())
            h_0_trk_cut1_Bs.Fill(Bs.M())
        if len(pip_cut2) > 2 and len(pim_cut2) > 2:
            pion_p = pip_cut2[0]+pip_cut2[1]+pip_cut2[2]
            pion_m = pim_cut2[0]+pim_cut2[1]+pim_cut2[2]
            Bs = pion_p + pion_m
            h_0_trk_cut2_pion_plus.Fill(pion_p.M())
            h_0_trk_cut2_pion_minus.Fill(pion_m.M())
            h_0_trk_cut2_Bs.Fill(Bs.M())
        if len(pip_cut3) > 2 and len(pim_cut3) > 2:
            pion_p = pip_cut3[0]+pip_cut3[1]+pip_cut3[2]
            pion_m = pim_cut3[0]+pim_cut3[1]+pim_cut3[2]
            Bs = pion_p + pion_m
            h_0_trk_cut3_pion_plus.Fill(pion_p.M())
            h_0_trk_cut3_pion_minus.Fill(pion_m.M())
            h_0_trk_cut3_Bs.Fill(Bs.M())
        if len(pip_cut4) > 2 and len(pim_cut4) > 2:
            pion_p = pip_cut4[0]+pip_cut4[1]+pip_cut4[2]
            pion_m = pim_cut4[0]+pim_cut4[1]+pim_cut4[2]
            Bs = pion_p + pion_m
            h_0_trk_cut4_pion_plus.Fill(pion_p.M())
            h_0_trk_cut4_pion_minus.Fill(pion_m.M())
            h_0_trk_cut4_Bs.Fill(Bs.M())

        h_0_trk_match_ntrk.Fill(ntrk0)
        h_0_trk_cut1_match_ntrk.Fill(ntrk1)
        h_0_trk_cut2_match_ntrk.Fill(ntrk2)
        h_0_trk_cut3_match_ntrk.Fill(ntrk3)
        h_0_trk_cut4_match_ntrk.Fill(ntrk4)
            
    h_0_trk_dR.Write()
    h_0_trk_iso.Write()
    h_0_trk_pt.Write()
    h_0_trk_eta.Write()
    h_0_trk_phi.Write()
    h_0_trk_d0.Write()
    h_0_trk_nstub.Write()
    h_0_trk_chi2dof.Write()
    h_0_trk_chi2rphi.Write()
    h_0_trk_chi2rz.Write()
    h_0_trk_bendchi2.Write()
    h_0_trk_MVA1.Write()

    h_0_trk_match_dR.Write()
    h_0_trk_match_iso.Write()
    h_0_trk_match_pt.Write()
    h_0_trk_match_eta.Write()
    h_0_trk_match_phi.Write()
    h_0_trk_match_d0.Write()
    h_0_trk_match_nstub.Write()
    h_0_trk_match_chi2dof.Write()
    h_0_trk_match_chi2rphi.Write()
    h_0_trk_match_chi2rz.Write()
    h_0_trk_match_bendchi2.Write()
    h_0_trk_match_MVA1.Write()
    h_0_trk_pion_plus.Write()
    h_0_trk_pion_minus.Write()
    h_0_trk_Bs.Write()

    h_0_trk_cut1_match_dR.Write()
    h_0_trk_cut1_match_iso.Write()
    h_0_trk_cut1_match_pt.Write()
    h_0_trk_cut1_match_eta.Write()
    h_0_trk_cut1_match_phi.Write()
    h_0_trk_cut1_match_d0.Write()
    h_0_trk_cut1_match_chi2dof.Write()
    h_0_trk_cut1_match_chi2rphi.Write()
    h_0_trk_cut1_match_chi2rz.Write()
    h_0_trk_cut1_match_bendchi2.Write()
    h_0_trk_cut1_match_MVA1.Write()
    h_0_trk_cut1_pion_plus.Write()
    h_0_trk_cut1_pion_minus.Write()
    h_0_trk_cut1_Bs.Write()
    h_0_trk_cut2_match_dR.Write()
    h_0_trk_cut2_match_iso.Write()
    h_0_trk_cut2_match_pt.Write()
    h_0_trk_cut2_match_eta.Write()
    h_0_trk_cut2_match_phi.Write()
    h_0_trk_cut2_match_d0.Write()
    h_0_trk_cut2_match_chi2dof.Write()
    h_0_trk_cut2_match_chi2rphi.Write()
    h_0_trk_cut2_match_chi2rz.Write()
    h_0_trk_cut2_match_bendchi2.Write()
    h_0_trk_cut2_match_MVA1.Write()
    h_0_trk_cut2_pion_plus.Write()
    h_0_trk_cut2_pion_minus.Write()
    h_0_trk_cut2_Bs.Write()
    h_0_trk_cut3_match_dR.Write()
    h_0_trk_cut3_match_iso.Write()
    h_0_trk_cut3_match_pt.Write()
    h_0_trk_cut3_match_eta.Write()
    h_0_trk_cut3_match_phi.Write()
    h_0_trk_cut3_match_d0.Write()
    h_0_trk_cut3_match_chi2dof.Write()
    h_0_trk_cut3_match_chi2rphi.Write()
    h_0_trk_cut3_match_chi2rz.Write()
    h_0_trk_cut3_match_bendchi2.Write()
    h_0_trk_cut3_match_MVA1.Write()
    h_0_trk_cut3_pion_plus.Write()
    h_0_trk_cut3_pion_minus.Write()
    h_0_trk_cut3_Bs.Write()
    h_0_trk_cut4_match_dR.Write()
    h_0_trk_cut4_match_iso.Write()
    h_0_trk_cut4_match_pt.Write()
    h_0_trk_cut4_match_eta.Write()
    h_0_trk_cut4_match_phi.Write()
    h_0_trk_cut4_match_d0.Write()
    h_0_trk_cut4_match_chi2dof.Write()
    h_0_trk_cut4_match_chi2rphi.Write()
    h_0_trk_cut4_match_chi2rz.Write()
    h_0_trk_cut4_match_bendchi2.Write()
    h_0_trk_cut4_match_MVA1.Write()
    h_0_trk_cut4_pion_plus.Write()
    h_0_trk_cut4_pion_minus.Write()
    h_0_trk_cut4_Bs.Write()
    h_0_trk_match_ntrk.Write()
    h_0_trk_cut1_match_ntrk.Write()
    h_0_trk_cut2_match_ntrk.Write()
    h_0_trk_cut3_match_ntrk.Write()
    h_0_trk_cut4_match_ntrk.Write()
    print(nct)

    nct=0
    start_time = time.time()
    npu = 200
    ensureDir('Plots'+str(npu)+'')
    file_list = ['/eos/cms/store/user/chuh/l1p2/PU200/Tau3pi_PY8_PU200_GTT_'+args.fname+'.root']
    tree = ROOT.TChain("L1TrackNtuple/eventTree")
    for file_name in file_list:
        tree.Add(file_name)
    Nevt = tree.GetEntries()

    print('Total Number of events = ', Nevt)

    evt = args.pnevt_PU200-1
    for entry in tree:

        evt+=1
        if (evt-args.pnevt_PU200)%5000==0: 
            time_elapsed = time.time() - start_time
            print('{0:.2f}'.format(float(evt-args.pnevt_PU200)/float(Nevt)*100.), '% processed ', '{0:.2f}'.format(float(evt-args.pnevt_PU200)/float(time_elapsed)), 'Hz')

        npi = 0
        for igen in range(len(tree.gen_pt)):
            if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                npi += 1
        if (npi == 6):
            nct += 1
        elif not (npu == 'minBias'):
            continue
        
        sumpt=0
        cnt1=0
        cnt2=0
        cntp=0
        cntm=0
        pip = []
        pim = []
        pip_cut1 = []
        pim_cut1 = []
        pip_cut2 = []
        pim_cut2 = []
        pip_cut3 = []
        pim_cut3 = []
        pip_cut4 = []
        pim_cut4 = []
        ntrk0 = 0
        ntrk1 = 0
        ntrk2 = 0
        ntrk3 = 0
        ntrk4 = 0

        for itrk in range(len(tree.trk_pt)):
            dRmin = 999.
            dRiso = 999.

            ntrk0+=1
            if tree.trk_MVA1[itrk] < 0.997 : 
                ntrk1+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2: 
                ntrk2+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.3: 
                ntrk3+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.2: 
                ntrk4+=1

            for igen in range(len(tree.gen_pt)):
                if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                    dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                        gen_mpdgid = tree.gen_mpdgid[igen]
            if dRmin < 0.02:
                if gen_mpdgid > 0:
                    cntp+=1
                elif gen_mpdgid < 0:
                    cntm+=1
        if cntp != 3 or cntm != 3: continue

        for itrk in range(len(tree.trk_pt)):
            dRmin = 999.
            dRiso = 999.
            for igen in range(len(tree.gen_pt)):
                if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                    dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                        gen_pt = tree.gen_pt[igen]
                        gen_eta = tree.gen_eta[igen]
                        gen_phi = tree.gen_phi[igen]
                        gen_z0 = tree.gen_z0[igen]
                        gen_mpdgid = tree.gen_mpdgid[igen]

            for jtrk in range(len(tree.trk_pt)):
                sumpt += tree.trk_pt[jtrk] 
                if itrk == jtrk:
                    continue
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
                if dR < dRiso:
                    dRiso = dR

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
            h_200_trk_z0_weight_all.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
            h_200_trk_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
            h_200_trk_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
            h_200_trk_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 : 
                h_200_trk_cut1_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2: 
                h_200_trk_cut2_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.3: 
                h_200_trk_cut3_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.2: 
                h_200_trk_cut4_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])

            cnt2+=1
            if dRmin < 0.02:
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
                h_200_trk_z0_weight_match.Fill(tree.trk_z0[itrk]*tree.trk_pt[itrk]/sumpt)
                h_200_trk_match_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                h_200_trk_match_phi_eta_weight.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk],tree.trk_pt[itrk]/sumpt)
                h_200_gen_phi_eta.Fill(gen_eta, gen_phi)
                h_200_gen_z0.Fill(gen_z0)
                h_200_diff_z0.Fill(gen_z0-tree.trk_z0[itrk])
                h_200_diff_pt.Fill(gen_pt-tree.trk_pt[itrk])
                if gen_mpdgid > 0:
                    h_200_trk_match_1_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                    h_200_trk_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
                    h_200_trk_match_1_z0.Fill(tree.trk_z0[itrk])
                    pip.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                else:
                    h_200_trk_match_2_phi_eta.Fill(tree.trk_eta[itrk], tree.trk_phi[itrk])
                    h_200_trk_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])
                    h_200_trk_match_2_z0.Fill(tree.trk_z0[itrk])
                    pim.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))

                if not tree.trk_MVA1[itrk] < 0.997: continue
                h_200_trk_cut1_match_dR.Fill(dRmin)
                h_200_trk_cut1_match_iso.Fill(dRiso)
                h_200_trk_cut1_match_pt.Fill(tree.trk_pt[itrk])
                h_200_trk_cut1_match_eta.Fill(tree.trk_eta[itrk])
                h_200_trk_cut1_match_phi.Fill(tree.trk_phi[itrk])
                h_200_trk_cut1_match_d0.Fill(tree.trk_d0[itrk])
                h_200_trk_cut1_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_200_trk_cut1_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_200_trk_cut1_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_200_trk_cut1_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_200_trk_cut1_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_200_trk_cut1_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut1.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_200_trk_cut1_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut1.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                if not abs(tree.trk_eta[itrk]) < 2 : continue
                h_200_trk_cut2_match_dR.Fill(dRmin)
                h_200_trk_cut2_match_iso.Fill(dRiso)
                h_200_trk_cut2_match_pt.Fill(tree.trk_pt[itrk])
                h_200_trk_cut2_match_eta.Fill(tree.trk_eta[itrk])
                h_200_trk_cut2_match_phi.Fill(tree.trk_phi[itrk])
                h_200_trk_cut2_match_d0.Fill(tree.trk_d0[itrk])
                h_200_trk_cut2_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_200_trk_cut2_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_200_trk_cut2_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_200_trk_cut2_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_200_trk_cut2_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_200_trk_cut2_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut2.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_200_trk_cut2_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut2.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                if not dRiso < 0.3: continue
                h_200_trk_cut3_match_dR.Fill(dRmin)
                h_200_trk_cut3_match_iso.Fill(dRiso)
                h_200_trk_cut3_match_pt.Fill(tree.trk_pt[itrk])
                h_200_trk_cut3_match_eta.Fill(tree.trk_eta[itrk])
                h_200_trk_cut3_match_phi.Fill(tree.trk_phi[itrk])
                h_200_trk_cut3_match_d0.Fill(tree.trk_d0[itrk])
                h_200_trk_cut3_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_200_trk_cut3_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_200_trk_cut3_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_200_trk_cut3_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_200_trk_cut3_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_200_trk_cut3_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut3.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_200_trk_cut3_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut3.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                if not dRiso < 0.2: continue
                h_200_trk_cut4_match_dR.Fill(dRmin)
                h_200_trk_cut4_match_iso.Fill(dRiso)
                h_200_trk_cut4_match_pt.Fill(tree.trk_pt[itrk])
                h_200_trk_cut4_match_eta.Fill(tree.trk_eta[itrk])
                h_200_trk_cut4_match_phi.Fill(tree.trk_phi[itrk])
                h_200_trk_cut4_match_d0.Fill(tree.trk_d0[itrk])
                h_200_trk_cut4_match_chi2dof.Fill(tree.trk_chi2dof[itrk])
                h_200_trk_cut4_match_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
                h_200_trk_cut4_match_chi2rz.Fill(tree.trk_chi2rz[itrk])
                h_200_trk_cut4_match_bendchi2.Fill(tree.trk_bendchi2[itrk])
                h_200_trk_cut4_match_MVA1.Fill(tree.trk_MVA1[itrk])
                if gen_mpdgid > 0:
                    h_200_trk_cut4_match_1_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pip_cut4.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
                elif gen_mpdgid < 0:
                    h_200_trk_cut4_match_2_phi_eta_z0.Fill(tree.trk_z0[itrk],tree.trk_phi[itrk],tree.trk_eta[itrk])
                    pim_cut4.append(create_lorentz_vector(tree.trk_pt[itrk],tree.trk_eta[itrk],tree.trk_phi[itrk]))
            
            if cnt1 >= 6:
                break

        Plot2D(h_200_trk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_match_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot2D(h_200_trk_match_phi_eta, h_200_gen_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_match_phi_eta.GetName() +str(evt)+ '.png', True, False, True)
        comparisonPlot2D(h_200_trk_phi_eta, h_200_trk_match_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_phi_eta.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlots(h_200_trk_z0, h_200_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_200_trk_z0.GetName() +str(evt)+ '.png', False, False, True)
        comparisonPlots(h_200_gen_z0, h_200_trk_match_z0, False, 'Plots'+str(npu)+'/compare_' + h_200_gen_z0.GetName() +str(evt)+ '.png', False, True, True)
        comparisonPlots2D(h_200_trk_phi_eta, h_200_trk_match_1_phi_eta, h_200_trk_match_2_phi_eta, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_phi_eta.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_200_trk_phi_eta_z0, h_200_trk_match_1_phi_eta_z0, h_200_trk_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparison3Plots(h_200_trk_match_1_z0, h_200_trk_match_2_z0, h_200_trk_z0, False, 'Plots'+str(npu)+'/'+h_200_trk_match_z0.GetName() +str(evt)+ '.png', False, True, True)
        Plots(h_200_diff_pt, titles, False, 'Plots'+str(npu)+'/' + h_200_diff_pt.GetName() +str(evt)+ '.png', False, False, False)
        Plots(h_200_diff_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_diff_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_200_trk_cut1_phi_eta_z0, h_200_trk_cut1_match_1_phi_eta_z0, h_200_trk_cut1_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_cut1_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_200_trk_cut2_phi_eta_z0, h_200_trk_cut2_match_1_phi_eta_z0, h_200_trk_cut2_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_cut2_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_200_trk_cut3_phi_eta_z0, h_200_trk_cut3_match_1_phi_eta_z0, h_200_trk_cut3_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_cut3_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)
        comparisonPlot3D(h_200_trk_cut4_phi_eta_z0, h_200_trk_cut4_match_1_phi_eta_z0, h_200_trk_cut4_match_2_phi_eta_z0, titles, False, 'Plots'+str(npu)+'/' + h_200_trk_cut4_phi_eta_z0.GetName() +str(evt)+ '.png', False, False, False)

        h_200_trk_phi_eta.Reset()
        h_200_trk_match_phi_eta.Reset()
        h_200_trk_phi_eta_weight.Reset()
        h_200_trk_match_phi_eta_weight.Reset()
        h_200_gen_phi_eta.Reset()
        h_200_trk_z0.Reset()
        h_200_gen_z0.Reset()
        h_200_trk_match_z0.Reset()
        h_200_diff_z0.Reset()
        h_200_diff_pt.Reset()
        h_200_trk_phi_eta_z0.Reset()
        h_200_trk_match_1_phi_eta.Reset()
        h_200_trk_match_2_phi_eta.Reset()
        h_200_trk_match_1_phi_eta_z0.Reset()
        h_200_trk_match_2_phi_eta_z0.Reset()
        h_200_trk_match_1_z0.Reset()
        h_200_trk_match_2_z0.Reset()
        h_200_trk_cut1_phi_eta_z0.Reset()
        h_200_trk_cut1_match_1_phi_eta_z0.Reset()
        h_200_trk_cut1_match_2_phi_eta_z0.Reset()
        h_200_trk_cut2_phi_eta_z0.Reset()
        h_200_trk_cut2_match_1_phi_eta_z0.Reset()
        h_200_trk_cut2_match_2_phi_eta_z0.Reset()
        h_200_trk_cut3_phi_eta_z0.Reset()
        h_200_trk_cut3_match_1_phi_eta_z0.Reset()
        h_200_trk_cut3_match_2_phi_eta_z0.Reset()
        h_200_trk_cut4_phi_eta_z0.Reset()
        h_200_trk_cut4_match_1_phi_eta_z0.Reset()
        h_200_trk_cut4_match_2_phi_eta_z0.Reset()

        pion_p = pip[0]+pip[1]+pip[2]
        pion_m = pim[0]+pim[1]+pim[2]
        Bs = pion_p + pion_m
        h_200_trk_pion_plus.Fill(pion_p.M())
        h_200_trk_pion_minus.Fill(pion_m.M())
        h_200_trk_Bs.Fill(Bs.M())
        if len(pip_cut1) > 2 and len(pim_cut1) > 2:
            pion_p = pip_cut1[0]+pip_cut1[1]+pip_cut1[2]
            pion_m = pim_cut1[0]+pim_cut1[1]+pim_cut1[2]
            Bs = pion_p + pion_m
            h_200_trk_cut1_pion_plus.Fill(pion_p.M())
            h_200_trk_cut1_pion_minus.Fill(pion_m.M())
            h_200_trk_cut1_Bs.Fill(Bs.M())
        if len(pip_cut2) > 2 and len(pim_cut2) > 2:
            pion_p = pip_cut2[0]+pip_cut2[1]+pip_cut2[2]
            pion_m = pim_cut2[0]+pim_cut2[1]+pim_cut2[2]
            Bs = pion_p + pion_m
            h_200_trk_cut2_pion_plus.Fill(pion_p.M())
            h_200_trk_cut2_pion_minus.Fill(pion_m.M())
            h_200_trk_cut2_Bs.Fill(Bs.M())
        if len(pip_cut3) > 2 and len(pim_cut3) > 2:
            pion_p = pip_cut3[0]+pip_cut3[1]+pip_cut3[2]
            pion_m = pim_cut3[0]+pim_cut3[1]+pim_cut3[2]
            Bs = pion_p + pion_m
            h_200_trk_cut3_pion_plus.Fill(pion_p.M())
            h_200_trk_cut3_pion_minus.Fill(pion_m.M())
            h_200_trk_cut3_Bs.Fill(Bs.M())
        if len(pip_cut4) > 2 and len(pim_cut4) > 2:
            pion_p = pip_cut4[0]+pip_cut4[1]+pip_cut4[2]
            pion_m = pim_cut4[0]+pim_cut4[1]+pim_cut4[2]
            Bs = pion_p + pion_m
            h_200_trk_cut4_pion_plus.Fill(pion_p.M())
            h_200_trk_cut4_pion_minus.Fill(pion_m.M())
            h_200_trk_cut4_Bs.Fill(Bs.M())

        h_200_trk_match_ntrk.Fill(ntrk0)
        h_200_trk_cut1_match_ntrk.Fill(ntrk1)
        h_200_trk_cut2_match_ntrk.Fill(ntrk2)
        h_200_trk_cut3_match_ntrk.Fill(ntrk3)
        h_200_trk_cut4_match_ntrk.Fill(ntrk4)
            
    h_200_trk_dR.Write()
    h_200_trk_iso.Write()
    h_200_trk_pt.Write()
    h_200_trk_eta.Write()
    h_200_trk_phi.Write()
    h_200_trk_d0.Write()
    h_200_trk_nstub.Write()
    h_200_trk_chi2dof.Write()
    h_200_trk_chi2rphi.Write()
    h_200_trk_chi2rz.Write()
    h_200_trk_bendchi2.Write()
    h_200_trk_MVA1.Write()

    h_200_trk_match_dR.Write()
    h_200_trk_match_iso.Write()
    h_200_trk_match_pt.Write()
    h_200_trk_match_eta.Write()
    h_200_trk_match_phi.Write()
    h_200_trk_match_d0.Write()
    h_200_trk_match_nstub.Write()
    h_200_trk_match_chi2dof.Write()
    h_200_trk_match_chi2rphi.Write()
    h_200_trk_match_chi2rz.Write()
    h_200_trk_match_bendchi2.Write()
    h_200_trk_match_MVA1.Write()
    h_200_trk_pion_plus.Write()
    h_200_trk_pion_minus.Write()
    h_200_trk_Bs.Write()

    h_200_trk_cut1_match_dR.Write()
    h_200_trk_cut1_match_iso.Write()
    h_200_trk_cut1_match_pt.Write()
    h_200_trk_cut1_match_eta.Write()
    h_200_trk_cut1_match_phi.Write()
    h_200_trk_cut1_match_d0.Write()
    h_200_trk_cut1_match_chi2dof.Write()
    h_200_trk_cut1_match_chi2rphi.Write()
    h_200_trk_cut1_match_chi2rz.Write()
    h_200_trk_cut1_match_bendchi2.Write()
    h_200_trk_cut1_match_MVA1.Write()
    h_200_trk_cut1_pion_plus.Write()
    h_200_trk_cut1_pion_minus.Write()
    h_200_trk_cut1_Bs.Write()
    h_200_trk_cut2_match_dR.Write()
    h_200_trk_cut2_match_iso.Write()
    h_200_trk_cut2_match_pt.Write()
    h_200_trk_cut2_match_eta.Write()
    h_200_trk_cut2_match_phi.Write()
    h_200_trk_cut2_match_d0.Write()
    h_200_trk_cut2_match_chi2dof.Write()
    h_200_trk_cut2_match_chi2rphi.Write()
    h_200_trk_cut2_match_chi2rz.Write()
    h_200_trk_cut2_match_bendchi2.Write()
    h_200_trk_cut2_match_MVA1.Write()
    h_200_trk_cut2_pion_plus.Write()
    h_200_trk_cut2_pion_minus.Write()
    h_200_trk_cut2_Bs.Write()
    h_200_trk_cut3_match_dR.Write()
    h_200_trk_cut3_match_iso.Write()
    h_200_trk_cut3_match_pt.Write()
    h_200_trk_cut3_match_eta.Write()
    h_200_trk_cut3_match_phi.Write()
    h_200_trk_cut3_match_d0.Write()
    h_200_trk_cut3_match_chi2dof.Write()
    h_200_trk_cut3_match_chi2rphi.Write()
    h_200_trk_cut3_match_chi2rz.Write()
    h_200_trk_cut3_match_bendchi2.Write()
    h_200_trk_cut3_match_MVA1.Write()
    h_200_trk_cut3_pion_plus.Write()
    h_200_trk_cut3_pion_minus.Write()
    h_200_trk_cut3_Bs.Write()
    h_200_trk_cut4_match_dR.Write()
    h_200_trk_cut4_match_iso.Write()
    h_200_trk_cut4_match_pt.Write()
    h_200_trk_cut4_match_eta.Write()
    h_200_trk_cut4_match_phi.Write()
    h_200_trk_cut4_match_d0.Write()
    h_200_trk_cut4_match_chi2dof.Write()
    h_200_trk_cut4_match_chi2rphi.Write()
    h_200_trk_cut4_match_chi2rz.Write()
    h_200_trk_cut4_match_bendchi2.Write()
    h_200_trk_cut4_match_MVA1.Write()
    h_200_trk_cut4_pion_plus.Write()
    h_200_trk_cut4_pion_minus.Write()
    h_200_trk_cut4_Bs.Write()
    h_200_trk_match_ntrk.Write()
    h_200_trk_cut1_match_ntrk.Write()
    h_200_trk_cut2_match_ntrk.Write()
    h_200_trk_cut3_match_ntrk.Write()
    h_200_trk_cut4_match_ntrk.Write()
    print(nct)

if args.fname == 'minBias':
    nct=0
    start_time = time.time()
    npu = 'minBias'
    ensureDir('Plots'+str(npu)+'')

    file_list = ['/eos/cms/store/user/chuh/l1p2/MinBias/MinBias_TuneCP5_14TeV-pythia8_GTT_'+str(args.pnevt_PU0)+'.root']
    tree = ROOT.TChain("L1TrackNtuple/eventTree")
    for file_name in file_list:
        tree.Add(file_name)
    Nevt = tree.GetEntries()

    print('Total Number of events = ', Nevt)

    evt = -1
    for entry in tree:
        evt+=1
        if evt%500==0: 
            time_elapsed = time.time() - start_time
            print('{0:.2f}'.format(float(evt)/float(Nevt)*100.), '% processed ', '{0:.2f}'.format(float(evt)/float(time_elapsed)), 'Hz')

        sumpt=0
        cnt1=0
        cnt2=0
        ntrk0 = 0
        ntrk1 = 0
        ntrk2 = 0
        ntrk3 = 0
        ntrk4 = 0

        for itrk in range(len(tree.trk_pt)):
            dRmin = 999.
            dRiso = 999.
            for jtrk in range(len(tree.trk_pt)):
                sumpt += tree.trk_pt[jtrk] 
                if itrk == jtrk:
                    continue
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
                if dR < dRiso:
                    dRiso = dR

            cnt2+=1
            ntrk0+=1
            
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

            if not tree.trk_MVA1[itrk] < 0.997: continue
            ntrk1+=1
            h_MinBias_trk_cut1_dR.Fill(dRmin)
            h_MinBias_trk_cut1_iso.Fill(dRiso)
            h_MinBias_trk_cut1_pt.Fill(tree.trk_pt[itrk])
            h_MinBias_trk_cut1_eta.Fill(tree.trk_eta[itrk])
            h_MinBias_trk_cut1_phi.Fill(tree.trk_phi[itrk])
            h_MinBias_trk_cut1_d0.Fill(tree.trk_d0[itrk])
            h_MinBias_trk_cut1_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_MinBias_trk_cut1_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_MinBias_trk_cut1_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_MinBias_trk_cut1_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_MinBias_trk_cut1_MVA1.Fill(tree.trk_MVA1[itrk])
            if not abs(tree.trk_eta[itrk]) < 2 : continue
            ntrk2+=1
            h_MinBias_trk_cut2_dR.Fill(dRmin)
            h_MinBias_trk_cut2_iso.Fill(dRiso)
            h_MinBias_trk_cut2_pt.Fill(tree.trk_pt[itrk])
            h_MinBias_trk_cut2_eta.Fill(tree.trk_eta[itrk])
            h_MinBias_trk_cut2_phi.Fill(tree.trk_phi[itrk])
            h_MinBias_trk_cut2_d0.Fill(tree.trk_d0[itrk])
            h_MinBias_trk_cut2_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_MinBias_trk_cut2_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_MinBias_trk_cut2_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_MinBias_trk_cut2_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_MinBias_trk_cut2_MVA1.Fill(tree.trk_MVA1[itrk])
            if not dRiso < 0.3: continue
            ntrk3+=1
            h_MinBias_trk_cut3_dR.Fill(dRmin)
            h_MinBias_trk_cut3_iso.Fill(dRiso)
            h_MinBias_trk_cut3_pt.Fill(tree.trk_pt[itrk])
            h_MinBias_trk_cut3_eta.Fill(tree.trk_eta[itrk])
            h_MinBias_trk_cut3_phi.Fill(tree.trk_phi[itrk])
            h_MinBias_trk_cut3_d0.Fill(tree.trk_d0[itrk])
            h_MinBias_trk_cut3_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_MinBias_trk_cut3_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_MinBias_trk_cut3_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_MinBias_trk_cut3_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_MinBias_trk_cut3_MVA1.Fill(tree.trk_MVA1[itrk])
            if not dRiso < 0.2: continue
            ntrk4+=1
            h_MinBias_trk_cut4_dR.Fill(dRmin)
            h_MinBias_trk_cut4_iso.Fill(dRiso)
            h_MinBias_trk_cut4_pt.Fill(tree.trk_pt[itrk])
            h_MinBias_trk_cut4_eta.Fill(tree.trk_eta[itrk])
            h_MinBias_trk_cut4_phi.Fill(tree.trk_phi[itrk])
            h_MinBias_trk_cut4_d0.Fill(tree.trk_d0[itrk])
            h_MinBias_trk_cut4_chi2dof.Fill(tree.trk_chi2dof[itrk])
            h_MinBias_trk_cut4_chi2rphi.Fill(tree.trk_chi2rphi[itrk])
            h_MinBias_trk_cut4_chi2rz.Fill(tree.trk_chi2rz[itrk])
            h_MinBias_trk_cut4_bendchi2.Fill(tree.trk_bendchi2[itrk])
            h_MinBias_trk_cut4_MVA1.Fill(tree.trk_MVA1[itrk])

        h_MinBias_trk_match_ntrk.Fill(ntrk0)
        h_MinBias_trk_cut1_match_ntrk.Fill(ntrk1)
        h_MinBias_trk_cut2_match_ntrk.Fill(ntrk2)
        h_MinBias_trk_cut3_match_ntrk.Fill(ntrk3)
        h_MinBias_trk_cut4_match_ntrk.Fill(ntrk4)
        

    h_MinBias_trk_dR.Write()
    h_MinBias_trk_iso.Write()
    h_MinBias_trk_pt.Write()
    h_MinBias_trk_eta.Write()
    h_MinBias_trk_phi.Write()
    h_MinBias_trk_z0.Write()
    h_MinBias_trk_d0.Write()
    h_MinBias_trk_nstub.Write()
    h_MinBias_trk_chi2dof.Write()
    h_MinBias_trk_chi2rphi.Write()
    h_MinBias_trk_chi2rz.Write()
    h_MinBias_trk_bendchi2.Write()
    h_MinBias_trk_MVA1.Write()

    h_MinBias_trk_cut1_dR.Write()
    h_MinBias_trk_cut1_iso.Write()
    h_MinBias_trk_cut1_pt.Write()
    h_MinBias_trk_cut1_eta.Write()
    h_MinBias_trk_cut1_phi.Write()
    h_MinBias_trk_cut1_d0.Write()
    h_MinBias_trk_cut1_chi2dof.Write()
    h_MinBias_trk_cut1_chi2rphi.Write()
    h_MinBias_trk_cut1_chi2rz.Write()
    h_MinBias_trk_cut1_bendchi2.Write()
    h_MinBias_trk_cut1_MVA1.Write()
    h_MinBias_trk_cut2_dR.Write()
    h_MinBias_trk_cut2_iso.Write()
    h_MinBias_trk_cut2_pt.Write()
    h_MinBias_trk_cut2_eta.Write()
    h_MinBias_trk_cut2_phi.Write()
    h_MinBias_trk_cut2_d0.Write()
    h_MinBias_trk_cut2_chi2dof.Write()
    h_MinBias_trk_cut2_chi2rphi.Write()
    h_MinBias_trk_cut2_chi2rz.Write()
    h_MinBias_trk_cut2_bendchi2.Write()
    h_MinBias_trk_cut2_MVA1.Write()
    h_MinBias_trk_cut3_dR.Write()
    h_MinBias_trk_cut3_iso.Write()
    h_MinBias_trk_cut3_pt.Write()
    h_MinBias_trk_cut3_eta.Write()
    h_MinBias_trk_cut3_phi.Write()
    h_MinBias_trk_cut3_d0.Write()
    h_MinBias_trk_cut3_chi2dof.Write()
    h_MinBias_trk_cut3_chi2rphi.Write()
    h_MinBias_trk_cut3_chi2rz.Write()
    h_MinBias_trk_cut3_bendchi2.Write()
    h_MinBias_trk_cut3_MVA1.Write()
    h_MinBias_trk_cut4_dR.Write()
    h_MinBias_trk_cut4_iso.Write()
    h_MinBias_trk_cut4_pt.Write()
    h_MinBias_trk_cut4_eta.Write()
    h_MinBias_trk_cut4_phi.Write()
    h_MinBias_trk_cut4_d0.Write()
    h_MinBias_trk_cut4_chi2dof.Write()
    h_MinBias_trk_cut4_chi2rphi.Write()
    h_MinBias_trk_cut4_chi2rz.Write()
    h_MinBias_trk_cut4_bendchi2.Write()
    h_MinBias_trk_cut4_MVA1.Write()
    h_MinBias_trk_match_ntrk.Write()
    h_MinBias_trk_cut1_match_ntrk.Write()
    h_MinBias_trk_cut2_match_ntrk.Write()
    h_MinBias_trk_cut3_match_ntrk.Write()
    h_MinBias_trk_cut4_match_ntrk.Write()

ofile.Close()