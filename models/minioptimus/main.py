import asyncio
from .society import Society

async def main():
    society = Society()
    await society.simulate()

if __name__ == "__main__":
    asyncio.run(main())