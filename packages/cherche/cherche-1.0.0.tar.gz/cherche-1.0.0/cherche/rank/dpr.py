from __future__ import annotations

__all__ = ["DPR"]


import typing

from ..similarity import dot
from .base import MemoryStore, Ranker


class DPR(Ranker):
    """DPR ranks documents using distinct models to encode the query and
    document contents.

    Parameters
    ----------
    key
        Field identifier of each document.
    on
        Fields to use to match the query to the documents.
    encoder
        Encoding function dedicated to documents.
    query_encoder
        Encoding function dedicated to the query.
    k
        Number of documents to reorder. The default value is None, i.e. all documents will be
        reordered and returned.
    similarity
        Similarity measure to compare documents embeddings and query embedding (similarity.cosine
        or similarity.dot).

    Examples
    --------

    >>> from pprint import pprint as print
    >>> from cherche import rank
    >>> from sentence_transformers import SentenceTransformer

    >>> documents = [
    ...    {"id": 0, "title": "Paris", "article": "This town is the capital of France", "author": "Wiki"},
    ...    {"id": 1, "title": "Eiffel tower", "article": "Eiffel tower is based in Paris", "author": "Wiki"},
    ...    {"id": 2, "title": "Montreal", "article": "Montreal is in Canada.", "author": "Wiki"},
    ... ]

    >>> ranker = rank.DPR(
    ...    key = "id",
    ...    on = ["title", "article"],
    ...    encoder = SentenceTransformer('facebook-dpr-ctx_encoder-single-nq-base').encode,
    ...    query_encoder = SentenceTransformer('facebook-dpr-question_encoder-single-nq-base').encode,
    ...    k = 2,
    ... )

    >>> ranker.add(documents=documents)
    DPR ranker
        key: id
        on: title, article
        k: 2
        similarity: dot
        Embeddings pre-computed: 3

    >>> print(ranker(q="Paris", documents=[{"id": 0}, {"id": 1}, {"id": 2}]))
    [{'id': 0, 'similarity': 74.0235366821289},
     {'id': 1, 'similarity': 68.8065185546875}]

    >>> print(ranker(q="Paris", documents=documents))
    [{'article': 'This town is the capital of France',
      'author': 'Wiki',
      'id': 0,
      'similarity': 74.0235366821289,
      'title': 'Paris'},
     {'article': 'Eiffel tower is based in Paris',
      'author': 'Wiki',
      'id': 1,
      'similarity': 68.8065185546875,
      'title': 'Eiffel tower'}]

    >>> ranker += documents

    >>> print(ranker(q="Paris", documents=[{"id": 0}, {"id": 1}, {"id": 2}]))
    [{'article': 'This town is the capital of France',
      'author': 'Wiki',
      'id': 0,
      'similarity': 74.0235366821289,
      'title': 'Paris'},
     {'article': 'Eiffel tower is based in Paris',
      'author': 'Wiki',
      'id': 1,
      'similarity': 68.8065185546875,
      'title': 'Eiffel tower'}]

    """

    def __init__(
        self,
        key: str,
        on: str | list,
        encoder,
        query_encoder,
        k: int | typing.Optionnal = None,
        similarity=dot,
        store=MemoryStore(),
        path: str | typing.Optionnal = None,
    ) -> None:
        super().__init__(
            key=key, on=on, encoder=encoder, k=k, similarity=similarity, store=store
        )
        self.query_encoder = query_encoder

    def __call__(self, q: str, documents: list, **kwargs) -> list:
        """Encode inputs query and ranks documents based on the similarity between the query and
        the selected field of the documents.

        Parameters
        ----------
        q
            Input query.
        documents
            List of documents to rank.

        """
        if not documents:
            return []

        return self.rank(
            query_embedding=self.query_encoder(q),
            documents=documents,
        )
