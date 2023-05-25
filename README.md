# PLDAC
Information retrieving for Conversational Systems / TREC CAsT 2023 participation
CoSPLADE : https://arxiv.org/abs/2301.04413
SPLADE : https://arxiv.org/pdf/2109.10086.pdf
xpmir original library : https://github.com/experimaestro/experimaestro-ir/

Experimaestro-IR is a Python library which implements various tools for experiments in the field of Information Retrieving.

Our modified version of xpmir is contained in xpmir.zip. It mainly consists of the change of the SPLADE training pipeline, which was modified to implement CoSPLADE instead.

CQR (Contextualised Query Reformulation) repository contains cqr.ipynb, which contains implementation of T5 fine-tuning on CANARD dataset for CQR.

All other files are functional, they were just tools for pre-processing data, indexing, retrieving etc... But they are not used in our main files.
