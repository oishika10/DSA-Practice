function isPalindrome(s: string): boolean {
  let start = 0;
  let end = s.length - 1;
  let isPalindrome: boolean = true;
  while (start < end) {
    if (s[start] !== s[end]) {
      isPalindrome = false;
      break;
    }
    start += 1;
    end -= 1;
  }
  return isPalindrome;
}

function longestPalindromeBruteForce(s: string): string {
  let maxString = s[0];
  for (let i = 0; i < s.length; i++) {
    for (let j = i + 1; j < s.length; j++) {
      const subString: string = s.slice(i, j + 1);
      if (isPalindrome(subString)) {
        if (subString.length > maxString.length) {
          maxString = subString;
        }
      }
    }
  }
  return maxString;
}

console.log("Longest palindromic string");
console.log(longestPalindromeBruteForce("babad"));
console.log(longestPalindromeBruteForce("cbbd"));

/**
 *  The main idea behind the approach is that if we know the status (i.e., palindrome or not) of the substring ranging [i, j], 
 * we can find the status of the substring ranging [i-1, j+1] by only matching the character str[i-1] and str[j+1].
    If the substring from i to j is not a palindrome, then the substring from i-1 to j+1 will also not be a palindrome.
    Otherwise, it will be a palindrome only if str[i-1] and str[j+1] are the same.
    Based on this fact, we can create a 2D table (say table[][] which stores status of substring str[i . . . j] ), and check for substrings with length from 1 to n. 
    For each length find all the substrings starting from each character i and find if it is a palindrome or not using the above idea. 
    The longest length for which a palindrome formed will be the required answer.
 */
function longestPalindromeDP(s: string): string {
  let maxString = s[0];
  let dpArray: boolean[][] = [];
  let maxLen = 1;
  let start = 0;

  for (let i = 0; i < s.length; i++) {
    dpArray.push(new Array(s.length).fill(false));
  }

  // String of length 1 is always a palindrome
  for (let i = 0; i < s.length; i++) {
    dpArray[i][i] = true;
  }

  // String of length 2 may or may not be a palindrome
  for (let i = 0; i < s.length - 1; i++) {
    if (s[i] === s[i + 1]) {
      dpArray[i][i + 1] = true;
      maxLen = 2;
      start = i;
    }
  }

  // We can only start filling the dpArray starting with string of length 3
  // since we calculated those before.
  for (let len = 3; len <= s.length; len++) {
    for (let i = 0; i + len - 1 < s.length; i++) {
      let j = i + len - 1;
      if (s[i] === s[j] && dpArray[i + 1][j - 1] == true) {
        dpArray[i][j] = true;
        if (maxLen < j - i + 1) {
          maxLen = len;
          start = i;
        }
      }
    }
  }

  return s.slice(start, start + maxLen);
}

console.log("Longest palindromic string");
console.log(longestPalindromeDP("babad"));
console.log(longestPalindromeDP("cbbd"));
