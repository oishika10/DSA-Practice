class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val?: number, next?: ListNode | null) {
    this.val = val === undefined ? 0 : val;
    this.next = next === undefined ? null : next;
  }
}

function mergeTwoLists(
  list1: ListNode | null,
  list2: ListNode | null,
): ListNode | null {
  if (!list1) {
    return list2;
  }

  if (!list2) {
    return list1;
  }

  let newList: ListNode = new ListNode();
  let referenceNodeList1: ListNode | null = list1;
  let referenceNodeList2: ListNode | null = list2;
  let referenceNodeNewList = newList;

  while (referenceNodeList1 && referenceNodeList2) {
    // logic
    if (referenceNodeList1.val <= referenceNodeList2.val) {
      referenceNodeNewList.next = referenceNodeList1;
      referenceNodeList1 = referenceNodeList1.next;
      referenceNodeNewList = referenceNodeNewList.next;
    } else {
      referenceNodeNewList.next = referenceNodeList2;
      referenceNodeList2 = referenceNodeList2.next;
      referenceNodeNewList = referenceNodeNewList.next;
    }
  }

  while (referenceNodeList1) {
    referenceNodeNewList.next = referenceNodeList1;
    referenceNodeList1 = referenceNodeList1.next;
    referenceNodeNewList = referenceNodeNewList.next;
  }

  while (referenceNodeList2) {
    referenceNodeNewList.next = referenceNodeList2;
    referenceNodeList2 = referenceNodeList2.next;
    referenceNodeNewList = referenceNodeNewList.next;
  }

  return newList.next;
}
