package bc19;
import java.lang.reflect.Array;
import java.util.*;

public class MyRobot extends BCAbstractRobot {
    public int turn;
    public LinkedList<Node> curPath;

    private LinkedList<Node> astar(int x, int y, int cost) {
        Node start_node = Node(me.x,me.y,None);
        start_node.g = 0.0; start_node.h = 0.0; start_node.f = 0.0;
        Node end_node = Node(x,y,None);
        end_node.g = 0.0; end_node.h = 0.0; end_node.f = 0.0;

        Heap<Node> open = new Heap<Node>(true);
        HashSet<Node> closed = new HashSet<Node>();

        open.add(start_node,start_node.f);

        while (open.size() != 0){
            Node current_node = open.poll();
            closed.add(current_node);

            // If the Goal was Found
            if (current_node.x == end_node.x && current_node.y == end_node.y){
                LinkedList<Node> path = new LinkedList<Node>();
                Node current = current_node;
                while (current != Null){
                    path.addFirst(current);
                    current = current.parent;
                }
            }

            // Generate Children
            HashSet<Node> children = new HashSet<Node>();
            Robot[] bot_collide = getVisibleRobots();
            switch (me.unit){
                case SPECS.PILGRIM:
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
                        if map[nodey][nodex] != true{
                            continue;
                        }

                        // Check robots in position
                        for (Robot botc: bot_collide){
                            if nodex == botc.x && nodey == botc.y{
                                continue;
                            }
                        }
                        // Append to children
                        children.add(new Node(nodex,nodey,current_node));
                    }
                default:
                    return new LinkedList<Node>();

            }

            // Loop through children
            for (Node child: children){

                for (Node closed_child: closed){
                    if child == closed_child:
                        continue;
                }

                int dx = abs(child.x - current_node.x);
                int dy = abs(child.y - current_node.y);

                child.g = current_node.g + dx + dy;
                child.h = current_node.h + (dx*dx + dy*dy)*cost;
                child.f = child.g + child.h;

                for (Node open_node : open){
                    if child == open_node and child.g > open_node.g {
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
                int[] pos = new int[2]{me.x,me.y};
                for (int y=me.y-10; y<= me.y+10; y++ ){
                    for (int x=me.x-10; x<= me.x+10; x++ ){
                        if (y > mapFuel.length-1 || y<0 || x > mapFuel.length-1 || x<0){
                            continue;
                        }
                        else {
                            if mapFuel[y][x] == true {
                                if (((pos[0] - me.x)*(pos[0] - me.x) + (pos[1] - me.y)*(pos[1] - me.y)) > ((x - me.x)*(x - me.x) + (y - me.y)*(y - me.y))) ||
                                 (((pos[0] - me.x)*(pos[0] - me.x) + (pos[1] - me.y)*(pos[1] - me.y)) == 0){
                                    pos[0] = x; pos[1] = y;
                                }
                            }
                        }
                    }
                }
                String sig = "" + x;
                sig = "" + sig.length() + sig;
                signal(Integer.parseInt(sig + y),2);
                return;
            }

        }

        if (me.unit == SPECS.PILGRIM) {
            if (turn == 1) {
                log("I am a pilgrim.");
                return;
                 
                //log(Integer.toString([0][getVisibleRobots()[0].castle_talk]));
            }
            if (turn == 3){
                Robot[] visibleBots = getVisibleRobots();
                for (Robot bot: visibleBots){
                    if (isRadioing(bot)){
                        String signal = "" + r.signal;
                        int parsePoint = 1 + Integer.parseInt(signal.subString(0,1));
                        int y = Integer.parseInt(signal.substring(parsePoint));
                        int x = Integer.parseInt(signal.substring(1,parsePoint));


                        me.curPath = astar(x,y,1);
                        break;
                    }
                }
                if me.curPath.size() > 0{
                    Node new_Node = me.curPath.removeFirst();
                    return move(new_Node.x - me.x,new_Node.y - me.y);
                } else {
                    return;
                }
            }
        }

        return null;

    }
}

public class Node {

    public Node(int x, int y, Node parent) {
        Node this.parent = parent
        int this.x = x
        int this.y = y

        double this.g = 0.0
        double this.h = 0.0
        double this.f = 0.0
    }
}

/** An instance is a min-heap or a max-heap of distinct values of type E
 *  with priorities of type double. 
 *  Author: David Gries. */
public class Heap<E> {

    /** Class Invariant:
     *   1. d[0..size-1] represents a complete binary tree. d[0] is the root;
     *      For each k, d[2k+1] and d[2k+2] are the left and right children of d[k].
     *      If k != 0, d[(k-1)/2] (using integer division) is the parent of d[k].
     *   
     *   2. For k in 0..size-1, d[k] contains the value and its priority.
     *   
     *   3. The values in d[0..size-1] are all different.
     *   
     *   4. For k in 1..size-1,
     *      if isMinHeap, (d[k]'s priority) >= (d[k]'s parent's priority),
     *      otherwise,    (d[k]'s priority) <= (d[k]'s parent's priority).
     *   
     *   map and the tree are in sync, meaning:
     *   
     *   5. The keys of map are the values in d[0..size-1].
     *      This implies that this.size = map.size().
     *   
     *   6. if value v is in d[k], then map.get(v) returns k.
     */
    protected final boolean isMinHeap;
    protected VP[] d;
    protected int size;
    protected HashMap<E, Integer> map;

    /** Constructor: an empty heap with capacity 10.
     *  It is a min-heap if isMin is true, a max-heap if isMin is false. */
    public Heap(boolean isMin) {
        isMinHeap= isMin;
        d= createVPArray(10);
        map= new HashMap<E, Integer>();
    }

    /** A VP object houses a value and a priority. */
    class VP {
        E val;             // The value
        double priority;   // The priority

        /** An instance with value v and priority p. */
        VP(E v, double p) {
            val= v;
            priority= p;
        }

        /** Return a representation of this VP object. */
        @Override public String toString() {
            return "(" + val + ", " + priority + ")";
        }
    }

    /** Add v with priority p to the heap.
     *  Throw an illegalArgumentException if v is already in the heap.
     *  The expected time is logarithmic and the worst-case time is linear
     *  in the size of the heap. */
    public void add(E v, double p) throws IllegalArgumentException {
        // TODO #1: Write this whole method. Note that bubbleUp is not implemented,
        // so calling it has no effect (yet). The first tests of add, using
        // test00Add, ensure that this method maintains fields d and map properly,
        // without worrying about bubbling up. 

        // Testing procedure test00Add should work. Look at its specification.

        // Do NOT call bubbleUp until the class invariant is true except
        // for the need to bubble up.
        // Calling bubbleUp is the last thing to be done.
        if (map.containsKey(v)) {
            throw new IllegalArgumentException("v is already in the heap");
        }
        ensureSpace();
        map.put(v, size);
        d[size]= new VP(v, p);
        size= size + 1;
        bubbleUp(size-1);
    }

    /** If size = length of d, double the length of array d.
     *  The worst-case time is proportional to the length of d. */
    protected void ensureSpace() {
        //TODO #2. Any method that increases the size of the heap must call
        // this method first. 
        if (size == d.length)  d= Arrays.copyOf(d, 2*d.length);
    }

    /** Return the size of this heap.
     *  This operation takes constant time. */
    public int size() { // Do not change this method
        return size;
    }

    /** Swap d[h] and d[k].
     *  Precondition: 0 <= h < heap-size, 0 <= k < heap-size. */
    void swap(int h, int k) {
        assert 0 <= h  &&  h < size  &&  0 <= k  &&  k < size;
        //TODO 3: When bubbling values up and (later on) down, two values,
        // say d[h] and d[k], will have to be swapped. At the same time,
        // the definition of map has to be maintained.
        // In order to always get this right, use method swap for this.
        // Method swap is tested by testing procedure test13Swap --it will
        // find no errors if you write this method properly.
        // 
        // Read the Assignment A5 note about map.put(...).
        VP temp= d[h];
        d[h]= d[k];
        d[k]= temp;
        map.put(d[h].val, h);
        map.put(d[k].val, k);
    }

    /** If a value with priority p1 should be above a value with priority
     *       p2 in the heap, return 1.
     *  If priority p1 and priority p2 are the same, return 0.
     *  If a value with priority p1 should be below a value with priority
     *       p2 in the heap, return -1.
     *  This is based on what kind of a heap this is,
     *  E.g. a min-heap, the value with the smallest priority is in the root.
     *  E.g. a max-heap, the value with the largest priority is in the root.
     */
    public int compareTo(double p1, double p2) {
        if (p1 == p2) return 0;
        if (isMinHeap) {
            return p1 < p2 ? 1 : -1;
        }
        return p1 > p2 ? 1 : -1;
    }

    /** If d[m] should be above d[n] in the heap, return 1.
     *  If d[m]'s priority and d[n]'s priority are the same, return 0.
     *  If d[m] should be below d[n] in the heap, return -1.
     *  This is based on what kind of a heap this is,
     *  E.g. a min-heap, the value with the smallest priority is in the root.
     *  E.g. a max-heap, the value with the largest priority is in the root.
     */
    public int compareTo(int m, int n) {
        return compareTo(d[m].priority, d[n].priority);
    }

    /** Bubble d[k] up the heap to its right place.
     *  Precondition: 0 <= k < size and
     *       The class invariant is true, except perhaps
     *       that d[k] belongs above its parent (if k > 0)
     *       in the heap, not below it. */
    void bubbleUp(int k) {
        // TODO #4 This method should be called within add in order
        // to bubble a value up to its proper place, based on its priority.
        // Do not use recursion. Use iteration.
        // Use method compareTo to test whether value k is in its right place.
        // If this method is written properly, testing procedure
        // test15Add_BubbleUp() will not find any errors.
        assert 0 <= k  &&  k < size;

        // Inv: 0 <= k < size and
        //      The class invariant is true, except perhaps
        //      that d[k] belongs above its parent (if k > 0)
        //      in the heap, not below it.
        while (k > 0) {
            int p= (k-1) / 2; // p is k's parent
            if (compareTo(k, p) <= 0) return;
            swap(k, p);
            k= p;
        }
    }

    /** If this is a min-heap, return the heap value with lowest priority.
     *  If this is a max-heap, return the heap value with highest priority
     *  Do not change the heap. This operation takes constant time.
     *  Throw a NoSuchElementException if the heap is empty. */
    public E peek() {
        // TODO 5: Do peek. This is an easy one. If it is correct,
        //         test25MinPeek() and test25MaxPeek will show no errors.
        if (size <= 0) throw new NoSuchElementException("heap is empty");
        return d[0].val;
    }

    /** Bubble d[k] down in heap until it finds the right place.
     *  If there is a choice to bubble down to both the left and
     *  right children (because their priorities are equal), choose
     *  the right child.
     *  Precondition: 0 <= k < size   and
     *           Class invariant is true except that perhaps
     *           d[k] belongs below one or both of its children. */
    void bubbleDown(int k) {
        // TODO 6: We suggest implementing and using upperChildOf, though
        //         you don't have to. DO NOT USE RECURSION. Use iteration.
        //         When this method is correct, testing procedures
        //         test30MinBubbledown and test31MinBubbledown and
        //         test31MaxBubbledown will not find errors.
        assert 0 <= k  &&  k < size;

        // Invariant: Class invariant is true except that perhaps
        //            d[k] belongs below one or both of its children
        while (2*k+1 < size) { // while d[k] has a child
            int uc= upperChild(k);
            if (compareTo(k, uc) >= 0) return;
            swap(k, uc);
            k= uc;
        }
    }

    /** If d[n] doesn't exist or has no child, return n.
     *  If d[n] has one child, return its index.
     *  If d[n] has two children with the same priority, return the
     *      index of the right one.
     *  If d[n] has two children with different priorities return the
     *      index of the one that must appear above the other in a heap. */
    protected int upperChild(int n) {
        if (size <= n) return n;
        int lc= 2*n + 1;                  // index of n's left child
        if (size <= lc) return n;         // n has no child
        if (size  ==  lc + 1) return lc;  // n has exactly one child
        return compareTo(lc, lc+1) > 0 ? lc : lc+1;
    }

    /** If this is a min-heap, remove and return heap value with lowest priority.
     * If this is a max-heap, remove and return heap value with highest priority.
     * The expected time is logarithmic and the worst-case time is linear
     * in the size of the heap.
     * Throw a NoSuchElementException if the heap is empty. */
    public E poll() {
        // TODO 7: When this method is written correctly, testing procedure
        //         test30Poll_BubbleDown_NoDups will not find errors.
        // 
        //         Note also testing procedure test40DuplicatePriorities
        //         This method tests to make sure that when bubbling up or down,
        //         two values with the same priority are not swapped.
        if (size <= 0) throw new NoSuchElementException("heap is empty");

        E v= d[0].val;
        swap(0, size-1);
        map.remove(v);
        size= size - 1;
        if (size > 0) bubbleDown(0);
        return v;
    }

    /** Change the priority of value v to p.
     *  The expected time is logarithmic and the worst-case time is linear
     *  in the size of the heap.
     *  Throw an IllegalArgumentException if v is not in the heap. */
    public void updatePriority(E v, double p) {
        // TODO  8: When this method is correctly implemented, testing procedure
        //          test50updatePriority() won't find errors.
        Integer index= map.get(v);
        if (index == null) throw new IllegalArgumentException("v is not in the priority queue");
        double oldP= d[index].priority;
        d[index].priority= p;
        int t= compareTo(p, oldP);
        if (t == 0) return;
        if (t < 0) bubbleDown(index);
        else bubbleUp(index);
    }

    /** Create and return an array of size n.
     *  This is necessary because generics and arrays don't interoperate nicely.
     *  A student in CS2110 would not be expected to know about the need
     *  for this method and how to write it. We had to search the web to
     *  find out how to do it. */
    VP[] createVPArray(int n) {
        return (VP[]) Array.newInstance(VP.class, n);
    }
}
