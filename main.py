# %%
x = [1, 2, 3, 4, 5]
y = [i**2 for i in x]
print(x, y)

# %%
import matplotlib.pyplot as plt

plt.plot(x, y)
plt.title("test")
plt.show()
