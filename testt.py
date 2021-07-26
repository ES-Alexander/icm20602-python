
import argparse
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF
import llog as ll
import pandas as pd
import matplotlib.pyplot as plt
import os

import math
dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path+'/icm20602.meta'

meta = 'test2.meta'
output = 'test2.csv'
log = ll.LLogWriter(meta, output)

log.log(ll.LLOG_CALIBRATION, f'                                            ')

# log.log(ll.LLOG_INFO, f'infox shax cmdx')

for i in range(20):
    log.log(ll.LLOG_ERROR, f'error{i}')

for i in range(100):
    log.log(ll.LLOG_DATA, f'{math.sin(i/5.0)} {i*i} {2*math.sin(i/4.0)} {math.sin(i/4.0 + 2)} {math.sin(i/4.0 + 4)}')

for i in range(5):
    log.log(ll.LLOG_ROM, f'{1.0/(i+1)} {i*100}')

log.close()

log = ll.LLogReader(output, meta)

dp = log.data['p']
dt = log.data['t']
dg = log.data[['gx', 'gy', 'gz']]


header = 'testt.py report header'
footer = 'testt.py report footer'
f, spec = log.figure(height_ratios=[1,2,4,2], columns=3, suptitle='some data plots', header=header, footer=footer)

plt.subplot(spec[0,:])
log.rom.table()

plt.subplot(spec[1,0])
dp.pplot(d2=dt, title='pressure + temperature')

plt.subplot(spec[1,1:])
dt.pplot(title='temperature data')

plt.subplot(spec[2,:])
dg.pplot(title='gyro data')

plt.subplot(spec[3,0])
dg.gx.pplot(title='gyro x')

plt.subplot(spec[3,1])
dg.gy.pplot(title='gyro y')

plt.subplot(spec[3,2])
dg.gz.pplot(title='gyro z')

with PdfPages('test.pdf') as pdf:
    pdf.savefig()
    f, spec = log.figure(height_ratios=[2,6], columns=1, suptitle='gyro data head', header=header, footer=footer)
    plt.subplot(spec[0])
    dgs = dg.stats()
    dg.stats().table(rl=True)

    plt.subplot(spec[1])
    dg.insert(0, 'time', log.data.time)
    dg.head(20).table()

    pdf.savefig()
    f, spec = log.figure(height_ratios=[1], columns=1, suptitle='log errors', header=header, footer=footer)
    plt.subplot(spec[0])
    log.error.table()
    # plt.plot([0, 1], [0.03, 0.03], color='blue', clip_on=False, 
    # transform=f.transFigure)
    pdf.savefig()


plt.show()
