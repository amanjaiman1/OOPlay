@sheet | Ch 02 · Packages

@chapter 02 | PACKAGES • STATIC • INNER CLASSES • SINGLETON | package · import · static members & blocks · why main() is static · System.out.println · inner classes · singleton | 🎬 OOP 2

# ✦ PACKAGES ✦

## 🧠 IDEA

A **package** is a folder + a namespace for classes. It groups related classes and lets two classes share a name without clashing.

## 🌍 IN REAL LIFE

Two students called *Rahul* in one school → "Rahul of 10-A" and "Rahul of 12-C". The section is the package. Same idea as two files called `notes.txt` in different folders.

## ❓ WHY DO WE NEED IT?

- our example has **two** classes named `Greeting` — one in package `a`, one in `b` — no clash
- big projects stay organised (`model`, `service`, `util` …)
- a package is also a **visibility boundary** (default access → Ch 04)

:::define
A [[b:package]] is a namespace that groups related classes and interfaces. It is both a **naming** and a **visibility-control** mechanism. The folder structure must mirror the package name.
:::

## ✍️ SYNTAX

```java "src/com/kunal/packages/a/Greeting.java"
package com.kunal.packages.a;                          // ① FIRST statement

import static com.kunal.packages.b.Message.message;    // ② imports

public class Greeting {                                // ③ the class
    public static void main(String[] args) {
        System.out.println("Hello world");
        message();                     // static import → no class name
    }
}
```

```sketch "folders = packages" sm
   src/
    └── com/
         └── kunal/
              └── packages/
                   ├── a/
                   │    └── Greeting.java     ← package com.kunal.packages.a;
                   └── b/
                        ├── Greeting.java     ← package com.kunal.packages.b;
                        └── Message.java
```

## 📦 import — 4 flavours

- `import java.util.ArrayList;` → one class
- `import java.util.*;` → every class of `java.util` (but **not** its sub-packages)
- `import static java.lang.Math.*;` → static members: `sqrt(16)` instead of `Math.sqrt(16)`
- no import at all → write the **fully qualified name**: `com.kunal.packages.b.Greeting g = new com.kunal.packages.b.Greeting();`

`java.lang` (String, System, Math, Integer, Object …) is imported **automatically**.

:::rule
- at most **one** `package` statement, and it comes first
- at most **one `public` top-level class** per file — and the file must be named after it
- order in a file: `package` → `import`s → classes
:::

:::trap
`import java.util.*;` does **not** give you `java.util.function.Consumer`. A sub-package is a completely separate package — the dots only look like a hierarchy.
:::

:::reality
Same simple name from two packages (`java.util.Date` and `java.sql.Date`)? Import one, write the other's fully qualified name. The JVM finds packages via the current directory, the `CLASSPATH` variable, or `-classpath` / `-cp`.
:::

@sheet | Ch 02 · static

# ✦ STATIC ✦

## ❓ WHY? — the problem

`Human` has `age`, `name`, `salary` … and **population**. Age belongs to *one* person. Population belongs to *all humans together*. As an instance field, every object would hold its own copy: kunal says 1, rahul says 1, arpit says 1 ✗.

## 🧠 IDEA

A `static` member ==belongs to the class, not to any object==. [[u:One copy, shared by everyone]], usable even before any object exists.

:::aside
static ≈ **ours**<br>instance ≈ **mine**
:::

## 🌍 IN REAL LIFE

A classroom: every student has their **own notebook** (instance), but there is **one whiteboard** (static). Write on the whiteboard → everyone sees the change.

## 💻 EXAMPLE

```java "Main.java" run hl=14,19
public class Main {
    public static void main(String[] args) {
        Human kunal = new Human(22, "Kunal");
        Human rahul = new Human(34, "Rahul");
        Human arpit = new Human(34, "Arpit");

        System.out.println(Human.population);   // ClassName.member ✓
    }
}

class Human {
    int age;
    String name;
    static long population;            // ONE copy for the whole class

    Human(int age, String name) {
        this.age = age;
        this.name = name;
        Human.population += 1;      // every object bumps ONE counter
    }
}
```

```output
3
```

## 🧠 VISUALIZE IT

```sketch
                     CLASS LEVEL  (one per class)
              ┌───────────────────────────────────┐
              │  Human.population = 3   ← shared  │
              └───────────────────────────────────┘
                 ↑ same counter, seen by all ↑
        ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
 HEAP   │ age  = 22     │ │ age  = 34     │ │ age  = 34     │
        │ name = Kunal  │ │ name = Rahul  │ │ name = Arpit  │
        └───────────────┘ └───────────────┘ └───────────────┘
              kunal             rahul             arpit
```

## ✍️ Static methods

A method that doesn't need any object's data can be `static` → call it with the class name: `Math.sqrt(25)`, `Arrays.sort(arr)`, `Integer.parseInt("7")`, `Human.message()`.

:::mistake
`kunal.population` compiles, but reads like "kunal's own population". Always write `Human.population` — it tells the reader the truth: it's shared.
:::

@sheet | Ch 02 · static rules

# ✦ STATIC — WHO CAN TALK TO WHOM? ✦

| FROM ↓ · TO → | static member | instance member |
|---|---|---|
| static method | ✓ directly | ✗ directly · ✓ through an object reference |
| instance method | ✓ directly | ✓ directly |

## ❓ WHY can't static touch instance members directly?

An instance member belongs to **some object**. A static method runs with [[r:no object at all]] — there is no `this`. So "`greeting()`" inside a static method means *greeting of … whom?*

```java "Main.java"
public class Main {
    static void fun() {
        // greeting();         ✗ no object here — whose greeting?
        Main obj = new Main();
        obj.greeting();        // ✓ now we NAME the object
    }

    void fun2() {
        greeting();            // ✓ means this.greeting()
    }

    void greeting() {
        System.out.println("Hello world");
    }
}
```

```java "this inside static" nocompile
class Human {
    int age;

    static void message() {
        System.out.println(this.age);
    }
}
```

```err "💥 compile error"
error: non-static variable this cannot be referenced from a static context
```

:::rule
- static methods: no `this`, no `super`
- static members are created when the class **loads**; instance members when an object is **created**
- local variables can't be `static` → `void f() { static int x; }` ✗
:::

:::reality
"A static method can only call static methods" is the short version. Precisely: it can't call instance methods **directly** (no implicit `this`) — through a reference like `obj.greeting()` it's perfectly fine.
:::

:::trap
Static methods are **not overridden** — a child's static method with the same signature only *hides* the parent's (Ch 03).
:::

@sheet vs | Comparison · static vs non-static

# ✦ STATIC [[vs]] NON-STATIC ✦

| | STATIC | NON-STATIC (instance) |
|---|---|---|
| Belongs to | the class | each object |
| Copies | **one**, shared | one **per object** |
| Access with | `ClassName.member` | `objectRef.member` |
| Comes alive | when the class is loaded | when an object is created with `new` |
| `this` / `super` | ✗ not available | ✓ available |
| Can use directly | only static members | static **and** instance members |
| Overriding | ✗ (hiding only) | ✓ |
| Examples | `Human.population`, `Math.PI`, `main()` | `kunal.name`, `kunal.greeting()` |

```sketch "whiteboard vs notebooks"
          ┌──────────────────────────┐
          │  WHITEBOARD  (static)    │   one, shared by the class
          └──────────────────────────┘
       ┌──────┐   ┌──────┐   ┌──────┐
       │ note │   │ note │   │ note │    one per object (instance)
       │ book │   │ book │   │ book │
       └──────┘   └──────┘   └──────┘
        kunal      rahul      arpit
```

:::remember
- `static` = class-level, shared · instance = object-level, private copy
- a static context has **no `this`** → name an object to reach instance members
- prefer `ClassName.staticMember`, never `object.staticMember`
:::

@sheet | Ch 02 · static blocks & init order

# ✦ STATIC BLOCK & INITIALIZATION ORDER ✦

## 🧠 IDEA

A `static { … }` block runs **exactly once** — when the class is first loaded. Use it when a static variable needs computation to initialise.

```java "StaticBlock.java" run
public class StaticBlock {
    static int a = 4;
    static int b;

    static {                         // runs ONCE, at class loading
        System.out.println("I am in static block");
        b = a * 5;
    }

    public static void main(String[] args) {
        StaticBlock obj = new StaticBlock();
        System.out.println(StaticBlock.a + " " + StaticBlock.b);
        StaticBlock.b += 3;
        System.out.println(StaticBlock.a + " " + StaticBlock.b);
        StaticBlock obj2 = new StaticBlock();  // no static block again
        System.out.println(StaticBlock.a + " " + StaticBlock.b);
    }
}
```

```output
I am in static block
4 20
4 23
4 23
```

## 🧠 VISUALIZE IT — the full order

```sketch
   class used for the first time  →  JVM loads it
        │
        ↓
   ① static variables + static { } blocks      top → bottom, ONCE
        │
        ↓
   ② main() starts
        │
        ↓   new Order()
   ③ parent constructor first (super)          every object
        │
        ↓
   ④ instance variables + instance { } blocks  top → bottom
        │
        ↓
   ⑤ rest of the constructor body
```

```java "Order.java" run
public class Order {
    static { System.out.println("1. static block"); }
    { System.out.println("3. instance block"); }
    Order() { System.out.println("4. constructor"); }

    public static void main(String[] args) {
        System.out.println("2. main starts");
        new Order();
        new Order();
    }
}
```

```output
1. static block
2. main starts
3. instance block
4. constructor
3. instance block
4. constructor
```

:::trap
Creating 5 objects runs the static block **once**, but the instance block **5 times**. And the static block of the class holding `main` runs **before** `main` itself.
:::

@sheet | Ch 02 · Why main() is static

# ✦ WHY IS `main()` STATIC? ✦

```java
public static void main(String[] args)
```

```sketch
   public      static      void       main       (String[] args)
     │           │           │          │               │
     ↓           ↓           ↓          ↓               ↓
  the JVM     the JVM      returns    the exact     command-line
  (outside    calls it     nothing    name the      arguments
  the class)  WITHOUT                 JVM looks     java Main hi 5
  can reach   creating an             for           → {"hi", "5"}
  it          object of Main
```

## ❓ WHY static?

When the program starts **no objects exist yet**. The JVM loads `Main` and needs a door to walk in through. If `main` were an instance method, the JVM would first have to build a `Main` object — with which constructor? which arguments? `static` removes that chicken-and-egg problem: [[u:**call it on the class itself**]].

```java "public void main(...)" bad
public class Main {
    public void main(String[] args) {          // no static
        System.out.println("hi");
    }
}
```

```err "💥 classic Java (8 … 24)"
Error: Main method is not static in class Main, please define the main method as:
   public static void main(String[] args)
```

:::reality
**Java 25** (JEP 512) relaxed the launcher: it also accepts an instance `main` (even without `String[] args`) and creates the object for you with the no-arg constructor. The interview answer is still: *"main is static so the JVM can call it without creating an object."*
:::

| variation | works? |
|---|---|
| `static public void main(String[] args)` | ✓ modifier order doesn't matter |
| `public static void main(String... args)` | ✓ varargs is fine |
| `public static void main(String args[])` | ✓ C-style array |
| `private static void main(String[] args)` | ✗ "Main method not found" |
| overloading `main(int x)` too | ✓ compiles — but the JVM only calls the `String[]` one |

:::mistake
`args` holds **Strings** only: `java Main 5` gives `args[0] = "5"`. Need a number → `Integer.parseInt(args[0])`.
:::

@sheet | Ch 02 · System.out.println internals

# ✦ HOW `System.out.println()` WORKS ✦

@@good

```sketch
       System   .   out   .   println("hi")
         │           │            │
         ↓           ↓            ↓
     a final       a STATIC     an INSTANCE method
     class in      field of     of class PrintStream
     java.lang     System, of   (overloaded for int, char,
     (no import)   type         double, String, Object …)
                   PrintStream
```

So `System.out` is a **static field** (no `System` object needed), and `println` runs **on the `PrintStream` object** that `out` refers to. Everything from this chapter, in one line!

## 🖨️ Printing an object

`println(Object x)` → `String.valueOf(x)` → `x.toString()`. Not overridden? You get `ClassName@hexHash`, e.g. `Test@1b6d3586`. Override `toString()` to print something useful:

```java "Main.java" run
public class Main {
    static class Test {
        String name;
        Test(String name) { this.name = name; }

        @Override
        public String toString() {      // without this → Main$Test@<hash>
            return name;
        }
    }

    public static void main(String[] args) {
        Test a = new Test("Kunal");
        System.out.println(a);          // calls a.toString() for you
    }
}
```

```output
Kunal
```

:::trap
`System.out.println(null);` does **not** print "null" — it doesn't even compile: `println(char[])` and `println(String)` both accept `null` → "reference to println is ambiguous". (`String s = null; System.out.println(s);` prints `null` fine.)
:::

@sheet | Ch 02 · Inner classes

# ✦ INNER CLASSES ✦

## 🧠 IDEA

A class declared **inside** another class. Two kinds matter:

- **inner class** (non-static) → every inner object is [[u:**tied to one outer object**]]
- **static nested class** → just *filed inside* the outer class; needs **no** outer object

## 🌍 IN REAL LIFE

Inner class = a **room**: it can't exist without *its* house, and it sees everything in that house. Static nested class = a **spare blueprint kept in the house's folder** — filed under "House", but you can use it with no house built at all.

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Outer outer = new Outer();
        Outer.Inner inner = outer.new Inner();      // needs an Outer object
        inner.show();

        Outer.Nested nested = new Outer.Nested();  // no Outer needed
        nested.show();
    }
}

class Outer {
    private int x = 10;
    static int y = 20;

    class Inner {                    // non-static → tied to one Outer
        void show() {
            System.out.println("Inner sees x = " + x + ", y = " + y);
        }
    }

    static class Nested {            // static → belongs to the class Outer
        void show() {
            System.out.println("Nested sees y = " + y);
        }
        // using x here ✗ — which Outer's x? there is no Outer object
    }
}
```

```output
Inner sees x = 10, y = 20
Nested sees y = 20
```

## 🧠 VISUALIZE IT — execution sketch

```sketch
   Outer outer = new Outer();
   Outer.Inner inner = outer.new Inner();

      STACK                    HEAP
   ┌─────────┐          ┌───────────────┐
   │ outer ●─┼────────→ │ Outer object  │ ←──────┐
   └─────────┘          │ x = 10        │        │  hidden link
   ┌─────────┐          └───────────────┘        │  "Outer.this"
   │ inner ●─┼────────→ ┌───────────────┐        │
   └─────────┘          │ Inner object  │ ───────┘
                        └───────────────┘

   Outer.Nested n = new Outer.Nested();      ← no link, no Outer needed
```

## ❓ WHY do the two syntaxes differ?

- `outer.new Inner()` → an inner object is built **for a particular outer object** and silently stores a link to it (`Outer.this`). So you must say *which* outer: `outer.`
- `new Outer.Nested()` → `Nested` is really an independent class with a long name; `Outer.` is only its address.

```java "puzzle — make Test non-static" nocompile
public class InnerClasses {
    class Test {                        // static removed
        String name;
        Test(String name) { this.name = name; }
    }

    public static void main(String[] args) {
        Test a = new Test("Kunal");     // main has no InnerClasses object!
    }
}
```

```err "💥 compile error"
error: non-static variable this cannot be referenced from a static context
```

:::rule
- only **nested** classes can be `static` — `static class A { }` at top level ✗
- an inner class can read the outer class's **private** members (and vice-versa)
:::

:::reality
Since Java 16 an inner (non-static) class may also declare `static` members — older notes say only static nested classes can. Two more kinds you'll meet later: **local** classes (inside a method) and **anonymous** classes (Comparator in Ch 06).
:::

@sheet | Ch 02 · Singleton

# ✦ SINGLETON CLASS ✦

## ❓ WHY?

Some things must exist **only once**: app configuration, a logger, a connection pool. Many copies → wasted resources and conflicting state.

## 🌍 IN REAL LIFE

A country has **one** President at a time. Everyone asking "who is the President?" gets the **same** person.

## 🧠 IDEA — 3 ingredients

1. `private` constructor → nobody outside can write `new`
2. a `private static` field holding **the** instance
3. a `public static` method → the only door in

```java "Main.java" run hl=12,14,16-21
public class Main {
    public static void main(String[] args) {
        Singleton obj1 = Singleton.getInstance();
        Singleton obj2 = Singleton.getInstance();
        Singleton obj3 = Singleton.getInstance();
        System.out.println(obj1 == obj2 && obj2 == obj3);
        // new Singleton();   ✗ Singleton() has private access
    }
}

class Singleton {
    private static Singleton instance;      // the ONE object

    private Singleton() { }                 // ① no outside new

    public static Singleton getInstance() { // ② the only door
        if (instance == null) {             // ③ first call only (lazy)
            instance = new Singleton();
        }
        return instance;
    }
}
```

```output
true
```

```sketch
   obj1 ───┐
   obj2 ───┼────→  ┌───────────────────────┐
   obj3 ───┘       │  the ONE Singleton    │
                   └───────────────────────┘
```

:::doubt "Why must getInstance() be static?"
Because before the first call **no object exists** — and you can't call an instance method without an object. Static is the only way in.
:::

:::reality
This lazy version is not thread-safe — two threads may both see `null` and create two objects. Real code uses an eager `private static final` instance, a `synchronized`/double-checked `getInstance()`, or simply `enum Config { INSTANCE }` (also safe against reflection & serialization).
:::

:::trap
A class whose **only** constructor is `private` can't be extended by a normal outside class — the child's constructor has no accessible `super()` to call.
:::

## ⭐ CHAPTER 02 — REMEMBER

:::remember
- package = folder + namespace; `package` first; `java.lang` auto-imported; `pkg.*` skips sub-packages
- `static` = one shared copy owned by the class; access as `ClassName.member`
- static context = no `this` → name an object to use instance members
- static block: once per class load · instance block: once per object
- `main` is static so the JVM can call it without an object
- inner: `outer.new Inner()` · static nested: `new Outer.Nested()`
- singleton = private constructor + private static instance + public static getter
:::

:::practice 🧪 PRACTICE — CHAPTER 02
### 🧪 QUICK CHECK
1. `class C { static int s; int i; C() { s++; i++; } }` — after `new C(); new C(); C c = new C();` what do `C.s` and `c.i` print?
2. Can a static method use `this`? Explain in one line *why*.
3. You create 5 objects of a class with a static block and an instance block. How many times does each run?

### 💻 CODE PRACTICE
1. `Ticket` class: each new ticket gets a unique id 1, 2, 3 … from a static counter; add `static int totalTickets()`.
2. A `Config` singleton holding `appName`. Prove with `==` that two calls return one object; then rewrite it eagerly.

### 🎯 INTERVIEW THINKING
`Human h = null; System.out.println(h.population);` — `population` is static. NullPointerException or not?

:::ans ☑ Answers
1. `3 1` — `s` is shared; each object has its own `i`. 2. ✗ — a static method runs with no current object. 3. Static block once, instance block 5 times.
**Interview:** no NPE — it prints the value. Static access is resolved from the reference's **type** at compile time; the `null` object is never touched.
:::
:::

:::teach
1. Ask "where should population live?" — put it in each object, show 1, 1, 1
2. Whiteboard vs notebooks
3. `static` field + `ClassName.member`
4. Let a static method try `this` — read the error together
5. Run `StaticBlock`, ask for the output order
6. Finish with Singleton = private constructor + static
:::

:::connect 🔗 NEXT →
`Box`, `BoxWeight`, `BoxPrice` all need length, width, height. Copy-paste the same fields into three classes? No → **inheritance** (Chapter 03).
:::
