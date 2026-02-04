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

function printPreOrderTreeTraversal(root: TreeNode | null) {
  if (root == null) {
    return;
  }

  console.log(root.val);
  printPreOrderTreeTraversal(root.left);
  printPreOrderTreeTraversal(root.right);
}

function invertTree(root: TreeNode | null): TreeNode | null {
  // base case
  if (root === null) {
    return null;
  }

  // recursive logic
  if (root.left) {
    invertTree(root.left);
  }

  if (root.right) {
    invertTree(root.right);
  }

  if (root.left && root.right) {
    const leftTree = root.left;
    root.left = root.right;
    root.right = leftTree;
  }

  return root;
}

const root1 = new TreeNode(4);
root1.left = new TreeNode(2);
root1.right = new TreeNode(7);

root1.left.left = new TreeNode(1);
root1.left.right = new TreeNode(3);

root1.right.left = new TreeNode(6);
root1.right.right = new TreeNode(9);

console.log("Root 1 before inversion");
printPreOrderTreeTraversal(root1);
invertTree(root1);
console.log("Root 1 after inversion");
printPreOrderTreeTraversal(root1);

// Tree for: [2,1,3]
const root2 = new TreeNode(2);
root2.left = new TreeNode(1);
root2.right = new TreeNode(3);

console.log("Root 2 before inversion");
printPreOrderTreeTraversal(root2);
invertTree(root2);
console.log("Root 2 after inversion");
printPreOrderTreeTraversal(root2);
