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
                "limit": 10
            }
        )

        # Check if the tool execution failed
        if tool_result.is_error:
            print("Error: Tool execution failed.")
            return

        # Handle both data and content
        if tool_result.data is not None:
            for i, candidate in enumerate(tool_result.data, start=1):
                print(f"{i}. {candidate['name']}")
                print(f"   LinkedIn: {candidate['linkedin_url']}")
                print(f"   Score: {candidate['score']}")
                print(f"   Snippet: {candidate['snippet']}")
                print("-------------------------------")
        else:
            for content in tool_result.content:
                if hasattr(content, 'text'):
                    try:
                        # Attempt to parse the text as JSON
                        structured_data = json.loads(content.text)
                        for i, candidate in enumerate(structured_data, start=1):
                            print(f"{i}. {candidate['name']}")
                            print(f"   LinkedIn: {candidate['linkedin_url']}")
                            print(f"   Score: {candidate['score']}")
                            print(f"   Snippet: {candidate['snippet']}")
                            print("-------------------------------")
                    except json.JSONDecodeError:
                        print(f"Text result (unstructured): {content.text}")

if __name__ == "__main__":
    asyncio.run(main())