function lengthOfLongestSubstringBruteForce(s: string): number {
  let result: number = 0;
  for (let i = 0; i < s.length; i++) {
    // Every possible starting index
    let visited: boolean[] = Array(26).fill(false);
    for (let j = i; j < s.length; j++) {
      // Every possible ending index
      if (visited[s[j].charCodeAt(0) - 97]) {
        break;
      } else {
        visited[s[j].charCodeAt(0) - 97] = true;
        result = Math.max(result, j - i + 1);
      }
    }
  }
  return result;
}

console.log(lengthOfLongestSubstringBruteForce("abcabcbb"));
console.log(lengthOfLongestSubstringBruteForce("bbbbb"));
console.log(lengthOfLongestSubstringBruteForce("pwwkew"));
