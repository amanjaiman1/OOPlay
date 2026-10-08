@sheet | Mini project 1

# ✦ PROJECT 1 · REPORT CARD SYSTEM ✦

<p class="center"><span class="chip must">Ch 01</span> <span class="chip high">Ch 02</span> <span class="chip good">Ch 03</span> classes · objects · constructors · <code>this</code> · static · encapsulation</p>

## 📝 Problem statement

A coaching institute keeps students' marks for 5 subjects in **three parallel arrays** (the exact pain from Ch 01) — and last week someone typed `140` as a mark. Build a small OOP system that stores students, **never accepts invalid data**, and prints report cards.

## ✅ Requirements

1. Every `Student` gets an automatic, **read-only** roll number 1, 2, 3 … (a static counter).
2. Two constructors — `Student(String name)` and `Student(String name, int[] marks)` — chained with `this(...)`.
3. `boolean setMarks(int subject, int value)` accepts only subject 0–4 and value 0–100.
4. `percentage()` and `grade()` → A ≥ 90 · B ≥ 75 · C ≥ 60 · D otherwise.
5. `toString()` returns one report-card line.
6. `static int totalStudents()`.
7. `ReportCardApp.main`: 3 students, 2 invalid updates (rejected), all cards, the topper.

## 🧩 Classes & relationships

```sketch
   ReportCardApp ──creates──→ Student  (many objects)
                    ├─ static int count       ← shared
                    ├─ final int rollNo       ← read-only
                    ├─ private String name
                    ├─ private int[] marks (5)
                    ├─ Student(name) ─this(...)─→ Student(name, marks)
                    ├─ boolean setMarks(...)  ← the ONLY way in
                    ├─ percentage() · grade()
                    └─ toString()
```

## ▶ Expected behaviour

```output "sample run"
✗ rejected: subject 2 → 140
✗ rejected: subject 7 → 50
Roll 1 | Aman  | 92.4% | A
Roll 2 | Riya  | 78.0% | B
Roll 3 | Kabir | 55.0% | D
Topper: Aman (92.4%) · students created: 3
```

## 🏗️ Starter structure

```java "Student.java — starter (compiles, logic is yours)"
public class Student {
    private static int count = 0;
    private final int rollNo;
    private final String name;
    private final int[] marks = new int[5];

    public Student(String name) {
        this(name, new int[5]);              // chaining is done for you
    }

    public Student(String name, int[] marks) {
        this.rollNo = ++count;
        this.name = name;
        // TODO: copy each mark through setMarks() so validation applies
    }

    public boolean setMarks(int subject, int value) {
        // TODO: reject a bad subject index or a value outside 0..100
        return false;
    }

    public double percentage() { return 0; }   // TODO
    public char grade()        { return 'D'; } // TODO
    public int getRollNo()     { return rollNo; }
    public static int totalStudents() { return count; }

    @Override
    public String toString() {
        return "";  // TODO: "Roll 1 | Aman  | 92.4% | A"
    }
}
```

:::sticky ⭐ Stretch goals
- implement `Comparable<Student>` and print a merit list (Ch 06)
- add a `Subject` **enum** instead of indexes 0–4 (Ch 07)
- prove `count` is shared: print `Student.totalStudents()` after each `new`
:::

@sheet | Mini project 2

# ✦ PROJECT 2 · RIDEX FARE ENGINE ✦

<p class="center"><span class="chip must">Ch 03</span> <span class="chip high">Ch 05</span> inheritance · polymorphism · abstraction · interfaces · overloading · overriding</p>

## 📝 Problem statement

RideX offers **Bikes, Autos and Cabs**. Every type prices a trip differently; electric vehicles get a green discount and cabs can be **shared** (fare split between riders). The booking screen must show the fare of **every** vehicle with **one loop** — and adding a new type tomorrow (say `EBike`) must not change that loop at all.

## ✅ Requirements

1. `abstract class Vehicle`: `regNo` (final), `driverName`, `baseFare`; `abstract double perKmRate()`; a **final** `fare(double km) = baseFare + km × perKmRate()`; an **overload** `fare(double km, double surge)`.
2. `Bike`, `Auto`, `Cab` extend `Vehicle`, override `perKmRate()` and `toString()`; `Cab` has `seats`.
3. `interface Electric` — constant `GREEN_DISCOUNT_PERCENT = 10`, `batteryLevel()`, `default double discounted(double fare)`.
4. `interface Shareable` — `maxRiders()`, `default double splitFare(double fare, int riders)`.
5. `EBike extends Bike implements Electric`; `Cab implements Shareable`.
6. `FareBoard.showFares(Vehicle[] fleet, double km)` uses polymorphism + `instanceof` patterns — it never names `Bike`, `Auto` or `Cab`.
7. `new Vehicle(...)` must be impossible; a vehicle's `regNo` can never change.

## 🧩 Classes & relationships

```sketch
                       abstract Vehicle
              regNo · driverName · baseFare
              perKmRate()            ← abstract
              fare(km) · fare(km, surge)
                 ┌───────────┼────────────┐
                 ↓           ↓            ↓
               Bike         Auto         Cab ─ ─ implements ─ ─→ Shareable
                 ↑
               EBike ─ ─ implements ─ ─→ Electric

   FareBoard ──uses──→ Vehicle[]   (knows ONLY the abstract type)
```

## ▶ Expected behaviour (10 km)

```output "sample run"
Bike   KA-01-1234 (Ravi)   ₹ 75.00
EBike  KA-01-5678 (Asha)   ₹ 67.50   green −10 %
Auto   KA-02-1111 (Manoj)  ₹ 145.00
Cab    KA-03-2222 (Sara)   ₹ 230.00  shared by 4 → ₹ 57.50 each
Surge ×1.5 on the Cab:     ₹ 345.00
```

## 🏗️ Starter structure

```java "Vehicle.java — starter"
public abstract class Vehicle {
    private final String regNo;
    protected final String driverName;
    protected final double baseFare;

    protected Vehicle(String regNo, String driverName, double baseFare) {
        this.regNo = regNo;
        this.driverName = driverName;
        this.baseFare = baseFare;
    }

    protected abstract double perKmRate();        // each type decides

    public final double fare(double km) {         // one formula for all
        return baseFare + km * perKmRate();
    }

    public double fare(double km, double surge) { // overload
        return 0;  // TODO
    }

    public String getRegNo() { return regNo; }
}

class Bike extends Vehicle {                      // worked example
    Bike(String regNo, String driver) { super(regNo, driver, 25); }
    @Override protected double perKmRate() { return 5; }
}

interface Electric {
    int GREEN_DISCOUNT_PERCENT = 10;
    int batteryLevel();
    default double discounted(double fare) {
        return fare;  // TODO: apply GREEN_DISCOUNT_PERCENT
    }
}

interface Shareable {
    int maxRiders();
    // TODO: default double splitFare(double fare, int riders)
}

// TODO: Auto (base 45, ₹10/km), Cab (base 80, ₹15/km, Shareable), EBike
```

```java "FareBoard.java — starter"
public class FareBoard {
    static void showFares(Vehicle[] fleet, double km) {
        for (Vehicle v : fleet) {
            double fare = v.fare(km);             // runtime polymorphism
            // TODO: v instanceof Electric e  → fare = e.discounted(fare)
            // TODO: v instanceof Shareable s → also print the split fare
            System.out.printf("%-6s %s  ₹ %.2f%n",
                    v.getClass().getSimpleName(), v.getRegNo(), fare);
        }
    }

    public static void main(String[] args) {
        Vehicle[] fleet = { new Bike("KA-01-1234", "Ravi") };  // TODO: more
        showFares(fleet, 10);
    }
}
```

:::sticky ⭐ Stretch goals
- add `EBike` **without editing** `showFares` — that's polymorphism paying rent
- sort the fleet by fare with a `Comparator` lambda (Ch 06)
- explain in one line why `fare(km)` is `final` but `perKmRate()` is `abstract`
:::

@sheet | Mini project 3

# ✦ PROJECT 3 · LIBRARY LITE ✦

<p class="center"><span class="chip must">Ch 06</span> <span class="chip high">Ch 07</span> generics · collections · exceptions · enums · lambdas · OOP design</p>

## 📝 Problem statement

A college library tracks **books** and **members**. Students may borrow at most **2** books, faculty **5**. Issued or lost books can't be issued again. The librarian wants search by genre, a title-sorted list, per-genre counts — and **clear messages instead of crashes**.

## ✅ Requirements

1. Enums: `Genre { FICTION, SCIENCE, HISTORY, TECH }`, `BookStatus { AVAILABLE, ISSUED, LOST }`, `MemberType { STUDENT(2), FACULTY(5) }` with a `maxBooks` field.
2. `interface Identifiable { String getId(); }`
3. `Book implements Identifiable` — id, title, author, genre, status; `equals`/`hashCode` on **id**; `toString`.
4. `Member implements Identifiable` — id, name, type, `List<Book> borrowed`.
5. Generic `Repository<T extends Identifiable>` backed by a `Map<String, T>`: `add(T)`, `T findById(String) throws NotFoundException`, `List<T> findAll(Predicate<T> filter)`.
6. Checked exceptions under one parent: `LibraryException` ← `NotFoundException`, `BookNotAvailableException`, `LimitExceededException`.
7. `Library.issue(memberId, bookId)` / `giveBack(...)` throw the right exception; `main` catches each one and prints its message — the program **never** crashes.
8. Reports: books of a genre (lambda filter), all books sorted by title (`Comparator`), count per genre (`EnumMap<Genre, Integer>`).

## 🧩 Classes & relationships

```sketch
             Identifiable (interface)
                ↑              ↑
              Book           Member ──has many──→ List<Book>
           Genre, BookStatus   MemberType (maxBooks)

   Repository<T extends Identifiable>     ← ONE generic class, Map inside
        used twice → Repository<Book>, Repository<Member>

   Library ──uses──→ both repositories
           ──throws─→ LibraryException
                        ├─ NotFoundException
                        ├─ BookNotAvailableException
                        └─ LimitExceededException
```

## ▶ Expected behaviour

```output "sample run"
Issued "Clean Code" to Aman
Issued "Sapiens" to Aman
✗ Aman (STUDENT) can borrow at most 2 books
✗ Book B9 not found
✗ "Clean Code" is ISSUED
Returned "Clean Code"
TECH books: [Clean Code, Effective Java]
Sorted: [A Brief History of Time, Clean Code, Effective Java, Sapiens]
Per genre: {FICTION=0, SCIENCE=1, HISTORY=1, TECH=2}
```

## 🏗️ Starter structure

```java "Library.java — starter (one file)"
import java.util.*;
import java.util.function.Predicate;

enum Genre { FICTION, SCIENCE, HISTORY, TECH }
enum BookStatus { AVAILABLE, ISSUED, LOST }

enum MemberType {
    STUDENT(2), FACULTY(5);
    private final int maxBooks;
    MemberType(int maxBooks) { this.maxBooks = maxBooks; }
    int maxBooks() { return maxBooks; }
}

interface Identifiable { String getId(); }

class LibraryException extends Exception {
    LibraryException(String msg) { super(msg); }
}
class NotFoundException extends LibraryException {
    NotFoundException(String msg) { super(msg); }
}
// TODO: BookNotAvailableException, LimitExceededException

class Repository<T extends Identifiable> {
    private final Map<String, T> items = new HashMap<>();

    void add(T item) { items.put(item.getId(), item); }

    T findById(String id) throws NotFoundException {
        T item = items.get(id);
        // TODO: throw new NotFoundException(...) when item is null
        return item;
    }

    List<T> findAll(Predicate<T> filter) {
        List<T> result = new ArrayList<>();
        // TODO: keep every value for which filter.test(value) is true
        return result;
    }
}

// TODO: class Book implements Identifiable   (equals + hashCode on id!)
// TODO: class Member implements Identifiable
// TODO: class Library { issue(...), giveBack(...), reports }
```

:::sticky ⭐ Stretch goals
- make `LOST` books reportable with `values()` and a `switch` on `BookStatus`
- replace the `HashMap` with a `TreeMap` — what changes in the output order, and why?
- write one JUnit-style test per exception (Ch 05: annotations like `@Test`)
:::

:::teach
1. Students read the problem and **list nouns** → classes, **verbs** → methods
2. Draw the relationship sketch before any code
3. Starter first: make it compile, then fill one TODO at a time
4. Demo the expected run; ask which chapter each line comes from
5. Review: "where is encapsulation? polymorphism? generics?"
:::
