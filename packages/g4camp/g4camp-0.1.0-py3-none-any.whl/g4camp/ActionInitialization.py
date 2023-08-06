from geant4_pybind import *
from g4camp.PrimaryGeneratorAction import PrimaryGeneratorAction
from g4camp.RunAction import RunAction
from g4camp.EventAction import EventAction
from g4camp.StackingAction import StackingAction
from g4camp.SteppingAction import SteppingAction
from g4camp.DataBuffer import DataBuffer

class ActionInitialization(G4VUserActionInitialization):

    def __init__(self, app):
        super().__init__()
        self.app = app

    def BuildForMaster(self):  # invoked in multithread mode only
        self.SetUserAction(RunAction(True))

    def Build(self):           # invoked in in boths modes: multihread - multiple time, serial - once
        self.SetUserAction(PrimaryGeneratorAction())
        self.SetUserAction(RunAction(False))
        self.SetUserAction(EventAction(self.app))
        self.SetUserAction(StackingAction(self.app))
        self.SetUserAction(SteppingAction(self.app))
