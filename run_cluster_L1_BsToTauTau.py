import os
import math
import sys
import time
import ROOT
import argparse
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

def spherical_distance(point1, point2):
    delta_eta = point1[0] - point2[0]
    delta_phi = math.fmod(point1[1] - point2[1] + 3 * math.pi, 2 * math.pi) - math.pi
    delta_z = point1[2] - point2[2]
    return np.sqrt(delta_eta**2 + delta_phi**2 + delta_z**2)


def circle_distance(point1, point2):
    delta_eta = point1[0] - point2[0]
    delta_phi = math.fmod(point1[1] - point2[1] + 3 * math.pi, 2 * math.pi) - math.pi
    return np.sqrt(delta_eta**2 + delta_phi**2)

def create_lorentz_vector(pt, eta, phi):
    vec = ROOT.TLorentzVector()
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    mass = 0.13957
    E = math.sqrt(px**2 + py**2 + pz**2 + mass**2)
    vec.SetPxPyPzE(px, py, pz, E)
    return vec

class HistogramManager:
    def __init__(self, output_file):
        self.output_file = ROOT.TFile(output_file, 'RECREATE')
        self.histograms = {}
        self.graph = {}
        self.count = 0

    def create_histogram(self, name, title, bins, x_min, x_max):
        self.histograms[name] = ROOT.TH1F(name, title, bins, x_min, x_max)

    def fill_histogram(self, name, value):
        if name in self.histograms:
            self.histograms[name].Fill(value)

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

    def draw_histograms(self, name1, name2, name3, cluster, ntrk):
        if not os.path.exists('plot'):
            os.makedirs('plot')
        self.graph[name1].SetMarkerSize(1)
        self.graph[name2].SetMarkerSize(2)
        self.graph[name3].SetMarkerSize(2)
        self.graph[name1].SetMarkerStyle(4)
        self.graph[name2].SetMarkerStyle(29)
        self.graph[name3].SetMarkerStyle(29)
        self.graph[name1].SetMarkerColor(1)
        self.graph[name2].SetMarkerColor(2)
        self.graph[name3].SetMarkerColor(4)
        self.graph[name1].GetXaxis().SetLimits(-3.2, 3.2)
        self.graph[name1].SetMinimum(-3.2)
        self.graph[name1].SetMaximum(3.2)
        self.graph[name1].GetXaxis().SetTitle("#eta")
        self.graph[name1].GetYaxis().SetTitle("#phi")
        for size, centers in cluster.items():
            c1 = ROOT.TCanvas("c1","",700,700)
            self.graph[name1].Draw('ap')
            if not "minBias" in str(self.graph[name1].GetName()):
                self.graph[name2].Draw('psame')
                self.graph[name3].Draw('psame')
            ellipses = []
            for center in centers:
                circle = ROOT.TEllipse(center[1], center[0], float(size)/2)
                circle.SetFillStyle(0)
                circle.SetLineWidth(1) 
                ellipses.append(circle)
            for circle in ellipses:
                circle.Draw("same")
            leg = ROOT.TLegend(0.65, 0.87, 0.9, 0.97)
            leg.SetBorderSize(0)
            leg.SetFillColor(10)
            leg.SetLineColor(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.05)
            leg.AddEntry(self.graph[name1], "Total", 'p')
            if not "minBias" in str(self.graph[name1].GetName()):
                leg.AddEntry(self.graph[name2], "#pi^{+} Matched", 'p')
                leg.AddEntry(self.graph[name3], "#pi^{-} Matched", 'p')
            leg.Draw()
            size = size.replace(".","")
            c1.SaveAs(f"plot/{name1}_{self.count}_{ntrk}_{size}.png")

    def draw_histograms_all(self, name1, name2, name3, name4, cluster, ntrk):
        if not os.path.exists('plot'):
            os.makedirs('plot')
        self.graph[name1].SetMarkerSize(1)
        self.graph[name2].SetMarkerSize(1)
        self.graph[name3].SetMarkerSize(2)
        self.graph[name4].SetMarkerSize(2)
        self.graph[name1].SetMarkerStyle(4)
        self.graph[name2].SetMarkerStyle(4)
        self.graph[name3].SetMarkerStyle(29)
        self.graph[name4].SetMarkerStyle(29)
        self.graph[name1].SetMarkerColor(1)
        self.graph[name2].SetMarkerColor(8)
        self.graph[name3].SetMarkerColor(2)
        self.graph[name4].SetMarkerColor(4)
        self.graph[name1].GetXaxis().SetLimits(-3.2, 3.2)
        self.graph[name1].SetMinimum(-3.2)
        self.graph[name1].SetMaximum(3.2)
        self.graph[name1].GetXaxis().SetTitle("#eta")
        self.graph[name1].GetYaxis().SetTitle("#phi")
        for size, centers in cluster.items():
            c1 = ROOT.TCanvas("c1","",700,700)
            self.graph[name1].Draw('ap')
            self.graph[name2].Draw('psame')
            size = float(size)
            str_size = f"{size:.1f}" 
            self.graph[f"h_trk_core_eta_phi_{str(str_size)}"].SetMarkerStyle(4)
            self.graph[f"h_trk_core_eta_phi_{str(str_size)}"].SetMarkerColor(38)
            self.graph[f"h_trk_core_eta_phi_{str(str_size)}"].Draw('psame')
            self.graph[f"h_trk_border_eta_phi_{str(str_size)}"].SetMarkerStyle(4)
            self.graph[f"h_trk_border_eta_phi_{str(str_size)}"].SetMarkerColor(41)
            self.graph[f"h_trk_border_eta_phi_{str(str_size)}"].Draw('psame')
            if not "minBias" in str(self.graph[name1].GetName()):
                self.graph[name3].Draw('psame')
                self.graph[name4].Draw('psame')
            ellipses = []
            for center in centers:
                circle = ROOT.TEllipse(center[1], center[0], float(size)/2)
                circle.SetFillStyle(0)
                circle.SetLineWidth(1) 
                ellipses.append(circle)
            for circle in ellipses:
                circle.Draw("same")
            leg = ROOT.TLegend(0.63, 0.81, 0.9, 0.97)
            leg.SetBorderSize(0)
            leg.SetFillColor(10)
            leg.SetLineColor(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.05)
            leg.AddEntry(self.graph[name1], "Pass selection", 'p')
            leg.AddEntry(self.graph[name2], "Fail selection", 'p')
            if not "minBias" in str(self.graph[name1].GetName()):
                leg.AddEntry(self.graph[name3], "#pi^{+} Matched", 'p')
                leg.AddEntry(self.graph[name4], "#pi^{-} Matched", 'p')
            leg.Draw()
            str_size = str_size.replace(".","")
            c1.SaveAs(f"plot/{name1}_full_{self.count}_{ntrk}_{str_size}.png")

    def dbscan_cluster(self, radius, min_points, data, idx, pt, dz):
        metric = circle_distance if len(data[0]) == 2 else spherical_distance
        dbscan = DBSCAN(eps=radius, min_samples=min_points, metric=metric)
        
        labels = dbscan.fit_predict(data)
        clustered_data = np.hstack((data, labels.reshape(-1, 1)))
        unique_labels = set(labels)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        cluster_info = {}
        mass = {}
        data = np.array(data)
        pt = np.array(pt)
        dz = np.array(dz)
        idx = np.array(idx)

        # Identify core samples
        core_samples_mask = np.zeros_like(labels, dtype=bool)
        core_samples_mask[dbscan.core_sample_indices_] = True

        core_points = data[core_samples_mask]
        border_points = data[(labels != -1) & ~core_samples_mask]

        str_size = f"{radius:.1f}"
        self.create_graph(f"h_trk_core_eta_phi_{str(str_size)}", len(core_points), core_points[:, 0], core_points[:, 1])
        self.create_graph(f"h_trk_border_eta_phi_{str(str_size)}", len(border_points), border_points[:, 0], border_points[:, 1])

        for label in unique_labels:
            if label != -1:  # Exclude noise
                # Get all points (tracks) in the current cluster
                cluster_points = data[labels == label]
                cluster_pts = pt[labels == label]
                cluster_dzs = dz[labels == label]
                cluster_idxs = idx[labels == label]  # Get the idx values for the current cluster

                # Calculate the maximum dz difference within the cluster
                dzmax = np.max(cluster_dzs) - np.min(cluster_dzs)

                # Initialize or update the mass dictionary for the current cluster
                if label not in mass:
                    mass[label] = {'dz': dzmax, 'sum': ROOT.TLorentzVector()}
                else:
                    mass[label]['dz'] = dzmax

                # Sum the Lorentz vectors for all points in this cluster
                for i in range(len(cluster_points)):
                    eta_value = cluster_points[i, 0]
                    phi_value = cluster_points[i, 1]
                    pt_value = cluster_pts[i]
                    mass[label]['sum'] += create_lorentz_vector(pt_value, eta_value, phi_value)

                # Calculate cluster information
                gen_positive = np.sum(cluster_idxs == 1)
                gen_negative = np.sum(cluster_idxs == 2)
                gen_fake = np.sum((cluster_idxs != 1) & (cluster_idxs != 2))
                gen_true = gen_positive + gen_negative

                # Update cluster info
                if label not in cluster_info:
                    center = np.mean(cluster_points, axis=0)
                    cluster_info[label] = {
                        'center': center, 
                        'total': len(cluster_points), 
                        'gen_positive': gen_positive, 
                        'gen_negative': gen_negative, 
                        'gen_fake': gen_fake, 
                        'gen_true': gen_true
                    }
                else:
                    cluster_info[label]['total'] += len(cluster_points)
                    cluster_info[label]['gen_positive'] += gen_positive
                    cluster_info[label]['gen_negative'] += gen_negative
                    cluster_info[label]['gen_fake'] += gen_fake
                    cluster_info[label]['gen_true'] += gen_true

        return n_clusters, cluster_info, mass

    def cluster(self, npu, ntrk, data, idx, pt, dz, obj):
        cone = 0.3 if obj == "dRs" else 0.1
        cluster = {}  # Correct definition as a dictionary

        for size in np.arange(cone, cone + 0.5, 0.1):
            str_size = f"{size:.1f}"  # Formatting size as a string for dictionary keys
            n_clusters, cluster_info, mass = self.dbscan_cluster(size, ntrk, data, idx, pt, dz)
            matched_clusters = 0

            if str_size not in cluster:
                cluster[str_size] = []  # Initialize an empty list for each size if it doesn't exist

            for label, info in cluster_info.items():
                center = info['center']
                cluster_details = [center[0], center[1]]  # Assuming 'center' has at least two dimensions
                cluster[str_size].append(cluster_details)

                self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_ntrk", int(info['total']), size)
                if n_clusters > 0:
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_ntrue", int(info['gen_true']), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_nfake", int(info['gen_fake']), size)

                if int(info['gen_true']) >= ntrk:
                    matched_clusters += 1
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_ntrk", int(info['total']), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_ntrue", int(info['gen_true']), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_nfake", int(info['gen_fake']), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_mass", mass[label]['sum'].M(), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_dzmax", mass[label]['dz'], size)

            self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_ncluster", n_clusters, size)
            if matched_clusters > 0: self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_efficiency", 1, size)
            else: self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_efficiency", 0, size)
            self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_ncluster", matched_clusters, size)

        return cluster 

def process_tracks(tree, npu, histogram_manager):
    evt = -1
    start_time = time.time()
    Nevt = tree.GetEntries()

    for entry in tree:
        evt += 1
        if evt % 10000 == 0:
            time_elapsed = time.time() - start_time
            print(f'{float(evt) / float(Nevt) * 100:.2f}% processed at {float(evt) / time_elapsed:.2f} Hz')

        ntrk = 0
        ntrk1 = 0
        ntrk2 = 0
        ntrk3 = 0
        ntrk4 = 0
        data_dR = []
        data_dRs = []
        idx_dR = []
        idx_dRs = []
        idx_pT = []
        idx_dz = []
        nct_dR = 0
        nct_dRs = 0
        flag = False
        x_tot = []
        y_tot = []
        x_pip = []
        y_pip = []
        x_pim = []
        y_pim = []
        x_fai = []
        y_fai = []

        for itrk in range(len(tree.trk_pt)):
            if not (abs(tree.trk_eta[itrk]) < 2.0 and tree.trk_dR[itrk] < 0.15 and tree.trk_MVA[itrk] < 0.997):
                x_fai.append(tree.trk_phi[itrk])
                y_fai.append(tree.trk_eta[itrk])
            ntrk += 1
            if tree.trk_MVA[itrk] < 0.997:
                ntrk1 += 1
                if abs(tree.trk_eta[itrk]) < 2.0:
                    ntrk2 += 1
                    if tree.trk_dR[itrk] < 0.15:
                        ntrk3 += 1
                        data_dR.append([tree.trk_phi[itrk], tree.trk_eta[itrk]])
                        idx_dR.append(tree.trk_gen[itrk])
                        idx_pT.append(tree.trk_pt[itrk])
                        idx_dz.append(tree.trk_dz[itrk])
                        nct_dR += 1
                        if tree.trk_gen[itrk] == 0:
                            x_tot.append(tree.trk_phi[itrk])
                            y_tot.append(tree.trk_eta[itrk])
                    if tree.trk_dRs[itrk] < 0.3:
                        ntrk4 += 1
                        data_dRs.append([tree.trk_z0[itrk], tree.trk_phi[itrk], tree.trk_eta[itrk]])
                        idx_dRs.append(tree.trk_gen[itrk])
                        nct_dRs += 1

            histogram_manager.fill_histogram(f"h_{npu}_trk_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_dRs", tree.trk_dRs[itrk])

            if tree.trk_gen[itrk] == 0 and "PU" in npu:
                continue
            flag = True
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_dRs", tree.trk_dRs[itrk])

            if not abs(tree.trk_eta[itrk]) < 2.0:
                continue
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_dRs", tree.trk_dRs[itrk])

            if not tree.trk_MVA[itrk] < 0.997:
                continue
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_dRs", tree.trk_dRs[itrk])

            if tree.trk_dRs[itrk] < 0.3:
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_pt", tree.trk_pt[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_eta", tree.trk_eta[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_phi", tree.trk_phi[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_d0", tree.trk_d0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_z0", tree.trk_z0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_MVA", tree.trk_MVA[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_dR", tree.trk_dR[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_dz", tree.trk_dz[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_dRs", tree.trk_dRs[itrk])

            if tree.trk_dR[itrk] < 0.15:
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_pt", tree.trk_pt[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_eta", tree.trk_eta[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_phi", tree.trk_phi[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_d0", tree.trk_d0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_z0", tree.trk_z0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_MVA", tree.trk_MVA[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_dR", tree.trk_dR[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_dz", tree.trk_dz[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_dRs", tree.trk_dRs[itrk])
                if tree.trk_gen[itrk] == 1: 
                    #histogram_manager.fill_2d_histogram(f"h_{npu}_trk_cut4_pos_eta_phi", tree.trk_phi[itrk], tree.trk_eta[itrk])
                    x_pip.append(tree.trk_phi[itrk])
                    y_pip.append(tree.trk_eta[itrk])
                if tree.trk_gen[itrk] == 2: 
                    #histogram_manager.fill_2d_histogram(f"h_{npu}_trk_cut4_neg_eta_phi", tree.trk_phi[itrk], tree.trk_eta[itrk])
                    x_pim.append(tree.trk_phi[itrk])
                    y_pim.append(tree.trk_eta[itrk])

        histogram_manager.fill_histogram(f"h_{npu}_trk_ntrk", ntrk)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_ntrk", ntrk1)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_ntrk", ntrk2)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_ntrk", ntrk3)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_ntrk", ntrk4)

        if (not "PU" in npu) or (len(x_pip) > 2 and len(x_pim) > 2):
            histogram_manager.count += 1
            histogram_manager.create_graph(f"h_{npu}_trk_cut4_eta_phi", len(x_tot), x_tot, y_tot)
            histogram_manager.create_graph(f"h_{npu}_trk_fai_eta_phi", len(x_fai), x_fai, y_fai)
            histogram_manager.create_graph(f"h_{npu}_trk_cut4_pos_eta_phi", len(x_pip), x_pip, y_pip)
            histogram_manager.create_graph(f"h_{npu}_trk_cut4_neg_eta_phi", len(x_pim), x_pim, y_pim)

            if nct_dR >= 6:
                cluster = histogram_manager.cluster(npu, 6, data_dR, idx_dR, idx_pT, idx_dz, "dR")
                histogram_manager.draw_histograms(f"h_{npu}_trk_cut4_eta_phi", f"h_{npu}_trk_cut4_pos_eta_phi", f"h_{npu}_trk_cut4_neg_eta_phi", cluster, 6)
                histogram_manager.draw_histograms_all(f"h_{npu}_trk_cut4_eta_phi", f"h_{npu}_trk_fai_eta_phi", f"h_{npu}_trk_cut4_pos_eta_phi", f"h_{npu}_trk_cut4_neg_eta_phi", cluster, 6)
            # if nct_dRs >= 6:
            #     cluster = histogram_manager.cluster(npu, 6, data_dRs, idx_dRs, idx_pT, idx_dz, "dRs")

def main(input_file, output_file):
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
    histogram_manager.create_histogram("h_"+npu+"_trk_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_z0",";z",150,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_ntrk",";N_{TTrack}",100,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_z0",";z",150,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_z0",";z",150,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_ntrk",";N_{TTrack}",100,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_z0",";z",150,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_ntrk",";N_{TTrack}",100,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_z0",";z",150,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_ntrk",";N_{TTrack}",100,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_z0",";z",150,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_ntrk",";N_{TTrack}",100,0,300)

    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_ncluster",";N_{Cluster}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_match_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_match_ncluster",";N_{Cluster}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_match_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_match_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_match_efficiency",";#epsilon_{Cluster}",2,0,2,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_mass", ";mass_{trks}",500,0,50,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dR6_dzmax", ";#Delta z^{max}_{trks}",400,0,20,5,0.1,0.6)

    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_ncluster",";N_{Cluster}",20,0,20,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_match_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_match_ncluster",";N_{Cluster}",20,0,20,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_match_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_match_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_match_efficiency",";#epsilon_{Cluster}",2,0,2,5,0.3,0.8)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_mass",";mass_{trks}",500,0,50,5,0.3,0.8)

    process_tracks(tree, npu, histogram_manager)

    histogram_manager.write_histograms()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_cluster_L1_BsToTauTau.py <file_number> <arg1>")
        sys.exit(1)

    file_number = sys.argv[1]
    arg1 = sys.argv[2]

    if file_number == 'PU0':
        main(f'/eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU0_GTT_{arg1}.root', "output.root")
    elif file_number == 'PU200':
        main(f'/eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU200_GTT_{arg1}.root', "output.root")
    else:
        main(f'/eos/cms/store/user/chuh/l1p2/skim/MinBias_TuneCP5_14TeV-pythia8_GTT_{arg1}.root', "output.root")