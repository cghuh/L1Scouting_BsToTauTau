#! /bin/bash
echo $1
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.32.02/x86_64-almalinux9.4-gcc114-opt/bin/thisroot.sh 
cp /eos/user/c/chuh/l1p2/run_batch_L1_BsToTauTau.py .
cp /eos/user/c/chuh/l1p2/DeltaR.py .
cp /eos/user/c/chuh/l1p2/officialStyle.py .
python3 run_batch_L1_BsToTauTau.py $1 $2 $3
if ls PlotsminBias ; then
	cp output.root /eos/user/c/chuh/l1p2/sample/output_${1}_${2}.root
	tar -czf minBias_${1}_${2}.tar.gz PlotsminBias/*png
	cp minBias_${1}_${2}.tar.gz /eos/user/c/chuh/l1p2/minBias/
else
	tar -czf PU0_${1}.tar.gz Plots0/*png
	tar -czf PU200_${1}.tar.gz Plots200/*png
	cp PU0_${1}.tar.gz /eos/user/c/chuh/l1p2/PU0/
	cp PU200_${1}.tar.gz /eos/user/c/chuh/l1p2/PU200/
	cp output.root /eos/user/c/chuh/l1p2/sample/output_${1}.root
fi
