import os
import sys
import numpy as np
import mdtraj as md
"""
Use distance.tcl first to produce the distance.dat file with the 2 centroids you've selected,
once you have that output simply run this script as follows:
e.g.: python3 rmsd_trajectory_filter.py centroids_distances.dat traj_filtered_aligned.xtc filtered.pdb
This script will clean the trajectory of possible cell jumps and produce a new one called "clean.xtc"
"""
to_purge = []
Average = []


def average():
    with open('test1.dat', 'r') as f:
        for lines in f:
            Average.append(float(lines.split()[2]))
        b = np.array(Average)
        print(f"\nThese are the values of centroids distance per frame: {b}")
        return int(sum(Average) / len(Average) + ((sum(Average) / len(Average)) / 5))


print(f"\nThis is the average of the centroid displacement: {average()}")


def awkfilter(limit, datafile):
    os.system("awk '$3<'%s'' '%s' > purged.txt" % (limit, datafile))
    with open('purged.txt', 'r') as purged:
        for lines in purged:
            to_purge.append(int(lines.split()[0]))
        a = np.array(to_purge)
        print(f"\nThese are the clean frames from the trajectory: {a}")
        return a


def trajedit(trajectory, pdb):
    traj = md.load(trajectory, top=pdb)
    slice = traj.slice(frame_list, copy=True)
    slice.save_xtc("clean.xtc", force_overwrite=True)


frame_list = awkfilter(average(), sys.argv[1])
trajectory = sys.argv[2]
pdb = sys.argv[3]
print(f"\nThe total number of frames in the new trajectory is: {len(frame_list)}")
trajedit(trajectory, pdb)
