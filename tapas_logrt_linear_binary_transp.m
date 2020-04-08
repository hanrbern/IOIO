function [pvec, pstruct] = tapas_logrt_linear_binary_transp(r, ptrans)
% --------------------------------------------------------------------------------------------------
% Copyright (C) 2016 Christoph Mathys, UZH & ETHZ
%
% This file is part of the HGF toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.

pvec    = NaN(1,length(ptrans));
pstruct = struct;

pvec(1)     = tapas_sgm(ptrans(1),1);       % ze1
pstruct.ze1 = pvec(1);
pvec(2)     = exp(ptrans(2));         % ze2
pstruct.ze2 = pvec(2);

pvec(3)     = ptrans(3);         % be0
pstruct.be0 = pvec(3);
pvec(4)     = ptrans(4);         % be1
pstruct.be1 = pvec(4);
pvec(5)     = ptrans(5);         % be2
pstruct.be2 = pvec(5);
pvec(6)     = ptrans(6);         % be3
pstruct.be3 = pvec(6);
pvec(7)     = ptrans(7);         % be4
pstruct.be4 = pvec(7);
pvec(8)     = exp(ptrans(8));    % ze
pstruct.ze  = pvec(8);

return;
