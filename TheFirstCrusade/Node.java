
public class Node {
        Node parent;
        int x;
        int y;
        double g; double h; double f;

        public Node(int x, int y, Node parent) {
            this.parent = parent;
            this.x = x;
            this.y = y;
        }
    }