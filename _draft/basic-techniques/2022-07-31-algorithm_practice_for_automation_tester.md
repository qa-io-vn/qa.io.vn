---
layout: post
title:  "Algorithm practice for automation tester"
author: toronto22
categories: [ automation test]
image: assets/images/6.jpg
---

As an automation tester, I want to implement the automation script fast as fast I can. So algorithm is the essential skill that needed to strengthen. I practice the algorithm skill, I choose Leetcode.com site.

## Collections

### Hashmap

1. [Number of Good Pairs](https://leetcode.com/problems/number-of-good-pairs/) (Easy - 9m - 90.46% - 67.4%)
2. [Jewels and Stones](https://leetcode.com/problems/jewels-and-stones/) (Easy - 8m - 60.04% - 70.21%)
3. [How Many Numbers Are Smaller Than the Current Number](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/) (Easy - 7m - 55.78% - 65.54%)
4. [Decode the Message](https://leetcode.com/problems/decode-the-message/) (Easy - 18m - 66.68% - 41.52%)
5. [Number of Arithmetic Triplets](https://leetcode.com/problems/number-of-arithmetic-triplets/) (Easy - 8m - 85.71% - 39.07%)
6. [Unique Morse Code Words](https://leetcode.com/problems/unique-morse-code-words/) (Easy - 14m - 20.83% - 44.14%)
7. [Count Number of Pairs With Absolute Difference K](https://leetcode.com/problems/count-number-of-pairs-with-absolute-difference-k/) (Easy - 6m - 12.73% - 82.77%)
8. [Count the Number of Consistent Strings](https://leetcode.com/problems/count-the-number-of-consistent-strings/) (Easy - 10m - 42.28% - 55.86%)
9. [Rings and Rods](https://leetcode.com/problems/rings-and-rods/) (Easy - 18m - 12.94% - 30.47%)
10. [Check if the Sentence Is Pangram](https://leetcode.com/problems/check-if-the-sentence-is-pangram/) (Easy - 7m - 47.47% - 95.60%)
11. [Destination City](https://leetcode.com/problems/destination-city/) (Easy - 12m - 57.93% - 64.58%)
12. [First Letter to Appear Twice](https://leetcode.com/problems/first-letter-to-appear-twice/) (Easy - 6m - 63.62% - 27.32%)






# My Solution

Number of Good Pairs (Easy - 9m - 90.46% - 67.4% - 1)
```js
class Solution {
    public int numIdenticalPairs(int[] nums) {
        int numGoodPairs = 0;
        HashMap<Integer, Integer> map = new HashMap<>();
        for(int i =0;i<nums.length;i++){
            if(map.containsKey(nums[i])){
                int count = map.get(nums[i]);
                numGoodPairs+=count;
                map.put(nums[i],count+1);
            } else {
                map.put(nums[i],1);
            }
        }
        return numGoodPairs;
    }
}
```

Jewels and Stones (Easy - 8m - 60.04% - 70.21%)
```js
class Solution {
    public int numJewelsInStones(String jewels, String stones) {
        int result = 0;
        List<Character> jewelTypes = new ArrayList<Character>();
        for(int i=0;i<jewels.length();i++){
            jewelTypes.add(jewels.charAt(i));
        }
        
        for(int i=0;i<stones.length();i++){
            if(jewelTypes.contains(stones.charAt(i))) result++;
        }
        return result;
    }
}
```

How Many Numbers Are Smaller Than the Current Number
```js
class Solution {
    public int[] smallerNumbersThanCurrent(int[] nums) {
        int size = nums.length;
        int[] results = new int[size];
        for(int i=0;i<nums.length;i++){
            int count=0;
            for(int j=0;j<nums.length;j++){
                if(nums[i]>nums[j]) count++;
            }
            results[i]=count;
        }
        return results;
    }
}
```
