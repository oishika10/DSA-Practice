class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;

  constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
    this.val = val === undefined ? 0 : val;
    this.left = left === undefined ? null : left;
    this.right = right === undefined ? null : right;
  }
}

function maxDepth(root: TreeNode | null): number {
  if (root == null) {
    return 0;
  }

  return Math.max(maxDepth(root.left) + 1, maxDepth(root.right) + 1);
}

const root1 = new TreeNode(3);
root1.left = new TreeNode(9);
root1.right = new TreeNode(20);

root1.right.left = new TreeNode(15);
root1.right.right = new TreeNode(7);

console.log("Calculate max depth of tree");
console.log(maxDepth(root1));

const root2 = new TreeNode(1);
root2.right = new TreeNode(2);

root2.right.left = new TreeNode(15);
console.log(maxDepth(root2));

export {};
