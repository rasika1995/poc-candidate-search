import asyncio
import json
from fastmcp.client import Client

async def main():
    async with Client(transport="http://localhost:8000/mcp") as client:
        # call_tool returns a CallToolResult object
        tool_result = await client.call_tool(
            "search_best_linkedin_profiles",
            {
                "skills": ["Node.js", "React"],
                "location": "Sri Lanka",
                "offset": 10
            }
        )

        # Check if the tool execution failed
        if tool_result.is_error:
            print("Error: Tool execution failed.")
            return

        # Handle both data and content
        if tool_result.data is not None:
            # Extract profiles and pagination
            profiles = tool_result.data.get("profiles", [])
            pagination = tool_result.data.get("pagination", {})

            # Display profiles
            for i, candidate in enumerate(profiles, start=1):
                print(f"{i}. {candidate['name']}")
                print(f"   LinkedIn: {candidate['linkedin_url']}")
                print(f"   Score: {candidate['score']}")
                print(f"   Snippet: {candidate['snippet']}")
                print("-------------------------------")

            # Display pagination details
            print("Pagination Details:")
            for key, value in pagination.items():
                print(f"   {key}: {value}")
        else:
            for content in tool_result.content:
                if hasattr(content, 'text'):
                    try:
                        # Attempt to parse the text as JSON
                        structured_data = json.loads(content.text)
                        profiles = structured_data.get("profiles", [])
                        pagination = structured_data.get("pagination", {})

                        # Display profiles
                        for i, candidate in enumerate(profiles, start=1):
                            print(f"{i}. {candidate['name']}")
                            print(f"   LinkedIn: {candidate['linkedin_url']}")
                            print(f"   Score: {candidate['score']}")
                            print(f"   Snippet: {candidate['snippet']}")
                            print("-------------------------------")

                        # Display pagination details
                        print("Pagination Details:")
                        for key, value in pagination.items():
                            print(f"   {key}: {value}")
                    except json.JSONDecodeError:
                        print(f"Text result (unstructured): {content.text}")

if __name__ == "__main__":
    asyncio.run(main())