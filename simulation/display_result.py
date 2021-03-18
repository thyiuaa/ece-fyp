import matplotlib.pyplot as plt
import numpy as np

axial_shear = np.loadtxt("result/axial_shear_result.dat",delimiter="\t\t")
lateral_shear = np.loadtxt("result/lateral_shear_result.dat",delimiter="\t\t")
axial_strain = np.loadtxt("result/axial_strain_result.dat",delimiter="\t\t")
lateral_strain = np.loadtxt("result/lateral_strain_result.dat",delimiter="\t\t")

fig1, ax1 = plt.subplots()
c1 = ax1.pcolormesh(axial_shear)
ax1.set_title('Axial Shear')
fig1.colorbar(c1, ax=ax1)
fig1.tight_layout()

fig2, ax2 = plt.subplots()
c2 = ax2.pcolormesh(lateral_shear)
ax2.set_title('Lateral Shear')
fig2.colorbar(c2, ax=ax2)
fig2.tight_layout()

fig3, ax3 = plt.subplots()
c3 = ax3.pcolormesh(axial_strain)
ax3.set_title('Axial Strain')
fig3.colorbar(c3, ax=ax3)
fig3.tight_layout()

fig4, ax4 = plt.subplots()
c4 = ax4.pcolormesh(lateral_strain)
ax4.set_title('Lateral Strain')
fig4.colorbar(c4, ax=ax4)
fig4.tight_layout()

plt.show()