import os, math, sys
import time
from DeltaR import returndR
from DeltaR import returndRs
import copy
import random
import ROOT
import argparse
import numpy as np

from officialStyle import officialStyle

ROOT.gROOT.SetBatch(True)
officialStyle(ROOT.gStyle)
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
    c1 = ROOT.TCanvas(cname,"",700,700)
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
    c1 = ROOT.TCanvas(cname,"",700,700)
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
    c1 = ROOT.TCanvas(cname,"",700,700)
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
    c1 = ROOT.TCanvas(cname,"",700,700)
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
    c1 = ROOT.TCanvas(cname,"",1400,700)
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
    c1 = ROOT.TCanvas(cname,"",700,700)
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
    c1 = ROOT.TCanvas(cname,"",700,700)
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

h_200_trk_pt         = ROOT.TH1F("h_200_trk_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_eta        = ROOT.TH1F("h_200_trk_eta",";#eta",250,-2.5,2.5)
h_200_trk_phi        = ROOT.TH1F("h_200_trk_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_d0         = ROOT.TH1F("h_200_trk_d0",";d0",200,-1,1)
h_200_trk_z0         = ROOT.TH1F("h_200_trk_z0",";z",300,-15,15)
h_200_trk_nstub      = ROOT.TH1F("h_200_trk_nstub",";nstub",8,2,10)
h_200_trk_chi2dof    = ROOT.TH1F("h_200_trk_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_chi2rphi   = ROOT.TH1F("h_200_trk_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_chi2rz     = ROOT.TH1F("h_200_trk_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_bendchi2   = ROOT.TH1F("h_200_trk_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_MVA1       = ROOT.TH1F("h_200_trk_MVA1",";MVA1",5000,0,1)
h_200_trk_match_pt         = ROOT.TH1F("h_200_trk_match_pt",";p_{T} [GeV]",400,0,20)
h_200_trk_match_eta        = ROOT.TH1F("h_200_trk_match_eta",";#eta",250,-2.5,2.5)
h_200_trk_match_phi        = ROOT.TH1F("h_200_trk_match_phi",";#phi",50,-math.pi,math.pi)
h_200_trk_match_d0         = ROOT.TH1F("h_200_trk_match_d0",";d0",200,-1,1)
h_200_trk_match_z0         = ROOT.TH1F("h_200_trk_match_z0",";z",300,-15,15)
h_200_trk_match_nstub      = ROOT.TH1F("h_200_trk_match_nstub",";nstub",8,2,10)
h_200_trk_match_chi2dof    = ROOT.TH1F("h_200_trk_match_chi2dof",";#chi^{2}/dof",400,0,20)
h_200_trk_match_chi2rphi   = ROOT.TH1F("h_200_trk_match_chi2rphi",";#chi^{2}rphi",400,0,20)
h_200_trk_match_chi2rz     = ROOT.TH1F("h_200_trk_match_chi2rz",";#chi^{2}rz",200,0,10)
h_200_trk_match_bendchi2   = ROOT.TH1F("h_200_trk_match_bendchi2",";bend #chi^{2}",200,0,10)
h_200_trk_match_MVA1       = ROOT.TH1F("h_200_trk_match_MVA1",";MVA1",5000,0,1)

h_MinBias_trk_pt         = ROOT.TH1F("h_MinBias_trk_pt",";p_{T} [GeV]",400,0,20)
h_MinBias_trk_eta        = ROOT.TH1F("h_MinBias_trk_eta",";#eta",250,-2.5,2.5)
h_MinBias_trk_phi        = ROOT.TH1F("h_MinBias_trk_phi",";#phi",50,-math.pi,math.pi)
h_MinBias_trk_d0         = ROOT.TH1F("h_MinBias_trk_d0",";d0",200,-1,1)
h_MinBias_trk_z0         = ROOT.TH1F("h_MinBias_trk_z0",";z",300,-15,15)
h_MinBias_trk_nstub      = ROOT.TH1F("h_MinBias_trk_nstub",";nstub",8,2,10)
h_MinBias_trk_chi2dof    = ROOT.TH1F("h_MinBias_trk_chi2dof",";#chi^{2}/dof",400,0,20)
h_MinBias_trk_chi2rphi   = ROOT.TH1F("h_MinBias_trk_chi2rphi",";#chi^{2}rphi",400,0,20)
h_MinBias_trk_chi2rz     = ROOT.TH1F("h_MinBias_trk_chi2rz",";#chi^{2}rz",200,0,10)
h_MinBias_trk_bendchi2   = ROOT.TH1F("h_MinBias_trk_bendchi2",";bend #chi^{2}",200,0,10)
h_MinBias_trk_MVA1       = ROOT.TH1F("h_MinBias_trk_MVA1",";MVA1",5000,0,1)

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
            dRsmin = 999.

            for jtrk in range(len(tree.trk_pt)):
                if itrk == jtrk:
                    continue
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
                if dR < dRiso:
                    dRiso = dR
                dR = returndRs(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_z0[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk], tree.trk_z0[jtrk])
                if dR < dRsmin:
                    dRsmin = dR
            ntrk0+=1
            if tree.trk_MVA1[itrk] < 0.997 : 
                ntrk1+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2: 
                ntrk2+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRiso < 0.3: 
                ntrk3+=1
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRsmin < 0.3: 
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
            dRsmin = 999.
            dRsmax = -999.
            dRsmax1 = -999.
            dRsmax2 = -999.
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
                dR = returndRs(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_z0[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk], tree.trk_z0[jtrk])
                if dR < dRsmin:
                    dRsmin = dR
                if dRmin < 0.02:
                    dRtmp = 999.
                    for igen in range(len(tree.gen_pt)):
                        if (abs(tree.gen_mpdgid[igen]) == 15 and abs(tree.gen_pdgid[igen]) == 211 and tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                            dRt = returndR(tree.trk_eta[jtrk], tree.trk_phi[jtrk], tree.gen_eta[igen], tree.gen_phi[igen])
                            if dRt < dRtmp:
                                dRtmp = dRt
                    if dRtmp < 0.02 and dR > dRsmax:
                        dRsmax = dR
                    if dRtmp < 0.02 and dR > dRsmax1 and gen_mpdgid > 0 and tree.gen_mpdgid[igen] > 0:
                        dRsmax1 = dR
                    if dRtmp < 0.02 and dR > dRsmax2 and gen_mpdgid < 0 and tree.gen_mpdgid[igen] < 0:
                        dRsmax2 = dR

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
            if tree.trk_MVA1[itrk] < 0.997 and abs(tree.trk_eta[itrk]) < 2 and dRsmin < 0.3: 
                h_200_trk_cut4_phi_eta_z0.Fill(tree.trk_z0[itrk], tree.trk_phi[itrk],tree.trk_eta[itrk])

            cnt2+=1
            if dRmin < 0.02:
                cnt1+=1
                h_200_trk_match_dR.Fill(dRmin)
                h_200_trk_match_iso.Fill(dRiso)
                h_200_trk_match_dRsMin.Fill(dRsmin)
                h_200_trk_match_dRsMax.Fill(dRsmax)
                h_200_trk_match_dRsMax1.Fill(dRsmax1)
                h_200_trk_match_dRsMax2.Fill(dRsmax2)
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
            dRsmin = 999.
            for jtrk in range(len(tree.trk_pt)):
                sumpt += tree.trk_pt[jtrk] 
                if itrk == jtrk:
                    continue
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
                if dR < dRiso:
                    dRiso = dR
                dR = returndRs(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_z0[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk], tree.trk_z0[jtrk])
                if dR < dRsmin:
                    dRsmin = dR

            cnt2+=1
            ntrk0+=1
            
            h_MinBias_trk_dR.Fill(dRmin)
            h_MinBias_trk_iso.Fill(dRiso)
            h_MinBias_trk_dRsMin.Fill(dRsmin)
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

ofile.Close()
