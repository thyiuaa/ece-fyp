import matplotlib.pyplot as plt
import numpy as np

axial_shear = np.loadtxt("result/axial_shear_result.dat")
lateral_shear = np.loadtxt("result/lateral_shear_result.dat")
axial_strain = np.loadtxt("result/axial_strain_result.dat")
lateral_strain = np.loadtxt("result/lateral_strain_result.dat")
axial_translation = np.loadtxt("result/axial_translation_result.dat")
lateral_translation = np.loadtxt("result/lateral_translation_result.dat")
correlation = np.loadtxt("result/correlation_result.dat")

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

fig5, ax5 = plt.subplots()
c5 = ax5.pcolormesh(lateral_translation)
ax5.set_title('Lateral Translation')
fig5.colorbar(c5, ax=ax5)
fig5.tight_layout()

fig6, ax6 = plt.subplots()
c6 = ax6.pcolormesh(axial_translation)
ax6.set_title('Axial Translation')
fig6.colorbar(c6, ax=ax6)
fig6.tight_layout()

fig7, ax7 = plt.subplots()
c7 = ax7.pcolormesh(correlation)
ax7.set_title('Correlation')
fig7.colorbar(c7, ax=ax7)
fig7.tight_layout()

plt.show()