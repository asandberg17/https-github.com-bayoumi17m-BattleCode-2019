from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
import nav
import util

__pragma__('iconv')
__pragma__('tconv')
__pragma__('opov')

# don't try to use global variables!!
class MyRobot(BCAbstractRobot):
    step = -1
    # Pilgrim
    homePath = []
    wave = []
    # Crusader
    already_been = {}
    base = None
    destination = None

    def turn(self):
        self.step += 1
        self.log("START TURN " + self.step)
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

            # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
            my_coord = (self.me['x'], self.me['y'])
            self.already_been[my_coord] = True
            if not self.destination:
                self.destination = nav.reflect(self.map, my_coord, self.me['id'] % 2)
            return self.move(*nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been))

        elif self.me['unit'] == SPECS['CASTLE']:
            if self.me['turn'] < 3:
                if random.randint(0,1):
                    mapEnergy = self.get_fuel_map()
                else:
                    mapEnergy = self.get_karbonite_map()

                size = len(mapEnergy) -1
                dist = 121
                targetX = "0"
                targetY = "0"
                for i in range(-10,11):
                    for k in range(-10,11):
                        if self.me['y'] + i < 0 or self.me['x'] + k < 0 or self.me['y'] + i > size or self.me['x'] + k > size:
                            continue
                        if mapEnergy[self.me['y'] + i][self.me['x'] + k] and i**2 + k**2 < dist:
                            targetX = str(self.me['x'] + k)
                            targetY = str(self.me['y'] + i)
                            dist = i**2 + k**2

                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)

                self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                return self.build_unit(SPECS['PILGRIM'], 1, 1)

            elif self.me['turn'] < 6:
                self.log("Building a Crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                return self.build_unit(SPECS['CRUSADER'], 1, 1)
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

                # Read Signal!
                signal = ""
                for botv in self.get_visible_robots():
                    if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
                        signal = str(botv['signal'])
                        break

                parsePoint = int(signal[0])
                y = int(signal[parsePoint:])
                x = int(signal[1:parsePoint+1])
                self.log("Pilgrim Signals:" + str(parsePoint) + ", " + str(y), + ", " + str(x))

                # self.wave[y][x] = 2

                # goal = (x,y)
                # q = util.Queue()
                # q.push(goal)
                # visited = []

                # while q.isEmpty == False:
                #     for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
                #         (cx,cy) = q.pop()
                #         newx = new_pos[0] + cx
                #         newy = new_pos[1] + cy

                #         if (newx > size-1 or newy > size-1 or 0 > newy or 0 > newx):
                #             continue;
                #         if (cx,cy) in visited:
                #             continue;
                #         if self.wave[newy][newx] == 1:
                #             continue;

                #         self.wave[newy][newx] += 1
                #         q.push((newx,newy))
                #         visited.append((cx,cy))

                # newScore = 1000
                # action = None
                # for moves in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                #     curScore = self.wave[self.me['y']][self.me['x']]
                #     newx = new_pos[0] + self.me['x']
                #     newy = new_pos[1] + self.me['y']

                #     if self.wave[newy][newx] < newScore and self.wave[newy][newx] != 1:
                #         newScore = self.wave[newy][newx]
                #         action = moves

                # homePath.append(action)
                # return self.move(action[0],action[1])

            if self.me['turn'] > 1:
                
                self.log("Pilgrim: ") #+ str(self.me['y']))

                # if self.wave[self.me['y']][self.me['x']] == 2 and self.me['fuel'] < 100:
                #     return self.mine()

                # elif self.me['fuel'] < 100 and self.wave[self.me['y']][self.me['x']] != 2:
                #     newScore = 1000
                #     action = None
                #     size = len(self.wave) - 1
                #     for moves in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                #         curScore = self.wave[self.me['y']][self.me['x']]
                #         newx = new_pos[0] + self.me['x']
                #         newy = new_pos[1] + self.me['y']

                #         if newy > size or newx > size or newy < 0 or newx < 0:
                #             continue

                #         if self.wave[newy][newx] < newScore and self.wave[newy][newx] != 1:
                #             newScore = self.wave[newy][newx]
                #             action = moves

                #     self.homePath.append(action)
                #     return self.move(action[0],action[1])

                # elif self.me['fuel'] == 100 and self.homePath != []:
                #     action = self.homePath.pop()
                #     action[0] = -action[0]
                #     action[1] = -action[1]
                #     return self.move(action[0],action[1])

                # else:
                #     for botV in self.get_visible_robots():
                #         if botv == SPECS['CASTLE']:
                #             break;

                #     return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], 0, self.me['fuel'])





                

robot = MyRobot()
