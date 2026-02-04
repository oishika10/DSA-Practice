function twoSumBruteForce(nums: number[], target: number): number[] {
  let indices: number[] = [];
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] == target) {
        indices.push(i);
        indices.push(j);
        return indices;
      }
    }
  }
  return indices;
}

console.log("Two Sum Brute Force");
console.log(twoSumBruteForce([2, 7, 11, 15], 9));
console.log(twoSumBruteForce([3, 2, 4], 6));
console.log(twoSumBruteForce([3, 3], 6));
console.log(twoSumBruteForce([3, 4], 6));
console.log(twoSumBruteForce([3, 4], 99));

function twoSumBruteEfficient(nums: number[], target: number): number[] {
  let numsIndices: Map<number, number> = new Map();
  for (let i = 0; i < nums.length; i++) {
    numsIndices.set(nums[i], i);
  }

  for (let i = 0; i < nums.length; i++) {
    const otherNumber: number | undefined = numsIndices.get(target - nums[i]);
    if (otherNumber) {
      return [i, otherNumber];
    }
  }
  return [];
}

console.log("Two Sum Efficient");
console.log(twoSumBruteForce([2, 7, 11, 15], 9));
console.log(twoSumBruteForce([3, 2, 4], 6));
console.log(twoSumBruteForce([3, 3], 6));
console.log(twoSumBruteForce([3, 4], 6));
console.log(twoSumBruteForce([3, 4], 99));
