# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import matplotlib.pyplot as plt
import h5py as h5

f = h5.File('data/data_10s_adq_short_seq.h5', 'r')
# f = h5.File('data/data_10s_adq_long_seq.h5', 'r')
# f = h5.File('data/data_10s_adq_laser_off.h5', 'r')

d_time = f['hists']['time']
#d_pok
#d_pbad

plt.figure()
# plt.scatter(d_time[0], d_time[1], s=4)
plt.plot(d_time[0], d_time[1])
plt.xlabel("time")
plt.ylabel("counts")
plt.show()