# Utility functions for MS-Marco experiments

from typing import Callable
from attrs import Factory
from functools import cache
import logging

from datamaestro import prepare_dataset
from datamaestro_text.transforms.ir import ShuffledTrainingTripletsLines
from datamaestro_text.data.ir import AdhocDocuments, Adhoc
from xpmir.datasets.adapters import RandomFold
from xpmir.evaluation import Evaluations, EvaluationsCollection
from xpmir.letor.samplers import PairwiseModelBasedSampler

from xpmir.measures import AP, RR, P, nDCG, R
from . import NeuralIRExperiment, configuration

from xpmir.interfaces.anserini import AnseriniRetriever

logging.basicConfig(level=logging.INFO)


@configuration
class ValidationSample:
    seed: int = 123
    size: int = 10


@configuration()
class RerankerTRECCastConfiguration(NeuralIRExperiment):
    """Configuration for rerankers"""

    validation: ValidationSample = Factory(ValidationSample)


@configuration()
class DualTRECCastConfiguration(NeuralIRExperiment):
    """Configuration for sparse retriever"""

    validation: ValidationSample = Factory(ValidationSample)


# TREC Cast 2020

v1_docs: AdhocDocuments = prepare_dataset("irds.trec-cast.v1.documents")

# Train / Val / Eval split
v1_train, v1_val, v1_eval = RandomFold.folds(dataset=prepare_dataset("irds.trec-cast.v1.2020.judged"), seed=123, size=[.80, .13, .07]).submit()
#v1_dev: Callable[[], Adhoc] = partial_cache(prepare_dataset, "irds.trec-cast.v1.2020.judged")
v1_measures = [AP @ 10, nDCG @ 3, nDCG @ 10, RR, R @ 10]


@cache
def v1_sampler() -> PairwiseInBatchNegativesSampler:
    """Train sampler
    """
    train_triples = prepare_dataset("irds.msmarco-passage.train.docpairs")
    triplets = ShuffledTrainingTripletsLines(
        seed=123,
        data=train_triples,
    ).submit()
    return PairwiseInBatchNegativesSampler(dataset=v1_train, retriever=AnseriniRetriever(k=1000, ))


@cache
def v1_validation_dataset(cfg: ValidationSample):
    """Sample dev topics to get a validation subset"""
    return RandomFold(
        dataset=v1_eval,
        seed=cfg.seed,
        fold=0,
        sizes=[cfg.size]
    ).submit()


@cache
def v1_tests():
    """MS-Marco default test collections: DL TREC 2019 & 2020 + devsmall"""
    return EvaluationsCollection(
        msmarco_dev=Evaluations(v1_devsmall(), v1_measures),
        trec2019=Evaluations(
            prepare_dataset("irds.msmarco-passage.trec-dl-2019"), v1_measures
        ),
        trec2020=Evaluations(
            prepare_dataset("irds.msmarco-passage.trec-dl-2020"), v1_measures
        ),
    )
