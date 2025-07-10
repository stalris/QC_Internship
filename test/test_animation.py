import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = [0, 1, 2]
y = [0, 1, 2]

# create a figure and axes once

fig, ax = plt.subplots()

def plot_frame(i):
    ax.clear()
    ax.plot(x[:i], y[:i], 'bo')
    ax.set_title(f"frame {i}")
   
ani = animation.FuncAnimation(fig, plot_frame, frames=3)

# ax.plot(x,y)
plt.show()
