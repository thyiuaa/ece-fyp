import matplotlib.pyplot as plt
import numpy as np

fig1, ax1 = plt.subplots()
pre_img = np.loadtxt("rf_2media_0percent_FieldII.dat")
c1 = ax1.pcolormesh(pre_img)
ax1.set_title('Pre-compression Image')
fig1.colorbar(c1, ax=ax1)
fig1.tight_layout()

fig2, ax2 = plt.subplots()
post_img = np.loadtxt("rf_2media_5percent_FieldII.dat")
c2 = ax2.pcolormesh(post_img)
ax2.set_title('Post-compression Image')
fig2.colorbar(c2, ax=ax2)
fig2.tight_layout()

plt.show()
