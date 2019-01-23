from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
import nav
import util
import defense
# import time
# import copy

__pragma__('iconv')
__pragma__('tconv')
__pragma__('opov')



# don't try to use global variables!!
class MyRobot(BCAbstractRobot):
    #for castles
    numCastles = 0
    attkCastle = 0
    castles = []
    castleLoc = {}
    coolDown = 0
    resources_sphere=[]
    castleBeaten = False
    pilgrim=True
    turnPos = 0
    build_guard=False
    guard_build_loc=(0,0)
    global_resources = []
    local_resources = []
    filled_resources = {}

    defense = True
    has_moved=False
    squad=False
    guard=False
    step=0
    # Make parent the id of the Castle or centroid bot
    defense_fields = {'parent' : None, 'level': 1, 'state': 'FOLLOW', 'branch': 0, 'branch_type': 'active', 'length': util.crossLength()}
    defending = False
    moved=0
    castle_loc = (-1,-1)
    blocked_spots = {}

    pilgrims_built=0
    closest_resources=[]

    karboniteMining = True
    attempt=0

    wave = []
    should_build_church=False
    build_site=(0,0)
    #homePath = (0,0)
    closest_dropoff=(0,0)
    target=(0,0)
    dropping_off=False
    mapSize = 0

    progress = 1e10

    already_been = {}
    base = None
    destination = None

    #variables for crusaders
    home=(0,0)
    castleBeaten=False
    destination=(0,0)
    last_health=0
    raider=True
    castle_killer=False
    returning_to_base=False
    squad=False
    meeting_place=(0,0)
    preacher_pair=False
    is_home=False


    def turn(self):

        if self.me['unit'] == SPECS['PROPHET']:
            self.log("Prophet health: " + str(self.me['health']))
            attack_order = {SPECS['PREACHER']: 1, SPECS['CRUSADER']: 3, SPECS['PROPHET']: 2}

            visible = self.get_visible_robots()
            full_map = self.get_passable_map()
            fuel_map = self.get_fuel_map()
            karbonite_map = self.get_karbonite_map()

            # get attackable robots
            attackable = []
            in_vision = []
            type_seen = 0
            

            for r in visible:
                # x = 5
                if not self.is_visible(r):
                    # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
                    continue
                # now all in vision range, can see x, y etc
                if r['unit'] == SPECS['CASTLE'] or r['unit'] == SPECS['CHURCH']:
                    if self.me['team'] == r['team']:
                        self.castle_loc = (r['x'],r['y'])

                if self.me['turn'] == 1:
                    if r['unit'] == SPECS['PROPHET']:
                        type_seen += 1

                in_vision.append(r)
                dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
                if r['team'] != self.me['team'] and SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_RADIUS'][0] <= dist <= SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_RADIUS'][1]:
                    attackable.append(r)

            if attackable:
                # attack first robot
                r = attackable[0]
                if r['unit'] == SPECS['CASTLE']:
                    self.castleBeaten = True
                for a in attackable:
                    if attack_order[a['unit']] < attack_order[r['unit']]:
                        r = a
                self.log('Prophet attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])

            moves = []
            for i in range(-4,5):
                for k in range(-4,5):
                    if i**2 + k**2 <= SPECS['UNITS'][SPECS['PROPHET']]['SPEED']:
                        moves.append((i,k))


            
            # # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
            my_coord = (self.me['x'], self.me['y'])
            self.already_been[my_coord] = True
            # self.log(nav.symmetric(self.map)) #for some reason this would sometimes throw an error
            if not self.destination:
                self.log("trying to move")
                # self.log(str(castle_loc == (-1,-1)))
                if self.castle_loc == (-1,-1):
                    self.destination = nav.defense(full_map, self.get_visible_robot_map(), my_coord)
                # elif type_seen < 16: # Change to be defualt until 4 preachers detected?
                #     self.log("Found Castle")
                #     # self.destination = nav.defense(self.get_passable_map(), self.get_visible_robot_map(), my_coord)
                #     # self.destination, self.defense_fields = nav.defense_2(self.log, self.get_passable_map(), castle_loc, in_vision, self.defense_fields) 
                #     self.destination = defense.hilbert_defense(self.log, my_coord, self.castle_loc, nav.symmetric(fuel_map), self.get_visible_robot_map(), full_map, fuel_map, karbonite_map, SPECS['PROPHET'], self.me['team'], SPECS, type_seen)
                #     self.log("Castle Loc is: " + str(self.castle_loc) + " and my destination is: " + str(self.destination))
                else:
                    self.log("DA BUBBLE")
                    self.destination = defense.lattice(self.log, my_coord, self.castle_loc, full_map, fuel_map, karbonite_map, self.get_visible_robot_map())
                    self.log("DESTINATION: " + str(self.destination))
                    # self.destination = (None, None)

            # self.log("DESTINATION is blocked: " + str(self.destination in self.blocked_spots) + " at " + str(self.destination))

            # if self.destination in self.blocked_spots:
            #     self.destination = defense.hilbert_defense(self.log, my_coord, self.castle_loc, nav.symmetric(fuel_map), self.get_visible_robot_map(), full_map, fuel_map, karbonite_map, SPECS['PROPHET'], self.me['team'], SPECS, self.blocked_spots)
            #     self.log("Castle Loc is: " + str(self.castle_loc) + " and my new destination is: " + str(self.destination))
                # self.blocked_spots = {}


            if my_coord[0]==self.destination[0] and my_coord[1]==self.destination[1]:
                self.log("CURRENTLY STANDING AT "+my_coord)
                self.log("DEFENDING MY DESTINATION AT " + str(self.destination))
                self.blocked_spots = {}
                self.defending = True
                return

            self.log("Trying to move to "+ str(self.destination))
            path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
            action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
            #return self.move(*nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been))
            self.log(action)
            return self.move(*action)



            
        if self.me['unit'] == SPECS['CRUSADER']:
            self.log("Crusader health: " + str(self.me['health']))
            my_loc=self.me['x'],self.me['y']
            if self.me['turn']==1:
                self.home=my_loc
                self.last_health=self.me['health']

            visible = self.get_visible_robots()
            moves = []
            for i in range(-4,5):
                for k in range(-4,5):
                    if i**2 + k**2 <= SPECS['UNITS'][SPECS['CRUSADER']]['SPEED']:
                        moves.append((i,k))

            # get attackable robots
            attackable = []
            possible_targets=[]
            signal = -1
            church_in_sight=False
            for r in visible:
                if self.is_radioing(r) and self.is_visible(r) and r['unit'] == SPECS['CASTLE']:
                    self.log("Receiving Signal: " + str(r['signal']))
                    signal = r['signal']
                # x = 5
                if not self.is_visible(r):
                    # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
                    continue
                # now all in vision range, can see x, y etc
                possible_targets.append(r)
                dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
                if r['team'] ==self.me['team'] and r['unit']==SPECS['CHURCH']:
                    church_in_sight=True
                if r['team'] != self.me['team'] and SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][0] <= dist <= SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][1]:
                    attackable.append(r)
                    
            #TODO: now sort attackable, this can be done last

            if attackable:
                # attack first robot
                r = attackable[0]
                if r['unit'] == SPECS['CASTLE']:
                    self.castleBeaten = True
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])
            
            #TODO: now sort possible_targets if our health is decreasing otherwise continue with the given task
            #we can sort possible_targets like we sort attackable
            if self.last_health>self.me['health']:
                self.last_health=self.me['health']
                #so we are under attack and not attacking back
                if possible_targets:
                    # attack first robot that is out of range but someone is firing on us
                    r = possible_targets[0]
                    target=(r['x'],r['y'])
                    path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, target, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)

            #so there is nobody to attack and no one attacking us time to continue with the mission
            self.last_health=self.me['health']

            if signal!=-1:
                #process any signal received from a castle
                self.log('receiving a signal')
                self.destination = util.unHash(signal - 57471)

                #TODO: HERE WE WILL PROCESS THE DIFFERENT SIGNALS AND DETERMINE IF THIS UNIT IS A GUARD OR ATTACKING

            if self.raider:
                self.log('I am a raider. I will attack '+self.destination)
                if (my_loc[0]-self.destination[0])**2 +(my_loc[1]-self.destination[1])**2 <6:
                    #if there is a church he can return home for his next target
                    if church_in_sight:
                        self.destination=self.home
                        path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.destination, moves)
                        action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                        self.raider=False
                        self.returning_to_base=True
                        return self.move(*action)
                    #else he is guarding there is nothing to do if he is not standing on a resource
                    church_site=nav.church_build_site(self,SPECS,self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map(),self.get_visible_robot_map())
                    if self.get_fuel_map()[my_loc[1]][my_loc[0]] or self.get_karbonite_map()[my_loc[1]][my_loc[0]] or my_loc==church_site:
                        safe_tile=nav.get_safe_tile(my_loc,self.get_passable_map(),self.get_karbonite_map(),self.get_fuel_map(),church_site)
                        path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, safe_tile, moves)
                        action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                        return self.move(*action)
                    return

                else:
                    self.log('not in position, sir!')
                    #hes not at his post he needs to get there
                    #MAYBE TODO: GET THE BEST POSITION TO GUARD RESOURCES FROM, PROPHETS WILL DEFINITELY NEED IT, OR WRITE IT FOR CASTLES
                    path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.destination, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])

                    return self.move(*action)

                   
            if self.castle_killer:
                self.log('I am the slayer of castles. I will attack '+self.destination)
                #he is either at his destination or not
                if my_loc==self.destination:
                    self.log('At my destination')
                    #hes in position but not attacking anymore, the castle must be beaten and he should return home
                    #going to have it right now so that he moves home and gets a new target
                    self.castle_killer=False
                    self.returning_to_base=True
                    path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.destination, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    #must inform the castle that the enemy is vanquished
                    self.castle_talk(111)
                    return self.move(*action)
                else:
                    #so he is moving to his destination
                    if self.squad != True:
                        self.squad=nav.homies(self,SPECS,my_loc,self.get_visible_robots(),self.me['team'])
                        if self.meeting_place==(0,0):
                            self.meeting_place=nav.meeting_place(self,my_loc,self.destination,moves)
                        #TODO: GET A FUNCTION THAT RETURNS A GOOD MEETING PLACE FOR FIVE CRUSADERS AND DOESNT LAND THEM ON RESOURCES AND IS TOWARDS THE ENEMY
                        if self.squad:
                            #then it is time to ride forth and do battle
                            path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.destination, moves)
                            action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                            return self.move(*action)
                        if self.meeting_place==my_loc:
                            #then he is patiently waiting for his squad
                            return
                        #if self._meeting place is taken:
                            #must calculate a new meeting place
                        else:
                            #he is not as his meeting place nor does he have a squad
                            path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.meeting_place, moves)
                            action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                            return self.move(*action)
                    #so he does have a squad he can go and attack 
                    path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.destination, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)

            if self.returning_to_base:
                #he is returning home
                if self.is_home:
                    #drop off any resources and receive new signal for next enemy target
                    #CHANGE THIS
                    #PLEASE CHANGE THIS
                    #TRYING TO MAKE IT GLARINLGY OBVIOUS!!!!!!!!!!!!!!!!!!!!
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    return
                #so he must still need to move home
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, self.destination, moves)
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                return self.move(*action)


            # if self.preacher_pair:
                #he is now in a squadron with preachers
                #TODO: MPDIFY HOMIES TO MAKE A PREACHER VERSION WHICH COUNTS FOR TWO PREACHERS AND TWO CRUSADERS
                # PREACHER SHOULD BE BEHIND CRUSADER BUT ALL THIS CAN BE DONE LATER

                


               
        elif self.me['unit'] == SPECS['PREACHER']:
            self.log("Preahcer health: " + str(self.me['health'])) 

            if self.me['turn'] == 1:
                self.homePath = (self.me['x'],self.me['y'])

            visible = self.get_visible_robots()
            # moves = [(-4, 0), (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2), (-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3), (-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (1, 3), (2, -3), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (2, 3), (3, -2), (3, -1), (3, 0), (3, 1), (3, 2), (4, 0)]
            moves = []
            for i in range(-4,5):
                for k in range(-4,5):
                    if i**2 + k**2 <= SPECS['UNITS'][SPECS['PREACHER']]['SPEED']:
                        moves.append((i,k))

            # get attackable robots
            attackable = []
            signal = -1
            for r in visible:
                if self.is_radioing(r) and self.is_visible(r) and r['unit'] == SPECS['CASTLE']:
                    self.log("Recieving Signal: " + str(r.signal))
                    signal = r.signal
                # x = 5
                if not self.is_visible(r):
                    # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
                    continue
                # now all in vision range, can see x, y etc
                dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
                if r['team'] != self.me['team'] and SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][0] <= dist <= SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][1]:
                    attackable.append(r)

            if attackable:
                # attack first robot
                # r = attackable[0]['x'], attackable[0]['y']
                r = nav.aiming(self.is_visible, self.log, (self.me['x'],self.me['y']), visible, self.me['team'], SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][0], SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][1])
                self.log("Attack_pos: " + str(r))

                # self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r[0], r[1])

            my_coord = (self.me['x'], self.me['y'])    
            if self.moved<4 and self.fuel>5 and self.defense==True and False:
                self.moved=self.moved+1
                destination = my_coord
                self.destination = nav.reflect(self.map, destination, nav.symmetric(self.get_fuel_map()))
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                return self.move(*action)

            else:

                if not self.destination:
                    self.log("trying to move")
                    if signal != -1:
                        destination = util.unHash(signal)
                    else:
                        destination = my_coord
                        self.destination = nav.reflect(self.map, destination, nav.symmetric(self.get_fuel_map()))

                # self.log("Signal: " + str(signal))
                if signal >= 0:
                    self.destination = nav.reflect(self.map, util.unHash(signal), nav.symmetric(self.get_fuel_map()))

                self.log("My destination is " + self.destination)
                if (self.destination[0]-my_coord[0])**2 + (self.destination[1]-my_coord[1])**2 < 10:
                    self.log("Holding my ground")
                    self.destination = self.homePath
                    path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                    # self.log("Length of path: " + len(path))
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)
                    # return


                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)

                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                # self.log("Cost: " + str((action[0]**2 + action[1]**2)*SPECS['UNITS'][SPECS['CRUSADER']]['FUEL_PER_MOVE']))
                # self.log("Fuel: " + str(self.fuel))
                return self.move(*action)

        elif self.me['unit'] == SPECS['CASTLE']:
            self.log("I AM A CASTLE HEAR ME ROAR")
            self.log("Fuel: " + str(self.fuel))
            self.log("karbonite: " + str(self.karbonite))
            # self.log("Health: " + str(self.me['health']))
            #initializing my coordinates
            my_coord = (self.me['x'], self.me['y'])

            if self.me['turn'] == 1:
                # Build list of locations with a resource
                lst1 = []
                lst2 = []
                for i in range(len(self.get_fuel_map())):
                    for k in range(len(self.get_fuel_map())):
                        if self.get_fuel_map()[i][k] or self.get_karbonite_map()[i][k]:
                            lst1.append(util.nodeHash(k,i))
                            lst2.append((k,i))

                util.insertionSort(self.log, lst1)
                util.insertionSortLoc(self.log, lst2, (self.me['x'], self.me['y']))

                # Order list of all locations
                for n in range(len(lst1)):
                    lst1[n] = util.unHash(lst1[n])
                self.global_resources = lst1
                self.local_resources = lst2

            if self.me['turn'] == 3:
                self.me['health'] = 1000
                for bot in self.get_visible_robots():
                    if bot.castle_talk > 0:
                        temp = self.castleLoc[bot['id']]
                        self.castleLoc[bot['id']] = (bot.castle_talk - 192, self.castleLoc[bot['id']][1])

                for k in self.castleLoc.keys():
                    self.castles.append(k)
                    self.numCastles += 1

            self.log("TURN: " + str(self.me['turn']))
            # self.log("the map is "+ nav.symmetric(self.map))
            my_coord = (self.me['x'], self.me['y'])

            if self.me['turn'] < 3:
                # Send location over castleTalk to other castles
                if self.me['turn'] == 1:
                    self.castle_talk(self.me['y'] + 192)
                    self.log("Sending Y loc: " + str(self.me['y'] + 192))
                    for bot in self.get_visible_robots():
                        if bot.castle_talk > 0:
                            self.turnPos += 1
                            self.castleLoc[bot['id']] = (-1, bot.castle_talk - 192)
                elif self.me['turn'] == 2:
                    self.castle_talk(self.me['x'] + 192)
                    self.log("Sending X loc: " + str(self.me['x'] + 192))
                    for bot in self.get_visible_robots():
                        if bot.castle_talk > 0:
                            if bot['id'] in self.castleLoc.keys():
                                temp = self.castleLoc[bot['id']]
                                self.castleLoc[bot['id']] = (bot.castle_talk - 192, self.castleLoc[bot['id']][1])
                            else:
                                self.castleLoc[bot['id']] = (-1, bot.castle_talk - 192)

                if not self.resources_sphere:
                    karbonite_map=self.get_karbonite_map()
                    fuel_map=self.get_fuel_map()
                    self.resources_sphere=nav.get_closest_resources(self.log,my_coord,self.map,karbonite_map,fuel_map)
                    self.log(self.resources_sphere)
                if self.me['turn']==1 and self.turnPos == 0:
                    #builds and send a pilgrim to its target first turn
                    targetX, targetY = self.resources_sphere[self.pilgrims_built]
                    targetX = str(targetX); targetY = str(targetY)
                    if self.fuel >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_FUEL']+2 and self.karbonite >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_KARBONITE']:
                        self.log("Sending to target: (" + targetX + ", " + targetY + ")")
                        # self.signal(int("" + str(len(targetX)) + targetX + targetY),4)
                        signal = self.local_resources[self.pilgrims_built]
                        for bot in self.get_visible_robots():
                            if bot['castle_talk'] > 0 and bot['castle_talk'] < 192:
                                self.filled_resources[self.global_resources[bot['castle_talk'] - 1]] = 1

                        i = 0
                        while signal in self.filled_resources:
                            signal = self.local_resources[self.pilgrims_built + i]
                            i = i + 1

                        self.signal(util.nodeHash(*signal) + 57471, 4)

                        self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                        goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                        self.pilgrims_built=self.pilgrims_built+1
                        return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
                if self.me['turn']==2 and self.turnPos == 0:
                    #builds and send a pilgrim to its target first turn
                    targetX, targetY = self.resources_sphere[self.pilgrims_built]
                    targetX = str(targetX); targetY = str(targetY)
                    if self.fuel >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_FUEL']+2 and self.karbonite >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_KARBONITE']:
                        self.log("Sending to target: (" + targetX + ", " + targetY + ")")
                        # self.signal(int("" + str(len(targetX)) + targetX + targetY),4)
                        signal = self.local_resources[self.pilgrims_built]
                        for bot in self.get_visible_robots():
                            if bot['castle_talk'] > 0 and bot['castle_talk'] < 192:
                                self.filled_resources[self.global_resources[bot['castle_talk'] - 1]] = 1

                        i = 0
                        while signal in self.filled_resources:
                            signal = self.local_resources[self.pilgrims_built + i]
                            i = i + 1

                        self.signal(util.nodeHash(*signal) + 57471, 4)

                        self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                        goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                        self.pilgrims_built=self.pilgrims_built+1
                        return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
            
            if self.me['turn']==3 and self.turnPos == 0:
                # self.log("Turn Pos: " + self.turnPos)
                # self.log("Castle Loc: " + str(self.castleLoc))
                self.log("Building a Prophet")
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                return self.build_unit(SPECS['PROPHET'], goal_dir[0], goal_dir[1])


            # if self.build_guard and self.attempt==0:
            #     signal = self.local_resources[self.pilgrims_built-1]
            #     # target=nav.reflect(self.map, target, nav.symmetric(self.map))
            #     self.guard_build_loc=signal
            #     if self.karbonite<20 or self.fuel<50:
            #         self.attempt=self.attempt+1
            #         return
            #     self.signal(util.nodeHash(*signal) + 57471, 4)
            #     self.log("Building a Crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
            #     goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #     self.build_guard=False
            #     return self.build_unit(SPECS['CRUSADER'], goal_dir[0], goal_dir[1])

            # if self.build_guard:
            #     if self.karbonite<20 or self.fuel<50:
            #         self.attempt=self.attempt+1
            #         return
            #     self.attempt=0
            #     signal = self.local_resources[self.pilgrims_built-1]
            #     self.signal(util.nodeHash(*signal) + 57471, 4)
            #     self.log("Building a Crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
            #     goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #     self.build_guard=False
            #     return self.build_unit(SPECS['CRUSADER'], goal_dir[0], goal_dir[1])


            if self.me['turn']<25 and self.karbonite>=30:
                # targetX, targetY = self.resources_sphere[self.pilgrims_built]
                # targetX = str(targetX); targetY = str(targetY)
                if self.fuel >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_FUEL']+202 and self.karbonite >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_KARBONITE']:

                    # self.log("Sending to target: (" + targetX + ", " + targetY + ")")
                    # self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                    signal = self.local_resources[self.pilgrims_built]
                    for bot in self.get_visible_robots():
                        if bot['castle_talk'] > 0 and bot['castle_talk'] < 192:
                            self.filled_resources[self.global_resources[bot['castle_talk'] - 1]] = 1

                    i = 0
                    while signal in self.filled_resources:
                        signal = self.local_resources[self.pilgrims_built + i]
                        i = i + 1

                    self.signal(util.nodeHash(*signal) + 57471, 4)

                    self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                    goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                    self.pilgrims_built=self.pilgrims_built+1
                    symmetric=nav.symmetric(self.get_passable_map())
                    self.log('this is a horizontal map:'+symmetric)
                    if symmetric:
                        x=signal[1]
                    else:
                        x=signal[0]
                    if x>=len(self.get_passable_map())/2:
                        self.build_guard=True
                    return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])

            if self.me['turn']<45:
                signal = self.local_resources[self.pilgrims_built]
                self.signal(util.nodeHash(*signal) + 57471, 2)
                self.log("Building a Crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                return self.build_unit(SPECS['CRUSADER'], goal_dir[0], goal_dir[1])


 

        
        elif self.me['unit']==SPECS['PILGRIM']:
            self.log('Happy Thanksgiving!')
            my_loc = (self.me['x'], self.me['y'])
            moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            # self.log("Progress: " + str(self.progress))

            #getting first turn target from castle
            if self.me['turn'] == 1:
                # Map Building
                # fuelMap = self.fuel_map
                self.local_resources = -1
                self.homePath = my_loc
                self.closest_dropoff = my_loc

                lst1 = []
                for i in range(self.get_fuel_map()):
                    for k in range(self.get_fuel_map()):
                        if self.get_fuel_map()[i][k] or self.get_karbonite_map()[i][k]:
                            lst1.append(util.nodeHash(k,i))
                util.insertionSort(self.log, lst1)

                # Order list of all locations
                for n in range(len(lst1)):
                    lst1[n] = util.unHash(lst1[n])
                self.global_resources = lst1

                # Read Signal!
                for botv in self.get_visible_robots():
                    if not self.is_visible(botv):
                        continue
                    if self.is_radioing(botv) and (botv['unit'] == SPECS["CASTLE"] or botv['unit'] == SPECS["CHURCH"]):
                        self.target = util.unHash(botv['signal'] - 57471)
                        # based on target in relation

                for n in range(len(self.global_resources)):
                    if self.global_resources[n] == self.target:
                        self.local_resources = n
                        break

            self.log("Castle Talk: " + str(self.local_resources))

            self.castle_talk(self.local_resources + 1)

            self.log("Target: " + str(self.target) + ", Current Loc: " + str(my_loc))

            karbMiner = self.get_karbonite_map()[self.target[1]][self.target[0]]
            # self.log("TARGET: " + self.target)
            # self.log("karbMiner: " + str(karbMiner))
            drop_off = False
            for botv in self.get_visible_robots():
                if not self.is_visible(botv):
                    continue
                if botv['unit'] == SPECS['CASTLE'] or botv['unit'] == SPECS['CHURCH']:
                    if botv['team'] != self.me['team']:
                        continue
                    for giving in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if util.nodeHash(giving[0]+self.me['x'], giving[1]+self.me['y']) == util.nodeHash(botv['x'],botv['y']):
                            drop_off = True
                            break;

                if drop_off:
                    break

            if karbMiner:
                energy = 'karbonite'
                capacity = SPECS['UNITS'][SPECS['PILGRIM']]['KARBONITE_CAPACITY']
            else:
                energy = 'fuel'
                capacity = SPECS['UNITS'][SPECS['PILGRIM']]['FUEL_CAPACITY']


            if self.me[energy]<capacity:
                #if not full and at target and shouldnt build church, mining. Actually if at target and still havent built church 
                #should not be trying to build church


                if my_loc[0]==self.target[0] and my_loc[1]==self.target[1]:
                    self.log('Mining')
                    # self.progress = 1e10
                    return self.mine()
                #so the bot isnt at the target so it must be moving, either dropping off or going to build a church to dropoff
                if nav.distance(self.target,my_loc) < 100:
                    taken=nav.resource_occupied(self,SPECS,self.me,my_loc,self.target,self.get_visible_robots())
                    # self.log("Taken: " + taken)
                    if taken:
                        if self.attempt<1:
                            self.log('I am attempting to find a new resource')
                            self.closest_resources=nav.get_closest_resources_pilgrim(self.log,my_loc,self.get_visible_robot_map(),self.get_passable_map(),self.get_fuel_map(),self.get_karbonite_map())
                        self.attempt=self.attempt+1
                        self.target=self.closest_resources[self.attempt]
                        self.log('attempt '+self.attempt+'now trying to move to'+self.target)

                self.log("Moving!")
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.target), moves)
                # self.log("Path: " + str(path))
                # if self.progress > util.euclidianDistance(my_loc, self.target):
                        # self.progress = util.euclidianDistance(my_loc, self.target)
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                self.log("Action: " + str(action[0]) + ", " + str(action[1]))
                self.log(action)
                return self.move(action[0],action[1])

            #so now we know the tank is full
            else:
                self.log('well this is problematic')
                if drop_off==True:
                    self.log('what is going on')
                    #so the bot can drop off so it should and keep going with its life
                    self.dropping_off=False
                    # self.progress = 1e10
                    return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], self.me['karbonite'], self.me['fuel'])
                # #sadly he cannot dropoff
                elif self.dropping_off==True and self.should_build_church==False:
                    self.closest_dropoff=nav.get_closest_dropoff(self,self.get_visible_robots(),self.homePath)
                    self.log('back to moving 2')
                    if self.progress > util.euclidianDistance(my_loc, self.closest_dropoff):
                        self.progress = util.euclidianDistance(my_loc, self.closest_dropoff)
                    path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    self.log('the path i am trying to take is '+path[1].x+','+path[1].y)
                    return self.move(*action)
                
                else:
                    self.log('im trying bob')
                    #checking to see if we should build a church  
                    karb=self.karbonite
                    fuel=self.fuel
                    self.should_build_church=nav.church_or_no(self,my_loc,self.map,self.get_visible_robots(),karb,fuel)

                    self.log('should i build a church'+self.should_build_church)
                    if not self.should_build_church:
                        self.log('this is funs')
                        self.closest_dropoff=nav.get_closest_dropoff(self,self.get_visible_robots(),self.homePath)
                    if self.should_build_church:
                        self.log('whoops')
                        #we should build a church so get a good build location
                        self.build_site=nav.church_build_site(self,SPECS,self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map(),self.get_visible_robot_map())
                        self.closest_dropoff=self.build_site
                        self.log('im trying to build at '+self.build_site)
                        #now check if we are close to the build site
                        if (abs(my_loc[0]-self.build_site[0])<2) and (abs(my_loc[1]-self.build_site[1])<2):
                            #so we can and should build
                            self.log('lets see how far we get  trying to build at '+self.build_site)
                            return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])
                        #we arent close, so we must move to the closest dropoff site (this only works because pilgrims only take steps of one)
                #so no matter what, even if were not building a church, we want to move to the dropoff site
                self.dropping_off=True
                self.log('back to moving')
                # if self.progress > util.euclidianDistance(my_loc, self.closest_dropoff):
                #         self.progress = util.euclidianDistance(my_loc, self.closest_dropoff)
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
                self.log("PATH: " + str(path))
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                return self.move(*action)



        elif self.me['unit']==SPECS['CHURCH']:
            my_coord = (self.me['x'], self.me['y'])
            my_loc=self.me['x'],self.me['y']
            if self.me['turn']%3==0:
                self.log('Building a Prophet')
                goal_dir=nav.spawn(my_coord, self.get_passable_map(), self.get_visible_robot_map())
                return self.build_unit(SPECS['PROPHET'], goal_dir[0], goal_dir[1])

          

            
robot = MyRobot()
