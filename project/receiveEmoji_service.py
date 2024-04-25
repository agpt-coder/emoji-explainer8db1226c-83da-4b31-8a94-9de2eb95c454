import unicodedata

import httpx
from pydantic import BaseModel


class EmojiResponseModel(BaseModel):
    """
    Model for responding to the emoji input request. It provides feedback on validation success or details any error that occurred during the validation process.
    """

    is_valid: bool
    message: str


async def receiveEmoji(emoji: str) -> EmojiResponseModel:
    """
    Receives an emoji character from a user, validates it to ensure it's a proper emoji, and sends it to the Explanation Processor module. The emoji should be a valid Unicode character recognized as an emoji. If the validation is successful, the emoji is sent using an internal API call to Groq's llama3 for further explanation. The route should be able to handle a JSON request containing the emoji and respond with either a success or an error message detailing the validation outcome.

    Args:
        emoji (str): A valid Unicode emoji character submitted by the user for explanation.

    Returns:
        EmojiResponseModel: Model for responding to the emoji input request. It provides feedback on validation success or details any error that occurred during the validation process.
    """
    if not (emoji and is_emoji(emoji)):
        return EmojiResponseModel(
            is_valid=False, message=f"{emoji} is not a valid emoji."
        )
    explanation = await fetch_emoji_explanation(emoji)
    if explanation:
        return EmojiResponseModel(is_valid=True, message=explanation)
    else:
        return EmojiResponseModel(
            is_valid=False,
            message="Failed to fetch explanation for the submitted emoji.",
        )


def is_emoji(character: str) -> bool:
    """
    Checks if the character is a recognized emoji.

    Args:
        character (str): A single Unicode character.

    Returns:
        bool: True if the character is an emoji, False otherwise.
    """
    return character in unicodedata.lookup("EMOJI")


async def fetch_emoji_explanation(emoji: str) -> str:
    """
    Fetches the explanation for the specified emoji from Groq's llama3 service.

    Args:
        emoji (str): A valid Unicode emoji character.

    Returns:
        str: Explanation text for the emoji or None if an error occurred.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/llama3/explain", json={"emoji": emoji}
        )
        if response.status_code == 200:
            return response.json().get("explanation")
        else:
            return ""
