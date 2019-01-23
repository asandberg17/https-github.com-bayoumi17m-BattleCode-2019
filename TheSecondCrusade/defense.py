import random
import util
import math
import time
import hilbert


def hilbert_points(pprint,p):
    N = 2 # Number of Dimensions

    # pprint("P is: " + p)

    spacing = 4

    pmax = 2
    side = 2**pmax
    min_coord = 0
    max_coord = spacing*(side - 1)
    cmin = min_coord - 0.5
    cmax = max_coord + 0.5

    dx = 0.5*spacing
    offset = -3

    hc = hilbert.HilbertCurve(pprint, p, N)

    for i in range(2,p,-1):
        offset += dx
        dx *= 2

    sidep = 2**p

    npts = 2**(N*p)
    pts = []
    for i in range(npts):
        pts.append(hc.coordinates_from_distance(i))

    # pprint("pts var is: " + str(pts))
    
    new_pts = []
    for pt in pts:
        new_pts.append((spacing*(pt[0]*side/sidep) + offset, spacing*(pt[1]*side/sidep) + offset))

    # Returns pts of defense relative to the castle

    return new_pts

def hilbert_defense(pprint, loc, castle_loc, h_symmetry, visible_map, full_map, fuel_map, karbonite_map, unit_type, team, SPECS, type_seen):
    units = {SPECS['PROPHET']: 2, SPECS['PREACHER']: 1}
    points = hilbert_points(pprint, units[unit_type])[type_seen:]
    size = len(full_map)
    # pprint("hilbert_points is: " + str(points)) # Returned points are wrong
    # quadrantSplit = util.quadSplit(points)
    # if h_symmetry and castle_loc[1] >= size // 2:
    #     # We are on lower half so build top first
    #     pts = [item for sublist in quadrantSplit for item in sublist]
    # elif h_symmetry and castle_loc[1] < size // 2: 
    #     # We are on top half so build the bottom first
    #     quadrantSplit[2], quadrantSplit[0] = quadrantSplit[0], quadrantSplit[2]
    #     quadrantSplit[3], quadrantSplit[1] = quadrantSplit[1], quadrantSplit[3]
    #     pts = [item for sublist in quadrantSplit for item in sublist]
    # elif not h_symmetry and castle_loc[0] >= size // 2:
    #     # We are on right half so we build the left side first
    #     quadrantSplit[0], quadrantSplit[1], quadrantSplit[2], quadrantSplit[3] = quadrantSplit[1], quadrantSplit[2], quadrantSplit[0], quadrantSplit[3]
    #     pts = [item for sublist in quadrantSplit for item in sublist]
    # elif not h_symmetry and castle_loc[0] < size // 2:
    #     # We are on left half so we build the right side first
    #     quadrantSplit[2], quadrantSplit[0] = quadrantSplit[0], quadrantSplit[2]
    #     pts = [item for sublist in quadrantSplit for item in sublist]

    pos_arr = []
    for pt in points:
        pos_arr.append((castle_loc[0] + pt[0], castle_loc[1] + pt[1]))

    # pprint("Potential Spots: " + str(pos_arr))

    defense_pos = castle_loc
    for pos in pos_arr:
        if pos[0] < 0 or pos[1] < 0 or pos[1] >= size or pos[0] >= size:
            continue

        while not full_map[pos[1]][pos[0]]:
            if pos[1] < castle_loc[1]:
                pos[1] += 1 
                continue
            if pos[1] > castle_loc[1]:
                pos[1] -= 1 
                continue
            if pos[0] > castle_loc[0]:
                pos[0] -= 1 
                continue
            if pos[0] < castle_loc[0]:
                pos[0] += 1
                continue

        # init_pos = castle_loc
        # i = 0
        # dirs=[(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1, -1),(-1, 0),(-1, 1)]
        # collide_w_resource = False
        # while fuel_map[pos[1]][pos[0]] or karbonite_map[pos[1]][pos[0]] or not full_map[pos[1]][pos[0]]:
        #     pos = init_pos
        #     if i >= len(dirs):
        #         collide_w_resource = True
        #         break
        #     pos = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
        #     i += 1

        # if collide_w_resource:
        #     continue

        # if visible_map[pos[1]][pos[0]] > 0:
        #     continue


        defense_pos = pos
        break

    pprint("defense_pos: " + str(defense_pos))


    return defense_pos


def encircle(pprint, attack_loc, r2, tol, full_map):
    # Used to trap a castle in one spot so that it can not grow
    # If dist >= 150, continue towards the attack_loc
    # Otherwise using our vision, expand the shape
    # Potentially layer-up, returns a pair of destination and string representing action
    # (destination, Action)
    # Actions include 
    #"Follow": Follow the edge or stay behind current layer,
    #"Expand": continue forward toward our goal,
    #"Stop": Hold current position

    encirclement = []
    encirclement_rev = []
    size = len(full_map)

    for j in range(size):
        for l in range(size):
            if (l-attack_loc[0])**2 + (j-attack_loc[1])**2 <= r2+tol and (l-attack_loc[0])**2 + (j-attack_loc[1])**2 >= r2-tol:
                if full_map[j][l] == True:
                    encirclement.append((l,j))
                    encirclement_rev.append((l,j))
                # pprint("Dist_sq: " + str((l-attack_loc[0])**2 + (j-attack_loc[1])**2) + ", is close: " + str(util.isclose((l-attack_loc[0])**2 + (j-attack_loc[1])**2,r2,rel_tol=0,abs_tol=8)))
            # pprint("Dist: ")
            # if util.isclose((l-attack_loc[0])**2 + (j-attack_loc[1])**2, r2,abs_tol=10):
            #     pprint("Close")
            #     if full_map[j][l] == True:
            #         encirclement.append((l,j))
            #         encirclement_rev.append((l,j))

    # pprint("Len of encirclement: " + str(len(encirclement)))

    return encirclement, encirclement_rev.reverse()

def BFSlattice(pprint, castle_loc, full_map, fuel_map, karbonite_map,vis, check_vis):
    moves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    # start_time = time.time()

    visible = []
    for v in range(8320):
        visible.append(0)

    visible[int(util.nodeHash(*castle_loc))] = 1

    for v in vis:
        if not check_vis(v):
            continue
        visible[int(util.nodeHash(v['x'],v['y']))] = 1

    pprint("Checking (55,4): " + str(visible[1774]))

    size = len(full_map)
    settled = []
    visited = []
    frontier = []
    expanded_nodes = []
    for i in range(size):
        row = []
        vrow = []
        vrow1 = []
        for k in range(size):
            row.append(0)
            vrow1.append(0)
            vrow.append(0)
        visited.append(vrow)
        settled.append(row)
        expanded_nodes.append(vrow1)

    start_node = util.Node(None, castle_loc[0], castle_loc[1])

    frontier.append(start_node)

    visited[start_node.y][start_node.x] = start_node
    j = -1
    current_node = None

    expanded_nodes[castle_loc[1]][castle_loc[0]] = 1

    while len(frontier) > 0: # and (time.time() - start_time)*1000 <= 18
        j += 1

        current_node = frontier[0]
        current_index = 0
        pprint("Frontier: " + str(frontier))
        pprint("Node:" + str(current_node))


        frontier.pop(current_index)
        settled[current_node.y][current_node.x] = 1

        if full_map[current_node.y][current_node.x]:
            if not fuel_map[current_node.y][current_node.x] and not karbonite_map[current_node.y][current_node.x]:
                if visible[int(util.nodeHash(current_node.x,current_node.y))] == 0:
                    if (current_node.x + current_node.y) % 2 != 0:
                        return current_node

        children = []
        for move in moves:
            newx = current_node.x + move[0]
            newy = current_node.y + move[1]

            if newx >= size or newy >= size or newx < 0 or newy < 0:
                continue

            # pprint("Pot New Nodes: " + str((newx,newy)))

            if expanded_nodes[newy][newx] == 1:
                continue

            if full_map[newy][newx] == False:
                continue

            if visible[int(util.nodeHash(newx,newy))] == 1:
                continue

            if fuel_map[newy][newx] or karbonite_map[newy][newx]:
                continue

            new_node = util.Node(current_node,newx,newy)
            children.append(new_node)

        for child in children:

            # if settled[child.y][child.x]:
            #     continue

            # child.g = 1
            # child.h = 0
            # child.f = child.g + child.h

            frontier.append(child)
            expanded_nodes[child.y][child.x] = 1

    # return castle_loc
    

def lattice(pprint, protect_loc, pass_map, fuel_map, karbonite_map, vis, check_vis):
    # Defensive lattice
    # 
    path = BFSlattice(pprint,protect_loc,pass_map,fuel_map,karbonite_map,vis,check_vis)

    return (path.x, path.y)
    # return (0,0)