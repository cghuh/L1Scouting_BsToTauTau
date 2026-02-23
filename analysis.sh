#! /bin/bash
set -euo pipefail

echo "$1"
echo "HOSTNAME=$(hostname)"
echo "PWD=$(pwd)"
echo "DATE=$(date)"
echo "OS=$(uname -a)"

# -- CMSSW runtime (recommended)
export SCRAM_ARCH=el9_amd64_gcc12
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/work/c/chuh/L1_BsToTauTau/CMSSW_15_1_0_pre3/src
eval "$(scram runtime -sh)"
cd - >/dev/null

# -- inputs
cp /eos/user/c/chuh/l1p2/run_cluster_L1_HToTauTau_CLUE.py .
cp /eos/user/c/chuh/l1p2/DeltaR.py .
cp /eos/user/c/chuh/l1p2/officialStyle.py .

# English comment: Keep threads deterministic
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

# -- Use CMSSW python
PYBIN="$(command -v python3)"
echo "PYBIN=$PYBIN"
$PYBIN -c "import sys; import _ctypes; import ctypes; print('OK _ctypes',_ctypes.__file__); print('exe',sys.executable)"

# -- Your local pip packages (CLUEstering) if installed in ~/.local
export PYTHONUSERBASE="$HOME/.local"
export PYTHONPATH="$HOME/.local/lib/python3.9/site-packages:${PYTHONPATH:-}"
export PATH="$HOME/.local/bin:${PATH}"

$PYBIN run_cluster_L1_HToTauTau_CLUE.py "$1" "$2"

cp output.root /eos/user/c/chuh/l1p2/sample/output_"${1}"_"${2}".root
