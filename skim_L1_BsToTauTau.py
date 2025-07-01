import os
import time
from DeltaR import returndR, returndRs
from ROOT import TChain, TFile, TTree, std
import argparse
import ROOT

ROOT.gROOT.SetBatch(True)

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='file name')
parser.add_argument('pnevt_PU0', type=int, help='number of previous events for PU0')
#parser.add_argument('pnevt_PU200', type=int, help='number of previous events for PU200')
args = parser.parse_args()

def process_file(file_list, output_name, start_event):
    #chain = TChain("L1TrackNtuple/eventTree")
    chain = TChain("eventTree")
    for file_name in file_list:
        chain.Add(file_name)
    Nevt = chain.GetEntries()

    ofile = TFile(output_name, "RECREATE")
    oput = TTree("eventTree", "Processed tree")

    _genpt = std.vector('float')()
    _geneta = std.vector('float')()
    _genphi = std.vector('float')()
    _pt = std.vector('float')()
    _eta = std.vector('float')()
    _phi = std.vector('float')()
    _z0 = std.vector('float')()
    _d0 = std.vector('float')()
    _MVA = std.vector('float')()
    _dR = std.vector('float')()
    _dz = std.vector('float')()
    _dRs = std.vector('float')()
    _gen = std.vector('int')()

    chain.SetBranchAddress("gen_pt", _genpt)
    chain.SetBranchAddress("gen_eta", _geneta)
    chain.SetBranchAddress("gen_phi", _genphi)
    chain.SetBranchAddress("trk_pt", _pt)
    chain.SetBranchAddress("trk_eta", _eta)
    chain.SetBranchAddress("trk_phi", _phi)
    chain.SetBranchAddress("trk_z0", _z0)
    chain.SetBranchAddress("trk_d0", _d0)
    chain.SetBranchAddress("trk_MVA1", _MVA)

    oput.Branch("gen_pt", _genpt)
    oput.Branch("gen_eta", _geneta)
    oput.Branch("gen_phi", _genphi)
    oput.Branch("trk_pt", _pt)
    oput.Branch("trk_eta", _eta)
    oput.Branch("trk_phi", _phi)
    oput.Branch("trk_z0", _z0)
    oput.Branch("trk_d0", _d0)
    oput.Branch("trk_MVA", _MVA)
    oput.Branch("trk_dR", _dR)
    oput.Branch("trk_dz", _dz)
    oput.Branch("trk_dRs", _dRs)
    oput.Branch("trk_gen", _gen)

    print('Total Number of events = ', Nevt)

    evt = start_event
    for entry in range(Nevt):
        chain.GetEntry(entry)
        _dR.clear()
        _dz.clear()
        _dRs.clear()
        _gen.clear()
        evt += 1
        if (evt - start_event) % 2000 == 0:
            time_elapsed = time.time() - start_time
            print('{0:.2f}'.format(float(evt - start_event) / float(Nevt) * 100.), '% processed ', '{0:.2f}'.format(float(evt - start_event) / float(time_elapsed)), 'Hz')

        cntp = 0
        cntm = 0
        for itrk in range(len(chain.trk_pt)):
            dRmin = 999.
            gen_mpdgid = 0
            for igen in range(len(chain.gen_pt)):
                if abs(chain.gen_mpdgid[igen]) == 15 and abs(chain.gen_pdgid[igen]) == 211 and chain.gen_pt[igen] > 2. and abs(chain.gen_eta[igen]) < 2.3:
                    dR = returndR(chain.trk_eta[itrk], chain.trk_phi[itrk], chain.gen_eta[igen], chain.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                        gen_mpdgid = chain.gen_mpdgid[igen]
            if dRmin < 0.02:
                if gen_mpdgid > 0:
                    cntp += 1
                elif gen_mpdgid < 0:
                    cntm += 1

        for itrk in range(len(chain.trk_pt)):
            dRmin = 999.
            dzmin = 999.
            dRiso = 999.
            dRsmin = 999.
            gen = 0
            for jtrk in range(len(chain.trk_pt)):
                if itrk == jtrk:
                    continue
                dR = returndR(chain.trk_eta[itrk], chain.trk_phi[itrk], chain.trk_eta[jtrk], chain.trk_phi[jtrk])
                if dR < dRiso:
                    dRiso = dR
                dR = abs(chain.trk_z0[itrk]-chain.trk_z0[jtrk]) 
                if dR < dzmin:
                    dzmin = dR
                dR = returndRs(chain.trk_eta[itrk], chain.trk_phi[itrk], chain.trk_z0[itrk], chain.trk_eta[jtrk], chain.trk_phi[jtrk], chain.trk_z0[jtrk])
                if dR < dRsmin:
                    dRsmin = dR

            for igen in range(len(chain.gen_pt)):
                if abs(chain.gen_mpdgid[igen]) == 15 and abs(chain.gen_pdgid[igen]) == 211 and chain.gen_pt[igen] > 2. and abs(chain.gen_eta[igen]) < 2.3:
                    dR = returndR(chain.trk_eta[itrk], chain.trk_phi[itrk], chain.gen_eta[igen], chain.gen_phi[igen])
                    if dR < dRmin:
                        dRmin = dR
                        gen_mpdgid = chain.gen_mpdgid[igen]
            if dRmin < 0.02 and (cntp == 3 or cntm == 3):
                if gen_mpdgid > 0:
                    gen = 1
                elif gen_mpdgid < 0:
                    gen = 2

            _dR.push_back(dRiso)
            _dz.push_back(dzmin)
            _dRs.push_back(dRsmin)
            _gen.push_back(gen)
        oput.Fill()
    
    oput.Write()
    ofile.Close()

if args.fname == 'PU0':
    file_list_PU0 = ['/eos/cms/store/user/chuh/l1p2/PU0/Tau3pi_PY8_PU0_GTT_' + str(args.pnevt_PU0) + '.root']
    process_file(file_list_PU0, "output_PU0.root", -1)
elif args.fname == 'PU200':
    file_list_PU200 = ['/eos/cms/store/user/chuh/l1p2/PU200/Tau3pi_PY8_PU200_GTT_' + str(args.pnevt_PU0) + '.root']
    process_file(file_list_PU200, "output_PU200.root", -1)
elif args.fname == 'minBias':
    file_list_minBias = ['/eos/cms/store/user/chuh/l1p2/MinBias/MinBias_TuneCP5_14TeV-pythia8_GTT_' + str(args.pnevt_PU0) + '.root']
    process_file(file_list_minBias, "output_minBias.root", -1)
