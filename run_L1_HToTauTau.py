import os
import math
import sys
import time
import ROOT
import itertools
import numpy as np
from array import array
from sklearn.cluster import DBSCAN
from DeltaR import returndR
from officialStyle import officialStyle

ROOT.gROOT.SetBatch(True)
officialStyle(ROOT.gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

class HistogramManager:
    def __init__(self, output_file):
        self.output_file = ROOT.TFile(output_file, 'RECREATE')
        self.histograms = {}
        self.graph = {}
        self.count = 0
        self.flag = True

    def create_histogram(self, name, title, bins, x_min, x_max):
        self.histograms[name] = ROOT.TH1F(name, title, bins, x_min, x_max)

    def fill_histogram(self, name, value):
        if name in self.histograms:
            self.histograms[name].Fill(value)

    def fill_bin_histogram(self, name, bin, value):
        if name in self.histograms:
            self.histograms[name].SetBinContent(bin, value)

    def create_2d_histogram(self, name, title, binx, x_min, x_max, biny, y_min, y_max):
        self.histograms[name] = ROOT.TH2F(name, title, binx, x_min, x_max, biny, y_min, y_max)

    def create_graph(self, name, bin, x, y):
        if len(x) > 0 and len(y) > 0:
            x_array = array('d', [float(val) for val in x])
            y_array = array('d', [float(val) for val in y])
            self.graph[name] = ROOT.TGraph(bin, y_array, x_array)
        else:
            self.graph[name] = ROOT.TGraph()
        self.graph[name].SetName(name)

    def fill_2d_histogram(self, name, valuex, valuey):
        if name in self.histograms:
            self.histograms[name].Fill(valuex, valuey)

    def write_histograms(self):
        self.output_file.cd()
        for histogram in self.histograms.values():
            histogram.Write()
        self.output_file.Close()

    def reset_histograms(self, name):
        #self.histograms[name].Reset()
        self.graph[name].Set(0)

def process_tracks(tree, npu, histogram_manager):
    evt = -1
    start_time = time.time()
    Nevt = tree.GetEntries()

    print(f'Total number of events: {Nevt}')

    for entry in tree:
        evt += 1
        if evt % 500 == 0:
            time_elapsed = time.time() - start_time
            print(f'{float(evt) / float(Nevt) * 100:.2f}% processed at {float(evt) / time_elapsed:.2f} Hz')

        ntrk = 0

        for igen in range(len(tree.gen_pt)):
            histogram_manager.fill_histogram(f"h_{npu}_gen_pt", tree.gen_pt[igen])
            histogram_manager.fill_histogram(f"h_{npu}_gen_eta", tree.gen_eta[igen])
            histogram_manager.fill_histogram(f"h_{npu}_gen_phi", tree.gen_phi[igen])

        for itrk in range(len(tree.trk_pt)):
            ntrk += 1

            histogram_manager.fill_histogram(f"h_{npu}_trk_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_MVA", tree.trk_MVA[itrk])

            if tree.trk_gen[itrk] == 0 and "PU" in npu:
                continue
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_MVA", tree.trk_MVA[itrk])

        histogram_manager.fill_histogram(f"h_{npu}_trk_ntrk", ntrk)

def main(input_file, flag):
    output_file = "output.root"

    print(input_file)
    tree = ROOT.TChain("eventTree")
    tree.Add(input_file)

    if not tree:
        print(f"Error: Could not retrieve 'tree' from {input_file}")
        return

    if "PU0" in str(input_file):
        npu = "PU0"
    elif "PU200" in str(input_file):
        npu = "PU200"
    else:
        npu = "minBias"

    histogram_manager = HistogramManager(output_file)
    histogram_manager.create_histogram("h_"+npu+"_gen_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_gen_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_gen_phi",";#phi",50,-math.pi,math.pi)

    histogram_manager.create_histogram("h_"+npu+"_trk_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_ntrk",";N_{TTrack}",150,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_MVA",";MVA",5000,0,1)

    histogram_manager.flag = flag
    process_tracks(tree, npu, histogram_manager)

    histogram_manager.write_histograms()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_cluster_L1_BsToTauTau.py <file_number> <arg1> <flag>")
        sys.exit(1)

    file_number = sys.argv[1]
    arg1 = sys.argv[2]
    flag = True if len(sys.argv) == 4 else False

    if arg1 == 'test':
        main(f'/eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU200_GTT_188.root', flag)
    elif file_number == 'PU200':
        main(f'/eos/cms/store/user/chuh/l1p2/skim/HTau3pi_PY8_PU200_GTT_{arg1}.root', flag)
    else:
        main(f'/eos/cms/store/user/chuh/l1p2/skim/MinBias_TuneCP5_14TeV-pythia8_GTT_{arg1}.root', flag)
