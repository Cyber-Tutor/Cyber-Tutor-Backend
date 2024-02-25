
class QuizQuestion:
    """
    choices is a dictionary with keys a, b, c, d
    answer is one of the keys in choices
    topics is a list of topics that the question covers
    """
    def __init__(self, question, answer, choices, explanation, topics):
        self.question = question
        self.answer = answer
        self.choices = choices
        self.explanation = explanation
        self.topics = topics

    @staticmethod
    def from_dict(data):
        return QuizQuestion(
            question=data['question'],
            answer=data['answer'],
            choices=data['choices'],
            explanation=data['explanation'],
            topics=data['topics']
        )
    
    def to_dict(self):
        return {
            'question': self.question,
            'answer': self.answer,
            'choices': self.choices,
            'explanation': self.explanation,
            'topics': self.topics
        }
    
    def __repr__(self):
        return f"QuizQuestion(question={self.question}, answer={self.answer}, choices={self.choices}, explanation={self.explanation}, topics={self.topics})"