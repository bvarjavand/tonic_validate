from ast import Dict
from typing import List

import openai
from tvalmetrics.classes.llm_response import LLMResponse
from tvalmetrics.classes.run_score import Score
from tvalmetrics.metrics.answer_similarity_metric import AnswerSimilarityMetric

from tvalmetrics.metrics.metric import Metric
from tvalmetrics.services.openai_service import OpenAIService


class ValidateScorer:
    def __init__(self, metrics: List[Metric]):
        self.metrics = metrics

    def score_run(self, responses: List[LLMResponse]) -> List[Score]:
        """Calculate metric scores for a list of LLMResponse objects.

        Parameters
        ----------
        responses: List[LLMResponse]
            The list of LLMResponse objects to be scored.

        Returns
        -------
        float
            The score for the list of LLMResponse objects.
        """
        results: List[Score] = []
        for response in responses:
            # We cache per response, so we need to create a new OpenAIService
            openai_service = OpenAIService()
            for metric in self.metrics:
                score = metric.score(response, openai_service)
                results.append(
                    Score(score=score, metric_name=metric.name, llm_response=response)
                )
        return results
