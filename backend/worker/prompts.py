"""
Worker AI prompts for generating specific content components.
Based on the technical architecture specifications.
"""

def get_learning_objective_prompt(topic: str, core_question: str) -> str:
    """
    Generate prompt for creating learning objective summary.
    
    Args:
        topic: The learning topic
        core_question: The core question
        
    Returns:
        Formatted prompt string
    """
    return f"""You are a world-class curriculum designer. Write a concise and engaging summary for a learning objective. Do not add any other commentary.

TOPIC: {topic}
CORE_QUESTION: {core_question}

SUMMARY:"""


def get_knowledge_component_prompt(topic: str, component_type: str, purpose: str) -> str:
    """
    Generate prompt for creating knowledge components.
    
    Args:
        topic: The learning topic
        component_type: Type of component (CORE_CONCEPT, FACT, EXAMPLE, etc.)
        purpose: The specific purpose of this component
        
    Returns:
        Formatted prompt string
    """
    return f"""You are an expert educator specializing in {component_type}. Create exactly one {component_type} for the following topic.

TOPIC: {topic}
COMPONENT_TYPE: {component_type}
PURPOSE: {purpose}

YOUR OUTPUT (ONLY THE {component_type} ITSELF):"""


def get_comprehension_check_prompt(topic: str) -> str:
    """
    Generate prompt for creating comprehension checks.
    
    Args:
        topic: The learning topic
        
    Returns:
        Formatted prompt string
    """
    return f"""You are an assessment designer. Create one multiple-choice question to test understanding of {topic}.

- Generate 1 question with 4 plausible options.
- Indicate the correct answer and provide a one-sentence explanation of why it is correct.
- Format your output as a JSON object with the following keys: `question_text`, `options` (array), `correct_index` (integer), `explanation`.

TOPIC: {topic}"""


# Component-specific prompts
COMPONENT_PROMPTS = {
    'CORE_CONCEPT': {
        'system_prompt': 'You are an expert educator who excels at explaining complex concepts in simple, clear terms.',
        'instruction': 'Define the core concept clearly and concisely, focusing on the essential understanding needed.'
    },
    'FACT': {
        'system_prompt': 'You are a fact-checker and educational content creator who presents accurate, verifiable information.',
        'instruction': 'State an important, accurate fact about the topic that students should know.'
    },
    'EXAMPLE': {
        'system_prompt': 'You are an expert educator who creates clear, concrete examples that illustrate abstract concepts.',
        'instruction': 'Create a specific, concrete example that demonstrates the concept with real numbers or details.'
    },
    'PRINCIPLE': {
        'system_prompt': 'You are an educational philosopher who identifies and explains fundamental principles.',
        'instruction': 'Explain a key principle or rule that governs this topic.'
    },
    'ANALOGY': {
        'system_prompt': 'You are a creative educator who makes complex topics accessible through analogies.',
        'instruction': 'Create a helpful analogy that relates this concept to something familiar.'
    },
    'WARNING': {
        'system_prompt': 'You are an experienced educator who helps students avoid common mistakes.',
        'instruction': 'Highlight a common mistake or misconception students should avoid.'
    }
}


def get_component_system_prompt(component_type: str) -> str:
    """
    Get the system prompt for a specific component type.
    
    Args:
        component_type: Type of component
        
    Returns:
        System prompt string
    """
    return COMPONENT_PROMPTS.get(component_type, {}).get('system_prompt', 'You are an expert educator.')


def get_component_instruction(component_type: str) -> str:
    """
    Get the instruction for a specific component type.
    
    Args:
        component_type: Type of component
        
    Returns:
        Instruction string
    """
    return COMPONENT_PROMPTS.get(component_type, {}).get('instruction', 'Create educational content for this topic.')
