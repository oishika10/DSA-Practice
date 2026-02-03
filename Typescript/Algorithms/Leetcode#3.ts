function getAlphabetPosition(alphabet: string) {
  return alphabet.charCodeAt(0) - 97;
}

function lengthOfLongestSubstringBruteForce(s: string): number {
  let result: number = 0;
  for (let i = 0; i < s.length; i++) {
    // Every possible starting index
    let visited: boolean[] = Array(26).fill(false);
    for (let j = i; j < s.length; j++) {
      // Every possible ending index
      if (visited[getAlphabetPosition(s[j])]) {
        break;
      } else {
        visited[getAlphabetPosition(s[j])] = true;
        result = Math.max(result, j - i + 1);
      }
    }
  }
  return result;
}

console.log("Length of longest substring using Brute Force");
console.log(lengthOfLongestSubstringBruteForce("abcabcbb"));
console.log(lengthOfLongestSubstringBruteForce("bbbbb"));
console.log(lengthOfLongestSubstringBruteForce("pwwkew"));

function lengthOfLongestSubstringSlidingWindow(s: string): number {
  let i: number = 0;
  let j: number = 0;
  let visited: boolean[] = Array(26).fill(false);
  let result: number = 0;
  while (j < s.length) {
    while (visited[getAlphabetPosition(s[j])]) {
      visited[getAlphabetPosition(s[i])] = false;
      i += 1;
    }
    visited[getAlphabetPosition(s[j])] = true;
    result = Math.max(result, j - i + 1);
    j += 1;
  }
  return result;
}

console.log("Length of longest substring using Sliding Window");
console.log(lengthOfLongestSubstringSlidingWindow("abcabcbb"));
console.log(lengthOfLongestSubstringSlidingWindow("bbbbb"));
console.log(lengthOfLongestSubstringSlidingWindow("pwwkew"));
