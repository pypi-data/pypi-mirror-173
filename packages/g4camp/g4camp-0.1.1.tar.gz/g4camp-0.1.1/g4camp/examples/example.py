from g4camp.g4camp import g4camp
from time import time
import sys

n_events = 10

#app = g4camp(multithread=True, thread_num=16) # does not work faster
app = g4camp(multithread=False)
app.setMacro("electrons.mac")
app.setSkipMinMax(0.001, 0.05)
app.configure()

time0 = time()
for data in app.run(n_events):
    vertices = data.vertices
    tracks = data.tracks
    photon_cloud = data.photon_cloud
print(f"# Run time:  {(time()-time0):.2f} sec, {((time()-time0)/n_events):.2f} sec/event")
