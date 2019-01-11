from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
import nav
import util
import time
# import copy

__pragma__('iconv')
__pragma__('tconv')
__pragma__('opov')



# don't try to use global variables!!
class MyRobot(BCAbstractRobot):

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
            self.log("the map is "+ nav.symmetric(self.map))
            if self.me['turn'] < 10:
                my_coord = (self.me['x'], self.me['y'])
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.log("Building a crusader at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                return self.build_unit(SPECS['CRUSADER'], goal_dir[0],goal_dir[1])
            else:
                self.log("Castle health: " + self.me['health'])
        
        elif self.me['unit'] == SPECS['PILGRIM']:
            if self.me['turn'] == 1:
                # Map Building
                fuelMap = self.fuel_map
                passMap = self.map
                karbMap = self.karbonite_map
                size = len(fuelMap)
                for y in range(size):
                    row = []
                    for x in range(size):
                        if passMap[y][x] == False:
                            row.append(1)
                        else:
                            row.append(0)
                    self.wave.append(row)
                # self.wave = copy.deepcopy(passMap)

                # Read Signal!
                signal = ""
                for botv in self.get_visible_robots():
                    if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
                        signal = str(botv['signal'])
                        break

                parsePoint = int(signal[0])
                y = int(signal[parsePoint+1:])
                x = int(signal[1:parsePoint+1])

                self.wave[y][x] = 2
                self.targetX = x
                self.targetY = y

                
            if self.me['turn'] == 2:

                start = time.time()
                goal = (util.Node(self.targetX,self.targetY),2)
                q = util.Queue()
                q.push(goal)
                visited = set()
                #j= 0

                while q.isEmpty() == False:
                    # self.log(str(self.wave))
                    #j += 1
                    # self.log(str(len(visited)) + ", " + str((time.time() - start)*1000))
                    
                    (n,cs) = q.pop()
                    cy = n.y
                    cx = n.x

                    if n not in visited:
                        visited.add(n)
                        self.wave[cy][cx] =  1 + cs
                        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
                            newx = new_pos[0] + cx
                            newy = new_pos[1] + cy
                            
                            if (newx > size-1 or newy > size-1 or 0 > newy or 0 > newx):
                                continue;
                            if self.wave[newy][newx] == 1:
                                continue;

                            q.push((util.Node(newx, newy), self.wave[cy][cx]))

                curScore = self.wave[self.me['y']][self.me['x']]
                newScore = curScore
                action = (0,0)
                
                for moves in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    newx = moves[0] + self.me['x']
                    newy = moves[1] + self.me['y']
                    self.log("Action: " + str(moves) + ", Cur: " + str(curScore) + ", New: " + str(self.wave[newy][newx]))

                    if self.wave[newy][newx] < newScore and self.wave[newy][newx] != 1:
                        newScore = self.wave[newy][newx]
                        action = moves
                


                self.homePath.append(action)
                return self.move(action[0],action[1])

            if self.me['turn'] > 2:
                if self.wave[self.me['y']][self.me['x']] == 2 and self.me['fuel'] < 100:
                    # self.log("MINING")
                    return self.mine()

                elif self.me['fuel'] < 100 and self.wave[self.me['y']][self.me['x']] != 2:
                    curScore = self.wave[self.me['y']][self.me['x']]
                    newScore = curScore
                    action = (-100,-100)
                    size = len(self.wave) - 1
                    for moves in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        newx = moves[0] + self.me['x']
                        newy = moves[1] + self.me['y']
                        self.log("Action: " + str(moves) + ", Cur: " + str(curScore) + ", New: " + str(self.wave[newy][newx]))

                        if newy > size or newx > size or newy < 0 or newx < 0:
                            continue

                        if self.wave[newy][newx] < newScore and self.wave[newy][newx] < 10000:
                            newScore = self.wave[newy][newx]
                            action = moves

                    self.homePath.append(action)
                    return self.move(action[0],action[1])

                elif self.me['fuel'] == 100 and self.homePath != []:
                    
                    action = self.homePath.pop()
                    action[0] = -action[0]
                    action[1] = -action[1]
                    return self.move(action[0],action[1])

                else:
                    
                    for botv in self.get_visible_robots():
                        if botv['unit'] == SPECS['CASTLE']:
                            break;
                    return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], 0, self.me['fuel'])

robot = MyRobot()