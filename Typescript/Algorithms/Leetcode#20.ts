function isValid(s: string): boolean {
  const openers: Array<string> = ["[", "{", "("];
  let stack: Array<string> = [];
  for (let i = 0; i < s.length; i++) {
    if (openers.includes(s[i])) {
      stack.push(s[i]);
    } else {
      if (s[i] === ")") {
        if (stack.pop() !== "(") {
          return false;
        }
      } else if (s[i] == "}") {
        if (stack.pop() !== "{") {
          return false;
        }
      } else {
        // s[i] == "]"
        if (stack.pop() !== "[") {
          return false;
        }
      }
    }
  }
  return stack.length === 0;
}

console.log(isValid("()"));
console.log(isValid("()[]{}"));
console.log(isValid("(]"));
console.log(isValid("([])"));
console.log(isValid("([)]"));
