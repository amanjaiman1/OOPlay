@sheet | Ch 03 · The four pillars

@chapter 03 | THE FOUR PILLARS OF OOP | inheritance · super · types of inheritance · polymorphism · overloading · overriding · dynamic dispatch · final · encapsulation · abstraction | 🎬 OOP 3

# ✦ THE 4 PILLARS ✦

```sketch "the map of this chapter"
                              «OOP»
                                │
          ┌─────────────────────┼─────────────────────┐
          ↓                     ↓                     ↓
    «INHERITANCE»         «POLYMORPHISM»        «ENCAPSULATION»
     reuse a parent        one name,             data + methods +
     "IS-A"                many behaviours       controlled access
          │               ┌─────┴─────┐               │
       extends       overloading  overriding     private + get/set
       super()      (compile time) (runtime)
          └─────────────────────┬─────────────────────┘
                                ↓
                          «ABSTRACTION»
                       show WHAT, hide HOW
                     (abstract class, interface)
```

| pillar | one line | real life |
|---|---|---|
| Inheritance | child reuses & extends the parent's code | a child inherits the family's features |
| Polymorphism | same call → different behaviour | one person: student, athlete, son, employee |
| Encapsulation | data hidden, reached only through checked methods | an ATM: you press buttons, never touch the cash box |
| Abstraction | expose only what's essential | driving without knowing engine internals |

:::idea
All four answer one question: **how do we build big programs without drowning?** Reuse (inheritance), flexibility (polymorphism), safety (encapsulation), simplicity (abstraction).
:::

@sheet | Ch 03 · Inheritance

# ✦ INHERITANCE ✦

## ❓ WHY? — the problem

We have `Box` with `l, h, w`. Now we need `BoxWeight` (+ weight) and `BoxPrice` (+ cost). Copy-paste `l, h, w` and the constructors into each? Fix a bug → fix it 3 times ✗.

## 🧠 IDEA

A **child class** gets all the (non-private) members of a **parent class** and adds only what's new. Relationship: [[o:**IS-A**]] — a `BoxWeight` **is a** `Box`.

## 🌍 IN REAL LIFE

A child inherits common traits from the parents (surname, eye colour) and adds their own (their skills).

:::define
[[b:Inheritance]] — a mechanism where one class (**subclass / child / derived**) acquires the properties and behaviour of another (**superclass / parent / base**) using `extends`.
:::

## 💻 EXAMPLE — the Box family

```java "Main.java" run hl=23,27
public class Main {
    public static void main(String[] args) {
        BoxWeight box = new BoxWeight(2, 3, 4, 8);
        System.out.println(box.h + " " + box.w + " " + box.weight
                           + " " + box.getL());
    }
}

class Box {
    private double l;           // private → only Box's code can touch
    double h, w;

    Box(double l, double h, double w) {
        System.out.println("Box class constructor");
        this.l = l;
        this.h = h;
        this.w = w;
    }

    public double getL() { return l; }
}

class BoxWeight extends Box {       // BoxWeight IS-A Box
    double weight;                  // only the NEW stuff

    BoxWeight(double l, double h, double w, double weight) {
        super(l, h, w);             // let the parent set up its own part
        this.weight = weight;
    }
}
```

```output
Box class constructor
3.0 4.0 8.0 2.0
```

## 🧠 VISUALIZE IT — one object, two parts

```sketch
   box ──→ ┌──────────────────────────────┐
           │ Box part   l = 2.0 (private) │ ← inside the object,
           │            h = 3.0           │   but BoxWeight code
           │            w = 4.0           │   must use getL()
           ├──────────────────────────────┤
           │ BoxWeight  weight = 8.0      │
           └──────────────────────────────┘
                ONE object — not two!
```

## 🔑 Parent reference → child object

```java "the experiment"
Box box5 = new BoxWeight(2, 3, 4, 8);   // ✓ a BoxWeight IS-A Box
box5.w;                                 // ✓ w is declared in Box
box5.weight;                            // ✗ Box has no 'weight'

BoxWeight box6 = new Box(2, 3, 4);      // ✗ compile error
```

:::doubt "Why is `BoxWeight box6 = new Box(…)` an error?"
The reference type `BoxWeight` promises you can use `box6.weight`. But a plain `Box` object **has no weight part** — that promise would be a lie. So the compiler refuses. Parent ref → child object ✓; child ref → parent object ✗.
:::

:::rule
- a class can `extends` **only one** class
- **private** members are not accessible in the child (they still exist inside the object)
- [[r:constructors are never inherited]] — the child calls them with `super(...)`
:::

@sheet | Ch 03 · super & the constructor chain

# ✦ `super` & THE CONSTRUCTOR CHAIN ✦

## 🧠 IDEA

`super` = "my **parent's** part". Two forms:

1. `super(...)` → call the **parent's constructor** (must be the first statement)
2. `super.member` → use a parent's field/method that the child has hidden or overridden

## 💻 Constructors run parent-first

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        new BoxPrice(5, 8, 200);
    }
}

class Box {
    double l, h, w;
    Box(double side) {
        // super();  ← added for you → calls Object()
        l = h = w = side;
        System.out.println("1. Box");
    }
}

class BoxWeight extends Box {
    double weight;
    BoxWeight(double side, double weight) {
        super(side);
        this.weight = weight;
        System.out.println("2. BoxWeight");
    }
}

class BoxPrice extends BoxWeight {
    double cost;
    BoxPrice(double side, double weight, double cost) {
        super(side, weight);
        this.cost = cost;
        System.out.println("3. BoxPrice");
    }
}
```

```output
1. Box
2. BoxWeight
3. BoxPrice
```

```sketch
      calls climb UP                         bodies finish top → down
   ┌───────────────────────┐
   │ Object()              │  ← the top of EVERY chain          ① done
   └───────────▲───────────┘
               │ super()          (implicit)
   ┌───────────┴───────────┐
   │ Box(5)                │                    ② prints "1. Box"
   └───────────▲───────────┘
               │ super(side)
   ┌───────────┴───────────┐
   │ BoxWeight(5, 8)       │                    ③ prints "2. BoxWeight"
   └───────────▲───────────┘
               │ super(side, weight)
   ┌───────────┴───────────┐
   │ BoxPrice(5, 8, 200)   │  ← new starts here ④ prints "3. BoxPrice"
   └───────────────────────┘
```

**Why parent first?** The parent knows nothing about the child, but the child may depend on the parent's fields already being ready.

## ⚠️ No `super(...)` written?

Java silently inserts `super();` — the parent's **no-arg** constructor. If the parent doesn't have one:

```java "Child.java" nocompile
class Parent {
    Parent(int x) { }          // only a parameterized constructor
}

class Child extends Parent {
    Child() { }                // hidden super() → Parent() doesn't exist
}
```

```err "💥 compile error"
error: constructor Parent in class Parent cannot be applied to given types;
  required: int
  found:    no arguments
```

## 💻 `super.method()` — reuse, then add

```java
class BoxWeight extends Box {
    @Override
    void show() {
        super.show();                              // parent's version first
        System.out.println("weight = " + weight);  // then the extra part
    }
}
```

:::trap
`new BoxPrice(...)` creates **one** object, not three. `super(...)` initialises the parent *part* of the same object — no separate parent object is ever made.
:::

:::trap
**Constructors are not inherited** and therefore can't be overridden. `BoxWeight` doesn't get `Box(double l, double h, double w)` for free — it must declare its own and pass values up with `super(...)`.
:::

@sheet vs | Comparison · this vs super

# ✦ `this` [[vs]] `super` ✦

| | `this` | `super` |
|---|---|---|
| Refers to | the current object | the **parent part** of the current object |
| Field | `this.x` → this class's field | `super.x` → the parent's (hidden) field |
| Method | `this.f()` → this class's version | `super.f()` → the parent's version |
| Constructor call | `this(...)` → another constructor of the **same** class | `super(...)` → a constructor of the **parent** |
| Position | first statement | first statement |
| Added automatically? | never | `super()` — when you write neither `this(...)` nor `super(...)` |
| In a static method | ✗ | ✗ |

```sketch
            ┌──────────────────────────────┐
  this ───→ │ BoxWeight object             │
            │ ┌──────────────────────────┐ │
            │ │ Box part     ← super     │ │
            │ └──────────────────────────┘ │
            │ weight                       │
            └──────────────────────────────┘
```

:::mistake
Writing `this(...)` **and** `super(...)` in one constructor ✗ — both want to be first. Put `super(...)` in the constructor that `this(...)` delegates to.
:::

@sheet | Ch 03 · Types of inheritance

# ✦ TYPES OF INHERITANCE ✦

```sketch
   SINGLE            MULTILEVEL             HIERARCHICAL
     A                   Box                      Shapes
     │                    │                 ┌───────┼────────┐
     ↓                    ↓                 ↓       ↓        ↓
     B                BoxWeight          Circle  Square  Triangle
                          │
                          ↓
                       BoxPrice

   MULTIPLE  ✗ (classes)                  HYBRID  (mix of the above)
     A       B                                   A
      ╲     ╱                                 ┌──┴──┐
       ↘   ↙                                  ↓     ↓
         C      class C extends A, B ✗        B     C
                                               ╲   ╱
                                                ↘ ↙
                                                 D    ✗ with classes
```

| type | Java classes? |
|---|---|
| Single | ✓ |
| Multilevel | ✓ |
| Hierarchical | ✓ |
| Multiple | ✗ — ✓ only through **interfaces** (Ch 05) |
| Hybrid | ✗ with classes — ✓ through interfaces |

## 💎 Why no multiple inheritance? — the diamond problem

```sketch
                 A    greet()
              ↙     ↘
     B greet()        C greet()      both override greet()
              ↘     ↙
                 D                   D d = new D();
                                     d.greet();   → B's or C's ??
```

Two parents could provide **different** code for the same method — the child can't pick. Two parents also means two constructor chains and two copies of A's fields. Java avoids the whole mess: **one parent class**, but **many interfaces**.

:::trap
"Java doesn't support multiple inheritance" — precisely: no multiple inheritance **of classes (state & implementation)**. A class *can* implement many interfaces (multiple inheritance **of type**).
:::

:::mistake
`class A extends A` or `A extends B, B extends A` — cyclic inheritance ✗ compile error.
:::

@sheet | Ch 03 · Polymorphism & overloading

# ✦ POLYMORPHISM ✦

## 🧠 IDEA

**Poly** = many, **morph** = forms → one name, many behaviours.

## 🌍 IN REAL LIFE

The same person acts as a **student** in class, an **athlete** on the field, a **son** at home, an **employee** at work. One person, many forms — the situation decides the behaviour.

```sketch
                     POLYMORPHISM
               ┌───────────┴────────────┐
               ↓                        ↓
         COMPILE-TIME                RUNTIME
           (static)                 (dynamic)
               │                        │
          OVERLOADING              OVERRIDING
       same name, different    same signature in
       parameter lists         parent and child
       compiler picks by       JVM picks by the
       the ARGUMENTS           actual OBJECT
```

# ✦ METHOD OVERLOADING ✦ (compile-time)

Same method name, **different parameter list** — in the same class (or inherited).

```java "Numbers.java" run
public class Numbers {
    int    sum(int a, int b)        { return a + b; }
    double sum(double a, int b)     { return a + b; }
    int    sum(int a, int b, int c) { return a + b + c; }

    public static void main(String[] args) {
        Numbers obj = new Numbers();
        System.out.println(obj.sum(2, 3));       // sum(int, int)
        System.out.println(obj.sum(2.5, 3));     // sum(double, int)
        System.out.println(obj.sum(1, 3, 7));    // 3 params
    }
}
```

```output
5
5.5
11
```

:::rule
Overload by **number**, **type** or **order** of parameters. Return type alone ✗ — Java can't choose by what you do with the result.
:::

```java "Calc.java" nocompile
class Calc {
    int    add(int a, int b) { return a + b; }
    double add(int a, int b) { return a + b; }   // only return type differs
}
```

```err "💥 compile error"
error: method add(int,int) is already defined in class Calc
```

## ☕ Automatic type promotion

```java "Overload.java" run
public class Overload {
    static void test(double a) { System.out.println("test(double) " + a); }

    public static void main(String[] args) {
        int i = 88;
        test(i);          // no test(int) → int is widened to double
    }
}
```

```output
test(double) 88.0
```

Java widens (`int → long → float → double`) **only if no exact match exists**.

:::connect
Constructor overloading (Ch 01) is the same idea. And `System.out.println` is heavily overloaded — `println(int)`, `println(String)`, `println(Object)` …
:::

@sheet | Ch 03 · Method overriding

# ✦ METHOD OVERRIDING ✦ (runtime)

## 🌍 IN REAL LIFE

A child inherits "cook dinner" from the parent but **redefines how** — same task name, new way of doing it.

```sketch
         Parent      void area()   "I am in shapes"
            │
            ↓  same method signature
         Child       void area()   "pi * r * r"
            │
            ↓
    new implementation REPLACES the inherited one
```

## 💻 EXAMPLE — Shapes

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Shapes shape  = new Shapes();
        Shapes circle = new Circle();
        Shapes square = new Square();
        shape.area();
        circle.area();
        square.area();
    }
}

class Shapes {
    void area() { System.out.println("I am in shapes"); }
}

class Circle extends Shapes {
    @Override                  // "compiler, check that I really override"
    void area() { System.out.println("Area is pi * r * r"); }
}

class Square extends Shapes {
    @Override
    void area() { System.out.println("Area is square of side"); }
}
```

```output
I am in shapes
Area is pi * r * r
Area is square of side
```

:::rule
1. **same name + same parameter list** (else it's overloading!)
2. return type: same, or a **subtype** (covariant return — `Box copy()` → `BoxWeight copy()` ✓)
3. access: same or **wider** — `public` → `protected` ✗ ("attempting to assign weaker access privileges")
4. can't override: `final` · `static` (hidden) · `private` (not inherited) · constructors
5. may not throw new or broader **checked** exceptions
:::

## 🧠 How does Java decide which `area()` runs?

```sketch
   Shapes circle = new Circle();
   circle.area();

   COMPILER  →  "does type Shapes have area()?"   ✓ → call allowed
   JVM       →  "what is the OBJECT really?"       Circle
             →  run Circle.area()
                (not in Circle? → look in Shapes → then Object)
```

This runtime lookup is **dynamic method dispatch** — how Java implements runtime polymorphism.

:::mistake
Forgetting `@Override` and typing `void Area()` or `void area(int r)` → you silently created a **new** method; the parent's still runs. `@Override` turns that bug into a compile error.
:::

@sheet | Ch 03 · Parent obj = new Child()

# ✦ POLYMORPHISM: `Parent obj = new Child()` ✦

@@must

```sketch
        Parent   obj   =   new Child();
        └──┬──┘            └─────┬─────┘
           ↓                     ↓
     REFERENCE TYPE          OBJECT TYPE
           ↓                     ↓
    WHAT members can I     WHICH overridden method
    access?                actually runs?
    (compiler · early)     (JVM · runtime · late)
```

:::aside
say it 10 times:<br>**reference → access**<br>**object → behaviour**
:::

## 💻 EXAMPLE 1 — one loop, many behaviours

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Shapes[] shapes = { new Circle(), new Square(), new Triangle() };
        for (Shapes s : shapes) {
            s.area();                 // ONE line of code, 3 behaviours
        }
    }
}

class Shapes {
    void area() { System.out.println("Shape area"); }
}
class Circle extends Shapes {
    void area() { System.out.println("pi * r * r"); }
}
class Square extends Shapes {
    void area() { System.out.println("side * side"); }
}
class Triangle extends Shapes {
    void area() { System.out.println("0.5 * b * h"); }
}
```

```output
pi * r * r
side * side
0.5 * b * h
```

Add a `Hexagon` tomorrow → the loop doesn't change. That's the real power.

## 💻 EXAMPLE 2 — the reference limits, the object decides

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        a.sound();                 // ✓ Dog's version runs (object type)
        // a.fetch();          ✗ type Animal has no fetch()

        if (a instanceof Dog) {
            Dog d = (Dog) a;   // downcast → reference now allows it
            d.fetch();
        }
    }
}

class Animal { void sound() { System.out.println("..."); } }

class Dog extends Animal {
    @Override void sound() { System.out.println("Bark"); }
    void fetch() { System.out.println("Fetching the ball"); }
}
```

```output
Bark
Fetching the ball
```

Wrong downcast → compiles, but crashes: `Animal x = new Animal(); Dog d = (Dog) x;` → **ClassCastException**. Check with `instanceof` first.

## 💻 EXAMPLE 3 — fields & static methods are NOT polymorphic

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Parent obj = new Child();
        System.out.println(obj.name);   // field         → reference type
        obj.instanceHello();            // overridden    → object type
        obj.staticHello();              // static method → reference type
    }
}

class Parent {
    String name = "parent field";
    void instanceHello()      { System.out.println("Parent instance"); }
    static void staticHello() { System.out.println("Parent static"); }
}

class Child extends Parent {
    String name = "child field";                      // HIDES the field
    @Override void instanceHello() { System.out.println("Child instance"); }
    static void staticHello()      { System.out.println("Child static"); }
}
```

```output
parent field
Child instance
Parent static
```

| what you use via `obj` | decided by | when |
|---|---|---|
| which members are allowed | reference type | compile time |
| a field | reference type | compile time |
| a static method | reference type | compile time |
| an overridden instance method | **object type** | **runtime** |

:::trap
Static methods are [[r:hidden, not overridden]]. `obj.staticHello()` follows the *reference* type → "Parent static". Putting `@Override` on a static method is a compile error: "static methods cannot be annotated with @Override".
:::

:::trap
Casting the reference does **not** change the object: `((Parent) new Child()).instanceHello()` still prints "Child instance".
:::

@sheet vs | Comparison · Overloading vs Overriding

# ✦ OVERLOADING [[vs]] OVERRIDING ✦

@@must

| | OVERLOADING | OVERRIDING |
|---|---|---|
| Where | same class (or a child adding a new version) | parent ↔ child — needs inheritance |
| Name | same | same |
| Parameters | **must differ** (number / type / order) | **must be identical** |
| Return type | anything — but it can't be the *only* difference | same or covariant (a subtype) |
| Access | anything | same or **wider** |
| `static` methods | ✓ can be overloaded | ✗ only hidden |
| `private` / `final` methods | ✓ can be overloaded | ✗ can't be overridden |
| Decided by | the **compiler**, from the argument types | the **JVM**, from the object's type |
| Binding | early (static) | late (dynamic) |
| Polymorphism | compile-time | runtime |
| `@Override` | ✗ compile error if used | ✓ always write it |
| Example | `sum(int, int)` · `sum(int, int, int)` | `Circle.area()` replaces `Shapes.area()` |

```sketch
   OVERLOADING                          OVERRIDING
   one class, many signatures           one signature, many classes

     Numbers                                  Shapes    area()
     ├─ sum(int, int)                            ↑
     ├─ sum(double, int)                   ┌─────┴─────┐
     └─ sum(int, int, int)               Circle      Square
                                         area()      area()

   compiler picks by the ARGUMENTS      JVM picks by the OBJECT
```

:::mistake
Writing `public boolean equals(Student s)` instead of `equals(Object o)` is **overloading**, not overriding — `HashSet` keeps calling the inherited `equals(Object)`, so your version never runs. `@Override` would have turned this into a compile error.
:::

:::remember
- different parameters → overloading · same signature in a child → overriding
- overloading = compiler decides · overriding = JVM decides at runtime
- changing only the return type or parameter *names* is neither → "already defined"
:::

@sheet | Ch 03 · final & static in inheritance

# ✦ `final` & `static` IN INHERITANCE ✦

## 🔒 3 jobs of `final`

| on | meaning | example |
|---|---|---|
| variable | can't be re-assigned (Ch 01) | `final int MAX = 10;` |
| method | can't be **overridden** | `final void area() { }` |
| class | can't be **extended** | `final class String`, all wrapper classes |

```sketch "early vs late binding"
   normal method     →  JVM decides at RUNTIME  →  LATE binding
   final / static /
   private method    →  can't be overridden     →  EARLY binding
                        (compile time — the call may even be inlined)
```

:::rule
- `abstract final class` ✗ — abstract *needs* a child, final *forbids* one
- every method of a `final` class is effectively final
:::

## 🧊 Can we override static methods?

**No.** A static method belongs to the class and is resolved at compile time from the **reference type** — there's no object to "dispatch" on.

```java "the Box family"
class Box {
    static void greeting() {
        System.out.println("Hey, I am in Box class");
    }
}

class BoxWeight extends Box {
    static void greeting() {
        System.out.println("Hey, I am in BoxWeight class");
    }
}

Box b = new BoxWeight();
b.greeting();           // "Hey, I am in Box class" ← reference type wins
BoxWeight.greeting();   // "Hey, I am in BoxWeight class"
```

- static methods **are inherited** — `BoxWeight.greeting()` works even without redefining it
- redefining one in the child = **method hiding**
- instance method trying to "override" a static one (or vice-versa) ✗ compile error

:::reality
**Polymorphism doesn't apply to fields** either: a same-named field in the child *hides* the parent's (see Example 3). Rule of thumb: only **non-static, non-private, non-final instance methods** are polymorphic.
:::

@sheet | Ch 03 · Encapsulation

# ✦ ENCAPSULATION ✦

## 🧠 IDEA — it's NOT just "make variables private"

```sketch
         DATA
          +
        METHODS            →   ENCAPSULATION
          +                    (a capsule: inside is protected,
    CONTROLLED ACCESS           outside sees only safe buttons)
```

## 🌍 IN REAL LIFE

An **ATM**: you can withdraw, deposit, check balance — through buttons that verify your PIN and your balance. You can **never** open the cash box and grab notes yourself.

## ❓ WHY? — the problem

```java "without encapsulation" bad
class Student { int marks; }

Student s = new Student();
s.marks = -50;              // nothing stops nonsense data!
```

## 💻 EXAMPLE — with encapsulation

```java "Student.java"
class Student {

    private int marks;
//!   ↑ private → protect the internal state

    public void setMarks(int marks) {
//!              ↑ setter → the ONLY way in, and it validates
        if (marks >= 0 && marks <= 100) {
            this.marks = marks;
        }
    }

    public int getMarks() {
//!             ↑ getter → controlled read
        return marks;
    }
}
```

```java "Main.java — trying to cheat" run
public class Main {
    public static void main(String[] args) {
        Student s = new Student();
        s.setMarks(85);
        s.setMarks(-50);                  // rejected by the setter
        // s.marks = -50;        ✗ marks has private access
        System.out.println(s.getMarks());
    }
}

class Student {
    private int marks;
    public void setMarks(int marks) {
        if (marks >= 0 && marks <= 100) this.marks = marks;
    }
    public int getMarks() { return marks; }
}
```

```output
85
```

## ✓ What you gain

- **validation** in one place
- **read-only** field → getter only (e.g. `accountNo`); **write-only** → setter only (e.g. a password)
- change the inside (store marks as `double`?) without breaking code outside
- debugging: data changes through **one door** — put a breakpoint there

:::define
[[b:Data hiding]] — keeping fields `private` so they can't be accessed directly. It is the main *tool* of encapsulation; encapsulation is the bigger idea: bundling data with the methods that guard it.
:::

:::mistake
`private` fields + a setter that accepts **anything** = zero protection. [[u:Encapsulation lives in the *checks*, not in the keyword.]]
:::

@sheet | Ch 03 · Abstraction

# ✦ ABSTRACTION ✦

## 🧠 IDEA

Show [[o:**what**]] an object does, hide **how** it does it.

```sketch
         COMPLEX SYSTEM
     (fuel injection, sparks,
      gears, ECU software …)
               │
               │  hide details
               ↓
        SIMPLE INTERFACE
     steering · pedals · start
               │
               ↓
          USER USES IT
```

## 🌍 IN REAL LIFE

You **drive** a car with a steering wheel and two pedals — you don't need to understand combustion. You **send** a WhatsApp message without knowing about TCP/IP.

## 💻 Abstraction at every level

```java "Car.java" run
public class Main {
    public static void main(String[] args) {
        Car car = new Car();
        car.start();                // the user only knows "start"
    }
}

class Car {
    public void start() {           // simple, public
        injectFuel();
        igniteSpark();
        System.out.println("Car started");
    }
    private void injectFuel()  { /* complex detail, hidden */ }
    private void igniteSpark() { /* complex detail, hidden */ }
}
```

```output
Car started
```

- a **method** is abstraction: `Arrays.sort(arr)` — you don't care which algorithm runs inside
- a **class** with a small public API hides private helpers (`resize()` in our ArrayList, Ch 06)
- `List<Integer> list = new ArrayList<>();` — you code against **what** a List does
- **abstract classes & interfaces** (Ch 05) are Java's tools for *designing* with abstraction

:::mistake
"Abstraction = the `abstract` keyword" ✗. The keyword is one tool. Abstraction is the **idea** of hiding complexity behind a simple interface — a plain method already does it.
:::

@sheet vs | Comparison · Encapsulation vs Abstraction

# ✦ ENCAPSULATION [[vs]] ABSTRACTION ✦

| | ENCAPSULATION | ABSTRACTION |
|---|---|---|
| Question it answers | **how** do I protect the data? | **what** should the user see? |
| View | inside (implementation level) | outside (design level) |
| Hides | data (internal state) | complexity (implementation details) |
| Achieved with | `private` fields + validating getters/setters | abstract classes, interfaces, public API methods |
| ATM example | locked cash box, PIN-checked operations | a screen with 4 simple buttons |
| Java example | `private int marks` + `setMarks()` | `List` interface, `car.start()` |

```sketch
    ABSTRACTION = what you see       ENCAPSULATION = what's locked
   ┌─────────────────────────┐      ┌─────────────────────────────┐
   │ [Withdraw]  [Deposit]   │      │ private balance             │
   │ [Balance]   [PIN]       │      │ private pin                 │
   └─────────────────────────┘      │ withdraw() checks pin, bal  │
                                    └─────────────────────────────┘
```

:::idea
They work **together**: encapsulation is *how* you build the capsule; abstraction is the *simple face* the capsule shows. Good encapsulation makes abstraction possible.
:::

## ⭐ CHAPTER 03 — REMEMBER

:::remember
- `extends` = IS-A; one parent class only; private & constructors are not inherited
- constructors run **parent first**; missing `super(...)` → hidden `super()`
- **reference type → what you can access · object type → which overridden method runs**
- overloading = compile time (different params) · overriding = runtime (same signature)
- static methods & fields are **hidden**, not overridden · `final` method = can't override
- encapsulation = data + methods + controlled access · abstraction = show what, hide how
:::

:::practice 🧪 PRACTICE — CHAPTER 03
### 🧪 QUICK CHECK
1. `Box b = new BoxWeight(2, 3, 4, 8); System.out.println(b.weight);` — compiles?
2. Parent has `void f(int x)`, child declares `void f(long x)`. Overloading or overriding? Which runs for `child.f(5)`?
3. `A ← B ← C` (C extends B extends A), each constructor prints its letter. Output of `new C()`?

### 💻 CODE PRACTICE
1. `Employee` (name, baseSalary, `double salary()`), with `Manager` (+bonus) and `Intern` (half salary) overriding `salary()`. Store all in `Employee[]` and print the payroll with **one** loop.
2. Encapsulated `BankAccount`: private balance; `deposit` / `withdraw` reject negatives and overdrafts; no `setBalance`. Show that `acc.balance = 1000000` fails to compile.

### 🎯 INTERVIEW THINKING
```java
class A { void show() { System.out.println("A"); } }
class B extends A { void show() { System.out.println("B"); } }

A obj = new B();
((A) obj).show();
```
"A" or "B"? Why?

:::ans ☑ Answers
1. ✗ — reference type `Box` has no `weight`. 2. Overloading (different parameter type) — `f(5)` picks the exact match `f(int)`, the parent's. 3. `A B C` — parent constructors finish first.
**Interview:** `B`. A cast changes only the *reference type* (what may be called). Which overridden method runs is always decided by the **object** — a `B`.
:::
:::

:::teach
1. Copy-paste Box → BoxWeight → BoxPrice: feel the pain
2. Parent/child analogy → `extends`
3. Print the constructor chain, ask for the order
4. `Shapes[]` loop → polymorphism in one line
5. Board: "reference decides ACCESS, object decides BEHAVIOUR"
6. `marks = -50` bug → encapsulation; ATM → abstraction
:::

:::connect 🔗 NEXT →
`protected`, default, `private`, `public` — who exactly can see what across packages? And who is the parent of every class, even `Box`? → **Access control & the `Object` class** (Chapter 04).
:::
