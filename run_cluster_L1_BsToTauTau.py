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

def calculate_invariant_mass(lorentz_vectors):
    total_vector = ROOT.TLorentzVector()
    for vec in lorentz_vectors:
        total_vector += vec
    return total_vector.M()  # Return the invariant mass

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
                circle.SetLineWidth(1.2) 
                circle.SetLineColor(6) 
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
            c1 = ROOT.TCanvas("c1","",1000,750)
            pad1 = ROOT.TPad("pad1", "Pad 1", 0.0, 0.0, 0.75, 1.0)
            pad2 = ROOT.TPad("pad2", "Pad 2", 0.75, 0.0, 1.0, 1.0)
            pad1.Draw()
            pad2.Draw()
            pad1.cd()
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
                circle.SetLineColor(6) 
                ellipses.append(circle)
            for circle in ellipses:
                circle.Draw("same")
            
            cms_lat=ROOT.TLatex()
            cms_lat.SetTextSize(0.040)
            cms_lat.SetTextAlign(11)
            #cms_lat.DrawLatex(-3.5,3.35,"#bf{CMS}#scale[0.7]{#font[52]{  Phase-2 Simulation Preliminary  }}#scale[0.75]{PU200(14 TeV)}")
            cms_lat.DrawLatex(-3,3.35,"#bf{CMS} #scale[0.8]{#font[52]{Phase-2 Simulation Preliminary}}")
            cms_lat.DrawLatex(1.5,3.35,"#scale[0.9]{PU 200 (14 TeV)}")
    
            pad2.cd()
            #leg = ROOT.TLegend(0.67, 0.70, 0.97, 0.98)
            leg = ROOT.TLegend(0.00, 0.70, 0.50, 0.9)
            leg.SetBorderSize(0)
            leg.SetLineColor(0)
            #leg.SetFillStyle(0)
            leg.SetTextSize(0.075)
            #leg.SetHeader(f"cone size: {str(str_size)}")
            leg.AddEntry(self.graph[name1], "Track passing quality criteria", 'p')
            leg.AddEntry(self.graph[name2], "Track failing quality criteria", 'p')
            if not "minBias" in str(self.graph[name1].GetName()):
                leg.AddEntry(self.graph[name3], "#pi^{+} Matched Track", 'p')
                leg.AddEntry(self.graph[name4], "#pi^{-} Matched Track", 'p')
            leg.Draw()
            str_size = str_size.replace(".","")
            c1.Update()
            c1.SaveAs(f"plot/{name1}_full_{self.count}_{ntrk}_{str_size}.png")
            c1.Close()
            del c1

    def dbscan_cluster(self, radius, min_points, data, idx, pt, dz):
        dbscan = DBSCAN(eps=radius, min_samples=6, metric=circle_distance)
        
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
                if label not in mass:
                    mass[label] = {'dz': dzmax}
                else:
                    mass[label]['dz'] = dzmax

                # # Generate all combinations of 6 tracks in the current cluster
                # track_combinations = list(itertools.combinations(range(len(cluster_pts)), 6))
                # highest_pt_indices = np.argsort(cluster_pts)[-6:]

                # lorentz_vectors = []
                # for i in highest_pt_indices:
                #     eta_value = cluster_points[i, 0]
                #     phi_value = cluster_points[i, 1]
                #     pt_value = cluster_pts[i]
                #     lorentz_vector = create_lorentz_vector(pt_value, eta_value, phi_value)
                #     lorentz_vectors.append(lorentz_vector)

                # high_invariant_mass = calculate_invariant_mass(lorentz_vectors)

                # # Initialize variables to store the best combination
                # best_invariant_mass = float('inf')  # Set initial mass to a large value

                # # Iterate through all combinations of 6 tracks
                # for comb in track_combinations:
                #     lorentz_vectors = []
                #     for i in comb:
                #         eta_value = cluster_points[i, 0]
                #         phi_value = cluster_points[i, 1]
                #         pt_value = cluster_pts[i]
                #         lorentz_vector = create_lorentz_vector(pt_value, eta_value, phi_value)
                #         lorentz_vectors.append(lorentz_vector)
                    
                #     # Calculate the invariant mass for this combination
                #     invariant_mass = calculate_invariant_mass(lorentz_vectors)

                #     # Check if this invariant mass is closer to 1 than the previous best
                #     if abs(invariant_mass - 5.36689) < abs(best_invariant_mass - 5.36689):
                #         best_invariant_mass = invariant_mass

                # Initialize or update the mass dictionary for the current cluster
                # if label not in mass:
                #     mass[label] = {'dz': dzmax, 'sum': ROOT.TLorentzVector(), 'mass': best_invariant_mass, 'mass_': high_invariant_mass}
                #     mass[label] = {'dz': dzmax, 'sum': ROOT.TLorentzVector(), 'mass': best_invariant_mass, 'mass_': high_invariant_mass}
                # else:
                #     mass[label]['dz'] = dzmax
                #     mass[label]['mass'] = best_invariant_mass

                # # Sum the Lorentz vectors for all points in this cluster
                # for i in range(len(cluster_points)):
                #     eta_value = cluster_points[i, 0]
                #     phi_value = cluster_points[i, 1]
                #     pt_value = cluster_pts[i]
                #     mass[label]['sum'] += create_lorentz_vector(pt_value, eta_value, phi_value)

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
        cone = 0.1 
        cluster = {}  # Correct definition as a dictionary

        for size in np.arange(cone, cone + 0.5, 0.1):
            str_size = f"{size:.1f}"  # Formatting size as a string for dictionary keys
            n_clusters, cluster_info, mass = self.dbscan_cluster(size, 6, data, idx, pt, dz)
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

                if int(info['gen_true']) >= 6 or npu == "minBias":
                    matched_clusters += 1
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_ntrk", int(info['total']), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_ntrue", int(info['gen_true']), size)
                    self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_nfake", int(info['gen_fake']), size)
                    # self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_mass", mass[label]['sum'].M(), size)
                    # self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_dzmax", mass[label]['dz'], size)
                    # self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_invmass_6trk", mass[label]['mass'], size)
                    # self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_invmass_6htrk", mass[label]['mass_'], size)

            self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_ncluster", n_clusters, size)
            if matched_clusters > 0: self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_efficiency", 1, size)
            else: self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_efficiency", 0, size)
            self.fill_2d_histogram(f"h_{npu}_cluster_{obj}{ntrk}_match_ncluster", matched_clusters, size)

        return cluster 

def process_tracks(tree, npu, histogram_manager):
    evt = -1
    start_time = time.time()
    Nevt = tree.GetEntries()

    ncnt0 = 0
    ncnt1 = 0
    ncnt2 = 0
    ncnt3 = 0
    ncnt4 = 0
    ncnt5 = 0

    print(f'Total number of events: {Nevt}')

    for entry in tree:
        evt += 1
        if evt % 30 == 0:
            time_elapsed = time.time() - start_time
            print(f'{float(evt) / float(Nevt) * 100:.2f}% processed at {float(evt) / time_elapsed:.2f} Hz')

        ntrk = 0
        ntrk1 = 0
        ntrk2 = 0
        ntrk3 = 0
        ntrk4 = 0
        data_ntrk = []
        data_MVA = []
        idx_ntrk = []
        idx_MVA = []
        idx_pT1 = []
        idx_dz1 = []
        idx_pT2 = []
        idx_dz2 = []
        flag = False
        x_tot = []
        y_tot = []
        x_pip = []
        y_pip = []
        x_pim = []
        y_pim = []
        x_fai = []
        y_fai = []
        n0 = 0
        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        mva__ = 0
        mva_pt = 0
        mva_pt_ = 0
        ntrk_1 = 0

        for igen in range(len(tree.gen_pt)):
            histogram_manager.fill_histogram(f"h_{npu}_gen_pt", tree.gen_pt[igen])
            histogram_manager.fill_histogram(f"h_{npu}_gen_eta", tree.gen_eta[igen])
            histogram_manager.fill_histogram(f"h_{npu}_gen_phi", tree.gen_phi[igen])

        for itrk in range(len(tree.trk_pt)):
            if abs(tree.trk_eta[itrk]) < 2.0 and tree.trk_MVA[itrk] < 0.997:
                ntrk3 += 1
            if (tree.trk_gen[itrk] == 0 and "PU" in npu): continue
            if not (abs(tree.trk_eta[itrk]) < 2.0): continue
            flag = True
            mva_pt  += tree.trk_pt[itrk]*tree.trk_MVA[itrk]
            mva_pt_ += tree.trk_pt[itrk]
            mva__   += tree.trk_MVA[itrk]
            ntrk_1 += 1

        if flag == True:
            histogram_manager.fill_histogram(f"h_{npu}_trk_wMVA", mva_pt/mva_pt_)
            histogram_manager.fill_histogram(f"h_{npu}_trk_uMVA", mva__/ntrk_1)
        else:
            mva__ = -1
            ntrk_1 = 1

        for itrk in range(len(tree.trk_pt)):
            if not (abs(tree.trk_eta[itrk]) < 2.0 and tree.trk_MVA[itrk] < 0.997):
                x_fai.append(tree.trk_phi[itrk])
                y_fai.append(tree.trk_eta[itrk])
            ntrk += 1
            if abs(tree.trk_eta[itrk]) < 2.0:
                ntrk1 += 1
                if (mva__/ntrk_1 < 0.93 or mva__/ntrk_1 > 0.98):
                    data_MVA.append([tree.trk_phi[itrk], tree.trk_eta[itrk]])
                    idx_MVA.append(tree.trk_gen[itrk])
                    idx_pT2.append(tree.trk_pt[itrk])
                    idx_dz2.append(tree.trk_dz[itrk])
                    ntrk2 += 1
                if tree.trk_MVA[itrk] < 0.997:
                    data_ntrk.append([tree.trk_phi[itrk], tree.trk_eta[itrk]])
                    idx_ntrk.append(tree.trk_gen[itrk])
                    idx_pT1.append(tree.trk_pt[itrk])
                    idx_dz1.append(tree.trk_dz[itrk])
                    if tree.trk_gen[itrk] == 0:
                        x_tot.append(tree.trk_phi[itrk])
                        y_tot.append(tree.trk_eta[itrk])
                    if ntrk3 > 63:
                        ntrk4 += 1

            histogram_manager.fill_histogram(f"h_{npu}_trk_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_dRs", tree.trk_dRs[itrk])
            n0 += 1

            if tree.trk_gen[itrk] == 0 and "PU" in npu:
                continue
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut0_dRs", tree.trk_dRs[itrk])
            n1 += 1

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
            n2 += 1

            #if mva__/ntrk_1 > 0.93 and mva__/ntrk_1 < 0.98: continue
            if (mva__/ntrk_1 < 0.93 or mva__/ntrk_1 > 0.98):
                n3 += 1
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_pt", tree.trk_pt[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_eta", tree.trk_eta[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_phi", tree.trk_phi[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_d0", tree.trk_d0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_z0", tree.trk_z0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_MVA", tree.trk_MVA[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_dR", tree.trk_dR[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_dz", tree.trk_dz[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_dRs", tree.trk_dRs[itrk])

            if not tree.trk_MVA[itrk] < 0.997:
                continue
            n4 += 1
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_pt", tree.trk_pt[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_eta", tree.trk_eta[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_phi", tree.trk_phi[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_d0", tree.trk_d0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_z0", tree.trk_z0[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_MVA", tree.trk_MVA[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_dR", tree.trk_dR[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_dz", tree.trk_dz[itrk])
            histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_dRs", tree.trk_dRs[itrk])
            if tree.trk_gen[itrk] == 1: 
                x_pip.append(tree.trk_phi[itrk])
                y_pip.append(tree.trk_eta[itrk])
            if tree.trk_gen[itrk] == 2: 
                x_pim.append(tree.trk_phi[itrk])
                y_pim.append(tree.trk_eta[itrk])

            if ntrk3 > 63:
                n5 += 1
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_pt", tree.trk_pt[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_eta", tree.trk_eta[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_phi", tree.trk_phi[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_d0", tree.trk_d0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_z0", tree.trk_z0[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_MVA", tree.trk_MVA[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_dR", tree.trk_dR[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_dz", tree.trk_dz[itrk])
                histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_dRs", tree.trk_dRs[itrk])
                #data_dRs.append(tree.trk_phi[itrk], tree.trk_eta[itrk])
                #idx_dRs.append(tree.trk_gen[itrk])

        histogram_manager.fill_histogram(f"h_{npu}_trk_ntrk", ntrk)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut1_ntrk", ntrk1)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut2_ntrk", ntrk2)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut3_ntrk", ntrk3)
        histogram_manager.fill_histogram(f"h_{npu}_trk_cut4_ntrk", ntrk4)
        if(n0 > 5): ncnt0 += 1
        if(n1 > 5): ncnt1 += 1
        if(n2 > 5): ncnt2 += 1
        if(n3 > 5): ncnt3 += 1
        if(n4 > 5): ncnt4 += 1
        if(n5 > 5): ncnt5 += 1

        if (not "PU" in npu) or (len(x_pip) > 2 and len(x_pim) > 2):
            histogram_manager.count += 1
            histogram_manager.create_graph(f"h_{npu}_trk_cut2_eta_phi", len(x_tot), x_tot, y_tot)
            histogram_manager.create_graph(f"h_{npu}_trk_fai_eta_phi", len(x_fai), x_fai, y_fai)
            histogram_manager.create_graph(f"h_{npu}_trk_cut2_pos_eta_phi", len(x_pip), x_pip, y_pip)
            histogram_manager.create_graph(f"h_{npu}_trk_cut2_neg_eta_phi", len(x_pim), x_pim, y_pim)

            if n5 >= 6:
                cluster = histogram_manager.cluster(npu, '6', data_ntrk, idx_ntrk, idx_pT1, idx_dz1, "ntrk")
                if histogram_manager.flag:
                    histogram_manager.draw_histograms_all(f"h_{npu}_trk_cut2_eta_phi", f"h_{npu}_trk_fai_eta_phi", f"h_{npu}_trk_cut2_pos_eta_phi", f"h_{npu}_trk_cut2_neg_eta_phi", cluster, 6)
            if n3 >= 6:
                cluster = histogram_manager.cluster(npu, '6', data_MVA, idx_MVA, idx_pT2, idx_dz2, "MVA")
                if histogram_manager.flag:
                    histogram_manager.draw_histograms_all(f"h_{npu}_trk_cut2_eta_phi", f"h_{npu}_trk_fai_eta_phi", f"h_{npu}_trk_cut2_pos_eta_phi", f"h_{npu}_trk_cut2_neg_eta_phi", cluster, 6)
            # if n4 >= 6:
            #     print(f'start 2nd clustering')
            #     cluster = histogram_manager.cluster(npu, 'ant', data_dRs, idx_dRs, idx_pT, idx_dz, "dR")
            #     print(f'draw 2nd clustering')
            #     if histogram_manager.flag:
            #         histogram_manager.draw_histograms_all(f"h_{npu}_trk_cut2_eta_phi", f"h_{npu}_trk_fai_eta_phi", f"h_{npu}_trk_cut2_pos_eta_phi", f"h_{npu}_trk_cut2_neg_eta_phi", cluster, 6)

    histogram_manager.fill_bin_histogram(f"h_{npu}_trk_cutflow", 1, ncnt0)
    histogram_manager.fill_bin_histogram(f"h_{npu}_trk_cutflow", 2, ncnt1)
    histogram_manager.fill_bin_histogram(f"h_{npu}_trk_cutflow", 3, ncnt2)
    histogram_manager.fill_bin_histogram(f"h_{npu}_trk_cutflow", 4, ncnt3)
    histogram_manager.fill_bin_histogram(f"h_{npu}_trk_cutflow", 5, ncnt4)
    histogram_manager.fill_bin_histogram(f"h_{npu}_trk_cutflow", 6, ncnt5)

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
    histogram_manager.create_histogram("h_"+npu+"_trk_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_ntrk",";N_{TTrack}",150,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_wMVA",";p_{T} weighted MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_uMVA",";#mu_{MVA}",5000,0,1)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut0_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut1_ntrk",";N_{TTrack}",150,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut2_ntrk",";N_{TTrack}",150,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut3_ntrk",";N_{TTrack}",300,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_pt",";p_{T} [GeV]",400,0,20)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_eta",";#eta",250,-2.5,2.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_phi",";#phi",50,-math.pi,math.pi)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_d0",";d0",100,-1,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_z0",";z",60,-15,15)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_MVA",";MVA",5000,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_dR",";min #Delta R_{TTracks}",100,0,1)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_dz",";min #Delta z_{TTracks}",10,0,0.5)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_dRs",";min #Delta R^{*}_{TTracks}",100,0,2)
    histogram_manager.create_histogram("h_"+npu+"_trk_cut4_ntrk",";N_{TTrack}",300,0,300)

    histogram_manager.create_histogram("h_"+npu+"_trk_cutflow","",6,0,6)

    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_ncluster",";N_{Cluster}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_match_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_match_ncluster",";N_{Cluster}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_match_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_match_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_match_efficiency",";#epsilon_{Cluster}",2,0,2,5,0.1,0.6)
    #histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_dzmax", ";#Delta z^{max}_{trks}",100,0,10,5,0.1,0.6)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_mass", ";mass_{trks}",250,0,50,5,0.1,0.6)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_invmass_6trk", ";mass_{trks}",50,0,10,5,0.1,0.6)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_MVA6_invmass_6htrk", ";mass_{trks}",50,0,10,5,0.1,0.6)

    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_ncluster",";N_{Cluster}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_match_ntrk",";N_{Cluster TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_match_ncluster",";N_{Cluster}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_match_ntrue",";N_{Cluster matched TTrack}",20,0,20,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_match_nfake",";N_{Cluster fake TTrack}",40,0,40,5,0.1,0.6)
    histogram_manager.create_2d_histogram("h_"+npu+"_cluster_ntrk6_match_efficiency",";#epsilon_{Cluster}",2,0,2,5,0.1,0.6)
    # histogram_manager.create_2d_histogram("h_"+npu+"_cluster_dRs6_mass",";mass_{trks}",500,0,50,5,0.3,0.8)

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
        main(f'Tau3pi_PY8_PU200_GTT_188.root', flag)
    elif file_number == 'PU0':
        main(f'/eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU0_GTT_{arg1}.root', flag)
    elif file_number == 'PU200':
        main(f'/eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU200_GTT_{arg1}.root', flag)
    else:
        main(f'/eos/cms/store/user/chuh/l1p2/skim/MinBias_TuneCP5_14TeV-pythia8_GTT_{arg1}.root', flag)
