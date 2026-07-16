"""Offline Airbnb-like MCP stub for deterministic notebook execution.

The real OpenBnB server performs network searches. This local server exposes
compatible tool names and returns fixed listings, allowing the mini-agent to
run without Node.js, npm, internet access, or external credentials.
"""

from typing import Any

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("AirbnbStub")


# Fixed sample data. Prices are demonstration values, not live quotations.
LISTINGS: dict[str, list[dict[str, Any]]] = {
    "paris": [
        {
            "id": "paris-101",
            "name": "Canal-side studio",
            "location": "Paris, France",
            "price_per_night": 145,
            "rating": 4.82,
            "features": ["balcony", "wifi", "kitchen"],
            "url": "https://example.com/airbnb/paris-101",
        },
        {
            "id": "paris-202",
            "name": "Montmartre apartment",
            "location": "Paris, France",
            "price_per_night": 210,
            "rating": 4.91,
            "features": ["city view", "workspace", "washer"],
            "url": "https://example.com/airbnb/paris-202",
        },
        {
            "id": "paris-303",
            "name": "Latin Quarter room",
            "location": "Paris, France",
            "price_per_night": 95,
            "rating": 4.67,
            "features": ["private room", "wifi"],
            "url": "https://example.com/airbnb/paris-303",
        },
    ],
    "london": [
        {
            "id": "london-101",
            "name": "Shoreditch loft",
            "location": "London, UK",
            "price_per_night": 190,
            "rating": 4.79,
            "features": ["workspace", "wifi", "kitchen"],
            "url": "https://example.com/airbnb/london-101",
        },
        {
            "id": "london-202",
            "name": "Camden garden flat",
            "location": "London, UK",
            "price_per_night": 230,
            "rating": 4.88,
            "features": ["garden", "washer", "kitchen"],
            "url": "https://example.com/airbnb/london-202",
        },
    ],
    "abidjan": [
        {
            "id": "abidjan-101",
            "name": "Cocody modern residence",
            "location": "Abidjan, Côte d’Ivoire",
            "price_per_night": 120,
            "rating": 4.74,
            "features": ["pool", "wifi", "parking"],
            "url": "https://example.com/airbnb/abidjan-101",
        },
        {
            "id": "abidjan-202",
            "name": "Marcory business apartment",
            "location": "Abidjan, Côte d’Ivoire",
            "price_per_night": 85,
            "rating": 4.69,
            "features": ["workspace", "wifi", "air conditioning"],
            "url": "https://example.com/airbnb/abidjan-202",
        },
    ],
}


def normalize_location(location: str) -> str:
    """Map common location strings to the stub's lookup keys."""
    normalized = location.strip().lower()

    if "paris" in normalized:
        return "paris"
    if "london" in normalized:
        return "london"
    if "abidjan" in normalized:
        return "abidjan"

    return normalized


@mcp.tool()
def airbnb_search(
    location: str,
    checkin: str | None = None,
    checkout: str | None = None,
    adults: int = 1,
    children: int = 0,
    infants: int = 0,
    pets: int = 0,
    minPrice: int | None = None,
    maxPrice: int | None = None,
    propertyType: str | None = None,
    limit: int = 3,
) -> dict[str, Any]:
    """Return fixed Airbnb-like listings for a location.

    The argument names intentionally resemble the real OpenBnB MCP tool so
    that the orchestrator can switch between the stub and real server.
    """
    key = normalize_location(location)
    candidates = list(LISTINGS.get(key, []))

    if minPrice is not None:
        candidates = [
            item for item in candidates
            if item["price_per_night"] >= minPrice
        ]

    if maxPrice is not None:
        candidates = [
            item for item in candidates
            if item["price_per_night"] <= maxPrice
        ]

    # The stub does not deeply model guest capacity or property types, but
    # it echoes filters to make the data flow visible.
    selected = candidates[: max(1, min(limit, 5))]

    return {
        "source": "offline Airbnb stub",
        "location": location,
        "checkin": checkin,
        "checkout": checkout,
        "guests": {
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets,
        },
        "propertyType": propertyType,
        "count": len(selected),
        "listings": selected,
    }


@mcp.tool()
def airbnb_listing_details(id: str) -> dict[str, Any]:
    """Return one fixed listing by its identifier."""
    for city_listings in LISTINGS.values():
        for listing in city_listings:
            if listing["id"] == id:
                return {
                    "source": "offline Airbnb stub",
                    "listing": listing,
                }

    return {
        "error": f"Unknown listing id: {id}",
    }


def main() -> None:
    """Start the offline Airbnb stub over STDIO."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
