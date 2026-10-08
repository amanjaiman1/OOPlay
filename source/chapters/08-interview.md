@sheet | Interview bank · Fundamentals

@chapter ★ | INTERVIEW • PROJECTS • REVISION | 85 interview questions · 3 mini projects · master map · one-page cheat sheet | ✍️ revise

# ✦ INTERVIEW BANK ✦

85 questions in 5 rounds. Answer **out loud** first, then read the answer. Numbers continue across pages so you can say "revise Q47".

```sketch
   🟢→ FUNDAMENTALS  15    definitions you must say in one breath
   🟡→ INTERMEDIATE  20    rules + the "why" behind them
   🔴→ TRICKY        20    where most candidates slip
   💻→ OUTPUT        15    predict, then open the answer
   🧠→ CONCEPTUAL    15    design-level thinking
```

## 🟢 FUNDAMENTALS

:::qa
Q: What is OOP? Name its four pillars.
A: A way of organising programs around **objects** that bundle data and behaviour. Pillars: **inheritance, polymorphism, encapsulation, abstraction**.

Q: Class vs object?
A: A class is the blueprint (logical, written once). An object is an instance created at runtime with `new`; it occupies heap memory and has its own state.

Q: What exactly does `new` do?
A: Allocates memory for the object on the heap at runtime, initialises fields (defaults → initialisers → constructor) and returns a **reference** to it.

Q: What is a constructor, and how is it different from a method?
A: A block that initialises a new object: same name as the class, no return type, runs automatically once per `new`, is never inherited and can't be `static`/`final`/`abstract`.

Q: When does Java give you a default constructor?
A: Only when the class declares **no constructor at all**. Write any constructor and the no-arg one disappears.

Q: What is `this`?
A: A reference to the current object. Uses: `this.field` (vs a parameter), `this(...)` (constructor chaining), passing or returning the current object.

Q: What is a static variable?
A: A class-level variable: one shared copy, created when the class loads, accessed as `ClassName.var` (e.g. `Human.population`).

Q: What is a package and why use one?
A: A namespace + folder for related classes. It prevents name clashes (two `Greeting` classes), organises code and acts as an access boundary.

Q: What is inheritance? Which keyword?
A: A child class acquiring a parent's members with `extends` — an **IS-A** relationship (`BoxWeight` is a `Box`).

Q: What is method overloading?
A: Same method name, different parameter lists (number / type / order). The compiler picks the version → compile-time polymorphism.

Q: What is method overriding?
A: A subclass redefining an inherited instance method with the **same signature**. The JVM picks the version from the object's type → runtime polymorphism.

Q: What is encapsulation?
A: Bundling data with the methods that operate on it **and** controlling access — private fields reached only through validating methods.

Q: What is abstraction?
A: Exposing only what an object does while hiding how — via simple public methods, abstract classes and interfaces.

Q: Name Java's access modifiers from most to least restrictive.
A: `private` → default (package-private) → `protected` → `public`.

Q: What is an interface?
A: A contract of methods a class promises to implement. Methods are implicitly `public abstract` (plus `default`/`static`/`private` with bodies), fields are `public static final`; a class can implement many.
:::

@sheet | Interview bank · Intermediate

## 🟡 INTERMEDIATE

:::qa
Q: Why can't a static method use instance variables directly?
A: Instance variables belong to an object, and a static method runs with **no current object** (`this` doesn't exist). Use a reference: `obj.field`.

Q: What does `super()` do, and where must it be?
A: Calls the parent's constructor; it must be the **first statement**. If you write neither `this(...)` nor `super(...)`, the compiler inserts `super()`.

Q: In what order do constructors run in `A ← B ← C` when you write `new C()`?
A: Calls climb up to `Object`, bodies finish top-down: `Object` → `A` → `B` → `C`. The parent part must be ready before the child's.

Q: What is dynamic method dispatch?
A: Resolving a call to an overridden method **at runtime** from the actual object's class — the mechanism behind runtime polymorphism.

Q: List the rules for a valid override.
A: Same name & parameters; same or covariant return type; same or **wider** access; no new or broader checked exceptions; the parent method must not be `final`, `static` or `private`.

Q: Can you overload `main()`?
A: Yes — but the launcher calls only the entry-point form (`public static void main(String[] args)`; Java 25 also accepts instance `main`). Other overloads are ordinary methods.

Q: What is a static block and when does it run?
A: Code that runs **once** when the class is initialised (first use) — for the main class, before `main()` starts. Used for complex static initialisation.

Q: Inner class vs static nested class?
A: Inner (non-static) objects are tied to an outer object — created as `outer.new Inner()` — and can use its instance members. Static nested classes need no outer object — `new Outer.Nested()` — and see only static outer members directly.

Q: How do you write a singleton?
A: `private` constructor + `private static` instance + `public static getInstance()`. Make it thread-safe with eager init, synchronisation, or simply `enum Singleton { INSTANCE }`.

Q: What does `final` mean on a variable, a method and a class?
A: Variable → assigned once. Method → can't be overridden. Class → can't be extended (`String`, wrapper classes).

Q: Can an abstract class have a constructor? Can you instantiate it?
A: It can have constructors (run via `super(...)` to set up the parent part), but `new AbstractClass()` is a compile error.

Q: Abstract class vs interface — the two differences that matter most?
A: (1) An abstract class can hold **state** and **constructors**; an interface can't. (2) A class extends **one** class but implements **many** interfaces.

Q: What are default methods and why were they added?
A: Interface methods with a body (Java 8). They let interfaces gain new methods without breaking every class that already implements them (e.g. `forEach`).

Q: A class implements two interfaces that both have `default void hi()`. What happens?
A: Compile error ("types … are incompatible") until the class overrides `hi()`; inside it may call `A.super.hi()`.

Q: Why must `hashCode()` be overridden together with `equals()`?
A: The contract says equal objects must have equal hash codes. `HashSet`/`HashMap` find the bucket by `hashCode()` first — break it and lookups miss, duplicates appear.

Q: `==` vs `equals()` for Strings?
A: `==` checks whether both references point to the **same object**; `equals()` compares the **characters**. Always use `equals()` for content.

Q: What are generics, and what do they buy you?
A: Type parameters (`List<T>`) — compile-time type safety, no casts, one reusable implementation for all types.

Q: What is type erasure?
A: The compiler removes generic type information after checking it; at runtime `T` becomes `Object` (or its bound). Hence no `new T[]`, no `instanceof T`.

Q: Checked vs unchecked exceptions?
A: Checked (subclasses of `Exception`, not `RuntimeException`) must be caught or declared with `throws`. Unchecked (`RuntimeException`, `Error`) aren't enforced by the compiler.

Q: Shallow vs deep copy?
A: Shallow copies each field's value — nested objects are **shared**. Deep copy also duplicates the nested mutable objects so the copies are fully independent.
:::

@sheet | Interview bank · Tricky

## 🔴 TRICKY

:::qa
Q: Can we override a static method?
A: No. A same-signature static method in the child **hides** the parent's; calls are resolved from the reference type at compile time, and `@Override` on it is a compile error.

Q: Can we override a private method?
A: No — private methods aren't inherited. A same-named method in the child is a brand-new, unrelated method.

Q: Can a constructor be `final`, `static` or `abstract`?
A: None of them — compile error. Constructors aren't inherited (so `final`/`abstract` are meaningless) and they initialise an instance (so `static` makes no sense).

Q: Is Java pass-by-reference for objects?
A: No — Java is **always pass-by-value**. For objects the value copied is the *reference*: you can mutate the shared object, but re-pointing the parameter never affects the caller (the `swap(Integer, Integer)` puzzle).

Q: `final StringBuilder sb = new StringBuilder("a"); sb.append("b");` — legal?
A: ✓ Legal. `final` freezes the **reference**, not the object; only `sb = new StringBuilder()` would fail.

Q: `Human h = null; h.population` where `population` is static — NullPointerException?
A: No — it prints the value. Static access is bound to the reference's **type** at compile time; the null object is never touched.

Q: A parent constructor calls a method that the child overrides. Which version runs, and what does it see?
A: The **child's** version (dynamic dispatch works even during construction) — but the child's fields aren't initialised yet, so it sees default values (`0`, `null`). See Q61.

Q: Can an interface have a constructor or instance fields?
A: No. Interfaces have no state: fields are implicitly `public static final` constants, and constructors are not allowed.

Q: Can an abstract class be `final`?
A: No — "illegal combination of modifiers": abstract needs a subclass, final forbids one.

Q: Does `import java.util.*;` import `java.util.function.Function`?
A: No. Sub-packages are separate packages; a wildcard import covers one package only.

Q: Can a top-level class be `private` or `static`?
A: Neither. Top-level classes are `public` or package-private; `static` applies only to nested classes.

Q: Overloads `f(long)`, `f(Integer)`, `f(Object)` — which one does `f(5)` call?
A: `f(long)`. Resolution order: exact/widening primitive first, then boxing, then varargs. (`f('a')` also picks `long`.) See Q59.

Q: Can you `new` an enum? Can an enum extend a class?
A: No and no. Constants are created by the JVM; every enum already extends `java.lang.Enum`. It **can** implement interfaces.

Q: What does `try { return 1; } finally { return 2; }` return?
A: `2` — a `return` in `finally` overrides the earlier one (and would even swallow an exception). Never return from `finally`.

Q: `try { return x; } finally { x = 2; }` with `int x = 1` — returned value?
A: `1`. The return value is evaluated and saved before `finally` runs; changing the local afterwards doesn't affect it. See Q65.

Q: Is `List<String>` a subtype of `List<Object>`?
A: No — generics are **invariant**. Otherwise you could add an `Integer` through the `List<Object>` view. Use `List<?>` / `List<? extends Object>`.

Q: Does `super.clone()` call a constructor?
A: No. `Object.clone()` allocates a field-by-field copy without running any constructor (and throws `CloneNotSupportedException` unless the class implements `Cloneable`).

Q: Can a class be abstract without any abstract method?
A: Yes — it simply can't be instantiated. (The reverse isn't allowed: an abstract method forces the class to be abstract.)

Q: Inside `two.Derived extends one.Base`, does `new Base().display()` compile if `display()` is protected?
A: No. Outside the package, protected members are reachable only **through inheritance** — on `this` or references of type `Derived` (or its subtypes).

Q: `System.out.println(null);` — what does it print?
A: Nothing — it doesn't compile: "reference to println is ambiguous" (`println(char[])` vs `println(String)`).
:::

@sheet | Interview bank · Output questions

## 💻 OUTPUT QUESTIONS — predict first!

:::qa
Q: Reference juggling.

```java "▶ predict the output" run
public class Main {
    public static void main(String[] args) {
        Student a = new Student();
        a.name = "A";
        Student b = a;
        b.name = "B";
        a = new Student();
        a.name = "C";
        System.out.println(b.name + " " + a.name);
    }
}

class Student { String name; }
```

:::ans
```output
B C
```
`b = a` copies the arrow → "B" overwrites "A" in the shared object. Then `a` is re-pointed to a **new** object; `b` still holds the old one.
:::

Q: Static counter with ids.

```java "▶ predict the output" run
public class Main {
    static int count = 0;
    int id;

    Main() { count++; id = count; }

    public static void main(String[] args) {
        Main x = new Main(), y = new Main(), z = new Main();
        System.out.println(x.id + " " + y.id + " " + z.id
                           + " " + Main.count);
    }
}
```

:::ans
```output
1 2 3 3
```
`count` is shared and keeps growing; each object snapshots it into its **own** `id`.
:::

Q: Static blocks, instance blocks and constructors across inheritance.

```java "▶ predict the output" run
class A {
    static { System.out.print("SA "); }
    { System.out.print("IA "); }
    A() { System.out.print("CA "); }
}

class B extends A {
    static { System.out.print("SB "); }
    { System.out.print("IB "); }
    B() { System.out.print("CB "); }
}

public class Main {
    public static void main(String[] args) {
        new B();
        System.out.println("|");
        new B();
        System.out.println("|");
    }
}
```

:::ans
```output
SA SB IA CA IB CB |
IA CA IB CB |
```
Static parts run **once** (parent class first). For every object: parent's instance block + constructor, then the child's.
:::

Q: Overload resolution — widening vs boxing.

```java "▶ predict the output" run
public class Main {
    static void f(long x)    { System.out.println("long"); }
    static void f(Integer x) { System.out.println("Integer"); }
    static void f(Object x)  { System.out.println("Object"); }

    public static void main(String[] args) {
        f(5);
        f('a');
        f(Integer.valueOf(5));
        f("hi");
    }
}
```

:::ans
```output
long
long
Integer
Object
```
Widening (`int`/`char` → `long`) beats boxing. An `Integer` matches exactly. A `String` only fits `Object`.
:::

Q: Fields vs overridden methods.

```java "▶ predict the output" run
class Parent {
    String name = "Parent";
    String getName() { return name; }
}

class Child extends Parent {
    String name = "Child";
    @Override String getName() { return name; }
}

public class Main {
    public static void main(String[] args) {
        Parent p = new Child();
        System.out.println(p.name + " " + p.getName()
                           + " " + ((Child) p).name);
    }
}
```

:::ans
```output
Parent Child Child
```
Fields follow the **reference** type (no polymorphism); the overridden method follows the **object**; the cast changes the reference type to `Child`.
:::

:::

@sheet | Interview bank · Output questions (2)

:::qa

Q: An overridden method called from the parent's constructor.

```java "▶ predict the output" run
class Parent {
    Parent() { show(); }
    void show() { System.out.println("Parent show"); }
}

class Child extends Parent {
    int x = 5;
    @Override void show() { System.out.println("Child show " + x); }
}

public class Main {
    public static void main(String[] args) {
        new Child();
    }
}
```

:::ans
```output
Child show 0
```
Dynamic dispatch picks `Child.show()` — but `Parent()` runs **before** `Child`'s field initialisers, so `x` is still `0`.
:::

Q: Static hiding vs overriding.

```java "▶ predict the output" run
class A {
    static String who() { return "A"; }
    String me() { return "A"; }
}

class B extends A {
    static String who() { return "B"; }
    @Override String me() { return "B"; }
}

public class Main {
    public static void main(String[] args) {
        A obj = new B();
        System.out.println(obj.who() + obj.me() + B.who());
    }
}
```

:::ans
```output
ABB
```
`obj.who()` → static, reference type `A`. `obj.me()` → overridden, object `B`. `B.who()` → called on class `B`.
:::

Q: The string pool.

```java "▶ predict the output" run
public class Main {
    public static void main(String[] args) {
        String s1 = "java";
        String s2 = "ja" + "va";        // joined by the compiler
        String part = "ja";
        String s3 = part + "va";        // joined at runtime
        System.out.println((s1 == s2) + " " + (s1 == s3)
                           + " " + s1.equals(s3));
    }
}
```

:::ans
```output
true false true
```
Constant expressions are folded at compile time → same pooled object. Runtime concatenation creates a **new** String; `equals` still matches the characters.
:::

Q: The Integer cache.

```java "▶ predict the output" run
public class Main {
    public static void main(String[] args) {
        Integer a = 100, b = 100, c = 1000, d = 1000;
        System.out.println((a == b) + " " + (c == d) + " " + c.equals(d));
    }
}
```

:::ans
```output
true false true
```
Autoboxing reuses cached objects for −128…127; 1000 creates two separate objects. `equals` compares values.
:::

Q: `finally` vs the returned value.

```java "▶ predict the output" run
public class Main {
    static int test() {
        int x = 1;
        try {
            return x;
        } finally {
            x = 2;
            System.out.println("finally x=" + x);
        }
    }

    public static void main(String[] args) {
        System.out.println(test());
    }
}
```

:::ans
```output
finally x=2
1
```
`return x` saves the value **1** first; `finally` runs before the method actually leaves, but changing `x` can't alter the saved value.
:::

:::

@sheet | Interview bank · Output questions (3)

:::qa

Q: Which catch wins?

```java "▶ predict the output" run
public class Main {
    public static void main(String[] args) {
        try {
            int[] arr = new int[2];
            arr[2] = 5;
            System.out.println("A");
        } catch (ArithmeticException e) {
            System.out.println("B");
        } catch (RuntimeException e) {
            System.out.println("C");
        } finally {
            System.out.println("D");
        }
        System.out.println("E");
    }
}
```

:::ans
```output
C
D
E
```
`ArrayIndexOutOfBoundsException` skips "A", isn't an `ArithmeticException`, **is** a `RuntimeException` → "C". `finally` always → "D". Handled, so the program continues → "E".
:::

Q: Pass-by-value with an array.

```java "▶ predict the output" run
public class Main {
    static void change(int[] arr, int n) {
        arr[0] = 99;              // changes the SHARED array
        n = 99;                   // changes a local copy
        arr = new int[]{-1};      // re-points the local copy only
    }

    public static void main(String[] args) {
        int[] arr = {1, 2};
        int n = 1;
        change(arr, n);
        System.out.println(arr[0] + " " + n);
    }
}
```

:::ans
```output
99 1
```
The method received a **copy of the reference**: mutating through it is visible, re-pointing it isn't. `n` is a primitive copy.
:::

Q: Shallow clone.

```java "▶ predict the output" run
public class Main {
    static class Box implements Cloneable {
        int size = 1;
        int[] items = {1, 2};

        public Box clone() throws CloneNotSupportedException {
            return (Box) super.clone();
        }
    }

    public static void main(String[] args) throws Exception {
        Box a = new Box();
        Box b = a.clone();
        b.size = 5;
        b.items[0] = 9;
        System.out.println(a.size + " " + a.items[0] + " " + (a == b));
    }
}
```

:::ans
```output
1 9 false
```
Two different objects (`false`); the primitive `size` was copied; the `items` array is **shared** by the shallow copy.
:::

Q: `remove(int)` vs `remove(Object)`.

```java "▶ predict the output" run
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 2));
        Set<Integer> set = new HashSet<>(list);
        list.remove(1);
        list.remove(Integer.valueOf(2));
        System.out.println(list + " " + set.size());
    }
}
```

:::ans
```output
[1, 3] 3
```
`remove(1)` deletes **index** 1 → `[1, 3, 2]`; `remove(Integer.valueOf(2))` deletes the first value 2 → `[1, 3]`. The set dropped the duplicate: {1, 2, 3}.
:::

Q: When do enum constructors run?

```java "▶ predict the output" run
public class Main {
    enum Level {
        LOW, MEDIUM, HIGH;
        Level() { System.out.print(name().charAt(0)); }
    }

    public static void main(String[] args) {
        System.out.print("start ");
        Level l = Level.HIGH;
        System.out.println(" " + l.ordinal() + " "
                           + Level.LOW.compareTo(l));
    }
}
```

:::ans
```output
start LMH 2 -2
```
All constants are built at the enum's **first use**, in order (L, M, H). `HIGH` has ordinal 2; `compareTo` subtracts ordinals: 0 − 2 = −2.
:::
:::

@sheet | Interview bank · Conceptual

## 🧠 CONCEPTUAL

:::qa
Q: Why does Java forbid multiple inheritance of classes but allow many interfaces?
A: Two parent **classes** can bring conflicting code and duplicate state (the diamond problem) plus two constructor chains. Interfaces carry no state, and conflicting defaults must be resolved explicitly — so many interfaces are safe.

Q: Why is `main()` static?
A: At startup no object exists; `static` lets the JVM call `main` on the class itself without guessing how to construct one. (Java 25's launcher can also create the object for an instance `main`, but the classic answer stands.)

Q: Why aren't constructors inherited?
A: A constructor initialises **its own** class's part of the object. A parent's constructor knows nothing about the child's fields, so inheriting it would create half-initialised objects. Children reuse it explicitly through `super(...)`.

Q: Why is composition often preferred over inheritance?
A: HAS-A relationships can be swapped at runtime (`NiceCar.upgradeEngine()`), don't lock you into one parent, and don't break when a base class changes (the fragile base class problem). Use inheritance for true IS-A families.

Q: When would you choose an abstract class over an interface?
A: When related classes share **state and code** (fields, constructors, protected helpers) and form a genuine family. Choose an interface for a capability that unrelated classes can implement.

Q: Compile-time type vs runtime type — why does the difference matter?
A: The compile-time (reference) type decides **what you may call**; the runtime (object) type decides **which overridden method runs**. Every polymorphism question is really this sentence.

Q: Why keep fields private even if the getter and setter do nothing special?
A: Freedom to change later: add validation, make the field read-only, compute it, log changes — without touching any caller. Public fields freeze your design forever.

Q: How does a `HashMap` find a key?
A: `hashCode()` picks the bucket; `equals()` finds the exact key inside it. That's why the two must agree (Ch 04).

Q: Why are Strings immutable (and the class final)?
A: Safe sharing in the string pool, cacheable hash codes for map keys, thread safety, and security (file paths, class names can't be altered after checks). `final` stops subclasses from breaking those guarantees.

Q: What do generics solve that an `Object`-based container can't?
A: With `Object` the compiler can't stop wrong types going in, and every read needs a cast that may fail at runtime. Generics move those errors to compile time and remove the casts.

Q: Conceptually, why can't static methods be overridden?
A: Overriding means "decide at runtime from the object". A static method has no object — it's bound to the class at compile time — so there is nothing to dispatch on.

Q: When should you create a custom exception — checked or unchecked?
A: When a domain-specific failure deserves its own name (`InsufficientBalanceException`). Checked if the caller can reasonably recover and must be forced to think about it; unchecked for programming errors.

Q: Why is `Vector` considered legacy?
A: It predates the Collections Framework and synchronises every call — a cost most code doesn't need, and it still doesn't make compound actions safe. `ArrayList` + targeted concurrency tools are better.

Q: Why are enums better than `int` or `String` constants?
A: Type safety (only valid values compile), a namespace, usable in `switch`, can carry fields and methods, built-in `values()`/`valueOf()`, and `==` comparison is safe.

Q: How do the four pillars cooperate in one design — say, payments?
A: An interface `PaymentMethod` (**abstraction**) implemented by `Card`, `Upi`, `Wallet` (**inheritance** of type); `checkout(PaymentMethod p)` calls `p.pay()` (**polymorphism**); each class keeps balances and PINs private behind validated methods (**encapsulation**).
:::
