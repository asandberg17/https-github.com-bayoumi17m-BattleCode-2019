package bc19;
import java.lang.reflect.Array;
import java.util.*;

public class MyRobot extends BCAbstractRobot {
    public int turn;
    public LinkedList<Node> curPath;

    public LinkedList<Node> astar(int x, int y, int cost) {
        Node start_node = new Node(me.x,me.y,null);
        start_node.g = 0.0; start_node.h = 0.0; start_node.f = 0.0;
        Node end_node = new Node(x,y,null);
        end_node.g = 0.0; end_node.h = 0.0; end_node.f = 0.0;

        Heap<Node> open = new Heap<Node>(true);
        HashSet<Node> closed = new HashSet<Node>();

        open.add(start_node,start_node.f);
        HashSet<Node> children = new HashSet<Node>();
        while (open.size() > 0){
            Node current_node = open.poll();
            closed.add(current_node);

            // If the Goal was Found
            if (current_node.x == end_node.x && current_node.y == end_node.y){
                LinkedList<Node> path = new LinkedList<Node>();
                Node current = current_node;
                while (current != null){
                    path.addFirst(current);
                    current = current.parent;
                }
            }

            // Generate Children

            Robot[] bot_collide = getVisibleRobots();
            int[][] possible = new int[][] {new int[]{-2,0},new int[]{-1,0},new int[]{-1,1},new int[]{0,1},new int[]{0,2},new int[]{1,1},new int[]{1,0},new int[]{2,0},new int[]{1,-1},new int[]{0,-1},new int[]{0,-2}};

            for (int[] new_position : possible){
                int nodex = current_node.x + new_position[0];
                int nodey = current_node.y + new_position[1];

                boolean[][] map = getPassableMap();
                // Check Map Boundaries
                if ((nodex > (map.length -1)) || (nodex < 0) || (nodey < 0) || (nodey > (map.length - 1))) {
                    continue;
                }

                // Check walkable terrain
                if (map[nodey][nodex] != true) {
                    continue;
                }

                // Check robots in position
                for (Robot botc: bot_collide){
                    if (nodex == botc.x && nodey == botc.y) {
                        continue;
                    }
                }
                // Append to children
                children.add(new Node(nodex,nodey,current_node));
                }

            

                // Loop through children
                for (Node child: children){

                    for (Node closed_child: closed){
                        if (child == closed_child) {
                            continue;
                        }
                    }

                    int dx = Math.abs(child.x - current_node.x);
                    int dy = Math.abs(child.y - current_node.y);

                    child.g = current_node.g + dx + dy;
                    child.h = current_node.h + (dx*dx + dy*dy)*cost;
                    child.f = child.g + child.h;

                    for (Node open_node : open.map.keySet()){
                        if (child == open_node && child.g > open_node.g){
                            continue;
                        }

                    }


                    try {
                        open.add(child,child.f);
                    } catch (Exception e) {
                        open.updatePriority(child,child.f);
                    }
                }

        }
    }

    public Action turn() {
        turn++;

        if (me.unit == SPECS.CASTLE) {
            if (turn == 1) {
                return buildUnit(SPECS.PILGRIM,1,0);
            }

            if (turn ==2){
                boolean[][] mapFuel = getFuelMap();
                int[] pos = new int[]{me.x, me.y};
                for (int y=me.y-10; y<= me.y+10; y++ ){
                    for (int x=me.x-10; x<= me.x+10; x++ ){
                        if (y > mapFuel.length-1 || y<0 || x > mapFuel.length-1 || x<0){
                            continue;
                        }
                        else {
                            if (mapFuel[y][x] == true) {
                                if ((((pos[0] - me.x)*(pos[0] - me.x) + (pos[1] - me.y)*(pos[1] - me.y)) > ((x - me.x)*(x - me.x) + (y - me.y)*(y - me.y))) ||
                                 (((pos[0] - me.x)*(pos[0] - me.x) + (pos[1] - me.y)*(pos[1] - me.y)) == 0)) {
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
                return null;
                 
                //log(Integer.toString([0][getVisibleRobots()[0].castle_talk]));
            }
            if (turn == 2){
                Robot[] visibleBots = getVisibleRobots();
                for (Robot bot: visibleBots){
                    if (isRadioing(bot)){
                        String signal = "" + bot.signal;
                        int parsePoint = 1 + Integer.parseInt(signal.substring(0,1));
                        int y = Integer.parseInt(signal.substring(parsePoint));
                        int x = Integer.parseInt(signal.substring(1,parsePoint));


                        curPath = astar(x,y,1);
                        break;
                    }
                }
                if (curPath.size() > 0) {
                    Node new_Node = curPath.removeFirst();
                    return move(new_Node.x - me.x,new_Node.y - me.y);
                } else {
                    return null;
                }
            }
        }

        return null;
    }
}
