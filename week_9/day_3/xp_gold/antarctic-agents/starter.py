"""Antarctic Agents: a tiny multi-agent simulation with smolagents.

The simulation contains:
- four PenguinAgent instances;
- one ScientistAgent;
- a shared resource-distribution history;
- a `find_food` tool registered on every penguin;
- three rounds of message-driven decisions.

Two model modes are available:

1. Stub mode, enabled by default:
   deterministic, free, offline, and suitable for testing.

2. Hugging Face mode:
   uses `InferenceClientModel` and requires a read token.

Run:
    python starter.py
"""

from __future__ import annotations

import json
import os
import random
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict

from dotenv import load_dotenv
from smolagents import (
    InferenceClientModel,
    Model,
    Tool,
    ToolCallingAgent,
    tool,
)
from smolagents.models import (
    ChatMessage,
    ChatMessageToolCall,
    ChatMessageToolCallFunction,
    MessageRole,
)

load_dotenv()


# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------

def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable safely."""

    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    return raw_value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


USE_REAL_MODEL = env_bool("USE_REAL_MODEL", False)
HF_MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "HuggingFaceH4/zephyr-7b-beta",
).strip()
SIMULATION_SEED = int(
    os.getenv("SIMULATION_SEED", "42")
)

# One dedicated random generator makes the run reproducible when the seed
# remains unchanged while still producing random-looking food yields.
RNG = random.Random(SIMULATION_SEED)


# -------------------------------------------------------------------------
# Shared state
# -------------------------------------------------------------------------

DISTRIBUTION_HISTORY: dict[str, list[dict[str, Any]]] = {}


def reset_simulation_state(seed: int = SIMULATION_SEED) -> None:
    """Clear global history and reset the pseudo-random generator."""

    DISTRIBUTION_HISTORY.clear()
    RNG.seed(seed)


@tool
def check_history(
    penguin_name: str,
) -> Dict[str, Any]:
    """Check recent scientist distributions for one penguin.

    Args:
        penguin_name: Name of the penguin whose history should be checked.

    Returns:
        A dictionary with food received in the three latest distributions
        and whether the scientist has ever granted a tool.
    """

    history = DISTRIBUTION_HISTORY.get(
        penguin_name,
        [],
    )

    recent_food = sum(
        record["food"]
        for record in history[-3:]
    )

    has_tool = any(
        record["has_tool"]
        for record in history
    )

    return {
        "recent_food": recent_food,
        "has_tool": has_tool,
    }


@tool
def record_distribution(
    penguin_name: str,
    food: int,
    has_tool: bool,
) -> str:
    """Record resources distributed by the scientist.

    Args:
        penguin_name: Name of the penguin receiving resources.
        food: Number of food units granted by the scientist.
        has_tool: Whether the scientist granted a tool on this turn.

    Returns:
        A short confirmation message.
    """

    DISTRIBUTION_HISTORY.setdefault(
        penguin_name,
        [],
    ).append({
        "food": int(food),
        "has_tool": bool(has_tool),
    })

    tool_phrase = (
        "a tool"
        if has_tool
        else "no tool"
    )

    return (
        f"Recorded: {penguin_name} got "
        f"{food} food and {tool_phrase}"
    )


@tool
def find_food(
    penguin_name: str,
    method: str,
) -> int:
    """Find a small random quantity of food.

    Fishing is more productive but should normally be chosen only when the
    penguin owns a tool. Any method other than fishing is normalized to
    foraging.

    Args:
        penguin_name: Name of the penguin looking for food.
        method: Search method, normally "fishing" or "foraging".

    Returns:
        Food units found: 2–7 for fishing and 0–3 for foraging.
    """

    normalized_method = method.strip().lower()

    if normalized_method == "fishing":
        food_found = RNG.randint(2, 7)
    else:
        normalized_method = "foraging"
        food_found = RNG.randint(0, 3)

    print(
        f"🐟 {penguin_name} used {normalized_method} "
        f"and found {food_found} food."
    )

    return food_found


# -------------------------------------------------------------------------
# JSON helpers
# -------------------------------------------------------------------------

def extract_json_object(value: Any) -> dict[str, Any]:
    """Extract one JSON object from an agent response.

    Real language models sometimes surround JSON with prose or Markdown.
    This helper first attempts a direct parse, then extracts the widest
    object enclosed by braces.
    """

    if isinstance(value, dict):
        return value

    text = str(value).strip()

    # Some smolagents outputs may include a final_answer label.
    if "final_answer:" in text:
        text = text.split("final_answer:")[-1].strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end <= start:
            raise ValueError(
                f"No JSON object was found in: {text!r}"
            )

        parsed = json.loads(
            text[start : end + 1]
        )

    if not isinstance(parsed, dict):
        raise ValueError(
            "The agent response must be a JSON object."
        )

    return parsed


def make_tool_call(
    name: str,
    arguments: dict[str, Any],
    call_id: str,
) -> ChatMessage:
    """Create one structured tool call for ToolCallingAgent."""

    return ChatMessage(
        role=MessageRole.ASSISTANT,
        content="",
        tool_calls=[
            ChatMessageToolCall(
                function=(
                    ChatMessageToolCallFunction(
                        name=name,
                        arguments=arguments,
                    )
                ),
                id=call_id,
                type="function",
            )
        ],
    )


def content_to_text(content: Any) -> str:
    """Flatten smolagents message content into text."""

    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        pieces = []

        for block in content:
            if isinstance(block, dict):
                pieces.append(
                    str(block.get("text", ""))
                )
            else:
                pieces.append(str(block))

        return "\n".join(pieces)

    return str(content)


def latest_user_task(
    messages: list[ChatMessage],
) -> str:
    """Return the latest user task from model history."""

    for message in reversed(messages):
        if message.role == MessageRole.USER:
            return re.sub(
                r"^New task:\s*",
                "",
                content_to_text(
                    message.content
                ).strip(),
                flags=re.IGNORECASE,
            )

    return ""


# -------------------------------------------------------------------------
# Key-free deterministic model
# -------------------------------------------------------------------------

class DeterministicSimulationModel(Model):
    """A transparent model that emits valid simulation JSON.

    The class follows the current smolagents Model interface. It is not a
    language model; it deterministically converts prompts into decisions so
    the multi-agent architecture can be executed without a token.
    """

    def __init__(self) -> None:
        super().__init__(
            model_id="antarctic-deterministic-stub"
        )

    @staticmethod
    def _integer(
        pattern: str,
        text: str,
        default: int = 0,
    ) -> int:
        """Extract the first integer matching a regular expression."""

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        return int(match.group(1)) if match else default

    @staticmethod
    def _boolean(
        pattern: str,
        text: str,
        default: bool = False,
    ) -> bool:
        """Extract a true/false value matching a regular expression."""

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return default

        return match.group(1).lower() == "true"

    def _penguin_decision(
        self,
        task: str,
    ) -> dict[str, Any]:
        """Choose request_food or find_food from penguin state."""

        food = self._integer(
            r"Current food:\s*(\d+)",
            task,
        )
        round_number = self._integer(
            r"Round:\s*(\d+)",
            task,
            default=1,
        )
        has_tool = self._boolean(
            r"Has tool:\s*(true|false)",
            task,
        )

        name_match = re.search(
            r"You are (Penguin\d+)",
            task,
            flags=re.IGNORECASE,
        )
        name = (
            name_match.group(1)
            if name_match
            else "Penguin0"
        )
        penguin_index = self._integer(
            r"Penguin(\d+)",
            name,
        )

        # Very low-food penguins may request assistance. The alternating
        # rule creates a mix of requests and self-found food.
        should_request = (
            food <= 1
            and (round_number + penguin_index) % 3 == 1
        )

        if should_request:
            return {
                "action": "request_food",
                "method": "none",
            }

        return {
            "action": "find_food",
            "method": (
                "fishing"
                if has_tool
                else "foraging"
            ),
        }

    def _scientist_decision(
        self,
        task: str,
    ) -> dict[str, Any]:
        """Allocate limited food and occasionally grant the tool."""

        food = self._integer(
            r"Penguin food:\s*(\d+)",
            task,
        )
        recent_food = self._integer(
            r"Recent distributed food:\s*(\d+)",
            task,
        )
        supply = self._integer(
            r"Scientist food supply:\s*(\d+)",
            task,
        )
        has_tool = self._boolean(
            r"Penguin has tool:\s*(true|false)",
            task,
        )
        tool_available = self._boolean(
            r"Scientist tool available:\s*(true|false)",
            task,
        )
        requested_food = (
            "request_food" in task
        )

        if supply <= 0:
            give_food = 0
        elif requested_food and food <= 2:
            give_food = min(4, supply)
        elif food < 4 and recent_food < 5:
            give_food = min(2, supply)
        else:
            give_food = 0

        give_tool = (
            tool_available
            and not has_tool
            and food <= 4
        )

        return {
            "give_food": give_food,
            "give_tool": give_tool,
        }

    def generate(
        self,
        messages: list[ChatMessage],
        stop_sequences: list[str] | None = None,
        response_format: dict[str, str] | None = None,
        tools_to_call_from: list[Tool] | None = None,
        **kwargs: Any,
    ) -> ChatMessage:
        """Emit a `final_answer` tool call containing valid JSON."""

        del (
            stop_sequences,
            response_format,
            tools_to_call_from,
            kwargs,
        )

        task = latest_user_task(messages)

        if "SCIENTIST_DECISION" in task:
            decision = self._scientist_decision(
                task
            )
            call_id = "scientist-decision"
        else:
            decision = self._penguin_decision(
                task
            )
            call_id = "penguin-decision"

        return make_tool_call(
            name="final_answer",
            arguments={
                "answer": json.dumps(decision)
            },
            call_id=call_id,
        )


def build_model() -> Model:
    """Create the configured Hugging Face or deterministic model."""

    if not USE_REAL_MODEL:
        return DeterministicSimulationModel()

    token = (
        os.getenv("HF_API_TOKEN")
        or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        or ""
    ).strip()

    if not token:
        raise RuntimeError(
            "USE_REAL_MODEL=true requires HF_API_TOKEN "
            "or HUGGINGFACEHUB_API_TOKEN."
        )

    # Preserve compatibility with libraries that read the legacy variable.
    os.environ.setdefault(
        "HUGGINGFACEHUB_API_TOKEN",
        token,
    )

    return InferenceClientModel(
        model_id=HF_MODEL_ID,
        token=token,
        temperature=0,
        max_tokens=400,
        timeout=120,
    )


MODEL = build_model()


# -------------------------------------------------------------------------
# Domain state
# -------------------------------------------------------------------------

@dataclass
class PenguinState:
    """Serializable final state for one penguin."""

    name: str
    food: int
    has_tool: bool
    distributions: list[dict[str, Any]]


class ScientistAgent(ToolCallingAgent):
    """Agent responsible for distributing shared resources."""

    def __init__(
        self,
        initial_food_supply: int = 20,
        refresh_interval: int = 5,
    ) -> None:
        super().__init__(
            tools=[
                check_history,
                record_distribution,
            ],
            model=MODEL,
            name="scientist",
            description=(
                "A scientist who reacts to penguin actions "
                "and allocates limited food and one fishing tool."
            ),
            max_steps=2,
            verbosity_level=0,
        )

        if initial_food_supply < 0:
            raise ValueError(
                "initial_food_supply cannot be negative."
            )

        if refresh_interval <= 0:
            raise ValueError(
                "refresh_interval must be positive."
            )

        self.initial_food_supply = initial_food_supply
        self.food_supply = initial_food_supply
        self.tool_available = True
        self.refresh_interval = refresh_interval
        self.turn_counter = 0

    def refresh_resources(self) -> None:
        """Periodically reset scientist resources."""

        self.food_supply = self.initial_food_supply
        self.tool_available = True

        print("\n🔄 Scientist Resources Refreshed!")
        print(
            f"Food Supply Reset to: "
            f"{self.food_supply}"
        )
        print(
            f"Tool Availability Reset to: "
            f"{self.tool_available}"
        )

    def _safe_decision(
        self,
        penguin: "PenguinAgent",
        action: dict[str, Any],
        history: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a conservative fallback if model output is invalid."""

        requested_food = (
            action.get("action")
            == "request_food"
        )

        food = (
            min(2, self.food_supply)
            if requested_food
            and penguin.food <= 2
            else 0
        )

        tool = (
            self.tool_available
            and not penguin.has_tool
            and penguin.food <= 2
            and not history["has_tool"]
        )

        return {
            "give_food": food,
            "give_tool": tool,
        }

    def respond_to_action(
        self,
        penguin: "PenguinAgent",
        penguin_action: dict[str, Any],
    ) -> None:
        """Inspect one penguin and allocate scientist resources."""

        self.turn_counter += 1

        if (
            self.turn_counter
            % self.refresh_interval
            == 0
        ):
            self.refresh_resources()

        history = check_history.forward(
            penguin.name
        )

        print(
            f"\n--- Turn {self.turn_counter}: "
            f"Scientist Responds to {penguin.name} ---"
        )
        print(
            f"Penguin Action: {penguin_action}"
        )
        print(
            f"Penguin State: food={penguin.food}, "
            f"has_tool={penguin.has_tool}"
        )
        print(
            "Penguin History: "
            f"recent_food={history['recent_food']}, "
            f"has_had_tool={history['has_tool']}"
        )
        print(
            "Scientist Resources: "
            f"food={self.food_supply}, "
            f"tool_available={self.tool_available}"
        )

        prompt = f"""
        SCIENTIST_DECISION
        Penguin: {penguin.name}
        Penguin action: {json.dumps(penguin_action)}
        Penguin food: {penguin.food}
        Penguin has tool: {str(penguin.has_tool).lower()}
        Recent distributed food: {history['recent_food']}
        Penguin has previously received tool: {str(history['has_tool']).lower()}
        Scientist food supply: {self.food_supply}
        Scientist tool available: {str(self.tool_available).lower()}

        Return strict JSON only:
        {{"give_food": <integer from 0 to 5>, "give_tool": <boolean>}}
        """

        try:
            response = self.run(
                prompt,
                reset=True,
            )
            decision = extract_json_object(
                response
            )
        except Exception as error:
            print(
                "⚠️ Scientist decision fallback: "
                f"{type(error).__name__}: {error}"
            )
            decision = self._safe_decision(
                penguin,
                penguin_action,
                history,
            )

        requested_food = int(
            decision.get(
                "give_food",
                0,
            )
        )
        food = max(
            0,
            min(
                requested_food,
                5,
                self.food_supply,
            ),
        )

        tool_granted = (
            bool(
                decision.get(
                    "give_tool",
                    False,
                )
            )
            and self.tool_available
            and not penguin.has_tool
        )

        if food:
            self.food_supply -= food
            penguin.food += food

        if tool_granted:
            penguin.has_tool = True
            self.tool_available = False

        confirmation = (
            record_distribution.forward(
                penguin.name,
                food,
                tool_granted,
            )
        )

        print("\nScientist's Decision:")
        print(f"  - Food to Give: {food}")
        print(
            f"  - Tool to Give: "
            f"{tool_granted}"
        )
        print(f"  - History: {confirmation}")

        print("\nPost-Action State:")
        print(
            "  Scientist: "
            f"food={self.food_supply}, "
            f"tool_available={self.tool_available}"
        )
        print(
            f"  {penguin.name}: "
            f"food={penguin.food}, "
            f"has_tool={penguin.has_tool}"
        )


class PenguinAgent(ToolCallingAgent):
    """Agent that chooses how to obtain food each round."""

    def __init__(self, name: str) -> None:
        # The new exercise tool is registered here.
        super().__init__(
            tools=[find_food],
            model=MODEL,
            name=name,
            description=(
                "A penguin who can request scientist help "
                "or search for food."
            ),
            max_steps=2,
            verbosity_level=0,
        )

        self.name = name
        self.food = 0
        self.has_tool = False

    def _safe_action(self) -> dict[str, str]:
        """Return an always-valid fallback action."""

        if self.food <= 1:
            return {
                "action": "request_food",
                "method": "none",
            }

        return {
            "action": "find_food",
            "method": (
                "fishing"
                if self.has_tool
                else "foraging"
            ),
        }

    def take_action(
        self,
        round_number: int,
    ) -> dict[str, str]:
        """Ask the penguin agent for one strict JSON action."""

        history = check_history.forward(
            self.name
        )

        prompt = f"""
        You are {self.name}.
        Round: {round_number}
        Current food: {self.food}
        Has tool: {str(self.has_tool).lower()}
        Recent scientist food: {history['recent_food']}
        Previously received tool: {str(history['has_tool']).lower()}

        Choose exactly one action:
        - find_food with method "fishing" when you have a tool;
        - find_food with method "foraging" when you do not have a tool;
        - request_food when your food is very low.

        Return strict JSON only:
        {{"action": "find_food|request_food", "method": "fishing|foraging|none"}}
        """

        try:
            response = self.run(
                prompt,
                reset=True,
            )
            action = extract_json_object(
                response
            )
        except Exception as error:
            print(
                f"⚠️ {self.name} action fallback: "
                f"{type(error).__name__}: {error}"
            )
            return self._safe_action()

        action_name = str(
            action.get(
                "action",
                "",
            )
        ).strip().lower()

        method = str(
            action.get(
                "method",
                "",
            )
        ).strip().lower()

        if action_name not in {
            "find_food",
            "request_food",
        }:
            return self._safe_action()

        if action_name == "request_food":
            return {
                "action": "request_food",
                "method": "none",
            }

        expected_method = (
            "fishing"
            if self.has_tool
            else "foraging"
        )

        # A penguin without a tool cannot fish.
        if method != expected_method:
            method = expected_method

        return {
            "action": "find_food",
            "method": method,
        }


# -------------------------------------------------------------------------
# Simulation
# -------------------------------------------------------------------------

def run_simulation(
    rounds: int = 3,
    penguin_count: int = 4,
    seed: int = SIMULATION_SEED,
) -> dict[str, Any]:
    """Run the complete multi-agent simulation.

    Args:
        rounds: Number of simulation rounds.
        penguin_count: Number of penguin agents.
        seed: Seed controlling random food yields.

    Returns:
        A serializable summary containing final resources and history.
    """

    if rounds <= 0:
        raise ValueError(
            "rounds must be positive."
        )

    if penguin_count <= 0:
        raise ValueError(
            "penguin_count must be positive."
        )

    reset_simulation_state(seed)

    scientist = ScientistAgent(
        initial_food_supply=20,
        refresh_interval=5,
    )

    penguins = [
        PenguinAgent(f"Penguin{index}")
        for index in range(
            penguin_count
        )
    ]

    print("\n🐧 Starting Antarctic Simulation")
    print(
        f"Model mode: "
        f"{'Hugging Face' if USE_REAL_MODEL else 'deterministic stub'}"
    )
    print(f"Random seed: {seed}")

    for round_number in range(
        1,
        rounds + 1,
    ):
        print("\n" + "=" * 58)
        print(f"ROUND {round_number}")
        print("=" * 58)

        penguin_actions = {}

        # Every penguin independently sends an action decision.
        for penguin in penguins:
            action = penguin.take_action(
                round_number
            )
            penguin_actions[penguin.name] = action

            print(
                f"{penguin.name} Action: "
                f"{action}"
            )

        # Self-found food is applied before the scientist responds.
        for penguin in penguins:
            action = penguin_actions[
                penguin.name
            ]

            if (
                action["action"]
                == "find_food"
            ):
                food_found = find_food.forward(
                    penguin.name,
                    action["method"],
                )
                penguin.food += food_found

        # The scientist receives each action as a separate message.
        for penguin in penguins:
            scientist.respond_to_action(
                penguin,
                penguin_actions[
                    penguin.name
                ],
            )

    states = []

    print("\n" + "=" * 58)
    print("FINAL STATE")
    print("=" * 58)
    print(
        "Scientist remaining resources: "
        f"{scientist.food_supply} food, "
        f"tool_available={scientist.tool_available}"
    )

    for penguin in penguins:
        state = PenguinState(
            name=penguin.name,
            food=penguin.food,
            has_tool=penguin.has_tool,
            distributions=list(
                DISTRIBUTION_HISTORY.get(
                    penguin.name,
                    [],
                )
            ),
        )
        states.append(state)

        print(
            f"{penguin.name}: "
            f"food={penguin.food}, "
            f"has_tool={penguin.has_tool}, "
            f"distributions={len(state.distributions)}"
        )

    return {
        "rounds": rounds,
        "seed": seed,
        "model_mode": (
            "real"
            if USE_REAL_MODEL
            else "stub"
        ),
        "scientist": {
            "food_supply": scientist.food_supply,
            "tool_available": scientist.tool_available,
            "turn_counter": scientist.turn_counter,
        },
        "penguins": [
            asdict(state)
            for state in states
        ],
        "distribution_history": {
            name: list(records)
            for name, records
            in DISTRIBUTION_HISTORY.items()
        },
    }


if __name__ == "__main__":
    summary = run_simulation()

    print("\nJSON SUMMARY")
    print(
        json.dumps(
            summary,
            indent=2,
        )
    )
