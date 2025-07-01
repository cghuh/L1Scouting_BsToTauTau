rm -f sample/output_minBias.root sample/output_PU0.root sample/output_PU200.root
hadd -f sample/output_PU0.root sample/*PU0*root
hadd -f sample/output_PU200.root sample/*PU200*root
hadd -f sample/output_minBias.root sample/*minBias*root
hadd -f output.root sample/output_PU0.root sample/output_PU200.root sample/output_minBias.root
