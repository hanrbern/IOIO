function [RV] = IOIO_results (filename)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function runs the results from a user playing the IOIO game
%
% The inputs used are extracted from playing the IOIO game on python. 
% The inputs are extracted using extract_subjects.m.
%
% The prc_models tested depend on the parameter(s) selected. Each parameter
% has corresponding prc_models that rely on the parameter. 
%
% This function shows the correlation between simulated
% responses and estimated responses using a Perceptual Model and parameter 
% of your choice. 
%
% This function also shows the recovered values of each of the parameters
% selected based on each model tested.
% 
% This function uses the unit square sigmoid and quasinewton optimization
% functions from the tapas toolbox.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INPUT ARGUMENTS:
%     
%     parameter           Perceptual models tested will depend on the parameter(s) chosen
%                         
%                           -'om2' Omega will be tested for models with fixed kappa values
%                           
%                           -'kap' Kappa will be tested for models without fixed kappa values
%
%                           -'m_2' m2 will be tested for all models
%
%                           -'m_3' m3 will be tested for all models
%
% OUTPUT ARGUMENTS:
%
%       T                   Table showing how well each of the parameters
%                           were recovered for each of the models used.
%                           Table appears on the Summary tab of
%                           integrated_game.mlapp.
%                                               
%        
%       RV                  Table showing the recovered values of each of
%                           the parameters for each of the models used.
%                           Table appears on the Recovered Values tab of
%                           integrated_game.mlapp.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set path to the compass toolboxes and models
path_toolbox1='Users\hannah\Documents\GitHub\compass\toolboxes\HGF'; %% Modify to the path of the HGF Toolbox
addpath(genpath(path_toolbox1));
path_toolbox2='Users\hannah\Documents\GitHub\compass\models'; %% Modify to the path of the models
addpath(genpath(path_toolbox2));

[subjects, correct_colour, prob_colour, prob_advice] = extract_subjects()
u = [correct_colour, prob_colour, prob_advice]

% Cells containing functions with fixed kappa or unfixed kappa
m_kafxd = {'compass_hgf_kafxd', 'compass_hgf_ar1_lvl2_kafxd', 'compass_hgf_ar1_lvl3_kafxd', 'compass_hgf_attractor_kafxd'};
m = {'compass_hgf', 'compass_hgf_ar1_lvl2', 'compass_hgf_ar1_lvl3', 'compass_hgf_attractor'};
m_all = {'compass_hgf_kafxd', 'compass_hgf_ar1_lvl2_kafxd', 'compass_hgf_ar1_lvl3_kafxd', 'compass_hgf_attractor_kafxd', 'compass_hgf', 'compass_hgf_ar1_lvl2', 'compass_hgf_ar1_lvl3', 'compass_hgf_attractor'};
m_lvl2 = {'compass_hgf_ar1_lvl2_kafxd', 'compass_hgf_ar1_lvl2'};
m_lvl3 = {'compass_hgf_ar1_lvl3_kafxd', 'compass_hgf_ar1_lvl3'};

% parameter_diff to be used in table T to show how well each parameter was recovered
% parameter _value to be used in table RV to show the values recovered for each parameter
models = {'compass_hgf_kafxd', 'compass_hgf_ar1_lvl2_kafxd', 'compass_hgf_ar1_lvl3_kafxd', 'compass_hgf_attractor_kafxd', 'compass_hgf', 'compass_hgf_ar1_lvl2', 'compass_hgf_ar1_lvl3', 'compass_hgf_attractor'};
ka_diff = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
om2_diff = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
m2_diff = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
m3_diff = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
ka_value = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
om2_value = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
m2_value = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};
m3_value = {'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A';'N/A'};

parameters = {'kap'; 'om2'; 'm_2'; 'm_3'}

for k = 1:length(parameters)
    parameter = parameters{k}
    
    switch parameter 
        case 'kap'
            prc_model = m;
            vec = linspace(0, 2.5, 30);
            for j=1:length(prc_model)
                prc_config = strcat(prc_model, '_config');
            end
            for j = 1:length(prc_model)
                % Empty arrays to collect simulations and estimations data and calculated
                % differences
                simulations = [];
                estimations = [];
                differences = [];
                % Function will loop through every value of the parameter tested
                for i = 1:length(vec)
                    % prc_pvec changes according to the model based on if the model has
                    % drift or not. prc_pvec is a row vector of perceptual model
                    % parameter values. 
                    % sim2 is a simulation based off of the first estimation 
                    % est2 is an estimation based off of sim2 
                    % sum_diff finds the differences between the values found in est2
                    % and est (using sim2).
                    % Both tables T and RV are then updated for each model
                    if (isequal('compass_hgf', prc_model{j})||isequal('compass_hgf_attractor', prc_model{j}))
                        prc_pvec = [NaN 0 1 NaN 0 1 NaN 0 0 1 vec(i) NaN -3 -6];
                    else
                        prc_pvec = [NaN 0 1 NaN 0 1 NaN 0 0 NaN 0 1 1 vec(i) NaN -3 -6];
                    end
                    rng('default');
                    sim = tapas_simModel(u, prc_model{j}, prc_pvec, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est = tapas_fitModel(sim.y, sim.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    rng('default');
                    sim2 = tapas_simModel(u, prc_model{j}, est.p_prc.p, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est2 = tapas_fitModel(sim2.y, sim2.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    simulations = [simulations, sim2.p_prc.ka(2)];
                    estimations = [estimations, est2.p_prc.ka(2)];
                    differences = estimations - simulations;
                    sum_diff = sum(abs(differences));
                    ka_diff{j+4} = sum_diff;
                    ka_value{j+4} = est2.p_prc.ka(2);
                    
                end
            end
        case 'om2'
            prc_model = m_kafxd;
            vec = linspace(-1 , -7, 30);
            for j=1:length(prc_model)
                prc_config = strcat(prc_model, '_config'); 
            end
            for j = 1:length(prc_model)
                % Empty arrays to collect simulations and estimations data and calculated
                % differences
                simulations = [];
                estimations = [];
                differences = [];
                % Function will loop through every value of the parameter tested
                for i = 1:length(vec)
                    % prc_pvec changes according to the model based on if the model has
                    % drift or not. prc_pvec is a row vector of perceptual model
                    % parameter values. 
                    % sim2 is a simulation based off of the first estimation 
                    % est2 is an estimation based off of sim2 
                    % sum_diff finds the differences between the values found in est2
                    % and est (using sim2).
                    % Both tables T and RV are then updated for each model
                    if (isequal('compass_hgf_kafxd', prc_model{j}) || isequal('compass_hgf_attractor_kafxd', prc_model{j}))
                        prc_pvec = [NaN 0 1 NaN 0 1 NaN 0 0 1 1 NaN vec(i) -6];
                    else
                        prc_pvec = [NaN 0 1 NaN 0 1 NaN 0 0 NaN 0 1 1 1 NaN vec(i) -6];
                    end
                    rng('default');
                    sim = tapas_simModel(u, prc_model{j}, prc_pvec, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est = tapas_fitModel(sim.y, sim.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    rng('default');
                    sim2 = tapas_simModel(u, prc_model{j}, est.p_prc.p, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est2 = tapas_fitModel(sim2.y, sim2.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    simulations = [simulations, sim2.p_prc.om(2)];
                    estimations = [estimations, est2.p_prc.om(2)];
                    differences = estimations - simulations;
                    sum_diff = sum(abs(differences));
                    om2_diff{j} = sum_diff;
                    om2_value{j} = est2.p_prc.om(2);
                    
                end
            end
        
        case 'm_2'
            prc_model = m_lvl2;
            vec = linspace(-5, 5, 30);
            for j = 1:length(prc_model)
                prc_config = strcat(prc_model, '_config');
            end
            for j = 1:length(prc_model)
                % Empty arrays to collect simulations and estimations data and calculated
                % differences
                simulations = [];
                estimations = [];
                differences = [];
                % Function will loop through every value of the parameter tested
                for i = 1:length(vec)
                    % prc_pvec changes according to the model based on if the model has
                    % drift or not. prc_pvec is a row vector of perceptual model
                    % parameter values. 
                    % sim2 is a simulation based off of the first estimation 
                    % est2 is an estimation based off of sim2 
                    % sum_diff finds the differences between the values found in est2
                    % and est (using sim2).
                    % Both tables T and RV are then updated for each model
                    prc_pvec = [NaN 0 1 NaN 0 1 NaN 0 0 NaN vec(i) 1 1 1 NaN -3 -6];
                    rng('default');
                    sim = tapas_simModel(u, prc_model{j}, prc_pvec, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est = tapas_fitModel(sim.y, sim.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    rng('default');
                    sim2 = tapas_simModel(u, prc_model{j}, est.p_prc.p, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est2 = tapas_fitModel(sim2.y, sim2.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    simulations = [simulations, sim2.p_prc.m(2)];
                    estimations = [estimations, est2.p_prc.m(2)]; 
                    differences = estimations - simulations;
                    sum_diff = sum(abs(differences));
                    if j == 1
                        m2_diff{2} = sum_diff;
                        m2_value{2} = est2.p_prc.m(2);
                        
                    elseif j == 2
                        m2_diff{6} = sum_diff;
                        m2_value{6} = est2.p_prc.m(2);
                        
                    end
                end
            end
        case 'm_3'
            prc_model = m_lvl3;
            vec = linspace(-5, 5, 30);
            for j = 1:length(prc_model)
                prc_config = strcat(prc_model, '_config');
            end
            for j = 1:length(prc_model)
                % Empty arrays to collect simulations and estimations data and calculated
                % differences
                simulations = [];
                estimations = [];
                differences = [];
                % Function will loop through every value of the parameter tested
                for i = 1:length(vec)
                    % prc_pvec changes according to the model based on if the model has
                    % drift or not. prc_pvec is a row vector of perceptual model
                    % parameter values. 
                    % sim2 is a simulation based off of the first estimation 
                    % est2 is an estimation based off of sim2 
                    % sum_diff finds the differences between the values found in est2
                    % and est (using sim2).
                    % Both tables T and RV are then updated for each model
                    prc_pvec = [NaN 0 1 NaN 0 1 NaN 0 0 NaN 0 vec(i) 1 1 NaN -3 -6];
                    rng('default');
                    sim = tapas_simModel(u, prc_model{j}, prc_pvec, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est = tapas_fitModel(sim.y, sim.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    rng('default');
                    sim2 = tapas_simModel(u, prc_model{j}, est.p_prc.p, 'dmpad_unitsq_sgm', [0.5, 5]);
                    est2 = tapas_fitModel(sim2.y, sim2.u, prc_config{j}, 'dmpad_unitsq_sgm_config', 'tapas_quasinewton_optim_config');
                    simulations = [simulations, sim2.p_prc.m(3)];
                    estimations = [estimations, est2.p_prc.m(3)]; 
                    differences = estimations - simulations;
                    sum_diff = sum(abs(differences));
                    if j == 1
                        m3_diff{3} = sum_diff;
                        m3_value{3} = est2.p_prc.m(3);
                        
                    elseif j == 2
                        m3_diff{7} = sum_diff;
                        m3_value{7} = est2.p_prc.m(3);
                        
                    end
                end
            end
    end            
end
    RV = table(ka_value, om2_value, m2_value, m3_value, 'RowNames', models);
    cd /Users/hannah/Documents/GitHub/kivy_app/IOIO/data
    filename = 'results.xlsx';
    writetable(RV,filename)
end
