import os
import tempfile
import requests
import streamlit as st

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 5


# ============================================================
# STREAMLIT PAGE
# ============================================================

st.set_page_config(
    page_title="AI Research Paper Agent",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">📚 AI Research Paper Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Read, search, understand and analyze research papers
    using RAG + FAISS + Ollama
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "chunk_metadata" not in st.session_state:
    st.session_state.chunk_metadata = []

if "index" not in st.session_state:
    st.session_state.index = None

if "papers" not in st.session_state:
    st.session_state.papers = []

if "processed" not in st.session_state:
    st.session_state.processed = False


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    return model


# ============================================================
# CHECK OLLAMA
# ============================================================

def check_ollama():

    try:

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )

        return response.status_code == 200

    except Exception:

        return False


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    pages = []

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getbuffer()
        )

        temp_path = temp_file.name

    try:

        reader = PdfReader(temp_path)

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text()

            if text:

                pages.append(
                    {
                        "text": text,
                        "page": page_number,
                        "source": uploaded_file.name
                    }
                )

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)

    return pages


# ============================================================
# TEXT CHUNKING
# ============================================================

def create_chunks(pages):

    all_chunks = []

    metadata = []

    chunk_size = 1000
    overlap = 200

    for page in pages:

        text = page["text"]

        # Clean whitespace
        text = " ".join(
            text.split()
        )

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            if chunk.strip():

                all_chunks.append(
                    chunk
                )

                metadata.append(
                    {
                        "source": page["source"],
                        "page": page["page"]
                    }
                )

            start += (
                chunk_size - overlap
            )

    return all_chunks, metadata


# ============================================================
# CREATE VECTOR DATABASE
# ============================================================

def create_vector_database(chunks):

    model = load_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    return index


# ============================================================
# RETRIEVE RELEVANT CHUNKS
# ============================================================

def retrieve_chunks(
    question,
    chunks,
    metadata,
    index,
    top_k=5
):

    model = load_embedding_model()

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(
        question_embedding,
        min(top_k, len(chunks))
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx == -1:
            continue

        results.append(
            {
                "text": chunks[idx],
                "source": metadata[idx]["source"],
                "page": metadata[idx]["page"],
                "score": float(score)
            }
        )

    return results


# ============================================================
# SEND PROMPT TO OLLAMA
# ============================================================

def ask_ollama(prompt):

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# ============================================================
# CREATE RESEARCH CONTEXT
# ============================================================

def build_context(results):

    context = ""

    for i, result in enumerate(results):

        context += f"""

SOURCE {i + 1}

Paper: {result["source"]}
Page: {result["page"]}

Content:
{result["text"]}

-----------------------------------------
"""

    return context


# ============================================================
# RESEARCH QUESTION
# ============================================================

def answer_question(
    question,
    results
):

    context = build_context(results)

    prompt = f"""
You are an AI Research Paper Assistant.

Your task is to answer the user's question using
ONLY the research paper information provided below.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not use information that is not in the context.
3. If the answer is not available, say:
   "The answer was not found in the uploaded papers."
4. Explain your answer clearly.
5. Mention the paper and page for important claims.
6. Separate evidence from your interpretation.

USER QUESTION:

{question}

RESEARCH PAPER CONTEXT:

{context}

Return the answer using this structure:

### Answer

Give a clear and direct answer.

### Evidence

Explain the evidence from the papers.

Use citations like:

[Source: paper.pdf, Page: 5]

### Key Insights

- Important insight 1
- Important insight 2
- Important insight 3

### Research Context

Explain how the answer relates to the research.
"""

    return ask_ollama(prompt)


# ============================================================
# SUMMARIZE PAPER
# ============================================================

def summarize_papers(results):

    context = build_context(results)

    prompt = f"""
You are an academic research assistant.

Summarize the research paper content below.

Do not invent information.

Provide:

### 1. Overview

### 2. Research Problem

### 3. Methodology

### 4. Dataset

### 5. Results

### 6. Main Contributions

### 7. Limitations

### 8. Future Work

### 9. Key Takeaways

For important facts include:

[Source: paper.pdf, Page: X]

RESEARCH PAPER CONTENT:

{context}
"""

    return ask_ollama(prompt)


# ============================================================
# COMPARE PAPERS
# ============================================================

def compare_papers(results):

    context = build_context(results)

    prompt = f"""
You are an expert research analyst.

Compare the uploaded research papers using ONLY
the information provided below.

Do not invent missing information.

Compare:

1. Research problem
2. Methodology
3. Algorithms/models
4. Dataset
5. Evaluation metrics
6. Results
7. Advantages
8. Limitations
9. Future work

Create a markdown comparison table.

Then provide:

### Overall Comparison

### Strongest Approach

### Research Gaps

Use citations where possible.

RESEARCH PAPERS:

{context}
"""

    return ask_ollama(prompt)


# ============================================================
# RESEARCH INSIGHTS
# ============================================================

def research_insights(results):

    context = build_context(results)

    prompt = f"""
You are an AI research analyst.

Analyze the research papers below.

Identify:

### Research Trends

### Important Findings

### Common Methodologies

### Common Datasets

### Research Gaps

### Limitations

### Future Research Opportunities

### Potential Research Ideas

Do not invent facts.

Clearly identify when something is an analytical
conclusion rather than explicitly stated in a paper.

Include paper/page citations when possible.

RESEARCH PAPERS:

{context}
"""

    return ask_ollama(prompt)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 Upload Research Papers")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if check_ollama():

        st.success(
            "🟢 Ollama is running"
        )

    else:

        st.error(
            "🔴 Ollama is not running"
        )

        st.info(
            "Start Ollama and try again."
        )

    st.divider()

    st.write(
        f"AI Model: **{OLLAMA_MODEL}**"
    )

    st.write(
        f"Embedding Model: **{EMBEDDING_MODEL}**"
    )


# ============================================================
# PROCESS PAPERS
# ============================================================

if st.sidebar.button(
    "🚀 Process Papers",
    use_container_width=True
):

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF."
        )

    elif not check_ollama():

        st.error(
            "Ollama is not running."
        )

    else:

        try:

            all_pages = []

            paper_names = []

            progress = st.progress(0)

            total = len(
                uploaded_files
            )

            for i, file in enumerate(
                uploaded_files
            ):

                paper_names.append(
                    file.name
                )

                pages = extract_pdf_text(
                    file
                )

                all_pages.extend(
                    pages
                )

                progress.progress(
                    (i + 1) / total
                )

            if not all_pages:

                st.error(
                    "Could not extract text from the PDFs."
                )

            else:

                with st.spinner(
                    "Creating text chunks..."
                ):

                    chunks, metadata = (
                        create_chunks(
                            all_pages
                        )
                    )

                with st.spinner(
                    "Creating embeddings..."
                ):

                    vector_index = (
                        create_vector_database(
                            chunks
                        )
                    )

                st.session_state.chunks = (
                    chunks
                )

                st.session_state.chunk_metadata = (
                    metadata
                )

                st.session_state.index = (
                    vector_index
                )

                st.session_state.papers = (
                    paper_names
                )

                st.session_state.processed = True

                st.success(
                    "✅ Papers processed successfully!"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Papers",
                        len(paper_names)
                    )

                with col2:
                    st.metric(
                        "Pages",
                        len(all_pages)
                    )

                with col3:
                    st.metric(
                        "Chunks",
                        len(chunks)
                    )

        except Exception as e:

            st.error(
                f"Processing error: {e}"
            )


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💬 Ask Papers",
        "📝 Summarize",
        "📊 Compare",
        "💡 Insights"
    ]
)


# ============================================================
# TAB 1
# ============================================================

with tab1:

    st.header(
        "🔎 Ask Questions About Your Papers"
    )

    question = st.text_area(
        "Enter your question:",
        placeholder=(
            "Example: What is the main contribution "
            "of the paper?"
        ),
        height=100
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if not st.session_state.processed:

            st.warning(
                "Please upload and process a paper first."
            )

        elif not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "Searching the papers..."
                ):

                    results = retrieve_chunks(
                        question,
                        st.session_state.chunks,
                        st.session_state.chunk_metadata,
                        st.session_state.index,
                        TOP_K
                    )

                with st.spinner(
                    "Ollama is generating the answer..."
                ):

                    answer = answer_question(
                        question,
                        results
                    )

                st.subheader(
                    "🤖 AI Answer"
                )

                st.markdown(
                    answer
                )

                st.subheader(
                    "📚 Retrieved Sources"
                )

                for i, result in enumerate(
                    results
                ):

                    with st.expander(
                        f"📄 {i + 1}. "
                        f"{result['source']} "
                        f"— Page {result['page']}"
                    ):

                        st.write(
                            result["text"]
                        )

                        st.caption(
                            f"Similarity score: "
                            f"{result['score']:.3f}"
                        )

            except Exception as e:

                st.error(
                    f"AI error: {e}"
                )


# ============================================================
# TAB 2
# ============================================================

with tab2:

    st.header(
        "📝 Research Paper Summary"
    )

    if st.button(
        "Generate Summary",
        use_container_width=True
    ):

        if not st.session_state.processed:

            st.warning(
                "Please upload and process papers first."
            )

        else:

            try:

                with st.spinner(
                    "Generating summary..."
                ):

                    results = retrieve_chunks(
                        "abstract methodology "
                        "results conclusion limitations",
                        st.session_state.chunks,
                        st.session_state.chunk_metadata,
                        st.session_state.index,
                        10
                    )

                    summary = summarize_papers(
                        results
                    )

                st.markdown(
                    summary
                )

            except Exception as e:

                st.error(
                    f"Summary error: {e}"
                )


# ============================================================
# TAB 3
# ============================================================

with tab3:

    st.header(
        "📊 Compare Research Papers"
    )

    if st.button(
        "Compare Papers",
        use_container_width=True
    ):

        if not st.session_state.processed:

            st.warning(
                "Please upload and process papers first."
            )

        elif len(
            st.session_state.papers
        ) < 2:

            st.warning(
                "Please upload at least 2 research papers."
            )

        else:

            try:

                with st.spinner(
                    "Comparing papers..."
                ):

                    results = retrieve_chunks(
                        "methodology dataset "
                        "algorithm model results "
                        "limitations future work",
                        st.session_state.chunks,
                        st.session_state.chunk_metadata,
                        st.session_state.index,
                        10
                    )

                    comparison = compare_papers(
                        results
                    )

                st.markdown(
                    comparison
                )

            except Exception as e:

                st.error(
                    f"Comparison error: {e}"
                )


# ============================================================
# TAB 4
# ============================================================

with tab4:

    st.header(
        "💡 Research Insights"
    )

    if st.button(
        "Generate Insights",
        use_container_width=True
    ):

        if not st.session_state.processed:

            st.warning(
                "Please upload and process papers first."
            )

        else:

            try:

                with st.spinner(
                    "Analyzing research papers..."
                ):

                    results = retrieve_chunks(
                        "research findings trends "
                        "research gaps limitations "
                        "future research opportunities",
                        st.session_state.chunks,
                        st.session_state.chunk_metadata,
                        st.session_state.index,
                        10
                    )

                    insights = research_insights(
                        results
                    )

                st.markdown(
                    insights
                )

            except Exception as e:

                st.error(
                    f"Insight error: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Research Paper Agent | "
    "RAG + FAISS + Sentence Transformers + Ollama"
)