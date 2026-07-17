"""Key-free tests for the Antarctic Agents simulation."""

import os

os.environ["USE_REAL_MODEL"] = "false"
os.environ["SIMULATION_SEED"] = "42"

import starter


def test_find_food_ranges():
    """Fishing and foraging stay inside the required ranges."""

    starter.reset_simulation_state(seed=7)

    fishing_values = [
        starter.find_food.forward(
            "TestPenguin",
            "fishing",
        )
        for _ in range(20)
    ]

    foraging_values = [
        starter.find_food.forward(
            "TestPenguin",
            "foraging",
        )
        for _ in range(20)
    ]

    assert all(
        2 <= value <= 7
        for value in fishing_values
    )
    assert all(
        0 <= value <= 3
        for value in foraging_values
    )


def test_three_round_simulation_updates_state():
    """The complete simulation runs and updates food/history."""

    summary = starter.run_simulation(
        rounds=3,
        penguin_count=4,
        seed=42,
    )

    assert summary["rounds"] == 3
    assert summary["scientist"]["turn_counter"] == 12
    assert len(summary["penguins"]) == 4

    assert all(
        penguin["food"] >= 0
        for penguin in summary["penguins"]
    )

    assert any(
        penguin["food"] > 0
        for penguin in summary["penguins"]
    )

    assert all(
        len(
            summary[
                "distribution_history"
            ][penguin["name"]]
        )
        == 3
        for penguin in summary["penguins"]
    )

    assert any(
        penguin["has_tool"]
        for penguin in summary["penguins"]
    )
