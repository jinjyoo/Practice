return (i > 0) ? dp[j] - dp[i-1] : dp[j];

/* Multiple intialization */
int a = 0, b = 0;
String one, two, three;
one = two = three = "";  // only for immutables


/* Golfing */
if((v = someMethod()) != 0) return true;
maxCur = Math.max(0, maxCur += prices[i] - prices[i-1]);


// Arrays:
arr.clone()
Arrays.sort(coins, Collections.reverseOrder()); //https://stackoverflow.com/questions/1694751/java-array-sort-descending
Arrays.fill(array, -1);
Arrays.binarySearch(arr, start, end, x)

// https://stackoverflow.com/questions/12231453/syntax-for-creating-a-two-dimensional-array
int[][] multi = new int[5][10];  // 5x10
int marks[][]={{50,60,55,67,70},{62,65,70,70,81},{72,66,77,80,69}};  // 3 x 5
int[][] multi = new int[5][];  // variable lengths
multi[0] = new int[10]; 
multi[1] = new int[6]; 
multi[2] = new int[9] 


//Initializing array: https://stackoverflow.com/questions/3160347/java-how-initialize-an-array-in-java-in-one-line
int[] arraylists = {1, 2, 3, 4, 5, 6, ,7, 8};  // works
array = {1, 1, 1, 1, 2, 5, ,7, 8}; // doesn't work
array = new int[] {1, 1, 2, 3, 5, 8};  // works


//Lists
ArrayList
lis.set(i, lis.get(i)+1);   // incrementing for arraylists


//Maps
Map<String, Integer> map = new HashMap<String,Integer>();
if(map.containsKey(key))
    map.get(key)++;
else
    map.put(key, 1);
// https://stackoverflow.com/questions/6802483/how-to-directly-initialize-a-hashmap-in-a-literal-way
HashMap<String, String> h = new HashMap<String, String>() {{
    put("a","b"); // first brace creates anonymous class, second brace initializes
}};  /* NOTE: just use put, not h.put */


// Iterators
for (Iterator<String> i = someList.iterator(); i.hasNext();)


/* Don't use this */
public class Pair<L, R> { // https://stackoverflow.com/questions/521171/a-java-collection-of-value-pairs-tuples

	private final L left;
	private final R right;

	public Pair(L left, R right) {
		this.left = left;
		this.right = right;
	}

	public L getLeft() { return left; }
	public R getRight() { return right; }

	@Override
	public int hashCode() { 
		// return left.hashCode() ^ right.hashCode();   // this means a^b has same hash as b^a...
		long l = left.hashCode() * 2654435761L; 
		return (int)l + (int)(l >>> 32) + right.hashCode();
	}  

	@Override
	public boolean equals(Object o) {
		if (!(o instanceof Pair)) return false;
		Pair pairo = (Pair) o;
		return this.left.equals(pairo.getLeft()) &&
		       this.right.equals(pairo.getRight());
	}

}

// Practice: https://www.compilejava.net/
import java.lang.Math; // headers MUST be above the first class

public class HelloWorld {
  public static void main(String[] args) {
    int[] dp = new int[5];
    System.out.println(dp[0]);
  }
  
}


