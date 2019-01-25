import util
import math
import random

def sortedResources(pprint, karb_map, fuel_map, loc):
    size = len(karb_map)
    lst1 = []
    for y in range(size):
        for x in range(size):
            if karb_map[y][x]:# or fuel_map[y][x]:
                lst1.append((x,y))

    util.insertionSortLoc(pprint, lst1, loc)

    return lst1


def behind(loc, castle_loc, full_map, h_symmetric):
    size = len(full_map)
    if h_symmetric:
        if castle_loc[1] <= size // 2:
            if loc[1] <= castle_loc[1]:
                return True
            else:
                return False
        else:
            if loc[1] >= castle_loc[1]:
                return True
            else:
                return False
    else:
        if castle_loc[0] <= size // 2:
            if loc[0] <= castle_loc[0]:
                return True
            else:
                return False
        else:
            if loc[0] >= castle_loc[0]:
                return True
            else:
                return False


def unattainable(lst1, castle_loc, full_map, h_symmetric, loc):
    lst2 = []

    for i in range(len(lst1)):
        
        if util.euclidianDistance(lst1[i],castle_loc) <= 100:
            continue

        if util.euclidianDistance(lst1[i],loc) <= 100:
            continue

        if behind(lst1[i],castle_loc,full_map, h_symmetric):
            continue

        if behind(lst1[i],loc,full_map, h_symmetric):
            continue

        lst2.append(lst1[i])

    return lst2

def hotspots(targets):
    target_zones = []
    current = target[0]
    for target in targets:
        dist = util.euclidianDistance(target,current)
        if dist >= 20:
            target_zones.append(target)
            current = target

    return target_zones

def anti_expand_targets(pprint, karb_map, fuel_map, full_map, castle_loc, h_symmetric, loc):
    # Generate sorted resources
    lst1 = sortedResources(pprint, karb_map, fuel_map, castle_loc)
    # Remove unattianable resources
    lst1 = unattainable(lst1, castle_loc, full_map, h_symmetric, loc)

    return lst1


def centroid_attack(full_map, is_visible, visible_bots):
    ax = 0; ay = 0; 
    bx = 0; by = 0;
    cx = 0; cy = 0;

    if len(visible_bots) < 3:
        return (random.randint(-1,1), random.randint(-1,1))
    
    k = 0
    for bot in visible_bots:
        if not is_visible(bot):
            continue
        if k == 0:
            ax = bot['x']
            ay = bot['y']
        elif k == 1:
            bx = bot['x']
            by = bot['y']
        elif k == 2:
            cx = bot['x']
            cy = bot['y']
            break

        k += 1

    ox = 1/(2 * ((ax - bx)*(by - cy) - (ay - by)*(bx - cx))) * ((by - cy)*(ax**2 - bx**2 + ay**2 - by**2) + (by - ay)*(bx**2 - cx**2 + by**2 - cy**2))
    oy = 1/(2 * ((ax - bx)*(by - cy) - (ay - by)*(bx - cx))) * ((cx - bx)*(ax**2 - bx**2 + ay**2 - by**2) + (ax - bx)*(bx**2 - cx**2 + by**2 - cy**2))

    return (int(ox), int(oy))




