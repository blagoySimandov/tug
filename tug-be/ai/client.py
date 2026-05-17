from typing import Type, TypeVar, cast, Literal
from pydantic import BaseModel
from google import genai
from google.genai import types
from os import environ

T = TypeVar("T", bound=BaseModel)



class AiClient:
    DEFAULT_MODEL = "gemini-3-flash-preview"
    TTS_MODEL = "gemini-2.5-flash-preview-tts"

    AvaillableTTSVoices = Literal[
        "Puck", "Achernar", "Alnilam", "Autonoe", "Enceladus", "Rasalgethi",
        "Sadachbia", "Schedar", "Umbriel", "Zubenelgenubi", # Male-leaning
        "Achird", "Algenib", "Callirrhoe", "Despina", "Pulcherrima",
        "Sulafat", "Vindemiatrix", "Zephyr" # Female-leaning
    ]

    def __init__(self):
        self.client = genai.Client(api_key=environ["GEMINI_TUG_API_KEY"])

    def generate_content(self, prompt: str, model: str = DEFAULT_MODEL) -> str | None:
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "temperature": 0,
                "top_p": 0.95,
                "top_k": 20,
            },
        )
        return response.text

    def generate_structured_content(
        self, prompt: str, schema: Type[T], model: str = DEFAULT_MODEL
    ) -> T:
        """
        Example Usage:
        class Recipe(BaseModel):
            name: str
            ingredients: list[str]

        ai = AiClient()
        recipe = ai.generate_structured_content("Generate a cake recipe", Recipe)
        print(recipe.name)
        """
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0,
                top_p=0.95,
                top_k=20,
            ),
        )
        # response.parsed will be an instance of the schema class
        return cast(T, response.parsed)

    def generate_speech(
        self, prompt: str, voice_name: AvaillableTTSVoices = "Puck", model: str = TTS_MODEL
    ) -> bytes | None:
        """Generates speech (TTS) from a prompt and returns the audio bytes."""

        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
                response_modalities=["AUDIO"],
                temperature=0.7,
            ),
        )

        candidates = response.candidates
        if not candidates or not candidates[0].content:
            return None

        parts = candidates[0].content.parts
        if not parts:
            return None

        for part in parts:
            if part.inline_data:
                return part.inline_data.data

        return None

