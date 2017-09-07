// From CTCI
int binarySearch(int[] a, int x) {
    int low = 0;
    int high = a.length-1;
    int mid;
    while (low <= high) {
        mid = (low + high) / 2;
        if (a[mid] < x) {
            low = mid + 1;
        } else if (a[mid] > x) {
            high = mid - 1;
        } else {
            return mid;
        }
    }
    return -1; // Error
}

static int binary(int key, int[] array) {
    int lo = 0;
    int hi = array.length - 1;    //different
    while (lo <= hi) {            //different  // the target is in range [low, high]
        int mid = (lo + hi) / 2;  //favors low
        if (array[mid] <= key) {  // ### NOTE that we include equality, and return low at end, instead of mid (see 3-4)
            lo = mid + 1;         //different
        } else {
            hi = mid - 1;
        }
    }
    return lo;                    
}

static int binary(int key, int[] array){
    int lo = 0;
    int hi = array.length;            //different
    while (lo < hi) {                 //different  // the target is in range [low, high)
        int mid = (lo + hi) / 2; 
        if (array[mid] <= key) {
            lo = mid + 1; 
        } else {
            hi = mid;                 //different
        }
    }
    return lo;
}

// Ex. 3-4  https://leetcode.com/articles/guess-number-higher-or-lower/   #Straightforward binary search
public int guessNumber(int n) { // Not optimized
    int low = 1;
    int high = n;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        int res = guess(mid);
        if (res == 0)
            return mid;
        else if (res < 0)
            high = mid - 1;
        else
            low = mid + 1;
    }
    return -1;
}

public int guessNumber(int n) { // optimized
    int low = 1;
    int high = n;
    while (low < high) {
        int mid = (low + high) >>> 1;
        if (guess(mid) <= 0)
            high = mid;
        else
            low = mid + 1;
    }
    return low;
}

