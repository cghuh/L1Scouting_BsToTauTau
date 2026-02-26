import os
import time
from DeltaR import returndR
from ROOT import TChain, TFile, TTree, std
import argparse
import ROOT

ROOT.gROOT.SetBatch(True)

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name')
parser.add_argument('pnevt_PU0', type=int, help='number of previous events for PU0')
args = parser.parse_args()

def process_file(file_list, output_name, is_minbias):
    chain = TChain("L1TrackNtuple/eventTree")
    for file_name in file_list:
        chain.Add(file_name)
    Nevt = chain.GetEntries()

    ofile = TFile(output_name, "RECREATE")
    oput = TTree("eventTree", "Processed tree")

    # input/output vectors (we mirror input branches to output)
    _genpt  = std.vector('float')()
    _geneta = std.vector('float')()
    _genphi = std.vector('float')()
    _genz0  = std.vector('float')()  # new: gen_z0
    _pt  = std.vector('float')()
    _eta = std.vector('float')()
    _phi = std.vector('float')()
    _z0  = std.vector('float')()
    _d0  = std.vector('float')()
    _MVA = std.vector('float')()
    _gen = std.vector('int')()       # labels: 0/1/2

    # Set addresses (we still access other arrays via chain.<name>)
    chain.SetBranchAddress("gen_pt",  _genpt)
    chain.SetBranchAddress("gen_eta", _geneta)
    chain.SetBranchAddress("gen_phi", _genphi)
    chain.SetBranchAddress("gen_z0",  _genz0)   # new: read gen_z0
    chain.SetBranchAddress("trk_pt",  _pt)
    chain.SetBranchAddress("trk_eta", _eta)
    chain.SetBranchAddress("trk_phi", _phi)
    chain.SetBranchAddress("trk_z0",  _z0)
    chain.SetBranchAddress("trk_d0",  _d0)
    chain.SetBranchAddress("trk_MVA1", _MVA)

    # Output branches (write-through of input vectors + labels)
    oput.Branch("gen_pt",  _genpt)
    oput.Branch("gen_eta", _geneta)
    oput.Branch("gen_phi", _genphi)
    oput.Branch("gen_z0",  _genz0)   # new: save gen_z0
    oput.Branch("trk_pt",  _pt)
    oput.Branch("trk_eta", _eta)
    oput.Branch("trk_phi", _phi)
    oput.Branch("trk_z0",  _z0)
    oput.Branch("trk_d0",  _d0)
    oput.Branch("trk_MVA", _MVA)
    oput.Branch("trk_gen", _gen)

    print('Total Number of events = ', Nevt)
    t0 = time.time()
    kept = 0

    ALLOWED_MOTHERS = {15, -15, 20213, -20213, 213, -213, 113}

    for entry in range(Nevt):
        chain.GetEntry(entry)
        _gen.clear()
        chain.GetEntry(entry)
        if entry % 2000 == 0 and entry > 0:
            dt = max(1e-6, time.time() - t0)
            print(f"{100.0*entry/Nevt:.2f}% processed  {(entry/dt):.2f} Hz  kept={kept}")
        
        # Initialize labels for all tracks with 0
        for _ in range(len(chain.trk_pt)):
            _gen.push_back(0)

        test = 0
        # Collect candidate gen-pions per tau sign with kinematic cuts
        gen_plus_idxs = []   # mother tau pdgid > 0
        gen_minus_idxs = []  # mother tau pdgid < 0
        for igen in range(len(chain.gen_pt)):
            # require charged pion from tau with basic kinematic cuts
            #if abs(chain.gen_pdgid[igen]) != 211:
            if abs(int(round(float(chain.gen_pdgid[igen])))) != 211:
                continue
            test+=1
            #if abs(chain.gen_mother_pdgid[igen]) != 15:
            if abs(chain.gen_mother_pdgid[igen]) not in ALLOWED_MOTHERS:
                continue
            if chain.gen_pt[igen] <= 2.0 or abs(chain.gen_eta[igen]) >= 2.5:
                continue
            if chain.gen_mother_pdgid[igen] > 0:
                gen_plus_idxs.append(igen)
            elif chain.gen_mother_pdgid[igen] < 0:
                gen_minus_idxs.append(igen)
        print(f"check gen = {test}")

        # Helper: count how many gen pions (in the given set) have at least one track within dR<0.02
        def count_matched(gen_idxs):
            cnt = 0
            for igen in gen_idxs:
                dRmin = 999.0
                for itrk in range(len(chain.trk_pt)):
                    dR = returndR(chain.trk_eta[itrk], chain.trk_phi[itrk],
                                  chain.gen_eta[igen], chain.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                if dRmin < 0.02:
                    cnt += 1
            return cnt

        cntp = count_matched(gen_plus_idxs)
        cntm = count_matched(gen_minus_idxs)

        # Require BOTH sides to have exactly 3 matched gen-pions
        if not (cntp == 3 and cntm == 3):
            if is_minbias: ifoput.Fill()
            continue

        # Build candidate (trk, gen) pairs for BOTH signs with dR<0.02
        # Tie-breaker: prefer smaller |trk_z0 - gen_z0|
        selected_gen_idxs = gen_plus_idxs + gen_minus_idxs
        pairs = []  # (dR, abs_dz0, itrk, igen)
        for itrk in range(len(chain.trk_pt)):
            trk_z0 = chain.trk_z0[itrk]
            for igen in selected_gen_idxs:
                dR = returndR(chain.trk_eta[itrk], chain.trk_phi[itrk],
                              chain.gen_eta[igen], chain.gen_phi[igen])
                if dR < 0.02:
                    dz0 = abs(trk_z0 - chain.gen_z0[igen])
                    pairs.append((dR, dz0, itrk, igen))

        # Sort by (smallest dR, then smallest |Δz0|)
        pairs.sort(key=lambda x: (x[0], x[1]))

        used_trk = set()
        used_gen = set()
        matched = []  # (itrk, igen)

        # Aim for up to 6 matches (3 from tau+ and 3 from tau-)
        for dR, dz0, itrk, igen in pairs:
            if itrk in used_trk or igen in used_gen:
                continue
            used_trk.add(itrk)
            used_gen.add(igen)
            matched.append((itrk, igen))
            if len(matched) == 6:
                break

        # Assign labels to matched tracks: 1 for tau+, 2 for tau-
        for itrk, igen in matched:
            if chain.gen_mother_pdgid[igen] > 0:
                _gen[itrk] = 1
            elif chain.gen_mother_pdgid[igen] < 0:
                _gen[itrk] = 2

        oput.Fill(); kept += 1

    oput.Write()
    ofile.Close()
    print(f"Done. kept events = {kept}")

if args.fname == 'PU0':
    file_list_PU0 = [f'/eos/cms/store/user/chuh/l1p2/PU0/Tau3pi_PY8_PU0_GTT_{args.pnevt_PU0}.root']
    process_file(file_list_PU0, "output_PU0.root", is_minbias=False)
elif args.fname == 'PU200':
    #file_list_PU200 = [f'/eos/cms/store/group/phys_bphys/ytakahas/chuh/Htautau/step3/CRAB_UserFiles/crab_BsTau3pi_step3_Ntuple/250927_105123/0000/step3_{args.pnevt_PU0}.root']
    file_list_PU200 = [f'/eos/cms/store/group/phys_bphys/ytakahas/chuh/Htautau/step3/CRAB_UserFiles/crab_BsTau3pi_step3_Ntuple/250930_102147/0000/step3_{args.pnevt_PU0}.root']
    #file_list_PU200 = [f'/eos/cms/store/group/phys_bphys/ytakahas/chuh/Htautau/step3/CRAB_UserFiles/crab_HTau3pi_step3_Ntuple/250921_212012/0000/step3_{args.pnevt_PU0}.root']
    process_file(file_list_PU200, "output_PU200.root", is_minbias=False)
elif args.fname == 'minBias':
    file_list_minBias = [f'/eos/cms/store/group/phys_bphys/ytakahas/chuh/minBias/MinBias_TuneCP5_14TeV-pythia8/crab_bkg/250824_133513/0000/out_{args.pnevt_PU0}.root']
    process_file(file_list_minBias, "output_minBias.root", is_minbias=False)
