from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
import nav
import util
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

    defense = True
    # Make parent the id of the Castle or centroid bot
    defense_fields = {'parent' : None, 'level': 1, 'state': 'FOLLOW', 'branch': 0, 'branch_type': 'active', 'length': util.crossLength()}
    defending = False

    pilgrims_built=0
    closest_resources=[]

    karboniteMining = True

    wave = []
    should_build_church=False
    build_site=(0,0)
    homePath = (0,0)
    closest_dropoff=(0,0)
    target=(0,0)
    dropping_off=False
    visited = []
    mapSize = 0

    already_been = {}
    base = None
    destination = None

    def turn(self):
        # self.log(str(self.me))
        if self.me['unit'] == SPECS['PROPHET']:
            self.log("Prophet health: " + str(self.me['health']))
            attack_order = {SPECS['PREACHER']: 1, SPECS['CRUSADER']: 3, SPECS['PROPHET']: 2}

            visible = self.get_visible_robots()

            # get attackable robots
            attackable = []
            castle_loc = (-1,-1)
            in_vision = []

            for r in visible:
                # x = 5
                if not self.is_visible(r):
                    # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
                    continue
                # now all in vision range, can see x, y etc
                if r['unit'] == SPECS['CASTLE'] and self.me['team'] == r['team']:
                    castle_loc = (r['x'],r['y'])

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
                if castle_loc == (-1,-1):
                    self.destination = nav.defense(self.get_passable_map(), self.get_visible_robot_map(), my_coord)
                else:
                    self.log("Found Castle")
                    # self.destination = nav.defense(self.get_passable_map(), self.get_visible_robot_map(), my_coord)
                    self.destination = nav.defense_2(self.log, self.get_passable_map(), castle_loc, in_vision, self.defense_fields) 

            if my_coord[0]==self.destination[0] and my_coord[1]==self.destination[1]:
                self.log("CURRENTLY STANDING AT "+my_coord)
                self.log("DEFENDING MY DESTINATION AT "+self.destination)
                self.defending = True
                return
            self.log("Trying to move to "+ self.destination)
            path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
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
                    self.log("Recieving Signal: " + str(r.signal))
                    signal = r.signal
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
                path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                if self.castleBeaten: 
                    self.castle_talk(111)
                return self.move(*action)
                # return


            path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)

            action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
            # self.log("Cost: " + str((action[0]**2 + action[1]**2)*SPECS['UNITS'][SPECS['CRUSADER']]['FUEL_PER_MOVE']))
            # self.log("Fuel: " + str(self.fuel))
            return self.move(*action)


            
            # # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
            # my_coord = (self.me['x'], self.me['y'])
            # self.already_been[my_coord] = True
            # # self.log(nav.symmetric(self.map)) #for some reason this would sometimes throw an error
            # # self.log("My destination is "+self.destination)
            # if not self.destination:
            #     self.log("trying to move")
            #     self.destination = nav.reflect(self.map, my_coord, nav.symmetric(self.map))
            # self.log("Trying to move to "+ self.destination)

            # goal_dir=nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been)
            # x=0
            # jump_dir=goal_dir
            # while x<2:
            #     loc=nav.apply_dir(my_coord,jump_dir)
            #     self.already_been[loc] = True
            #     goal_dir=nav.goto(loc, self.destination, self.map, self.get_visible_robot_map(), self.already_been)
            #     x=x+1
            #     jump_dir=jump_dir[0]+goal_dir[0],jump_dir[1]+goal_dir[1]

            # if jump_dir[0]**2+jump_dir[1]**2>9:
            #     self.log("not sure")
            #     jump_dir=jump_dir[0]-goal_dir[0],jump_dir[1]-goal_dir[1]
            #     if nav.symmetric(self.map):
            #         jump_dirh=jump_dirh[0],jump_dir[1]+1
            #         loc=nav.apply_dir(my_coord,jump_dir)
            #         self.log("hi")
            #         if jump_dirh[0]**2+jump_dirh[1]**2<9 and nav.is_passable(self.map,loc,jump_dirh,self.get_visible_robot_map()):
            #             return self.move(*jump_dirh[0],jump_dir[1]+1)
            #         else:
            #             return self.move(*jump_dir)
            #     else:
            #         jump_dirv=jump_dir[0]+1,jump_dir[1]
            #         loc=nav.apply_dir(my_coord,jump_dir)
            #         self.log("bye")
            #         if jump_dirv[0]**2+jump_dirv[1]**2<9 and nav.is_passable(self.map,loc,jump_dirv,self.get_visible_robot_map()):
            #             return self.move(*jump_dirv)
            #         else:
            #             return self.move(*jump_dir)

            # self.log("why")
            # loc=nav.apply_dir(my_coord,jump_dir)
            # self.log("this should not even be returning "+loc)
            # return self.move(*jump_dir)
            # goal_dir=nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been)
            # #return self.move(*nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been))
            # self.log(goal_dir)
            # return self.move(*goal_dir)
               
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

            if self.me['turn'] == 1:
                self.homePath = (self.me['x'], self.me['y'])

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
                r = nav.aiming((self.me['x'],self.me['y']), attackable, self.me['team'], SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][0], SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][1])
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r[0] - self.me['x'], r[1] - self.me['y'])

            my_coord = (self.me['x'], self.me['y'])    
            
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
                path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)
                self.log("Length of path: " + len(path))
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                return self.move(*action)
                # return


            path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), my_coord, self.destination, moves)

            action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
            # self.log("Cost: " + str((action[0]**2 + action[1]**2)*SPECS['UNITS'][SPECS['CRUSADER']]['FUEL_PER_MOVE']))
            # self.log("Fuel: " + str(self.fuel))
            return self.move(*action)

        elif self.me['unit'] == SPECS['CASTLE']:
            self.log("I AM A CASTLE HEAR ME ROAR")
            #initializing my coordinates
            my_coord = (self.me['x'], self.me['y'])
            if self.coolDown > 0:
                self.coolDown -= 1

            #checking if castle has not yet calculated closest resources
            # if len(closest_resources) == 0:
            #     self.closest_resources = nav.get_closest_resources(my_coord,self.map,self.get_visible_robot_map(),self.get_fuel_map(),self.get_karbonite_map())
            #this will return all the resources in range 10 of the castle and then two more. The castle will keep track of how many pilgrims
            #it sends and send them to the corresponding index of closest_resource until if it builds another pilgrim number of pilgrims 
            #sent would be greater than len(closest_resources)
            attacker_return = False
            if self.me['turn'] >= 3:
                terminated = False
                for bot in self.get_visible_robots():
                    if self.is_visible(bot):
                        if bot['unit'] == SPECS['CRUSADER'] or bot['unit'] == SPECS['PREACHER']:
                            attacker_return = True
                    if bot.castle_talk == 111 and self.coolDown == 0:
                        self.log("terminated")
                        terminated = True
                        self.coolDown = 30
                        break
                if terminated:
                    self.castles.pop(0)

            if self.me['turn'] == 3:
                for bot in self.get_visible_robots():
                    if bot.castle_talk > 0:
                        temp = self.castleLoc[bot['id']]
                        self.castleLoc[bot['id']] = (bot.castle_talk - 1, self.castleLoc[bot['id']][1])

                for k in self.castleLoc.keys():
                    self.castles.append(k)
                    self.numCastles += 1


            # self.log("WICKED IMPORTANT: " + self.castles)
            # self.log("DOUBLE IMPORTANT: " + str(self.castleLoc))



            self.log("TURN: " + str(self.me['turn']))
            # self.log("the map is "+ nav.symmetric(self.map))
            my_coord = (self.me['x'], self.me['y'])
            # self.log(str(SPECS['UNITS'][SPECS['CRUSADER']]))

            if self.castles != [] and self.me['turn'] % 30 != 0:
                attack_castle = self.castleLoc[self.castles[0]]
                self.log(str(attack_castle))
                self.signal(int(util.nodeHash(*attack_castle)),100)
            else:
                pass
                # self.log("HOW DID THIS HAPPEN!!")

            # self.log(str(self.numCastles))
            # self.log(str(self.castles))

            if self.me['turn'] < 3:
                # Send location over castleTalk to other castles
                if self.me['turn'] == 1:
                    self.castle_talk(self.me['y'] + 1)
                    self.log("Sending Y loc: " + str(self.me['y'] + 1))
                    for bot in self.get_visible_robots():
                        if bot.castle_talk > 0:
                            self.castleLoc[bot['id']] = (-1, bot.castle_talk - 1)
                elif self.me['turn'] == 2:
                    self.castle_talk(self.me['x'] + 1)
                    self.log("Sending X loc: " + str(self.me['x'] + 1))
                    for bot in self.get_visible_robots():
                        if bot.castle_talk > 0:
                            if bot['id'] in self.castleLoc.keys():
                                temp = self.castleLoc[bot['id']]
                                self.castleLoc[bot['id']] = (bot.castle_talk - 1, self.castleLoc[bot['id']][1])
                            else:
                                self.castleLoc[bot['id']] = (-1, bot.castle_talk - 1)
                    # self.log(str(self.castleLoc))


                    # self.log(str(self.numCastles))

                # if not self.karboniteMining:
                #     mapEnergy = self.get_fuel_map()
                #     self.karboniteMining  = True
                # else:
                #     mapEnergy = self.get_karbonite_map()
                #     self.karboniteMining = False

                # targetX, targetY = nav.get_closest_karbonite((self.me['x'],self.me['y']), mapEnergy)
                # targetX = str(targetX); targetY = str(targetY)

                # self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                if not self.resources_sphere:
                    karbonite_map=self.get_karbonite_map()
                    fuel_map=self.get_fuel_map()
                    self.resources_sphere=nav.get_closest_resources(self.log,my_coord,self.get_passable_map(),karbonite_map,fuel_map)
                    self.log(self.resources_sphere)
                #sending pilgrim its target
                targetX, targetY = self.resources_sphere[self.pilgrims_built]
                targetX = str(targetX); targetY = str(targetY)
                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)

                self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.pilgrims_built=self.pilgrims_built+1
                return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
            elif self.me['turn']<20 or self.me['turn'] % 30 == 0:

                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                if not self.resources_sphere:
                    karbonite_map=self.get_karbonite_map()
                    fuel_map=self.get_fuel_map()
                    self.resources_sphere=nav.get_closest_resources(self.log,my_coord,self.map,karbonite_map,fuel_map)
                    self.log(self.resources_sphere)
                
                self.log("Sphere of influence: " + str(self.resources_sphere))

                #sending pilgrim its target
                targetX, targetY = self.resources_sphere[self.pilgrims_built]
                targetX = str(targetX); targetY = str(targetY)
                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)
                self.log("Signal sent is: " + str(len(targetX)) + targetX + targetY)

                self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.pilgrims_built=self.pilgrims_built+1
                return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])

            elif self.me['turn'] < 40:


                    # self.log(str(self.castleLoc))
                    # self.log(str(self.castles))

                    # self.log(str(self.castleLoc))

                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.log(self.me['turn'])

                if self.fuel > self.numCastles*SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_KARBONITE']:
                    self.log("Building a Prophet at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                    return self.build_unit(SPECS['PROPHET'], goal_dir[0],goal_dir[1])

            elif self.me['turn'] % 3 == 0:
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                # self.log(self.me['turn'])
                if self.fuel > self.numCastles*SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['PROPHET']]['CONSTRUCTION_KARBONITE']:
                    self.log("Building a Prophet at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                    return self.build_unit(SPECS['PROPHET'], goal_dir[0],goal_dir[1])

            elif self.me['turn'] % 2 == 0:
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                # self.log(self.me['turn'])
                if random.random() < 0.8 and self.fuel > self.numCastles*SPECS['UNITS'][SPECS['CRUSADER']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['CRUSADER']]['CONSTRUCTION_KARBONITE']:
                    self.log("Building a Crusader at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                    return self.build_unit(SPECS['CRUSADER'], goal_dir[0],goal_dir[1])
                elif self.fuel > self.numCastles*SPECS['UNITS'][SPECS['PREACHER']]['CONSTRUCTION_FUEL'] and self.karbonite > self.numCastles*SPECS['UNITS'][SPECS['PREACHER']]['CONSTRUCTION_KARBONITE']:
                    self.log("Building a Preacher at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                    return self.build_unit(SPECS['PREACHER'], goal_dir[0],goal_dir[1])

            else:
                pass
        
        elif self.me['unit']==SPECS['PILGRIM']:
            self.log('Happy Thanksgiving!')
            my_loc=(self.me['x'],self.me['y'])
            moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

            #getting first turn target from castle
            if self.me['turn'] == 1:
                # Map Building
                # fuelMap = self.fuel_map
                self.homePath = my_loc
                self.closest_dropoff = my_loc

                # Read Signal!
                signal = ""
                for botv in self.get_visible_robots():
                    if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
                        signal = str(botv['signal'])
                        break

                parsePoint = int(signal[0])
                y = int(signal[parsePoint+1:])
                x = int(signal[1:parsePoint+1])
                # self.log("Signal is: " + signal + " and target is: " + str((x,y)))

                # self.wave[y][x] = 2
                self.target=(x,y)
                # self.log("The target is: " + str((self.targetX,self.targetY)))

                moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.target), moves)
                # for node in path:
                #     self.log("Path " + str((node.x,node.y)))
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                # self.log("Trying to move by: " + str(action) + " from " + str((self.me['x'],self.me['y'])))
                return self.move(*action)


            #checking if it is possible to dropoff
            if self.me['turn'] > 1:

                karbMiner = self.get_karbonite_map()[self.target[1]][self.target[0]]
                # self.log("karbMiner: " + str(karbMiner))
                drop_off = False
                for botv in self.get_visible_robots():
                    if botv['unit'] == SPECS['CASTLE'] or botv['unit'] == SPECS['CHURCH']:
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
                    if nav.distance(self.target,my_loc)<100:
                        taken=nav.resource_occupied(self.me,my_loc,self.target,self.get_visible_robots())
                        if taken:
                            self.log('my spot is taken:'+taken)
                            self.target=nav.new_resource_target(self.log,self.me,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map(),self.get_visible_robots())


                    if my_loc[0]==self.target[0] and my_loc[1]==self.target[1]:
                        self.log('Mining')
                        return self.mine()
                    #so the bot isnt at the target so it must be moving, either dropping off or going to build a church to dropoff
                    if self.dropping_off==True:
                        if self.should_build_church==True:
                            if my_loc[0]-self.build_site[0]<2 and my_loc[1]-self.build_site[1]<2:
                                #check once more if the church has to be built
                                self.should_build_church=nav.church_or_no(self,my_loc,self.map,self.get_visible_robots())
                                #now build the church if possible
                                if  self.should_build_church:
                                    #now free to build church
                                    return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])
                                #it shouldnt build the church anymore so now there is a church in range it should go there
                                self.closest_dropoff=nav.get_closest_dropoff(self,visible)
                                path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
                                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                                return self.move(*action)
                    #so it must not be dropping off and it must be moving to the target
                    self.log("Moving!")
                    path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.target), moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)

                #so now we know the tank is full
                else:
                    self.log('well this is problematic')
                    if drop_off==True:
                        #so the bot can drop off so it should and keep going with its life
                        return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], self.me['karbonite'], self.me['fuel'])
                    # #sadly he cannot dropoff
                    else:
                        self.log('im trying bob')
                        #checking to see if we should build a church  
                        self.should_build_church=nav.church_or_no(self,my_loc,self.map,self.get_visible_robots())
                        self.log('should i build a church'+self.should_build_church)
                        if not self.should_build_church:
                            self.closest_dropoff=nav.get_closest_dropoff(self,self.get_visible_robots())
                        if self.should_build_church:
                            self.log('whoops')
                            #we should build a church so get a good build location
                            self.build_site=nav.church_build_site(self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map())
                            self.closest_dropoff=self.build_site
                            #now check if we are close to the build site
                            if my_loc[0]-self.build_site[0]<2 and my_loc[1]-self.build_site[1]<2:
                                #so we can and should build
                                self.log('lets see how far we get')
                                return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])
                            #we arent close, so we must move to the closest dropoff site (this only works because pilgrims only take steps of one)
                    #so no matter what, even if were not building a church, we want to move to the dropoff site
                    self.dropping_off=True
                    self.log('back to moving')
                    path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)






                                
                                






        # elif self.me['unit'] == SPECS['PILGRIM']:
        #     self.log("Let us feast with the Indians")
        #     self.log('karbonite:'+self.karbonite)
        #     self.log('Fuel:'+self.fuel)
        #     # self.log('I should build a church:'+self.should_build_church)
        #     my_loc=(self.me['x'],self.me['y'])
        #     if self.me['turn'] == 1:
        #         # Map Building
        #         # fuelMap = self.fuel_map
        #         self.homePath = my_loc
        #         self.closest_dropoff = my_loc

        #         # Read Signal!
        #         signal = ""
        #         for botv in self.get_visible_robots():
        #             if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
        #                 signal = str(botv['signal'])
        #                 break

        #         parsePoint = int(signal[0])
        #         y = int(signal[parsePoint+1:])
        #         x = int(signal[1:parsePoint+1])
        #         # self.log("Signal is: " + signal + " and target is: " + str((x,y)))

        #         # self.wave[y][x] = 2
        #         self.targetX = x
        #         self.targetY = y
        #         # self.log("The target is: " + str((self.targetX,self.targetY)))

        #         moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        #         path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.target), moves)
        #         # for node in path:
        #         #     self.log("Path " + str((node.x,node.y)))
        #         action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        #         # self.log("Trying to move by: " + str(action) + " from " + str((self.me['x'],self.me['y'])))
        #         return self.move(*action)

        #     if self.me['turn'] > 1:

        #         karbMiner = self.get_karbonite_map()[self.target[1]][self.target[0]]
        #         # self.log("karbMiner: " + str(karbMiner))
        #         drop_off = False
        #         for botv in self.get_visible_robots():
        #             if botv['unit'] == SPECS['CASTLE'] or botv['unit'] == SPECS['CHURCH']:
        #                 for giving in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        #                     if util.nodeHash(giving[0]+self.me['x'], giving[1]+self.me['y']) == util.nodeHash(botv['x'],botv['y']):
        #                         drop_off = True
        #                         break;

        #             if drop_off:
        #                 break

        #         if karbMiner:
        #             energy = 'karbonite'
        #             capacity = SPECS['UNITS'][SPECS['PILGRIM']]['KARBONITE_CAPACITY']
        #         else:
        #             energy = 'fuel'
        #             capacity = SPECS['UNITS'][SPECS['PILGRIM']]['FUEL_CAPACITY']

        #         # botv_pos = []
        #         # for botv in self.get_visible_robots():
        #         #     botv_pos.append(util.nodeHash(botv.x,botv.y))
                    
        #         if util.nodeHash(self.me['x'],self.me['y']) == util.nodeHash(self.targetX,self.targetY) and self.me[energy] < capacity:
        #             self.log("MINING")
        #             # self.log(energy + " " + str(self.me[energy]) + "/" + str(capacity))
        #             visible=self.get_visible_robots()
        #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        #             return self.mine()
                
        #         elif self.should_build_church and not self.build_site[0]-my_loc[0]<2 and not self.build_site[1]-my_loc[1]<2:
        #             # This is always False unless the self.build_site attribute is to the lower right of pilgrim location! 
        #             # This is because the value will only be greater than two is the location is > 2 to the lower right diagonal (or 8r^2)
        #             self.log('checking if a church is necessary')
        #             #check if a church is still necessary
        #             visible=self.get_visible_robots()
        #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        #             if not self.should_build_church:
        #                 #now there is a church in range and it should go there
        #                 self.closest_dropoff=nav.get_closest_dropoff(self,visible)
        #             #now move to where the dropoff point should be
        #             path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)

        #         elif self.should_build_church and self.build_site[0]-my_loc[0]<2 and self.build_site[1]-my_loc[1]<2:
        #             self.log('we have moved closed enough to build the church')
        #             #check if a church is still necessary
        #             visible=self.get_visible_robots()
        #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        #             if not self.should_build_church:
        #                 #now there is a church in range and it should go there
        #                 self.closest_dropoff=nav.get_closest_dropoff(self,visible)
        #                 path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
        #                 action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        #                 return self.move(*action)

        #             #now it should build the church
        #             self.should_build_church=False  
        #             self.build_site=nav.church_build_site(self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map())
        #             self.closest_dropoff=self.build_site
        #             self.log("trying to build a church at "+self.build_site)
        #             return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])

        #         elif self.me[energy] < capacity and util.nodeHash(self.me['x'],self.me['y']) != util.nodeHash(self.targetX,self.targetY):
        #             self.log("Moving!!!")
        #             moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        #             path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), my_loc, (self.targetX,self.targetY), moves)
        #             action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        #             return self.move(*action)


        #         #FOR SOME REASON THIS WAS NOT ASSIGNING THINGS WELL
        #         elif self.me[energy] == capacity and util.nodeHash(*self.closest_dropoff) != util.nodeHash(*my_loc) and not drop_off:
        #             self.log('I got this far! Im full')
        #             # self.log("WORKING LOOP")
        #             visible = self.get_visible_robots()
        #             moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        #             self.should_build_church=nav.church_or_no(self,(self.me['x'],self.me['y']),visible)
        #             self.log('Maybe a church now:'+self.should_build_church)
        #             if self.should_build_church:
        #                 self.log('here2')
        #                 self.build_site=nav.church_build_site(self.log,my_loc,self.map,self.get_fuel_map(),self.get_karbonite_map())
        #                 self.log('my build site is'+self.build_site)
        #                 self.closest_dropoff=self.build_site
        #             if self.should_build_church and self.build_site[0]-my_loc[0]<2 and self.build_site[1]-my_loc[1]<2:
        #                 self.log("trying to build a church at "+self.build_site)
        #                 return self.build_unit(SPECS['CHURCH'],self.build_site[0]-my_loc[0],self.build_site[1]-my_loc[1])
                    

        #             path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (my_loc), self.closest_dropoff, moves)
        #             action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
        #             return self.move(*action)


        #         elif drop_off and self.me[energy] == capacity:
                    
        #             return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], self.me['karbonite'], self.me['fuel'])
            
robot = MyRobot()
