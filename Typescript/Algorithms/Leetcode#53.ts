function maxSubArray(nums: number[]): number {
  // Stores the result (maximum sum found so far)
  let res = nums[0];

  // Maximum sum of subnumsay ending at current position
  let maxEnding = nums[0];

  for (let i = 1; i < nums.length; i++) {
    // Either extend the previous subnumsay or start
    // new from current element
    maxEnding = Math.max(maxEnding + nums[i], nums[i]);

    // Update result if the new subarray sum is larger
    res = Math.max(res, maxEnding);
  }
  return res;
}
