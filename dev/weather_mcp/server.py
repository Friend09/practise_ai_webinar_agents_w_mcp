"""
Weather MCP server - A model context protocol server that provides weather information

This server implements:
- a weather tool that returns hardcoded temperature data
- mcp prompt template for weather related interactions
- stdio transport for communication w/ claude desktop

built using fastmcp
"""

import sys
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# create fastmcp server
mcp = FastMCP("weather-server")

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get current weather information for a specified city.
    Returns temperature data for the requested location.

    Args:
        city: Name of the city to get weather for (eg: 'New york')

    Returns:
        Formatted weather information string
    """
    # validate city parameters
    if not city or not city.strip():
        raise ValueError("City parameter cannot be empty")

    city = city.strip()
    print(f"Processing weather request for city {city}", file=sys.stderr)

    # get current timestamp for the response
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    weather_report = (
        f"Weather Report for {city}\n"
        "========================\n"
        f"Current Temperature: 83F\n"
        "Conditions: Clear\n"
        "Humidity: 65%\n"
        "Wind: Light breeze\n"
        f"Last Updated: {timestamp}\n"
        "\n"
    )

    print(f"Returning. weather data for {city}", file=sys.stderr)
    return weather_report


@mcp.prompt()
def weather_inquiry(location: str) -> str:
    """
    Template for asking abouat the weather conditions in a specific location.

    Args:
        location: The city or location to inquire about

    Returns:
        Formatted prompt for weather inquiries
    """
    prompt = f"""I need current weather information for {location}. Please provide the temperature and any relevant weather conditions. If you need to use a tool to get this information, please do so."""

    return (prompt)

@mcp.prompt()
def weather_travel_advice(destination: str, travel_date: str = None) -> list[base.Message]:
    """
    Template for getting weather-based travel advice for a destination.

    Args:
        destination: Travel destination city
        travel_date: Planned travel date (optional)

    Returns:
        List of messages for travel weather advice
    """
    date_info = f" for travel on {travel_date}" if travel_date else " for current conditions"

    prompt_text = (
        f"""
        I'm planning to travel to {destination}{date_info}. Please check the current weather conditions and provide advice on what to pack and any weather-related conditions for my trip. Use the weather tool to get current temperature data.
        """
    )

    return [
        base.UserMessage(prompt_text)
    ]

def main():
    """
    Main entry point for the weather mcp server.
    sets up stdio transport and starts the server to listen for mcp requests.
    """
    try:
        print("Starting weatehr MCP server...", file=sys.stderr)
        print("Server ready to accept connections via stdio", file=sys.stderr)

        mcp.run()

    except Exception as e:
        print(f"Failed to start weather mcp server {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
