import argparse
import asyncio
import json
from fastmcp import Client


async def main():
    parser = argparse.ArgumentParser(description="Find best candidates for a job")
    
    parser.add_argument(
        "--skills", required=True, help="Comma-separated list of skills (e.g., Python,Django)"
    )
    parser.add_argument("--location", default="", help="Candidate location (optional)")
    parser.add_argument("--experience", default="", help="Experience filter (optional)")
    parser.add_argument("--position", default="", help="Position filter (optional)")
    parser.add_argument("--limit", type=int, default=10, help="Number of candidates per page")
    parser.add_argument("--page", type=int, default=1, help="Page number for pagination")
    
    args = parser.parse_args()
    
    # Split skills into list
    skills = [s.strip() for s in args.skills.split(",") if s.strip()]

    # Simple inference from file path - defaults to STDIO transport
    async with Client("server.py") as client:
    # async with Client(transport="http://localhost:8000/mcp") as client:
        result = await client.call_tool("find_best_candidates", {
            "skills": skills,
            "location": args.location,
            "experience": args.experience or None,
            "position": args.position or None,
            "limit": args.limit,
            "page": args.page
        })

        if result.is_error:
            print("Tool error:", result)
            return

        # Robust handling
        if result.data is not None:
            candidates = result.data.get("candidates", [])
            pagination = result.data.get("pagination", {})
        else:
            # Fallback: parse content as JSON
            try:
                fallback_data = json.loads(result.content)
                candidates = fallback_data.get("candidates", [])
                pagination = fallback_data.get("pagination", {})
            except Exception:
                candidates = []
                pagination = {}
        print("=== Best Candidates ===")
        print(json.dumps({
            "candidates": candidates,
            "pagination": pagination
        }, indent=2, ensure_ascii=False))
        
if __name__ == "__main__":
    asyncio.run(main())