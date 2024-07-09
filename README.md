Run original code to produce TTree from ntuples (Gen - TTrack)
- ```python runTauDisplay_BcJpsiTauNu_org.py```
- ```python compare.py``` (plotting)

Run code to produce TTree from ntuples (TTrack - Gen)
- ```python runTauDisplay_BcJpsiTauNu_org.py```
- ```python compare.py``` (plotting)


Latest code for study:

(Not use) Run code to draw plots directly from each ntuples (TTrack - Gen, BsToTauTau_PU0, BsToTauTau_PU200, MinBias)
- ```python run_BsToTauTau.py```

(Not use) Run code to draw plots directly from all ntuples (TTrack - Gen)
- ```python run_L1_BsToTauTau.py```

Run code to make histograms from ntuples (single file)
- ```source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.32.02/x86_64-almalinux9.4-gcc114-opt/bin/thisroot.sh```
- ```python3 run_batch_BsToTauTau.py input1 input2 input3```

Run code to make histograms from all ntuples using HTcondor
- ```condor_submit analysis.submit```
- Need to fix the output file location - Default is changgi's eos director

Draw code from output(run_batch_BsToTauTau.py) 
- ```python3 plot_L1_BsToTauTau.py```

Code description
- Select 6 gen accepted pions ($p_T$ > 20 GeV, $|\eta|$ < 2.3)
- histogram name with \*match* is match gen pion and TTrack with $\Delta$ R < 0.02
- No matching for MinBias
