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

		

		return null;

	}
}
