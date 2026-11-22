# Examples

Small, runnable snippets. Each file starts with **what it is**, **when to use it**, and a **source**. Each ends with an `assert` that proves the point.

Run one: `python3 examples/concurrency/locks/01_mutex.py`. Run all: `python3 -m pytest examples`.

## Concurrency: locks (Python `threading`)

| File | One line |
|---|---|
| [01_mutex.py](concurrency/locks/01_mutex.py) | One thread at a time |
| [02_rlock.py](concurrency/locks/02_rlock.py) | The same thread may lock again |
| [03_semaphore.py](concurrency/locks/03_semaphore.py) | At most N threads at a time |
| [04_bounded_semaphore.py](concurrency/locks/04_bounded_semaphore.py) | A semaphore that catches extra releases |
| [05_event.py](concurrency/locks/05_event.py) | Wait for one signal |
| [06_condition.py](concurrency/locks/06_condition.py) | Wait until data is ready (producer/consumer) |
| [07_barrier.py](concurrency/locks/07_barrier.py) | Everyone waits until all arrive |
| [08_gil.py](concurrency/locks/08_gil.py) | Why threads don't speed up CPU work in Python |

## Design patterns: creational

| File | One line |
|---|---|
| [01_singleton.py](patterns/creational/01_singleton.py) | Exactly one instance |
| [02_factory_method.py](patterns/creational/02_factory_method.py) | Subclasses pick which object to create |
| [03_abstract_factory.py](patterns/creational/03_abstract_factory.py) | Create a matching family of objects |
| [04_builder.py](patterns/creational/04_builder.py) | Build a complex object step by step |
| [05_prototype.py](patterns/creational/05_prototype.py) | Copy a ready-made object |

## Principles: SOLID

| File | One line |
|---|---|
| [s_single_responsibility.py](principles/solid/s_single_responsibility.py) | One reason to change |
| [o_open_closed.py](principles/solid/o_open_closed.py) | Add new code, don't edit old code |
| [l_liskov_substitution.py](principles/solid/l_liskov_substitution.py) | A subclass must work wherever its parent works |
| [i_interface_segregation.py](principles/solid/i_interface_segregation.py) | Small interfaces, no unused methods |
| [d_dependency_inversion.py](principles/solid/d_dependency_inversion.py) | Depend on interfaces, inject the concrete thing |
