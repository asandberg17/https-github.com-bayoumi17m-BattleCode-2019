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

    karboniteMining = True

    wave = []
    homePath = []
    visited = []
    mapSize = 0

    already_been = {}
    base = None
    destination = None

    def turn(self):
        if self.me['unit'] == SPECS['CRUSADER']:
            self.log("Crusader health: " + str(self.me['health']))

            visible = self.get_visible_robots()

            # get attackable robots
            attackable = []
            for r in visible:
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
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])

            # # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
            my_coord = (self.me['x'], self.me['y'])
            self.already_been[my_coord] = True
            self.log("My destination is "+self.destination)
            if not self.destination:
                self.log("trying to move")
                self.destination = nav.reflect(self.map, my_coord, nav.symmetric(self.map))
            self.log("Trying to move to "+ self.destination)
            return self.move(*nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been))
            
               
        elif self.me['unit'] == SPECS['CASTLE']:
            # self.log("the map is "+ nav.symmetric(self.map))

            if self.me['turn'] < 3:
                if not self.karboniteMining:
                    mapEnergy = self.get_fuel_map()
                    self.karboniteMining  = True
                else:
                    mapEnergy = self.get_karbonite_map()
                    self.karboniteMining = False

                size = len(mapEnergy) -1
                dist = 121
                targetX = "0"
                targetY = "0"
                for i in range(-20,21):
                    for k in range(-20,21):
                        if self.me['y'] + i < 0 or self.me['x'] + k < 0 or self.me['y'] + i > size or self.me['x'] + k > size:
                            continue
                        if mapEnergy[self.me['y'] + i][self.me['x'] + k] and i**2 + k**2 < dist:
                            targetX = str(self.me['x'] + k)
                            targetY = str(self.me['y'] + i)
                            dist = i**2 + k**2

                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)

                self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                my_coord = (self.me['x'], self.me['y'])
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
            elif self.me['turn'] < 10:
                my_coord = (self.me['x'], self.me['y'])
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.log("Building a crusader at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                return self.build_unit(SPECS['CRUSADER'], goal_dir[0],goal_dir[1])
            else:
                pass
                # self.log("Castle health: " + self.me['health'])
        
        elif self.me['unit'] == SPECS['PILGRIM']:
            if self.me['turn'] == 1:
                # Map Building
                # fuelMap = self.fuel_map
                passMap = self.map
                # karbMap = self.karbonite_map
                self.mapSize = len(passMap)
                for y in range(self.mapSize):
                    row = []
                    vrow = []
                    for x in range(self.mapSize):
                        vrow.append(0)
                        if passMap[y][x] == False:
                            row.append(0)
                        else:
                            row.append(0)
                    self.wave.append(row)
                    self.visited.append(vrow)

                # self.log("IMPORTANT0: " + str(self.visited[12][38]))

                # Read Signal!
                signal = ""
                for botv in self.get_visible_robots():
                    if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
                        signal = str(botv['signal'])
                        break

                # self.log("Signal: " + signal)
                parsePoint = int(signal[0])
                y = int(signal[parsePoint+1:])
                x = int(signal[1:parsePoint+1])

                self.wave[y][x] = 2
                self.targetX = x
                self.targetY = y
                # self.log("IMPORTANT1: " + str(self.visited[12][38]))

            if self.me['turn'] == 2:
                # start = time.time()
                goal = (self.targetX,self.targetY,2)
                q = util.Queue()
                q.push(goal)
                # j= 0

                # self.log("IMPORTANT2: " + str(self.visited[12][38]))


                while q.isEmpty() == False:
                    # self.log(str(self.wave))
                    # j += 1
                    # self.log(str(j) + ", " + str((time.time() - start)*1000))
                    
                    (cx,cy,cs) = q.pop()
                    # self.log(str(self.wave))
                    # self.log("Position: " + str((cx,cy)) + ", Value: " +  str(self.visited[cy][cx]))

                    if not self.visited[cy][cx]:
                        self.visited[cy][cx] = 1
                        self.wave[cy][cx] =  1 + cs
                        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
                            newx = new_pos[0] + cx
                            newy = new_pos[1] + cy
                            
                            if (newx > self.mapSize-1 or newy > self.mapSize-1 or 0 > newy or 0 > newx):
                                continue;
                            if self.wave[newy][newx] == 1:
                                continue;

                            new_node = (newx,newy,self.wave[cy][cx])

                #             # self.log(str(newx > size-1))
                #             # self.log("visited: " + str((newx,newy)) + "~" + str(self.visited[newy][newx]))
                #             # self.log(str(self.me['id']) + ": " + str(self.visited))
                            
                            if self.visited[newy][newx]:
                                pass
                            else:
                                q.push(new_node)

                curScore = self.wave[self.me['y']][self.me['x']]
                newScore = curScore
                action = (0,0)
                
                for moves in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    newx = moves[0] + self.me['x']
                    newy = moves[1] + self.me['y']
                    if (newx > self.mapSize-1 or newy > self.mapSize-1 or 0 > newy or 0 > newx):
                                continue;
                    # self.log("Action: " + str(moves) + ", Cur: " + str(curScore) + ", New: " + str(self.wave[newy][newx]))

                    if self.wave[newy][newx] < newScore and self.wave[newy][newx] != 1:
                        newScore = self.wave[newy][newx]
                        action = moves
                


                self.homePath.append(action)
                return self.move(action[0],action[1])

            if self.me['turn'] > 1:
                karbMiner = self.get_karbonite_map()[self.targetY][self.targetX]
                self.log("karbMiner: " + str(karbMiner))

                if karbMiner:
                    energy = 'karbonite'
                    capacity = SPECS['UNITS'][SPECS['PILGRIM']]['KARBONITE_CAPACITY']
                else:
                    energy = 'fuel'
                    capacity = SPECS['UNITS'][SPECS['PILGRIM']]['FUEL_CAPACITY']

                botv_pos = []
                for botv in self.get_visible_robots():
                    botv_pos.append(util.nodeHash(botv.x,botv.y))
                if self.wave[self.me['y']][self.me['x']] == 3 and self.me[energy] < capacity:
                    # self.log("MINING")
                    self.log(energy + " " + str(self.me[energy]) + "/" + str(capacity))
                    return self.mine()

                elif self.me[energy] < capacity and self.wave[self.me['y']][self.me['x']] != 3:
                    curScore = self.wave[self.me['y']][self.me['x']]
                    newScore = curScore
                    action = (0,0)
                    size = len(self.wave) - 1
                    for moves in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        newx = moves[0] + self.me['x']
                        newy = moves[1] + self.me['y']

                        if util.nodeHash(newx,newy) in botv_pos:
                            continue;

                        if (newx > self.mapSize-1 or newy > self.mapSize-1 or 0 > newy or 0 > newx):
                                continue;
                        # self.log("Action: " + str(moves) + ", Cur: " + str(curScore) + ", New: " + str(self.wave[newy][newx]))

                        if newy > size or newx > size or newy < 0 or newx < 0:
                            continue

                        if self.wave[newy][newx] < newScore and self.wave[newy][newx] != 1:
                            newScore = self.wave[newy][newx]
                            action = moves

                    self.homePath.append(action)
                    return self.move(action[0],action[1])

                elif self.me[energy] == capacity and self.homePath != []:
                    
                    action = self.homePath.pop()
                    action[0] = -action[0]
                    action[1] = -action[1]
                    return self.move(action[0],action[1])

                else:
                    
                    for botv in self.get_visible_robots():
                        if botv['unit'] == SPECS['CASTLE']:
                            break;
                    return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], self.me['karbonite'], self.me['fuel'])

robot = MyRobot()