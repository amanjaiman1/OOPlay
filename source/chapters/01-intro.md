@sheet | Ch 01 · Introduction to OOP

@chapter 01 | INTRODUCTION TO OOP | classes · objects · references · new · constructors · this · wrapper classes · final · garbage collection | 🎬 OOP 1

# ✦ WHY OOP? ✦

## 🧠 IDEA

The real world is made of **things** — students, cars, bank accounts. Each thing ==has data== (name, balance) and ==does work== (greet, withdraw). Object-Oriented Programming lets code copy that shape: bundle *data + behaviour* into one unit called an **object**.

## ❓ WHY DO WE NEED IT? — feel the problem first

Store roll no, name and marks of 5 students:

```java "😩 without OOP" bad
int[]    rno   = new int[5];
String[] name  = new String[5];
float[]  marks = new float[5];
// student #3 = rno[2] + name[2] + marks[2]   ← scattered in 3 arrays!
```

- one student's data lives in **3 different places**
- add "phone no." → change every array and every loop
- nothing stops index mix-ups between arrays
- where does `greeting()` belong? to *whom*?

```java "😍 with OOP"
class Student {            // ONE new data type that groups everything
    int rno;
    String name;
    float marks;
}

Student[] students = new Student[5];   // 5 students, ONE array
```

:::idea
A class lets you **create your own data type**. `int` stores one number — `Student` stores a whole student.
:::

## 🌍 IN REAL LIFE

Procedural code = **a recipe**: step 1, step 2, step 3. OOP = **a restaurant**: chef, waiter, cashier — each one knows its own data and its own job, and they work by talking to each other.

| | PROCEDURAL | OBJECT-ORIENTED |
|---|---|---|
| Thinks in | steps / functions | objects (data + behaviour) |
| Data | separate, often global | inside objects, can be hidden |
| Reuse | copy functions around | inheritance, composition |
| Safety | anyone can change any data | access control (`private` …) |
| Large projects | gets tangled fast | maps the real world, scales |
| Examples | C | Java, C#, C++ (C++ & Python are multi-paradigm) |

:::reality
Java is not "100 % pure" OOP — primitives (`int`, `char`, …) are not objects and `static` members exist without any object. It's a deliberate speed/convenience trade-off.
:::

@sheet | Ch 01 · Class & Object

# ✦ CLASS & OBJECT ✦

## 🧠 IDEA

[[b:Class]] = **blueprint / template**. [[b:Object]] = the **actual thing** built from it — an [[o:instance]] of the class.

```sketch
          CLASS = blueprint                     OBJECTS = real things
   ┌───────────────────────────┐          ┌─────────────┐  ┌─────────────┐
   │  class Student            │          │ rno   = 15  │  │ rno   = 18  │
   │    ─ rno                  │   new    │ name  =Kunal│  │ name  =Rahul│
   │    ─ name                 │ ───────→ │ marks = 85.4│  │ marks = 90.3│
   │    ─ marks                │          └─────────────┘  └─────────────┘
   │    ─ greeting()           │               kunal            rahul
   └───────────────────────────┘
       logical (just a plan)              physical (occupy memory in heap)
```

:::aside
finding classes in a problem:<br>**nouns** → classes<br>**verbs** → methods
:::

## 🌍 IN REAL LIFE

An architect's **house plan** → you can't sleep in a plan, but you can build 100 houses from it. Every house follows the same plan, yet each can have its own paint colour (its own *state*).

:::define
- [[b:Class]] — a named group of **properties** (fields) and **functions** (methods). It creates a new data type.
- [[b:Object]] — an instance of a class. Exists at runtime, occupies memory.
- [[b:Instance variable (field)]] — declared inside the class, outside methods. *Every object gets its own copy.*
- [[b:Method]] — a function inside a class; the object's behaviour.
:::

## ✍️ SYNTAX

```java
class ClassName {
    // fields   → state
    // methods  → behaviour
}

ClassName ref = new ClassName();   // create an object
ref.field;                         // dot operator → reach into that object
ref.method();
```

## 💻 EXAMPLE 1

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Student kunal = new Student();
        kunal.rno = 15;
        kunal.name = "Kunal";
        kunal.greeting();

        Student rahul = new Student();       // never touched
        System.out.println(rahul.name + " " + rahul.rno
                           + " " + rahul.marks);
    }
}

class Student {
    int rno;
    String name;
    float marks = 90;      // explicit initial value

    void greeting() {
        System.out.println("Hello! My name is " + name);
    }
}
```

```output
Hello! My name is Kunal
null 0 90.0
```

## 🔎 WHAT JUST HAPPENED?

1. `new Student()` → a fresh object in the heap; every field gets a **default value** (unless initialised, like `marks = 90`).
2. `kunal.rno = 15` → the dot operator reaches *kunal's* copy of `rno`.
3. `rahul` is a different object → `null 0 90.0`.

| field type | default value |
|---|---|
| `byte short int long` | `0` |
| `float double` | `0.0` |
| `char` | `'\u0000'` |
| `boolean` | `false` |
| any reference (`String`, arrays, objects) | `null` |

## 🧠 VISUALIZE IT — 3 properties of every object

```sketch
                          an OBJECT
           ┌──────────────────┼──────────────────┐
           ↓                  ↓                  ↓
         STATE             IDENTITY           BEHAVIOUR
     values of its       which object is     what it can do
     fields right now    it? (its own place   = its methods
     name = "Kunal"       in memory)          greeting()
```

:::mistake
`Student kunal;` creates **no object** — only an empty reference variable. Use a local one before assigning → ✗ compile error. A field left like that is `null` → `NullPointerException` when you use it.
:::

@sheet vs | Comparison · Class vs Object

# ✦ CLASS [[vs]] OBJECT ✦

| | CLASS | OBJECT |
|---|---|---|
| What | blueprint / template | instance / real thing |
| Nature | logical construct | physical — occupies heap memory |
| Created with | `class` keyword, written once | `new`, as many times as you like |
| Memory | class info loaded once by JVM | each object → its own copy of fields |
| Example | `class Car { }` | `new Car()` |
| Analogy | cookie cutter | cookies |

```sketch "one cutter, many cookies"
          ┌───────────┐
          │  CLASS    │   ← one definition
          │  (cutter) │
          └─────┬─────┘
       ┌────────┼────────┐
       ↓        ↓        ↓
    ( obj1 ) ( obj2 ) ( obj3 )   ← same shape, different state
```

:::remember
- A class is written once; objects are created at **runtime** with `new`.
- Two objects of the same class are independent — changing one doesn't change the other.
- Methods are shared code; **fields** are per-object (until we meet `static`).
:::

@sheet | Ch 01 · References, new & memory

# ✦ REFERENCES, `new` & MEMORY ✦

## 🧠 IDEA

`new` **creates the object in the heap** at runtime and **returns a reference** to it — think of it as an arrow / address-like handle. The variable stores only that arrow, [[r:never the object itself]].

```java
Student s;            // ① declare a reference — no object yet
s = new Student();    // ② create object in heap, store its reference in s
```

```sketch
   ① Student s;                         ② s = new Student();

     STACK             HEAP               STACK             HEAP
   ┌─────────┐                          ┌─────────┐      ┌───────────────┐
   │ s : ?   │      (nothing)           │ s : ●───┼────→ │ Student obj   │
   └─────────┘                          └─────────┘      │ rno   = 0     │
                                                         │ name  = null  │
                                                         │ marks = 90.0  │
                                                         └───────────────┘
```

## 🧠 Who looks at which side?

```sketch
        Student  s  =  new Student();
        └──┬──┘        └─────┬─────┘
           ↓                 ↓
     LEFT side:          RIGHT side:
     the COMPILER        the JVM at RUNTIME
     checks the type     creates the object
     (what you may call) (dynamic memory allocation)
```

## 💻 Two references, ONE object

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Student one = new Student();
        Student two = one;           // copies the ARROW, not the object
        one.name = "Something something";
        System.out.println(two.name);
    }
}

class Student { String name; }
```

```output
Something something
```

```sketch
     one ──────┐
               ↓
       ┌─────────────────────────────────┐
       │ Student { name = "Something…" } │   ← ONE object in heap
       └─────────────────────────────────┘
               ↑
     two ──────┘
```

## ❓ Why no `new` for `int`?

Primitives are **not objects** — the variable holds the value itself. No heap trip → fast.

```sketch
      int a = 10;                     Student s = new Student();
      STACK                           STACK             HEAP
    ┌──────────┐                    ┌─────────┐      ┌──────────┐
    │  a = 10  │ ← the value        │ s : ●───┼────→ │  object  │
    └──────────┘                    └─────────┘      └──────────┘
```

:::reality
"Locals on the stack, objects on the heap" is the right mental model. Fields — even `int` fields — live *inside* their object on the heap, and the JIT may optimise allocations away. A Java reference is **not** a pointer you can do maths on — no pointer arithmetic is part of what makes Java safe.
:::

:::trap
`Student b = a;` does **not** copy the object — it copies the **reference**. Both names now control the same object. (Real copying = cloning, Ch 06.)
:::

@sheet vs | Comparison · Reference vs Object

# ✦ REFERENCE [[vs]] OBJECT ✦

## 🌍 IN REAL LIFE — remote & TV

The **remote** is the reference; the **TV** is the object. Two remotes can control one TV. A remote can be paired to nothing (`null`). Lose every remote → nobody can reach that TV → it's garbage.

| | REFERENCE | OBJECT |
|---|---|---|
| Is | an arrow / handle | the actual block of data |
| Lives | stack (local var) or inside another object (field) | heap |
| Made by | a declaration: `Student s;` | `new Student()` |
| Can be `null`? | ✓ yes | ✗ an object is never "null" |
| Re-pointable? | ✓ (unless `final`) | — |
| `==` on two refs | compares arrows: same object? | — |
| Its type decides | what you're **allowed to call** (compiler) | which overridden method **runs** (JVM, Ch 03) |

```sketch "the 4 words students mix up"
   VARIABLE   = the named box             →   s
   REFERENCE  = what the box holds        →   ●  (an arrow)
   OBJECT     = what the arrow points to  →   Student { … }
   MEMORY     = where they live           →   s on STACK · object on HEAP
```

:::mistake
Saying "`s` **is** a Student object". Better: "`s` **[[u:refers to]]** a Student object." Getting this sentence right fixes half of all OOP confusion.
:::

@sheet | Ch 01 · Constructors

# ✦ CONSTRUCTORS ✦

## ❓ WHY?

Filling fields one by one (`kunal.rno = 15; kunal.name = …`) is boring and easy to forget. We want to **create + initialise in one line**:

```java
Student kunal = new Student(15, "Kunal Kushwaha", 85.4f);
```

## 🌍 IN REAL LIFE

When a house is built, electricity, paint and keys are set up **exactly once**, at construction time — before anyone moves in.

:::define
A **constructor** is a special block that runs automatically when an object is created with `new`, *before* `new` hands back the reference. It has the **same name as the class** and [[r:no return type]] — not even `void`.
:::

:::rule
- No constructor written → compiler adds a **default no-arg constructor**.
- You write **any** constructor → the default one is **not** added.
- `void Student() { }` is **not** a constructor — it's an ordinary method that happens to share the class name!
:::

## 💻 EXAMPLE — all 3 kinds (the class example)

```java "Main.java" run hl=14,17,22
public class Main {
    public static void main(String[] args) {
        Student kunal  = new Student(15, "Kunal Kushwaha", 85.4f);
        Student random = new Student(kunal);   // copy-style
        Student def    = new Student();        // no-arg
        System.out.println(kunal.name + " | " + random.name);
        System.out.println(def.name + " " + def.marks);
    }
}

class Student {
    int rno; String name; float marks = 90;

    Student() {                                    // ① no-arg
        this(13, "default person", 100.0f);        //    → delegates to ③
    }
    Student(Student other) {                       // ② takes another object
        this.rno = other.rno;
        this.name = other.name;
        this.marks = other.marks;
    }
    Student(int rno, String name, float marks) {   // ③ parameterized
        this.rno = rno; this.name = name; this.marks = marks;
    }
}
```

```output
Kunal Kushwaha | Kunal Kushwaha
default person 100.0
```

Three constructors, same name, different parameters → [[y:constructor overloading]]. Java picks the one whose parameters match the arguments.

## ⚠️ The disappearing default constructor

```java "Box.java" nocompile
class Box {
    int l;
    Box(int l) { this.l = l; }
}

class Test {
    void make() {
        Box b = new Box();     // ✗ no Box() exists any more
    }
}
```

```err "💥 compile error"
error: constructor Box in class Box cannot be applied to given types;
  required: int
  found:    no arguments
```

| | CONSTRUCTOR | METHOD |
|---|---|---|
| Name | same as class | anything |
| Return type | none (not even `void`) | must have one (`void` counts) |
| Called | automatically by `new`, once per object | explicitly, any number of times |
| Inherited? | ✗ never | ✓ (non-private) |
| Can be `static / final / abstract`? | ✗ | ✓ |

:::trap
"Constructors return nothing, so `new` returns nothing?" ✗ — the constructor has no return type, but the `new` **expression** evaluates to the reference of the new object.
:::

@sheet | Ch 01 · this

# ✦ THE `this` KEYWORD ✦

## 🧠 IDEA

`this` = a reference to the **current object** — the object on which the method or constructor is running right now.

```java "the classic use"
class Student {
    String name;

    Student(String name) {
        this.name = name;
//!          ↑      ↑
//!          │      └── the PARAMETER (local variable)
//!          └── the FIELD of the current object
    }
}
```

:::mistake
`name = name;` assigns the parameter **to itself** (the local variable *shadows* the field). The field stays `null`. Use `this.name = name;`.
:::

## 🧠 VISUALIZE IT — `this` changes with the caller

```sketch
   kunal.greeting();   →   inside greeting():  this == kunal
   rahul.greeting();   →   inside greeting():  this == rahul

     kunal ───→ ┌──────────────┐ ←─── this
                │ name = Kunal │      (while kunal.greeting() runs)
                └──────────────┘
```

## ✍️ 4 uses of `this`

1. `this.field` — separate a field from a same-named parameter
2. `this(...)` — call another constructor of the **same** class (constructor chaining)
3. `obj.compare(this)` — pass the current object as an argument
4. `return this;` — return the current object → calls can be chained: `acc.deposit(10).deposit(20)`

## 💻 CONSTRUCTOR CHAINING

```sketch
   new Student()
        │
        ↓   this(13, "default person", 100.0f)
   Student(int, String, float)      ← the real work is written ONCE here
        │
        ↓
   object ready: rno = 13, name = "default person", marks = 100.0
```

:::rule
`this(...)` (and `super(...)`, Ch 03) must be the **first statement** of a constructor — and a constructor can't call both.
:::

:::reality
Since **Java 25** ("flexible constructor bodies") you may write statements *before* `this(...)`/`super(...)` — e.g. argument checks — as long as they don't use the object being built. Exams and most codebases still follow the classic "first statement" rule.
:::

:::trap
`this` cannot appear in a `static` method — a static method runs without any current object (Ch 02).
:::

@sheet | Ch 01 · Wrapper classes

# ✦ WRAPPER CLASSES ✦

## 🧠 IDEA

Every primitive has an **object version** in `java.lang`:

| primitive | `byte` | `short` | `int` | `long` | `float` | `double` | `char` | `boolean` |
|---|---|---|---|---|---|---|---|---|
| wrapper | `Byte` | `Short` | `Integer` | `Long` | `Float` | `Double` | `Character` | `Boolean` |

## ❓ WHY?

- collections & generics hold **objects only** → `ArrayList<int>` ✗ · `ArrayList<Integer>` ✓
- a wrapper can be `null` ("no value yet")
- handy helpers: `Integer.parseInt("42")`, `Integer.MAX_VALUE`, `Character.isDigit(c)`

```java
Integer num = 45;   // autoboxing:  int → Integer   (Integer.valueOf(45))
int n = num;        // unboxing:    Integer → int   (num.intValue())
```

## 💻 The swap puzzle

```java "WrapperExample.java" run
public class WrapperExample {
    public static void main(String[] args) {
        Integer a = 10, b = 20;
        swap(a, b);
        System.out.println(a + " " + b);
    }

    static void swap(Integer a, Integer b) {
        Integer temp = a;
        a = b;
        b = temp;
    }
}
```

```output
10 20
```

## 🔎 WHAT JUST HAPPENED?

Java is **always pass-by-value**. For objects, the *value* that gets copied is the reference. `swap()` shuffles **its own copies** of the arrows; `main`'s `a` and `b` never move. (And `Integer` is immutable, so the 10-object can't turn into 20 either.)

```sketch
      main()                               swap()
      a ───→ «10» ←─────────────────────── a'  ┐  swap() re-points only
      b ───→ «20» ←─────────────────────── b'  ┘  its own copies a', b'
```

:::trap Integer cache
`Integer x = 127, y = 127;` → `x == y` is **true** (values −128…127 are cached).
`Integer p = 128, q = 128;` → `p == q` is **false** (two different objects).
Compare wrappers with `.equals()`, never `==`.
:::

:::mistake
`Integer v = null; int k = v;` → unboxing `null` throws **NullPointerException**.
:::

@sheet | Ch 01 · final

# ✦ THE `final` KEYWORD ✦

## 🧠 IDEA

`final` = **assign once, never re-assign**.

- final variable → a constant; must be initialised exactly once (at declaration, or — for a field — in every constructor)
- convention: `static final int MAX_SIZE = 10;` → UPPER_SNAKE_CASE
- final method → can't be overridden · final class → can't be extended (both in Ch 03)

```java "final with primitives vs references"
final int bonus = 2;
bonus = 3;                          // ✗ compile error

final A kunal = new A("Kunal Kushwaha");
kunal.name = "other name";          // ✓ allowed — the OBJECT changes
kunal = new A("new object");        // ✗ compile error — the ARROW is fixed
```

```sketch
     final A kunal
     ┌───────┐  arrow is welded  ┌─────────────────────┐
     │   ●───┼─────────────────→ │ name = "other name" │ ← contents
     └───────┘   (can't move)    └─────────────────────┘   CAN change
         ✗ ─ ─ ─→  new A("new object")
```

:::trap
A `final` reference ≠ an immutable object. `final` freezes [[u:the **arrow**, not the **object**]]. Immutability (like `String`) must be designed into the class: private final fields, no setters.
:::

:::doubt "Must a final field be given a value right away?"
No — a **blank final** may be assigned later, but exactly once on every path of every constructor:

`final int VALUE;  Parent(int age) { VALUE = 32456789; }` ✓
:::

@sheet | Ch 01 · Garbage collection

# ✦ GARBAGE COLLECTION ✦

## 🧠 IDEA

An object that **no reference can reach** is useless. The JVM's **Garbage Collector (GC)** finds such objects and frees their memory automatically — no `free()` / `delete` like C/C++.

:::aside
you can't *delete* objects in Java — you just let go of them
:::

## 🌍 IN REAL LIFE

Food-court trays: once you walk away from your table, staff clear the tray. You don't clean it yourself — and you don't decide *when* they come.

```java
A obj = new A("first");
obj = new A("second");    // "first" has no reference left → eligible for GC
```

```sketch
   BEFORE                        AFTER   obj = new A("second")

   obj ──→ ┌─────────┐           obj ─┐    ┌─────────┐
           │ "first" │                │    │ "first" │ ← unreachable
           └─────────┘                │    └─────────┘   = garbage ✗
                                      └──→ ┌──────────┐
                                           │ "second" │
                                           └──────────┘
```

## 4 ways an object becomes eligible

1. its reference is re-assigned (above)
2. its reference is set to `null`
3. the method holding the only reference finishes (local goes out of scope)
4. "island of isolation" — objects pointing only at each other, nothing outside points at them

:::reality
- `System.gc()` is only a **request**; the JVM may ignore it.
- Old code overrides `finalize()` (e.g. to print "Object is destroyed"). It is **deprecated** (since Java 9, *for removal* since Java 18): it may run late or never. For cleanup use `close()` / try-with-resources.
:::

:::trap
"GC destroys an object the moment it becomes unreachable" ✗ — it only becomes [[o:eligible]]. When (or whether) GC runs is the JVM's decision.
:::

## ⭐ CHAPTER 01 — REMEMBER

:::remember
- class = blueprint (logical); object = instance (physical, heap)
- `new` allocates at runtime and returns a **reference**; `b = a` copies only the arrow
- constructor: class name, no return type; the default one exists only if you write none
- `this` = current object; `this(...)` goes first in a constructor
- `final` reference ≠ immutable object · unreachable ≠ destroyed (just eligible)
:::

:::practice 🧪 PRACTICE — CHAPTER 01
### 🧪 QUICK CHECK
1. `Student a = new Student(); Student b = a; b.name = "X";` → what is `a.name`?
2. A class has only `Box(int side)`. Does `new Box()` compile? Why?
3. Inside a constructor you wrote `name = name;` — what is the field's value afterwards?

### 💻 CODE PRACTICE
1. `BankAccount` with `accountNo`, `holder`, `balance`: three constructors chained with `this(...)`, and `deposit(double)` that `return this;` so `acc.deposit(100).deposit(50)` works.
2. Create 3 `Student` objects, then make two of them unreachable in two *different* ways. Draw the stack/heap picture after every line.

### 🎯 INTERVIEW THINKING
`final int[] arr = {1, 2, 3}; arr[0] = 100;` — does it compile? What does `arr[0]` hold? And `arr = new int[3];`?

:::ans ☑ Answers
1. `"X"` — one object, two arrows. 2. ✗ — writing any constructor removes the default one. 3. The default (`null`) — the parameter was assigned to itself.
**Interview:** ✓ compiles and `arr[0]` is `100` — the array object can change. `arr = new int[3];` ✗ — the final arrow can't move.
:::
:::

:::teach
1. Start with 5 students in 3 arrays — let them *feel* the mess
2. Analogy: house plan → houses
3. Write `class Student`, create two objects
4. Draw stack & heap for **every** `new`
5. Ask: `b = a; b.name = "X";` → `a.name`?
6. Then constructors + `this` to kill the boring assignments
:::

:::connect 🔗 NEXT →
Every `Student` has its **own** `name`. But some data belongs to **all** students together — like the total population. Who owns that? → `static` (Chapter 02).
:::
