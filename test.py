#%%
from expression import Expression
from uncertainValue import UncertainValue
from uncertainvaluelist import UncertainValueList
import numpy as np
import plotter

#%%
length = UncertainValue(18, 0.1 * 10 ** -3, label="l [m]")
width = UncertainValue(26, 0.1 * 10 ** -2, label="w [m]")

A = Expression("l * w", label = "A [m^2]")
A.setVariable("l", length)
A.setVariable("w", width)
print(A)

# %%

U = UncertainValueList(
        np.array([0.0101, 0.0200, 0.0500, 0.1002, 0.1502, 0.2003, 0.2512, 0.3000, 0.4020, 0.5006, 0.6027, 0.6997, 0.8005, 0.9003, 1.0008, 2.0040, 3.0250, 4.0107, 5.0041, 6.028, 7.012, 8.016, 9.002, 9.993, 10.104, 10.197, 10.293, 10.403, 10.510, 10.617, 10.708, 10.805, 10.901, 11.025, 11.195, 11.389, 11.591, 11.802, 11.983]),
        np.array([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]),
        label = "U [V]"
    )

I = UncertainValueList(
        np.array([1.6075, 3.3417, 8.450, 16.434, 23.261, 28.794, 33.142, 36.274, 40.803, 44.178, 47.335, 50.212, 53.140, 55.974, 58.67, 83.38, 104.81, 123.08, 139.78, 155.57, 169.85, 183.54, 196.30, 208.51, 209.85, 210.94, 212.09, 214.96, 216.25, 217.53, 218.61, 219.74, 220.88, 222.32, 224.29, 226.51, 228.80, 231.16, 233.18]) * 10**-3,
        np.array([0.0001, 0.0001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]) * 10**-3,
        label = "I [A]"
    )

P = U * I # [W]
R = U / I # [Ohm]

print(R)

alpha = 0.0049 # [1/K] confirmed

R0 = R.getValueAtIndex(0)

T0 = UncertainValue(273.15 + 21, 1.0, label="T0 [K]")

T = ((R - R0) / (R0 * alpha)) + T0 # use expressions for this
# dT = np.sqrt((dR / (R0 * alpha)) ** 2 + dT0 ** 2)

plotter.plotData(T, P)
#%%

f0 = UncertainValueList(
    np.array([200.5, 218.5, 240.25, 267.5, 299.25, 419.0, 540.0, 1009.0, 368.75, 456.25, 720.0, 873.5]),
    0,
    "f0 [Hz]"
)
L = UncertainValueList(
    np.array([21.3, 19.1, 17.5, 16.0, 14.4, 11.5, 9.8, 5.8, 12.4, 10.5, 7.7, 6.6]) * 10 ** -2,
    5 * 10 ** -3,
    "f0 [Hz]"
)
V = UncertainValueList(
    (320 - np.array([0.0001, 50, 95, 135, 160, 240, 260, 300, 210, 240, 285, 295])) * 10 ** -6,
    15 * 10 ** -6,
    "f0 [Hz]"
)

plotter.fitLinearData(f0 ** 2, V ** -1)
plotter.fitLinearData(1 / (f0 * 4), L)