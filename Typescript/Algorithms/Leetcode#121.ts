function maxProfitBruteForce(prices: number[]): number {
  let profit = 0;
  for (let i = 0; i < prices.length; i++) {
    for (let j = i + 1; j < prices.length; j++) {
      profit = Math.max(profit, prices[j] - prices[i]);
    }
  }
  return profit;
}

console.log("Best Time to Buy and Sell Stock Brute Force");
console.log(maxProfitBruteForce([7, 1, 5, 3, 6, 4]));
console.log(maxProfitBruteForce([7, 6, 4, 3, 1]));

function maxProfitUsingPointers(prices: number[]): number {
  let profit = 0;
  let left = 0;
  let right = 1;
  while (left < right && right < prices.length) {
    if (prices[right] - prices[left] <= 0) {
      left = right;
      right += 1;
    } else if (prices[right] - prices[left] > 0) {
      profit = Math.max(profit, prices[right] - prices[left]);
      right += 1;
    }
  }
  return profit;
}

console.log("Best Time to Buy and Sell Stock Using Pointers");
console.log(maxProfitUsingPointers([7, 1, 5, 3, 6, 4]));
console.log(maxProfitUsingPointers([7, 6, 4, 3, 1]));
