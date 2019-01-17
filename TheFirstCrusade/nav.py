from random import *
import util
import math
import time


coord_to_dir = {
    (0,0): "C",
    (0,1): "S",
    (1,1): "SE",
    (1,0): "E",
    (1,-1): "NE",
    (0,-1): "N",
    (-1, -1): "NW",
    (-1, 0): "W",
    (-1, 1): "SW",
}

dir_to_coord = {
    "C": (0,0),
    "S": (0,1),
    "SE": (1,1),
    "E": (1,0),
    "NE": (1,-1),
    "N": (0,-1),
    "NW": (-1, -1),
    "W": (-1, 0),
    "SW": (-1, 1),   
}

def calculate_dir(start, target):
    """
    Calculate the direction in which to go to get from start to target.
    start: a tuple representing an (x,y) point
    target: a tuple representing an (x,y) point
    as_coord: whether you want a coordinate (-1,0) or a direction (S, NW, etc.)
    """
    dx = target[0] - start[0]
    dy = target[1] - start[1]
    if dx < 0:
        dx = -1
    elif dx > 0:
        dx = 1
    
    if dy < 0:
        dy = -1
    elif dy > 0: 
        dy = 1
    
    return (dx, dy)

rotate_arr = [    
    (0,1),
    (1,1),
    (1,0),
    (1,-1),
    (0,-1),
    (-1, -1),
    (-1, 0),
    (-1, 1)
]

def get_list_index(lst, tup):
    # only works for 2-tuples
    if len(lst)==0:
        return -1
    for i in range(len(lst)):
        if lst[i][0] == tup[0] and lst[i][1] == tup[1]:
            return i
    return -1

def rotate(orig_dir, amount):
    direction = rotate_arr[(get_list_index(rotate_arr, orig_dir) + amount) % 8]
    return direction

def reflect(full_map, loc, horizontal=True):
    #need to use len-1 not len as a 57x57 board will only go up to a tile 56, start on that the h mirror should be zero
    v_reflec = (len(full_map[0])-1 - loc[0], loc[1])
    h_reflec = (loc[0], len(full_map)-1 - loc[1])
    if horizontal:
        return h_reflec if full_map[h_reflec[1]][h_reflec[0]] else v_reflec
    else:
        return v_reflec if full_map[v_reflec[1]][v_reflec[0]] else h_reflec

def is_passable(full_map, loc, coord_dir, robot_map=None):
    new_point = (loc[0] + coord_dir[0], loc[1] + coord_dir[1])
    if new_point[0] < 0 or new_point[0] >= len(full_map):
        return False
    if new_point[1] < 0 or new_point[1] >= len(full_map):
        return False
    if not full_map[new_point[1]][new_point[0]]:
        return False
    if robot_map is not None and robot_map[new_point[1]][new_point[0]] > 0:
        return False
    return True
    

def apply_dir(loc, dir):
    return (loc[0] + dir[0], loc[1] + dir[1])

# def goto(loc, target, full_map, robot_map, already_been):
#     goal_dir1 = calculate_dir(loc, target) 
#     loc1=apply_dir(loc,goal_dir1)
#     goal_dir2 = calculate_dir(loc1, target)
#     goal_dir2=goal_dir2[0]+goal_dir1[0],goal_dir2[1]+goal_dir1[1]
#     loc2=apply_dir(loc1,goal_dir2)
#     goal_dir3 = calculate_dir(loc2, target)
#     goal_dir3=goal_dir3[0]+goal_dir2[0],goal_dir3[1]+goal_dir2[1]
#     # calculate three goal directions, run at three, if it doesnt work run at two...
#     goal_dir=goal_dir3
#     loc=loc2
#     if goal_dir is (0,0):
#         return (0,0)
#     # self.log("MOVING FROM " + str(my_coord) + " TO " + str(nav.dir_to_coord[goal_dir]))
#     if goal_dir3[0]**2 +goal_dir3[1]**2>9:
#         goal_dir=goal_dir2
#         loc=loc1
#     i = 0
#     while not is_passable(full_map, loc, goal_dir, robot_map) and i < 4:# or apply_dir(loc, goal_dir) in already_been: # doesn't work because `in` doesn't work :(
#         # alternate checking either side of the goal dir, by increasing amounts (but not past directly backwards)
#         if i > 0:
#             i = -i
#         else:
#             i = -i + 1
#         goal_dir = rotate(goal_dir, i)
#     return goal_dir

def goto(loc, target, full_map, robot_map, already_been):
    goal_dir = calculate_dir(loc, target)
    if goal_dir is (0,0):
        return (0,0)
    # self.log("MOVING FROM " + str(my_coord) + " TO " + str(nav.dir_to_coord[goal_dir]))
    i = 0
    while not is_passable(full_map, loc, goal_dir, robot_map) and i < 4:# or apply_dir(loc, goal_dir) in already_been: # doesn't work because `in` doesn't work :(
        # alternate checking either side of the goal dir, by increasing amounts (but not past directly backwards)
        if i > 0:
            i = -i
        else:
            i = -i + 1
        goal_dir = rotate(goal_dir, i)
    return goal_dir
    # while not is_passable(full_map, loc, goal_dir, robot_map) and not in_list(already_been,loc):# or apply_dir(loc, goal_dir) in already_been: # doesn't work because `in` doesn't work :(
    #     # alternate checking either side of the goal dir, by increasing amounts (but not past directly backwards)
    #     # if i > 0:
    #     #     i = -i
    #     # else:
    #     #     i = -i + 1
    #     goal_dir = rotate(goal_dir, -i)
    #     loc=apply_dir(loc,goal_dir)
    # return goal_dir 
    
    

def in_list(dict,key):
 
    if key in dict.keys(): 
        return True
    else: 
        return False


def get_closest_karbonite(loc, karb_map):
    closest_karb = (-100, -100)
    karb_dist_sq = 100000
    for x in range(len(karb_map)):
        if abs(x - loc[0]) > karb_dist_sq:
            break
        for y in range(len(karb_map)):
            if abs(y - loc[1]) > karb_dist_sq:
                break
            if karb_map[y][x] and sq_dist((x,y), loc) < karb_dist_sq:
                karb_dist_sq = sq_dist((x,y), loc)
                closest_karb = (x,y)
    return closest_karb

def sq_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def spawn(loc,full_map,robot_map):
    goal_dir=(-1,0)
    while not is_passable(full_map, loc, goal_dir, robot_map):
        goal_dir = rotate(goal_dir, 1)
    
    return goal_dir

def symmetric(full_map):
    l=len(full_map)-1

    coord1=randint(0,l),randint(0,l)
    coord1_h=coord1[0],l-coord1[1]
    coord2=randint(0,l),randint(0,l)
    coord2_h=coord2[0],l-coord2[1]
    coord3=randint(0,l),randint(0,l)
    coord3_h=coord3[0],l-coord3[1]
    coord4=randint(0,l),randint(0,l)
    coord4_h=coord4[0],l-coord4[1]
    coord5=randint(0,l),randint(0,l)
    coord5_h=coord5[0],l-coord5[1]
    coord6=randint(0,l),randint(0,l)
    coord6_h=coord6[0],l-coord6[1]
    coord7=randint(0,l),randint(0,l)
    coord7_h=coord7[0],l-coord7[1]
    coord8=randint(0,l),randint(0,l)
    coord8_h=coord8[0],l-coord8[1]
    coord9=randint(0,l),randint(0,l)
    coord9_h=coord9[0],l-coord9[1]
    coord10=randint(0,l),randint(0,l)
    coord10_h=coord10[0],l-coord10[1]


    while not full_map[coord1[1]][coord1[0]]:
        coord1=randint(0,l),randint(0,l)
    coord1_h=coord1[0],l-coord1[1]
    while not full_map[coord2[1]][coord2[0]]:
        coord2=randint(0,l),randint(0,l)
    coord2_h=coord2[0],l-coord2[1]
    while not full_map[coord3[1]][coord3[0]]:
        coord3=randint(0,l),randint(0,l)
    coord3_h=coord3[0],l-coord3[1]
    while not full_map[coord4[1]][coord4[0]]:
        coord4=randint(0,l),randint(0,l)
    coord4_h=coord4[0],l-coord4[1]




    if full_map[coord1_h[1]][coord1_h[0]]==full_map[coord1[1]][coord1[0]]:
        if full_map[coord2_h[1]][coord2_h[0]]==full_map[coord2[1]][coord2[0]]:
            if full_map[coord3_h[1]][coord3_h[0]]==full_map[coord3[1]][coord3[0]]:
                if full_map[coord4_h[1]][coord4_h[0]]==full_map[coord4[1]][coord4[0]]:
                    if full_map[coord5_h[1]][coord5_h[0]]==full_map[coord5[1]][coord5[0]]:
                        if full_map[coord6_h[1]][coord6_h[0]]==full_map[coord6[1]][coord6[0]]:
                            if full_map[coord7_h[1]][coord7_h[0]]==full_map[coord7[1]][coord7[0]]:
                                if full_map[coord8_h[1]][coord8_h[0]]==full_map[coord8[1]][coord8[0]]:
                                    if full_map[coord9_h[1]][coord9_h[0]]==full_map[coord9[1]][coord9[0]]:
                                        if full_map[coord10_h[1]][coord10_h[0]]==full_map[coord10[1]][coord10[0]]:
                                            return True
    return False

def distance(x1,y1):
    x_dist = x1[0] - y1[0]
    y_dist = x1[1] - y1[1] 
    return x_dist**2 + y_dist**2

def astar(pprint,check_vis,vis,full_map,start,goal,moves):

    start_time = time.time()
    visible = []
    for v in range(8320):
        visible.append(0)

    for v in vis:
        if not check_vis(v):
            continue
        visible[int(util.nodeHash(v['x'],v['y']))] = 1

    # pprint(str(vis))

    size = len(full_map)
    settled = []
    visited = []
    frontier = []
    for i in range(size):
        row = []
        vrow = []
        for k in range(size):
            row.append(0)
            vrow.append(0)
        visited.append(vrow)
        settled.append(row)

    start_node = util.Node(None,*start)
    end_node = util.Node(None,*goal)

    # for v in vis:
    #     settled[v['y']][v['x']] = 1

    frontier.append(start_node)

    visited[start_node.y][start_node.x] = start_node
    j = -1
    current_node = None
    expanded = 1
    expanded_nodes = [start]

    while frontier != []:
        j += 1
        # print(current_node == frontier[0])
        # pprint("Iteration: " + str(j) + " Nodes expanded: " + str(expanded))
        # pprint("Nodes: " + str(expanded_nodes))

        current_node = frontier[0]
        current_index = 0

        for index, n in enumerate(frontier):
            if n.f < current_node.f:
                current_index = index 
                current_node = n

        frontier.pop(current_index)
        settled[current_node.y][current_node.x] = 1

        # pprint(j,current_node.x,current_node.y,current_node.f)

        if util.nodeHash(current_node.x,current_node.y) == util.nodeHash(end_node.x,end_node.y) or (time.time() - start_time)*1000 > 20:
            # pprint("COMPLETE")
            path = []
            current = current_node
            while current != None:
                path.insert(0,current)
                current = current.parent

            # pprint("Time: " + str((time.time() - start_time)*1000))
            return path

        children = []
        for move in moves:
            newx = current_node.x + move[0]
            newy = current_node.y + move[1]

            collision = False
            if visible[int(util.nodeHash(newx,newy))]:
                collision = True

            if collision:
                # pprint("collision")
                continue


            if newx > size - 1 or newx < 0 or newy > size - 1 or newy < 0:
                continue

            # print(full_map[newy][newx])
            if full_map[newy][newx] == False:
                continue

            new_node = util.Node(current_node,newx,newy)
            children.append(new_node)


        for child in children:

            if settled[child.y][child.x]:
                continue

            child.g = child.g + 1
            child.h = math.sqrt((child.y - end_node.y)**2 + (child.x - end_node.x)**2)
            child.f = child.g + child.h

            open_node = visited[child.y][child.x]
            if open_node != 0:
                if open_node.f < child.f:
                    continue

            frontier.append(child)
            expanded_nodes.append((child.x,child.y))
            expanded += 1



def defense(full_map, bot_map, loc):
    spoke=randint(1,4)
    target=loc[0],loc[1]

    if spoke==1:
        target=target[0],target[1]+3
        while not full_map[target[1]][target[0]]:
            target=target[0],target[1]+1
    if spoke==2:
        target=target[0]+3,target[1]
        while not full_map[target[1]][target[0]]:
            target=target[0]+1,target[1]
    if spoke==3:
        target=target[0],target[1]-3
        while not full_map[target[1]][target[0]]:
            target=target[0],target[1]-1
    if spoke==4:
        target=target[0]-3,target[1]
        while not full_map[target[1]][target[0]]:
            target=target[0]-1,target[1]
    return target

def defense_2(pprint, full_map, castle_loc, visible, defense_fields):
    pprint("Starting!")
    vis = []
    for i in range(8320):
        vis.append(0)

    for bot in visible:
        vis[int(util.nodeHash(bot['x'],bot['y']))] = 1

    pos = castle_loc
    initial_branch = util.crossBranch()
    pprint("Before the loop")
    start = time.time()
    timer = time.time() - start
    while defense_fields['state'] != 'STOP' and timer*1000 < 30:
        # pprint("Time: " + timer)
        pprint("Pos: " + pos)
        if defense_fields['state'] == 'EXPAND':
            if not full_map[pos[1]][pos[0]]:
                # Case 1: Position is impassable
                if castle_loc[1] > len(full_map) // 2 and castle_loc[0] > len(full_map) // 2:
                    while not full_map[pos[1]][pos[0]]:
                        pos = pos[0] - 1, pos[1] - 1
                elif castle_loc[1] > len(full_map) // 2 and castle_loc[0] < len(full_map) // 2:
                    while not full_map[pos[1]][pos[0]]:
                        pos = pos[0] + 1, pos[1] - 1
                elif castle_loc[1] < len(full_map) // 2 and castle_loc[0] > len(full_map) // 2:
                    while not full_map[pos[1]][pos[0]]:
                        pos = pos[0] - 1, pos[1] + 1
                elif castle_loc[1] < len(full_map) // 2 and castle_loc[0] < len(full_map) // 2:
                    while not full_map[pos[1]][pos[0]]:
                        pos = pos[0] + 1, pos[1] + 1

                
            if vis[int(util.nodeHash(*pos))]:
                pprint("SOMEONES HOME")
                # Case 2: Position has already been taken by another bot
                # if defense_fields['level'] > 2:
                #     # Sub-case: Already filled branch
                #     angle = util.crossAngle(util.crossBranch())
                #     pos = math.cos(angle)*util.crossLength(), math.sin(angle)*util.crossLength()
                #     if vis[int(util.nodeHash(*pos))]:
                #         # Sub-sub-case: If new branch has already been expanded and we see that someone is there
                #         defense_fields = {'parent' : None, 'level': 1, 'state': 'FOLLOW', 'branch': 0, 'branch_type': 'active', 'length': util.crossLength()}
                #     else:
                #         # Sub-sub-case: New Diamond has not been started
                #         defense_fields['level'] = 0
                #         defense_fields['state'] = 'STOP'
                #         defense_fields['branch_type'] = 'head'

                # sub case: unfilled branch
                defense_fields['level'] += 1
                # defense_fields['branch'] = util.crossBranch()
                # defense_fields['length'] = defense_fields['length']*util.crossScale()
                defense_fields['state'] = 'FOLLOW'


            else:
                # Case 3: Resource location? (Edge Case we ignore for now)

                # Case 4: Reach Expansion destination
                defense_fields['state'] = 'STOP'

        elif defense_fields['state'] == 'FOLLOW':

            defense_fields['branch'] = util.crossBranch()
            if defense_fields['branch_type'] != 'head':
                defense_fields['state'] = 'EXPAND'
                defense_fields['length'] = util.crossScale()*defense_fields['length']
                angle = util.crossAngle(defense_fields['branch'])
                # pprint("Angle is " + angle + ", Cos and Sine respectively: " + (math.cos(angle),math.sin(angle)))
                x, y = math.cos(angle)*defense_fields['length'], math.sin(angle)*defense_fields['length']
                # pprint("X is " + x + ", Y is " + y)
                pos = int(round(pos[0]+x,0)), int(round(pos[1]+y,0))
            else:
                defense_fields['length'] = util.crossScale()*defense_fields['length']
                defense_fields['level'] += 1
            # Still need to do case analysis

        timer = time.time() - start

    defense_pos = pos
    pprint("Final Pos: " + defense_pos)
    return defense_pos


def get_closest_resources(pprint,loc,full_map,fuel_map,karbonite_map):
    closest_resources=[]
    closest_resources_large=[]

    #ill get the closest resources in a radius of 25, then ill go through that list and make all the resources in a radius of two,
    #then each castle or church should send pilgrims to any in their radius two circle then send three more out to the next two elements
    #on the radius 25 list
    x_start=loc[0]-(len(full_map)//2)
    y_start=loc[1]-(len(full_map)//2)
    if x_start<0:
        x_start=0
    if y_start<0:
        y_start=0
    x_end=loc[0]+(len(full_map)//2)
    y_end=loc[1]+(len(full_map)//2)
    if x_end>len(full_map):
        x_end=len(full_map)
    if y_end>len(full_map):
        y_end=len(full_map)
    for x in range(x_start,x_end):
        for y in range(y_start,y_end):
            if fuel_map[y][x] or karbonite_map[y][x]:
                # pprint("Adding Resource: " + str([x,y]))
                closest_resources_large.append((x,y))
    
    x_start=loc[0]-2
    x_end=loc[0]+3
    y_start=loc[1]-2
    y_end=loc[1]+3
    if x_start<0:
        x_start=0
    if y_start<0:
        y_start=0
    if x_end>len(full_map):
        x_end=len(full_map)
    if y_end>len(full_map):
        y_end=len(full_map)
    for x in range(x_start,x_end):
        for y in range(y_start,y_end):
            if fuel_map[y][x] or karbonite_map[y][x]:
                closest_resources.append((x,y))


    #now have order both lists by distance
    util.insertionSortLoc(pprint, closest_resources, loc)
    util.insertionSortLoc(pprint, closest_resources_large, loc)
    # quickSort(closest_resources,closest_resources[0],closest_resources[len(closest_resources)+1],loc)
    # quickSort(closest_resources_large,closest_resources_large[0],closest_resources_large[len(closest_resources_large)+1],loc)
    if len(closest_resources)<len(closest_resources_large):
        closest_resources.append(closest_resources_large[len(closest_resources)])
    if len(closest_resources)<len(closest_resources_large):
        closest_resources.append(closest_resources_large[len(closest_resources)])
    # pprint("my closest resources are "+ str(closest_resources) + " with a location of: " + str(loc))
    # pprint(str(closest_resources_large))
    return closest_resources_large

def quickSort(l,min,max,loc):
    if min<max:
        j=partition(l,min,max,loc)

        quickSort(l,min,j-1,loc)
        quickSort(l,j,max,loc)

def partition(l,min,max,loc):
    t=min+1
    j=max
    temp=None
    pivot_dist=(l[0][0]-loc[0])**2+(l[0][1]-loc[1])**2
    t_dist=(l[t][0]-loc[0])**2+(l[t][1]-loc[1])**2
    j_dist=(l[j][0]-loc[0])**2+(l[j][1]-loc[1])**2
    while t<j:
        if t_dist<=pivot_dist:
            t=t+1
            t_dist=(l[t][0]-loc[0])**2+(l[t][1]-loc[1])**2
        elif j_dist>=pivot_dist:
            j=j-1
            j_dist=(l[j][0]-loc[0])**2+(l[j][1]-loc[1])**2
        else:
            temp=l[t]
            l[t]=l[j]
            l[j]=temp
            t=t+1
            j=j-1
            t_dist=(l[t][0]-loc[0])**2+(l[t][1]-loc[1])**2
    j_dist=(l[j][0]-loc[0])**2+(l[j][1]-loc[1])**2
    return j




#first send pilgrims to nearest resources alternating between type  when the robots get there and are full they check if there is 
#a church within radius 5, if they can build a church they then see if there are any other resources within radius 5 if there are
#find the middle and test if it is viable, if not move slightly
def church_or_no(me,loc,map,visible,karb,fuel):
    churches = []
    #could make this a little faster by making it a while loop that exists once weve reached the length of visible or returns once we find a church
    for r in visible:
        if not me.is_visible(r):
            # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
            continue
        # now all in vision range, can see x, y etc
        #check of 
        bot_loc=r['x'],r['y']
        dist=distance(bot_loc,loc)
        # pprint('i am this far away'+dist +'from a bot that is at'+bot_loc)
        # pprint('and i am at '+loc)
        if r['team'] == me.me['team'] and (r['unit']=='1' or r['unit']=='0') and dist<10:
            churches.append(r)

    # pprint(str(churches))
    # total_karbonite=karbonite+my_karbonite
    # total_fuel=fuel+my_fuel

    return len(churches)==0 and karb>=50 and fuel>=200
#returns a boolean on whether or not a church needs to be built
#when were standing on the location to build a church we need to check once more that it is still necessary and that another robot
#hasnt built one before

#return the coordinates of a good buidling site
#use self.get_visible_robot_map() for this
def church_build_site(pprint,loc,full_map,fuel_map,karbonite_map):
    #like attackable want to get all the tiles that are in vision that have resources
    #loop through grid around loc
    # center = loc[0]-2,loc[1]-2
    resources=[]
    x_start=loc[0]-2
    y_start=loc[1]-2
    for x in range(x_start,loc[0]+3):
        for y in range (y_start,loc[1]+3):
            if x >= len(full_map) or y >= len(full_map) or x < 0 or y < 0:
                continue
            if fuel_map[y][x]==True or karbonite_map[y][x]==True:
                resources.append([x,y])
    #now we have all the tiles nearby that have resources, have to find a sort of center
    x_cent=0
    y_cent=0
    for i in range(len(resources)):
        x_cent=x_cent+resources[i][0]
        y_cent=y_cent+resources[i][1]
    pprint('the number of resources found was '+len(resources) +'i am at '+loc)
    x_cent=int(x_cent/len(resources))
    y_cent=int(y_cent/len(resources))
    site=(x_cent,y_cent)
    #we now have the geographical middle but it may not be a whole number and it may not be a buildable location
    dirs=[(1,1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(-2,0),(2,0)]
    i=0
    init_site = site
    # pprint("Site: " + str(site))
    # pprint(full_map[site[1]][site[0]])
    # pprint(fuel_map[site[1]][site[0]])
    # pprint(karbonite_map[site[1]][site[0]])
    # if full_map[site[1]][site[0]] != True or fuel_map[site[1]][site[0]] or karbonite_map[site[1]][site[0]]:
    #     site2 = apply_dir(site,dirs[i])
    #     pprint("Site2: " + site2)
    #     i = i + 1
    #     if site2[0] < 0 or site2[1] < 0 or site2[0] >= len(full_map) or site2[1] >= len(full_map):
    #         site2 = apply_dir(site2,dirs[i])
    #         i = i + 1
        # pprint(full_map[site2[1]][site2[0]])
        # pprint(full_map[site2[1]][site2[0]])
        # pprint(fuel_map[site2[1]][site2[0]])
        # pprint(karbonite_map[site2[1]][site2[0]])
    
    while full_map[site[1]][site[0]] != True or fuel_map[site[1]][site[0]] or karbonite_map[site[1]][site[0]]:
        if i >= len(dirs):
            break
        site=apply_dir(site,dirs[i])
        i=i+1

        if site[0] < 0 or site[1] < 0 or site[0] >= len(full_map) or site[1] >= len(full_map):
            site = init_site


    # return (loc[0]-1,loc[1]-1)
    return site

def get_closest_dropoff(self, visible,homePath):
    best=None
    best_dist=1000
    for r in visible:
        if not self.is_visible(r):
            # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
            continue
        # now all in vision range, can see x, y etc
        dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
        #check of 
        if r['team'] == self.me['team'] and (r['unit']==1 or r['unit']==0):
            if dist<best_dist:
                best_dist=dist
                best=r
    if best!=None:          
        return best['x'],best['y']
    return homePath

def aiming(loc, visible, team, attackmin, attackmax):
    attkmax = int(math.sqrt(attackmax))
    attkmin = int(math.sqrt(attackmin))

    attack_map = []
    for i in range(-attkmax,attkmax+1):
        row = []
        for k in range(-attkmax,attkmax+1):
            row.append(0)
        attack_map.append(row)

    size = len(attack_map)

    attack_map[len(attack_map) // 2][len(attack_map) // 2] = -10
    centroid = (len(attack_map) // 2, len(attack_map) // 2)

    for botv in visible:
        rel_pos = (centroid[0] + (botv['x'] - loc[0]), centroid[1] + (botv['y'] - loc[1]))
        for i in range(-1,2):
            for k in range(-1,2):
                attk_map_pos = (rel_pos[0] + i, rel_pos[1] + k)
                if attk_map_pos[0] < 0 or attk_map_pos[0] >= size or attk_map_pos[1] < 0 or attk_map_pos >= size:
                    continue

                if botv['team'] != team:
                    attack_map[attk_map_pos[1]][attk_map_pos[0]] += 1
                else:
                    attack_map[attk_map_pos[1]][attk_map_pos[0]] -= 1

    max_pos = centroid
    for i in range(size):
        for k in range(size):
            if attack_map[max_pos[1]][max_pos[0]] < attack_map[i][k]:
                max_pos = (k,i)

    return (max_pos[0] - centroid[0], max_pos[1] - centroid[1])


def resource_occupied(self,SPECS,me,loc,target,visible):
    # self.log("target: " + target[1])
    # self.log("visible " + str(visible))
    for r in visible:
        if not self.is_visible(r):
            continue
        if r['x'] == target[0] and r['y'] == target[1] and r['unit'] == SPECS['PILGRIM'] and r['id'] != me['id']:
            return True
    return False



def new_resource_target(self,SPECS,pprint,me,loc,full_map,fuel_map,karbonite_map,visible):
    closest_resources=get_closest_resources(pprint,loc,full_map,fuel_map,karbonite_map)
    # pprint("new resources: " + str(closest_resources))
    i=0
    occupied=resource_occupied(self,SPECS,me,loc,closest_resources[0],visible)
    dist=distance(closest_resources[i],loc)
    # pprint("got this far")
    # pprint("Occupied: " + occupied)
    # if occupied:
    #     i = i + 1
    #     occupied=resource_occupied(self,SPECS,me,loc,closest_resources[i],visible)
    #     pprint("Occupied again? " + occupied)

    while occupied and dist < 100:
        if i >= len(closest_resources) - 1:
            break
        i += 1
        # pprint("closest_resources_new: " + str(closest_resources[i]))
        occupied=resource_occupied(self,SPECS,me,loc,closest_resources[i],visible)
        dist=distance(closest_resources[i],loc)
    # pprint("Return Value: " + closest_resources[i])
    return closest_resources[i]
    # return closest_resources[0]


def homies(self,SPECS,loc,visible,team):
    buddies=0
    for r in visible:
        if not self.is_visible(r):
            continue
        if r['team']==team and r['unit']==SPECS['CRUSADER']:
            buddies=buddies+1
    return buddies>4



def get_closest_resources_church(pprint,loc,robot_map,full_map,fuel_map,karbonite_map):
    closest_resources=[]
    closest_resources_large=[]

    #ill get the closest resources in a radius of 25, then ill go through that list and make all the resources in a radius of two,
    #then each castle or church should send pilgrims to any in their radius two circle then send three more out to the next two elements
    #on the radius 25 list
    x_start=loc[0]-(len(full_map)//2)
    y_start=loc[1]-(len(full_map)//2)
    if x_start<0:
        x_start=0
    if y_start<0:
        y_start=0
    x_end=loc[0]+(len(full_map)//2)
    y_end=loc[1]+(len(full_map)//2)
    if x_end>len(full_map):
        x_end=len(full_map)
    if y_end>len(full_map):
        y_end=len(full_map)
    for x in range(x_start,x_end):
        for y in range(y_start,y_end):
            if (fuel_map[y][x] or karbonite_map[y][x]) and robot_map[y][x]<=0:
                closest_resources_large.append((x,y))
    
    x_start=loc[0]-2
    x_end=loc[0]+3
    y_start=loc[1]-2
    y_end=loc[1]+3
    if x_start<0:
        x_start=0
    if y_start<0:
        y_start=0
    if x_end>len(full_map):
        x_end=len(full_map)
    if y_end>len(full_map):
        y_end=len(full_map)
    for x in range(x_start,x_end):
        for y in range(y_start,y_end):
            if fuel_map[y][x] or karbonite_map[y][x]:
                closest_resources.append((x,y))


    #now have order both lists by distance
    util.insertionSortLoc(pprint, closest_resources, loc)
    util.insertionSortLoc(pprint, closest_resources_large, loc)
    # quickSort(closest_resources,closest_resources[0],closest_resources[len(closest_resources)+1],loc)
    # quickSort(closest_resources_large,closest_resources_large[0],closest_resources_large[len(closest_resources_large)+1],loc)
    if len(closest_resources)<len(closest_resources_large):
        closest_resources.append(closest_resources_large[len(closest_resources)])
    if len(closest_resources)<len(closest_resources_large):
        closest_resources.append(closest_resources_large[len(closest_resources)])
    return closest_resources





    









