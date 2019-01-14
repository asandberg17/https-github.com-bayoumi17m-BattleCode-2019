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
    if new_point[0] < 0 or new_point[0] > len(full_map):
        return False
    if new_point[1] < 0 or new_point[0] > len(full_map):
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



        


# def goto(loc, target, full_map, robot_map, already_been):
#     goal_dir = calculate_dir(loc, target)
#     if goal_dir is (0,0):
#         return (0,0)
#     #self.log("MOVING FROM " + str(my_coord) + " TO " + str(nav.dir_to_coord[goal_dir]))
#     #while (not is_passable(full_map, loc, goal_dir, robot_map)) or (apply_dir(loc, goal_dir) in already_been):
#     target=apply_dir(loc, goal_dir)
#     # while (not is_passable(full_map, loc, goal_dir, robot_map)) or (apply_dir(loc, goal_dir) in already_been):
#     #     goal_dir = rotate(goal_dir, 1)
#     #     target=apply_dir(loc, goal_dir)
#     return goal_dir
    
   



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
    coord1_h=coord1[0],l-1-coord1[1]
    coord2=randint(0,l),randint(0,l)
    coord2_h=coord2[0],l-1-coord2[1]
    coord3=randint(0,l),randint(0,l)
    coord3_h=coord3[0],l-1-coord3[1]
    coord4=randint(0,l),randint(0,l)
    coord4_h=coord4[0],l-1-coord4[1]
    coord5=randint(0,l),randint(0,l)
    coord5_h=coord5[0],l-1-coord5[1]
    coord6=randint(0,l),randint(0,l)
    coord6_h=coord6[0],l-1-coord6[1]
    coord7=randint(0,l),randint(0,l)
    coord7_h=coord7[0],l-1-coord7[1]
    coord8=randint(0,l),randint(0,l)
    coord8_h=coord8[0],l-1-coord8[1]
    coord9=randint(0,l),randint(0,l)
    coord9_h=coord9[0],l-1-coord9[1]
    coord10=randint(0,l),randint(0,l)
    coord10_h=coord10[0],l-1-coord10[1]


    while full_map[coord1[1]][coord1[0]]:
        coord1=randint(0,l),randint(0,l)
    coord1_h=coord1[0],l-1-coord1[1]
    while full_map[coord2[1]][coord2[0]]:
        coord2=randint(0,l),randint(0,l)
    coord2_h=coord2[0],l-1-coord2[1]
    while full_map[coord3[1]][coord3[0]]:
        coord3=randint(0,l),randint(0,l)
    coord3_h=coord3[0],l-1-coord3[1]
    while full_map[coord4[1]][coord4[0]]:
        coord4=randint(0,l),randint(0,l)
    coord4_h=coord4[0],l-1-coord4[1]




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
    y_dist = x1[1] - y1[0] 
    return x_dist**2 + y_dist**2

def astar(pprint,vis,full_map,start,goal,moves):

    # visible = []
    # for v in range(len(vis)):
    #     if util.nodeHash(*start) != util.nodeHash(vis[v]['x'], vis[v]['x']):
    #          visible.append(util.nodeHash(vis[v]['x'], vis[v]['x']))

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
    start_time = time.time()
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

        if util.nodeHash(current_node.x,current_node.y) == util.nodeHash(end_node.x,end_node.y) or j >= 20:
            # pprint("COMPLETE")
            path = []
            current = current_node
            while current != None:
                path.insert(0,current)
                current = current.parent
            return path

        children = []
        for move in moves:
            newx = current_node.x + move[0]
            newy = current_node.y + move[1]

            collision = False
            for v in vis:
                # pprint("Robot's Position: " + str((v['x'],v['y'])))
                # pprint(str(newx == v['x'] and newy == v['y']))
                if util.nodeHash(newx,newy) == util.nodeHash(v['x'],v['y']):
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



def defense(full_map, loc):
    spoke=randint(1,4)
    target=loc[0],loc[1]

    if spoke==1:
        target=target[0],target[1]+3
        while not full_map[target[0]][target[1]]:
            target=target[0],target[1]+1
    if spoke==2:
        target=target[0]+3,target[1]
        while not full_map[target[0]][target[1]]:
            target=target[0]+1,target[1]
    if spoke==3:
        target=target[0],target[1]-3
        while not full_map[target[0]][target[1]]:
            target=target[0],target[1]-1
    if spoke==4:
        target=target[0]-3,target[1]
        while not full_map[target[0]][target[1]]:
            target=target[0]-1,target[1]
    return target





def get_closest_resources(loc,map,robot_map,fuel_map,karbonite_map):
    closest_resources=[]
    k=get_closest_karbonite(loc,karbonite_map)
    karb=True
    k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2

    #need to get a list of any castles or churches nearby

    #also need to get a way to 
    while k_dist<10:
        closest_resources.append(k)
        if karb==True:
            k=get_closest_karbonite(loc,fuel_map)
            k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2
            karb=False
        else:
            k=get_closest_karbonite(loc,karbonite_map)
            k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2
            karb=True
    #checking to make sure that the other type or resource doesnt have a deposit still in range
    if karb==True:
        k=get_closest_karbonite(loc,fuel_map)
        k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2
        karb=False
    else:
        k=get_closest_karbonite(loc,karbonite_map)
        k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2
        karb=True
    if k_dist<10:
        closest_resources.append(k)
    #now adding a final two locations, these will be the last two pilgrims the castle will send out and far enough away to build churches
    i=0
    while i<2:
        if karb==True:
            k=get_closest_karbonite(loc,fuel_map)
            k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2
            karb=False
        else:
            k=get_closest_karbonite(loc,karbonite_map)
            k_dist=(k[0]-loc[0])**2 +(k[1]-loc[1])**2
            karb=True
        closest_resources.append(k)
        i=i+1

    #need to make sure churches dont send pilgrims to resources within ten of a castle or other church
    #use self.get_robot(id) to figure out the type or robot

    return closest_resources

#first send pilgrims to nearest resources alternating between type  when the robots get there and are full they check if there is 
#a church within radius 5, if they can build a church they then see if there are any other resources within radius 5 if there are
#find the middle and test if it is viable, if not move slightly
def church_or_no(self,loc,map,visible,robot_map,fuel_map,karbonite_map,total_karb,total_fuel,self_tank):
    up=True
    churches = []
    #could make this a little faster by making it a while loop that exists once weve reached the length of visible or returns once we find a church
    for r in visible:
        if not self.is_visible(r):
            # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
            continue
        # now all in vision range, can see x, y etc
        dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
        #check of 
        if r['team'] == self.me['team'] and r['unit']=='1':
            churches.append(r)
    return not churches
#returns a boolean on whether or not a church needs to be built
#when were standing on the location to build a church we need to check once more that it is still necessary and that another robot
#hasnt built one before

#return the coordinates of a good buidling site
def church_build_site(loc,map,fuel_map,Karbonite_map,robot_map):
    dir=build_site[0]-loc[0],build_site[1]-loc[1]
    if is_passable(fmap, loc, dir, robot_map=None)==False:
    #the position wasn't good try another

def aiming(loc,map,robot_map)

    









