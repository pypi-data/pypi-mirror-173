import time

import numpy as np
from streamtracer import StreamTracer, VectorGrid

nsteps = 10000
step_size = 0.1
tracer = StreamTracer(nsteps, step_size)

field = np.ones((180, 360, 50, 3))
grid_spacing = [1, 2, 1]
grid = VectorGrid(field, grid_spacing)

times = {}
for nseeds in 2**np.arange(8):
    t = time.time()
    seeds = np.repeat([[0, 0, 0]], nseeds, axis=0)
    tracer.trace(seeds, grid)
    dt = time.time() - t
    assert len(tracer.xs) == nseeds
    times[nseeds] = dt
    print(nseeds, dt / nseeds)


import matplotlib.pyplot as plt
fig, ax = plt.subplots()

ax.plot(times.keys(), times.values(), marker='.')
ax.set_xlabel('n seeds')
ax.set_ylabel('time (s)')
ax.set_xscale('log')
ax.set_yscale('log')
plt.show()
