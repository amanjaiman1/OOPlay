@sheet cover

<div class="cover-title"><span class="s">✦</span> JAVA OOP <span class="s">✦</span></div>
<div class="cover-under"></div>
<div class="cover-sub">my handwritten notebook · from <em>class</em> to <em>enum</em></div>

<div class="label">
<div class="row"><span class="k">Name</span><span class="v">_____________________________</span></div>
<div class="row"><span class="k">Subject</span><span class="v">Object Oriented Programming in Java</span></div>
<div class="row"><span class="k">Lectures</span><span class="v">Kunal Kushwaha · Java OOP playlist · OOP 1 → OOP 7</span></div>
<div class="row"><span class="k">Code</span><span class="v">github.com/kunal-kushwaha/DSA-Bootcamp-Java › lectures/17-oop</span></div>
<div class="row"><span class="k">Roll No.</span><span class="v">________ &nbsp;&nbsp; Section: ____</span></div>
</div>

```sketch
      Class  ───→  Blueprint             ┌──────────────────────────┐
        │                                │  REMEMBER                │
        ↓  new                           │  class  = plan on paper  │
      Object ───→  Real Thing            │  object = thing in heap  │
                                         └──────────────────────────┘
```

## ✍️ How to read these notes

<div class="legend">
<div><span class="hl-r">red highlight</span> → critical Java rule</div>
<div><mark>yellow highlight</mark> → important concept</div>
<div><span class="hl-g">green highlight</span> → syntax / code pattern</div>
<div><span class="hl-b">blue highlight</span> → definition / term</div>
<div>★ must remember &nbsp; ✓ correct &nbsp; ✗ wrong</div>
<div>≠ different &nbsp; <b>?</b> common confusion</div>
<div>🧠 mental model &nbsp; 💡 intuition</div>
<div>⚠️ mistake &nbsp; 🎯 interview trap &nbsp; ☕ Java reality</div>
</div>

<p class="center" style="margin-top:14px"><span class="chip must">🔴 MUST KNOW</span> <span class="chip high">🟠 HIGHLY IMPORTANT</span> <span class="chip good">🟡 GOOD TO KNOW</span></p>

<p class="center small" style="color:#6b6e7c">Every page follows the same loop → WHY? → real life → concept → Java → code → visualise → mistake → trap → practice → revise.<br>On screen, answers are folded under “☑ Answers” — try first, then open.</p>

@sheet index

# ✦ INDEX ✦

@index

@sheet | The story of this notebook

# ✦ THE STORY OF OOP ✦

Every new idea in this notebook exists because the previous idea hit a wall. Read this page first, and come back to it whenever a chapter feels disconnected.

```sketch "problem  →  the concept that fixes it" sm
    THE PROBLEM WE HIT                         THE CONCEPT THAT FIXES IT
    ──────────────────                         ─────────────────────────
    1 student's data is spread over 3 arrays ─→  CLASS     (make your own type)
    a class is only a plan, no real student  ─→  OBJECT    (+ new, references)
    every object starts empty, set 1 by 1    ─→  CONSTRUCTOR
    field and parameter have the same name   ─→  this
    some data belongs to ALL objects         ─→  static
    two classes called Greeting collide      ─→  PACKAGES
    same code copy-pasted into many classes  ─→  INHERITANCE
    one call should behave differently       ─→  POLYMORPHISM
    anyone can write  marks = -50            ─→  ENCAPSULATION
    user drowns in internal details          ─→  ABSTRACTION
    "every child MUST define career()"       ─→  ABSTRACT CLASS
    a class needs MANY parents' contracts    ─→  INTERFACE
    our ArrayList only stores int            ─→  GENERICS
    one bad input crashes the whole program  ─→  EXCEPTIONS
    b = a copies only the arrow              ─→  CLONING
    arrays are fixed size, no ready tools    ─→  COLLECTIONS
    "day" could be any random String         ─→  ENUMS
```

```sketch "the learning path"
   Class → Object → Constructor → this → static → Packages
                                                     │
     ┌───────────────────────────────────────────────┘
     ↓
   Inheritance → Polymorphism → Encapsulation → Abstraction
                                                     │
     ┌───────────────────────────────────────────────┘
     ↓
   Abstract class → Interface → Generics → Lambdas → Exceptions
                                                     │
     ┌───────────────────────────────────────────────┘
     ↓
   Cloning → Collections → Enums  ★ done
```

| Chapter | Lecture | What it covers |
|---|---|---|
| 01 | OOP 1 | classes, objects, references, `new`, constructors, `this`, wrappers, `final`, garbage collection |
| 02 | OOP 2 | packages, `import`, `static`, static blocks, `main()`, inner classes, singleton, `System.out.println` internals |
| 03 | OOP 3 | inheritance, `super`, polymorphism, overloading, overriding, encapsulation, abstraction |
| 04 | OOP 4 | access modifiers, built-in packages, the `Object` class, `equals`/`hashCode`, `instanceof` |
| 05 | OOP 5 | abstract classes, interfaces, default/static methods, nested interfaces, annotations |
| 06 | OOP 6 | custom ArrayList, generics, wildcards, Comparable/Comparator, lambdas, exceptions, cloning |
| 07 | OOP 7 | collections framework, `Vector` & synchronization, enums |
| ★ | — | interview bank (85 Q), 3 mini projects, master map, one-page cheat sheet |
