package bc19;

public class MyRobot extends BCAbstractRobot {
	public int turn;

	public Action turn() {
		turn++;
		
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

		return null;

	}
}
