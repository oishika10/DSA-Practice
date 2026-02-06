function printKnapsackTest(
  testName: string,
  profit: number[],
  weight: number[],
  capacity: number,
) {
  console.log("=".repeat(50));
  console.log(`🧪 ${testName}`);
  console.log("-".repeat(50));

  console.log("Inputs:");
  console.log("  Profit:  ", profit);
  console.log("  Weight:  ", weight);
  console.log("  Capacity:", capacity);

  console.log();
  console.log("Brute Force Solution:");
  const brute = knapSackBruteForce(capacity, profit, weight, profit.length);
  console.log("  → Max Profit:", brute);

  console.log();
  console.log("Dynamic Programming Solution:");
  const dp = knapSackDynamicProgramming(capacity, profit, weight);
  console.log("  → Max Profit:", dp);

  console.log();
  console.log("Result Match:", brute === dp ? "✅ YES" : "❌ NO");
  console.log("=".repeat(50));
  console.log();
}

function knapSackBruteForce(
  capacity: number,
  profit: number[],
  weight: number[],
  n: number,
): number {
  if (capacity == 0 || n == 0) {
    return 0;
  }

  let withoutNthItem = 0;
  let withNthItem = 0;
  if (weight[n - 1] > capacity) {
    withoutNthItem = knapSackBruteForce(capacity, profit, weight, n - 1);
  } else {
    withNthItem =
      knapSackBruteForce(capacity - weight[n - 1], profit, weight, n - 1) +
      profit[n - 1];
  }

  return Math.max(withoutNthItem, withNthItem);
}

/**
 * Dynamic Programming Table (dp):
 *
 * dp is a 2D table with (n + 1) rows and (W + 1) columns.
 *
 * - Rows (i = 0 to n):
 *   Each row represents how many items we are allowed to consider.
 *   Row i means we are only allowed to use the first i items.
 *   Row 0 represents the base case where no items are considered.
 *
 * - Columns (w = 0 to W):
 *   Each column represents the current weight capacity of the knapsack.
 *   Column w means the knapsack can carry at most w units of weight.
 *   Column 0 represents the base case where the knapsack has zero capacity.
 *
 * - Cell meaning:
 *   dp[i][w] stores the maximum total value that can be achieved
 *   by choosing from the first i items such that the total weight
 *   of the chosen items does NOT exceed w.
 *
 * How values are filled:
 * - If the i-th item is not included, dp[i][w] is equal to dp[i - 1][w]
 *   (same capacity, but one fewer item to choose from).
 *
 * - If the i-th item is included (only possible when its weight <= w),
 *   dp[i][w] is the value of item i plus dp[i - 1][w - weight[i]],
 *   which represents the best value achievable with the remaining capacity.
 *
 * - dp[i][w] is the maximum of these two choices.
 *
 * Final answer:
 * - The maximum value achievable with all items and full capacity
 *   is stored in dp[n][W].
 */

function knapSackDynamicProgramming(
  capacity: number,
  profit: number[],
  weight: number[],
): number {
  let dpTable: number[][] = [];
  let numberOfItems: number = profit.length;

  // The 0th row means that there are no items considered for that row.
  for (let i = 0; i < numberOfItems + 1; i++) {
    dpTable.push(new Array(capacity + 1).fill(0));
  }

  for (let i = 1; i <= numberOfItems; i++) {
    for (let j = 1; j <= capacity; j++) {
      if (weight[i - 1] > j) {
        // this means we cannot take this item
        dpTable[i][j] = dpTable[i - 1][j];
      } else {
        // this means we can take this item
        const remainingWeight = j - weight[i - 1];
        if (remainingWeight < 0) {
          dpTable[i][j] = dpTable[i - 1][j];
        } else {
          dpTable[i][j] = Math.max(
            dpTable[i - 1][j],
            dpTable[i - 1][j - weight[i - 1]] + profit[i - 1],
          );
        }
      }
    }
  }

  return dpTable[numberOfItems][capacity];
}

printKnapsackTest("Classic Knapsack Example", [60, 100, 120], [10, 20, 30], 50);

printKnapsackTest("Small Capacity Example", [1, 6, 10, 16], [1, 2, 3, 5], 7);

printKnapsackTest("Nothing Fits", [10, 20, 30], [5, 10, 15], 4);
