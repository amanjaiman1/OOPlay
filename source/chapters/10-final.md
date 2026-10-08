@sheet | Master map

# ✦ THE MASTER MAP ✦

One page, the whole playlist. Cover the right side with your hand and explain each box aloud — if you can, you're ready.

```sketch xs
                                       «JAVA OOP»
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ↓                                 ↓                                 ↓
 «CLASSES / OBJECTS»                «CONSTRUCTORS»                       «STATIC»
  blueprint → instance            same name, no return             one copy per class
  reference ≠ object · new        default · this(...)              static block · main()
         │                                 │                       packages · singleton
         └─────────────────────────────────┼─────────────────────────────────┘
                                           ↓
                                     «INHERITANCE» ───→  every class → Object
                              extends · IS-A · super(...)        toString · equals
                              one parent · ctors not inherited   hashCode · getClass
                                           ↓
                                    «POLYMORPHISM»
                              ┌────────────┴─────────────┐
                              ↓                          ↓
                        ‹Overloading›               ‹Overriding›
                    compile time · params      runtime · same signature
                                           ↓
                                    «ENCAPSULATION»───→  private < default
                              private data + checked methods      < protected < public
                                           ↓
                                     «ABSTRACTION»
                              ┌────────────┴─────────────┐
                              ↓                          ↓
                      ‹Abstract Class›              ‹Interface›
                   state · ctor · 1 parent    contract · many · default/static
                                           ↓
                                       «GENERICS»
                              <T> · type safety · wildcards · erasure
                                           ↓
                                      «EXCEPTIONS»
                        try/catch/finally · throw vs throws · checked/unchecked
                                           ↓
                                        «CLONING»
                                reference → shallow → deep copy
                                           ↓
                                     «COLLECTIONS»
                           List · Set · Queue  |  Map (separate) · Vector
                                           ↓
                                        «ENUMS»
                         fixed constants · private ctor · values() · valueOf()
```

:::idea
Read it top-down as a story: **make objects** → **share & organise** them → **reuse** them (inheritance) → **vary** them (polymorphism) → **protect** them (encapsulation) → **simplify** them (abstraction) → make them **type-safe** (generics), **robust** (exceptions), **copyable** (cloning), **groupable** (collections) and **restricted to valid values** (enums).
:::

@sheet cheat | One-page cheat sheet

# ✦ ONE-PAGE CHEAT SHEET ✦

:::cols
:::col
## 🔑 Keywords

| keyword | meaning |
|---|---|
| `class` | defines a blueprint |
| `new` | creates an object, returns its reference |
| `this` | current object · `this(...)` same-class ctor |
| `super` | parent part · `super(...)` parent ctor |
| `static` | belongs to the class, one copy |
| `final` | assign once · no override · no extend |
| `extends` | inherit one class · an interface extends interfaces |
| `implements` | sign one or more interface contracts |
| `abstract` | no instance (class) · no body (method) |
| `interface` | pure contract type |
| `try` | guard risky code |
| `catch` | handle a matching exception |
| `finally` | always runs → cleanup |
| `throw` | raise one exception object now |
| `throws` | declare possible exceptions in the signature |
:::
:::col
## 🏛️ The 4 pillars

| pillar | in one line | Java tool |
|---|---|---|
| Inheritance | reuse a parent, IS-A | `extends`, `super` |
| Polymorphism | one call, many behaviours | overloading · overriding |
| Encapsulation | data + methods + controlled access | `private` + getters/setters |
| Abstraction | show what, hide how | abstract class · interface |

## ⚖️ Comparisons in one line

| pair | the difference |
|---|---|
| Class vs Object | blueprint vs instance in the heap |
| Reference vs Object | the arrow vs the thing it points to |
| Static vs Non-static | one shared copy vs one per object |
| Overloading vs Overriding | new params, compile time vs same signature, runtime |
| Encapsulation vs Abstraction | protect the data vs hide the complexity |
| Abstract class vs Interface | state + ctor + 1 parent vs contract + many |
| `==` vs `equals()` | same object vs same content |
| Shallow vs Deep copy | nested objects shared vs copied |
| `throw` vs `throws` | raise it now vs warn in the signature |
| Collection vs Map | single elements vs key → value pairs |

:::
:::

## ⭐ 20 golden Java rules

:::twocol
1. A reference is not the object — `b = a` copies only the arrow.
2. Java is always pass-by-value; for objects, the reference is copied.
3. Write any constructor and the free default one disappears.
4. `this(...)`/`super(...)` come first; `super()` is added if you write neither.
5. Constructors are never inherited — so never overridden.
6. Static = one copy per class; a static context has no `this`.
7. Static methods are hidden, not overridden; fields are never polymorphic.
8. Reference type → what you may call; object type → which override runs.
9. Overloading needs different parameters — return type alone isn't enough.
10. Overriding keeps the signature and can't reduce access.
11. `final` freezes the variable, not the object it points to.
12. One parent class, many interfaces.
13. Interface fields are `public static final`; its methods are `public`.
14. Abstract classes can't be instantiated but do have constructors.
15. `protected` outside the package works only through inheritance.
16. Override `equals()` → override `hashCode()` with the same fields.
17. Compare objects with `.equals()`; `==` checks identity.
18. Generics are invariant and object-only: `List<Integer>` ≠ `List<Number>`, `List<int>` ✗.
19. Catch specific → general; `finally` always runs (never `return` from it).
20. `Map` is not a `Collection`; enums can't extend or be extended.
:::

<p class="center small" style="margin-top:10px;color:#6b6e7c">✦ end of notebook ✦ &nbsp; revise the traps (#1–#36), redo the 15 output questions, build one mini project ✦</p>
