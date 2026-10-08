@sheet | Ch 04 · Access modifiers

@chapter 04 | ACCESS CONTROL • PACKAGES • OBJECT CLASS | private · default · protected · public · built-in packages · Object · toString · equals · hashCode · getClass · instanceof | 🎬 OOP 4

# ✦ ACCESS MODIFIERS ✦

## 🧠 IDEA

An access modifier decides **who is allowed to see a member** (field, method, constructor, nested class). Java has 4 levels — from most locked to most open:

`private` → *default* (no keyword) → `protected` → `public`

:::aside
default access has **no keyword** — you just write nothing
:::

## 🌍 IN REAL LIFE

```sketch "your house"
   private    →  your diary         only YOU
   default    →  the family fridge  everyone in the SAME house (package)
   protected  →  family heirlooms   the house + your CHILDREN, even
                                    in another city (other package)
   public     →  the doorbell       ANYONE on the street
```

## 📋 THE ACCESS MATRIX

@@must

```sketch
                 SAME     SAME      CHILD in        OTHER
                 CLASS    PACKAGE   other package   (world)
   private        ✓        ✗          ✗              ✗
   default        ✓        ✓          ✗              ✗
   protected      ✓        ✓          ✓ *            ✗
   public         ✓        ✓          ✓              ✓

   * only through inheritance — see the next page!
```

| | class | package | subclass (same pkg) | subclass (other pkg) | world |
|---|---|---|---|---|---|
| `public` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `protected` | ✓ | ✓ | ✓ | ✓ * | ✗ |
| *default* | ✓ | ✓ | ✓ | ✗ | ✗ |
| `private` | ✓ | ✗ | ✗ | ✗ | ✗ |

## 💻 Class `A` — the access demo

```java "com/kunal/access/A.java"
package com.kunal.access;

public class A {
    protected int num;      // package + children
    String name;            // default → package only
    int[] arr;

    public int getNum() { return num; }            // public door
    public void setNum(int num) { this.num = num; }

    public A(int num, String name) {
        this.num = num;
        this.name = name;
        this.arr = new int[num];
    }
}
```

From `com.kunal.singleton.Main` (other package, **not** a child): `a.getNum()` ✓ · `a.num` ✗ · `a.name` ✗.

:::rule
- a **top-level** class can only be `public` or default — `private class A {}` at top level ✗ (nested classes may use all four)
- a `public` class must live in a file with the same name
- overriding can't **reduce** access (Ch 03): `public` → `protected` ✗
:::

## 🧭 When to use which?

- fields → `private` (+ getters/setters when needed) — encapsulation
- methods other code needs → `public`
- helpers used only inside the class → `private`
- "hooks" meant for subclasses → `protected`
- package-internal helpers → default
- constructor → `private` when objects must be controlled (Singleton)

@sheet | Ch 04 · The protected nuance

# ✦ THE `protected` NUANCE ✦

@@high

## 🧠 IDEA

In **another package**, a subclass can use a protected member [[r:only through inheritance]] — on *itself* (or objects of its own type / its subtypes). It can **not** poke at the protected members of an arbitrary parent object.

```java "one/Base.java"
package one;

public class Base {
    protected void display() { System.out.println("in Base"); }
}
```

```java "two/Derived.java"
package two;
import one.Base;

public class Derived extends Base {
    void test(Base b, Derived d) {
        display();                // ✓ inherited — called on this
        d.display();              // ✓ a Derived reference
        new Derived().display();  // ✓ a Derived object
        b.display();              // ✗ has protected access in Base
        new Base().display();     // ✗ has protected access in Base
    }
}
```

```sketch
            package one                   package two
        ┌──────────────────┐          ┌────────────────────────────┐
        │ Base             │  extends │ Derived                    │
        │ protected        │ ←─────── │                            │
        │   display()      │          │ this.display()       ✓     │
        └──────────────────┘          │ derivedRef.display() ✓     │
                                      │ baseRef.display()    ✗     │
                                      │ new Base().display() ✗     │
                                      └────────────────────────────┘
```

## ❓ WHY this rule?

If `b` is just "some `Base`", it might really be `OtherChild` — a sibling class that `Derived` knows nothing about. Letting `Derived` tamper with a *stranger's* protected internals would be unsafe. Its **own** kind (`Derived` and its subclasses)? Fine — that's shared family knowledge.

:::trap
"protected = visible to all subclasses, everywhere" — only **through inheritance**. In a different package, `new Base().display()` does **not** compile, even inside a subclass of `Base`. (In the **same** package, protected behaves like default → everything ✓.)
:::

:::trap
A **default** (package-private) member is **not inherited** by a subclass in another package at all: calling it there → "cannot find symbol".
:::

@sheet | Ch 04 · Built-in packages

# ✦ BUILT-IN PACKAGES ✦

## 🧠 IDEA

The JDK ships thousands of ready classes, organised in packages. Know the big ones:

| package | what lives there | examples |
|---|---|---|
| `java.lang` | core language — **auto-imported** | `String`, `Math`, `System`, `Object`, `Integer`, `Thread`, exceptions |
| `java.util` | collections & utilities | `ArrayList`, `HashMap`, `Scanner`, `Arrays`, `Collections`, `Random` |
| `java.io` | input / output, files | `File`, `BufferedReader`, `InputStreamReader`, `PrintStream` |
| `java.net` | networking | `URL`, `Socket`, `URI` (+ `java.net.http.HttpClient`) |
| `java.awt` | old GUI toolkit | `Frame`, `Button`, `Color`, `Graphics` |
| `javax.swing` | GUI built on AWT | `JFrame`, `JButton`, `JLabel` |
| `java.applet` | browser applets | `Applet` — *history now* (see below) |

```sketch "java is a tree of packages"
                         java
       ┌──────┬──────┬────┴───┬──────┬──────────┐
       ↓      ↓      ↓        ↓      ↓          ↓
     lang   util    io       net    awt       time
              │
       ┌──────┴──────┐
       ↓             ↓
    function    concurrent       ← SEPARATE packages: java.util.*
                                   does NOT import these
```

:::reality
**Applets are gone.** The Applet API was deprecated in JDK 9, deprecated *for removal* in JDK 17 and **removed in JDK 26** ([JEP 504](https://openjdk.org/jeps/504)). Mention it only as history; no browser runs applets today.
:::

:::connect
`System.out` (Ch 02) = class `System` from `java.lang` — that's why you never import it. `Scanner` is in `java.util` — that's why you always do.
:::

@sheet | Ch 04 · The Object class

# ✦ THE `Object` CLASS ✦

## 🧠 IDEA

`java.lang.Object` is the **root of every class hierarchy**. A class that extends nothing [[u:silently]] extends `Object`.

```sketch
                 Object          ← java.lang.Object — the root
                   ↑
                 Person          class Person { }
                   ↑                 = class Person extends Object { }
                 Student
                   ↑
             CollegeStudent      still an Object, 3 levels down
```

## ❓ WHY does it matter?

- **every** object (arrays too!) gets the same basic methods for free
- `Object o = anything;` works → `println(Object x)` can print *any* object
- before generics, collections stored `Object` — Chapter 06 starts exactly from that problem

## 📋 The methods every object has

| method | job | override it? |
|---|---|---|
| `toString()` | text form; default `ClassName@hexHash` | ✓ almost always |
| `equals(Object o)` | logical equality; default = `==` | ✓ for value-like classes |
| `hashCode()` | int "bucket number" for `HashSet`/`HashMap`; default identity-based | ✓ **whenever** `equals` is |
| `getClass()` | the runtime class of the object | ✗ it's `final` |
| `clone()` | field-by-field copy (`protected`, needs `Cloneable`) | Ch 06 |
| `finalize()` | old cleanup hook | ✗ deprecated |
| `wait()`, `notify()`, `notifyAll()` | thread coordination | ✗ `final` |

```java "ObjectDemo.java" run
public class ObjectDemo {
    int num;
    float gpa;

    ObjectDemo(int num, float gpa) { this.num = num; this.gpa = gpa; }

    @Override
    public boolean equals(Object obj) {
        return this.num == ((ObjectDemo) obj).num;   // "same num = equal"
    }

    public static void main(String[] args) {
        ObjectDemo obj1 = new ObjectDemo(12, 56.8f);
        ObjectDemo obj2 = new ObjectDemo(12, 78.9f);
        System.out.println(obj1 == obj2);         // two different objects
        System.out.println(obj1.equals(obj2));    // our rule says equal
        System.out.println(obj1.getClass().getName());
    }
}
```

```output
false
true
ObjectDemo
```

(Inside package `com.kunal.access` the last line prints `com.kunal.access.ObjectDemo` — the fully qualified name.)

:::mistake
This quick `equals` would crash on `obj1.equals("hi")` (ClassCastException) and on `null`. And it overrides `equals` **without** `hashCode` — which breaks `HashSet`/`HashMap` (next page).
:::

@sheet | Ch 04 · equals & hashCode

# ✦ `equals()` + `hashCode()` ✦

## 🧠 IDEA — how a HashSet thinks

```sketch
   set.add(x)
       │
       ↓  ① x.hashCode()  → which BUCKET?
   ┌───────┬───────┬───────┬───────┬───────┐
   │   0   │   1   │   2   │   3   │   4   │   buckets
   └───────┴───────┴───────┴───────┴───────┘
                       │
                       ↓  ② equals() with each item IN THAT BUCKET only
                  already there?  → don't add
```

If two "equal" objects land in **different buckets**, `equals()` is never even asked → duplicates ✗.

## 💻 EXAMPLE — doing it right

```java "Main.java" run hl=21-27,29-32
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        Set<Student> set = new HashSet<>();
        set.add(new Student(15, "Kunal"));
        set.add(new Student(15, "Kunal"));   // the "same" student again
        System.out.println(set.size());
        System.out.println(new Student(15, "Kunal"));
    }
}

class Student {
    private final int rno;
    private final String name;

    Student(int rno, String name) { this.rno = rno; this.name = name; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                    // same object
        if (!(o instanceof Student)) return false;     // null / other type
        Student other = (Student) o;
        return rno == other.rno && Objects.equals(name, other.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(rno, name);         // SAME fields as equals
    }

    @Override
    public String toString() {
        return "Student{rno=" + rno + ", name=" + name + "}";
    }
}
```

```output
1
Student{rno=15, name=Kunal}
```

Delete `hashCode()` and run again → `2` — two "equal" students both stored.

:::rule
**The contract**
1. `a.equals(b)` is true → `a.hashCode() == b.hashCode()` **must** be true
2. same hash code does **not** mean equal (collisions are allowed)
3. `equals` must be reflexive, symmetric, transitive, consistent — and `x.equals(null)` is `false`
4. override [[r:both or neither]], using the **same fields**
:::

:::trap
Override `equals()` without `hashCode()` → it compiles, it runs, and it silently breaks every `HashSet`/`HashMap`: `contains()` says false for an "equal" object, duplicates appear.
:::

@sheet vs | Comparison · == vs equals()

# ✦ `==` [[vs]] `.equals()` ✦

| | `==` | `.equals()` |
|---|---|---|
| What is it | operator | method (from `Object`) |
| On primitives | compares **values** ✓ | ✗ can't call methods on primitives |
| On references | **same object?** (identity) | **same content?** — *if the class overrides it* |
| Default in `Object` | identity | identity too (until overridden!) |
| `String` | same object in memory? | same characters? |
| Customisable | ✗ | ✓ override it |
| With `null` | `x == null` is safe | `null.equals(x)` → NullPointerException |

```java "verified on Java 25" run
public class Main {
    public static void main(String[] args) {
        String x = "hi";
        String y = "hi";              // same pooled literal
        String z = new String("hi");  // forced new object
        System.out.println((x == y) + " " + (x == z) + " " + x.equals(z));

        Integer a = 127, b = 127, c = 128, d = 128;
        System.out.println((a == b) + " " + (c == d) + " " + c.equals(d));
    }
}
```

```output
true false true
true false true
```

```sketch
       STRING POOL (part of heap)            HEAP
       ┌──────────┐                      ┌──────────┐
  x ──→│   "hi"   │←── y                 │   "hi"   │←── z  (new String)
       └──────────┘                      └──────────┘
     x == y  ✓ same object             x == z       ✗ different objects
                                       x.equals(z)  ✓ same characters
```

:::trap
`Integer` values from −128 to 127 are cached, so `==` *seems* to work in small tests and fails at 128. Rule: [[u:**objects → `.equals()`**, primitives → `==`]].
:::

:::mistake
`if (name.equals("Kunal"))` crashes when `name` is `null`. Safer: `"Kunal".equals(name)` or `Objects.equals(name, "Kunal")`.
:::

@sheet | Ch 04 · getClass & instanceof

# ✦ `getClass()` & `instanceof` ✦

## 🧠 IDEA

- `getClass()` → the **exact** runtime class of the object
- `x instanceof T` → **IS-A** test: is the object a `T` or any subtype of `T`?

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println(a.getClass().getSimpleName()); // real type
        System.out.println(a instanceof Dog);
        System.out.println(a instanceof Animal);
        System.out.println(a instanceof Object);

        Animal b = null;
        System.out.println(b instanceof Animal);             // null → false

        if (a instanceof Dog d) {      // Java 16+: test + cast in one step
            d.bark();
        }
    }
}

class Animal { }
class Dog extends Animal { void bark() { System.out.println("Woof"); } }
```

```output
Dog
true
true
true
false
Woof
```

| | `getClass()` | `instanceof` |
|---|---|---|
| Answers | "exactly which class?" | "is it a kind of …?" |
| `Dog` object vs `Animal` | `Dog` ≠ `Animal` | ✓ true |
| On `null` | NullPointerException | `false` |

```java "unrelated types" nocompile
public class Test {
    public static void main(String[] args) {
        String s = "hello";
        System.out.println(s instanceof Integer);
    }
}
```

```err "💥 compile error"
error: incompatible types: String cannot be converted to Integer
```

:::trap
`null instanceof Anything` is always **false** — no exception. That's why `instanceof` is the classic first line of `equals()`.
:::

## ⭐ CHAPTER 04 — REMEMBER

:::remember
- `private` < default < `protected` < `public`; top-level classes: only `public` or default
- protected in another package = only **through inheritance** (on your own type)
- `java.lang` is auto-imported; sub-packages are separate packages
- every class extends `Object` → `toString`, `equals`, `hashCode`, `getClass` for free
- override `equals` → override `hashCode` (same fields)
- `==` = same object · `.equals()` = same content · `instanceof` = IS-A
:::

:::practice 🧪 PRACTICE — CHAPTER 04
### 🧪 QUICK CHECK
1. `two.Derived extends one.Base`. Inside `Derived`, does `new Base().display()` compile if `display()` is protected?
2. Two `Student`s are equal by `equals()`, but `hashCode()` isn't overridden. Add both to a `HashSet` — size?
3. `String a = "java"; String b = new String("java");` → `a == b`? `a.equals(b)`?

### 💻 CODE PRACTICE
1. `Point(x, y)`: override `toString`, `equals`, `hashCode`. Prove it works as a `HashMap` key: `map.get(new Point(1, 2))`.
2. Packages `bank` and `app`: `Account` with a private balance, a protected `applyInterest()`, a default `audit()`. In `app`, `SavingsAccount extends Account` — list which calls compile and why.

### 🎯 INTERVIEW THINKING
A class overrides `equals()` to compare `id`, but not `hashCode()`. Everything "works" in your tests with `ArrayList`. When does it break, and how would the bug look in production?

:::ans ☑ Answers
1. ✗ — outside the package, protected works only through inheritance (`this` / `Derived` references). 2. Almost always **2** — different default hash codes → different buckets. 3. `false`, `true`.
**Interview:** `ArrayList.contains` uses only `equals`, so it looks fine. The moment the objects go into a `HashSet` or become `HashMap` keys, lookups miss and duplicates appear — "the cache never hits", "the set has two copies of the same user".
:::
:::

:::teach
1. House analogy: diary · fridge · heirlooms · doorbell
2. Fill the access matrix together on the board
3. Two-package demo — let `new Base().display()` fail live
4. Print an object without `toString()` — "what's that @1b6d…?"
5. HashSet duplicates → motivate `hashCode()`
6. Quiz: `getClass()` vs `instanceof` on a `Dog`
:::

:::connect 🔗 NEXT →
`Object` gives every class common methods with *default* behaviour. What if a parent wants to **force** every child to write its own `career()`? And how do we get multiple inheritance without the diamond problem? → **Abstract classes & interfaces** (Chapter 05).
:::
