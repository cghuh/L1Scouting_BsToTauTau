import os
import ROOT
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from array import array

ROOT.gROOT.SetBatch(True)
officialStyle(ROOT.gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

ofile = ROOT.TFile("plot.root", "RECREATE")

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_histogram(file, hist_name):
    hist = file.Get(hist_name)
    return hist

def comparisonPlots(hist1, hist2, isLog=False, pname='sync.pdf', isScale = False, isGen=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname,"",700,700)
    if isLog:
        c1.SetLogy()
        hist1.GetYaxis().SetRangeUser(1e-4,2)
    if isScale:
        hist1.Scale(1./hist1.GetSumOfWeights())
        hist2.Scale(1./hist2.GetSumOfWeights())
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.SetLineColor(1)
    hist1.SetMarkerColor(1)
    hist1.Draw('ep')
    hist2.Draw('epsame')

    cms_lat=ROOT.TLatex()
    cms_lat.SetTextSize(0.05)
    cms_lat.DrawLatex(hist1.GetXaxis().GetBinLowEdge(1),2.2,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    cms_lat.DrawLatex(hist1.GetXaxis().GetBinLowEdge(hist1.GetNbinsX()),2.2,"#scale[0.9]{14 TeV}")

    if isLegend:
        leg = ROOT.TLegend(0.40, 0.68, 0.9, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        if isGen:
            leg.AddEntry(hist1, "Gen", 'lp')
            leg.AddEntry(hist2, "TTrack", 'lp')
        else:
            leg.AddEntry(hist2, "H #rightarrow #tau#tau, PU 200", 'lp')
            leg.AddEntry(hist1, "minBias", 'lp')
        leg.Draw()

    c1.Print(pname)
    ofile.cd()
    c1.Write()


# Ensure directory for output plots exists
ensureDir('Plots_compare')

# Open ROOT file and retrieve histograms
file = ROOT.TFile.Open('output.root')

# Define list of histogram names
hist_names = [
    "h_PU200_gen_pt",          "h_minBias_gen_pt",
    "h_PU200_gen_eta",         "h_minBias_gen_eta",
    "h_PU200_gen_phi",         "h_minBias_gen_phi",
    "h_PU200_trk_pt",          "h_minBias_trk_pt", 
    "h_PU200_trk_eta",         "h_minBias_trk_eta", 
    "h_PU200_trk_phi",         "h_minBias_trk_phi", 
    "h_PU200_trk_d0",          "h_minBias_trk_d0", 
    "h_PU200_trk_z0",          "h_minBias_trk_z0", 
    "h_PU200_trk_MVA",         "h_minBias_trk_MVA", 
    "h_PU200_trk_ntrk",        "h_minBias_trk_ntrk", 
    "h_PU200_trk_cut0_pt",     "h_minBias_trk_cut0_pt", 
    "h_PU200_trk_cut0_eta",    "h_minBias_trk_cut0_eta", 
    "h_PU200_trk_cut0_phi",    "h_minBias_trk_cut0_phi", 
    "h_PU200_trk_cut0_d0",     "h_minBias_trk_cut0_d0", 
    "h_PU200_trk_cut0_z0",     "h_minBias_trk_cut0_z0", 
    "h_PU200_trk_cut0_MVA",    "h_minBias_trk_cut0_MVA", 
]

for i in range(0, len(hist_names), 3):
    hist1 = get_histogram(file, hist_names[i])
    hist2 = get_histogram(file, hist_names[i+1])
  
    if hist1 and hist2 and hist3:
        comparisonPlots(hist1, hist2, True, 'Plots_compare/compares_' + hist1.GetName() + '.png', True, False, True)

file.Close()
ofile.Close()
