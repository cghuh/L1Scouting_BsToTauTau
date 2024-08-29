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

def efficienciesPlot(hist_PU0, hist_PU200, hist_minBias, isLog=False, pname='sync.pdf'):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname,"",700,700)
    if isLog:
        c1.SetLogy()
    hist0 = ROOT.TH1F("eff_pu0", "", 4,0,4)
    hist1 = ROOT.TH1F("eff_pu200", "", 4,0,4)
    hist2 = ROOT.TH1F("eff_minBias", "", 4,0,4)
    hist0.SetBinContent(1, hist_PU0[1].Integral()/hist_PU0[0].Integral())
    hist0.SetBinContent(2, hist_PU0[2].Integral()/hist_PU0[0].Integral())
    hist0.SetBinContent(3, hist_PU0[3].Integral()/hist_PU0[0].Integral())
    hist0.SetBinContent(4, hist_PU0[4].Integral()/hist_PU0[0].Integral())
    hist1.SetBinContent(1, hist_PU200[1].Integral()/hist_PU200[0].Integral())
    hist1.SetBinContent(2, hist_PU200[2].Integral()/hist_PU200[0].Integral())
    hist1.SetBinContent(3, hist_PU200[3].Integral()/hist_PU200[0].Integral())
    hist1.SetBinContent(4, hist_PU200[4].Integral()/hist_PU200[0].Integral())
    hist0.SetLineColor(4)
    hist0.SetMarkerColor(4)
    hist1.SetLineColor(2)
    hist1.SetMarkerColor(2)
    hist0.GetYaxis().SetRangeUser(0,1.0)
    hist0.Draw('ep')
    hist1.Draw('epsame')
    if hist_minBias:
        hist2.SetBinContent(1, hist_minBias[1].Integral()/hist_minBias[0].Integral())
        hist2.SetBinContent(2, hist_minBias[2].Integral()/hist_minBias[0].Integral())
        hist2.SetBinContent(3, hist_minBias[3].Integral()/hist_minBias[0].Integral())
        hist2.SetBinContent(4, hist_minBias[4].Integral()/hist_minBias[0].Integral())
        hist2.SetLineColor(1)
        hist2.SetMarkerColor(1)
        hist2.Draw('epsame')

    leg = ROOT.TLegend(0.40, 0.68, 0.9, 0.88)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.05)
    leg.AddEntry(hist0, "B_{s}#rightarrow#tau#tau, PU0", 'lp')
    leg.AddEntry(hist1, "B_{s}#rightarrow#tau#tau, PU200", 'lp')
    if hist_minBias:
        leg.AddEntry(hist2, "MinBias", 'lp')
    leg.Draw()

    c1.Print(pname)
    ofile.cd()
    c1.Write()

def efficiencies(hist1, hist2, hist3, hist4, hist5, isLog=False, pname='sync.pdf'):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname,"",700,700)
    if isLog:
        c1.SetLogy()
    hist = ROOT.TH1F("eff", "", 4,0,4)
    hist.SetBinContent(1, hist2.Integral()/hist1.Integral())
    hist.SetBinContent(2, hist3.Integral()/hist1.Integral())
    hist.SetBinContent(3, hist4.Integral()/hist1.Integral())
    hist.SetBinContent(4, hist5.Integral()/hist1.Integral())
    hist.SetLineColor(1)
    hist.SetMarkerColor(1)
    hist.GetYaxis().SetRangeUser(0,0.5)
    if "trk_match" in str(hist1.GetName()): hist.GetYaxis().SetRangeUser(0,2)
    hist.Draw('ep')

    c1.Print(pname)
    ofile.cd()
    c1.Write()

def comparisonPlots(hist1, hist2, isLog=False, pname='sync.pdf', isScale = False, isGen=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname,"",700,700)
    #hist1.SetMaximum(0.05)
    if "dRsMax" in str(hist1.GetName()): 
        hist1.Rebin(2)
        hist2.Rebin(2)
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
            leg.AddEntry(hist1, "B_{s} #rightarrow #tau#tau, PU0", 'lp')
            leg.AddEntry(hist2, "B_{s} #rightarrow #tau#tau, PU200", 'lp')
        leg.Draw()

    c1.Print(pname)
    ofile.cd()
    c1.Write()

def comparison3Plots(hist1, hist2, hist3, isLog=False, pname='sync.pdf', isScale=False, isPipm=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname, "", 700, 700)
    hist1.SetMaximum(8)
    if isLog:
        c1.SetLogy()
    if isScale:
        hist1.Scale(1./hist1.GetSumOfWeights())
        hist2.Scale(1./hist2.GetSumOfWeights())
        if(hist3.Integral()>0): hist3.Scale(1./hist3.GetSumOfWeights())
        hist3.GetYaxis().SetRangeUser(1e-4, 2)
    if "MVA" in str(hist1.GetName()):
        hist3.GetXaxis().SetRangeUser(0.98, 1)
    hist3.SetLineColor(1)
    hist3.SetMarkerColor(1)
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.SetLineColor(4)
    hist1.SetMarkerColor(4)
    hist1.SetLineWidth(2)
    hist2.SetLineWidth(2)
    hist3.SetLineWidth(2)
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
            leg.AddEntry(hist1, "B_{s}#rightarrow#tau#tau, PU0", 'lp')
            leg.AddEntry(hist2, "B_{s}#rightarrow#tau#tau, PU200", 'lp')
            leg.AddEntry(hist3, "MinBias", 'lp')
        leg.Draw()
    c1.Print(pname)
    ofile.cd()
    c1.Write()

def comparison3_2DPlots(hist2D1, hist2D2, hist2D3, isLog=False, pname='sync.pdf', isScale=False, isPipm=False, isLegend=False):
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname, "", 700, 700)
    nybins = hist2D1.GetNbinsY()

    if "efficiency" in str(hist2D1.GetName()): 
        if "dRs" in str(hist2D1.GetName()): 
            h1 = ROOT.TH1D("eff_PU0", ";cone size;#epsilon_{clustering}", 5,0.3,0.8)
            h2 = ROOT.TH1D("eff_PU200", ";cone size;#epsilon_{clustering}", 5,0.3,0.8)
            h3 = ROOT.TH1D("eff_minBias", ";cone size;#epsilon_{clustering}", 5,0.3,0.8)
        else:
            h1 = ROOT.TH1D("eff_PU0", ";cone size;#epsilon_{clustering}", 5,0.1,0.6)
            h2 = ROOT.TH1D("eff_PU200", ";cone size;#epsilon_{clustering}", 5,0.1,0.6)
            h3 = ROOT.TH1D("eff_minBias", ";cone size;#epsilon_{clustering}", 5,0.1,0.6)

            # Iterate over Y bins to project and analyze
    for ybin in range(1, nybins + 1):
        hist1 = hist2D1.ProjectionX(f"{hist2D1.GetName()}_px_{ybin}", ybin, ybin)
        hist2 = hist2D2.ProjectionX(f"{hist2D2.GetName()}_px_{ybin}", ybin, ybin)
        hist3 = hist2D3.ProjectionX(f"{hist2D3.GetName()}_px_{ybin}", ybin, ybin)

        # Handle efficiency calculations
        if "efficiency" in str(hist2D1.GetName()): 
            if hist1.Integral() > 0: 
                h1.SetBinContent(ybin, hist1.GetBinContent(2)/hist1.Integral(1,2))
            if hist2.Integral() > 0: 
                h2.SetBinContent(ybin, hist2.GetBinContent(2)/hist2.Integral(1,2))
            if hist3.Integral() > 0: 
                h3.SetBinContent(ybin, hist3.GetBinContent(2)/hist3.Integral(1,2))


        if isLog:
            c1.SetLogy()
        if isScale:
            if(hist1.Integral()>0): hist1.Scale(1./hist1.GetSumOfWeights())
            if(hist2.Integral()>0): hist2.Scale(1./hist2.GetSumOfWeights())
            if(hist3.Integral()>0): hist3.Scale(1./hist3.GetSumOfWeights())
            hist1.GetYaxis().SetRangeUser(1e-4, 2)
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
            if "dRs" in str(hist2D1.GetName()): leg.SetHeader(f"cluster size {0.2+0.1*ybin:.1f}")
            else: leg.SetHeader(f"cluster size {0.0+0.1*ybin:.1f}")
            leg.AddEntry(hist1, "B_{s}#rightarrow#tau#tau, PU0", 'lp')
            leg.AddEntry(hist2, "B_{s}#rightarrow#tau#tau, PU200", 'lp')
            leg.AddEntry(hist3, "MinBias", 'lp')
            leg.Draw()
        if not "efficiency" in str(hist2D1.GetName()): 
            c1.Print(pname.replace("_h_", "_h_"+f"{ybin}"))
            ofile.cd()
            c1.Write()

    if "efficiency" in str(hist2D1.GetName()): 
        c1.SetLogy(0)
        h1.SetLineColor(4)
        h2.SetLineColor(2)
        h3.SetLineColor(1)
        h1.SetMarkerColor(4)
        h2.SetMarkerColor(2)
        h3.SetMarkerColor(1)
        h1.GetYaxis().SetRangeUser(0, 1)
        h1.Draw('ep')
        h2.Draw('epsame')
        h3.Draw('epsame')
        #h1 = ROOT.TH1D("eff_PU0", ";#epsilon_{clustering}", 4,0.1,0.5)
        if isLegend:
            leg = ROOT.TLegend(0.40, 0.28, 0.9, 0.48)
            leg.SetBorderSize(0)
            leg.SetFillColor(10)
            leg.SetLineColor(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.05)
            leg.AddEntry(h1, "B_{s}#rightarrow#tau#tau, PU0", 'lp')
            leg.AddEntry(h2, "B_{s}#rightarrow#tau#tau, PU200", 'lp')
            leg.AddEntry(h3, "minBias", 'lp')
            leg.Draw()
        c1.Print(pname)
        ofile.cd()
        c1.Write()

def comparisonROC(hist1, hist2, hist3, pname='sync.pdf', isLegend=False):
    # Remove specific strings from the canvas name
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    
    # Create a canvas
    c1 = ROOT.TCanvas(cname, "", 700, 700)
    
    # Initialize lists for ROC curve points
    x1 = []
    y1 = []
    x2 = []
    if "MVA" in str(hist1.GetName()):
        hist1.GetXaxis().SetRangeUser(0, 1)
        hist2.GetXaxis().SetRangeUser(0, 1)
        hist3.GetXaxis().SetRangeUser(0, 1)
    
    # Calculate the ROC curve points
    if "eta" in str(hist1.GetName()):
        for i in range(1, 250):
            x1.append((hist1.Integral(i, 250)+hist1.Integral(251,hist1.GetNbinsX()+1-i)) / hist1.Integral())
            x2.append((hist2.Integral(i, 250)+hist2.Integral(251,hist2.GetNbinsX()+1-i)) / hist2.Integral())
            y1.append(1 - ((hist3.Integral(i, 250)+hist3.Integral(251,hist3.GetNbinsX()+1-i)) / hist3.Integral()))
            # if i==50: print(str((hist1.Integral(i, 250)+hist1.Integral(251,hist1.GetNbinsX()+1-i)) / hist1.Integral())+", "+str(1 - ((hist3.Integral(i, 250)+hist3.Integral(251,hist3.GetNbinsX()+1-i)) / hist3.Integral())))
            # if i==200: print(str((hist1.Integral(i, 250)+hist1.Integral(251,hist1.GetNbinsX()+1-i)) / hist1.Integral())+", "+str(1 - ((hist3.Integral(i, 250)+hist3.Integral(251,hist3.GetNbinsX()+1-i)) / hist3.Integral())))
    elif "d0" in str(hist1.GetName()):
        for i in range(1, 100):
            x1.append((hist1.Integral(i, 100)+hist1.Integral(101,hist1.GetNbinsX()+1-i)) / hist1.Integral())
            x2.append((hist2.Integral(i, 100)+hist2.Integral(101,hist2.GetNbinsX()+1-i)) / hist2.Integral())
            y1.append(1 - ((hist3.Integral(i, 100)+hist3.Integral(101,hist3.GetNbinsX()+1-i)) / hist3.Integral()))
            # if i==80: print(str((hist2.Integral(i, 100)+hist2.Integral(101,hist2.GetNbinsX()+1-i)) / hist2.Integral())+", "+str(1 - ((hist3.Integral(i, 100)+hist3.Integral(101,hist3.GetNbinsX()+1-i)) / hist3.Integral())))
    elif "pt" in str(hist1.GetName()):
        for i in range(1, hist1.GetNbinsX() + 1):
            x1.append(hist1.Integral(i, hist1.GetNbinsX() + 1) / hist1.Integral())
            x2.append(hist2.Integral(i, hist2.GetNbinsX() + 1) / hist2.Integral())
            y1.append(1 - (hist3.Integral(i, hist1.GetNbinsX() + 1) / hist3.Integral()))
            #if i==60: print(str(hist2.Integral(i, hist2.GetNbinsX() + 1) / hist2.Integral())+", "+ str(1 - (hist3.Integral(i, hist1.GetNbinsX() + 1) / hist3.Integral())))
    else:
        for i in range(1, hist1.GetNbinsX() + 1):
            x1.append(hist1.Integral(1, i) / hist1.Integral())
            x2.append(hist2.Integral(1, i) / hist2.Integral())
            y1.append(1 - (hist3.Integral(1, i) / hist3.Integral()))
            # if "MVA" in str(hist1.GetName()):
            #     if i==4985: print(str(hist2.Integral(1, i) / hist2.Integral())+", "+str(1 - (hist3.Integral(1, i) / hist3.Integral())))
            # if "iso" in str(hist1.GetName()):
            #     if i==20: print(str(hist2.Integral(1, i) / hist2.Integral())+", "+str(1 - (hist3.Integral(1, i) / hist3.Integral())))
            #     if i==30: print(str(hist2.Integral(1, i) / hist2.Integral())+", "+str(1 - (hist3.Integral(1, i) / hist3.Integral())))
            # if "dRsMin" in str(hist1.GetName()):
            #     if i==30: print(str(hist2.Integral(1, i) / hist2.Integral())+", "+str(1 - (hist3.Integral(1, i) / hist3.Integral())))
            #     if i==40: print(str(hist2.Integral(1, i) / hist2.Integral())+", "+str(1 - (hist3.Integral(1, i) / hist3.Integral())))
    
    # Create TGraph objects for the ROC curves
    g1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
    g2 = ROOT.TGraph(len(x2), array('d', x2), array('d', y1))
    
    # Set graph styles
    g1.SetLineColor(1)
    g1.SetMarkerColor(1)
    g2.SetLineColor(2)
    g2.SetMarkerColor(2)
    g1.GetXaxis().SetTitle("#epsilon_{B_{s} #rightarrow #tau#tau}")
    g1.GetYaxis().SetTitle("1-#epsilon_{minBias}")
    g1.GetXaxis().SetLimits(0, 1)
    g1.GetYaxis().SetRangeUser(0, 1)
    
    # Draw the ROC curves
    g1.Draw('ALP')
    g2.Draw('LP same')
    
    # Add legend if specified
    if isLegend:
        leg = ROOT.TLegend(0.40, 0.58, 0.9, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.SetHeader(hist1.GetXaxis().GetTitle())
        leg.AddEntry(g1, "B_{s} #rightarrow #tau#tau, PU0", 'lp')
        leg.AddEntry(g2, "B_{s} #rightarrow #tau#tau, PU200", 'lp')
        leg.Draw()
    
    # Save the canvas
    c1.Print(pname)
    ofile.cd()
    c1.Write()

def DrawROC(hist1, hist2, hist3, pname='sync.pdf', isLegend=False):
    # Remove specific strings from the canvas name
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    
    # Create a canvas
    c1 = ROOT.TCanvas(cname, "", 700, 700)
    
    # Initialize lists for ROC curve points
    x1 = []
    y1 = []
    x2 = []
    
    # Calculate the ROC curve points
    for i in range(1, hist1.GetNbinsY() + 1):
        x1.append(hist1.Integral(2, 50, i, i) / hist1.Integral(1, 50, i, i))
        x2.append(hist2.Integral(2, 50, i, i) / hist2.Integral(1, 50, i, i))
        y1.append(hist3.Integral(1, 1,  i, i) / hist3.Integral(1, 50, i, i))
    
    # Create TGraph objects for the ROC curves
    g1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
    g2 = ROOT.TGraph(len(x2), array('d', x2), array('d', y1))
    
    # Set graph styles
    g1.SetLineColor(1)
    g1.SetMarkerColor(1)
    g2.SetLineColor(2)
    g2.SetMarkerColor(2)
    g1.GetXaxis().SetTitle("#epsilon_{B_{s} #rightarrow #tau#tau}")
    g1.GetYaxis().SetTitle("1-#epsilon_{minBias}")
    g1.GetYaxis().SetNdivisions(505)
    g1.GetXaxis().SetLimits(0, 1)
    g1.GetYaxis().SetRangeUser(0.9, 1)
    
    # Draw the ROC curves
    g1.Draw('ALP')
    g2.Draw('LP same')
    
    # Add legend if specified
    if isLegend:
        leg = ROOT.TLegend(0.30, 0.50, 0.80, 0.80)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.SetHeader('Clustering performance')
        leg.AddEntry(g1, "B_{s} #rightarrow #tau#tau, PU0", 'lp')
        leg.AddEntry(g2, "B_{s} #rightarrow #tau#tau, PU200", 'lp')
        leg.Draw()
    
    # Save the canvas
    c1.Print(pname)
    ofile.cd()
    c1.Write()

# Ensure directory for output plots exists
ensureDir('Plots_compare')

# Open ROOT file and retrieve histograms
file = ROOT.TFile.Open('output.root')

# Define list of histogram names
hist_names = [
    "h_PU0_trk_pt",         "h_PU200_trk_pt",          "h_minBias_trk_pt", 
    "h_PU0_trk_eta",        "h_PU200_trk_eta",         "h_minBias_trk_eta", 
    "h_PU0_trk_phi",        "h_PU200_trk_phi",         "h_minBias_trk_phi", 
    "h_PU0_trk_d0",         "h_PU200_trk_d0",          "h_minBias_trk_d0", 
    "h_PU0_trk_z0",         "h_PU200_trk_z0",          "h_minBias_trk_z0", 
    "h_PU0_trk_MVA",        "h_PU200_trk_MVA",         "h_minBias_trk_MVA", 
    "h_PU0_trk_dR",         "h_PU200_trk_dR",          "h_minBias_trk_dR", 
    "h_PU0_trk_dz",         "h_PU200_trk_dz",          "h_minBias_trk_dz", 
    "h_PU0_trk_dRs",        "h_PU200_trk_dRs",         "h_minBias_trk_dRs", 
    "h_PU0_trk_ntrk",       "h_PU200_trk_ntrk",        "h_minBias_trk_ntrk", 
    "h_PU0_trk_cut0_pt",    "h_PU200_trk_cut0_pt",     "h_minBias_trk_cut0_pt", 
    "h_PU0_trk_cut0_eta",   "h_PU200_trk_cut0_eta",    "h_minBias_trk_cut0_eta", 
    "h_PU0_trk_cut0_phi",   "h_PU200_trk_cut0_phi",    "h_minBias_trk_cut0_phi", 
    "h_PU0_trk_cut0_d0",    "h_PU200_trk_cut0_d0",     "h_minBias_trk_cut0_d0", 
    "h_PU0_trk_cut0_z0",    "h_PU200_trk_cut0_z0",     "h_minBias_trk_cut0_z0", 
    "h_PU0_trk_cut0_MVA",   "h_PU200_trk_cut0_MVA",    "h_minBias_trk_cut0_MVA", 
    "h_PU0_trk_cut0_dR",    "h_PU200_trk_cut0_dR",     "h_minBias_trk_cut0_dR", 
    "h_PU0_trk_cut0_dz",    "h_PU200_trk_cut0_dz",     "h_minBias_trk_cut0_dz", 
    "h_PU0_trk_cut0_dRs",   "h_PU200_trk_cut0_dRs",    "h_minBias_trk_cut0_dRs", 
    "h_PU0_trk_cut0_ntrk",  "h_PU200_trk_cut0_ntrk",   "h_minBias_trk_cut0_ntrk", 
    "h_PU0_trk_cut1_pt",    "h_PU200_trk_cut1_pt",     "h_minBias_trk_cut1_pt", 
    "h_PU0_trk_cut1_eta",   "h_PU200_trk_cut1_eta",    "h_minBias_trk_cut1_eta", 
    "h_PU0_trk_cut1_phi",   "h_PU200_trk_cut1_phi",    "h_minBias_trk_cut1_phi", 
    "h_PU0_trk_cut1_d0",    "h_PU200_trk_cut1_d0",     "h_minBias_trk_cut1_d0", 
    "h_PU0_trk_cut1_z0",    "h_PU200_trk_cut1_z0",     "h_minBias_trk_cut1_z0", 
    "h_PU0_trk_cut1_MVA",   "h_PU200_trk_cut1_MVA",    "h_minBias_trk_cut1_MVA", 
    "h_PU0_trk_cut1_dR",    "h_PU200_trk_cut1_dR",     "h_minBias_trk_cut1_dR", 
    "h_PU0_trk_cut1_dz",    "h_PU200_trk_cut1_dz",     "h_minBias_trk_cut1_dz", 
    "h_PU0_trk_cut1_dRs",   "h_PU200_trk_cut1_dRs",    "h_minBias_trk_cut1_dRs", 
    "h_PU0_trk_cut1_ntrk",  "h_PU200_trk_cut1_ntrk",   "h_minBias_trk_cut1_ntrk", 
    "h_PU0_trk_cut2_pt",    "h_PU200_trk_cut2_pt",     "h_minBias_trk_cut2_pt", 
    "h_PU0_trk_cut2_eta",   "h_PU200_trk_cut2_eta",    "h_minBias_trk_cut2_eta", 
    "h_PU0_trk_cut2_phi",   "h_PU200_trk_cut2_phi",    "h_minBias_trk_cut2_phi", 
    "h_PU0_trk_cut2_d0",    "h_PU200_trk_cut2_d0",     "h_minBias_trk_cut2_d0", 
    "h_PU0_trk_cut2_z0",    "h_PU200_trk_cut2_z0",     "h_minBias_trk_cut2_z0", 
    "h_PU0_trk_cut2_MVA",   "h_PU200_trk_cut2_MVA",    "h_minBias_trk_cut2_MVA", 
    "h_PU0_trk_cut2_dR",    "h_PU200_trk_cut2_dR",     "h_minBias_trk_cut2_dR", 
    "h_PU0_trk_cut2_dz",    "h_PU200_trk_cut2_dz",     "h_minBias_trk_cut2_dz", 
    "h_PU0_trk_cut2_dRs",   "h_PU200_trk_cut2_dRs",    "h_minBias_trk_cut2_dRs", 
    "h_PU0_trk_cut2_ntrk",  "h_PU200_trk_cut2_ntrk",   "h_minBias_trk_cut2_ntrk", 
    "h_PU0_trk_cut3_pt",    "h_PU200_trk_cut3_pt",     "h_minBias_trk_cut3_pt", 
    "h_PU0_trk_cut3_eta",   "h_PU200_trk_cut3_eta",    "h_minBias_trk_cut3_eta", 
    "h_PU0_trk_cut3_phi",   "h_PU200_trk_cut3_phi",    "h_minBias_trk_cut3_phi", 
    "h_PU0_trk_cut3_d0",    "h_PU200_trk_cut3_d0",     "h_minBias_trk_cut3_d0", 
    "h_PU0_trk_cut3_z0",    "h_PU200_trk_cut3_z0",     "h_minBias_trk_cut3_z0", 
    "h_PU0_trk_cut3_MVA",   "h_PU200_trk_cut3_MVA",    "h_minBias_trk_cut3_MVA", 
    "h_PU0_trk_cut3_dR",    "h_PU200_trk_cut3_dR",     "h_minBias_trk_cut3_dR", 
    "h_PU0_trk_cut3_dz",    "h_PU200_trk_cut3_dz",     "h_minBias_trk_cut3_dz", 
    "h_PU0_trk_cut3_dRs",   "h_PU200_trk_cut3_dRs",    "h_minBias_trk_cut3_dRs", 
    "h_PU0_trk_cut3_ntrk",  "h_PU200_trk_cut3_ntrk",   "h_minBias_trk_cut3_ntrk", 
    "h_PU0_trk_cut4_pt",    "h_PU200_trk_cut4_pt",     "h_minBias_trk_cut4_pt", 
    "h_PU0_trk_cut4_eta",   "h_PU200_trk_cut4_eta",    "h_minBias_trk_cut4_eta", 
    "h_PU0_trk_cut4_phi",   "h_PU200_trk_cut4_phi",    "h_minBias_trk_cut4_phi", 
    "h_PU0_trk_cut4_d0",    "h_PU200_trk_cut4_d0",     "h_minBias_trk_cut4_d0", 
    "h_PU0_trk_cut4_z0",    "h_PU200_trk_cut4_z0",     "h_minBias_trk_cut4_z0", 
    "h_PU0_trk_cut4_MVA",   "h_PU200_trk_cut4_MVA",    "h_minBias_trk_cut4_MVA", 
    "h_PU0_trk_cut4_dR",    "h_PU200_trk_cut4_dR",     "h_minBias_trk_cut4_dR", 
    "h_PU0_trk_cut4_dz",    "h_PU200_trk_cut4_dz",     "h_minBias_trk_cut4_dz", 
    "h_PU0_trk_cut4_dRs",   "h_PU200_trk_cut4_dRs",    "h_minBias_trk_cut4_dRs", 
    "h_PU0_trk_cut4_ntrk",  "h_PU200_trk_cut4_ntrk",   "h_minBias_trk_cut4_ntrk", 
]

# for i in range(0, len(hist_names), 3):
#     hist1 = get_histogram(file, hist_names[i])
#     hist2 = get_histogram(file, hist_names[i+1])
#     hist3 = get_histogram(file, hist_names[i+2])
    
#     if hist1 and hist2 and hist3:
#         comparison3Plots(hist1, hist2, hist3, True, 'Plots_compare/compares_' + hist1.GetName() + '.png', True, False, True)
#         comparisonROC(hist1,hist2,hist3,'Plots_compare/ROC_' + hist1.GetName() + '.png',True)

hist_names = [
  "h_PU0_cluster_dR6_ntrk",        "h_PU200_cluster_dR6_ntrk",        "h_minBias_cluster_dR6_ntrk", 
  "h_PU0_cluster_dR6_ncluster",    "h_PU200_cluster_dR6_ncluster",    "h_minBias_cluster_dR6_ncluster", 
  "h_PU0_cluster_dR6_match_ntrk",        "h_PU200_cluster_dR6_match_ntrk",        "h_minBias_cluster_dR6_ntrk", 
  "h_PU0_cluster_dR6_match_ncluster",    "h_PU200_cluster_dR6_match_ncluster",    "h_minBias_cluster_dR6_ncluster", 
  "h_PU0_cluster_dR6_match_ntrue",       "h_PU200_cluster_dR6_match_ntrue",       "h_minBias_cluster_dR6_ntrue", 
  "h_PU0_cluster_dR6_match_nfake",       "h_PU200_cluster_dR6_match_nfake",       "h_minBias_cluster_dR6_nfake", 
  "h_PU0_cluster_dR6_match_efficiency",  "h_PU200_cluster_dR6_match_efficiency",  "h_minBias_cluster_dR6_efficiency", 
  "h_PU0_cluster_dRs6_match_ntrk",        "h_PU200_cluster_dRs6_match_ntrk",        "h_minBias_cluster_dRs6_ntrk", 
  "h_PU0_cluster_dRs6_match_ncluster",    "h_PU200_cluster_dRs6_match_ncluster",    "h_minBias_cluster_dRs6_ncluster", 
  "h_PU0_cluster_dRs6_match_ntrue",       "h_PU200_cluster_dRs6_match_ntrue",       "h_minBias_cluster_dRs6_ntrue", 
  "h_PU0_cluster_dRs6_match_nfake",       "h_PU200_cluster_dRs6_match_nfake",       "h_minBias_cluster_dRs6_nfake", 
  "h_PU0_cluster_dRs6_match_efficiency",  "h_PU200_cluster_dRs6_match_efficiency",  "h_minBias_cluster_dRs6_efficiency", 
]

# for i in range(0, len(hist_names), 3):
#     hist1 = get_histogram(file, hist_names[i])
#     hist2 = get_histogram(file, hist_names[i+1])
#     hist3 = get_histogram(file, hist_names[i+2])
    
#     #if "efficiency" in hist_names[i+2]: hist3 = hist2

#     if hist1 and hist2 and hist3:
#         comparison3_2DPlots(hist1, hist2, hist3, True, 'Plots_compare/compares_' + hist1.GetName() + '.png', True, False, True)

hist_names = [
  "h_PU0_cluster_dR6_match_ncluster",    "h_PU200_cluster_dR6_match_ncluster",    "h_minBias_cluster_dR6_ncluster", 
]

for i in range(0, len(hist_names), 3):
    hist1 = get_histogram(file, hist_names[i])
    hist2 = get_histogram(file, hist_names[i+1])
    hist3 = get_histogram(file, hist_names[i+2])
    
    if hist1 and hist2 and hist3:
        DrawROC(hist1,hist2,hist3,'Plots_compare/ROC_' + hist1.GetName() + '.png',True)

# hist_names = [
#     "h_0_trk_pion_plus", "h_200_trk_pion_plus", 
#     "h_0_trk_pion_minus", "h_200_trk_pion_minus", 
#     "h_0_trk_Bs", "h_200_trk_Bs", 
#     "h_0_trk_cut1_pion_plus", "h_200_trk_cut1_pion_plus", 
#     "h_0_trk_cut1_pion_minus", "h_200_trk_cut1_pion_minus", 
#     "h_0_trk_cut1_Bs", "h_200_trk_cut1_Bs", 
#     "h_0_trk_cut2_pion_plus", "h_200_trk_cut2_pion_plus", 
#     "h_0_trk_cut2_pion_minus", "h_200_trk_cut2_pion_minus", 
#     "h_0_trk_cut2_Bs", "h_200_trk_cut2_Bs", 
#     "h_0_trk_cut3_pion_plus", "h_200_trk_cut3_pion_plus", 
#     "h_0_trk_cut3_pion_minus", "h_200_trk_cut3_pion_minus", 
#     "h_0_trk_cut3_Bs", "h_200_trk_cut3_Bs", 
#     "h_0_trk_cut4_pion_plus", "h_200_trk_cut4_pion_plus", 
#     "h_0_trk_cut4_pion_minus", "h_200_trk_cut4_pion_minus", 
#     "h_0_trk_cut4_Bs", "h_200_trk_cut4_Bs", 
#     "h_0_trk_match_dRsMax", "h_200_trk_match_dRsMax",
#     "h_0_trk_cut1_match_dRsMax", "h_200_trk_cut1_match_dRsMax",
#     "h_0_trk_cut2_match_dRsMax", "h_200_trk_cut2_match_dRsMax",
#     "h_0_trk_cut3_match_dRsMax", "h_200_trk_cut3_match_dRsMax",
#     "h_0_trk_cut4_match_dRsMax", "h_200_trk_cut4_match_dRsMax",
#     "h_0_trk_match_dRsMax1", "h_200_trk_match_dRsMax1",
#     "h_0_trk_cut1_match_dRsMax1", "h_200_trk_cut1_match_dRsMax1",
#     "h_0_trk_cut2_match_dRsMax1", "h_200_trk_cut2_match_dRsMax1",
#     "h_0_trk_cut3_match_dRsMax1", "h_200_trk_cut3_match_dRsMax1",
#     "h_0_trk_cut4_match_dRsMax1", "h_200_trk_cut4_match_dRsMax1",
#     "h_0_trk_match_dRsMax2", "h_200_trk_match_dRsMax2",
#     "h_0_trk_cut1_match_dRsMax2", "h_200_trk_cut1_match_dRsMax2",
#     "h_0_trk_cut2_match_dRsMax2", "h_200_trk_cut2_match_dRsMax2",
#     "h_0_trk_cut3_match_dRsMax2", "h_200_trk_cut3_match_dRsMax2",
#     "h_0_trk_cut4_match_dRsMax2", "h_200_trk_cut4_match_dRsMax2",
# ]

# for i in range(0, len(hist_names), 2):
#     hist1 = get_histogram(file, hist_names[i])
#     hist2 = get_histogram(file, hist_names[i+1])
#     if hist_names[i] == "h_0_trk_Bs":
#         hist1.Rebin(2)
#         hist2.Rebin(2)
    
#     if hist1 and hist2:
#         comparisonPlots(hist1, hist2, False, 'Plots_compare/compares_' + hist1.GetName() + '.png', True, False, True)


# hist1 = get_histogram(file, "h_0_trk_match_MVA1")
# hist2 = get_histogram(file, "h_0_trk_cut1_match_MVA1")
# hist3 = get_histogram(file, "h_0_trk_cut2_match_MVA1")
# hist4 = get_histogram(file, "h_0_trk_cut3_match_MVA1")
# hist5 = get_histogram(file, "h_0_trk_cut4_match_MVA1")
# efficiencies(hist1,hist2,hist3,hist4,hist5,False, 'Plots_compare/efficiency_trk_PU0.png')

# hist_PU0 = [hist1, hist2, hist3, hist4, hist5]

# hist1 = get_histogram(file, "h_200_trk_match_MVA1")
# hist2 = get_histogram(file, "h_200_trk_cut1_match_MVA1")
# hist3 = get_histogram(file, "h_200_trk_cut2_match_MVA1")
# hist4 = get_histogram(file, "h_200_trk_cut3_match_MVA1")
# hist5 = get_histogram(file, "h_200_trk_cut4_match_MVA1")
# efficiencies(hist1,hist2,hist3,hist4,hist5,False, 'Plots_compare/efficiency_trk_PU200.png')

# hist_PU200 = [hist1, hist2, hist3, hist4, hist5]

# hist1 = get_histogram(file, "h_MinBias_trk_MVA1")
# hist2 = get_histogram(file, "h_MinBias_trk_cut1_MVA1")
# hist3 = get_histogram(file, "h_MinBias_trk_cut2_MVA1")
# hist4 = get_histogram(file, "h_MinBias_trk_cut3_MVA1")
# hist5 = get_histogram(file, "h_MinBias_trk_cut4_MVA1")
# efficiencies(hist1,hist2,hist3,hist4,hist5,False, 'Plots_compare/efficiency_trk_minBias.png')

# hist_minBias = [hist1, hist2, hist3, hist4, hist5]

# efficienciesPlot(hist_PU0,hist_PU200,hist_minBias,False, 'Plots_compare/efficiency_trk.png')

# hist1 = get_histogram(file, "h_0_trk_Bs")
# hist2 = get_histogram(file, "h_0_trk_cut1_Bs")
# hist3 = get_histogram(file, "h_0_trk_cut2_Bs")
# hist4 = get_histogram(file, "h_0_trk_cut3_Bs")
# hist5 = get_histogram(file, "h_0_trk_cut4_Bs")
# efficiencies(hist1,hist2,hist3,hist4,hist5,False, 'Plots_compare/efficiency_evt_PU0.png')

# hist_PU0 = [hist1, hist2, hist3, hist4, hist5]

# hist1 = get_histogram(file, "h_200_trk_Bs")
# hist2 = get_histogram(file, "h_200_trk_cut1_Bs")
# hist3 = get_histogram(file, "h_200_trk_cut2_Bs")
# hist4 = get_histogram(file, "h_200_trk_cut3_Bs")
# hist5 = get_histogram(file, "h_200_trk_cut4_Bs")
# efficiencies(hist1,hist2,hist3,hist4,hist5,False, 'Plots_compare/efficiency_evt_PU200.png')

# hist_PU200 = [hist1, hist2, hist3, hist4, hist5]
# hist_minBias = []

# efficienciesPlot(hist_PU0,hist_PU200,hist_minBias,False, 'Plots_compare/efficiency_6trk_evt.png')

# hist1 = get_histogram(file, "h_0_trk_pion_plus")
# hist2 = get_histogram(file, "h_0_trk_cut1_pion_plus")
# hist3 = get_histogram(file, "h_0_trk_cut2_pion_plus")
# hist4 = get_histogram(file, "h_0_trk_cut3_pion_plus")
# hist5 = get_histogram(file, "h_0_trk_cut4_pion_plus")

# hist_PU0 = [hist1, hist2, hist3, hist4, hist5]

# hist1 = get_histogram(file, "h_200_trk_pion_plus")
# hist2 = get_histogram(file, "h_200_trk_cut1_pion_plus")
# hist3 = get_histogram(file, "h_200_trk_cut2_pion_plus")
# hist4 = get_histogram(file, "h_200_trk_cut3_pion_plus")
# hist5 = get_histogram(file, "h_200_trk_cut4_pion_plus")

# hist_PU200 = [hist1, hist2, hist3, hist4, hist5]
# hist_minBias = []

# efficienciesPlot(hist_PU0,hist_PU200,hist_minBias,False, 'Plots_compare/efficiency_3trk_evt.png')

file.Close()
ofile.Close()