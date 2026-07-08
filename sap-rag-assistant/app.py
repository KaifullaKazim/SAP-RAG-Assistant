"""
SAP BTP Knowledge Assistant - Simple RAG using TF-IDF + Groq LLM

Architecture:
1. Load documents
2. Build TF-IDF index
3. Retrieve Top-K chunks
4. Build prompt
5. Send to Groq
"""
" all the imports here"
import os
import glob
import sys
from dataclasses import dataclass  


from dotenv import load_dotenv
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

TOP_K = int(os.getenv("TOP_K", 3))

MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------------------------
# Data Class
# -------------------------------------------------

@dataclass
class Chunk:
    text: str
    source: str


# -------------------------------------------------
# Load Documents
# -------------------------------------------------

def load_chunks(docs_dir=DOCS_DIR):

    chunks = []

    txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))

    for path in sorted(txt_files):

        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        source = os.path.basename(path)

        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        for paragraph in paragraphs:

            chunks.append(
                Chunk(
                    text=paragraph,
                    source=source
                )
            )

    return chunks


# -------------------------------------------------
# Retriever
# -------------------------------------------------

class Retriever:

    def __init__(self, chunks):

        self.chunks = chunks

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.matrix = self.vectorizer.fit_transform(
            [chunk.text for chunk in chunks]
        )

    def retrieve(self, query, k=TOP_K):

        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.matrix
        )[0]

        ranked = sorted(
            zip(self.chunks, similarities),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            item
            for item in ranked[:k]
            if item[1] > 0
        ]


# -------------------------------------------------
# Prompt Builder
# -------------------------------------------------

def build_prompt(query, retrieved):

    context = "\n\n".join(

        f"[Source: {chunk.source}]\n{chunk.text}"

        for chunk, _ in retrieved
    )

    return f"""
You are an SAP BTP Knowledge Assistant.

Use ONLY the supplied context.

If the answer cannot be found in the context, reply with:

"I don't have enough information in my knowledge base."

Do not hallucinate.

==========================
CONTEXT
==========================

{context}

==========================
QUESTION
==========================

{query}

==========================
ANSWER
==========================
"""


# -------------------------------------------------
# Groq Generation
# -------------------------------------------------

def generate(prompt):

    if not API_KEY:

        return (
            "\nERROR:\n"
            "GROQ_API_KEY not found.\n"
            "Please add it to your .env file."
        )

    try:

        client = Groq(api_key=API_KEY)

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=500,
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"\nGroq Error:\n{e}"


# -------------------------------------------------
# Ask Question
# -------------------------------------------------

def answer(query, retriever):

    retrieved = retriever.retrieve(query)

    print("\n" + "=" * 70)

    print("Question:")
    print(query)

    print("=" * 70)

    if not retrieved:

        print("\nNo relevant context found.")

        return

    print("\nRetrieved Sources:\n")

    for chunk, score in retrieved:

        print(
            f"• {chunk.source}"
            f" (Similarity: {score:.3f})"
        )

    prompt = build_prompt(query, retrieved)

    print("\nGenerating Answer...\n")

    response = generate(prompt)

    print(response)

    print()


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    chunks = load_chunks()

    if not chunks:

        print(f"No documents found inside:\n{DOCS_DIR}")

        sys.exit(1)

    print("=" * 70)
    print("SAP BTP Knowledge Assistant")
    print("=" * 70)

    print(
        f"\nIndexed {len(chunks)} chunks from "
        f"{len(glob.glob(os.path.join(DOCS_DIR,'*.txt')))} documents."
    )

    print(f"Model : {MODEL}")
    print(f"Top K : {TOP_K}")

    retriever = Retriever(chunks)

    if len(sys.argv) > 1:

        answer(
            " ".join(sys.argv[1:]),
            retriever
        )

        return

    print("\nType your question.")
    print("Type 'quit' to exit.\n")

    while True:

        query = input("> ").strip()

        if query.lower() in ["quit", "exit"]:

            print("\nGoodbye!")

            break

        if query:

            answer(query, retriever)


if __name__ == "__main__":
    main()