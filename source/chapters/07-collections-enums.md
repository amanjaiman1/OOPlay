@sheet | Ch 07 · Why collections?

@chapter 07 | COLLECTIONS • VECTOR • ENUMS | why collections · the framework map · List · Set · Queue · Map · Vector & synchronization · enums | 🎬 OOP 7

# ✦ WHY COLLECTIONS? ✦

## ❓ WHY? — what arrays can't do

- **fixed size** — decided at creation (we hacked around it with our own ArrayList in Ch 06)
- no built-in add / remove / search / "contains" / sort-for-objects — you write the loops
- one shape only: an indexed row. Real problems want *unique items*, *first-come-first-served*, *look up by name* …

## 🌍 IN REAL LIFE — different containers for different jobs

```sketch
   a numbered SHELF      →  keeps order, allows duplicates     →  List
   a STAMP ALBUM         →  each stamp only once               →  Set
   a TICKET-COUNTER LINE →  first come, first served           →  Queue
   a DICTIONARY          →  look up a meaning by its word      →  Map
```

:::define
The [[b:Collections Framework]] (`java.util`) is a unified architecture for storing and manipulating groups of objects: **interfaces** (what a container can do), **implementations** (how it does it) and **algorithms** (`Collections.sort`, `max`, `reverse` …).
:::

:::idea
It's every earlier chapter working together: **interfaces** (`List`) + **generics** (`List<Integer>`) + **polymorphism** (`List<Integer> l = new ArrayList<>()`) + **abstraction** (you never see the resize code).
:::

@sheet | Ch 07 · The framework map

# ✦ THE COLLECTIONS MAP ✦

@@must

```sketch
                          Iterable            ← anything you can for-each
                             │
                        Collection
             ┌───────────────┼────────────────┐
             ↓               ↓                ↓
           List             Set             Queue
             │               │                │
        ArrayList         HashSet        PriorityQueue
        LinkedList ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ → (also a Queue/Deque)
        Vector         LinkedHashSet      ArrayDeque
          └ Stack         TreeSet


                            Map               ← NOT a Collection!
               ┌─────────────┼──────────────┐
            HashMap    LinkedHashMap      TreeMap
```

| interface | promise | go-to class |
|---|---|---|
| `List` | ordered, index-based, duplicates ✓ | `ArrayList` |
| `Set` | no duplicates | `HashSet` (`TreeSet` = sorted) |
| `Queue` | FIFO: add at the back, take from the front | `ArrayDeque`, `LinkedList` |
| `Map` | key → value pairs, keys unique | `HashMap` (`TreeMap` = sorted keys) |

:::aside
List = **order**<br>Set = **unique**<br>Queue = **FIFO**<br>Map = **lookup**
:::

## ✍️ Program to the interface

```java
List<Integer> list = new ArrayList<>();    // ✓ reference type = interface
// later: new LinkedList<>() or new Vector<>() — nothing else changes
```

:::trap
[[r:`Map` does not extend `Collection`]] — `Collection<String> c = new HashMap<>();` ✗ "incompatible types". A map stores **pairs**, not single elements. (Loop it with `map.entrySet()`, `keySet()` or `values()`.)
:::

:::trap
`Collection` ≠ `Collections`. `Collection` is the root **interface**; `Collections` is a **utility class** of static helpers: `Collections.sort(list)`, `Collections.max(list)`, `Collections.synchronizedList(…)`.
:::

@sheet | Ch 07 · List, Set, Queue, Map

# ✦ THE BIG FOUR — QUICK TOUR ✦

```java "Main.java" run
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();      // order + duplicates
        list.add(34); list.add(78); list.add(34);
        list.remove(Integer.valueOf(78));            // remove by VALUE
        System.out.println(list + " first=" + list.get(0));

        Set<String> set = new HashSet<>();           // no duplicates
        set.add("java"); set.add("java"); set.add("dsa");
        System.out.println(set.size() + " " + set.contains("dsa"));

        Queue<String> queue = new LinkedList<>();    // FIFO
        queue.offer("A"); queue.offer("B"); queue.offer("C");
        System.out.println(queue.poll() + " " + queue);

        Map<String, Integer> marks = new HashMap<>();   // key → value
        marks.put("Kunal", 89);
        marks.put("Rahul", 95);
        marks.put("Kunal", 99);                      // same key → replaced
        System.out.println(marks.get("Kunal") + " " + marks.size());
    }
}
```

```output
[34, 34] first=34
2 true
A [B, C]
99 2
```

## 🧠 ArrayList vs LinkedList — the picture

```sketch
   ArrayList    [ 10 | 20 | 30 | 40 |    |    ]   one block of memory
                  ↑ get(2) jumps straight there → fast reads
                  insert in the middle → shift everything → slow

   LinkedList   (10) ↔ (20) ↔ (30) ↔ (40)          separate linked nodes
                  get(2) walks node by node → slow reads
                  insert/remove at the ends → just relink → fast
```

## 🧠 Map — the picture

```sketch
        KEY            VALUE
      "Kunal"  ───→     99
      "Rahul"  ───→     95        keys unique · values may repeat
```

:::trap
On a `List<Integer>`, `list.remove(1)` removes the element at **index 1**, not the value 1. `List.of(10, 20, 30)` → `remove(1)` leaves `[10, 30]`. For the value use `list.remove(Integer.valueOf(1))`.
:::

:::reality
`HashSet` / `HashMap` don't keep insertion order (they order by hash buckets — Ch 04's `hashCode`!). Need insertion order → `LinkedHashSet` / `LinkedHashMap`; sorted → `TreeSet` / `TreeMap`.
:::

@sheet vs | Comparison · Collection vs Map

# ✦ COLLECTION [[vs]] MAP ✦

| | `Collection` | `Map` |
|---|---|---|
| Stores | single elements | **key → value** pairs |
| Root of | `List`, `Set`, `Queue` | `HashMap`, `TreeMap`, `LinkedHashMap` |
| Extends `Iterable`? | ✓ — `for (x : coll)` works | ✗ — loop over `entrySet()` / `keySet()` / `values()` |
| Add | `add(e)` | `put(k, v)` |
| Find | `contains(e)` | `get(k)`, `containsKey(k)` |
| Duplicates | `List` ✓, `Set` ✗ | keys ✗ · values ✓ |
| Example | names of all students | roll no. → student |

```java "looping a Map"
// Map.Entry = a nested interface (Ch 05)
for (Map.Entry<String, Integer> e : marks.entrySet()) {
    System.out.println(e.getKey() + " → " + e.getValue());
}
```

:::remember
- `Collection` = a bag of elements · `Map` = a lookup table
- `Map` is part of the Collections **Framework** but not a `Collection`
- `Map.Entry` is the nested interface from Ch 05
:::

@sheet | Ch 07 · Vector & synchronization

# ✦ VECTOR & SYNCHRONIZATION ✦

## 🧠 IDEA

`Vector` is a growable array — like `ArrayList` — but **every method is `synchronized`**: only **one thread at a time** can run a method on the same Vector.

```java "Main.java" run
import java.util.List;
import java.util.Vector;

public class Main {
    public static void main(String[] args) {
        List<Integer> vector = new Vector<>();  // same List API
        vector.add(45);
        vector.add(5);
        vector.add(15);
        vector.add(56);
        System.out.println(vector);
    }
}
```

```output
[45, 5, 15, 56]
```

## 🌍 IN REAL LIFE

A shop with **one billing counter and one token**: one customer at a time — no mixed-up bills, but you wait in line even when the shop is empty (that waiting = locking cost).

```sketch
   ArrayList (not synchronized)      Vector (synchronized)
   Thread 1 ─→ add() ┐               Thread 1 ─→ add()  ✓ holds the lock
   Thread 2 ─→ add() ┴→ corrupt? ✗   Thread 2 ─→ add()  … waits its turn
```

| | `ArrayList` | `Vector` |
|---|---|---|
| Synchronized | ✗ | ✓ every method |
| Speed, single thread | faster | slower (lock on every call) |
| Grows by | ~50 % | 100 % (doubles) |
| Age | Java 1.2 — part of the framework | Java 1.0 — *legacy*, retro-fitted to `List` |
| Default capacity | 10 (allocated on the first `add`) | 10 |
| Today | the default choice | rarely used |

:::reality
@@good Need a thread-safe list today? `Collections.synchronizedList(new ArrayList<>())` or `CopyOnWriteArrayList` (`java.util.concurrent`). And remember: synchronized **methods** don't make **combinations** safe — `if (!v.contains(x)) v.add(x);` can still race between the two calls.
:::

@sheet | Ch 07 · Enums

# ✦ ENUMS ✦

## ❓ WHY? — the problem

```java "risky" bad
String day = "Mondy";     // typo — compiles happily
int size = 7;             // 7 means…? nothing stops invalid values
```

## 🧠 IDEA

An **enum** is a type with a [[o:**fixed**]] set of named values. [[u:The compiler allows *only* those.]]

## 🌍 IN REAL LIFE

A coffee menu: SMALL, MEDIUM, LARGE — you can't order "MEDIUM-ish". A traffic light: RED, YELLOW, GREEN — nothing else.

:::define
An [[b:enum]] is a special class whose instances are a fixed list of [[b:enum constants]] — each one `public static final`, created once by the JVM.
:::

## 💻 EXAMPLE — Basic.java

```java "Basic.java" run
public class Basic {
    interface A { void hello(); }

    enum Week implements A {
        Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday;
        // each constant = a public static final Week object

        Week() {                                 // implicitly private
            System.out.println("Constructor called for " + this);
        }

        @Override
        public void hello() { System.out.println("hey how are you"); }
    }

    public static void main(String[] args) {
        Week week = Week.Monday;      // first use → ALL 7 constants built
        week.hello();
        System.out.println(Week.valueOf("Monday") + " " + week.ordinal());
    }
}
```

```output
Constructor called for Monday
Constructor called for Tuesday
Constructor called for Wednesday
Constructor called for Thursday
Constructor called for Friday
Constructor called for Saturday
Constructor called for Sunday
hey how are you
Monday 0
```

## 🧠 VISUALIZE IT — what the compiler builds

```sketch
   enum Week { Monday, Tuesday, … }

   ≈  final class Week extends java.lang.Enum<Week> {
          public static final Week Monday  = new Week();   // ordinal 0
          public static final Week Tuesday = new Week();   // ordinal 1
          …
          private Week() { … }
      }
```

| method | returns | example |
|---|---|---|
| `values()` | all constants, in order | `for (Week d : Week.values())` |
| `valueOf(String)` | the constant with **exactly** that name | `Week.valueOf("Monday")` |
| `ordinal()` | position from 0 | `Week.Wednesday.ordinal()` → 2 |
| `name()` / `toString()` | the name | `"Monday"` |
| `compareTo()` | order by ordinal | `Monday.compareTo(Friday)` < 0 |

```java "switch on an enum"
switch (week) {
    case Saturday, Sunday -> System.out.println("weekend");
    default               -> System.out.println("work day");
}
```

:::trap
`valueOf` is **case-sensitive**: `Week.valueOf("monday")` → `IllegalArgumentException: No enum constant Basic.Week.monday`.
:::

@sheet | Ch 07 · Enum constructors, methods & inheritance

# ✦ ENUM CONSTRUCTORS, METHODS & INHERITANCE ✦

## 💻 Constants with their own data

```java "Main.java" run
public class Main {
    enum Size {
        SMALL(100), MEDIUM(150), LARGE(200);  // each calls the constructor

        private final int price;              // every constant has its own

        Size(int price) { this.price = price; }

        int getPrice() { return price; }
    }

    public static void main(String[] args) {
        for (Size s : Size.values()) {
            System.out.println(s + " " + s.ordinal()
                               + " price=" + s.getPrice());
        }
        Size mine = Size.valueOf("LARGE");
        System.out.println(mine == Size.LARGE);   // == is safe for enums
    }
}
```

```output
SMALL 0 price=100
MEDIUM 1 price=150
LARGE 2 price=200
true
```

:::rule
**Constructors**
- implicitly `private`; writing `public`/`protected` ✗ "modifier public not allowed here"
- run **once per constant**, when the enum class is first used — never by you: `new Week()` ✗ "enum classes may not be instantiated"
- *why?* public constructors would allow extra objects — against the whole idea of a fixed set
:::

## 🧬 Enums and inheritance

```sketch
            java.lang.Enum          ← every enum extends this, silently
                  ↑
                 Week   ─ ─ ─ implements ─ ─ ─→  A  (interfaces ✓, many)
                  ↑
                  ✗  class X extends Week → "cannot inherit from final"
```

- an enum **can't extend** any class — it already extends `java.lang.Enum` (single inheritance!)
- an enum **can't be extended** — it's implicitly `final`
- an enum **can implement** any number of interfaces ✓
- `toString()` returns the constant's name; compare with `==` or `equals()` — same result

:::reality
Two classic notes, updated:
1. "Enums can contain only concrete methods" — an enum **may** declare an `abstract` method if **every** constant supplies its own body: `PLUS { int apply(int a, int b) { return a + b; } }`.
2. "Enums can't be declared inside a method" — true before Java 16; since Java 16 **local enums** are allowed.
:::

:::trap
The constructor output appears at the **first use** of the enum (`Week.Monday`), not at `Week week;` — and it runs for **all** constants at once, in declaration order.
:::

## ⭐ CHAPTER 07 — REMEMBER

:::remember
- Collection → List (order, dups) · Set (unique) · Queue (FIFO); Map is separate
- program to the interface: `List<T> x = new ArrayList<>()`
- `HashSet`/`HashMap` depend on `equals` + `hashCode` (Ch 04)
- `Vector` = synchronized legacy ArrayList — safe per call, slower
- enum = fixed set of `public static final` objects; private constructors; `values()`, `valueOf()`, `ordinal()`
- enums extend `java.lang.Enum` → can't extend, can't be extended, can implement
:::

:::practice 🧪 PRACTICE — CHAPTER 07
### 🧪 QUICK CHECK
1. `List<Integer> l = new ArrayList<>(List.of(10, 20, 30)); l.remove(1);` — what's left?
2. Does `Map` extend `Collection`? How do you loop through a map's pairs?
3. An enum has 4 constants and you use it 100 times. How many times does its constructor run?

### 💻 CODE PRACTICE
1. Word counter: split a sentence, count each word in a `HashMap<String, Integer>`, print words that appear more than once.
2. `enum TrafficLight { RED(30), YELLOW(5), GREEN(25) }` with a `duration` field and `next()` (RED → GREEN → YELLOW → RED). Simulate 6 changes.

### 🎯 INTERVIEW THINKING
"Vector is synchronized, so `if (!v.contains(x)) v.add(x);` is thread-safe." True or false?

:::ans ☑ Answers
1. `[10, 30]` — `remove(int)` removes by **index**. 2. ✗ — use `for (Map.Entry<K, V> e : map.entrySet())`. 3. **4** times — once per constant, at first use.
**Interview:** false. Each call is atomic, but the *pair* isn't — another thread can add `x` between `contains` and `add`. Wrap both in one `synchronized (v) { … }` block (or use a `Set`).
:::
:::

:::teach
1. Array pain: fixed size, manual searching
2. Containers: shelf · stamp album · ticket line · dictionary
3. Draw the map — circle "Map is NOT a Collection"
4. Swap `ArrayList` → `LinkedList` → `Vector` in one line
5. Enum: coffee sizes; show the compile error for a typo
6. Ask: *when* do enum constructors run?
:::

:::connect 🔗 THE END OF THE PLAYLIST →
From one `class Student` to collections of objects and type-safe constants — that's the full OOP journey. Next pages: the **interview bank**, **3 mini projects**, the **master map** and the **one-page cheat sheet**.
:::
