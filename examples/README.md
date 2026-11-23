# Examples

Small, runnable snippets. Each file starts with **what it is**, **when to use it** and a **source**. Each ends with an `assert` that proves the point.

Run one: `python3 examples/concurrency/lock_mutex.py`. Run all: `python3 -m pytest examples`.

## Concurrency (Python `threading`)

The file prefix tells you the question the tool answers.

| Prefix | Question |
|---|---|
| `lock_` | Only **one** thread at a time? |
| `limit_` | At most **N** threads at a time? |
| `wait_` | Wait for **another thread** first? |

| File | One line |
|---|---|
| [lock_mutex.py](concurrency/lock_mutex.py) | One thread at a time |
| [lock_rlock.py](concurrency/lock_rlock.py) | The same thread may lock again |
| [limit_semaphore.py](concurrency/limit_semaphore.py) | At most N threads at a time |
| [limit_bounded_semaphore.py](concurrency/limit_bounded_semaphore.py) | Same, but an extra release raises an error |
| [wait_event.py](concurrency/wait_event.py) | Wait for one signal |
| [wait_condition.py](concurrency/wait_condition.py) | Wait until data is ready (producer/consumer) |
| [wait_barrier.py](concurrency/wait_barrier.py) | Everyone waits until all arrive |
| [gil.py](concurrency/gil.py) | Why threads don't speed up CPU work in Python |

## Design patterns

The prefix is the GoF group: `creational_` (how objects are created). `structural_` and `behavioral_` come later.

| File | One line |
|---|---|
| [creational_singleton.py](patterns/creational_singleton.py) | Exactly one instance |
| [creational_factory_method.py](patterns/creational_factory_method.py) | Subclasses pick which object to create |
| [creational_abstract_factory.py](patterns/creational_abstract_factory.py) | Create a matching family of objects |
| [creational_builder.py](patterns/creational_builder.py) | Build a complex object step by step |
| [creational_prototype.py](patterns/creational_prototype.py) | Copy a ready-made object |

## Principles: SOLID

The prefix is the SOLID letter.

| File | One line |
|---|---|
| [s_single_responsibility.py](principles/solid/s_single_responsibility.py) | One reason to change |
| [o_open_closed.py](principles/solid/o_open_closed.py) | Add new code, don't edit old code |
| [l_liskov_substitution.py](principles/solid/l_liskov_substitution.py) | A subclass must work wherever its parent works |
| [i_interface_segregation.py](principles/solid/i_interface_segregation.py) | Small interfaces, no unused methods |
| [d_dependency_inversion.py](principles/solid/d_dependency_inversion.py) | Depend on interfaces, inject the concrete thing |

## Communication

The prefix is the communication style: `request_` (the caller waits for the answer). `push_` and `messaging_` come later. See [Communication styles](../CONTEXT.md#communication-styles).

| File | One line |
|---|---|
| [request_payload_size.py](communication/request_payload_size.py) | The same order as JSON (143 bytes) and as Protobuf (40 bytes) |
| [request_encode_speed.py](communication/request_encode_speed.py) | Encode/decode time for the same order, JSON vs Protobuf (needs `pip install protobuf`) |
