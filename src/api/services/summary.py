import logging
import time
from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.core.config import settings
from src.schemas import SummaryInput, SummaryOutput

logger = logging.getLogger(__name__)

summary_router = APIRouter(tags=["summarize"])


class SummaryService:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.llm.api_key,
            base_url=settings.llm.api_base,
            model=settings.llm.model_name,
            temperature=0.0,
            max_tokens=255
        )
        
        system_prompt = """
#Role
You are helping the user come up with a short, meaningful header for their own message.

#Language
Write only in English.

#ResponseRules
Do not repeat or rephrase the message.
Do not address the user or respond to the message.
Write the header as if the user is giving a title to their own message.
Make the header as short as possible (preferably 7-15 words).
The header should be a short statement, not a question.
The header should help the user easily find this message later.
Don't make up anything extra, just use the information in the message.

#ContentRestrictions
Under no circumstances include profanity, offensive language, slurs, explicit content, or any terms related to illegal or highly sensitive topics.

#FallbackHeaders
If the message contains such content, replace the header with a neutral phrase such as:
    - "Mentions sensitive content"
    - "Being rude or offensive"
    - "Geopolitics is mentioned inappropriately"
    - "Inappropriate conversation"
    - "Offensive topic"
    - "A very controversial topic is mentioned"
    - "Refers to restricted or inappropriate topic"

#Input
Message: {message}

#OutputFormat
Return only the header text without any additional formatting, explanations or JSON.
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
        ])
        
        self.chain = prompt | self.llm

    async def summarize(self, summary_input: SummaryInput) -> str:
        """
        Helper summarize function
        """
        logger.info(f"Start generate summary for: {summary_input.chat_id}")
        
        start = time.time()
        response = await self.chain.ainvoke({'message': summary_input.question})
        
        if hasattr(response, 'content'):
            output = response.content
        else:
            output = str(response)
            
        output = output.strip()
        logger.info(f"Summary generated in {time.time() - start:.2f}s, generated summary: {output}")
        return output

summary_service = SummaryService()


@summary_router.post(
                    "/summarize", 
                     response_model=SummaryOutput,
                     description="Returns a concise summary to help user find this message later",
                     summary="Generate a short header for a chat message"
                     )
async def summarize(input_data: SummaryInput):
    """
    Generate a summary/header for a chat message.
    """
    try:
        logger.info(f"Processing summarize request for chat_id: {input_data.chat_id}")
        
        summary_text = await summary_service.summarize(input_data)
        
        return SummaryOutput(
            request_id=input_data.request_id,
            chat_id=input_data.chat_id,
            user_id=input_data.user_id,
            name=summary_text
        )
    except Exception as e: # To Do# What Exception?
        logger.error(f"Error processing summarize request: {str(e)}")
        return SummaryOutput(
            request_id=input_data.request_id,
            chat_id=input_data.chat_id,
            user_id=input_data.user_id,
            name= "Service unavailable now" # Should be a lang plug?
        )