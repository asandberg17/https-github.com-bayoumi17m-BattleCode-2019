package bc19;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;




package student;
/* Time spent on a6:  hh hours and mm minutes.

 * Name(s):
 * Netid(s): 
 * What I thought about this assignment: 
 * 
 *
 *
 */

import java.lang.reflect.Array;

import java.util.*;

/** An instance is a min-heap of distinct values of type V with
 *  priorities of type double. Since it's a min-heap, the value
 *  with the smallest priority is at the root of the heap. */
public class Heap<V> {

    /** The contents of c represent a complete binary tree. c[0] is the root;
     * c[2i+1] and c[2i+2] are the left and right children of c[i].
     * If i is not 0, c[i/2] (using integer division) is the parent of c[i].
     * 
     * Class Invariant:
     *   1. The tree is complete. It consists of c[0..size-1].
     *   
     *   2. For i in 0..size-1, c[i] contains the value and its priority.
     *      For i in size..c.length-1, c[i] = null.
     *   
     *   3. The values in c[0..size-1] are all different
     *   
     *   4. For i in 1..size-1, (c[i]'s priority) >= (c[i]'s parent's priority)
     *   
     *   map and the tree are in sync:
     *     5. The keys of map are the values in c[0..size-1]
     *     6. c[map[v]] has value v
     * 
     * Note that invariant 5 implies that this.size equals map.size
     */
    protected Entry[] c;
    protected int size;
    protected HashMap<V, Integer> map;

    /** Constructor: an empty heap with capacity 10. */
    public Heap() {
        c= createEntryArray(10);
        map= new HashMap<V, Integer>();
    }
    
    /** An Entry contains a value and a priority. */
    class Entry {
        V value;
        double priority;
        
        /** An Entry with value v and priority p*/
        Entry(V v, double p) {
            value= v;
            priority= p;
        }
    }
    
    /** Add v with priority p to the heap.
     *  Throw an illegalArgumentException if v is already in the heap.
     *  The expected time is logarithmic and the worst-case time is linear
     *  in the size of the heap. */
    public void add(V v, double p) throws IllegalArgumentException {
        // TODO #1: Write this whole method. Note that bubbleUp is not implemented,
        // so calling it will have no effect (yet). The first tests of add, using
        // test00Add, ensure that this method maintains fields c and map properly,
        // without worrying about bubbling up. Look at the spec of test00Add.
        if (map.containsKey(v)) {
            throw new IllegalArgumentException("v is already in the heap");
        }
        ensureSpace();
        map.put(v, size);
        c[size]= new Entry(v, p);
        size= size + 1;
        bubbleUp(size-1);
    }

       
    /** If size = length of c, double the length of array c. */
    public void ensureSpace() {
        //TODO #2. Any method that changes the size of array c needs to call
        // this method first. If you write this method correctly AND method
        // add calls this method appropriately, testing procedure
        // test10ensureSpace will not find errors.
        if (size != c.length) return;
        
        Entry[] newC= createEntryArray(2*c.length);
        for (int k= 0; k < size; k= k+1) {
            newC[k]= c[k];
        }
        c= newC;
    }

    /** Return the number of values in this heap.
     *  This operation takes constant time. */
    public int size() {
        return size;
    }

    /** Swap c[h] and c[k].
     *  Precondition: 0 <= h < c.size, 0 <= k < c.size. */
    void swap(int h, int k) {
        //TODO 3: When bubbling values up and down (later on), two values,
        // say c[h] and c[k], will have to be swapped. At the same time,
        // field map has to be maintained. In order to always get this right,
        // use method swap for this. Method swap is tested by testing
        // procedure test13Add_Swap --it will find no errors if you write
        // this method properly.
        Entry temp= c[h];
        c[h]= c[k];
        c[k]= temp;
        map.put(c[h].value, h);
        map.put(c[k].value, k);
    }
    
    /** Bubble c[k] up in heap to its right place.
     *  Precondition: Priority of every c[i] >= its parent's priority
     *                except perhaps for c[k] */
    private void bubbleUp(int k) {
        // TODO #4 As you know, this method should be called within add in order
        // to bubble a value up to its proper place, based on its priority.
        // Do not use recursion. Use iteration.
        // If this method is written properly, testing procedure
        // test15Add_BubbleUp() will not find any errors.
        
        // Inv: Priority of every c[i] >= its parent's priority except perhaps for c[k]
        while (k > 0) {
            int p= (k-1) / 2; // p is k's parent
            if (c[k].priority >= c[p].priority) return;
            swap(k, p);
            k= p;
        }
    }

    /** Return the value of this heap with lowest priority. Do not
     *  change the heap. This operation takes constant time.
     *  Throw a NoSuchElementException if the heap is empty. */
    public V peek() {
        // TODO 5: Do peek. This is an easy one. 
        //         test20Peek() will not find errors if this is correct.
        if (size <= 0) throw new NoSuchElementException("heap is empty");
        return c[0].value;
    }
    
    /** Return the lowest priority in the heap. This operation takes constant time.
    *  Throw a NoSuchElementException if v is not in the heap. */
   public Double peekAtPriority() {
       if (size <= 0) throw new NoSuchElementException("heap is empty");
       return c[0].priority;
   }

    /** Remove and return the element of this heap with lowest priority.
     *  The expected time is logarithmic and the worst-case time is linear
     *  in the size of the heap.
     *  Throw a NoSuchElementException if the heap is empty. */
    public V poll() {
        // TODO 6: Do poll and bubbleDown (#7) together. When they are
        //         written correctly, testing procedure test30Poll_BubbleDown_NoDups
        //         will not find errors.
        // 
        //         Note also testing procedure test40testDuplicatePriorities
        //         This method tests to make sure that when bubbling up or down,
        //         two values with the same priority are not swapped.
        if (size <= 0) throw new NoSuchElementException("heap is empty");

        V v= c[0].value;
        
        swap(0, size-1);
        map.remove(v);
        size= size - 1;
        c[size]= null;
        bubbleDown(0);
        return v;
    }
    
    /** Bubble c[k] down in heap until it finds the right place.
     *  If there is a choice to bubble down to both the left and
     *  right children (because their priorities are equal), choose
     *  the right child.
     *  Note: If size == 0 (the heap is empty), just return.
     *  Precondition: Each c[i]'s priority <= its childrens' priorities 
     *                except perhaps for c[k] */
    private void bubbleDown(int k) {
        // TODO 7: Do poll (#6) and bubbleDown together. We also suggest
        //         implementing and using smallerChildOf, though you don't
        //         have to. Do not use recursion. Use iteration.
        
        // Invariant: Priority of every c[i] <= its childrens' priorities
        //            except perhaps for c[k]
        while (2*k+1 < size) {  // while k has a child
            int sc= smallerChildOf(k);
            if (c[k].priority <= c[sc].priority) return;
            swap(k, sc);
            k= sc;
        }
    }

    /** Return the index of the smaller child of c[n]
     *  If the two children have the same priority, choose the right one.
     *  Precondition: left child exists: 2n+1 < size of heap */
     int smallerChildOf(int n) {
        int lChild= 2*n + 1;
        if (lChild + 1  ==  size) return lChild;
        return c[lChild].priority < c[lChild+1].priority ? lChild : lChild+1;
    }

    /** Change the priority of value v to p.
     *  The expected time is logarithmic and the worst-case time is linear
     *  in the size of the heap.
     *  Throw an IllegalArgumentException if v is not in the heap. */
    public void changePriority(V v, double p) {
        // TODO  8: When this method is correctly implemented, testing procedure
        //          test50ChangePriority() won't find errors.
        Integer index= map.get(v);
        if (index == null)
            throw new IllegalArgumentException("v is not in the priority queue");
        if (p > c[index].priority) {
            c[index].priority= p;
            bubbleDown(index);
        } else {
            c[index].priority= p;
            bubbleUp(index);
        }
    }
    
    /** Create and return an Entry[] of size n.
     *  This is necessary because Generic and arrays don't interoperate nicely.
     *  A student in CS2110 would not be expected to know about the need
     *  for this method and how to write it. */
     Entry[] createEntryArray(int n) {
        return (Entry[]) Array.newInstance(Entry.class, n);
    }
}


public class MyRobot extends BCAbstractRobot {
	public int turn;

	public Action turn() {
		turn++;
		//initializing all the maps
		boolean[][] terrainMap = getPassableMap(); //obtaining terrain map
		int[][] robotMap=getVisibleRobotMap(); //obtaining robots in view
		boolean[][] karboniteMap=getKarboniteMap(); 
		boolean[][] fuelMap=getFuelMap();
		
		
		// The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
					//directions = [(0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)];

		if (me.unit == SPECS.CASTLE) {
			//decide what to build
			
					if (turn == 1) {
						log("Building a pilgrim.");
						return buildUnit(SPECS.PILGRIM,1,0);
					}
		}

		if (me.unit== SPECS.CHURCH) {
			//decide what to build

		}

		
		if (me.unit== SPECS.CRUSADER) {
			//decide whether to move or attack
			//soldier

		}

		
		if (me.unit== SPECS.PROPHET) {
			//decide whether to move or attack
			//soldier

		}

		
		if (me.unit== SPECS.PREACHER) {
			//decide whether to move or attack
			//soldier

		}
		

		if (me.unit == SPECS.PILGRIM) {
			//decide whether to move or collect
			//worker
			

				
			}
		}
	
	
	
	public class soldier() {
		//has to decide whether to attack or to move
		
		//if this unit has been designated DEFENSIVE, forms square around castles
			// and then churches and then stays put
		
		//else if unit is OFFENSIVE
		//if castle reports large number of enemies moving in, pull back, form 
			//defensive swarm
		
		
		//attack
		//how many enemy units are there, how many friendly
		
		//if more friendly then enemy, attack, else retreat to where castle has 
			//reported larger concentration of friendlies
		
		//can we see the type of the enemy units?
	}
	
	public class worker() {
		//has to decide whether to mine or move
		
		//if protected, ie more friendly than enemy soldiers nearby, can pick up 
			//resources otherwise retreat
		//if standing on resources, pick them up
		//have to choose between going after fuel or karbonite
			//we can do this by first choosing the resource closest, then determine
			//path to closest other type of resource, if church is considerably closer
			//and first resource is low, return to church, otherwise fill up on
			//other resource then return to church
		//if not standing on resources, identify closest source and if it is PROTECTED
			//move to it
		
		//if one tank is at 75%, consider moving to next resource, if both, return
		
		
	}
	
	//PROTECTED will have to be designated and sent out by castles maybe? somehow
		//idnetify which tiles are in our sphere of influence, ie there is a church
		//and all churches must have guards
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	//MOVEMENT CLASSES
	
	
	/**Tile of the map, had an x and y position, and boolean traversible
	 * indicating if the terrain is traversible, and color, red for enemy,
	 * green for friendly, blue for carbonite, red for Fuel, grey for empty,
	 * black for unknown   
	 */
	public static class Tile() {
		int x;
		int y;
		boolean traversible;
		String color;
		
		/**Constructor
		 * 
		 */
		public Tile(int x, int y) {
			x=x;
			y=y;
			
			traversible=terrainMap[x][y];  //traversible indicates whether or not the tile
				//can be traversed
			int id= robotMap[x][y];
			
			//the tile is empty
			if (id==0) {
				if (karboniteMap[x][y]==true) {
					color=blue;
				}
				else if (fuelMap[x][y]==true) {
					color=red;
				}
				else {
					color=grey;
				}
			}
			//if the tile is not visible (too far)
			else if(id==-1) {
				color=black;
			}
			//if the tile has a robot on it
			else {
				if (getRobot(id).team==me.team) {
					color=green;
				}
				else {
					color=red;
				}
			}
		}
		
		
	}
	
	
	/** An instance contains information about a Tile: the previous Tile
     *  on a shortest path from the start Tile to this Tile and the distance
     *  of this Tile from the start Tile. */
	//creds to Proffessor Gries
    public static class SFdata {
        private Tile backPointer; // backpointer on path from start Tile to this one
        private int distance; // distance from start node to this one

        /** Constructor: an instance with distance d from the start node and
         *  backpointer p.*/
        private SFdata(int d, Tile p) {
            distance= d;     // Distance from start node to this one.
            backPointer= p;  // Backpointer on the path (null if start node)
        }

        /** return a representation of this instance. */
        public String toString() {
            return "dist " + distance + ", bckptr " + backPointer;
        }
    }
    
    /** Return the path from the start node to node end.
     *  Precondition: nData contains all the necessary information about
     *  the path. */
    public static List<Tile> constructPath(Tile end, HashMap<Tile, SFdata> nData) {
        LinkedList<Tile> path= new LinkedList<Tile>();
        Tile p= end;
        // invariant: All the Tiles from p's successor to the end are in
        //            path, in reverse order.
        while (p != null) {
            path.addFirst(p);
            p= nData.get(p).backPointer;
        }
        return path;
    }
    
    
    
    public static List<Tile> shortestPath(Tile start, Tile end) {
        // Implement Dijkstras's shortest-path algorithm presented
        

        // The frontier set, as discussed in lecture 20
        Heap<Tile> F= new Heap<Tile>();
        
        HashMap<Tile, SFdata> info= new HashMap<Tile, SFdata>(); //map to 
        	//contain each Tile and their backpointer and distance to the start

        F.add(start, 0);
        info.put(start, new SFdata(0, null));
        // inv: See Piazza note Assignment A6 (Fall 2018), 
        //      together with def of F and info
        while (F.size() != 0) {
            Tile f= F.poll();
            if (f == end) return constructPath(end, info);
            int fDist= info.get(f).distance;
            
            for (Edge e : f.getExits()) {// for each neighbor w of f
                Node w= e.getOther(f);
                int newWdist= fDist + e.length;
                SFdata wInfo= info.get(w);
                if (wInfo == null) { //if w not in F or S
                    info.put(w, new SFdata(newWdist,f));
                    F.add(w, newWdist);
                } else if (newWdist < wInfo.distance) {
                    wInfo.distance= newWdist;
                    wInfo.backPointer= f;
                    F.changePriority(w, newWdist);
                }
            }
        }

        // no path from v to end
        
        return new LinkedList<Node>(); // no path found
    }
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		return null;

	}

