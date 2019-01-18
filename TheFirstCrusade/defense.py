import random
import util
import math
import time
import hilbert


def hilbert_points(p):
    N = 2 # Number of Dimensions

    spacing = 2

    pmax = 2
    side = 2**pmax
    min_coord = 0
    max_coord = spacing*(side - 1)
    cmin = min_coord - 0.5
    cmax = max_coord + 0.5

    dx = 0.5*spacing
    offset = -1

    hc = hilbert.HilbertCurve(p, N)

    sidep = 2**p

    npts = 2**(N*p)
    pts = []
    for i in range(npts):
        pts.append(hc.coordinates_from_distance(i))
    pts = [
        [spacing*(pt[0]*side/sidep) + offset,
         spacing*(pt[1]*side/sidep) + offset]
        for pt in pts]

    # Returns pts of defense relative to the castle

    return pts

def hilbert_defense(loc, castle_loc, h_symmetry, visible_map, full_map, fuel_map, karbonite_map, unit_type, team, SPECS):
    units = {SPECS['PROPHET']: 2, SPECS['PREACHER']: 1}
    points = hilbert_points(units[unit_type])
    size = len(full_map)
    quadrantSplit = util.quadSplit(points)
    if h_symmetry and castle_loc[1] >= size // 2:
        # We are on lower half so build top first
        pts = [item for sublist in quadrantSplit for item in sublist]
    elif h_symmetry and castle_loc[1] < size // 2: 
        # We are on top half so build the bottom first
        quadrantSplit[2], quadrantSplit[0] = quadrantSplit[0], quadrantSplit[2]
        quadrantSplit[3], quadrantSplit[1] = quadrantSplit[1], quadrantSplit[3]
        pts = [item for sublist in quadrantSplit for item in sublist]
    elif not h_symmetry and castle_loc[0] >= size // 2:
        # We are on right half so we build the left side first
        quadrantSplit[0], quadrantSplit[1], quadrantSplit[2], quadrantSplit[3] = quadrantSplit[1], quadrantSplit[2], quadrantSplit[0], quadrantSplit[3]
        pts = [item for sublist in quadrantSplit for item in sublist]
    elif not h_symmetry and castle_loc[0] < size // 2:
        # We are on left half so we build the right side first
        quadrantSplit[2], quadrantSplit[0] = quadrantSplit[0], quadrantSplit[2]
        pts = [item for sublist in quadrantSplit for item in sublist]

    pos_arr = []
    for pt in pts:
        pos_arr.append((castle_loc[0] + pt[0], castle_loc[1] + pt[1]))

    defense_pos = pos
    for pos in pos_arr:
        if pos[0] < 0 or pos[1] < 0 or pos[1] >= size or pos[0] >= size:
            continue

        init_pos = pos
        i = 0
        dirs=[(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1, -1),(-1, 0),(-1, 1)]
        collide_w_resource = False
        while fuel_map[pos[1]][pos[0]] or karbonite_map[pos[1]][pos[0]] or not full_map[pos[1]][pos[0]]:
            pos = init_pos
            if i >= len(dirs):
                collide_w_resource = True
                break
            pos = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
            i += 1

        if collide_w_resource:
            continue

        if visible_map[pos[1]][pos[0]] > 0:
            continue

        defense_pos = pos
        break


    return defense_pos





def gosper_defense():
    pass