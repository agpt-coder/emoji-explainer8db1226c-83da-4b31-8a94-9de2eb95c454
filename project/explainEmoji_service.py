import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class EmojiExplanationResponse(BaseModel):
    """
    Model for the response containing the emoji with its explanation.
    """

    emoji: str
    explanation: str


async def explainEmoji(emoji: str) -> EmojiExplanationResponse:
    """
    Receives an emoji and returns its explanation. It checks the database first for an existing explanation. If not found,
    it fetches the explanation from the Groq's llama3 service using the `fetch_explanation_from_groq` function, stores
    it in the database, and then returns the explanation.

    Args:
        emoji (str): A single emoji character that needs an explanation.

    Returns:
        EmojiExplanationResponse: Model for the response containing the emoji with its explanation.
    """
    emoji_record = await prisma.models.Emoji.prisma().find_unique(
        where={"symbol": emoji}, include={"explanations": True}
    )
    if emoji_record and emoji_record.explanations:
        explanation_text = emoji_record.explanations[0].content
    else:
        explanation_text = await fetch_explanation_from_groq(emoji)
        if not emoji_record:
            emoji_record = await prisma.models.Emoji.prisma().create(
                data={"symbol": emoji}
            )
        await prisma.models.Explanation.prisma().create(
            data={
                "content": explanation_text,
                "emojiId": emoji_record.id,
                "updatedBy": 1,
            }
        )
    return EmojiExplanationResponse(emoji=emoji, explanation=explanation_text)


async def fetch_explanation_from_groq(emoji: str) -> str:
    """
    Fetches an explanation of an emoji from the Groq llama3 service.

    Args:
        emoji (str): The emoji to get an explanation for.

    Returns:
        str: A fetched explanation from the Groq service.

    This implementation uses HTTPX for asynchronous HTTP requests.
    """
    url = f"https://api.groq.com/llama3/explain?emoji={emoji}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        result = response.json()
        return result["explanation"]
