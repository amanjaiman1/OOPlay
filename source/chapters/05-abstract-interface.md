@sheet | Ch 05 · The multiple inheritance problem

@chapter 05 | ABSTRACT CLASS • INTERFACE • ANNOTATIONS | multiple inheritance problem · abstract classes · interfaces · default & static methods · extending & nested interfaces · @Override | 🎬 OOP 5

# ✦ THE MULTIPLE INHERITANCE PROBLEM ✦

## ❓ WHY this chapter?

Two needs pull in opposite directions:

1. A parent wants to **force** children to write certain methods ("every child must define `career()`"), without writing them itself.
2. A class wants behaviour from **many** parents (a `Car` is an engine-thing, a brake-thing, a media-thing) — but Java allows only **one** parent class because of the diamond problem.

```sketch
        A greet() { "A" }      ← code + state in both parents
           ↙       ↘
   B greet() {"B"}  C greet() {"C"}
           ↘       ↙
             D             d.greet() → "B" or "C" ??   ✗ classes

   FIX: parents that only PROMISE a method (no code, no state)
        → nothing can conflict → many parents become safe ✓
```

:::idea
**Abstract class** = a *partly built* parent: some code, some promises. **Interface** = a *pure contract*: "whoever signs me must provide these methods". A class may extend one class but sign **many** contracts.
:::

@sheet | Ch 05 · Abstract classes

# ✦ ABSTRACT CLASSES ✦

## 🧠 IDEA

An `abstract` class is an **incomplete** class. It may declare `abstract` methods — methods with **no body** — that every concrete child [[r:must]] implement.

## 🌍 IN REAL LIFE

A parent says: *"Every child of mine **must** choose a career and a partner — but I won't decide for them."* The rule is fixed; the details are each child's responsibility.

:::define
- [[b:abstract method]] — declared without a body: `abstract void career();` — "subclass responsibility"
- [[b:abstract class]] — declared with `abstract`; can't be instantiated; may mix abstract and concrete methods
:::

## 💻 EXAMPLE

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Son son = new Son(30);
        son.career();
        son.normal();

        Parent daughter = new Daughter(28);  // abstract type as ref ✓
        daughter.career();

        Parent.hello();                       // static method ✓
        // Parent mom = new Parent(45);       ✗ Parent is abstract
    }
}

abstract class Parent {
    int age;
    final int VALUE;

    Parent(int age) {                // constructor ✓ (runs via super)
        this.age = age;
        VALUE = 32456789;
    }

    static void hello() { System.out.println("hey"); }
    void normal() { System.out.println("this is a normal method"); }

    abstract void career();                   // no body → child decides
    abstract void partner();
}

class Son extends Parent {
    Son(int age) { super(age); }
    @Override
    void career()  { System.out.println("I am going to be a doctor"); }
    @Override
    void partner() { System.out.println("I love Pepper Potts"); }
}

class Daughter extends Parent {
    Daughter(int age) { super(age); }
    @Override
    void career()  { System.out.println("I am going to be a coder"); }
    @Override
    void partner() { System.out.println("I love Iron Man"); }
}
```

```output
I am going to be a doctor
this is a normal method
I am going to be a coder
hey
```

## 🧠 VISUALIZE IT

```sketch
            abstract class Parent
       ┌──────────────────────────────────┐
       │ age, VALUE            ✓ state    │
       │ Parent(int age)       ✓ ctor     │
       │ normal()  { … }       ✓ body     │
       │ career();             ✗ no body  │ ← promises the child
       │ partner();            ✗ no body  │   MUST keep
       └────────────────┬─────────────────┘
                ┌───────┴────────┐
                ↓                ↓
               Son            Daughter       each fills in
            "doctor"          "coder"        career() + partner()
```

## ❓ Why can't we write `new Parent(45)`?

It's incomplete — `mom.career()` would have **no code to run**. The compiler refuses: *"Parent is abstract; cannot be instantiated"*.

:::doubt "No objects… so why does an abstract class have a constructor?"
`new Son(30)` builds **one** object that contains a `Parent` part. `super(age)` runs `Parent`'s constructor to initialise *that part* (`age`, `VALUE`). A constructor **initialises**; only `new` **creates**.
:::

@sheet | Ch 05 · Abstract class rules

# ✦ ABSTRACT CLASS — THE RULES ✦

| inside an abstract class … | allowed? |
|---|---|
| abstract methods (zero or more) | ✓ |
| concrete methods, `final` methods | ✓ |
| constructors | ✓ — run through `super(...)` |
| instance, static and `final` fields | ✓ |
| static methods → `Parent.hello()` | ✓ |
| `abstract static void f();` | ✗ illegal combination of modifiers |
| `abstract Parent();` (abstract constructor) | ✗ modifier abstract not allowed here |
| `new Parent(…)` | ✗ cannot be instantiated |
| `abstract final class` | ✗ illegal combination of modifiers |

## ❓ Why no `abstract static`?

A static method is called on the **class**: `Parent.career()`. If it were abstract there'd be an **empty** method to call — and static methods can't be overridden, so no child could ever fill it in.

## ⚠️ Forgot one abstract method?

```java "Son.java" nocompile
abstract class Parent {
    abstract void career();
    abstract void partner();
}

class Son extends Parent {
    void career() { }        // partner() forgotten
}
```

```err "💥 compile error"
error: Son is not abstract and does not override abstract method partner() in Parent
```

Either implement **all** abstract methods, or declare the child `abstract` too.

:::trap
"An abstract class must contain an abstract method" ✗ — zero abstract methods is legal (you still can't instantiate it). The reverse **is** true: a class with even one abstract method **must** be declared abstract.
:::

:::trap
"Multiple inheritance via abstract classes?" ✗ — an abstract class is still a **class**. `class C extends A, B` is illegal whether A and B are abstract or not.
:::

@sheet | Ch 05 · Interfaces

# ✦ INTERFACES ✦

## 🧠 IDEA

An interface is a [[o:**contract**]]: it lists [[u:*what* a class must be able to do, never *how*]]. A class **signs** it with `implements`.

:::aside
abstract class = **IS-A**<br>interface = **CAN-DO**
:::

## 🌍 IN REAL LIFE

A **power socket**: any appliance with the right plug works — the socket doesn't care if it's a phone charger or a kettle. Or a job description: "every *Driver* must `start()`, `stop()`, `brake()`" — each driver does it their own way.

:::define
An [[b:interface]] is a reference type containing abstract method signatures (plus, since Java 8, `default` and `static` methods) and constants. A class can implement **any number** of interfaces.
:::

## ✍️ SYNTAX — what Java adds silently

```java
interface Engine {
    int PRICE = 78000;     // = public static final int PRICE = 78000;
    void start();          // = public abstract void start();
}
```

## 💻 EXAMPLE — one car, three contracts

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Car car = new Car();
        car.start();
        car.brake();
        System.out.println(Engine.PRICE);
    }
}

interface Engine {
    int PRICE = 78000;
    void start(); void stop(); void acc();
}
interface Brake { void brake(); }
interface Media { void start(); void stop(); }   // same start()/stop()!

class Car implements Engine, Brake, Media {
    @Override
    public void start() { System.out.println("I start like a normal Car"); }
    @Override
    public void stop()  { System.out.println("I stop like a normal Car"); }
    @Override
    public void acc()   { System.out.println("I accelerate"); }
    @Override
    public void brake() { System.out.println("I brake like a normal Car"); }
}
```

```output
I start like a normal Car
I brake like a normal Car
78000
```

```sketch
     (interface)          (interface)          (interface)
       Engine               Brake                Media
   start() stop() acc()    brake()          start()  stop()
          ↑                   ↑                    ↑
          └─────────────── implements ─────────────┘
                              │
                             Car     ← ONE class, THREE contracts
                                       ONE start() serves Engine + Media
```

:::rule
- implementing methods must be **`public`** — `void start() { }` → "attempting to assign weaker access privileges; was public"
- interface variables are constants → `PRICE = 1;` in a class → "cannot assign a value to static final variable PRICE"
- no constructors, no instance fields → an interface holds **no state**
- implement **every** abstract method, or the class must be `abstract`
:::

:::trap
Same abstract method in two interfaces (`Engine.start()`, `Media.start()`) is **not** a diamond problem — neither has code, so **one** implementation satisfies both.
:::

@sheet | Ch 05 · Interface references & swappable parts

# ✦ INTERFACE REFERENCES ✦

## 🧠 Same rule as Ch 03

```java
Engine car = new Car();      // interface type as reference ✓
car.acc();                   // ✓ Engine declares acc()
car.brake();                 // ✗ Engine has no brake()
Media carMedia = new Car();
carMedia.stop();             // runs Car's stop() — the OBJECT decides
```

**Reference type → what you may call · object type → which code runs.**

## 💻 "Separate classes, same interface" — plug-in parts

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        NiceCar car = new NiceCar();
        car.start();
        car.startMusic();
        car.upgradeEngine();       // swap the part at RUNTIME
        car.start();
    }
}

interface Engine { void start(); }
interface Media  { void start(); }

class PowerEngine implements Engine {
    public void start() { System.out.println("Power engine start"); }
}
class ElectricEngine implements Engine {
    public void start() { System.out.println("Electric engine start"); }
}
class CDPlayer implements Media {
    public void start() { System.out.println("Music start"); }
}

class NiceCar {
    private Engine engine = new PowerEngine(); // HAS-A Engine (any!)
    private Media player = new CDPlayer();     // HAS-A Media

    void start()         { engine.start(); }
    void startMusic()    { player.start(); }
    void upgradeEngine() { engine = new ElectricEngine(); }
}
```

```output
Power engine start
Music start
Electric engine start
```

```sketch
      NiceCar                       Engine slot
   ┌──────────────┐
   │ engine ●─────┼───→ PowerEngine ─ ─ upgradeEngine() ─ ─→ Electric…
   │ player ●─────┼───→ CDPlayer           (Media slot)
   └──────────────┘
   car.start() → engine.start() → whatever engine is plugged in now
```

:::idea
`Car implements Engine` says "a car **IS** an engine" — odd. `NiceCar` says "a car **HAS** an engine" — natural, and the engine is swappable. This is **composition**, and coding against the **interface** (`Engine`) instead of a class is what makes the swap possible.
:::

@sheet | Ch 05 · Extending interfaces · default & static

# ✦ EXTENDING INTERFACES ✦

```java "Main.java — extendDemo" run
public class Main implements B {
    public void fun()   { System.out.println("fun from A's contract"); }
    public void greet() { System.out.println("greet from B"); }

    public static void main(String[] args) {
        Main obj = new Main();
        obj.fun();
        obj.greet();
        A ref = obj;               // B extends A → Main IS-A A too
        ref.fun();
    }
}

interface A { void fun(); }
interface B extends A { void greet(); }    // B = A's methods + greet()
```

```output
fun from A's contract
greet from B
fun from A's contract
```

An interface `extends` interfaces (even **several**: `interface C extends A, B`). The implementing class owes **all** inherited methods.

# ✦ `default` & `static` METHODS ✦ (Java 8+)

## ❓ WHY default methods?

Add a method to an interface used by 1000 classes → all 1000 break. A `default` method ships **with a body**, so old classes keep compiling. (That's how `forEach()` was added to every collection.)

```java "Main.java — extendDemo2" run
public class Main implements A, B {
    @Override
    public void fun() {          // MUST override: A and B both give fun()
        A.super.fun();           // optionally reuse one parent's version
        System.out.println("Main's own fun");
    }

    public static void main(String[] args) {
        new Main().fun();
        A.greeting();            // static → call via the INTERFACE name
        // Main.greeting();      ✗ static interface methods: not inherited
    }
}

interface A {
    default void fun() { System.out.println("I am in A"); }
    static void greeting() { System.out.println("Hey I am static method"); }
}

interface B {
    default void fun() { System.out.println("I am in B"); }
}
```

```output
I am in A
Main's own fun
Hey I am static method
```

:::rule
**Default-method conflicts**
1. **class wins** — a method in the class (or its superclass) beats any interface default
2. **more specific interface wins** — `B extends A`, both define `fun()` → B's
3. two **unrelated** interfaces with the same default → compile error ("types A and B are incompatible") until you override it
:::

:::trap
Static interface methods are **not inherited** — not by implementing classes, not by sub-interfaces. `A.greeting()` ✓ · `obj.greeting()` / `Main.greeting()` ✗. They must have a body.
:::

:::reality
@@good Since Java 9 interfaces may also have **`private`** methods — helpers shared by default methods. Everything else in an interface is implicitly `public`.
:::

@sheet | Ch 05 · Nested interfaces

# ✦ NESTED INTERFACES ✦

## 🧠 IDEA

An interface declared **inside** a class (or another interface) — grouped with the class it belongs to. Use it as `Outer.InterfaceName`.

```java "Main.java — nested" run
public class Main {
    public static void main(String[] args) {
        A.NestedInterface obj = new B();   // Outer.Inner name
        System.out.println(obj.isOdd(6));
        System.out.println(obj.isOdd(7));
    }
}

class A {
    public interface NestedInterface {     // a member of class A
        boolean isOdd(int num);
    }
}

class B implements A.NestedInterface {
    @Override
    public boolean isOdd(int num) {
        return (num & 1) == 1;             // last bit 1 → odd
    }
}
```

```output
false
true
```

| | top-level interface | nested interface |
|---|---|---|
| allowed access | `public` or default | `public`, `protected`, `private` or default |
| static? | — | implicitly `static` (no outer object needed) |
| named as | `NestedInterface` | `A.NestedInterface` |

:::connect
`Map.Entry<K, V>` (Ch 07) is a real nested interface — `for (Map.Entry<String, Integer> e : map.entrySet())`.
:::

@sheet vs | Comparison · Abstract class vs Interface

# ✦ ABSTRACT CLASS [[vs]] INTERFACE ✦

@@must

| | ABSTRACT CLASS | INTERFACE |
|---|---|---|
| Keyword | `abstract class` | `interface` |
| A class uses it with | `extends` — **one** only | `implements` — **many** |
| Methods | abstract + concrete, any access | abstract (implicitly `public`) + `default` + `static` + `private` |
| Variables | anything: instance, static, final, non-final | only `public static final` constants |
| Constructors | ✓ (run via `super`) | ✗ |
| Holds state (instance fields) | ✓ | ✗ |
| Multiple inheritance | ✗ | ✓ — interfaces can even extend many interfaces |
| Can implement / extend the other | ✓ abstract class can implement interfaces | ✗ interface can't extend a class |
| Relationship | **IS-A** — a family of related classes | **CAN-DO** — a capability / contract |
| Use when | related classes share code **and** state | unrelated classes share a **capability** |
| JDK examples | `Number` (← `Integer`, `Double`), `AbstractList` | `Comparable`, `Runnable`, `List` |

```sketch "which one?"
   "they ARE the same kind of thing, sharing code/state" → ABSTRACT CLASS
         Animal  ←  Dog, Cat                (common: name, age, eat())

   "they CAN DO the same thing, otherwise unrelated"     → INTERFACE
         Comparable ←  String, Integer, Student
         Flyable    ←  Bird, Plane, Superman
```

:::trap
"Interfaces have default methods now, so they're the same as abstract classes" ✗. Interfaces still have **no state** (no instance fields), **no constructors**, and all non-private members are **public** — and a class can implement many of them.
:::

:::remember
- can't instantiate either one — both work as **reference types**
- abstract class = partial implementation for a family; interface = contract for anyone
- design tip: start with an interface; add an abstract class when implementations share code
:::

@sheet | Ch 05 · Annotations

# ✦ ANNOTATIONS ✦

## 🧠 IDEA

An annotation (`@Something`) is **metadata** stuck onto code. It doesn't change what the code does by itself — the **compiler, tools and frameworks** read it and act on it.

## 🌍 IN REAL LIFE

Labels on a parcel: "FRAGILE", "THIS SIDE UP". The contents don't change — but the delivery person handles the box differently.

| annotation | tells … | effect |
|---|---|---|
| `@Override` | compiler: "I mean to override" | ✗ error if nothing is overridden |
| `@Deprecated` | users: "don't use this any more" | warning wherever it's used |
| `@FunctionalInterface` | compiler: "exactly ONE abstract method" | ✗ error if 0 or 2+ (Ch 06 lambdas) |
| `@SuppressWarnings("unchecked")` | compiler: "I know, be quiet" | hides that warning (generic casts, Ch 06) |

## 💻 Why `@Override` saves you

```java "Student.java" nocompile
class Student {
    @Override
    public String tostring() {     // typo: small "s"
        return "Student";
    }
}
```

```err "💥 compile error — a GOOD error"
error: method does not override or implement a method from a supertype
```

Without `@Override` this compiles silently, and `println(student)` keeps printing `Student@1b6d3586` — a bug you'd hunt for an hour.

:::reality
Frameworks run on annotations: `@Test` (JUnit), `@Entity`, `@Autowired`, `@GetMapping` (Spring). You can define your own with `@interface` — good to know, not needed for this playlist.
:::

## ⭐ CHAPTER 05 — REMEMBER

:::remember
- abstract class: can't `new`; may have constructors, state, concrete & static methods
- abstract method: no body → children implement it or become abstract
- ✗ `abstract static` · ✗ abstract constructor · ✗ `abstract final`
- interface = contract: methods `public abstract`, variables `public static final`
- many interfaces per class → multiple inheritance of **type**, no diamond of state
- default conflicts: class wins → specific interface wins → else override (`X.super.m()`)
- static interface methods: call via the interface, never inherited
:::

:::practice 🧪 PRACTICE — CHAPTER 05
### 🧪 QUICK CHECK
1. Can an abstract class have a constructor? Who calls it, and when?
2. `interface Shape { int SIDES = 0; }` — can an implementing class write `SIDES = 4;`?
3. `class C implements A, B` where both interfaces have `default void hi()` — does it compile?

### 💻 CODE PRACTICE
1. Abstract `Shape` with abstract `area()` and concrete `describe()`; `Circle` and `Rectangle` extend it. Store both in `Shape[]` and print the areas in one loop.
2. Interfaces `Playable` and `Recordable`; `Phone` implements both. A `MusicSystem` **has-a** `Playable` and can swap it at runtime.

### 🎯 INTERVIEW THINKING
"Since Java 8 interfaces can have method bodies. So why do abstract classes still exist?"

:::ans ☑ Answers
1. ✓ — it runs through `super(...)` when a child object is created, to initialise the parent part. 2. ✗ — interface fields are `public static final`. 3. ✗ — unrelated duplicate defaults; `C` must override `hi()` (and may call `A.super.hi()`).
**Interview:** interfaces can't hold **state** (instance fields) or have **constructors**, and their members are public. An abstract class is a partial implementation with shared fields and protected helpers for a family of related classes.
:::
:::

:::teach
1. Recall the diamond problem from Ch 03
2. "Parent forces career()" story → `abstract`
3. Try `new Parent()` — read the error together
4. Interface = contract; `Car implements Engine, Brake, Media`
5. Swap engines in `NiceCar` → power of interface references
6. Build the comparison table with the class; quiz on default conflicts
:::

:::connect 🔗 NEXT →
Contracts make code flexible — but our home-made list stores **only `int`**. One class that works for *any* type, still type-safe? → **Generics** (Chapter 06).
:::
