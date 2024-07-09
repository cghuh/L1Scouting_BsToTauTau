#! /bin/bash
echo $1
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.32.02/x86_64-almalinux9.4-gcc114-opt/bin/thisroot.sh 
cp /eos/user/c/chuh/l1p2/skim_L1_BsToTauTau.py .
cp /eos/user/c/chuh/l1p2/DeltaR.py .
cp /eos/user/c/chuh/l1p2/officialStyle.py .
python3 skim_L1_BsToTauTau.py $1 $2 $3
if [ "$1" == "minBias" ]; then
	cp *minBias.root /eos/cms/store/user/chuh/l1p2/skim/MinBias_TuneCP5_14TeV-pythia8_GTT_${2}.root
else
	cp *PU0.root /eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU0_GTT_${1}.root
	cp *PU200.root /eos/cms/store/user/chuh/l1p2/skim/Tau3pi_PY8_PU200_GTT_${1}.root
fi
