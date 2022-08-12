# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import matplotlib.pyplot as plt
import h5py as h5

f = h5.File('data/data_10s_adq_short_seq.h5', 'r')
# f = h5.File('data/data_10s_adq_long_seq.h5', 'r')
# f = h5.File('data/data_10s_adq_laser_off.h5', 'r')

a = f.attrs
d_time = f['hists']['time']
#d_pok
#d_pbad

plt.figure()
# plt.scatter(d_time[0], d_time[1], s=4)
plt.plot(d_time[0], d_time[1])
plt.xlabel("time")
plt.ylabel("counts")

for i in range(2 * int(a['qkd_param_num_qubits'][0])):
    if ((i+1) % 2):
        plt.axvline(x=(i/2 * a['qkd_param_qubit_times'][0] + a['qkd_param_offsets'][0]), color='g', ls='--', lw=1)
        plt.axvline(x=(i/2 * a['qkd_param_qubit_times'][0] + a['qkd_param_offsets'][0] + a['qkd_param_phases'][0]), color='r', ls='--', lw=1)

    else:
        plt.axvline(x=((i-1)/2 * a['qkd_param_qubit_times'][0] + a['qkd_param_offsets'][0] + a['qkd_param_integration_windows'][0]), color='g', ls='--', lw=1)
        plt.axvline(x=((i-1)/2 * a['qkd_param_qubit_times'][0] + a['qkd_param_offsets'][0] + a['qkd_param_integration_windows'][0] + a['qkd_param_phases'][0]), color='r', ls='--', lw=1)

plt.show()