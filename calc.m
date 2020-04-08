function pvec = calc()
u = load('data.txt');
input = u(:,1:3);
response = u(:,4);
path_toolbox1='.\HGF';
addpath(genpath(path_toolbox1));
path_toolbox2='.\models';
addpath(genpath(path_toolbox2));

est = tapas_fitModel(response, input, 'compass_hgf_ar1_lvl2_config', 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
pvec = est.p_prc.p;

