#! /bin/bash
echo $1
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.32.02/x86_64-almalinux9.4-gcc114-opt/bin/thisroot.sh 
cp /eos/user/c/chuh/l1p2/run_cluster_L1_BsToTauTau.py .
cp /eos/user/c/chuh/l1p2/DeltaR.py .
cp /eos/user/c/chuh/l1p2/officialStyle.py .
python3 run_cluster_L1_BsToTauTau.py $1 $2
cp output.root /eos/user/c/chuh/l1p2/sample/output_${1}_${2}.root
