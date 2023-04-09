from attrs import define
from experimaestro import experiment
from functools import partial, cached_property
import logging

from datamaestro import prepare_dataset
from datamaestro_text.transforms.ir import ShuffledTrainingTripletsLines
from datamaestro_text.data.ir import AdhocDocuments, Adhoc
from experimaestro.launcherfinder import find_launcher
from xpmir.datasets.adapters import RandomFold
from xpmir.evaluation import Evaluations, EvaluationsCollection
import xpmir.interfaces.anserini as anserini
from xpmir.letor import Device, Random
from xpmir.letor.batchers import PowerAdaptativeBatcher
from xpmir.letor.devices import CudaDevice
from xpmir.letor.optim import (
    TensorboardService,
)
from xpmir.letor.samplers import PairwiseSampler, PairwiseModelBasedSampler
from xpmir.measures import AP, RR, P, nDCG, R
#from xpmir.rankers import documents_retriever, RandomScorer
from xpmir.utils.utils import find_java_home
from experimaestro.utils.jobs import jobmonitor
from pathlib import Path
import sys
from IPython.display import display, Markdown, Latex


from . import PaperExperiment

logging.basicConfig(level=logging.INFO)

# Espace pour les fichiers
libpath = Path(".") / "lib" / "xpmir_userlib"
libpath.mkdir(parents=True, exist_ok=True)
(libpath / "__init__.py").touch()
libpath = str(libpath.absolute().parent)
if libpath not in sys.path:
    sys.path.append(libpath)


@define(kw_only=True)
class TRECCast2020Configuration(PaperExperiment):
    gpu: bool = True
    """Use GPU for computation"""


class TRECCast2020Experiment:
    """Basic settings for the experiment based on the TREC CAsT 2020, including the
    preparation of the dataset, evaluation metrics, etc"""

    eval: Adhoc
    """A set of 10 topics used for evaluation"""

    val: Adhoc
    """A set of topics used for validation"""

    def __init__(self, xp: experiment, cfg: TRECCast2020Configuration):
        self.cfg = cfg
        self.device = (
            CudaDevice() if cfg.gpu else Device()
        )  #: the device (CPU/GPU) for the experiment

        self.random = Random(seed=0)
        
        # Using TREC CAST 2020 queries and qrels
        dataset = prepare_dataset("irds.trec-cast.v1.2020.judged")
        
        # Validation/evaluation split
        ds_val, ds_eval = RandomFold.folds(dataset=dataset, seed=123, sizes=[.93, .7])
        jobmonitor(ds_val, ds_eval)

        # Datasets: train, validation and test
        self.documents: AdhocDocuments = prepare_dataset("irds.trec-cast.v1.documents")
        self.eval: Adhoc = ds_eval
        self.val: Adhoc = ds_val

        self.measures = [R @ 10, AP @ 10, nDCG @ 3, nDCG @ 10, RR]

        # Creates the directory with tensorboard data
        xp.token = xp.current.setenv("PYTHONPATH", libpath)
        self.tb = xp.current.add_service(TensorboardService(xp.current.resultspath / "runs"))
        xp.current.setenv("PYTHONPATH", libpath)

@define(kw_only=True)
class RerankerTRECCast2020Configuration(TRECCast2020Configuration):
    validation_size: int = 10
    """Number of validation topics"""


'''
class RerankerTRECCast2020Experiment(TRECCast2020Experiment):
    """Base class for reranker-based TREC CAST 2020 experiments"""

    cfg: RerankerTRECCast2020Configuration

    ds_val: RandomFold
    """TREC CAST 2020 validation set"""

    tests: EvaluationsCollection
    """The collections on which the models are evaluated"""

    @cached_property
    def train_sampler(self) -> PairwiseModelBasedSampler:
        """Train sampler
        By default, this uses shuffled pre-computed triplets from MS Marco
        """
        train_triples = prepare_dataset("irds.msmarco-passage.train.docpairs")
        triplesid = ShuffledTrainingTripletsLines(
            seed=123,
            data=train_triples,
        ).submit()

        return TripletBasedSampler(source=triplesid, index=self.documents)

    def __init__(self, xp: experiment, cfg: RerankerMSMarcoV1Configuration):
        super().__init__(xp, cfg)

        # Launcher for indexation
        self.launcher_index = find_launcher(cfg.indexation.requirements)

        # Sample the dev set to create a validation set
        self.ds_val = RandomFold(
            dataset=self.dev,
            seed=123,
            fold=0,
            sizes=[cfg.validation_size],
            exclude=self.devsmall.topics,
        ).submit()

        # Prepares the test collections evaluation
        self.tests = EvaluationsCollection(
            msmarco_dev=Evaluations(self.devsmall, self.measures),
            trec2019=Evaluations(
                prepare_dataset("irds.msmarco-passage.trec-dl-2019"), self.measures
            ),
            trec2020=Evaluations(
                prepare_dataset("irds.msmarco-passage.trec-dl-2020"), self.measures
            ),
        )

        # Sets the working directory and the name of the xp
        # Needed by Pyserini
        xp.setenv("JAVA_HOME", find_java_home())

        # Setup indices and validation/test base retrievers
        self.retrievers = partial(
            anserini.retriever,
            anserini.index_builder(launcher=self.launcher_index),
            model=self.basemodel,
        )  #: Anserini based retrievers

        self.model_based_retrievers = partial(
            documents_retriever,
            batch_size=cfg.retrieval.batch_size,
            batcher=PowerAdaptativeBatcher(),
            device=self.device,
        )  #: Model-based retrievers

        self.test_retrievers = partial(
            self.retrievers, k=cfg.retrieval.k
        )  #: Test retrievers

        # Search and evaluate with a random re-ranker
        random_scorer = RandomScorer(random=self.random).tag("reranker", "random")
        self.tests.evaluate_retriever(
            partial(
                self.model_based_retrievers,
                retrievers=self.test_retrievers,
                scorer=random_scorer,
                device=None,
            )
        )

        # Search and evaluate with the base model
        self.tests.evaluate_retriever(self.test_retrievers, self.launcher_index)
'''