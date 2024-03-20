#import os, math, sys
#from ROOT import TFile, TH1F, gROOT, TTree, Double, TChain, TLorentzVector, TVector3
#import numpy as num

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

file = ROOT.TFile.Open('../l1p2/Tau3pi_PY8_PU'+ str(npu) + '_GTT.root')
tree = file.Get('L1TrackNtuple/eventTree')


tree.SetBranchStatus('*', 0)
tree.SetBranchStatus('gen_*', 1)
tree.SetBranchStatus('trk_*', 1)
tree.SetBranchStatus('trkExt_*', 1)

Nevt = tree.GetEntries()

print('Total Number of events = ', Nevt)
evtid = 0


cnt_acc = 0
cnt_pi = 0
cnt_acc_match = 0
    
for evt in range(Nevt):
    tree.GetEntry(evt)

    if evt%10000==0: print('{0:.2f}'.format(float(evt)/float(Nevt)*100.), '% processed')

#    print (len(tree.gen_pt))

    flag_acc = True
    flag_match = True
    npi = 0
   
    for igen in range(len(tree.gen_pt)):

        out.gen_pt[0] = tree.gen_pt[igen]
        out.gen_eta[0] = tree.gen_eta[igen]
        out.gen_phi[0] = tree.gen_phi[igen]
        out.gen_z0[0] = tree.gen_z0[igen]
        out.ntrk[0] = len(tree.trkExt_pt)

        if not (out.gen_pt[0] > 2. and abs(out.gen_eta[0]) < 2.3):
            flag_acc = False
            
        if (out.gen_pt[0] > 2. and abs(out.gen_eta[0]) < 2.3):
					npi += 1

        dRmin = 9.
        itrk_bm = -1
        
        for itrk in range(len(tree.trkExt_pt)):

            dR = returndR(tree.trkExt_eta[itrk], tree.trkExt_phi[itrk],
                          tree.gen_eta[igen], tree.gen_phi[igen])


            if dR < dRmin:
                dRmin = dR
                itrk_bm = itrk

        if itrk_bm!=-1:
            out.dr[0] = dRmin
            out.trk_pt[0] = tree.trkExt_pt[itrk_bm]
            out.trk_eta[0] = tree.trkExt_eta[itrk_bm]
            out.trk_phi[0] = tree.trkExt_phi[itrk_bm]
            out.trk_z0[0] = tree.trkExt_z0[itrk_bm]
            out.trk_d0[0] = tree.trkExt_d0[itrk_bm]
            out.trk_nstub[0] = tree.trkExt_nstub[itrk_bm]
        else:
            out.dr[0] = -9.
            out.trk_pt[0] = -9.
            out.trk_eta[0] = -9.
            out.trk_phi[0] = -9.
            out.trk_z0[0] = -9.
            out.trk_d0[0] = -9.
            out.trk_nstub[0] = -9.


        if not (dRmin > 0 and dRmin < 0.02):
            flag_match = False

        
#        evtid += 1
        out.tree.Fill()

    if flag_acc: cnt_acc += 1
    if npi == 6: cnt_pi += 1
    if flag_acc and flag_match:
        cnt_acc_match += 1

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

#        for itrk in range(len(tree.trkExt_pt)):
#
#            dRmin = 9.
#            itrk_bm = -1
#            q = 9
#            
#            for igen in range(len(tree.gen_pt)):
#                    
#                dR = returndR(tree.trkExt_eta[itrk], tree.trkExt_phi[itrk],
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
#                    hist_match_pos.Fill(tree.trkExt_eta[itrk_bm], tree.trkExt_phi[itrk_bm])
#                elif q == -15:
#                    hist_match_neg.Fill(tree.trkExt_eta[itrk_bm], tree.trkExt_phi[itrk_bm])
#                else:
#                    print('This cannot happen!', q)
#            else:
#                hist_nomatch.Fill(tree.trkExt_eta[itrk_bm], tree.trkExt_phi[itrk_bm])



#        canvas = ROOT.TCanvas('can_' + str(cnt_acc_match))
#        hist_nomatch.Draw('')
#        hist_match_pos.Draw('same')
#        hist_match_neg.Draw('same')
#        canvas.SaveAs('Plots/ed_' + str(cnt_acc_match) + '.gif')

        
    
print(Nevt, 'evt processed.', cnt_pi, 'evt has detector acc. (', float(cnt_pi/Nevt), ')' )
print(Nevt, 'evt processed.', cnt_acc, 'evt has detector acc. (', float(cnt_acc/Nevt), ')' )
print(Nevt, 'evt processed.', cnt_acc_match, 'evt has detector acc. and matching (', float(cnt_acc_match/Nevt), ')' )

out.endJob()

