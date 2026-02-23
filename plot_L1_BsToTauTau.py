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
    hist0 = ROOT.TH1F("eff_pu0", "", 3,0,3)
    hist1 = ROOT.TH1F("eff_pu200", "", 3,0,3)
    hist2 = ROOT.TH1F("eff_minBias", "", 3,0,3)
    if hist_PU0:
        hist0.SetBinContent(1, hist_PU0.GetBinContent(3)/hist_PU0.GetBinContent(2))
        hist0.SetBinContent(2, hist_PU0.GetBinContent(5)/hist_PU0.GetBinContent(2))
        hist0.SetBinContent(3, hist_PU0.GetBinContent(6)/hist_PU0.GetBinContent(2))
    hist1.SetBinContent(1, hist_PU200.GetBinContent(3)/hist_PU200.GetBinContent(2))
    hist1.SetBinContent(2, hist_PU200.GetBinContent(5)/hist_PU200.GetBinContent(2))
    hist1.SetBinContent(3, hist_PU200.GetBinContent(6)/hist_PU200.GetBinContent(2))
    print(f"eff PU200: {hist_PU200.GetBinContent(2)/hist_PU200.GetBinContent(1)}, minBias : {hist_minBias.GetBinContent(2)/hist_minBias.GetBinContent(1)}")
    print(f"eff PU200: {hist_PU200.GetBinContent(3)/hist_PU200.GetBinContent(2)}, minBias : {hist_minBias.GetBinContent(3)/hist_minBias.GetBinContent(2)}")
    print(f"eff PU200: {hist_PU200.GetBinContent(4)/hist_PU200.GetBinContent(3)}, minBias : {hist_minBias.GetBinContent(4)/hist_minBias.GetBinContent(3)}")
    print(f"eff PU200: {hist_PU200.GetBinContent(5)/hist_PU200.GetBinContent(3)}, minBias : {hist_minBias.GetBinContent(5)/hist_minBias.GetBinContent(3)}")
    print(f"eff PU200: {hist_PU200.GetBinContent(6)/hist_PU200.GetBinContent(5)}, minBias : {hist_minBias.GetBinContent(6)/hist_minBias.GetBinContent(5)}")
    print(f"eff PU200: {hist_PU200.GetBinContent(6)/hist_PU200.GetBinContent(2)}, minBias : {hist_minBias.GetBinContent(6)/hist_minBias.GetBinContent(2)}")
    hist0.GetXaxis().SetBinLabel(1, "|#eta| < 2.0")
    hist0.GetXaxis().SetBinLabel(2, "MVA < 0.997")
    hist0.GetXaxis().SetBinLabel(3, "N_{trk} > 63")
    hist0.SetLineColor(4)
    hist0.SetMarkerColor(4)
    hist1.SetLineColor(2)
    hist1.SetMarkerColor(2)
    hist1.GetYaxis().SetRangeUser(5e-3,1.0)
    if hist_PU0:
        hist0.Draw('')
    if hist_minBias:
        hist2.SetBinContent(1, hist_minBias.GetBinContent(3)/hist_minBias.GetBinContent(2))
        hist2.SetBinContent(2, hist_minBias.GetBinContent(5)/hist_minBias.GetBinContent(2))
        hist2.SetBinContent(3, hist_minBias.GetBinContent(6)/hist_minBias.GetBinContent(2))
        hist2.SetLineColor(1)
        hist2.SetLineStyle(9)
        hist2.SetMarkerColor(1)
        hist2.Draw('same')
    hist1.Draw('same')

    cms_lat=ROOT.TLatex()
    cms_lat.SetTextSize(0.05)
    cms_lat.DrawLatex(0,1.12,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    cms_lat.DrawLatex(3.3,1.12,"#scale[0.9]{14 TeV}")

    leg = ROOT.TLegend(0.20, 0.20, 0.6, 0.40)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.05)
    if hist_PU0:
        leg.AddEntry(hist0, "B_{s}#rightarrow#tau#tau, PU 0", 'lp')
    leg.AddEntry(hist1, "B_{s}#rightarrow#tau#tau, PU 200", 'lp')
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
    hist = ROOT.TH1F("eff", "", 3,0,3)
    hist.SetBinContent(1, hist2.Integral()/hist1.Integral())
    hist.SetBinContent(2, hist3.Integral()/hist1.Integral())
    hist.SetBinContent(3, hist5.Integral()/hist1.Integral())
    hist.SetLineColor(1)
    hist.SetMarkerColor(1)
    #hist.GetYaxis().SetRangeUser(0,0.5)
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
            leg.AddEntry(hist1, "B_{s} #rightarrow #tau#tau, PU 0", 'lp')
            leg.AddEntry(hist2, "B_{s} #rightarrow #tau#tau, PU 200", 'lp')
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
        if(hist1.Integral()>0): hist1.Scale(1./hist1.GetSumOfWeights())
        if(hist2.Integral()>0): hist2.Scale(1./hist2.GetSumOfWeights())
        if(hist3.Integral()>0): hist3.Scale(1./hist3.GetSumOfWeights())
        hist3.GetYaxis().SetRangeUser(1e-4, 2)
    if "pt" in str(hist1.GetName()):
        hist1.Rebin(4)
        hist2.Rebin(4)
        hist3.Rebin(4)
        if "gen" in str(hist1.GetName()):
            hist3.GetXaxis().SetRangeUser(0, 10)
    if "eta" in str(hist1.GetName()):
        hist1.Rebin(5)
        hist2.Rebin(5)
        hist3.Rebin(5)
    if "MVA" in str(hist1.GetName()):
        hist3.GetXaxis().SetRangeUser(0.98, 1)
    if "wMVA" in str(hist1.GetName()) or "uMVA" in str(hist1.GetName()):
        hist3.GetXaxis().SetRangeUser(0.90, 1)
    elif "ntrk" in str(hist1.GetName()):
        hist3.GetXaxis().SetRangeUser(0, 250)
        hist3.GetYaxis().SetRangeUser(0, 0.25)
        if "cut3" in str(hist1.GetName()) or "cut4" in str(hist1.GetName()):
            hist3.GetXaxis().SetRangeUser(0, 180)
            hist3.GetYaxis().SetRangeUser(0, 0.15)
        c1.SetLogy(0)
    hist3.SetLineColor(1)
    hist3.SetMarkerColor(1)
    hist2.SetLineColor(2)
    hist2.SetMarkerColor(2)
    hist1.SetLineColor(4)
    hist1.SetMarkerColor(4)
    hist1.SetLineWidth(2)
    hist2.SetLineWidth(2)
    hist3.SetLineWidth(2)
    hist3.GetYaxis().SetTitle("p.d.f")
    hist3.Draw('ep')
    hist2.Draw('epsame')
    hist1.Draw('epsame')
    
    cms_lat=ROOT.TLatex()
    cms_lat.SetTextSize(0.05)
    cms_lat.DrawLatex(hist1.GetXaxis().GetBinLowEdge(1),2.2,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    if "MVA" in str(hist1.GetName()):
        if "wMVA" in str(hist1.GetName()) or "uMVA" in str(hist1.GetName()):
            cms_lat.DrawLatex(0.90,2.2,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
        else:
            cms_lat.DrawLatex(0.98,2.2,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    if "ntrk" in str(hist1.GetName()):
        cms_lat.DrawLatex(0.,0.82,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
        if not "cut4" in str(hist1.GetName()):
            cms_lat.DrawLatex(0.,0.41,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    cms_lat.SetTextAlign(31)
    cms_lat.DrawLatex(hist1.GetXaxis().GetBinLowEdge(hist1.GetNbinsX()),2.2,"#scale[0.9]{14 TeV}")
    if "ntrk" in str(hist1.GetName()):
        cms_lat.DrawLatex(250,0.41,"#scale[0.9]{14 TeV}")
        if "cut4" in str(hist1.GetName()):
            cms_lat.DrawLatex(50,0.83,"#scale[0.9]{14 TeV}")

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
            leg.AddEntry(hist1, "B_{s}#rightarrow#tau#tau, PU 0", 'lp')
            leg.AddEntry(hist2, "B_{s}#rightarrow#tau#tau, PU 200", 'lp')
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
        if "dzmax" in str(hist2D1.GetName()): 
            hist1.Rebin(2)
            hist2.Rebin(2)
            hist3.Rebin(2)
            hist1.GetXaxis().SetRangeUser(0,5)
        if "mass" in str(hist2D1.GetName()): 
            hist1.Rebin(2)
            hist2.Rebin(2)
            hist3.Rebin(2)
            hist1.GetXaxis().SetRangeUser(0,20)
        hist3.SetLineColor(1)
        hist3.SetMarkerColor(1)
        hist2.SetLineColor(2)
        hist2.SetMarkerColor(2)
        hist1.SetLineColor(4)
        hist1.SetMarkerColor(4)
        hist1.Draw('ep')
        hist2.Draw('epsame')
        hist3.Draw('epsame')
    
        cms_lat=ROOT.TLatex()
        cms_lat.SetTextSize(0.05)
        cms_lat.DrawLatex(0,2.2,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
        cms_lat.SetTextAlign(31)
        cms_lat.DrawLatex(hist1.GetXaxis().GetBinLowEdge(hist1.GetNbinsX()),2.2,"#scale[0.9]{14 TeV}")

        if isLegend:
            leg = ROOT.TLegend(0.40, 0.68, 0.9, 0.88)
            leg.SetBorderSize(0)
            leg.SetFillColor(10)
            leg.SetLineColor(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.05)
            if "dRs" in str(hist2D1.GetName()): leg.SetHeader(f"cluster size {0.2+0.1*ybin:.1f}")
            else: leg.SetHeader(f"cluster size {0.0+0.1*ybin:.1f}")
            leg.AddEntry(hist1, "B_{s}#rightarrow#tau#tau, PU 0", 'lp')
            leg.AddEntry(hist2, "B_{s}#rightarrow#tau#tau, PU 200", 'lp')
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
            leg.AddEntry(h1, "B_{s}#rightarrow#tau#tau, PU 0", 'lp')
            leg.AddEntry(h2, "B_{s}#rightarrow#tau#tau, PU 200", 'lp')
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
        h1 = ROOT.TH1D("eff_PU200", ";MVA;#epsilon", 5000,0,1)
        h2 = ROOT.TH1D("eff_minBias", ";MVA;#epsilon", 5000,0,1)
    
    if hist1.Integral() == 0: return 0

    
    # Calculate the ROC curve points
    if "eta" in str(hist1.GetName()):
        for i in range(1, 250):
            x1.append((hist1.Integral(i, 250)+hist1.Integral(251,hist1.GetNbinsX()+1-i)) / hist1.Integral())
            x2.append((hist2.Integral(i, 250)+hist2.Integral(251,hist2.GetNbinsX()+1-i)) / hist2.Integral())
            y1.append(1 - ((hist3.Integral(i, 250)+hist3.Integral(251,hist3.GetNbinsX()+1-i)) / hist3.Integral()))
    elif "d0" in str(hist1.GetName()):
        for i in range(1, 100):
            x1.append((hist1.Integral(i, 100)+hist1.Integral(101,hist1.GetNbinsX()+1-i)) / hist1.Integral())
            x2.append((hist2.Integral(i, 100)+hist2.Integral(101,hist2.GetNbinsX()+1-i)) / hist2.Integral())
            y1.append(1 - ((hist3.Integral(i, 100)+hist3.Integral(101,hist3.GetNbinsX()+1-i)) / hist3.Integral()))
    elif "pt" in str(hist1.GetName()):
        for i in range(1, hist1.GetNbinsX() + 1):
            x1.append(hist1.Integral(i, hist1.GetNbinsX() + 1) / hist1.Integral())
            x2.append(hist2.Integral(i, hist2.GetNbinsX() + 1) / hist2.Integral())
            y1.append(1 - (hist3.Integral(i, hist1.GetNbinsX() + 1) / hist3.Integral()))
    elif "uMVA" in str(hist1.GetName()) or "wMVA" in str(hist1.GetName()):
        for i in range(1, hist1.GetNbinsX() + 1):
            x1.append(hist1.Integral(hist1.GetNbinsX() - i, hist1.GetNbinsX() + 1) / hist1.Integral())
            x2.append(hist2.Integral(hist2.GetNbinsX() - i, hist2.GetNbinsX() + 1) / hist2.Integral())
            y1.append(1 - (hist3.Integral(hist2.GetNbinsX() - i, hist1.GetNbinsX() + 1) / hist3.Integral()))
            h1.SetBinContent(hist2.GetNbinsX() - i, hist2.Integral(hist2.GetNbinsX() - i, hist2.GetNbinsX() + 1) / hist2.Integral())
            h2.SetBinContent(hist3.GetNbinsX() - i, 1 - (hist3.Integral(hist3.GetNbinsX() - i, hist3.GetNbinsX() + 1) / hist3.Integral()))
    elif "ntrk" in str(hist1.GetName()):
        for i in range(1, hist1.GetNbinsX() + 1):
            x1.append(hist1.Integral(i, 100) / hist1.Integral())
            x2.append(hist2.Integral(i, 100) / hist2.Integral())
            y1.append(1 - (hist3.Integral(i, 100) / hist3.Integral()))
            if hist2.Integral(i, 100) / hist2.Integral() > 0.98 and 1 - (hist3.Integral(i, 100) / hist3.Integral()) > 0.98:
                print(i)
    else:
        for i in range(1, hist1.GetNbinsX() + 1):
            x1.append(hist1.Integral(1, i) / hist1.Integral())
            x2.append(hist2.Integral(1, i) / hist2.Integral())
            y1.append(1 - (hist3.Integral(1, i) / hist3.Integral()))
            if "MVA" in str(hist1.GetName()) and i == 4985:
                print(f"{hist2.Integral(1, i) / hist2.Integral()} and {hist3.Integral(1, i) / hist3.Integral()}")
    
    # Create TGraph objects for the ROC curves
    g1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
    g2 = ROOT.TGraph(len(x2), array('d', x2), array('d', y1))
    
    # Set graph styles
    g1.SetLineColor(1)
    g1.SetMarkerColor(1)
    g2.SetLineColor(2)
    g2.SetMarkerColor(2)
    g1.GetXaxis().SetTitle("B_{s} #rightarrow #tau#tau efficiency")
    g1.GetYaxis().SetTitle("Minimum Bias Rejection Efficiency")
    g1.GetXaxis().SetLimits(0, 1)
    g1.GetYaxis().SetRangeUser(0, 1)
    
    # Draw the ROC curves
    g1.Draw('ALP')
    g2.Draw('LP same')
    
    cms_lat=ROOT.TLatex()
    cms_lat.SetTextSize(0.05)
    cms_lat.DrawLatex(0,1.02,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    cms_lat.DrawLatex(0.8,1.02,"#scale[0.9]{14 TeV}")

    # Add legend if specified
    if isLegend:
        leg = ROOT.TLegend(0.40, 0.58, 0.9, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.SetHeader(hist1.GetXaxis().GetTitle())
        leg.AddEntry(g1, "B_{s} #rightarrow #tau#tau, PU 0", 'lp')
        leg.AddEntry(g2, "B_{s} #rightarrow #tau#tau, PU 200", 'lp')
        leg.Draw()
    
    # Save the canvas
    c1.Print(pname)
    ofile.cd()
    c1.Write()

    if "MVA" in str(hist1.GetName()) and not "cut" in str(hist1.GetName()):
        h1.GetYaxis().SetRangeUser(0, 1)
        h1.GetXaxis().SetTitle(h1.GetXaxis().GetTitle())
        h1.SetLineColor(2)
        h2.SetLineColor(1)
        h1.Draw('l')
        h2.Draw('lsame')
        cms_lat.SetTextSize(0.05)
        cms_lat.DrawLatex(0.,1.02,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
        cms_lat.DrawLatex(0.8,1.02,"#scale[0.9]{14 TeV}")
        leg = ROOT.TLegend(0.40, 0.58, 0.9, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.SetHeader(hist1.GetXaxis().GetTitle())
        leg.AddEntry(h1, "B_{s} #rightarrow #tau#tau, PU 200", 'lp')
        leg.AddEntry(h2, "MinBias", 'lp')
        leg.Draw()
        c1.Print(pname.replace("h_", "eff_"))


def DrawROC(hist_PU200_eff, hist_minBias_ncluster, pname='sync.pdf', isLegend=False, dc_slice=None):
    """
    ROC from 2D histograms. Both have Y = dc.
    - hist_PU200_eff (match_efficiency): X = IsMatched (1=fail, 2=true). sig_eff = true/(fail+true).
    - hist_minBias_ncluster: X = count (ncluster). bkg_rej = fraction in X bin 1 (0 clusters).
    - dc_slice: if set, use only the Y bin closest to this dc value (single point ROC).
    """
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname, "", 700, 700)
    # Both: Y = dc. Loop over dc bins (Y).
    n_dc = min(hist_PU200_eff.GetNbinsY(), hist_minBias_ncluster.GetNbinsY())
    nx_bkg = hist_minBias_ncluster.GetNbinsX()
    if dc_slice is not None:
        # use only the bin whose center is closest to dc_slice
        i_best = 1
        best = abs(hist_PU200_eff.GetYaxis().GetBinCenter(1) - dc_slice)
        for i in range(2, n_dc + 1):
            d = abs(hist_PU200_eff.GetYaxis().GetBinCenter(i) - dc_slice)
            if d < best:
                best = d
                i_best = i
        dc_range = [i_best]
    else:
        dc_range = range(1, n_dc + 1)
    x1, y1 = [], []
    for i in dc_range:
        den_sig = hist_PU200_eff.Integral(1, 2, i, i)   # fail+true for this dc
        den_bkg = hist_minBias_ncluster.Integral(1, nx_bkg, i, i)
        if den_sig > 0 and den_bkg > 0:
            sig_eff = hist_PU200_eff.Integral(2, 2, i, i) / den_sig   # true / (fail+true)
            bkg_rej = hist_minBias_ncluster.Integral(1, 2, i, i) / den_bkg
            x1.append(sig_eff)
            y1.append(bkg_rej)
    if len(x1) == 0:
        return
    g1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
    g1.SetLineColor(2)
    g1.SetMarkerColor(2)
    g1.SetMarkerStyle(22)
    g1.GetXaxis().SetTitle("B_{s} #rightarrow #tau#tau efficiency")
    g1.GetYaxis().SetTitle("Minimum Bias Rejection")
    g1.GetYaxis().SetNdivisions(505)
    g1.GetXaxis().SetLimits(0, 1)
    g1.GetYaxis().SetRangeUser(0.00, 1)
    g1.Draw('ALP')
    cms_lat = ROOT.TLatex()
    cms_lat.SetTextSize(0.05)
    cms_lat.DrawLatex(0, 1.01, "#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    cms_lat.DrawLatex(0.8, 1.01, "#scale[0.9]{(14 TeV)}")
    if isLegend:
        leg = ROOT.TLegend(0.20, 0.50, 0.70, 0.80)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.05)
        leg.SetHeader("Track clustering (dc scan)")
        leg.AddEntry(g1, "PU 200 vs MinBias", "lp")
        leg.Draw()
    c1.Print(pname)
    ofile.cd()
    c1.Write()


def DrawROC_dc_dm(rfile, pname='Plots_compare/ROC_dc_dm.png', isLegend=True):
    """
    ROC curves for dc (y-axis) and all dm values in one plot.
    minBias vs PU200; one curve per dm (dm=0.10, 0.20, ..., 0.60).
    """
    strings_to_remove = ["/", ".png"]
    cname = pname
    for string in strings_to_remove:
        cname = cname.replace(string, "_")
    c1 = ROOT.TCanvas(cname, "", 700, 700)
    # dm = dc + offset (from run_cluster_*_CLUE.py); one curve per offset
    dm_offset_list = [5, 10, 15, 20, 25, 30]  # 0.05, 0.10, ...
    colors = [1, 2, 4, 6, 8, 9]
    graphs = []
    dc_vals = []
    for idx, off in enumerate(dm_offset_list):
        h_sig = rfile.Get(f"h_PU200_dm_offset0.{off:02d}_match_efficiency")
        h_bkg = rfile.Get(f"h_minBias_dm_offset0.{off:02d}_ncluster")
        if not h_sig or not h_bkg:
            continue
        # match_efficiency: X=IsMatched(1=fail,2=true), Y=dc.  sig_eff = true/(fail+true).
        # ncluster: X=count, Y=dc.  bkg_rej = fraction in X bin 1.
        n_dc = min(h_sig.GetNbinsY(), h_bkg.GetNbinsY())
        nx_bkg = h_bkg.GetNbinsX()
        x1, y1 = [], []
        for i in range(1, n_dc + 1):
            den_sig = h_sig.Integral(1, 2, i, i)
            den_bkg = h_bkg.Integral(1, nx_bkg, i, i)
            if den_sig > 0 and den_bkg > 0:
                if idx == 0:
                    dc_vals.append(h_bkg.GetYaxis().GetBinCenter(i))
                sig_eff = h_sig.Integral(2, 2, i, i) / den_sig
                bkg_rej = h_bkg.Integral(1, 2, i, i) / den_bkg
                x1.append(sig_eff)
                y1.append(bkg_rej)
                print(f'{i}, sig eff: {sig_eff}, bkg rej: {bkg_rej}')
        if len(x1) == 0:
            continue
        g = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
        g.SetLineColor(colors[idx % len(colors)])
        g.SetMarkerColor(colors[idx % len(colors)])
        g.SetMarkerStyle(20 + (idx % 5))
        graphs.append((g, off))
    if not graphs:
        return
    #graphs[0][0].GetXaxis().SetTitle("B_{s} #rightarrow #tau#tau efficiency")
    graphs[0][0].GetXaxis().SetTitle("H #rightarrow #tau#tau efficiency")
    graphs[0][0].GetYaxis().SetTitle("Minimum Bias Rejection")
    graphs[0][0].GetXaxis().SetLimits(0, 1)
    graphs[0][0].GetYaxis().SetRangeUser(0.00, 1)
    graphs[0][0].Draw("ALP")
    for g, _ in graphs[1:]:
        g.Draw("LP same")
    # Draw dc labels at first curve's points (same dc for all curves)
    lat = ROOT.TLatex()
    lat.SetTextSize(0.025)
    lat.SetTextColor(ROOT.kBlack)
    g0 = graphs[0][0]
    npts = g0.GetN()
    for j in range(npts):
        x = g0.GetX()[j]
        y = g0.GetY()[j]
        dc = dc_vals[j] if j < len(dc_vals) else 0.0
        lat.DrawLatex(x + 0.02, y - 0.02, f"{dc:.2f}")
    cms_lat = ROOT.TLatex()
    cms_lat.SetTextSize(0.05)
    cms_lat.DrawLatex(0, 1.01, "#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
    cms_lat.DrawLatex(0.8, 1.01, "#scale[0.9]{(14 TeV)}")
    if isLegend:
        leg = ROOT.TLegend(0.60, 0.45, 0.80, 0.85)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.045)
        leg.SetHeader("d_{m} = d_{c} + offset")
        for g, off in graphs:
            leg.AddEntry(g, f"offset = 0.{off:02d}", "lp")
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
    "h_PU0_gen_pt",         "h_PU200_gen_pt",          "h_minBias_gen_pt",
    "h_PU0_gen_eta",        "h_PU200_gen_eta",         "h_minBias_gen_eta",
    "h_PU0_gen_phi",        "h_PU200_gen_phi",         "h_minBias_gen_phi",
    "h_PU0_trk_pt",         "h_PU200_trk_pt",          "h_minBias_trk_pt", 
    "h_PU0_trk_eta",        "h_PU200_trk_eta",         "h_minBias_trk_eta", 
    "h_PU0_trk_phi",        "h_PU200_trk_phi",         "h_minBias_trk_phi", 
    "h_PU0_trk_d0",         "h_PU200_trk_d0",          "h_minBias_trk_d0", 
    "h_PU0_trk_z0",         "h_PU200_trk_z0",          "h_minBias_trk_z0", 
    "h_PU0_trk_MVA",        "h_PU200_trk_MVA",         "h_minBias_trk_MVA", 
    "h_PU0_trk_uMVA",        "h_PU200_trk_uMVA",         "h_minBias_trk_uMVA", 
    "h_PU0_trk_wMVA",        "h_PU200_trk_wMVA",         "h_minBias_trk_wMVA", 
    "h_PU0_trk_dR",         "h_PU200_trk_dR",          "h_minBias_trk_dR", 
    "h_PU0_trk_dz",         "h_PU200_trk_dz",          "h_minBias_trk_dz", 
    "h_PU0_trk_ntrk",       "h_PU200_trk_ntrk",        "h_minBias_trk_ntrk", 
    "h_PU0_trk_cut0_pt",    "h_PU200_trk_cut0_pt",     "h_minBias_trk_cut0_pt", 
    "h_PU0_trk_cut0_eta",   "h_PU200_trk_cut0_eta",    "h_minBias_trk_cut0_eta", 
    "h_PU0_trk_cut0_phi",   "h_PU200_trk_cut0_phi",    "h_minBias_trk_cut0_phi", 
    "h_PU0_trk_cut0_d0",    "h_PU200_trk_cut0_d0",     "h_minBias_trk_cut0_d0", 
    "h_PU0_trk_cut0_z0",    "h_PU200_trk_cut0_z0",     "h_minBias_trk_cut0_z0", 
    "h_PU0_trk_cut0_MVA",   "h_PU200_trk_cut0_MVA",    "h_minBias_trk_cut0_MVA", 
    "h_PU0_trk_cut0_dR",    "h_PU200_trk_cut0_dR",     "h_minBias_trk_cut0_dR", 
    "h_PU0_trk_cut0_dz",    "h_PU200_trk_cut0_dz",     "h_minBias_trk_cut0_dz", 
    "h_PU0_trk_cut0_ntrk",  "h_PU200_trk_cut0_ntrk",   "h_minBias_trk_cut0_ntrk", 
    "h_PU0_trk_cut1_pt",    "h_PU200_trk_cut1_pt",     "h_minBias_trk_cut1_pt", 
    "h_PU0_trk_cut1_eta",   "h_PU200_trk_cut1_eta",    "h_minBias_trk_cut1_eta", 
    "h_PU0_trk_cut1_phi",   "h_PU200_trk_cut1_phi",    "h_minBias_trk_cut1_phi", 
    "h_PU0_trk_cut1_d0",    "h_PU200_trk_cut1_d0",     "h_minBias_trk_cut1_d0", 
    "h_PU0_trk_cut1_z0",    "h_PU200_trk_cut1_z0",     "h_minBias_trk_cut1_z0", 
    "h_PU0_trk_cut1_MVA",   "h_PU200_trk_cut1_MVA",    "h_minBias_trk_cut1_MVA", 
    "h_PU0_trk_cut1_dR",    "h_PU200_trk_cut1_dR",     "h_minBias_trk_cut1_dR", 
    "h_PU0_trk_cut1_dz",    "h_PU200_trk_cut1_dz",     "h_minBias_trk_cut1_dz", 
    "h_PU0_trk_cut1_ntrk",  "h_PU200_trk_cut1_ntrk",   "h_minBias_trk_cut1_ntrk", 
    "h_PU0_trk_cut2_pt",    "h_PU200_trk_cut2_pt",     "h_minBias_trk_cut2_pt", 
    "h_PU0_trk_cut2_eta",   "h_PU200_trk_cut2_eta",    "h_minBias_trk_cut2_eta", 
    "h_PU0_trk_cut2_phi",   "h_PU200_trk_cut2_phi",    "h_minBias_trk_cut2_phi", 
    "h_PU0_trk_cut2_d0",    "h_PU200_trk_cut2_d0",     "h_minBias_trk_cut2_d0", 
    "h_PU0_trk_cut2_z0",    "h_PU200_trk_cut2_z0",     "h_minBias_trk_cut2_z0", 
    "h_PU0_trk_cut2_MVA",   "h_PU200_trk_cut2_MVA",    "h_minBias_trk_cut2_MVA", 
    "h_PU0_trk_cut2_dR",    "h_PU200_trk_cut2_dR",     "h_minBias_trk_cut2_dR", 
    "h_PU0_trk_cut2_dz",    "h_PU200_trk_cut2_dz",     "h_minBias_trk_cut2_dz", 
    "h_PU0_trk_cut2_ntrk",  "h_PU200_trk_cut2_ntrk",   "h_minBias_trk_cut2_ntrk", 
    "h_PU0_trk_cut3_pt",    "h_PU200_trk_cut3_pt",     "h_minBias_trk_cut3_pt", 
    "h_PU0_trk_cut3_eta",   "h_PU200_trk_cut3_eta",    "h_minBias_trk_cut3_eta", 
    "h_PU0_trk_cut3_phi",   "h_PU200_trk_cut3_phi",    "h_minBias_trk_cut3_phi", 
    "h_PU0_trk_cut3_d0",    "h_PU200_trk_cut3_d0",     "h_minBias_trk_cut3_d0", 
    "h_PU0_trk_cut3_z0",    "h_PU200_trk_cut3_z0",     "h_minBias_trk_cut3_z0", 
    "h_PU0_trk_cut3_MVA",   "h_PU200_trk_cut3_MVA",    "h_minBias_trk_cut3_MVA", 
    "h_PU0_trk_cut3_dR",    "h_PU200_trk_cut3_dR",     "h_minBias_trk_cut3_dR", 
    "h_PU0_trk_cut3_dz",    "h_PU200_trk_cut3_dz",     "h_minBias_trk_cut3_dz", 
    "h_PU0_trk_cut3_ntrk",  "h_PU200_trk_cut3_ntrk",   "h_minBias_trk_cut3_ntrk", 
    "h_PU0_trk_cut4_pt",    "h_PU200_trk_cut4_pt",     "h_minBias_trk_cut4_pt", 
    "h_PU0_trk_cut4_eta",   "h_PU200_trk_cut4_eta",    "h_minBias_trk_cut4_eta", 
    "h_PU0_trk_cut4_phi",   "h_PU200_trk_cut4_phi",    "h_minBias_trk_cut4_phi", 
    "h_PU0_trk_cut4_d0",    "h_PU200_trk_cut4_d0",     "h_minBias_trk_cut4_d0", 
    "h_PU0_trk_cut4_z0",    "h_PU200_trk_cut4_z0",     "h_minBias_trk_cut4_z0", 
    "h_PU0_trk_cut4_MVA",   "h_PU200_trk_cut4_MVA",    "h_minBias_trk_cut4_MVA", 
    "h_PU0_trk_cut4_dR",    "h_PU200_trk_cut4_dR",     "h_minBias_trk_cut4_dR", 
    "h_PU0_trk_cut4_dz",    "h_PU200_trk_cut4_dz",     "h_minBias_trk_cut4_dz", 
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
  "h_PU0_cluster_ntrk6_ntrk",        "h_PU200_cluster_ntrk6_ntrk",        "h_minBias_cluster_ntrk6_ntrk", 
  "h_PU0_cluster_ntrk6_ncluster",    "h_PU200_cluster_ntrk6_ncluster",    "h_minBias_cluster_ntrk6_ncluster", 
  "h_PU0_cluster_ntrk6_dzmax",      "h_PU200_cluster_ntrk6_dzmax",      "h_minBias_cluster_ntrk6_dzmax", 
  "h_PU0_cluster_ntrk6_mass",       "h_PU200_cluster_ntrk6_mass",       "h_minBias_cluster_ntrk6_mass", 
  "h_PU0_cluster_ntrk6_invmass_6trk",       "h_PU200_cluster_ntrk6_invmass_6trk",       "h_minBias_cluster_ntrk6_invmass_6trk", 
  "h_PU0_cluster_ntrk6_invmass_6htrk",       "h_PU200_cluster_ntrk6_invmass_6htrk",       "h_minBias_cluster_ntrk6_invmass_6htrk", 
  "h_PU0_cluster_ntrk6_match_ntrk",        "h_PU200_cluster_ntrk6_match_ntrk",        "h_minBias_cluster_ntrk6_ntrk", 
  "h_PU0_cluster_ntrk6_match_ncluster",    "h_PU200_cluster_ntrk6_match_ncluster",    "h_minBias_cluster_ntrk6_ncluster", 
  "h_PU0_cluster_ntrk6_match_ntrue",       "h_PU200_cluster_ntrk6_match_ntrue",       "h_minBias_cluster_ntrk6_ntrue", 
  "h_PU0_cluster_ntrk6_match_nfake",       "h_PU200_cluster_ntrk6_match_nfake",       "h_minBias_cluster_ntrk6_nfake", 
  "h_PU0_cluster_ntrk6_match_efficiency",  "h_PU200_cluster_ntrk6_match_efficiency",  "h_minBias_cluster_ntrk6_efficiency", 
  "h_PU0_cluster_MVA6_ntrk",        "h_PU200_cluster_MVA6_ntrk",        "h_minBias_cluster_MVA6_ntrk", 
  "h_PU0_cluster_MVA6_ncluster",    "h_PU200_cluster_MVA6_ncluster",    "h_minBias_cluster_MVA6_ncluster", 
  "h_PU0_cluster_MVA6_dzmax",      "h_PU200_cluster_MVA6_dzmax",      "h_minBias_cluster_MVA6_dzmax", 
  "h_PU0_cluster_MVA6_mass",       "h_PU200_cluster_MVA6_mass",       "h_minBias_cluster_MVA6_mass", 
  "h_PU0_cluster_MVA6_invmass_6trk",       "h_PU200_cluster_MVA6_invmass_6trk",       "h_minBias_cluster_MVA6_invmass_6trk", 
  "h_PU0_cluster_MVA6_invmass_6htrk",       "h_PU200_cluster_MVA6_invmass_6htrk",       "h_minBias_cluster_MVA6_invmass_6htrk", 
  "h_PU0_cluster_MVA6_match_ntrk",        "h_PU200_cluster_MVA6_match_ntrk",        "h_minBias_cluster_MVA6_ntrk", 
  "h_PU0_cluster_MVA6_match_ncluster",    "h_PU200_cluster_MVA6_match_ncluster",    "h_minBias_cluster_MVA6_ncluster", 
  "h_PU0_cluster_MVA6_match_ntrue",       "h_PU200_cluster_MVA6_match_ntrue",       "h_minBias_cluster_MVA6_ntrue", 
  "h_PU0_cluster_MVA6_match_nfake",       "h_PU200_cluster_MVA6_match_nfake",       "h_minBias_cluster_MVA6_nfake", 
  "h_PU0_cluster_MVA6_match_efficiency",  "h_PU200_cluster_MVA6_match_efficiency",  "h_minBias_cluster_MVA6_efficiency", 
]

# for i in range(0, len(hist_names), 3):
#     hist1 = get_histogram(file, hist_names[i])
#     hist2 = get_histogram(file, hist_names[i+1])
#     hist3 = get_histogram(file, hist_names[i+2])
    
#     if hist1 and hist2 and hist3:
#         comparison3_2DPlots(hist1, hist2, hist3, True, 'Plots_compare/compares_' + hist1.GetName() + '.png', True, False, True)

# ROC: dc scan. dm = dc + offset; one plot per offset.
dm_offset_list = [5, 10, 15, 20, 25, 30]
for off in dm_offset_list:
    h_pu200 = get_histogram(file, f"h_PU200_dm_offset0.{off:02d}_match_efficiency")
    h_minb = get_histogram(file, f"h_minBias_dm_offset0.{off:02d}_ncluster")
    if h_pu200 and h_minb:
        DrawROC(h_pu200, h_minb, f'Plots_compare/ROC_dc_dm_offset0.{off:02d}.png', isLegend=True)

# ROC: dc and dm in one plot (one curve per dm)
DrawROC_dc_dm(file, 'Plots_compare/ROC_dc_dm_all.png', isLegend=True)

# ROC after max(dz) trimming: dc=0.2, dm_offset=0.2 (one curve per trim cut; single point per curve)
trim_suffixes = [("0", 0), ("0p5", 0.5), ("1", 1), ("1p5", 1.5), ("2", 2)]
dm_off_roc = 20   # dm_offset = 0.20
dc_trim_roc = 0.2
for ts, cut_val in trim_suffixes:
    # (1) ROC using match_efficiency (dc=0.2, dm_offset=0.2)
    h_sig_t = get_histogram(file, f"h_PU200_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_match_efficiency")
    h_bkg_t = get_histogram(file, f"h_minBias_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_ncluster")
    if h_sig_t and h_bkg_t:
        DrawROC(h_sig_t, h_bkg_t, f'Plots_compare/ROC_trim_maxdz{cut_val}.png', isLegend=True, dc_slice=dc_trim_roc)

# ROC trimming (dc scan style): curves = dc, points = dz(trim). X = Signal efficiency, Y = Minimum bias rejection
dc_vals_trim_plot = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
trim_suffixes_for_curve = [("no_trim", 0), ("0p1", 0.1), ("0p5", 0.5), ("1", 1), ("1p5", 1.5), ("2", 2)]
try:
    c_trim_dc = ROOT.TCanvas("ROC_trim_dc_dz", "", 700, 700)
    colors = [1, 2, 4, 6, 8, 9]
    graphs_trim_dc = []
    dz_labels_for_curve = ["no trim", "0.1", "0.5", "1", "1.5", "2"]
    h_no_eff = get_histogram(file, f"h_PU200_dm_offset0.{dm_off_roc:02d}_match_efficiency")
    h_no_bkg = get_histogram(file, f"h_minBias_dm_offset0.{dm_off_roc:02d}_ncluster")
    if h_no_eff and h_no_bkg:
        n_dc = min(h_no_eff.GetNbinsY(), h_no_bkg.GetNbinsY())
        nx_b = h_no_bkg.GetNbinsX()
        first_curve_labels = []
        for idx_dc, dc_target in enumerate(dc_vals_trim_plot):
            i_best = 1
            best = abs(h_no_eff.GetYaxis().GetBinCenter(1) - dc_target)
            for i in range(2, n_dc + 1):
                d = abs(h_no_eff.GetYaxis().GetBinCenter(i) - dc_target)
                if d < best:
                    best = d
                    i_best = i
            x_pts = []
            y_pts = []
            for j_trim, (ts, dz_val) in enumerate(trim_suffixes_for_curve):
                if ts == "no_trim":
                    h_s = h_no_eff
                    h_b = h_no_bkg
                else:
                    h_s = get_histogram(file, f"h_PU200_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_match_efficiency")
                    h_b = get_histogram(file, f"h_minBias_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_ncluster")
                if not h_s or not h_b:
                    continue
                den_s = h_s.Integral(1, 2, i_best, i_best)
                den_b = h_b.Integral(1, nx_b, i_best, i_best)
                if den_s > 0 and den_b > 0:
                    x_pts.append(h_s.Integral(2, 2, i_best, i_best) / den_s)
                    y_pts.append(h_b.Integral(1, 1, i_best, i_best) / den_b)
                    if idx_dc == 0:
                        first_curve_labels.append(dz_labels_for_curve[j_trim])
            if len(x_pts) < 2:
                continue
            g = ROOT.TGraph(len(x_pts), array('d', x_pts), array('d', y_pts))
            g.SetLineColor(colors[idx_dc % len(colors)])
            g.SetMarkerColor(colors[idx_dc % len(colors)])
            g.SetMarkerStyle(20 + (idx_dc % 5))
            graphs_trim_dc.append((g, dc_target))
        if graphs_trim_dc:
            graphs_trim_dc[0][0].GetXaxis().SetTitle("Signal efficiency (H #rightarrow #tau#tau)")
            graphs_trim_dc[0][0].GetYaxis().SetTitle("Minimum bias rejection")
            graphs_trim_dc[0][0].GetXaxis().SetLimits(0, 1)
            graphs_trim_dc[0][0].GetYaxis().SetRangeUser(0, 1)
            graphs_trim_dc[0][0].Draw("AP")
            for g, _ in graphs_trim_dc[1:]:
                g.Draw("P same")
            g0 = graphs_trim_dc[0][0]
            npts = g0.GetN()
            lat = ROOT.TLatex()
            lat.SetTextSize(0.025)
            lat.SetTextColor(ROOT.kBlack)
            for j in range(min(npts, len(first_curve_labels))):
                x = g0.GetX()[j]
                y = g0.GetY()[j]
                lat.DrawLatex(x + 0.02, y - 0.02, first_curve_labels[j])
            ROOT.TLatex().DrawLatex(0, 1.01, "#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
            ROOT.TLatex().SetTextAlign(31)
            ROOT.TLatex().DrawLatex(0.88, 1.01, "#scale[0.9]{(14 TeV)}")
            leg = ROOT.TLegend(0.60, 0.45, 0.80, 0.85)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.045)
            leg.SetHeader("d_{c} (trim: points = dz cut)")
            for g, dc_v in graphs_trim_dc:
                leg.AddEntry(g, f"d_{{c}} = {dc_v:.2f}", "p")
            leg.Draw()
            c_trim_dc.Print('Plots_compare/ROC_trim_dc_dz_style.png')
            ofile.cd()
            c_trim_dc.Write()
except Exception:
    pass

# ROC trimming: Signal efficiency vs Minimum Bias Rejection (dc=0.2, dm_offset=0.2) — single curve
try:
    c1 = ROOT.TCanvas("ROC_trim_all", "", 700, 700)
    curves = [("no trim", f"h_PU200_dm_offset0.{dm_off_roc:02d}_match_efficiency", f"h_minBias_dm_offset0.{dm_off_roc:02d}_ncluster")]
    for ts, cut_val in trim_suffixes:
        curves.append((f"trim: #geq2 |dz|<{cut_val}", f"h_PU200_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_match_efficiency", f"h_minBias_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_ncluster"))
    graphs_trim = []
    for idx, (label, name_sig, name_bkg) in enumerate(curves):
        h_s = get_histogram(file, name_sig)
        h_b = get_histogram(file, name_bkg)
        if not h_s or not h_b:
            continue
        n_dc = min(h_s.GetNbinsY(), h_b.GetNbinsY())
        nx_b = h_b.GetNbinsX()
        i_best = 1
        best = abs(h_s.GetYaxis().GetBinCenter(1) - dc_trim_roc)
        for i in range(2, n_dc + 1):
            d = abs(h_s.GetYaxis().GetBinCenter(i) - dc_trim_roc)
            if d < best:
                best = d
                i_best = i
        den_s = h_s.Integral(1, 2, i_best, i_best)
        den_b = h_b.Integral(1, nx_b, i_best, i_best)
        x1, y1 = [], []
        if den_s > 0 and den_b > 0:
            x1.append(h_s.Integral(2, 2, i_best, i_best) / den_s)
            y1.append(h_b.Integral(1, 1, i_best, i_best) / den_b)
        if len(x1) == 0:
            continue
        g = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
        graphs_trim.append((g, label))
    if graphs_trim:
        n_pts = len(graphs_trim)
        x_all = [g.GetX()[0] for g, _ in graphs_trim]
        y_all = [g.GetY()[0] for g, _ in graphs_trim]
        g_curve = ROOT.TGraph(n_pts, array('d', x_all), array('d', y_all))
        g_curve.SetMarkerStyle(20)
        g_curve.SetMarkerSize(1.2)
        g_curve.SetMarkerColor(ROOT.kBlack)
        g_curve.SetLineColor(ROOT.kBlack)
        g_curve.GetXaxis().SetTitle("Signal efficiency (H #rightarrow #tau#tau)")
        g_curve.GetYaxis().SetTitle("Minimum Bias Rejection")
        g_curve.GetXaxis().SetLimits(0, 1)
        g_curve.GetYaxis().SetRangeUser(0, 1)
        g_curve.Draw("ALP")
        ROOT.TLatex().DrawLatex(0, 1.01, "#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
        ROOT.TLatex().SetTextAlign(31)
        ROOT.TLatex().DrawLatex(0.88, 1.01, "#scale[0.9]{14 TeV}")
        leg = ROOT.TLegend(0.18, 0.55, 0.55, 0.88)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetHeader("trim: keep trk if #geq2 pairwise |dz|<cut (cm), d_{c}=0.2, d_{m}=0.4")
        for lab in [lbl for _, lbl in graphs_trim]:
            leg.AddEntry(g_curve, lab, "lp")
        leg.Draw()
        c1.Print('Plots_compare/ROC_trim_all.png')
        ofile.cd()
        c1.Write()
except Exception:
    pass

# ROC_trim_all without clustering efficiency: dc scan format (all trim curves on one graph)
# X = trim_match_eff(bin2)/no_trim_match_eff(bin2), Y = trim_ncluster.Integral(1,2)/no_trim_ncluster.Integral(3,last)
trim_suffixes_noeff = [("0p1", 0.1), ("0p5", 0.5), ("1", 1), ("1p5", 1.5), ("2", 2)]
try:
    c2 = ROOT.TCanvas("ROC_trim_all_noeff", "", 700, 700)
    h_no_trim_eff = get_histogram(file, f"h_PU200_dm_offset0.{dm_off_roc:02d}_match_efficiency")
    h_no_trim_bkg = get_histogram(file, f"h_minBias_dm_offset0.{dm_off_roc:02d}_ncluster")
    if h_no_trim_eff and h_no_trim_bkg:
        n_dc = min(h_no_trim_eff.GetNbinsY(), h_no_trim_bkg.GetNbinsY())
        nx_b = h_no_trim_bkg.GetNbinsX()
        colors = [1, 2, 4, 6, 8, 9]
        curves_noeff = []
        # no trim: at each dc, X=1, Y = no_trim ncluster(1,2)/no_trim ncluster(3,last)
        x_no = []
        y_no = []
        for i in range(1, n_dc + 1):
            den_b = h_no_trim_bkg.Integral(3, nx_b, i, i)
            if den_b > 0:
                x_no.append(1.0)
                y_no.append(h_no_trim_bkg.Integral(1, 2, i, i) / den_b)
        if len(x_no) > 0:
            g_no = ROOT.TGraph(len(x_no), array('d', x_no), array('d', y_no))
            g_no.SetMarkerStyle(20)
            g_no.SetMarkerColor(colors[0])
            g_no.SetLineColor(colors[0])
            curves_noeff.append((g_no, "no trim"))
        for idx, (ts, cut_val) in enumerate(trim_suffixes_noeff):
            h_trim_eff = get_histogram(file, f"h_PU200_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_match_efficiency")
            h_trim_bkg = get_histogram(file, f"h_minBias_dm_offset0.{dm_off_roc:02d}_trim_maxdz{ts}_ncluster")
            if not h_trim_eff or not h_trim_bkg:
                continue
            x_vals = []
            y_vals = []
            for i in range(1, n_dc + 1):
                den_eff = h_no_trim_eff.Integral(2, 2, i, i)
                den_b = h_no_trim_bkg.Integral(3, nx_b, i, i)
                if den_eff > 0 and den_b > 0:
                    x_vals.append(h_trim_eff.Integral(2, 2, i, i) / den_eff)
                    y_vals.append(h_trim_bkg.Integral(1, 2, i, i) / den_b)
            if len(x_vals) > 0:
                g = ROOT.TGraph(len(x_vals), array('d', x_vals), array('d', y_vals))
                g.SetMarkerStyle(21 + (idx % 5))
                g.SetMarkerColor(colors[(idx + 1) % len(colors)])
                g.SetLineColor(colors[(idx + 1) % len(colors)])
                curves_noeff.append((g, f"trim: #geq2 |dz|<{cut_val}"))
        if curves_noeff:
            curves_noeff[0][0].GetXaxis().SetTitle("trim match eff / no-trim match eff (bin 2)")
            curves_noeff[0][0].GetYaxis().SetTitle("trim ncluster(1,2)/no-trim ncluster(3,last)")
            curves_noeff[0][0].GetXaxis().SetLimits(0, 1.1)
            curves_noeff[0][0].GetYaxis().SetRangeUser(0, 1.1)
            curves_noeff[0][0].Draw("ALP")
            for g, _ in curves_noeff[1:]:
                g.Draw("LP same")
            ROOT.TLatex().DrawLatex(0, 1.01, "#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
            ROOT.TLatex().SetTextAlign(31)
            ROOT.TLatex().DrawLatex(0.88, 1.01, "#scale[0.9]{14 TeV}")
            leg = ROOT.TLegend(0.18, 0.50, 0.55, 0.88)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.SetHeader("trim: keep trk if #geq2 pairwise |dz|<cut; dc scan, d_{m}=0.4")
            for g, lab in curves_noeff:
                leg.AddEntry(g, lab, "lp")
            leg.Draw()
            c2.Print('Plots_compare/ROC_trim_all_noeff.png')
            ofile.cd()
            c2.Write()
except Exception:
    pass

# max(dz) distribution: project 2D (max_dz vs dc) to 1D; minBias vs PU200 vs signal-only
dm_offset_list_maxdz = [5, 10, 15, 20, 25, 30]
for off in dm_offset_list_maxdz:
    h_pu200_maxdz = get_histogram(file, f"h_PU200_dm_offset0.{off:02d}_max_dz")
    h_minb_maxdz = get_histogram(file, f"h_minBias_dm_offset0.{off:02d}_max_dz")
    h_pu200_sig = get_histogram(file, f"h_PU200_dm_offset0.{off:02d}_max_dz_signal_only")
    if h_pu200_maxdz and h_minb_maxdz:
        p_minb = h_minb_maxdz.ProjectionX(f"minBias_max_dz_px_{off}", 1, h_minb_maxdz.GetNbinsY())
        p_pu200 = h_pu200_maxdz.ProjectionX(f"PU200_max_dz_px_{off}", 1, h_pu200_maxdz.GetNbinsY())
        if p_minb.Integral() > 0:
            p_minb.Scale(1.0 / p_minb.Integral())
        if p_pu200.Integral() > 0:
            p_pu200.Scale(1.0 / p_pu200.Integral())
        cname = f"max_dz_dm_offset0_{off}"
        c1 = ROOT.TCanvas(cname, "", 700, 700)
        c1.SetLogy()
        p_minb.SetLineColor(1)
        p_minb.SetMarkerColor(1)
        p_pu200.SetLineColor(2)
        p_pu200.SetMarkerColor(2)
        p_minb.GetXaxis().SetTitle("max|dz| [cm]")
        p_minb.GetYaxis().SetTitle("a.u.")
        p_minb.GetYaxis().SetRangeUser(1e-4, 2)
        p_minb.Draw("ep")
        p_pu200.Draw("ep same")
        leg = ROOT.TLegend(0.5, 0.65, 0.88, 0.88)
        leg.SetBorderSize(0)
        leg.AddEntry(p_minb, "MinBias", "lp")
        leg.AddEntry(p_pu200, "PU 200", "lp")
        if h_pu200_sig:
            p_sig = h_pu200_sig.ProjectionX(f"PU200_max_dz_signal_px_{off}", 1, h_pu200_sig.GetNbinsY())
            if p_sig.Integral() > 0:
                p_sig.Scale(1.0 / p_sig.Integral())
            p_sig.SetLineColor(4)
            p_sig.SetMarkerColor(4)
            p_sig.Draw("ep same")
            leg.AddEntry(p_sig, "PU 200 (signal only)", "lp")
        ROOT.TLatex().DrawLatex(0.12, 0.92, "#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
        ROOT.TLatex().SetTextAlign(31)
        ROOT.TLatex().DrawLatex(0.88, 0.92, "#scale[0.9]{14 TeV}")
        leg.Draw()
        c1.Print(f'Plots_compare/max_dz_dm_offset0.{off:02d}.png')
        ofile.cd()
        c1.Write()

# Cutflow / efficiency (optional: only if these histograms exist in file)
hist2 = get_histogram(file, "h_PU200_trk_cutflow")
hist3 = get_histogram(file, "h_minBias_trk_cutflow")
if hist2 and hist3:
    efficienciesPlot(None, hist2, hist3, True, 'Plots_compare/efficiency_6trk_evt.png')

file.Close()
ofile.Close()