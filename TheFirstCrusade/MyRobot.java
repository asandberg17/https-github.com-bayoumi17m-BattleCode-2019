package bc19;
import java.lang.reflect.Array;
import java.util.*;

public class MyRobot extends BCAbstractRobot {
    public int turn;
    public LinkedList<Node> curPath;
    public int targetX;
    public int targetY;
    public int homeX;
    public int homeY;

    public LinkedList<Node> astar(int x, int y, int cost){
        Node start_node = new Node(me.x,me.y,null);
        start_node.g = 0.0; start_node.h = 0.0; start_node.f = 0.0;
        Node end_node = new Node(x,y,null);
        end_node.g = 0.0; end_node.h = 0.0; end_node.f = 0.0;

        Heap<Node> open = new Heap<Node>(true);
        HashSet<Node> closed = new HashSet<Node>();

        int k = -1;

        open.add(start_node,start_node.f);
        while (open.size() > 0){
            k++;

            Node current_node = open.poll();
            closed.add(current_node);

            // If Goal was found
            if ((current_node.x == end_node.x && current_node.y == end_node.y) || k > 100) {
                LinkedList<Node> path = new LinkedList<Node>();
                Node current = current_node;
                while (current != null){
                    path.addFirst(current);
                    current = current.parent;
                }
                return path;
            }

            Robot[] bot_collide = getVisibleRobots();
            ArrayList<int[]> possible = new ArrayList<int[]>(Arrays.asList(new int[]{-2,0},new int[]{-1,0},new int[]{-1,1},new int[]{0,1},new int[]{0,2},new int[]{1,1},new int[]{1,0},new int[]{2,0},new int[]{1,-1},new int[]{0,-1},new int[]{0,-2}));

            // Remove Possible Collisions
            for (Robot botc: bot_collide){
                possible.remove(new int[]{botc.x,botc.y});
            }

            HashSet<Node> children = new HashSet<Node>();
            for (int[] new_position: possible){
                int nodex = me.x + new_position[0];
                int nodey = me.y + new_position[1];

                boolean[][] map = getPassableMap();
                // Check map boundaries
                if ((nodex > (map.length -1)) || (nodex < 0) || (nodey < 0) || (nodey > (map.length - 1))) {
                    continue;
                }

                if (map[nodey][nodex] != true){
                    continue;
                }

                // Append to children
                children.add(new Node(nodex,nodey,current_node));

            }


            for (Node child: children){
                // if (closed.contains(child)) {
                //     continue;
                // }

                int dx = Math.abs(child.x - current_node.x);
                int dy = Math.abs(child.y - current_node.y);

                child.g = current_node.g + 1;//+ dx + dy;
                child.h = 0; //Math.sqrt((child.x - x)*(child.x - x) + (child.y - y)*(child.y - y)); //current_node.h + (dx*dx + dy*dy)*cost + 
                child.f = child.g + child.h;

                // for (Node open_node: open.map.keySet()){
                //     if (child == open_node && child.g > open_node.g){
                //         continue;
                //     }
                // }

                try {
                    open.add(child,child.f);
                } catch (IllegalArgumentException e) {
                    open.updatePriority(child,child.f);
                }
            }

        }

        return new LinkedList<Node>();
    }

    public Action turn() {
        turn++;

        if (me.unit == SPECS.CASTLE) {
            if (turn == 1) {
                log("Building a pilgrim.");
                return buildUnit(SPECS.PILGRIM,1,0);
            }
            if (turn == 2){
                boolean[][] mapFuel = getFuelMap();
                int[] pos = new int[]{0,0};

                for (int y=0; y<= mapFuel.length-1; y++ ){
                    for (int x=0; x<= mapFuel.length-1; x++ ){
                        if (y > mapFuel.length-1 || y<0 || x > mapFuel.length-1 || x<0){
                            continue;
                        } else {
                            if (mapFuel[y][x] == true) {
                                if (((pos[0] - me.x)*(pos[0] - me.x) + (pos[1] - me.y)*(pos[1] - me.y)) > ((x - me.x)*(x - me.x) + (y - me.y)*(y - me.y))) {
                                    pos[0] = x; pos[1] = y;
                                }
                            }
                        }
                    }
                }
                String sig = "" + pos[0];
                sig = "" + sig.length() + sig;
                signal(Integer.parseInt(sig + pos[1]),2);
                return null;
            }
        }

        if (me.unit == SPECS.PILGRIM) {
            if (turn == 1) {
                log("I am a pilgrim.");
                 
                //log(Integer.toString([0][getVisibleRobots()[0].castle_talk]));
            }
            if (turn == 2){
                // TODO
                if (curPath == null){
                    log("True");
                } else {
                    log("False");
                }

                Robot[] visibleBots = getVisibleRobots();
                for (Robot bot: visibleBots){
                    if (isRadioing(bot)){
                        String signal = "" + bot.signal;
                        log(signal);
                        int parsePoint = 1 + Integer.parseInt(signal.substring(0,1));

                        int x = Integer.parseInt(signal.substring(1,parsePoint));
                        int y = Integer.parseInt(signal.substring(parsePoint));
                        // log("X is " + x + " and Y is " + y);

                        //curPath = new LinkedList<Node>();
                        targetX = x;
                        targetY = y;

                        //curPath = astar(x,y,1);
                        break; 
                    }
                }
                int dx = targetX - me.x;
                if (dx > 0){
                    dx = 1;
                } else {
                    if (dx < 0){
                        dx = -1;
                    } else {
                        dx = 0;
                    }
                }

                int dy = targetY - me.y;
                if (dy > 0){
                    dy = 1;
                } else {
                    if (dy < 0){
                        dy = -1;
                    } else {
                        dy = 0;
                    }
                }
                log("dX is " + dx + " and dY is " + dy);

                return move(dx,dy);
                // if (curPath == null){
                //     log("True");
                // } else {
                //     log("False");
                // }
                // Node new_node = curPath.get(1);
                // curPath = null;
                // int dx = new_node.x - me.x;
                // int dy = new_node.y - me.y;
                // log("dx is " + dx + ", dy is " + dy);
                // if (me.id < 1000){
                //     for (Node n: curPath){
                //         log("(" + Integer.toString(n.x) + "," + Integer.toString(n.y) + ")");
                //     }
                //     log("~~~~~~~~~~~");
                // }
                //return move(dx,dy);
            }
            if (turn > 3){
                // curPath = null;
                // curPath = astar(targetX,targetY,1);
                // Node new_node = curPath.get(1);
                // int dx = new_node.x - me.x;
                // int dy = new_node.y - me.y;
                // return move(dx,dy);
                int dx = targetX - me.x;
                if (dx > 0){
                    dx = 1;
                } else {
                    if (dx < 0){
                        dx = -1;
                    } else {
                        dx = 0;
                    }
                }

                int dy = targetY - me.y;
                if (dy > 0){
                    dy = 1;
                } else {
                    if (dy < 0){
                        dy = -1;
                    } else {
                        dy = 0;
                    }
                }

                if (dx*dx + dy*dy == 0){
                    return mine();
                }
                return move(dx,dy);


            }
        }

        return null;

    }
}