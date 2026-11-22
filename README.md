# System Design 101

Learn system design step by step, from scratch. Every page explains one idea, with a picture where it helps and real code behind it.

## How to use

1. Start with **Foundations**: what happens when you open a website.
2. Then follow the **Project**: we build a food-delivery app (like Foodpanda) one service at a time. Each step links to the concepts it uses.
3. Look up any term in [CONTEXT.md](CONTEXT.md).

## Contents

| Section | What's inside |
|---|---|
| [Foundations](docs/00-foundations/) | How a request travels from your laptop to a server *(coming next)* |
| [Concepts](docs/concepts/) | One page per concept, reused across the project |
| [Project](project/foodpanda/) | The food-delivery build log and services |
| [Examples](examples/) | Small runnable snippets: locks, design patterns, SOLID |

## Run the examples

```bash
python3 examples/concurrency/locks/01_mutex.py   # any single example
python3 -m pytest examples scripts                # all examples + checks
```

For AI tools: [llms.txt](llms.txt) lists every page.
