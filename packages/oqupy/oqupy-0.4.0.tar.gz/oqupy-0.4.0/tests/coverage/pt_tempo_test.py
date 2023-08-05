# Copyright 2022 The TEMPO Collaboration
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Tests for the time_evovling_mpo.pt_tempo module.
"""

import pytest
import numpy as np

import oqupy as tempo

def test_pt_tempo_parameters():
    tempo_param = tempo.TempoParameters(
        0.1, None, 1.0e-5, None, None, 2.0e-5, "rough", "bla")
    str(tempo_param)
    assert tempo_param.dt == 0.1
    assert tempo_param.dkmax == None
    assert tempo_param.epsrel == 1.0e-5
    assert tempo_param.subdiv_limit == None
    assert tempo_param.liouvillian_epsrel == 2.0e-5
    tempo_param.dt = 0.05
    tempo_param.dkmax = 42
    tempo_param.epsrel = 1.0e-6
    tempo_param.subdiv_limit = 256
    tempo_param.liouvillian_epsrel = 2.0e-6
    assert tempo_param.dt == 0.05
    assert tempo_param.dkmax == 42
    assert tempo_param.epsrel == 1.0e-6
    assert tempo_param.liouvillian_epsrel == 2.0e-6
    del tempo_param.dkmax
    assert tempo_param.dkmax == None
    del tempo_param.subdiv_limit
    assert tempo_param.subdiv_limit == None

def test_pt_tempo_parameters_bad_input():
    with pytest.raises(AssertionError):
        tempo.TempoParameters("x", 42, 1.0e-5, None, None, 2.0e-6, "rough", "bla")
    with pytest.raises(AssertionError):
        tempo.TempoParameters(0.1, "x", 1.0e-5, None, None, 2.0e-6, "rough", "bla")
    with pytest.raises(AssertionError):
        tempo.TempoParameters(0.1, 42, "x", None, None, 2.0e-6, "rough", "bla")
    with pytest.raises(AssertionError):
        tempo.TempoParameters(0.1, 42, 1.0e-05, "x", None, 2.0e-6, "rough", "bla")
    with pytest.raises(AssertionError):
        tempo.TempoParameters(0.1, 42, 1.0e-05, None, "x", 2.0e-6, "rough", "bla")
    with pytest.raises(AssertionError):
        tempo.TempoParameters(0.1, 42, 1.0e-05, None, None, "x", "rough", "bla")

def test_pt_tempo():
    start_time = -0.3
    end_time = 0.84

    system = tempo.System(0.5 * tempo.operators.sigma("x"))
    correlation_function = lambda t: (np.cos(6.0*t)+1j*np.sin(6.0*t)) \
                                        * np.exp(-12.0*t)
    correlations = tempo.CustomCorrelations(correlation_function)
    bath = tempo.Bath(0.5 * tempo.operators.sigma("z"), correlations)
    initial_state = tempo.operators.spin_dm("z+")

    tempo_param_A = tempo.TempoParameters(0.1, 5, 1.0e-5, name="rough-A")
    pt_tempo_sys_A = tempo.PtTempo(bath=bath,
                                   parameters=tempo_param_A,
                                   start_time=start_time,
                                   end_time=end_time)
    assert pt_tempo_sys_A.dimension == 2
    pt_tempo_sys_A.compute()
    pt_A = pt_tempo_sys_A.get_process_tensor()
    assert len(pt_A) == 11

    tempo_param_B = tempo.TempoParameters(0.1, None, 1.0e-5, name="rough-B")
    pt_tempo_sys_B = tempo.PtTempo(bath=bath,
                                   parameters=tempo_param_B,
                                   start_time=start_time,
                                   end_time=end_time)
    pt_B = pt_tempo_sys_B.get_process_tensor()

def test_tempo_bad_input():
    start_time = -0.3
    end_time = 0.84

    correlation_function = lambda t: (np.cos(6.0*t)+1j*np.sin(6.0*t)) \
                                        * np.exp(-12.0*t)
    correlations = tempo.CustomCorrelations(correlation_function)
    bath = tempo.Bath(0.5 * tempo.operators.sigma("z"), correlations)

    tempo_param = tempo.TempoParameters(0.1, 5, 1.0e-5, name="rough-A")

    tempo.PtTempo(bath=bath,
                  parameters=tempo_param,
                  start_time=start_time,
                  end_time=end_time)

    with pytest.raises(AssertionError):
        tempo.PtTempo(bath=bath,
                      parameters=tempo_param,
                      start_time="bla",
                      end_time=end_time)
    with pytest.raises(AssertionError):
        tempo.PtTempo(bath=bath,
                      parameters=tempo_param,
                      start_time=start_time,
                      end_time="bla")
    with pytest.raises(AssertionError):
        tempo.PtTempo(bath=bath,
                      parameters=tempo_param,
                      start_time=0.0,
                      end_time=0.0001)

def test_tempo_compute():
    start_time = -0.3
    end_time = 0.84

    correlation_function = lambda t: (np.cos(6.0*t)+1j*np.sin(6.0*t)) \
                                        * np.exp(-12.0*t)
    correlations = tempo.CustomCorrelations(correlation_function)
    bath = tempo.Bath(0.5 * tempo.operators.sigma("z"), correlations)
    initial_state = tempo.operators.spin_dm("z+")

    with pytest.warns(UserWarning):
        pt_A = tempo.pt_tempo_compute(bath=bath,
                                      start_time=start_time,
                                      end_time=end_time)

