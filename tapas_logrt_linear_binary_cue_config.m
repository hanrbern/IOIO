function c = tapas_logrt_linear_binary_cue_config
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Contains the configuration for the linear log-reaction time response model according to as
% developed with Louise Marshall and Sven Bestmann
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% The Gaussian noise observation model assumes that responses have a Gaussian distribution around
% the inferred mean of the relevant state. The only parameter of the model is the noise variance
% (NOT standard deviation) zeta.
%
% --------------------------------------------------------------------------------------------------
% Copyright (C) 2016 Christoph Mathys, UZH & ETHZ
%
% This file is part of the HGF toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.


% Config structure
c = struct;

% Model name
c.model = 'Linear log-reaction time for binary models';

% Sufficient statistics of Gaussian parameter priors
%

% Zeta_1
c.logitze1mu = -realmax; % 0;
c.logitze1sa = 0;

% Zeta_2
c.logze2mu = log(48);
c.logze2sa = 4^2;

% Beta_0
c.be0mu = log(500); 
c.be0sa = 4;

% Beta_1
c.be1mu = 0;
c.be1sa = 4;

% Beta_2
c.be2mu = 0; 
c.be2sa = 4;

% Beta_3
c.be3mu = 0; 
c.be3sa = 4;

% Beta_4
c.be4mu = 0; 
c.be4sa = 4;

% Zeta
c.logze3mu = log(log(20));
c.logze3sa = log(2);

% Gather prior settings in vectors
c.priormus = [
    c.logitze1mu
    c.logze2mu
    c.be0mu,...
    c.be1mu,...
    c.be2mu,...
    c.be3mu,...
    c.be4mu,...
    c.logze3mu,...
         ];

c.priorsas = [
    c.logitze1sa
    c.logze2sa
    c.be0sa,...
    c.be1sa,...
    c.be2sa,...
    c.be3sa,...
    c.be4sa,...
    c.logze3sa,...
         ];

% Model filehandle
c.obs_fun = @tapas_logrt_linear_binary;

% Handle to function that transforms observation parameters to their native space
% from the space they are estimated in
c.transp_obs_fun = @tapas_logrt_linear_binary_transp;

return;
