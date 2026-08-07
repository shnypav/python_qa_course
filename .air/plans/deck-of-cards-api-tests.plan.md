# Add Deck of Cards API tests to hw_04_api_testing

## Context

`hw_04_api_testing` has 7 test modules covering Dog CEO, Open Brewery DB and JSONPlaceholder. Every one of them is a **stateless, single-request** test: fire one GET, assert the response. Nothing in the homework exercises a multi-step workflow where one call changes the state the next call observes.

Deck of Cards API (`https://deckofcardsapi.com/api/deck`) fills exactly that gap. It is free, needs no auth, and is genuinely stateful: creating a deck returns a `deck_id`, drawing decrements `remaining`, cards move into named piles, and reshuffling restores the deck. That makes it possible to write real sequential state-machine assertions while staying in the same plain-`requests` style as the rest of the directory.

All behaviors listed below were verified against the live API before writing this plan.

## Approach

Add **one new module**, `test_rest_08_deck_of_cards.py`, matching the structure of `test_rest_06_jsonplaceholder_extended.py` and `test_rest_07_openbrewery_extended.py`: module-level `BASE_URL`, `pytestmark = pytest.mark.usefixtures("log_test_case")`, plain `requests` calls, `cerberus` for schema validation, raw asserts.

No changes to `conftest.py`, no client wrapper, no `pytest.ini`, no new dependencies. Git history shows a client-abstraction + registered-markers version of hw_04 was added and later reverted — this plan deliberately does not re-tread that. The only new fixture is a module-local `deck_id` that creates a fresh shuffled deck, so tests never depend on each other's state.

## File changes

| File | Action | Responsibility |
|---|---|---|
| `hw_04_api_testing/test_rest_08_deck_of_cards.py` | **Create** | All Deck of Cards tests: deck creation variants, draw mechanics, card schema, stateful shuffle/pile workflows, negative cases |

Nothing else is touched. `requests` and `cerberus` are already in the root `requirements.txt`.

## Verified API behavior (basis for assertions)

| Request | Verified response |
|---|---|
| `GET /new/` | `success: true`, `remaining: 52`, `shuffled: false` |
| `GET /new/shuffle/` | `success: true`, `remaining: 52`, `shuffled: true` |
| `GET /new/shuffle/?deck_count=6` | `remaining: 312` |
| `GET /new/shuffle/?jokers_enabled=true` | `remaining: 54` |
| `GET /new/shuffle/?cards=AS,2S,KS,AD,2D,KD` | `remaining: 6` |
| `GET /{id}/draw/?count=N` | `len(cards) == N`, `remaining` drops by N |
| `GET /{id}/draw/` (no count) | 1 card, `remaining: 51` |
| `GET /{id}/draw/?count=60` on a 52-card deck | HTTP **200**, `success: false`, 52 cards returned, `remaining: 0` |
| Draw all 52 | 52 **distinct** `code` values |
| `GET /{id}/shuffle/` after drawing 10 | `remaining` back to 52 |
| `GET /{id}/shuffle/?remaining=true` after drawing 10 | `remaining` stays 42 |
| `GET /{id}/pile/hand/add/?cards=...` | `piles.hand.remaining == n`, deck `remaining` unchanged |
| `GET /{id}/pile/hand/list/` | `piles.hand.cards` holds the added cards |
| `GET /{id}/pile/hand/return/` | deck `remaining: 52`, `piles.hand.remaining: 0` |
| `GET /notarealdeck/draw/?count=1` | HTTP **404**, `success: false`, `error: "Deck ID does not exist."` |
| Card object shape | `code`, `image`, `images{svg,png}`, `value`, `suit` |

## Implementation steps

### Task 1 — Module scaffolding

Create `hw_04_api_testing/test_rest_08_deck_of_cards.py` with the same header as `test_rest_07_openbrewery_extended.py`:

```python
import pytest
import requests
from cerberus import Validator

pytestmark = pytest.mark.usefixtures("log_test_case")

BASE_URL = "https://deckofcardsapi.com/api/deck"
```

Add one function-scoped fixture returning a fresh shuffled single deck's id:

```python
@pytest.fixture
def deck_id():
    r = requests.get(f"{BASE_URL}/new/shuffle/", timeout=10)
    assert r.status_code == 200
    return r.json()["deck_id"]
```

Pass `timeout=10` on every call to match files 05–07 (the autouse `log_http_requests` fixture in `conftest.py:63` already injects a 15s default, so this is stylistic consistency, not a functional need).

### Task 2 — Deck creation

- `test_01_new_deck_is_not_shuffled` — `GET /new/`: `success is True`, `remaining == 52`, `shuffled is False`
- `test_02_new_shuffled_deck_is_shuffled` — `GET /new/shuffle/`: `shuffled is True`, `remaining == 52`
- `test_03_deck_count_sets_remaining` — parametrized `[(1, 52), (2, 104), (6, 312)]` with `ids=["single", "double", "six"]`
- `test_04_jokers_add_two_cards` — `?jokers_enabled=true` → `remaining == 54`
- `test_05_partial_deck_contains_only_requested_cards` — build a deck with `?cards=AS,2S,KS,AD,2D,KD`, assert `remaining == 6`, draw 6 and assert the drawn `code` set equals the requested set

### Task 3 — Draw mechanics and schema

- `test_06_draw_decrements_remaining` — parametrized `count` in `[1, 5, 10]`; `len(cards) == count` and `remaining == 52 - count`
- `test_07_card_schema` — cerberus `Validator(schema, require_all=True)` over a single drawn card; assert with `, v.errors` as in `test_rest_06_jsonplaceholder_extended.py:37`:

```python
schema = {
    "code": {"type": "string"},
    "image": {"type": "string"},
    "images": {
        "type": "dict",
        "schema": {"svg": {"type": "string"}, "png": {"type": "string"}},
    },
    "value": {"type": "string"},
    "suit": {"type": "string", "allowed": ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]},
}
```

- `test_08_drawn_cards_are_unique` — draw 52, assert `len(codes) == 52`, `len(set(codes)) == 52`, `remaining == 0`
- `test_09_draw_more_than_remaining_reports_failure` — draw 60 from a 52-card deck: HTTP 200, `success is False`, `len(cards) == 52`, `remaining == 0`

### Task 4 — Stateful workflows

- `test_10_full_shuffle_restores_deck` — draw 10 (`remaining == 42`) → `GET /{id}/shuffle/` → `remaining == 52`
- `test_11_shuffle_remaining_keeps_drawn_cards_out` — draw 10 → `GET /{id}/shuffle/?remaining=true` → `remaining == 42`
- `test_12_pile_add_and_list` — draw 4, join their codes, add to pile `hand`; assert `piles["hand"]["remaining"] == 4` and deck `remaining == 48`; then `GET /pile/hand/list/` and assert the listed codes match the drawn codes
- `test_13_pile_return_restores_deck` — after Task 12's setup, `GET /pile/hand/return/` → deck `remaining == 52`, `piles["hand"]["remaining"] == 0`

### Task 5 — Negative case

- `test_14_unknown_deck_returns_not_found` — `GET /notarealdeck/draw/?count=1`: HTTP 404, `success is False`, `"Deck ID does not exist." in result["error"]`

## Acceptance criteria

- `hw_04_api_testing/test_rest_08_deck_of_cards.py` exists and collects 14 test functions (20 test cases after parametrization: `test_03` ×3, `test_06` ×3).
- `pytest hw_04_api_testing/test_rest_08_deck_of_cards.py` exits 0 with network access.
- Every test asserts `r.status_code` before touching `r.json()`, matching the directory convention.
- No test depends on another test's deck; each obtains its own `deck_id`.
- No assertion depends on card *order* or on a shuffled deck differing from a sorted one — only on server-reported flags and counts.
- `conftest.py`, `requirements.txt` and all existing test modules are unmodified (`git diff --stat` shows exactly one new file).
- A timestamped log appears in the repo-root `logs/` directory containing `HTTP request started: GET https://deckofcardsapi.com/...` lines, confirming the existing `log_http_requests` fixture covers the new module.

## Verification

```bash
# new module only, verbose
pytest hw_04_api_testing/test_rest_08_deck_of_cards.py -v

# confirm no regression in the directory
pytest hw_04_api_testing -v

# confirm the existing logging fixture picked up the new calls
ls -t logs/hw_04_api_testing_*.log | head -1 | xargs grep -c deckofcardsapi
```

Expected: 20 passed for the new module; the existing suites behave as before (they hit third-party APIs, so treat network errors as environmental, per `AGENTS.md`); the grep returns a non-zero count.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| `deckofcardsapi.com` is a hobby-scale service and can be slow or briefly down | The autouse `log_http_requests` fixture already sets a 15s timeout and logs failures with full context; per `AGENTS.md`, network failures are environmental, not product failures |
| Over-draw returns HTTP **200** with `success: false`, not an error status — easy to assert wrongly | Verified against the live API; `test_09` asserts `status_code == 200` **and** `success is False` |
| `/{id}/return/` (deck-level) behaves differently from `/{id}/pile/{name}/return/` — the deck-level form left pile cards in place during probing | Use only the pile-scoped `/pile/hand/return/`, whose behavior is confirmed deterministic |
| Asserting that a shuffled deck's order differs from a known order would flake | No test asserts card order; `test_02` asserts the server's `shuffled` boolean instead |
| Each `deck_id` fixture call creates server-side state | Decks are ephemeral and expire on the provider's side; no cleanup endpoint exists and none is needed |