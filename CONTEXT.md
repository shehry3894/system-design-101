# System Design 101: glossary

One short definition per term. Each term links to the page or example that teaches it. When two words mean the same thing, we use one and list the other under _Avoid_.

## Concurrency

**Mutex**: A lock only one thread can hold at a time. [Example](examples/concurrency/locks/01_mutex.py)
_Avoid_: Lock (when you mean this specific kind)

**RLock**: A mutex the holding thread may acquire again without blocking itself. [Example](examples/concurrency/locks/02_rlock.py)
_Avoid_: Recursive lock

**Semaphore**: A counter of free slots, so at most N threads can enter. [Example](examples/concurrency/locks/03_semaphore.py)

**Event**: A flag that threads wait on until another thread sets it. [Example](examples/concurrency/locks/05_event.py)

**Condition**: A lock plus "wait until something is true", woken by notify. [Example](examples/concurrency/locks/06_condition.py)

**Barrier**: A meeting point where N threads wait until all have arrived. [Example](examples/concurrency/locks/07_barrier.py)

**GIL**: The CPython lock that lets only one thread run Python code at a time. [Example](examples/concurrency/locks/08_gil.py)

## Design patterns

**Singleton**: A class with exactly one instance. [Example](examples/patterns/creational/01_singleton.py)

**Factory Method**: A method that subclasses override to choose which object to create. [Example](examples/patterns/creational/02_factory_method.py)
_Avoid_: Factory (too vague; a "simple factory" is a different thing)

**Abstract Factory**: An object that creates a matching family of objects. [Example](examples/patterns/creational/03_abstract_factory.py)

**Builder**: An object that assembles a complex object step by step. [Example](examples/patterns/creational/04_builder.py)

**Prototype**: An object you copy to make new similar objects. [Example](examples/patterns/creational/05_prototype.py)

## Principles

**SOLID**: Five class-design principles: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion. [Examples](examples/principles/solid/)

**Dependency injection**: Passing a dependency in from outside instead of creating it inside. [Example](examples/principles/solid/d_dependency_inversion.py)
