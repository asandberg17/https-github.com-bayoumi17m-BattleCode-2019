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

    defense = True
    has_moved=False
    squad=False
    guard=False
    # Make parent the id of the Castle or centroid bot
    defense_fields = {'parent' : None, 'level': 1, 'state': 'FOLLOW', 'branch': 0, 'branch_type': 'active', 'length': util.crossLength()}
    defending = False
    moved=0
    castle_loc = (0,0)
    blocked_spots = {}

    pilgrims_built=0
    closest_resources=[]

    karboniteMining = True
    attempt=0

    wave = []
    should_build_church=False
    build_site=(0,0)
    homePath = (0,0)
    closest_dropoff=(0,0)
    target=(0,0)
    dropping_off=False
    mapSize = 0

    progress = 1e10

    already_been = {}
    base = None
    destination = None

    def turn(self):
        # self.log(str(self.me))
        # size = len(self.get_passable_map())
        # map_pass = self.get_passable_map()
        # maps = "["
        # for i in range(size):
        #     maps = maps +"["
        #     for k in range(size):
        #         if map_pass[i][k]:
        #             maps = maps + "0"
        #         else:
        #             maps = maps + "1"
        #         if k != size - 1:
        #             maps = maps + ","
        #     maps = maps + "]"
        #     if i != size - 1:
        #             maps = maps + ","

        # self.log(maps + "]")


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
                if r['unit'] == SPECS['CASTLE'] and self.me['team'] == r['team']:
                    self.castle_loc = (r['x'],r['y'])

                if self.me['turn'] == 1:
                    if r['unit'] == SPECS['PROPHET']:
                        type_seen += 1


                # if self.destination:
                #     # self.log("Our destination is: " + str(self.destination) + " and bot is at: " + str((r['x'],r['y'])))
                #     if self.destination[0] == r['x'] and self.destination[1] == r['y']:
                #         self.destination = defense.hilbert_defense(self.log, my_coord, self.castle_loc, nav.symmetric(fuel_map), self.get_visible_robot_map(), full_map, fuel_map, karbonite_map, SPECS['PROPHET'], self.me['team'], SPECS)
                    

                        # self.log("Adding bot to blocked")
                        # self.blocked_spots[self.destination] = 1

                # if not self.destination is None:
                #     # self.log("BOOM CHICKA BOW WOW")
                #     if (r['x'],r['y']) == self.destination:
                #         if util.euclidianDistance((self.me['x'],self.me['y']),self.destination) <= 5:
                #             self.destination, self.defense_fields = nav.defense_2(self.log, self.get_passable_map(), castle_loc, in_vision, self.defense_fields)

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

            # self.log("DESTINATION is blocked: " + str(self.destination in self.blocked_spots) + " at " + str(self.destination))

            # if self.destination in self.blocked_spots:
            #     self.destination = defense.hilbert_defense(self.log, my_coord, self.castle_loc, nav.symmetric(fuel_map), self.get_visible_robot_map(), full_map, fuel_map, karbonite_map, SPECS['PROPHET'], self.me['team'], SPECS, self.blocked_spots)
            #     self.log("Castle Loc is: " + str(self.castle_loc) + " and my new destination is: " + str(self.destination))
                # self.blocked_spots = {}


            if my_coord[0]==self.destination[0] and my_coord[1]==self.destination[1]:
                self.log("CURRENTLY STANDING AT "+my_coord)
                self.log("DEFENDING MY DESTINATION AT "+self.destination)
                self.blocked_spots = {}
                self.defending = True
                return

            self.log("Trying to move to "+ self.destination)
            path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
            action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
            #return self.move(*nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been))
            self.log(action)
            return self.move(*action)



            
        if self.me['unit'] == SPECS['CRUSADER']:
            self.log("Crusader health: " + str(self.me['health'])) 

            if self.me['turn'] == 1:
                self.homePath = (self.me['x'],self.me['y'])

            visible = self.get_visible_robots()
            # moves = [(-4, 0), (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2), (-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3), (-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (1, 3), (2, -3), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (2, 3), (3, -2), (3, -1), (3, 0), (3, 1), (3, 2), (4, 0)]
            moves = []
            for i in range(-4,5):
                for k in range(-4,5):
                    if i**2 + k**2 <= SPECS['UNITS'][SPECS['CRUSADER']]['SPEED']:
                        moves.append((i,k))

            if self.me['turn'] == 1:
                self.homePath = (self.me['x'],self.me['y'])

            # get attackable robots
            attackable = []
            signal = -1
            for r in visible:
                if self.is_radioing(r) and self.is_visible(r) and r['unit'] == SPECS['CASTLE']:
                    self.log('something is happening')
                    self.log("Recieving Signal: " + str(r.signal))
                    signal = r['signal']
                # x = 5
                if not self.is_visible(r):
                    # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
                    continue
                # now all in vision range, can see x, y etc
                dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
                if r['team'] != self.me['team'] and SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][0] <= dist <= SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][1]:
                    attackable.append(r)

            if attackable:
                # attack first robot
                r = attackable[0]
                if r['unit'] == SPECS['CASTLE']:
                    self.castleBeaten = True
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])

            my_coord = (self.me['x'], self.me['y'])   
            
            if not self.destination:
                # self.log("trying to move")
                if signal != -1:
                    self.log('receiving a signal')
                    destination = util.unHash(signal)
                    self.squad=True
                # else:
                    destination = my_coord
                    self.destination = nav.reflect(self.map, destination, nav.symmetric(self.map))

            # self.log("Signal: " + str(signal))
            # if signal >= 0:
            #     self.destination = nav.reflect(self.map, util.unHash(signal), nav.symmetric(self.map))

            self.log("My destination is " + self.destination)
            if (self.destination[0]-my_coord[0])**2 + (self.destination[1]-my_coord[1])**2 < 2 and self.guard==True:
                self.log('defending the pilgrims')
                return
            if (self.destination[0]-my_coord[0])**2 + (self.destination[1]-my_coord[1])**2 < 10 and self.guard==False:
                self.log("Holding my ground")
                self.destination = self.homePath # Change to next castle
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                if self.castleBeaten: 
                    self.castle_talk(111)
                return self.move(*action)
                # return
            if self.moved<4 and self.fuel>5:
                self.log('just a little closer')
                # destination = my_coord
                self.moved=self.moved+1
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                # self.log("Path length: " + str(len(path)))
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                return self.move(*action)
            if self.squad != True:
                self.squad=nav.homies(self,SPECS,my_coord,self.get_visible_robots(),self.me['team'])
            if self.squad==True:
                path = nav.astar(self.log, self.is_visible, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                # self.log("Cost: " + str((action[0]**2 + action[1]**2)*SPECS['UNITS'][SPECS['CRUSADER']]['FUEL_PER_MOVE']))
                # self.log("Fuel: " + str(self.fuel))
                return self.move(*action)
            else:
                self.log('Waiting for my squad')

               
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
            # if self.coolDown > 0:
            #     self.coolDown -= 1

            # attacker_return = False
            # if self.me['turn'] >= 3:
            #     terminated = False
            #     for bot in self.get_visible_robots():
            #         if self.is_visible(bot):
            #             if bot['unit'] == SPECS['CRUSADER'] or bot['unit'] == SPECS['PREACHER']:
            #                 attacker_return = True
            #         if bot.castle_talk == 111:
            #             self.log("terminated message")
            #             if attacker_return:
            #                 terminated = True
            #             self.coolDown = 30
            #             break
            #     if terminated:
            #         self.castles.pop(0)

            if self.me['turn'] == 3:
                self.me['health'] = 1000
                for bot in self.get_visible_robots():
                    if bot.castle_talk > 0:
                        temp = self.castleLoc[bot['id']]
                        self.castleLoc[bot['id']] = (bot.castle_talk - 192, self.castleLoc[bot['id']][1])

                for k in self.castleLoc.keys():
                    self.castles.append(k)
                    self.numCastles += 1


            # self.log("WICKED IMPORTANT: " + self.castles)
            # self.log("DOUBLE IMPORTANT: " + str(self.castleLoc))



            self.log("TURN: " + str(self.me['turn']))
            # self.log("the map is "+ nav.symmetric(self.map))
            my_coord = (self.me['x'], self.me['y'])
            # self.log(str(SPECS['UNITS'][SPECS['CRUSADER']]))

            # if self.castles != [] and self.me['turn'] % 30 != 0: # Why was this condition added?
            #     attack_castle = self.castleLoc[self.castles[0]]
            #     # self.log(str(attack_castle))
            #     # self.signal(int(util.nodeHash(*attack_castle)),10)
            # else:
            #     pass
                # self.log("HOW DID THIS HAPPEN!!")

            # self.log(str(self.numCastles))
            # self.log(str(self.castles))

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
                        self.signal(int("" + str(len(targetX)) + targetX + targetY),4)

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
                        self.signal(int("" + str(len(targetX)) + targetX + targetY),4)

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
            # if self.me['turn']<10:
            #     self.log("Building a Prophet")
            #     goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #     return self.build_unit(SPECS['PROPHET'], goal_dir[0], goal_dir[1])

            if self.build_guard and self.attempt==0:
                targetX, targetY = self.resources_sphere[self.pilgrims_built-1]
                targetX = str(targetX); targetY = str(targetY)
                target=(targetX,targetY)
                # target=nav.reflect(self.map, target, nav.symmetric(self.map))
                self.guard_build_loc=target
                if self.karbonite<20 or self.fuel<50:
                    self.attempt=self.attempt+1
                    return
                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                self.log("Building a Crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.build_guard=False
                return self.build_unit(SPECS['CRUSADER'], goal_dir[0], goal_dir[1])

            if self.build_guard:
                if self.karbonite<20 or self.fuel<50:
                    self.attempt=self.attempt+1
                    return
                self.attempt=0
                targetX=self.guard_build_loc[0]
                targetY=self.guard_build_loc[1]
                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                self.log("Building a Crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.build_guard=False
                return self.build_unit(SPECS['CRUSADER'], goal_dir[0], goal_dir[1])


            if self.pilgrims_built<len(self.resources_sphere) and self.me['turn']<25:# and self.me['turn'] % 2 == 0:
                targetX, targetY = self.resources_sphere[self.pilgrims_built]
                targetX = str(targetX); targetY = str(targetY)
                if self.fuel >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_FUEL']+2 and self.karbonite >= SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_KARBONITE']:

                    self.log("Sending to target: (" + targetX + ", " + targetY + ")")
                    self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                    dist=nav.sq_dist(my_coord,(targetX,targetY))
                    if dist>10:
                        self.build_guard=True

                    self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                    goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                    self.pilgrims_built=self.pilgrims_built+1
                    return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])

            # if self.me['turn']<100:
            #     if self.karbonite>20:
            #         if self.pilgrim==True and self.pilgrims_built<len(self.resources_sphere):
            #             targetX, targetY = self.resources_sphere[self.pilgrims_built]
            #             targetX = str(targetX); targetY = str(targetY)
            #             self.signal(int("" + str(len(targetX)) + targetX + targetY),2)

            #             self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
            #             goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #             self.pilgrims_built=self.pilgrims_built+1
            #             return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
            #         else:
            #             self.log('Building a Crusader')
            #             goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #             return self.build_unit(SPECS['CRUSADER'], goal_dir[0], goal_dir[1])
            # if self.me['turn']<450:
            #     if self.me['turn']%3==0:
            #         self.log('Building a Prophet')
            #         goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #         return self.build_unit(SPECS['PROPHET'], goal_dir[0], goal_dir[1])
            # elif self.me['turn'] < 30:


            #         # self.log(str(self.castleLoc))
            #         # self.log(str(self.castles))

            #         # self.log(str(self.castleLoc))

            #     goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #     self.log(self.me['turn'])

            #     if self.fuel > SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_FUEL'] and self.karbonite > SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_KARBONITE']:
            #         self.log("Building a Prophet at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
            #         return self.build_unit(SPECS['PROPHET'], goal_dir[0],goal_dir[1])

            # elif self.me['turn'] < 150:

            #     self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
            #     if not self.resources_sphere:
            #         karbonite_map=self.get_karbonite_map()
            #         fuel_map=self.get_fuel_map()
            #         self.resources_sphere=nav.get_closest_resources(self.log,my_coord,self.map,karbonite_map,fuel_map)
            #         self.log(self.resources_sphere)
                
            #     self.log("Sphere of influence: " + str(self.resources_sphere))
            #     self.log("Pilgrims built: " + self.pilgrims_built)

            #     #sending pilgrim its target
            #     if self.pilgrims_built < len(self.resources_sphere):
            #         self.log("Pilgrims built: " + self.pilgrims_built)
            #         targetX, targetY = self.resources_sphere[self.pilgrims_built]
            #         targetX = str(targetX); targetY = str(targetY)
            #         self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
            #         # self.log("Signal sent is: " + str(len(targetX)) + targetX + targetY)

            #         # self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
            #         goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #         self.log("Goal Dir: " + str(goal_dir))
            #         if self.fuel > SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_FUEL'] and self.fuel > SPECS['UNITS'][SPECS['PILGRIM']]['CONSTRUCTION_KARBONITE']:
            #             # self.log("Pilgrims: " + str(self.pilgrims_built) + " plus 1: " + str(self.pilgrims_built + 1))
            #             self.pilgrims_built = self.pilgrims_built + 1
            #             return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])

            # elif self.me['turn'] % 3 == 0:
            #     goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #     # self.log(self.me['turn'])
            #     if self.fuel > self.numCastles*SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_KARBONITE']:
            #         self.log("Building a Prophet at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
            #         return self.build_unit(SPECS['PROPHET'], goal_dir[0],goal_dir[1])

            # elif self.me['turn'] % 2 == 0:
            #     goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
            #     # self.log(self.me['turn'])
            #     if random.random() <= 0.6 and self.fuel > self.numCastles*SPECS['UNITS'][SPECS['CRUSADER']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['CRUSADER']]['CONSTRUCTION_KARBONITE']:
            #         self.log("Building a Crusader at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
            #         return self.build_unit(SPECS['CRUSADER'], goal_dir[0],goal_dir[1])
            #     elif self.fuel > self.numCastles*SPECS['UNITS'][SPECS['PREACHER']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['PREACHER']]['CONSTRUCTION_KARBONITE']:
            #         self.log("Building a Preacher at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
            #         return self.build_unit(SPECS['PREACHER'], goal_dir[0],goal_dir[1])

        
        elif self.me['unit']==SPECS['PILGRIM']:
            self.log('Happy Thanksgiving!')
            my_loc = (self.me['x'], self.me['y'])
            moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            # self.log("Progress: " + str(self.progress))

            #getting first turn target from castle
            if self.me['turn'] == 1:
                # Map Building
                # fuelMap = self.fuel_map
                self.homePath = my_loc
                self.closest_dropoff = my_loc

                # Read Signal!
                signal = ""
                for botv in self.get_visible_robots():
                    if not self.is_visible(botv):
                        continue
                    if self.is_radioing(botv) and (botv['unit'] == SPECS["CASTLE"] or botv['unit'] == SPECS["CHURCH"]):
                        signal = str(botv['signal'])
                        break

                parsePoint = int(signal[0])
                y = int(signal[parsePoint+1:])
                x = int(signal[1:parsePoint+1])
                self.log("Signal is: " + signal + " and target is: " + str((x,y)))

                # self.wave[y][x] = 2
                self.target=(x,y)
                # self.progress = util.euclidianDistance(self.target,my_loc)
                # self.log("The target is: " + str((self.targetX,self.targetY)))

                # moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                # path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, self.target, moves)
                # self.log("Path: " + str(path))
                # # for node in path:
                # #     self.log("Path " + str((node.x,node.y)))
                # # action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                # # self.log("Trying to move by: " + str(action) + " from " + str((self.me['x'],self.me['y'])))
                # # return self.move(*action)


            #checking if it is possible to dropoff
            # if self.me['turn'] > 1:
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
                    self.log("Taken: " + taken)
                    if taken:
                        if self.attempt<1:
                            self.log('I am attempting to find a new resource')
                            self.closest_resources=nav.get_closest_resources_pilgrim(self.log,my_loc,self.get_visible_robot_map(),self.get_passable_map(),self.get_fuel_map(),self.get_karbonite_map())
                        self.attempt=self.attempt+1
                        self.target=self.closest_resources[self.attempt]
                        self.log('attempt '+self.attempt+'now trying to move to'+self.target)



                        # self.log("Test_val: " + str(test_val))

                # if self.dropping_off==True:
                #     if self.should_build_church==True:
                #         if (my_loc[0]-self.build_site[0])**2 + (my_loc[1]-self.build_site[1])**2 <= 2:
                #             #check once more if the church has to be built
                #             karb=self.karbonite
                #             fuel=self.fuel
                #             self.should_build_church=nav.church_or_no(self,my_loc,self.map,self.get_visible_robots(),karb,fuel)
                #             #now build the church if possible
                #             if  self.should_build_church:
                #                 #now free to build church
                #                 return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1]) # Fixed to build only when adjacent!
                #             #it shouldnt build the church anymore so now there is a church in range it should go there
                #             self.closest_dropoff=nav.get_closest_dropoff(self,self.get_visible_robots(),self.homePath)
                #             path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
                #             action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                #             return self.move(*action)
                #so it must not be dropping off and it must be moving to the target
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
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                return self.move(*action)



        # elif self.me['unit']==SPECS['CHURCH']:
        #     my_loc=self.me['x'],self.me['y']
        #     if self.me['turn']<100:
        #         robot_map=self.get_visible_robot_map()
        #         self.resources_sphere=nav.get_closest_resources_church(self.log,my_loc,robot_map,self.get_passable_map(),self.get_fuel_map(),self.get_karbonite_map())
        #         self.log('length of resources sphere is '+len(self.resources_sphere))
        #         if self.pilgrims_built<len(self.resources_sphere):
        #             targetX, targetY = self.resources_sphere[self.pilgrims_built]
        #             targetX = str(targetX); targetY = str(targetY)
        #             self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
        #             self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
        #             goal_dir=nav.spawn(my_loc, self.map, self.get_visible_robot_map())
        #             self.pilgrims_built=self.pilgrims_built+1
        #             return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
          




                                
                                






        # # elif self.me['unit'] == SPECS['PILGRIM']:
        # #     self.log("Let us feast with the Indians")
        # #     self.log('karbonite:'+self.karbonite)
        # #     self.log('Fuel:'+self.fuel)
        # #     # self.log('I should build a church:'+self.should_build_church)
        # #     my_loc=(self.me['x'],self.me['y'])
        # #     if self.me['turn'] == 1:
        # #         # Map Building
        # #         # fuelMap = self.fuel_map
        # #         self.homePath = my_loc
        # #         self.closest_dropoff = my_loc

        # #         # Read Signal!
        # #         signal = ""
        # #         for botv in self.get_visible_robots():
        # #             if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
        # #                 signal = str(botv['signal'])
        # #                 break

        # #         parsePoint = int(signal[0])
        # #         y = int(signal[parsePoint+1:])
        # #         x = int(signal[1:parsePoint+1])
        # #         # self.log("Signal is: " + signal + " and target is: " + str((x,y)))

        # #         # self.wave[y][x] = 2
        # #         self.targetX = x
        # #         self.targetY = y
        # #         # self.log("The target is: " + str((self.targetX,self.targetY)))

        # #         moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # #         path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.target), moves)
        # #         # for node in path:
        # #         #     self.log("Path " + str((node.x,node.y)))
        # #         action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        # #         # self.log("Trying to move by: " + str(action) + " from " + str((self.me['x'],self.me['y'])))
        # #         return self.move(*action)

        # #     if self.me['turn'] > 1:

        # #         karbMiner = self.get_karbonite_map()[self.target[1]][self.target[0]]
        # #         # self.log("karbMiner: " + str(karbMiner))
        # #         drop_off = False
        # #         for botv in self.get_visible_robots():
        # #             if botv['unit'] == SPECS['CASTLE'] or botv['unit'] == SPECS['CHURCH']:
        # #                 for giving in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        # #                     if util.nodeHash(giving[0]+self.me['x'], giving[1]+self.me['y']) == util.nodeHash(botv['x'],botv['y']):
        # #                         drop_off = True
        # #                         break;

        # #             if drop_off:
        # #                 break

        # #         if karbMiner:
        # #             energy = 'karbonite'
        # #             capacity = SPECS['UNITS'][SPECS['PILGRIM']]['KARBONITE_CAPACITY']
        # #         else:
        # #             energy = 'fuel'
        # #             capacity = SPECS['UNITS'][SPECS['PILGRIM']]['FUEL_CAPACITY']

        # #         # botv_pos = []
        # #         # for botv in self.get_visible_robots():
        # #         #     botv_pos.append(util.nodeHash(botv.x,botv.y))
                    
        # #         if util.nodeHash(self.me['x'],self.me['y']) == util.nodeHash(self.targetX,self.targetY) and self.me[energy] < capacity:
        # #             self.log("MINING")
        # #             # self.log(energy + " " + str(self.me[energy]) + "/" + str(capacity))
        # #             visible=self.get_visible_robots()
        # #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        # #             return self.mine()
                
        # #         elif self.should_build_church and not self.build_site[0]-my_loc[0]<2 and not self.build_site[1]-my_loc[1]<2:
        # #             # This is always False unless the self.build_site attribute is to the lower right of pilgrim location! 
        # #             # This is because the value will only be greater than two is the location is > 2 to the lower right diagonal (or 8r^2)
        # #             self.log('checking if a church is necessary')
        # #             #check if a church is still necessary
        # #             visible=self.get_visible_robots()
        # #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        # #             if not self.should_build_church:
        # #                 #now there is a church in range and it should go there
        # #                 self.closest_dropoff=nav.get_closest_dropoff(self,visible)
        # #             #now move to where the dropoff point should be
        # #             path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)

        # #         elif self.should_build_church and self.build_site[0]-my_loc[0]<2 and self.build_site[1]-my_loc[1]<2:
        # #             self.log('we have moved closed enough to build the church')
        # #             #check if a church is still necessary
        # #             visible=self.get_visible_robots()
        # #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        # #             if not self.should_build_church:
        # #                 #now there is a church in range and it should go there
        # #                 self.closest_dropoff=nav.get_closest_dropoff(self,visible)
        # #                 path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
        # #                 action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        # #                 return self.move(*action)

        # #             #now it should build the church
        # #             self.should_build_church=False  
        # #             self.build_site=nav.church_build_site(self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map())
        # #             self.closest_dropoff=self.build_site
        # #             self.log("trying to build a church at "+self.build_site)
        # #             return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])

        # #         elif self.me[energy] < capacity and util.nodeHash(self.me['x'],self.me['y']) != util.nodeHash(self.targetX,self.targetY):
        # #             self.log("Moving!!!")
        # #             moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # #             path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.targetX,self.targetY), moves)
        # #             action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        # #             return self.move(*action)


        # #         #FOR SOME REASON THIS WAS NOT ASSIGNING THINGS WELL
        # #         elif self.me[energy] == capacity and util.nodeHash(*self.closest_dropoff) != util.nodeHash(*my_loc) and not drop_off:
        # #             self.log('I got this far! Im full')
        # #             # self.log("WORKING LOOP")
        # #             visible = self.get_visible_robots()
        # #             moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        # #             self.log('Maybe a church now:'+self.should_build_church)
        # #             if self.should_build_church:
        # #                 self.log('here2')
        # #                 self.build_site=nav.church_build_site(self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map())
        # #                 self.log('my build site is'+self.build_site)
        # #                 self.closest_dropoff=self.build_site
        # #             if self.should_build_church and self.build_site[0]-my_loc[0]<2 and self.build_site[1]-my_loc[1]<2:
        # #                 self.log("trying to build a church at "+self.build_site)
        # #                 return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])
                    

        # #             path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
        # #             action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        # #             return self.move(*action)


        # #         elif drop_off and self.me[energy] == capacity:
                    
        # #             return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], self.me['karbonite'], self.me['fuel'])
            
robot = MyRobot()
