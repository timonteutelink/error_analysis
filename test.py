#%%
from expression import Expression
from uncertainValue import UncertainValue

#%%
length = UncertainValue(18, absolute=True, error=0.1 * 10 ** -3, label="l [m]")
width = UncertainValue(26, absolute=True, error=0.1 * 10 ** -2, label="w [m]")

A = Expression("l * w", label = "A [m^2]")
A.setVariable("l", length)
A.setVariable("w", width)
print(A)

#%%

