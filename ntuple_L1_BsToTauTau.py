#import os, math, sys
#from ROOT import TFile, TH1F, gROOT, TTree, Double, TChain, TLorentzVector, TVector3
#import numpy as num

from distutils.ccompiler import gen_lib_options
from TreeProducerBcJpsiTauNu import *
from DeltaR import returndR
import copy
import random
import numpy as np
from ROOT import gROOT, gStyle

from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

npu = 0

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

#from optparse import OptionParser, OptionValueError
#usage = "usage: python runTauDisplay_BsTauTau.py"
#parser = OptionParser(usage)

#parser.add_option("-o", "--out", default='Myroot.root', type="string", help="output filename", dest="out")

#(options, args) = parser.parse_args()


ensureDir('Plots')

output='Myroot_' + str(npu) + '.root'

out = TreeProducerBcJpsiTauNu(output, 'mc')

file = ROOT.TFile.Open('Tau3pi_PY8_PU'+ str(npu) + '_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')


tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
#tree.SetBranchStatus('trk_*', 1)
tree.SetBranchStatus('trk_*', 1)

Nevt = tree.GetEntries()

print('Total Number of events = ', Nevt)
evtid = 0


cnt_acc = 0
cnt_acc_match = 0
    
count1=0
count2=0
nct=0
for evt in range(Nevt):
    tree.GetEntry(evt)

    if evt%10000==0: print('{0:.2f}'.format(float(evt)/float(Nevt)*100.), '% processed')

#    print (len(tree.gen_pt))

    flag_acc = True
    flag_match = True
    #matching = list()
    #dRmin_store = list()
   
    #for igen in range(len(tree.gen_pt)):
        # dRmin = 99999.
        # itrk_bm = -1
        # for itrk in range(len(tree.trk_pt)):

        #out.gen_pt[0] = tree.gen_pt[igen]
        #out.gen_eta[0] = tree.gen_eta[igen]
        #out.gen_phi[0] = tree.gen_phi[igen]
        #out.gen_z0[0] = tree.gen_z0[igen]
        #out.gen_ntrk[0] = len(tree.trk_pt)
        #out.gen_pdgid[0] = tree.gen_pdgid[igen]
        #out.gen_mpdgid[0] = tree.gen_mpdgid[igen]

            # #if not (out.gen_pt[0] > 2. and abs(out.gen_eta[0]) < 2.3):
            # #    flag_acc = False
            # if (out.gen_pt[0] > 2. and abs(out.gen_eta[0]) < 2.3):
            #     dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
            #     if dR < dRmin:
            #         dRmin = dR
            #         itrk_bm = itrk
            #         matching.append(itrk_bm)
            #         dRmin_store.append(dRmin)
    npi = 0
    for igen in range(len(tree.gen_pt)):
        if (tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
            npi += 1

    if (npi == 6):
        nct += 1
    else:
        continue
    
    for itrk in range(len(tree.trk_pt)):
        dRmin = 999.
        dRiso = 999.
        flag=-1
        for igen in range(len(tree.gen_pt)):
            if (tree.gen_pt[igen] > 2. and abs(tree.gen_eta[igen]) < 2.3):
                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.gen_eta[igen], tree.gen_phi[igen])
                if dR < dRmin:
                    dRmin = dR

        for jtrk in range(len(tree.trk_pt)):
            if itrk == jtrk:
                continue
            dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk], tree.trk_eta[jtrk], tree.trk_phi[jtrk])
            if dR < dRiso:
                dRiso = dR

        if dRmin < 0.02:
            flag = 1
            count1+=1
        elif dRmin == 999:
            flag=-1
        else:
            flag=0
            count2+=1
        out.trk_flag[0] = flag
        out.trk_dr[0] = dRmin
        out.trk_iso[0] = dRiso
        out.trk_pt[0] = tree.trk_pt[itrk]
        out.trk_eta[0] = tree.trk_eta[itrk]
        out.trk_phi[0] = tree.trk_phi[itrk]
        out.trk_z0[0] = tree.trk_z0[itrk]
        out.trk_d0[0] = tree.trk_d0[itrk]
        out.trk_nstub[0] = tree.trk_nstub[itrk]
        out.trk_phi_local[0] = tree.trk_phi_local[itrk]
        out.trk_chi2[0] = tree.trk_chi2[itrk]
        out.trk_chi2dof[0] = tree.trk_chi2dof[itrk]
        out.trk_chi2rphi[0] = tree.trk_chi2rphi[itrk]
        out.trk_chi2rz[0] = tree.trk_chi2rz[itrk]
        out.trk_bendchi2[0] = tree.trk_bendchi2[itrk]
        out.trk_MVA[0] = tree.trk_MVA1[itrk]
        out.trk_lhits[0] = tree.trk_lhits[itrk]
        out.trk_dhits[0] = tree.trk_dhits[itrk]
        out.trk_seed[0] = tree.trk_seed[itrk]
        out.trk_hitpattern[0] = tree.trk_hitpattern[itrk]
        out.trk_phiSector[0] = tree.trk_phiSector[itrk]
        out.trk_genuine[0] = tree.trk_genuine[itrk]
        out.trk_loose[0] = tree.trk_loose[itrk]
        out.trk_unknown[0] = tree.trk_unknown[itrk]
        out.trk_combinatoric[0] = tree.trk_combinatoric[itrk]
        out.trk_fake[0] = tree.trk_fake[itrk]
        out.trk_matchtp_pdgid[0] = tree.trk_matchtp_pdgid[itrk]
        out.trk_matchtp_pt[0] = tree.trk_matchtp_pt[itrk]
        out.trk_matchtp_eta[0] = tree.trk_matchtp_eta[itrk]
        out.trk_matchtp_phi[0] = tree.trk_matchtp_phi[itrk]
        out.trk_matchtp_z0[0] = tree.trk_matchtp_z0[itrk]
        out.trk_matchtp_dxy[0] = tree.trk_matchtp_dxy[itrk]
        out.trk_gtt_pt[0] = tree.trk_gtt_pt[itrk]
        out.trk_gtt_eta[0] = tree.trk_gtt_eta[itrk]
        out.trk_gtt_phi[0] = tree.trk_gtt_phi[itrk]
        out.trk_gtt_selected_index[0] = tree.trk_gtt_selected_index[itrk]
        out.trk_gtt_selected_emulation_index[0] = tree.trk_gtt_selected_emulation_index[itrk]
        out.tree.Fill()


        #if not (dRmin > 0 and dRmin < 0.02):
        #    flag_match = False

        
#        evtid += 1

    #if flag_acc: cnt_acc += 1
    #if flag_acc and flag_match:
    #    cnt_acc_match += 1

        # make 2D plots ...

#        hist_nomatch = ROOT.TH2F('hist_nomatch_' + str(cnt_acc_match), 'hist_nomatch_' + str(cnt_acc_match), 100,-2.5,2.5,100,-math.pi,math.pi)
#        hist_nomatch.SetMarkerStyle(21)
#        hist_nomatch.SetMarkerColor(1)
#        hist_nomatch.GetXaxis().SetTitle('#eta')
#        hist_nomatch.GetYaxis().SetTitle('#phi')
#        
#                
#        hist_match_neg = ROOT.TH2F('hist_match_neg_' + str(cnt_acc_match), 'hist_match_neg_' + str(cnt_acc_match), 100,-2.5,2.5,100,-math.pi,math.pi)
#        hist_match_neg.SetMarkerStyle(25)
#        hist_match_neg.SetMarkerColor(4)
#
#        hist_match_pos = ROOT.TH2F('hist_match_pos_' + str(cnt_acc_match), 'hist_match_pos_' + str(cnt_acc_match), 100,-2.5,2.5,100,-math.pi,math.pi)
#        hist_match_pos.SetMarkerStyle(25)
#        hist_match_pos.SetMarkerColor(2)

#        for itrk in range(len(tree.trk_pt)):
#
#            dRmin = 9.
#            itrk_bm = -1
#            q = 9
#            
#            for igen in range(len(tree.gen_pt)):
#                    
#                dR = returndR(tree.trk_eta[itrk], tree.trk_phi[itrk],
#                              tree.gen_eta[igen], tree.gen_phi[igen])
#
#
#                if dR < dRmin:
#                    dRmin = dR
#                    itrk_bm = itrk
#                    q = tree.gen_mpdgid[igen]
#                    
#            if dRmin > 0 and dRmin < 0.02:
#                if q == 15:
#                    hist_match_pos.Fill(tree.trk_eta[itrk_bm], tree.trk_phi[itrk_bm])
#                elif q == -15:
#                    hist_match_neg.Fill(tree.trk_eta[itrk_bm], tree.trk_phi[itrk_bm])
#                else:
#                    print('This cannot happen!', q)
#            else:
#                hist_nomatch.Fill(tree.trk_eta[itrk_bm], tree.trk_phi[itrk_bm])



#        canvas = ROOT.TCanvas('can_' + str(cnt_acc_match))
#        hist_nomatch.Draw('')
#        hist_match_pos.Draw('same')
#        hist_match_neg.Draw('same')
#        canvas.SaveAs('Plots/ed_' + str(cnt_acc_match) + '.gif')

        
    
print(nct)
print(count1, 'matched ', count2, 'not matched')
#print(Nevt, 'evt processed.', cnt_acc, 'evt has detector acc. (', float(cnt_acc/Nevt), ')' )
#print(Nevt, 'evt processed.', cnt_acc_match, 'evt has detector acc. and matching (', float(cnt_acc_match/Nevt), ')' )

out.endJob()

