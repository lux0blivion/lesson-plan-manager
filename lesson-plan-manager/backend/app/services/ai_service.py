import os
import time
import json
from ..logger import setup_logger

logger = setup_logger(__name__)

SYSTEM_PROMPT = """Você é um Assistente Pedagógico especializado em planejamento educacional.
Sua função é analisar planos de aula e sugerir conteúdos complementares, tópicos relacionados
e tags relevantes para enriquecer o material didático.

Sempre responda SOMENTE com um objeto JSON válido, sem texto adicional,
sem markdown, sem explicações.
O formato deve ser exatamente:
{
  "complementary_contents": "sugestões de conteúdos complementares",
  "related_topics": "tópicos relacionados que podem ser explorados",
  "suggested_tags": ["tag1", "tag2", "tag3"],
  "support_resources": "sugestões de recursos de apoio: livros, sites, vídeos"
}"""


def get_ai_recommendations(title: str, discipline: str, summary: str) -> dict:
    """Call Anthropic API and return structured recommendations."""

    start_time = time.time()

    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Mock mode for local development without API key
    if not api_key:
        logger.warning(
            "mock_ai_mode_enabled",
            title=title,
            discipline=discipline,
        )

        return {
            "complementary_contents": (
                f"Conteúdos complementares sobre {title}, "
                "conceitos fundamentais, aplicações práticas e estudos de caso."
            ),
            "related_topics": (
                f"Tópicos relacionados à disciplina de {discipline}, "
                "aprofundamento teórico e exercícios práticos."
            ),
            "suggested_tags": [
                discipline.lower(),
                "educação",
                "planejamento"
            ],
            "support_resources": (
                "Vídeos educativos, artigos científicos, livros introdutórios "
                "e plataformas online de aprendizagem."
            )
        }

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    user_message = f"""Analise o seguinte plano de aula e forneça recomendações pedagógicas:

Título da Aula: {title}
Disciplina: {discipline}
Ementa/Resumo: {summary}

Forneça:
1. Conteúdos complementares detalhados
2. Tópicos relacionados para aprofundamento
3. Exatamente 3 tags relevantes
4. Recursos de apoio (livros, sites, vídeos sugeridos)"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    latency = round(time.time() - start_time, 2)
    token_usage = message.usage.input_tokens + message.usage.output_tokens

    logger.info(
        "ai_request_completed",
        title=title,
        discipline=discipline,
        token_usage=token_usage,
        latency_seconds=latency,
        model=message.model,
    )

    raw_text = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]

        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

        raw_text = raw_text.strip()

    result = json.loads(raw_text)

    # Ensure suggested_tags is a list of exactly 3
    tags = result.get("suggested_tags", [])

    if isinstance(tags, list):
        result["suggested_tags"] = tags[:3]
    else:
        result["suggested_tags"] = []

    return result