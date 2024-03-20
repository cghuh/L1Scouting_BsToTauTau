#94244 evt processed. 32 evt has detector acc. ( 0.00033954416196256527 )
#94244 evt processed. 17 evt has detector acc. and matching ( 0.00018038283604261278 )
# from gen. study
acc_eff = 0.00018038283604261278

sigma=5.0660E8 # pb (14 TeV)
lum=100*1000. # fb * 1000 -> pb
f_bs = 0.1
br=7.7E-7
br_tau3p = 0.15


Nprod = lum*sigma*f_bs*2*br*br_tau3p*br_tau3p*acc_eff

print(Nprod)
