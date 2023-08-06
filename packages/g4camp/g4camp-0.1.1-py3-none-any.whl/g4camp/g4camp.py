import sys

import pkg_resources
available_packages = [pkg.key for pkg in pkg_resources.working_set]
if 'geant4-pybind' in available_packages:
    from geant4_pybind import *
else:
    sys.exit("Package 'geant4_pybind' is not available.")

from g4camp.DetectorConstruction import DetectorConstruction
from g4camp.CustomPhysicsList import CustomPhysicsList
from g4camp.ActionInitialization import ActionInitialization
from g4camp.DataBuffer import DataBuffer

class g4camp:

    def __init__(self, optics=True, multithread=False, thread_num=4):
        # By some reason multithread mode does not faster than serial mode
        # FIXME: number of threads can not be configured from here (why???)
        # For it is only configured by macro file
        #
        super().__init__()
        self.data_buffer = DataBuffer()
        #
        self.macro = "default.mac"
        self.optics = optics            # switch on/off optic physics
        self.ph_suppression_factor = 10 # must be integer
        self.skip_mode = 'fraction'     # 'fraction' (relative to E_init) or 'GeV' (absolute)
        self.skip_min = 1.e-3           # min energy to skip particle (wrt. E_init or in GeV)
        self.skip_max = 1.e-1           # max energy to skip particle (wrt. E_init or in GeV)
        self.random_seed = 1
        # the following varialbes are to be set later
        self.E_skip_min = None          # min particle energy to skip
        self.E_skip_max = None          # max particle energy to skip
        self.E_init = None              # initial kinetic energy in GeV
        #
        self.ph_counter = None
        #
        if multithread:
            self.runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.MT, thread_num)
        else:
            self.runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
        self.detConstruction = DetectorConstruction()
        self.physList = CustomPhysicsList(optics=self.optics)
        self.actInit = ActionInitialization(self)
        self.runManager.SetUserInitialization(self.detConstruction)
        self.runManager.SetUserInitialization(self.physList)
        self.runManager.SetUserInitialization(self.actInit)


    def configure(self):
        #self.actInit.stackingAction.SetPhotonSuppressionFactor(1./self.ph_fraction)
        self.UImanager = G4UImanager.GetUIpointer()
        self.UImanager.ApplyCommand(f"/control/execute {self.macro}")
        G4Random.setTheSeed(self.random_seed)

    def setMacro(self, macro):
        self.macro = macro

    def setSkipMinMax(self, skip_min, skip_max):
        self.skip_min = skip_min
        self.skip_max = skip_max

    def setRandomSeed(self, val):
        self.random_seed = int(val)

    def setPhotonSuppressionFactor(self, val):
        self.ph_suppression_factor = float(val)

    def run(self, n_events):
        for i in range(n_events):
            self.runManager.BeamOn(1)
            yield self.data_buffer
