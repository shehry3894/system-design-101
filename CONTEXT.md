# System Design 101: glossary

One short definition per term. Each term links to the page or example that teaches it. When two words mean the same thing, we use one and list the other under _Avoid_.

## Concurrency

**Mutex**: A lock only one thread can hold at a time. [Example](examples/concurrency/lock_mutex.py)
_Avoid_: Lock (when you mean this specific kind)

**RLock**: A mutex the holding thread may acquire again without blocking itself. [Example](examples/concurrency/lock_rlock.py)
_Avoid_: Recursive lock

**Semaphore**: A counter of free slots, so at most N threads can enter. [Example](examples/concurrency/limit_semaphore.py)

**Event**: A flag that threads wait on until another thread sets it. [Example](examples/concurrency/wait_event.py)

**Condition**: A lock plus "wait until something is true", woken by notify. [Example](examples/concurrency/wait_condition.py)

**Barrier**: A meeting point where N threads wait until all have arrived. [Example](examples/concurrency/wait_barrier.py)

**GIL** (Global Interpreter Lock): The CPython lock that lets only one thread run Python code at a time. [Example](examples/concurrency/gil.py)

## Design patterns

**Singleton**: A class with exactly one instance. [Example](examples/patterns/creational_singleton.py)

**Factory Method**: A method that subclasses override to choose which object to create. [Example](examples/patterns/creational_factory_method.py)
_Avoid_: Factory (too vague; a "simple factory" is a different thing)

**Abstract Factory**: An object that creates a matching family of objects. [Example](examples/patterns/creational_abstract_factory.py)

**Builder**: An object that assembles a complex object step by step. [Example](examples/patterns/creational_builder.py)

**Prototype**: An object you copy to make new similar objects. [Example](examples/patterns/creational_prototype.py)

## Principles

**SOLID**: Five class-design principles: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion. [Examples](examples/principles/solid/)

**Dependency injection**: Passing a dependency in from outside instead of creating it inside. [Example](examples/principles/solid/d_dependency_inversion.py)

## How a request travels

Taught in [How a request travels](docs/00-foundations/01-how-a-request-travels.md). Sources: [research note](docs/research/how-a-request-travels.md).

**IP address** (Internet Protocol address): A number that says where a host is on the network.

**Private address**: An address from 10/8, 172.16/12 or 192.168/16. It is only unique inside one network.

**NAT** (Network Address Translation): The router maps private addresses to its own public one.
_Avoid_: NAPT, Network Address Port Translation (when the difference doesn't matter)

**DNS** (Domain Name System): The system that turns a domain name into an IP address.

**Domain name**: A list of labels, like `google` + `com`.

**Registrar**: The company you buy a domain name from. It sits between you and the registry.

**Registry**: The operator that runs a top-level domain such as `.com`.

**Resolver**: A program that asks DNS servers to turn a name into an address. The *stub* resolver in your OS asks a *recursive* resolver, which does the real work.

**TTL** (time to live): How many seconds a DNS answer may be cached.

**TCP** (Transmission Control Protocol): Gives a reliable, in-order byte stream over IP.

**Port**: A number that picks the application on a host, e.g. 443 for HTTPS (HTTP over TLS).

**TLS** (Transport Layer Security): Encrypts and authenticates the connection.

**HTTP request** (Hypertext Transfer Protocol): A method (like `GET`) plus a target, headers and an optional body.

**Gateway**: A server in front of the real servers that forwards requests to them. Load balancing is one of its jobs.
_Avoid_: Reverse proxy (same thing; we say gateway)
