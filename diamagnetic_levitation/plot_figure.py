import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import h5py
from mpi4py import MPI

rank = MPI.COMM_WORLD.rank
size = MPI.COMM_WORLD.size


t_mar, b_mar, l_mar, r_mar = (0.01, 0.01, 0.01, 0.01)
h_slice, w_slice = (0.3125, 1)
h_pad = 0.03

h_total = t_mar + 3*h_slice + 2*h_pad + b_mar
w_total = l_mar + w_slice + r_mar

width = 3.4
scale = width/w_total

fig = plt.figure(1, figsize=(scale * w_total,
                             scale * h_total))

# axis
plot_axes = []
for i in range(3):
    left = l_mar / w_total
    bottom = 1 - (t_mar + h_slice + i*(h_slice+h_pad) ) / h_total
    width = w_slice / w_total
    height = h_slice / h_total
    plot_axes.append(fig.add_axes([left, bottom, width, height]))

Bmax = 20
Bmin = 4

filename = lambda s: 'snapshots/snapshots_s{:d}.h5'.format(s)
lw=1.4
levels=6

x_hist = np.array([])
y_hist = np.array([])
for j in range(14):
    f = h5py.File(filename(j+1), 'r')
    x_hist = np.concatenate((x_hist, f['tasks/x'][:,0,0]))
    y_hist = np.concatenate((y_hist, f['tasks/y'][:,0,0]))

file_nums = [2,8,14]

for i in range(3):
    with h5py.File(filename(file_nums[i]), 'r') as file:

        x = file['scales/x']['1.0'][:]
        y = file['scales/y']['1.0'][:]
        t = file['scales/sim_time'][0]
        A = file['tasks/A'][0]
        M = file['tasks/M'][0]
        print(M.min(), M.max(), M.mean(), M.std())
        yy, xx = np.meshgrid(y,x)
        im = plot_axes[i].contourf(xx,yy,M,[0.2,0.5,0.8,1.1],extend='both',cmap='Purples',zorder=1)
        im.cmap.set_under('white')
        im.changed()
        plot_axes[i].contour(xx,yy,A,
                  levels=np.linspace(Bmin,Bmax,levels),
                  colors=['black'],
                  linewidths=[lw],
                  linestyles=['solid'],zorder=3)
        plot_axes[i].contour(xx,yy,A,
                  levels=np.linspace(-Bmax,-Bmin,levels),
                  colors=['black'],
                  linewidths=[lw],
                  linestyles=['solid'],zorder=3)
        cadence = 12
        plot_axes[i].plot(x_hist[:(file_nums[i]-1)*50:cadence],y_hist[:(file_nums[i]-1)*50:cadence], '.', color='C2', zorder=5, lw=lw)
        plot_axes[i].axis([-4,12,-3.9,1.1])
        plot_axes[i].axis('off')

plt.savefig('fig_maglev.pdf')

