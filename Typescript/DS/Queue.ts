class Queue {
  private head: number = 0;
  private tail: number = 0;
  private capacity: number = 0;
  private queue: number[];
  private length: number = 0;

  constructor(capacity: number) {
    if (capacity <= 0) {
      throw Error("Capacity must be greater than 0");
    }

    this.queue = new Array<number>(capacity).fill(0);
    this.capacity = capacity;
  }

  public enqueue(element: number) {
    if (this.length >= this.capacity) {
      throw Error("Queue at full capacity, cannot accept any more items");
    }

    this.length += 1;
    this.queue[this.tail] = element;
    this.tail = (this.tail + 1) % this.capacity;
  }

  public dequeue() {
    if (this.length === 0) {
      throw Error("Queue has no items, there is nothing to dequeue");
    }

    this.length -= 1;
    const currHead = this.queue[this.head];
    this.head = (this.head + 1) % this.capacity;

    return currHead;
  }

  public getLength(): number {
    return this.length;
  }
}
