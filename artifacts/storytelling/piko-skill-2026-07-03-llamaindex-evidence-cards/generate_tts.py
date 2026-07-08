import asyncio
import pathlib
import re

import edge_tts


BASE = pathlib.Path(__file__).resolve().parent
INPUT = BASE / "voiceover.md"
OUTPUT = BASE / "audio" / "voiceover.mp3"


def clean_markdown(text: str) -> str:
    text = re.sub(r"^#.*$", "", text, flags=re.M)
    text = text.replace("`", "")
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


async def main() -> None:
    text = clean_markdown(INPUT.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text,
        voice="zh-CN-YunxiNeural",
        rate="+12%",
        pitch="+0Hz",
    )
    await communicate.save(str(OUTPUT))
    print(OUTPUT)


if __name__ == "__main__":
    asyncio.run(main())
