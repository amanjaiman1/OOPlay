@sheet | Ch 06 · Custom ArrayList

@chapter 06 | GENERICS • LAMBDAS • EXCEPTIONS • CLONING | custom ArrayList · generics · bounds & wildcards · Comparable/Comparator · lambdas · try/catch/finally · throw/throws · checked/unchecked · shallow & deep copy | 🎬 OOP 6

# ✦ BUILD YOUR OWN ArrayList ✦

## ❓ WHY? — the problem

Arrays are **fixed size**. `int[] a = new int[3];` then a 4th item → ✗ `ArrayIndexOutOfBoundsException`. We want a list that just… grows.

```sketch
   Fixed array        int[] a = new int[3];   a[3] = 9  ✗ out of bounds
        ↓
   Capacity problem   ┌───┬───┬───┐
        ↓             │ 1 │ 2 │ 3 │  full!
   Resize             └───┴───┴───┘
        ↓             make a new array, 2× the size
   Copy old items     ┌───┬───┬───┬───┬───┬───┐
        ↓             │ 1 │ 2 │ 3 │ 4 │   │   │  ← then add 4
   Custom ArrayList   └───┴───┴───┴───┴───┴───┘
                      add() hides all this → the list feels "infinite"
```

## 💻 EXAMPLE (compact version)

```java "CustomArrayList.java" run
import java.util.Arrays;

public class CustomArrayList {
    private int[] data = new int[10];   // DEFAULT_SIZE = 10
    private int size = 0;               // item count AND next free index

    public void add(int num) {
        if (size == data.length) resize();   // full? grow first
        data[size++] = num;
    }

    private void resize() {             // private → hidden detail
        int[] temp = new int[data.length * 2];
        for (int i = 0; i < data.length; i++) {
            temp[i] = data[i];          // copy old items
        }
        data = temp;                    // old array → garbage
    }

    public int remove()       { return data[--size]; }   // last item
    public int get(int index) { return data[index]; }
    public int size()         { return size; }

    @Override
    public String toString() {
        return Arrays.toString(Arrays.copyOf(data, size))
               + " size=" + size + " capacity=" + data.length;
    }

    public static void main(String[] args) {
        CustomArrayList list = new CustomArrayList();
        for (int i = 0; i < 14; i++) list.add(2 * i);
        System.out.println(list);
    }
}
```

```output
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26] size=14 capacity=20
```

:::connect
`resize()` is **private** → the user sees only `add/get/remove/size` = **abstraction + encapsulation** (Ch 03) in a real class. The real `java.util.ArrayList` does the same, growing by ~1.5×.
:::

## ⚠️ The new problem

It stores **only `int`**. Strings? Students? Write `StringArrayList`, `StudentArrayList` … ✗ copy-paste. Use `Object[]`? Then *anything* goes in and you cast everything coming out ✗. We need **one** class that works for any type **and** stays type-safe → **generics**.

@sheet | Ch 06 · Generics

# ✦ GENERICS ✦

## ❓ WHY? — the problem first

```java "raw ArrayList — no type checking" run
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList list = new ArrayList();   // raw type: holds Object
        list.add(10);
        list.add("Hello");                  // the compiler can't stop this
        for (Object o : list) {
            Integer n = (Integer) o;        // boom for "Hello" — at RUNTIME
            System.out.println(n * 2);
        }
    }
}
```

```err "💥 runtime"
20
Exception in thread "main" java.lang.ClassCastException: class java.lang.String cannot be cast to class java.lang.Integer
```

```java "with generics"
ArrayList<Integer> list = new ArrayList<>();  // <> "diamond": inferred
list.add(10);
list.add("Hello");      // ✗ COMPILE error — caught before the program runs
int n = list.get(0);    // ✓ no cast needed
```

## 🌍 IN REAL LIFE

A **labelled storage box**: "ONLY BOOKS". Nobody can drop a sandwich in it, and whatever you take out is surely a book.

```sketch
   BEFORE (raw)                     AFTER (generic)
   ┌──────────────┐                 ┌──────────────┐
   │ Box          │ ← anything,     │ Box<Integer> │ ← only Integer,
   │ 10 "hi" 3.5  │   surprise at   │ 10  20  30   │   checked at
   └──────────────┘   RUNTIME ✗     └──────────────┘   COMPILE time ✓

   Generics → type safety → fewer runtime type errors → less casting
```

:::define
**Generics** let a class, interface or method take a [[b:type parameter]] (`<T>`). [[u:The compiler fills in the real type at each use and checks it.]]
Common names: `T` type · `E` element · `K` key · `V` value · `N` number.
:::

## 💻 EXAMPLE — our list, now generic

```java "CustomGenArrayList.java" run
import java.util.Arrays;

public class CustomGenArrayList<T> {          // T = type parameter
    private Object[] data = new Object[10];   // new T[10] ✗ (see below)
    private int size = 0;

    public void add(T item) {
        if (size == data.length) {
            data = Arrays.copyOf(data, data.length * 2);
        }
        data[size++] = item;
    }

    @SuppressWarnings("unchecked")
    public T get(int index) { return (T) data[index]; }  // only Ts go in

    public int size() { return size; }

    public static void main(String[] args) {
        CustomGenArrayList<String> names = new CustomGenArrayList<>();
        names.add("Kunal");
        names.add("Rahul");
        // names.add(42);                ✗ compile error
        String first = names.get(0);     // no cast at the call site
        System.out.println(first + " " + names.size());
    }
}
```

```output
Kunal 2
```

:::reality
**Type erasure:** [[r:generics exist only for the compiler]]. At runtime `T` is erased to `Object` (or its bound), so `new T[10]` ("generic array creation"), `new T()` and `instanceof T` are impossible. Hence `Object[]` + a cast inside the class.
:::

:::trap
Generics work with **objects only**: `List<int>` ✗ ("unexpected type") → `List<Integer>` + autoboxing (Ch 01 wrappers).
:::

## ✍️ Generic methods & interfaces

```java
static <T> void printAll(T[] items) {        // <T> before the return type
    for (T item : items) System.out.print(item + " ");
}

interface GenericInterface<T> { void display(T value); }
class Main implements GenericInterface<Integer> {
    public void display(Integer value) { System.out.println(value); }
}
```

@sheet | Ch 06 · Bounds & wildcards

# ✦ BOUNDS & WILDCARDS ✦

## 🧠 Bounded type parameter — `<T extends Number>`

```java "WildcardExample"
public class WildcardExample<T extends Number> { // T: Number or subclass
    // inside, T has Number's methods: item.doubleValue(), item.intValue()
}

WildcardExample<Integer> a;   // ✓
WildcardExample<Double>  b;   // ✓
WildcardExample<String>  c;   // ✗ String is not a Number
```

```sketch
                  Object
                    ↑
                  Number          ← <T extends Number> allows Number
             ┌──────┼───────┐       and everything below it
          Integer  Double  Long
```

## 🎯 The big surprise

```java "List<Integer> is NOT a List<Number>" nocompile
import java.util.*;

class Test {
    void f() {
        List<Number> nums = new ArrayList<Integer>();
    }
}
```

```err "💥 compile error"
error: incompatible types: ArrayList<Integer> cannot be converted to List<Number>
```

**Why?** If it were allowed, `nums.add(3.14)` would push a `Double` into a list of `Integer`s. Wildcards are the safe way to say "a list of *some* kind of Number":

| syntax | means | read items as | can add? |
|---|---|---|---|
| `List<?>` | list of some unknown type | `Object` | ✗ (only `null`) |
| `List<? extends Number>` | Number or any **sub**type | `Number` | ✗ (only `null`) |
| `List<? super Integer>` | Integer or any **super**type | `Object` | ✓ `Integer`s |

```java "Main.java" run
import java.util.List;

public class Main {
    // accepts List<Integer>, List<Double>, List<Number> …
    static double sum(List<? extends Number> list) {
        double total = 0;
        for (Number n : list) total += n.doubleValue();
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sum(List.of(1, 2, 3)));
        System.out.println(sum(List.of(1.5, 2.5)));
    }
}
```

```output
6.0
4.0
```

:::reality
@@good Memory trick **PECS** — *Producer `extends`, Consumer `super`*: a list you only **read** from → `? extends T`; a list you only **put** into → `? super T`.
:::

@sheet | Ch 06 · Comparing objects

# ✦ COMPARING OBJECTS ✦

## ❓ WHY?

`Arrays.sort(intArray)` is obvious. `Arrays.sort(students)` — by marks? roll no? name? Java can't guess. Two ways to tell it:

- **`Comparable`** — the class defines its own *natural* order (`compareTo`)
- **`Comparator`** — an outside rule you pass in (`compare`), as many as you like

`compareTo` / `compare` return **negative** (this first) · **0** (equal) · **positive** (other first).

```java "Main.java" run
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Student[] list = {
            new Student(12, 89.76f), new Student(5, 99.52f),
            new Student(2, 95.52f),  new Student(13, 77.52f)
        };
        Arrays.sort(list);              // natural order → compareTo (marks)
        System.out.println(Arrays.toString(list));

        // a Comparator as a lambda → roll-number order
        Arrays.sort(list, (a, b) -> Integer.compare(a.rollno, b.rollno));
        System.out.println(Arrays.toString(list));
    }
}

class Student implements Comparable<Student> {
    int rollno;
    float marks;

    Student(int rollno, float marks) {
        this.rollno = rollno;
        this.marks = marks;
    }

    @Override
    public int compareTo(Student o) {
        return Float.compare(this.marks, o.marks);   // <0 · 0 · >0
    }

    @Override
    public String toString() { return rollno + ":" + marks; }
}
```

```output
[13:77.52, 12:89.76, 2:95.52, 5:99.52]
[2:95.52, 5:99.52, 12:89.76, 13:77.52]
```

## 💻 The same Comparator — anonymous class → lambda

```java
Arrays.sort(list, new Comparator<Student>() {      // anonymous inner class
    @Override
    public int compare(Student o1, Student o2) {
        return -(int) (o1.marks - o2.marks);       // descending
    }
});

// the same Comparator, written as a lambda:
Arrays.sort(list, (o1, o2) -> -(int) (o1.marks - o2.marks));
```

:::trap
`(int) (o1.marks - o2.marks)` **truncates**: 99.52 − 99.1 = 0.42 → `(int)` → **0** → "equal" → wrong order! Use `Float.compare(o2.marks, o1.marks)` (descending) — never subtract-and-cast floats.
:::

@sheet vs | Comparison · Comparable vs Comparator

# ✦ COMPARABLE [[vs]] COMPARATOR ✦

| | `Comparable<T>` | `Comparator<T>` |
|---|---|---|
| Package | `java.lang` | `java.util` |
| Method | `int compareTo(T other)` | `int compare(T a, T b)` |
| Lives | **inside** the class | **outside** — separate class or lambda |
| Orders per class | one *natural* order | unlimited |
| Must edit the class? | ✓ yes | ✗ no — works for classes you can't touch |
| Used by | `Arrays.sort(arr)`, `Collections.sort(list)`, `TreeSet` | `Arrays.sort(arr, cmp)`, `list.sort(cmp)` |
| JDK examples | `String` (A→Z), `Integer` (1→9) | `Comparator.reverseOrder()`, `String.CASE_INSENSITIVE_ORDER` |

```sketch
   Comparable  =  "I know how to compare MYSELF"   (built into Student)
   Comparator  =  "a JUDGE from outside"   (byMarks, byRollNo, byName …)
```

:::mistake
Sorting an array of objects that implement **neither** → compiles, then crashes at runtime: `ClassCastException: Student cannot be cast to class java.lang.Comparable`.
:::

@sheet | Ch 06 · Lambda expressions

# ✦ LAMBDA EXPRESSIONS ✦

## 🧠 IDEA

A lambda is a **method without a name** that you can store in a variable and pass around — *behaviour as data*.

```sketch
   (parameters)  ->  expression              (a, b) -> a + b

   (parameters)  ->  {                       (a, b) -> {
                       statements;               int r = a - b;
                       return value;             return r;
                     }                         }
```

:::define
A lambda implements a [[b:functional interface]] — an interface with **exactly one abstract method**: `Runnable`, `Comparator<T>`, `Consumer<T>`, `Function<T, R>`, `Predicate<T>`, or your own. `@FunctionalInterface` makes the compiler check the "exactly one" rule.
:::

## 💻 EXAMPLE — LambdaFunctions

```java "LambdaFunctions.java" run
import java.util.ArrayList;
import java.util.function.Consumer;

public class LambdaFunctions {
    public static void main(String[] args) {
        ArrayList<Integer> arr = new ArrayList<>();
        for (int i = 0; i < 5; i++) arr.add(i + 1);

        Consumer<Integer> fun = item -> System.out.print(item * 2 + ",");
        arr.forEach(fun);                       // pass behaviour IN
        System.out.println();

        Operation sum  = (a, b) -> a + b;
        Operation prod = (a, b) -> a * b;
        Operation sub  = (a, b) -> {            // block body
            int result = a - b;
            return result;
        };

        LambdaFunctions calc = new LambdaFunctions();
        System.out.println(calc.operate(5, 3, sum));
        System.out.println(calc.operate(5, 3, prod));
        System.out.println(calc.operate(5, 3, sub));
    }

    private int operate(int a, int b, Operation op) {
        return op.operation(a, b);
    }
}

@FunctionalInterface
interface Operation {
    int operation(int a, int b);      // exactly ONE abstract method
}
```

```output
2,4,6,8,10,
8
15
2
```

## ❓ WHY are lambdas useful?

- 1 line instead of a 5-line anonymous class (compare the Comparator page)
- pass **behaviour** into methods: `forEach`, `sort`, `removeIf`, streams
- one `operate()` method, unlimited operations → the calculator never changes

:::trap
Local variables used inside a lambda must be **final or effectively final**: `int x = 1; x++; Runnable r = () -> System.out.println(x);` ✗ "local variables referenced from a lambda expression must be final or effectively final".
:::

@sheet | Ch 06 · Exception handling

# ✦ EXCEPTION HANDLING ✦

## 🧠 IDEA

An **exception** is an unexpected event at runtime that breaks the normal flow — divide by zero, a `null`, a missing file. Handle it, and the program survives.

```sketch
   NORMAL FLOW
   ─────────→─────────→─────────→───────── done ✓

   WITH AN EXCEPTION
   ─────────→──────── ✗ ArithmeticException (b == 0)
                       │
                       ↓  jump to a matching catch
                 handle safely
                ↙            ↘
           catch              finally
      (report / recover)   (ALWAYS runs: cleanup)
```

:::aside
`catch` = plan B<br>`finally` = lock the car, always
:::

## 🌍 IN REAL LIFE

Driving to college (normal flow) → a tyre bursts (exception). Unhandled → the journey ends (crash). Handled → put on the spare (`catch`) — and whatever happens, lock the car at the end (`finally`).

```sketch "the family tree"
                        Throwable
              ┌─────────────┴──────────────┐
              ↓                            ↓
            Error                      Exception
   JVM-level trouble — don't       ┌───────┴──────────────┐
   catch: OutOfMemoryError,        ↓                      ↓
   StackOverflowError       RuntimeException         IOException,
                            = UNCHECKED              SQLException,
                            ArithmeticException,     MyException …
                            NullPointerException,    = CHECKED
                            ArrayIndexOutOfBounds…
```

## 💻 EXAMPLE

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        try {
            String name = "Kunal";
            if (name.equals("Kunal")) {
                throw new MyException("name is kunal");   // raise it NOW
            }
        } catch (MyException e) {
            System.out.println(e.getMessage());
        } catch (ArithmeticException e) {
            System.out.println(e.getMessage());
        } catch (Exception e) {                  // most general → LAST
            System.out.println("normal exception");
        } finally {
            System.out.println("this will always execute");
        }

        try {
            divide(5, 0);
        } catch (ArithmeticException e) {
            System.out.println(e.getMessage());
        }
    }

    static int divide(int a, int b) throws ArithmeticException {
        if (b == 0) {
            throw new ArithmeticException("please do not divide by zero");
        }
        return a / b;
    }
}

class MyException extends Exception {       // a CHECKED custom exception
    public MyException(String message) {
        super(message);                          // message → getMessage()
    }
}
```

```output
name is kunal
this will always execute
please do not divide by zero
```

:::rule
- catch [[r:specific → general]]; reversed → ✗ "exception ArithmeticException has already been caught"
- `finally` runs whether or not an exception happened — even after `return` (only `System.exit()` or a JVM crash skips it)
- a `try` needs at least one `catch` **or** a `finally`
- one catch for several types: `catch (IOException | SQLException e)`
:::

:::reality
For files/connections use **try-with-resources** — `try (var in = new FileReader("a.txt")) { … }` closes the resource automatically, even on exceptions. That's the modern replacement for `finalize()` (Ch 01).
:::

@sheet vs | Comparison · throw vs throws

# ✦ `throw` [[vs]] `throws` ✦

| | `throw` | `throws` |
|---|---|---|
| What | a **statement** that raises an exception right now | a **declaration** warning callers it *might* happen |
| Where | inside a method body | in the method signature |
| Followed by | **one object**: `throw new X("msg")` | exception **class names**, comma-separated |
| How many | one at a time | several: `throws IOException, SQLException` |
| Analogy | actually throwing the ball ⚾ | the sign "beware: balls may fly" |

```java
// throws = the warning label on the signature
static int divide(int a, int b) throws ArithmeticException {
    if (b == 0) throw new ArithmeticException("no / by 0");  // throw = act
    return a / b;
}
```

## 🧠 Exception propagation

Not caught where it's thrown? It travels **down the call stack** until someone catches it — or the JVM prints a stack trace and stops.

```java "Main.java" run
public class Main {
    public static void main(String[] args) {
        try {
            a();
        } catch (ArithmeticException e) {
            System.out.println("caught in main: " + e.getMessage());
        }
        System.out.println("program continues");
    }

    static void a() { b(); System.out.println("a() end"); }   // skipped!
    static void b() { System.out.println(10 / 0); }           // thrown here
}
```

```output
caught in main: / by zero
program continues
```

```sketch
   CALL STACK  (top = latest)
   ┌──────────────┐
   │ b()      ✗   │ ← thrown here, no catch → b() ends
   ├──────────────┤        ↓
   │ a()          │ ← no catch → a() ends ("a() end" never prints)
   ├──────────────┤        ↓
   │ main()   ✓   │ ← catch found → handled, program goes on
   └──────────────┘
```

@sheet vs | Comparison · Checked vs Unchecked

# ✦ CHECKED [[vs]] UNCHECKED ✦

| | CHECKED | UNCHECKED |
|---|---|---|
| Extends | `Exception` (but not `RuntimeException`) | `RuntimeException` (or `Error`) |
| Compiler forces handling? | ✓ catch it **or** declare `throws` | ✗ no |
| Usual cause | the outside world: files, network, DB | bugs in *our* code: null, bad index, ÷0 |
| Examples | `IOException`, `FileNotFoundException`, `SQLException`, `CloneNotSupportedException`, `InterruptedException` | `ArithmeticException`, `NullPointerException`, `ArrayIndexOutOfBoundsException`, `ClassCastException`, `NumberFormatException` |
| Ignore it → | ✗ compile error | compiles; crashes *if* it happens |

```java "MyException not handled" nocompile
class MyException extends Exception {
    MyException(String m) { super(m); }
}

class Demo {
    void f() {
        throw new MyException("oops");     // neither caught nor declared
    }
}
```

```err "💥 compile error"
error: unreported exception MyException; must be caught or declared to be thrown
```

## ✍️ Custom exceptions — pick the parent

```java
class MyException extends Exception { … }                    // checked
class InvalidMarksException extends RuntimeException { … }    // unchecked
```

:::trap
"Checked exceptions happen at compile time" ✗ — **all** exceptions happen at runtime. *Checked* only means the **compiler checks** that you handled or declared them.
:::

@sheet | Ch 06 · Object cloning

# ✦ OBJECT CLONING ✦

## ❓ WHY?

We want a **twin**: a separate object with the same data, so changing the twin doesn't touch the original.

## ① Reference copy — NOT a copy at all

```java
Human kunal = new Human(34, "Kunal Kushwaha");
Human twin = kunal;              // copies the ARROW only (Ch 01!)
```

```sketch
   kunal ──────┐
               ↓
          ┌───────────────────────┐
          │ Human  age = 34 …     │     ONE object
          └───────────────────────┘
               ↑
   twin  ──────┘          twin.age = 50  →  kunal.age is 50 too ✗
```

## ② Shallow copy — `super.clone()`

New object ✓, every field copied **as-is**: primitives by value, references by **arrow** → nested objects are [[r:shared]].

```sketch
   kunal ──→ ┌──────────────┐
             │ age = 34     │
             │ arr  ●───────┼──┐
             └──────────────┘  │     ┌───┬───┬───┬───┬───┬───┐
                               ├───→ │ 3 │ 4 │ 5 │ 6 │ 9 │ 1 │  ONE array
   twin  ──→ ┌──────────────┐  │     └───┴───┴───┴───┴───┴───┘  shared ✗
             │ age = 34     │  │
             │ arr  ●───────┼──┘     twin.arr[0] = 100 → kunal sees 100
             └──────────────┘
```

## ③ Deep copy — clone **and** copy what's inside

```sketch
   kunal ──→ ┌──────────────┐     ┌───┬───┬───┬───┬───┬───┐
             │ age = 34     │     │ 3 │ 4 │ 5 │ 6 │ 9 │ 1 │
             │ arr  ●───────┼───→ └───┴───┴───┴───┴───┴───┘
             └──────────────┘
   twin  ──→ ┌──────────────┐     ┌───┬───┬───┬───┬───┬───┐
             │ age = 34     │     │100│ 4 │ 5 │ 6 │ 9 │ 1 │  own array ✓
             │ arr  ●───────┼───→ └───┴───┴───┴───┴───┴───┘
             └──────────────┘
```

## 💻 EXAMPLE — deep copy

```java "Main.java" run hl=23-25
import java.util.Arrays;

public class Main {
    public static void main(String[] args)
            throws CloneNotSupportedException {
        Human kunal = new Human(34, "Kunal Kushwaha");
        Human twin = (Human) kunal.clone();
        twin.arr[0] = 100;
        System.out.println(Arrays.toString(twin.arr));
        System.out.println(Arrays.toString(kunal.arr));   // untouched ✓
    }
}

class Human implements Cloneable {      // marker interface: "clone allowed"
    int age;
    String name;
    int[] arr = {3, 4, 5, 6, 9, 1};

    Human(int age, String name) { this.age = age; this.name = name; }

    @Override
    public Object clone() throws CloneNotSupportedException {
        Human twin = (Human) super.clone();   // shallow: fields as-is
        twin.arr = new int[this.arr.length];  // deep: twin's OWN array
        for (int i = 0; i < arr.length; i++) twin.arr[i] = this.arr[i];
        return twin;
    }
}
```

```output
[100, 4, 5, 6, 9, 1]
[3, 4, 5, 6, 9, 1]
```

Keep only `return super.clone();` → **both** lines print `[100, 4, 5, 6, 9, 1]`.

:::rule
- the class must `implements Cloneable` (a **marker** interface — no methods) or `super.clone()` throws `CloneNotSupportedException`
- `Object.clone()` is `protected` → override it as `public` to call it from outside
- `super.clone()` builds the copy **without running any constructor**
:::

:::reality
Many Java experts avoid `Cloneable` (awkward design: checked exception, casts, shallow by default). A **copy constructor** — `new Human(kunal)` — is often clearer. Sharing a `String` field is fine: strings are immutable.
:::

@sheet vs | Comparison · Shallow vs Deep copy

# ✦ SHALLOW COPY [[vs]] DEEP COPY ✦

| | REFERENCE COPY | SHALLOW COPY | DEEP COPY |
|---|---|---|---|
| Code | `b = a;` | `super.clone()` | clone + copy nested objects |
| New object? | ✗ | ✓ | ✓ |
| Primitive fields | same object, so shared | copied | copied |
| Nested objects / arrays | shared | ✗ **shared** | ✓ copied |
| `b.arr[0] = 100` changes `a`? | ✓ yes | ✓ **yes** | ✗ no |
| Cost | free | cheap | more time & memory |

```sketch
   REFERENCE        SHALLOW                DEEP
   a ─┐             a → [obj] ─┐           a → [obj] → [arr]
      ↓                        ↓
     [obj]          b → [obj] ─┴→ [arr]    b → [obj] → [arr]
      ↑
   b ─┘             2 objects, 1 array     2 objects, 2 arrays ✓
```

:::trap
"`clone()` gives an independent copy" ✗ — by default it's **shallow**. Every mutable field (arrays, lists, other objects) must be copied by hand for a deep copy.
:::

## ⭐ CHAPTER 06 — REMEMBER

:::remember
- custom ArrayList = array + `size` + private `resize()` (double + copy)
- generics = compile-time type safety, no casts; objects only; erased at runtime
- `<T extends Number>` bounds T · `List<Integer>` is not a `List<Number>` · use wildcards
- `Comparable` = natural order inside · `Comparator` = outside rules, often lambdas
- lambda implements a functional interface (exactly one abstract method)
- catch specific → general · `finally` always runs · `throw` acts, `throws` warns
- checked = compiler forces handling · shallow clone shares nested objects
:::

:::practice 🧪 PRACTICE — CHAPTER 06
### 🧪 QUICK CHECK
1. Why can't you write `new T[10]` inside a generic class?
2. `List<Number> nums = new ArrayList<Integer>();` — does it compile? Why (not)?
3. A method contains `try { return 1; } finally { System.out.println("F"); }`. You print its result — what appears?

### 💻 CODE PRACTICE
1. Generic `Pair<K, V>` with getters, plus `static <T extends Comparable<T>> T max(T a, T b)`. Test with `Integer`s and `String`s.
2. A checked `InvalidMarksException`; `Student.setMarks()` throws it outside 0–100; `main` catches and prints the message. Then make it unchecked — what changes in the code?

### 🎯 INTERVIEW THINKING
A `Document` with a `List<String> lines` implements `Cloneable` and simply `return super.clone();`. The app's "undo" keeps a clone before each edit. Why does undo mysteriously stop working?

:::ans ☑ Answers
1. Type erasure — at runtime T is unknown, so the JVM can't create a `T[]`; use `Object[]` + cast. 2. ✗ — otherwise a `Double` could be added to a list of `Integer`s; use `List<? extends Number>`. 3. `F` then `1` — `finally` runs before the method actually returns.
**Interview:** shallow copy — the "backup" and the live document **share the same `lines` list**, so every edit changes the backup too. Deep-copy the list: `copy.lines = new ArrayList<>(lines);`.
:::
:::

:::teach
1. Build the int ArrayList — then ask: "now store Strings?"
2. Labelled box → generics; show the compile error for a wrong type
3. Sort students: `Comparable`, then a `Comparator` lambda
4. Lambda = "a nameless method you can pass around"
5. Tyre-burst story → run `divide(5, 0)` with and without `try`
6. Cloning: draw the shared array, change it live
:::

:::connect 🔗 NEXT →
We built **one** list by hand. Java ships a whole family — lists, sets, queues, maps — under one design. And for values that may only be one of a fixed set (days, sizes, states)? → **Collections & enums** (Chapter 07).
:::
