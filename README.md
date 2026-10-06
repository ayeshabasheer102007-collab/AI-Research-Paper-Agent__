# 🔬 AI Research Agent

> An advanced AI-powered research assistant that discovers, retrieves, analyzes, compares, and synthesizes academic research papers with evidence-backed citations.

The **AI Research Agent** goes beyond traditional RAG-based chatbots.

Instead of simply answering questions from a collection of documents, it performs a multi-step research workflow:

```text
Research Question
       ↓
Query Understanding
       ↓
Paper Discovery
       ↓
PDF Processing
       ↓
Metadata Extraction
       ↓
Semantic Chunking
       ↓
Hybrid Retrieval
       ↓
Reranking
       ↓
Evidence Extraction
       ↓
Paper Comparison
       ↓
Contradiction Detection
       ↓
Research Gap Detection
       ↓
Research Directions
       ↓
Cited Research Report
```

---

## 🚀 Why This Project?

Finding and understanding research literature manually can be time-consuming.

A researcher may need to:

- Search hundreds of papers
- Read abstracts and methodology sections
- Compare different approaches
- Track citations and references
- Identify conflicting findings
- Find limitations in existing work
- Discover unexplored research gaps

The **AI Research Agent** automates much of this workflow.

For example, a user can ask:

> **"Compare the approaches used for image segmentation from 2020–2025 and identify the major research gaps."**

The agent can:

1. Understand the research question
2. Generate search queries
3. Find relevant papers
4. Process paper content
5. Retrieve relevant evidence
6. Compare methodologies
7. Identify contradictions
8. Detect research gaps
9. Suggest future research directions
10. Generate a cited research report

---

# ✨ Features

## 📄 Paper Ingestion

Upload academic PDFs and automatically extract:

- Title
- Authors
- Abstract
- Sections
- Paragraphs
- References
- Page numbers
- Research content

---

## 🔎 Hybrid Search

The system combines multiple retrieval strategies.

```text
                User Query
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
    Semantic Search         BM25
          │                   │
          └─────────┬─────────┘
                    ↓
             Result Fusion
                    ↓
                Reranking
                    ↓
             Relevant Evidence
```

Instead of depending entirely on vector similarity, the system combines:

- Semantic search
- Keyword search
- BM25
- Metadata filtering
- Vector similarity
- Result fusion
- Reranking

---

## 🧠 AI Research Agent

The research agent can plan and execute a research workflow.

Example:

```text
User Question
      ↓
Research Planner
      ↓
Search Strategy
      ↓
Paper Retrieval
      ↓
Evidence Collection
      ↓
Analysis
      ↓
Final Report
```

The agent can determine what information is needed before generating the final answer.

---

# 📊 Paper Comparison

The system can compare papers across multiple dimensions.

Example:

| Paper | Method | Dataset | Metric | Result | Limitation |
|---|---|---|---|---|---|
| Paper A | CNN | Dataset X | Dice | 91.2% | High compute |
| Paper B | Transformer | Dataset X | Dice | 93.1% | Large model |
| Paper C | Hybrid | Dataset Y | IoU | 89.7% | Limited data |

Comparison dimensions can include:

- Method
- Architecture
- Dataset
- Training strategy
- Evaluation metrics
- Results
- Computational requirements
- Advantages
- Limitations

---

# ⚔️ Contradiction Detection

Research papers sometimes reach different conclusions.

The system attempts to identify potential disagreements.

Example:

```text
Paper A:
Method X improves segmentation performance.

Paper B:
Method X provides no significant improvement.
```

The system investigates whether the difference may be caused by:

- Different datasets
- Different evaluation metrics
- Different experimental settings
- Different baselines
- Different model configurations

Contradictions are always linked back to supporting evidence.

---

# 🕳️ Research Gap Detection

The system analyzes existing literature to identify potential gaps.

Possible gaps include:

- Underexplored datasets
- Missing experiments
- Weak baselines
- Computational limitations
- Reproducibility issues
- Inconsistent findings
- Lack of real-world validation
- Underexplored domains
- Missing comparisons

Example:

```text
Research Gap

Existing transformer-based models achieve strong
performance but often require substantial computational
resources.

Potential Direction

Develop lightweight hybrid architectures suitable for
resource-constrained environments.
```

AI-generated research directions are clearly distinguished from established findings.

---

# 🔗 Citation Graph

The project can model relationships between research papers.

```text
Paper A
   │
   ├──── cites ────→ Paper B
   │                    │
   │                    └──── cites ────→ Paper C
   │
   └──── cites ────→ Paper D
```

The citation graph can be used to understand:

- Influential papers
- Research evolution
- Citation relationships
- Research clusters
- Foundational work
- Related research

---

# 🧩 Knowledge Graph

The system can represent research entities as a knowledge graph.

### Nodes

```text
Paper
Author
Method
Dataset
Metric
Task
Conference
Institution
```

### Relationships

```text
AUTHORED_BY
USES_METHOD
EVALUATED_ON
USES_METRIC
CITES
EXTENDS
CONTRADICTS
PUBLISHED_AT
```

This allows higher-level research questions such as:

> Which datasets are most commonly used for image segmentation?

> Which researchers work on transformer-based segmentation?

> Which papers introduced this method?

> Which papers contradict this finding?

---

# 🏗️ Architecture

```text
                    ┌───────────────────┐
                    │   User Question   │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ Research Planner  │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ Paper Discovery   │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ PDF Processing    │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ Chunking          │
                    └─────────┬─────────┘
                              ↓
             ┌────────────────┴────────────────┐
             ↓                                 ↓
      Semantic Search                        BM25
             │                                 │
             └────────────────┬────────────────┘
                              ↓
                       Hybrid Retrieval
                              ↓
                         Reranking
                              ↓
                      Evidence Extraction
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         Comparison     Contradictions    Research Gaps
              │               │               │
              └───────────────┼───────────────┘
                              ↓
                    Research Directions
                              ↓
                     Citation Generator
                              ↓
                    Final Research Report
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

## AI / ML

- Large Language Models
- Sentence Transformers
- Semantic Embeddings
- BM25
- Cross-Encoder Reranking
- RAG
- Agentic AI

## Vector Search

- Qdrant

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Infrastructure

- Docker
- Docker Compose
- PostgreSQL
- Qdrant

---

# 📁 Project Structure

```text
ai-research-agent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── ingestion/
│   │   ├── retrieval/
│   │   ├── agents/
│   │   ├── analysis/
│   │   └── services/
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── Dockerfile
│
├── data/
│   ├── papers/
│   └── processed/
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-research-agent.git

cd ai-research-agent
```

---

## 2. Create environment variables

Copy:

```bash
cp .env.example .env
```

Configure your environment:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/research

QDRANT_URL=http://qdrant:6333

QDRANT_COLLECTION=research_papers

OPENAI_API_KEY=your_api_key

LLM_MODEL=gpt-4o-mini

EMBEDDING_MODEL=all-MiniLM-L6-v2
```

Never commit your real API keys to Git.

---

# 🐳 Running with Docker

Start the complete application:

```bash
docker compose up --build
```

The services will start:

```text
Frontend
   ↓
Backend
   ↓
PostgreSQL
   ↓
Qdrant
```

---

# 🌐 Application

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

# 📄 Upload a Research Paper

Example API request:

```bash
curl -X POST \
  http://localhost:8000/api/papers/upload \
  -F "file=@research-paper.pdf"
```

The pipeline processes:

```text
PDF
 ↓
Text Extraction
 ↓
Page Detection
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Database
```

---

# 🔍 Search Papers

Example:

```bash
curl "http://localhost:8000/api/search/?q=transformer%20image%20segmentation"
```

The search pipeline:

```text
Query
 ↓
Embedding
 ↓
Vector Search
 ↓
Keyword Search
 ↓
Fusion
 ↓
Reranking
 ↓
Top Evidence
```

---

# 🤖 Start a Research Task

Example:

```bash
curl -X POST \
  http://localhost:8000/api/research/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Compare CNN and transformer approaches for image segmentation from 2020 to 2025."
  }'
```

The agent generates a research workflow and retrieves relevant evidence.

---

# 🔬 Example Research Workflow

### User

```text
Compare CNN and transformer approaches
for medical image segmentation from 2020–2025.
```

### Agent

```text
Step 1
Understand research question

Step 2
Identify:
- CNN
- Transformer
- Medical image segmentation
- 2020–2025

Step 3
Generate search queries

Step 4
Retrieve relevant papers

Step 5
Rerank evidence

Step 6
Compare methodologies

Step 7
Analyze results

Step 8
Detect contradictions

Step 9
Identify research gaps

Step 10
Generate future research directions

Step 11
Generate cited report
```

---

# 📚 Evidence-Based Generation

The system follows an evidence-first approach.

```text
Retrieved Evidence
       ↓
Evidence Validation
       ↓
LLM
       ↓
Generated Claim
       ↓
Citation
```

Important rules:

- Never fabricate papers
- Never fabricate citations
- Never invent experimental results
- Do not treat unsupported assumptions as facts
- Clearly distinguish evidence from inference
- Report when evidence is insufficient

---

# 🧪 Evaluation

A major goal of this project is to evaluate the AI system rather than only demonstrate it.

Retrieval metrics:

```text
Recall@K
Precision@K
MRR
NDCG
```

Generation metrics:

```text
Citation Accuracy
Answer Faithfulness
Evidence Relevance
Groundedness
```

Example evaluation:

```text
                    Before      After
----------------------------------------
Recall@10            0.71       0.89
MRR                   0.62       0.81
NDCG@10               0.67       0.86
Citation Accuracy     0.78       0.94
```

These values are examples only; actual benchmark results should be generated by the project's evaluation pipeline.

---

# 🗺️ Development Roadmap

## Phase 1 — Foundation

- [x] Project structure
- [x] FastAPI backend
- [x] Next.js frontend
- [x] Docker
- [x] PostgreSQL
- [x] Qdrant

## Phase 2 — Paper Ingestion

- [ ] PDF upload
- [ ] PDF parsing
- [ ] Metadata extraction
- [ ] Section detection
- [ ] Reference extraction
- [ ] Semantic chunking

## Phase 3 — Retrieval

- [ ] Embedding generation
- [ ] Vector search
- [ ] BM25
- [ ] Hybrid retrieval
- [ ] Reciprocal Rank Fusion
- [ ] Cross-encoder reranking

## Phase 4 — Research Agent

- [ ] Query understanding
- [ ] Research planning
- [ ] Query expansion
- [ ] Agent tools
- [ ] Evidence extraction
- [ ] Cited answer generation

## Phase 5 — Research Intelligence

- [ ] Paper comparison
- [ ] Contradiction detection
- [ ] Research gap detection
- [ ] Research direction generation

## Phase 6 — Knowledge Graph

- [ ] Citation graph
- [ ] Knowledge graph
- [ ] Relationship extraction
- [ ] Interactive graph visualization

## Phase 7 — Evaluation

- [ ] Retrieval benchmark
- [ ] Citation evaluation
- [ ] Faithfulness evaluation
- [ ] End-to-end evaluation
- [ ] Performance optimization

---

# 🎯 Future Improvements

Potential future features include:

- arXiv integration
- Semantic Scholar integration
- Crossref integration
- DOI lookup
- Automatic paper discovery
- Multi-agent research workflows
- Research timeline visualization
- Author collaboration networks
- Topic clustering
- Automatic literature reviews
- Automatic survey generation
- Research trend analysis
- Paper recommendation
- Experiment tracking
- LaTeX report generation
- Export to PDF
- BibTeX generation
- Zotero integration

---

# 🔐 Reliability Principles

The AI Research Agent is designed around several principles:

### Groundedness

Answers should be based on retrieved research evidence.

### Transparency

Claims should be traceable to their sources.

### Reproducibility

Research workflows should be reproducible.

### Uncertainty

The system should acknowledge insufficient evidence.

### No fabricated citations

A citation should correspond to an actual source available to the system.

---

# 📈 Project Goals

The long-term goal is to transform the system from a simple:

```text
PDF → RAG → Chatbot
```

into:

```text
Research Question
       ↓
Research Planning
       ↓
Autonomous Literature Search
       ↓
Evidence Retrieval
       ↓
Research Synthesis
       ↓
Contradiction Analysis
       ↓
Research Gap Discovery
       ↓
Novel Research Directions
       ↓
Cited Literature Review
```

---

# 💡 Example Questions

The system should eventually support questions such as:

```text
What are the major approaches to image segmentation
between 2020 and 2025?
```

```text
Compare CNN and transformer architectures
for medical image segmentation.
```

```text
Which datasets are most commonly used
for medical image segmentation?
```

```text
Which papers report conflicting results
about transformer-based segmentation?
```

```text
What are the major limitations of current
medical image segmentation methods?
```

```text
What research gaps remain unexplored?
```

```text
Based on existing literature, what are
promising future research directions?
```

---

# 👨‍💻 Author

**Ayesha Basheer**

AI/ML Engineer | Researcher

GitHub: `https://github.com/your-username`

LinkedIn: `https://linkedin.com/in/your-profile`

---

# ⭐ Contributing

Contributions are welcome.

```bash
git checkout -b feature/new-feature

git commit -m "Add new feature"

git push origin feature/new-feature
```

Then open a pull request.

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Project Vision

> **Build an AI research assistant that doesn't just retrieve papers — it understands the research landscape.**

The ultimate goal is to help researchers move from:

```text
"What has already been done?"
```

to:

```text
"What is missing?"

        ↓

"Why is it missing?"

        ↓

"What can we investigate next?"
```

**AI Research Agent — From Literature Search to Research Discovery.**
