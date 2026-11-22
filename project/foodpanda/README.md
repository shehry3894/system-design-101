# Project: Foodpanda-style food delivery

We build it one service at a time. Each step lists the concepts it teaches.

| Step | Service | Status | Concepts |
|---|---|---|---|
| 1 | [auth_service](services/auth_service/) | Exists. Simplified, and its 6 tests pass. Known gaps below will move to `GAPS.md` (separate task, waiting on the owner). | JWT (JSON Web Token), password hashing, REST (Representational State Transfer), HS256 vs RS256, dependency injection *(pages come in M2)* |

## Known gaps in auth_service (fix in step 1)

- Anyone can register as `admin`: `/register` accepts any role.
- `Dockerfile` uses Python 3.11 while `pyproject.toml` needs 3.12+.
- Inside the container, uvicorn listens on `127.0.0.1`, so port 8001 is unreachable from the host.
- `passlib` and `python-jose` are barely maintained. FastAPI's docs now use `pwdlib` and `PyJWT`. `bcrypt` is pinned below 5 until then, because passlib 1.7.4 crashes on it.
- No schema migrations: `create_all()` never alters existing tables (Alembic planned).
- `pip/` duplicates the setup with pip instead of uv. Keep one.
- The tests need a running Postgres and share one user across tests, so they depend on run order.
