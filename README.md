Run original code to produce TTree from ntuples (Gen - TTrack)
- ```python runTauDisplay_BcJpsiTauNu_org.py```
- ```python compare.py``` (plotting)

Run code to produce TTree from ntuples (TTrack - Gen)
- ```python runTauDisplay_BcJpsiTauNu_org.py```
- ```python compare.py``` (plotting)


Latest code for study:

Run code to draw plots directly from each ntuples (TTrack - Gen, BsToTauTau_PU0, BsToTauTau_PU200, MinBias)
- ```python run_BsToTauTau.py```

Run code to draw plots directly from all ntuples (TTrack - Gen)
- ```python run_L1_BsToTauTau.py```

Code description
- Select 6 gen accepted pions ($p_T$ > 20 GeV, $|\eta|$ < 2.3)
- histogram name with \*match* is match gen pion and TTrack with $\Delta$ R < 0.02
- No matching for MinBias
- run only 10,000 events for MinBias sample due to running time(~1.5 Hz at lxplus eos)
