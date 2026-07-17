# Antarctic Agents

A three-round multi-agent simulation using `smolagents`.

## Agents

- Four penguins decide whether to forage, fish, or request food.
- One scientist reviews penguin state and distribution history.
- The scientist allocates limited food and a shared fishing tool.

## Tool added for the exercise

```python
@tool
def find_food(penguin_name: str, method: str) -> int:
    ...
```

It returns:

- fishing: 2–7 food;
- foraging: 0–3 food.

The tool is registered in every `PenguinAgent`:

```python
tools=[find_food]
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

## Run without a token

The default mode is deterministic and free:

```bash
python starter.py
```

## Run with Hugging Face

Edit `.env`:

```env
USE_REAL_MODEL=true
HF_API_TOKEN=hf_your_read_token
HF_MODEL_ID=HuggingFaceH4/zephyr-7b-beta
```

Then run:

```bash
python starter.py
```

The current `smolagents` API uses `InferenceClientModel`, the successor to
the older `HfApiModel` name used by the initial scaffold.

Model availability can change between Hugging Face inference providers. If
the selected model is unavailable, choose another instruction model
supported by your account or return to stub mode.

## Test

```bash
pytest -q
```

Tests run in stub mode and verify:

- valid `find_food` ranges;
- the three-round simulation;
- increasing penguin food totals;
- distribution-history updates;
- use of the shared scientist tool.
