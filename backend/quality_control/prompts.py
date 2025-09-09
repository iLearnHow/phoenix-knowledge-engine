"""
Quality control prompts for validating AI-generated content.
Based on the technical architecture specifications.
"""

CRITIC_AI_PROMPT_TEMPLATE = """
You are a harsh fact-checker. Your only goal is to find errors. Analyze the following TEXT for any factual inaccuracies, logical fallacies, or misleading statements. If the text is 100% accurate, respond with "APPROVED". If you find any issue, respond with "FLAGGED: [concise reason for flagging]".

TEXT: {content}
TOPIC: {topic}
"""

def get_critic_prompt(content: str, topic: str) -> str:
    """
    Generate the critic AI prompt for fact-checking content.
    
    Args:
        content: The content to be fact-checked
        topic: The topic context
        
    Returns:
        Formatted prompt string
    """
    return CRITIC_AI_PROMPT_TEMPLATE.format(content=content, topic=topic)


# Validation rules and thresholds
VALIDATION_RULES = {
    'summary': {
        'min_length': 50,
        'max_length': 500,
        'required_fields': ['title', 'core_question', 'summary']
    },
    'knowledge_component': {
        'min_length': 20,
        'max_length': 1000,
        'required_fields': ['type', 'content', 'sort_order']
    },
    'comprehension_check': {
        'min_length': 20,
        'max_length': 200,
        'required_fields': ['question_text', 'options', 'correct_index', 'explanation'],
        'min_options': 2,
        'max_options': 6
    }
}

# Content type validation
CONTENT_TYPE_VALIDATION = {
    'CORE_CONCEPT': {
        'min_length': 50,
        'max_length': 500,
        'keywords': ['concept', 'definition', 'understanding']
    },
    'FACT': {
        'min_length': 20,
        'max_length': 200,
        'keywords': ['fact', 'information', 'data']
    },
    'EXAMPLE': {
        'min_length': 50,
        'max_length': 800,
        'keywords': ['example', 'instance', 'case']
    },
    'PRINCIPLE': {
        'min_length': 30,
        'max_length': 400,
        'keywords': ['principle', 'rule', 'law']
    },
    'ANALOGY': {
        'min_length': 40,
        'max_length': 600,
        'keywords': ['analogy', 'like', 'similar', 'compare']
    },
    'WARNING': {
        'min_length': 30,
        'max_length': 300,
        'keywords': ['warning', 'caution', 'avoid', 'mistake']
    }
}
