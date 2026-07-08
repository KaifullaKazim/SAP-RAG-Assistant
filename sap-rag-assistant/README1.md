# SAP BTP Knowledge Assistant (RAG)

A minimal Retrieval-Augmented Generation system that answers questions about
SAP BTP concepts — CDS Views, OData, RAP, Fiori Elements, AI Core, the
Generative AI Hub, and Joule — grounded strictly in a small local knowledge
base, with cited sources.

Built to demonstrate the core RAG pattern end-to-end: **index → retrieve →
augment → generate**, without depending on a GPU, an internet-hosted
embedding model, or a paid vector database.

## Why TF-IDF instead of embeddings?

This is a deliberate scope choice, not a limitation I was unaware of. TF-IDF
+ cosine similarity is a completely valid retrieval strategy for a small,
keyword-distinct knowledge base like this one, and it means the whole
project runs offline in under a second with zero external dependencies
beyond `scikit-learn`. The retrieval step is isolated in a single
`Retriever` class specifically so it can be swapped for a real embedding
model without touching the rest of the pipeline.

**Natural next step:** replace `Retriever.retrieve()` with a call to
**SAP HANA Cloud Vector Engine** (store chunk embeddings generated via
SAP AI Core's embedding models, query with cosine/L2 search) — turning this
from a local demo into an SAP BTP-native RAG service. That's the direction
I'd take this in for a production "SAP Support Ticket Intelligence" version.

## How it works

1. **Index** — `docs/*.txt` are loaded and split into paragraph-level chunks.
2. **Retrieve** — the query and every chunk are TF-IDF vectorized; the top-3
   chunks by cosine similarity are selected.
3. **Augment** — those chunks are inserted into a prompt template that
   instructs the model to answer *only* from the given context.
4. **Generate** — the prompt is sent to Claude, which returns a grounded
   answer. If no API key is set, the app still prints the retrieved sources
   so the retrieval step can be evaluated on its own.

## Run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here   # optional — omit to see retrieval only
python app.py "What does RAP replace?"
```

Or drop into interactive mode:

```bash
python app.py
> How does Joule relate to the Generative AI Hub?
```

## Example output

```
Query: How does Joule relate to the Generative AI Hub?
------------------------------------------------------------
Retrieved sources:
  • ai_core_genai_hub.txt  (relevance: 0.629)
  • sap_joule.txt          (relevance: 0.511)
  • sap_joule.txt          (relevance: 0.456)

Generated answer:
Joule is built on top of SAP's Generative AI Hub and AI Core infrastructure...
```

## Project structure

```
sap-rag-assistant/
├── app.py              # retrieval + generation pipeline
├── docs/                # knowledge base (7 short SAP BTP concept docs)
├── requirements.txt
└── README.md
```

## Extending this

- Swap `docs/*.txt` for real SAP documentation or a support-ticket corpus.
- Swap the `Retriever` for SAP HANA Cloud Vector Engine + AI Core embeddings.
- Swap the CLI for a small Flask/CAP endpoint to make it a callable service.
- Add re-ranking or hybrid (keyword + vector) search for larger corpora.
