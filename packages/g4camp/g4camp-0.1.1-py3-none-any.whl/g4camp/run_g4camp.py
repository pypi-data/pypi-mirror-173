from g4camp.g4camp import g4camp
import time
import numpy as np
import h5py
import sys
import configargparse
import logging

log = logging.getLogger('run_g4camp')
logformat='[%(name)12s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)

def report_timing(func):
    def func_wrapper(*args, **kwargs):
        tic = time.time()
        result = func(*args, **kwargs)
        toc = time.time()
        dt = toc - tic
        log .info(f'{func.__name__}'.ljust(40)+f'{dt:6.3f} seconds'.rjust(30))
        return result
    return func_wrapper


def parse_arguments():
    p = configargparse.get_argument_parser()
    p.add_argument('-n', default=100, help="number of events")
    p.add_argument('-m', default='muons.mac', help="macro file for Geant4")
    p.add_argument('-o', default='output.h5', help="output file name")
    p.add_argument('--skip_min', default=0.002, help="minimal of particle energy to skip")
    p.add_argument('--skip_max', default=0.01, help="maximal of particle energy to skip")
    p.add_argument('--random_seed', default=1, help="random seed")
    p.add_argument('--photon_suppression', default=10, help="photon suppression factor")
    p.add_argument('-l', '--log-level', choices=('deepdebug', 'debug', 'info', 'warning', 'error', 'critical'), default='info', help='logging level')

    opts = p.parse_args()
    #
    log.setLevel(opts.log_level.upper())
    log.info("----------")
    log.info(p.format_help())
    log.info("----------")
    log.info(p.format_values())    # useful for logging where different settings came from
    return opts


@report_timing
def run(app, n_events=10, ofname="output.h5"):
    h5file = h5py.File(ofname, "w")  # create empty file
    h5file.close()
    for ievt, data in enumerate(app.run(n_events)):
        h5file = h5py.File(ofname, "a")
        g = h5file.create_group(f"event_{ievt}")
        g.create_dataset('photons', data = data.photon_cloud)
        vpositions = [vertex[0] for vertex in data.vertices]
        vparticles = [vertex[2][0] for vertex in data.vertices]
        for itrk, track in data.tracks.items():
            gtrack = g.create_group(f"track_{itrk}")
            gtrack.create_dataset('header', data=[track.unique_id, track.parent_id, track.pdg_id])
            gtrack.create_dataset('points', data=track.points)
        g.create_dataset('vertex_positions', data = vpositions)
        g.create_dataset('vertex_particles', data = vparticles)
        h5file.close()
        log.info(f" Event #{ievt}/{n_events}")
        #log.info(f"   Number of vertices: {len(app.data_buffer.vertices)}")
        #log.info(f"   Number of tracks: {len(app.data_buffer.tracks)}")
        #log.info(f"   Number of photons: {len(app.data_buffer.photon_cloud)}")
        db = app.data_buffer
        log.info(f"   Number of vertices / tracks / photons : {len(db.vertices):6.0f} / {len(db.tracks):6.0f} / {len(db.photon_cloud):6.0f}")


def main():
    opts = parse_arguments()
    macro = opts.m
    #
    app = g4camp(optics=False)
    app.setMacro(macro)
    app.setRandomSeed(int(opts.random_seed))
    app.setSkipMinMax(float(opts.skip_min), float(opts.skip_max))
    app.setPhotonSuppressionFactor(float(opts.photon_suppression))
    app.configure()
    run(app, n_events=int(opts.n), ofname=opts.o)


if __name__ == "__main__":
    main()

