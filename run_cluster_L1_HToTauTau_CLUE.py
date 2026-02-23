import math
import os
import sys

import numpy as np
import pandas as pd
import ROOT

# --- CLUEstering Library Import ---
try:
    import CLUEstering as clue
except ImportError:
    print("Error: 'CLUEstering' library is not installed.")
    print("Please install it using: pip install CLUEstering")
    sys.exit(1)

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

# ---------------------------------------------------------
# 1. Helper Functions
# ---------------------------------------------------------

def create_lorentz_vector(pt, eta, phi):
    vec = ROOT.TLorentzVector()
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    mass = 0.13957 # pion mass
    E = math.sqrt(px**2 + py**2 + pz**2 + mass**2)
    vec.SetPxPyPzE(px, py, pz, E)
    return vec

def calculate_invariant_mass(lorentz_vectors):
    total_vector = ROOT.TLorentzVector()
    for vec in lorentz_vectors:
        total_vector += vec
    return total_vector.M()

# ---------------------------------------------------------
# 2. CLUE Wrapper
# ---------------------------------------------------------

def run_clue_wrapper(points, dc, rhoc, dm):
    """
    points: np.array shape (N,2) with columns [eta, phi]
    Returns:
      final_labels (N,), centers (nClusters,2), debug_rho (N,), debug_delta (N,)
    """
    n_points = len(points)
    if n_points == 0:
        return np.array([]), np.array([]), np.array([]), np.array([])

    # 1) Ghost Points for Phi Wrapping
    margin = dc * 1.5
    pixel_map = []
    input_list = []

    # Original points
    for i in range(n_points):
        eta, phi = points[i]
        input_list.append([eta, phi, 1.0])  # [eta, phi, weight=1]
        pixel_map.append(i)

    pi = math.pi
    two_pi = 2 * pi

    # Ghost points
    for i in range(n_points):
        eta, phi = points[i]
        if phi < -pi + margin:
            input_list.append([eta, phi + two_pi, 1.0])
            pixel_map.append(i)
        elif phi > pi - margin:
            input_list.append([eta, phi - two_pi, 1.0])
            pixel_map.append(i)

    # 2) Build input for CLUE (eta, phi in original units)
    sx0 = []
    sx1 = []
    sw = []
    for eta, phi, w in input_list:
        sx0.append(eta)
        sx1.append(phi)
        sw.append(w)

    input_data = pd.DataFrame({
        "x": np.array(sx0, dtype=np.float32),
        "y": np.array(sx1, dtype=np.float32),
        "weight": np.array(sw, dtype=np.float32),
    })

    debug_rho = np.full(n_points, -1.0, dtype=np.float32)
    debug_delta = np.full(n_points, -1.0, dtype=np.float32)

    try:
        c = clue.clusterer(dc, rhoc, dm)
        c.read_data(input_data)
        c.run_clue()

        expanded_labels = np.array(c.labels, dtype=np.int32)

        if hasattr(c, "output_df") and c.output_df is not None:
            odf = c.output_df
            if "rho" in odf.columns:
                debug_rho[:] = np.array(odf["rho"].values[:n_points], dtype=np.float32)
            if "delta" in odf.columns:
                debug_delta[:] = np.array(odf["delta"].values[:n_points], dtype=np.float32)

    except Exception as e:
        print(f"CLUE execution error: {e}")
        return np.full(n_points, -1, dtype=np.int32), np.array([]), debug_rho, debug_delta

    if len(expanded_labels) != len(input_list):
        expanded_labels = np.resize(expanded_labels, len(input_list))

    # 3) Merge clusters using Union-Find
    max_label = int(np.max(expanded_labels)) if len(expanded_labels) else -1
    if max_label == -1:
        return np.full(n_points, -1, dtype=np.int32), np.array([]), debug_rho, debug_delta

    parent = list(range(max_label + 1))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        ri = find(i)
        rj = find(j)
        if ri != rj:
            parent[rj] = ri

    original_labels_map = {}
    for i, label in enumerate(expanded_labels):
        if label == -1:
            continue
        orig_idx = pixel_map[i]
        original_labels_map.setdefault(orig_idx, set()).add(int(label))

    for orig_idx, labels in original_labels_map.items():
        if len(labels) > 1:
            labels_list = list(labels)
            base = labels_list[0]
            for k in range(1, len(labels_list)):
                union(base, labels_list[k])

    final_labels = np.full(n_points, -1, dtype=np.int32)
    for i in range(n_points):
        l = int(expanded_labels[i]) 
        if l != -1:
            final_labels[i] = find(l)

    # 4) Centers
    unique_labels = set(final_labels.tolist())
    unique_labels.discard(-1)

    centers = []
    for lbl in unique_labels:
        mask = (final_labels == lbl)
        cluster_pts = points[mask]
        mean_eta = float(np.mean(cluster_pts[:, 0]))
        phis = cluster_pts[:, 1]
        x_comp = float(np.mean(np.cos(phis)))
        y_comp = float(np.mean(np.sin(phis)))
        mean_phi = float(np.arctan2(y_comp, x_comp))
        centers.append([mean_eta, mean_phi])

    return final_labels, np.array(centers, dtype=np.float32), debug_rho, debug_delta

# ---------------------------------------------------------
# 3. Histogram Manager
# ---------------------------------------------------------

class HistogramManager:
    def __init__(self, output_file):
        self.output_file = ROOT.TFile(output_file, "RECREATE")
        self.histograms = {}

    def create_2d_histogram(self, name, title, binx, x_min, x_max, biny, y_min, y_max):
        self.histograms[name] = ROOT.TH2F(name, title, binx, x_min, x_max, biny, y_min, y_max)
        
    def fill_2d_histogram(self, name, x, y):
        if name in self.histograms:
            self.histograms[name].Fill(x, y)

    def write_histograms(self):
        self.output_file.cd()
        for hist in self.histograms.values():
            hist.Write()
        self.output_file.Close()

    def draw_event_display(self, event_idx, data_points, labels, gen_indices, params_str):
        # Create output directory
        if not os.path.exists("plot-clue"):
            os.makedirs("plot-clue")
            
        # Create canvas
        c1 = ROOT.TCanvas(f"c1_{event_idx}_{params_str}", "", 800, 800)
        c1.SetLeftMargin(0.15)
        c1.SetRightMargin(0.05)
        
        # Draw frame (axes)
        frame = ROOT.TH2F("frame", f"Event {event_idx} {params_str};#eta;#phi", 100, -3.2, 3.2, 100, -3.2, 3.2)
        frame.SetStats(0)
        frame.Draw()

        # Keep references to prevent Python garbage collection
        self.keep_alive = [] 

        # 1. Draw noise points (grey)
        g_bkg = ROOT.TGraph()
        n_bkg = 0
        for i, point in enumerate(data_points):
            if labels[i] == -1: 
                g_bkg.SetPoint(n_bkg, point[0], point[1])
                n_bkg += 1
        
        if n_bkg > 0:
            g_bkg.SetMarkerStyle(24) 
            g_bkg.SetMarkerColor(17) # Gray
            g_bkg.SetMarkerSize(0.8)
            g_bkg.Draw("P SAME")
            self.keep_alive.append(g_bkg)

        # 2. Draw clusters (color cycling)
        colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kCyan, ROOT.kOrange, ROOT.kViolet, ROOT.kTeal]
        
        # Extract unique cluster IDs (excluding noise)
        unique_labels = sorted(list(set(labels)))
        if -1 in unique_labels:
            unique_labels.remove(-1)

        for idx, lbl in enumerate(unique_labels):
            color = colors[idx % len(colors)]
            
            mask = (labels == lbl)
            cluster_pts = data_points[mask]
            
            # Compute cluster center
            mean_eta = float(np.mean(cluster_pts[:, 0]))
            phis = cluster_pts[:, 1]
            x_comp = float(np.mean(np.cos(phis)))
            y_comp = float(np.mean(np.sin(phis)))
            mean_phi = float(np.arctan2(y_comp, x_comp))

            # 2-1. Draw cluster points
            g_cluster = ROOT.TGraph()
            for k, pt in enumerate(cluster_pts):
                g_cluster.SetPoint(k, pt[0], pt[1])
            
            g_cluster.SetMarkerStyle(20) # Full Circle
            g_cluster.SetMarkerColor(color)
            g_cluster.SetMarkerSize(1.2)
            g_cluster.Draw("P SAME")
            self.keep_alive.append(g_cluster)

            # 2-2. Draw circle (radius 0.2, adjustable)
            el = ROOT.TEllipse(mean_eta, mean_phi, 0.2, 0.2)
            el.SetFillStyle(0)
            el.SetLineColor(color)
            el.SetLineWidth(3)
            el.Draw("SAME")
            self.keep_alive.append(el)

        # 3. Draw gen particle (truth) markers
        g_pi_plus = ROOT.TGraph()
        g_pi_minus = ROOT.TGraph()
        n_plus, n_minus = 0, 0
        
        for i, gen_id in enumerate(gen_indices):
            eta, phi = data_points[i]
            if gen_id == 1:
                g_pi_plus.SetPoint(n_plus, eta, phi)
                n_plus += 1
            elif gen_id == 2:
                g_pi_minus.SetPoint(n_minus, eta, phi)
                n_minus += 1

        if n_plus > 0:
            g_pi_plus.SetMarkerStyle(29) # Star
            g_pi_plus.SetMarkerColor(ROOT.kBlack)
            g_pi_plus.SetMarkerSize(2.5)
            g_pi_plus.Draw("P SAME")
            self.keep_alive.append(g_pi_plus)

        if n_minus > 0:
            g_pi_minus.SetMarkerStyle(29) # Star
            g_pi_minus.SetMarkerColor(ROOT.kBlack)
            g_pi_minus.SetMarkerSize(2.5)
            g_pi_minus.Draw("P SAME")
            self.keep_alive.append(g_pi_minus)

        # Save to file
        output_filename = f"plot-clue-final/event_{event_idx}_{params_str}.png"
        c1.SaveAs(output_filename)
        c1.Close()
        
        # Clean up references
        self.keep_alive = []

# ---------------------------------------------------------
# 4. Main Processing
# ---------------------------------------------------------

def process_tracks(tree, npu, histogram_manager, scan_params):
    evt = -1
    Nevt = tree.GetEntries()
    print(f"Total number of events: {Nevt}")
    
    fixed_rhoc = 3.0 
    
    dcs = scan_params['dc']
    dm_offsets = scan_params['dm_offset']
    max_dz_cuts = scan_params['max_dz_cuts']  # trimming: keep track if >=2 pairwise |z0_i-z0_j| < cut; drop cluster if n_trk <= 3 after trim
    dc_min = 0.0
    dc_max = max(dcs) * 1.2
    n_bins_dc = 50

    def _trim_suffix(cut):
        if cut == 0: return "0"
        if cut == 0.5: return "0p5"
        if cut == 1.0: return "1"
        if cut == 1.5: return "1p5"
        if cut == 2.0: return "2"
        return str(cut).replace(".", "p")

    for offset in dm_offsets:
        dm_str = f"dm_offset{offset:.2f}"
        prefix = f"h_{npu}_{dm_str}"
        histogram_manager.create_2d_histogram(f"{prefix}_ncluster", f"N Clusters;Count;dc", 20, 0, 20, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_match_ncluster", f"N Matched Clusters;Count;dc", 20, 0, 20, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_ntrk", f"N Tracks/Cluster;N Tracks;dc", 20, 0, 20, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_ntrue", f"N True/Cluster;N True;dc", 10, 0, 10, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_nfake", f"N Fake/Cluster;N Fake;dc", 20, 0, 20, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_pt", f"Cluster Pt;Pt [GeV];dc", 50, 0, 100, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_mass", f"Cluster Mass;Mass [GeV];dc", 50, 0, 10, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_dz", f"Cluster z0 spread (max-min);cm;dc", 50, 0, 5, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_max_dz", f"Cluster max(dz0) (all trk);cm;dc", 50, 0, 5, n_bins_dc, dc_min, dc_max)
        if npu == "PU200":
            histogram_manager.create_2d_histogram(f"{prefix}_max_dz_signal_only", f"Cluster max(dz0) (signal trk only);cm;dc", 50, 0, 5, n_bins_dc, dc_min, dc_max)
        histogram_manager.create_2d_histogram(f"{prefix}_match_efficiency", f"Match Efficiency;IsMatched;dc", 2, 0, 2, n_bins_dc, dc_min, dc_max)
        for max_dz_cut in max_dz_cuts:
            ts = _trim_suffix(max_dz_cut)
            histogram_manager.create_2d_histogram(f"{prefix}_trim_maxdz{ts}_ncluster", f"N Clusters (trim: #geq2 |dz|<{max_dz_cut});Count;dc", 20, 0, 20, n_bins_dc, dc_min, dc_max)
            histogram_manager.create_2d_histogram(f"{prefix}_trim_maxdz{ts}_match_ncluster", f"N Matched Clusters (trim);Count;dc", 20, 0, 20, n_bins_dc, dc_min, dc_max)
            histogram_manager.create_2d_histogram(f"{prefix}_trim_maxdz{ts}_match_efficiency", f"Match Efficiency (trim);IsMatched;dc", 2, 0, 2, n_bins_dc, dc_min, dc_max)

    processed_evt_count = 0

    for entry in tree:
        evt += 1
        if evt % 100 == 0: print(f"Scanning event {evt}...")

        x_pip = []
        x_pim = []
        data_ntrk = []
        idx_gen = []
        pt = []
        z0 = []

        for i in range(len(tree.trk_pt)):
            if tree.trk_gen[i] == 1:
                x_pip.append(tree.trk_eta[i])
            if tree.trk_gen[i] == 2:
                x_pim.append(tree.trk_eta[i])
            data_ntrk.append([tree.trk_eta[i], tree.trk_phi[i]])
            idx_gen.append(tree.trk_gen[i])
            pt.append(tree.trk_pt[i])
            z0.append(tree.trk_z0[i])

        if (not "PU" in npu) or (len(x_pip) > 2 and len(x_pim) > 2):
            
            processed_evt_count += 1
            data_ntrk = np.array(data_ntrk)
            idx_gen = np.array(idx_gen)
            pt = np.array(pt)
            z0 = np.array(z0)
            if len(data_ntrk) == 0:
                continue

            for offset in dm_offsets:
                dm_str = f"dm_offset{offset:.2f}"
                prefix = f"h_{npu}_{dm_str}"

                for dc in dcs:
                    dm = dc + offset  # dm = dc + offset
                    labels, centers, _, _ = run_clue_wrapper(data_ntrk, dc=dc, rhoc=fixed_rhoc, dm=dm)
                    if processed_evt_count % 10000 == 1:
                        histogram_manager.draw_event_display(evt, data_ntrk, labels, idx_gen, f"dc{dc}_dm{dm:.2f}")

                    unique_labels = set(labels.tolist())
                    unique_labels.discard(-1)

                    n_clusters = 0
                    n_matched_clusters = 0
                    
                    # --- Efficiency: 1 if exactly 2 matched clusters (one per tau), else 0 ---
                    # Matched cluster = cluster with 3 signal tracks of the same trk_gen.
                    # We need 2 such clusters: one for gen1 (tau+), one for gen2 (tau-).
                    indices_gen1 = np.where(idx_gen == 1)[0]
                    indices_gen2 = np.where(idx_gen == 2)[0]
                    labels_gen1 = labels[indices_gen1]
                    labels_gen2 = labels[indices_gen2]

                    is_gen1_good = False
                    if len(labels_gen1) >= 3:
                        if np.all(labels_gen1 != -1) and len(np.unique(labels_gen1)) == 1:
                            is_gen1_good = True
                    is_gen2_good = False
                    if len(labels_gen2) >= 3:
                        if np.all(labels_gen2 != -1) and len(np.unique(labels_gen2)) == 1:
                            is_gen2_good = True

                    is_eff = 1 if (is_gen1_good and is_gen2_good) else 0
                    histogram_manager.fill_2d_histogram(f"{prefix}_match_efficiency", is_eff, dc)
                    # ------------------------------------------

                    for lbl in unique_labels:
                        mask = (labels == lbl)
                        cluster_pts = data_ntrk[mask]
                        cluster_pt = pt[mask]
                        cluster_z0 = z0[mask]
                        cluster_gen = idx_gen[mask]

                        n_total = len(cluster_pts)
                        n_pos = int(np.sum(cluster_gen == 1))
                        n_neg = int(np.sum(cluster_gen == 2))
                        n_fake = int(np.sum((cluster_gen != 1) & (cluster_gen != 2)))
                        n_true = n_pos + n_neg
                        
                        histogram_manager.fill_2d_histogram(f"{prefix}_ntrk", n_total, dc)
                        histogram_manager.fill_2d_histogram(f"{prefix}_ntrue", n_true, dc)
                        histogram_manager.fill_2d_histogram(f"{prefix}_nfake", n_fake, dc)

                        if n_total >= 3:
                            # max(dz0) = z0 spread within cluster (max(z0) - min(z0))
                            max_dz0_cluster = float(np.max(cluster_z0) - np.min(cluster_z0))
                            histogram_manager.fill_2d_histogram(f"{prefix}_dz", max_dz0_cluster, dc)
                            histogram_manager.fill_2d_histogram(f"{prefix}_max_dz", max_dz0_cluster, dc)
                            if npu == "PU200" and n_true > 0:
                                signal_mask = (cluster_gen == 1) | (cluster_gen == 2)
                                sig_z0 = cluster_z0[signal_mask]
                                max_dz0_signal = float(np.max(sig_z0) - np.min(sig_z0)) if len(sig_z0) >= 2 else 0.0
                                histogram_manager.fill_2d_histogram(f"{prefix}_max_dz_signal_only", max_dz0_signal, dc)
                            curr_pt = float(np.max(cluster_pt))
                            histogram_manager.fill_2d_histogram(f"{prefix}_pt", curr_pt, dc)

                            lorentz_vectors = []
                            for k in range(n_total):
                                vec = create_lorentz_vector(float(cluster_pt[k]), float(cluster_pts[k][0]), float(cluster_pts[k][1]))
                                lorentz_vectors.append(vec)
                            curr_mass = float(calculate_invariant_mass(lorentz_vectors))
                            histogram_manager.fill_2d_histogram(f"{prefix}_mass", curr_mass, dc)

                            # Matched cluster = cluster with 3+ tracks from one trk_gen only
                            if (n_pos >= 3 and n_neg == 0) or (n_pos == 0 and n_neg >= 3):
                                n_matched_clusters += 1
                        
                        n_clusters += 1

                    histogram_manager.fill_2d_histogram(f"{prefix}_ncluster", n_clusters, dc)
                    histogram_manager.fill_2d_histogram(f"{prefix}_match_ncluster", n_matched_clusters, dc)

                    # --- Trimming: keep track if >=2 pairwise |z0_i-z0_j| < cut; cluster with <=3 tracks after trim -> drop cluster ---
                    for max_dz_cut in max_dz_cuts:
                        pass_mask = np.zeros(len(labels), dtype=bool)
                        for lbl in unique_labels:
                            mask = (labels == lbl)
                            indices = np.where(mask)[0]
                            for i in indices:
                                n_within = np.sum(np.abs(z0[indices] - z0[i]) < max_dz_cut) - 1  # exclude self
                                pass_mask[i] = (n_within >= 2)
                        n_clusters_trim = 0
                        n_matched_trim = 0
                        for lbl in unique_labels:
                            trim_mask = (labels == lbl) & pass_mask
                            n_trim = int(np.sum(trim_mask))
                            if n_trim <= 3:
                                continue
                            n_clusters_trim += 1
                            n_pos_t = int(np.sum(trim_mask & (idx_gen == 1)))
                            n_neg_t = int(np.sum(trim_mask & (idx_gen == 2)))
                            if (n_pos_t >= 3 and n_neg_t == 0) or (n_pos_t == 0 and n_neg_t >= 3):
                                n_matched_trim += 1
                        ts = _trim_suffix(max_dz_cut)
                        histogram_manager.fill_2d_histogram(f"{prefix}_trim_maxdz{ts}_ncluster", n_clusters_trim, dc)
                        histogram_manager.fill_2d_histogram(f"{prefix}_trim_maxdz{ts}_match_ncluster", n_matched_trim, dc)
                        # Efficiency after trim: gen1/gen2 tracks passing trim must be in one cluster with >=3
                        gen1_pass = indices_gen1[pass_mask[indices_gen1]]
                        gen2_pass = indices_gen2[pass_mask[indices_gen2]]
                        labels_gen1_t = labels[gen1_pass]
                        labels_gen2_t = labels[gen2_pass]
                        is_gen1_ok = len(labels_gen1_t) >= 3 and np.all(labels_gen1_t != -1) and len(np.unique(labels_gen1_t)) == 1
                        is_gen2_ok = len(labels_gen2_t) >= 3 and np.all(labels_gen2_t != -1) and len(np.unique(labels_gen2_t)) == 1
                        is_eff_trim = 1 if (is_gen1_ok and is_gen2_ok) else 0
                        histogram_manager.fill_2d_histogram(f"{prefix}_trim_maxdz{ts}_match_efficiency", is_eff_trim, dc)


def main(input_file):
    output_file = "output.root"
    tree = ROOT.TChain("eventTree")
    tree.Add(input_file)
    
    if "PU200" in str(input_file): npu = "PU200"
    elif "HTau3pi" in str(input_file): npu = "PU200"
    else: npu = "minBias"
    
    print(f"[INFO] File: {input_file}")
    print(f"[INFO] NPU Mode detected as: {npu}")

    hm = HistogramManager(output_file)

    scan_params = {
        'dc': [0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        'dm_offset': [0.05, 0.10, 0.15, 0.20],
        'max_dz_cuts': [0.1, 0.5, 1.0, 1.5, 2.0],  # trimming: keep trk if >=2 pairwise |dz|<cut; drop cluster if n_trk<=3 after trim
    }
    
    process_tracks(tree, npu, hm, scan_params)
    hm.write_histograms()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_cluster_L1_HToTauTau_CLUE.py <file_number> <arg1>")
        print("  file_number: test | PU200 | minBias")
        sys.exit(1)

    file_number = sys.argv[1]
    arg1 = sys.argv[2]

    if file_number == "test":
        main(f"/eos/cms/store/user/chuh/l1p2/skim/HTau3pi_PU200_GTT_{arg1}.root")
    elif file_number == "PU200":
        main(f"/eos/cms/store/user/chuh/l1p2/skim/HTau3pi_PU200_GTT_{arg1}.root")
    else:
        main(f"/eos/cms/store/user/chuh/l1p2/skim/MinBias_TuneCP5_14TeV-pythia8_GTT_{arg1}.root")
