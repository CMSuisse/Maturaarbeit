import scipy.optimize as scop
from matplotlib import pyplot as plt
import numpy as np

FLUX = [
841128,
1073712,
336527,
614883,
145314,
202224,
1502406,
1056801,
540382,
632002,
171449,
356634,
1890106,
1035392,
644473,
477759,
171759,
535476
]

MAG = [
3.76,
2.68,
5.7,
3.78,
5.73,
5.48,
2.23,
2.46,
4.45,
3.77,
5.32,
3.79,
1.08,
2.22,
3.55,
3.77,
4.91,
2.56
]

objective_func = lambda x, a: -2.5*np.log10(x/a)

popt, _ = scop.curve_fit(objective_func, FLUX, MAG)
print(popt)
residuals = MAG - objective_func(FLUX, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((MAG-np.mean(MAG))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)

fig, ax = plt.subplots()
ax.scatter(FLUX, MAG)
ax.set_xlabel("Flux [ADU*s^-1]")
ax.set_ylabel("Magnitude")
ax.ticklabel_format(useOffset=False)
ax.locator_params(axis="x", tight=True, nbins=2)

x_line = np.arange(min(FLUX), max(FLUX), 1)
y_line = objective_func(x_line, *popt)
ax.plot(x_line, y_line, "--", color="red")
plt.show()