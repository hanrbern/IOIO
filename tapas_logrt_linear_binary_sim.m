function [y_ch,y_rt] = tapas_logrt_linear_binary_sim(r, infStates, p)
% Simulates logRTs with Gaussian noise
% as well as choices under the IOIO task model
% --------------------------------------------------------------------------------------------------
% Copyright (C) 2016 Christoph Mathys, TNU, UZH & ETHZ
% % modified by Andreea Diaconescu, 2018 TNU, UZH & ETHZ
% This file is part of the HGF toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.

% Get parameters
ze1 = p(1);
ze2 = p(2);
be0  = p(3);
be1  = p(4);
be2  = p(5);
be3  = p(6);
be4  = p(7);
ze3   = p(8);

% Number of trials
n = size(infStates,1);

% Inputs
u = r.u(:,1);
c = r.u(:,2);

% Extract trajectories of interest from infStates
mu1hat = infStates(:,1,1);
sa1hat = infStates(:,1,2);
mu3hat = infStates(:,3,1);
mu2    = infStates(:,2,3);
sa2    = infStates(:,2,4);
mu3    = infStates(:,3,3);

% Belief vector
% ~~~~~~~~
b = ze1.*mu1hat + (1-ze1).*c;

% additional decision noise injected?
if length(p)<9
    eta = 0;
else
    eta = p(9);
end

% Decision Temperature
ze = exp(-mu3hat) + exp(log(ze2) - eta);

% Apply the unit-square sigmoid to the inferred states
prob_choice = b.^(beta)./(b.^(beta)+...
    (1-b).^(beta));

% Surprise
% ~~~~~~~~
poo = mu1hat.^u.*(1-mu1hat).^(1-u); % probability of observed outcome
surp = -log2(poo);

% Bernoulli variance (aka irreducible uncertainty, risk) 
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bernv = sa1hat;

% Inferential variance (aka informational or estimation uncertainty, ambiguity)
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
inferv = tapas_sgm(mu2, 1).*(1 -tapas_sgm(mu2, 1)).*sa2; % transform down to 1st level

% Phasic volatility (aka environmental or unexpected uncertainty)
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pv = tapas_sgm(mu2, 1).*(1-tapas_sgm(mu2, 1)).*exp(mu3); % transform down to 1st level

% Calculate predicted log-reaction time
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logrt = be0 +be1.*surp +be2.*bernv +be3.*inferv +be4.*pv;

% Initialize random number generator
rng('shuffle');

% Simulate
y_ch = binornd(1, prob_choice);

% Simulate
y_rt = logrt+sqrt(ze3)*randn(n, 1);

end
