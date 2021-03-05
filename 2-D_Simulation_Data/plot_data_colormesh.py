import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
pre_img = np.loadtxt("rf_2media_0percent_FieldII.dat")
c = ax.pcolormesh(pre_img)
ax.set_title('Pre-compression Image')
fig.colorbar(c, ax=ax)
fig.tight_layout()
plt.show()

fig2, ax2 = plt.subplots()
post_img = np.loadtxt("rf_2media_5percent_FieldII.dat")
c2 = ax2.pcolormesh(post_img)
ax2.set_title('Post-compression Image')
fig2.colorbar(c, ax=ax2)
fig2.tight_layout()
plt.show()
