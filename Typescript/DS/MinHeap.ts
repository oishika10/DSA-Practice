class MinHeap {
  private elements: number[];

  constructor() {
    this.elements = new Array<number>();
  }

  private heapifyBottomUp(): void {
    let i: number = this.getLength() - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (this.elements[parent] > this.elements[i]) {
        [this.elements[i], this.elements[parent]] = [
          this.elements[parent],
          this.elements[i],
        ];
        i = parent;
      } else {
        break;
      }
    }
  }

  private heapifyTopDown(): void {
    let i = 0;
    const length = this.elements.length;

    while (2 * i + 1 < length) {
      const left = 2 * i + 1;
      const right = 2 * i + 2;

      let smallest = left;

      if (right < length && this.elements[right] < this.elements[left]) {
        smallest = right;
      }

      if (this.elements[i] <= this.elements[smallest]) break;

      [this.elements[i], this.elements[smallest]] = [
        this.elements[smallest],
        this.elements[i],
      ];

      i = smallest;
    }
  }

  public enqueue(element: number) {
    // Step 1: Add the element to the end
    this.elements.push(element);

    // Step 2: Heapify the heap
    this.heapifyBottomUp();
  }

  public dequeue(): number {
    if (this.elements.length === 0) {
      throw new Error("Heap is empty");
    }

    const minimumValue = this.elements[0];
    this.elements[0] = this.elements[this.getLength() - 1];
    this.elements.pop();
    this.heapifyTopDown();
    return minimumValue;
  }

  public getLength(): number {
    return this.elements.length;
  }
}
