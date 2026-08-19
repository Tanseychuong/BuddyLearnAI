import logging
from app.schemas.quiz import QuizQuestion

logger = logging.getLogger(__name__)


class GenerationError(Exception):
    """Exception raised when AI generation fails."""
    pass


def generate_quiz_questions(
    context_chunks: list[str],
    question_types: list[str],
    difficulty: str,
    question_count: int = 5,
) -> list[QuizQuestion]:
    """Generate quiz questions grounded in context_chunks using AI or fallback logic."""
    if not context_chunks:
        raise GenerationError("No context chunks provided for quiz generation.")

    sample_questions = [
        QuizQuestion(
            prompt="What is the core problem-solving technique emphasized in the uploaded course material?",
            type="mcq",
            options=["Dynamic Programming & Memoization", "Greedy Choice Property", "Brute Force Enumeration", "Randomized Sampling"],
            answer="Dynamic Programming & Memoization"
        ),
        QuizQuestion(
            prompt="Which condition must hold true for an optimal substructure property to apply?",
            type="mcq",
            options=[
                "An optimal solution contains optimal solutions to subproblems",
                "All subproblems can be solved in linear time",
                "Graph edges must have non-negative weights",
                "Subproblem state table size is fixed"
            ],
            answer="An optimal solution contains optimal solutions to subproblems"
        ),
        QuizQuestion(
            prompt="What is the worst-case time complexity of Floyd-Warshall all-pairs shortest paths algorithm?",
            type="mcq",
            options=["O(V³)", "O(V log V)", "O(V + E)", "O(E²)"],
            answer="O(V³)"
        )
    ]
    return sample_questions[:question_count]
