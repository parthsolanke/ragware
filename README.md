# RAGware ( Maybe develop in Go for Performance & Concurrency and also try to integrate PostgreSQL )
A simple plug-in modular library for developing RAG agents 🤖 and semantic search applications.

### RAGware GitHub Repository Structure

```
RAGware/
│
├── docs/
│   └── index.md                 # Main documentation file
│
├── ragware/
│   ├── semantic_search/
│   │   ├── __init__.py          # Initialization for semantic search module
│   │   ├── indexer.py           # Code for document indexing
│   │   ├── searcher.py          # Code for semantic search functionalities
│   │   └── api.py               # API endpoints for search operations
│   │
│   ├── rag_framework/
│   │   ├── __init__.py          # Initialization for RAG framework module
│   │   ├── generator.py         # Integration with generative model (LLM)
│   │   ├── utils.py             # Utility functions for RAG tasks
│   │   └── api.py               # API endpoints for RAG operations
│   │
│   ├── vector_database/
│   │   ├── __init__.py          # Initialization for vector database module
│   │   ├── storage.py           # Schema and storage operations for vectors
│   │   └── integration.py       # Integration with Elasticsearch
│   │
│   │
│   ├── client_llm/
│   │   ├── __init__.py          # Initialization for LLM client module
│   │   ├── client.py            # Client for communicating with LLM (e.g., GPT-3)
│   │   └── utils.py             # Utility functions for LLM interactions
│   │
│   ├── function_tools/
│   │   ├── __init__.py          # Initialization for function tools module
│   │   ├── function_caller.py   # Utility for calling functions within RAGware
│   │   └── utils.py             # General utility functions
│   │
│   ├── data_management/
│   │   ├── __init__.py          # Initialization for data management module
│   │   ├── file_manager.py      # File management and persistence
│   │   └── cache_manager.py     # Caching strategies using Redis
│   │
│   └── tests/
│       ├── test_semantic_search.py    # Unit tests for semantic search module
│       ├── test_rag_framework.py      # Unit tests for RAG framework module
│       ├── test_vector_database.py    # Unit tests for vector database module
│       ├── test_client_llm.py         # Unit tests for LLM client module
│       ├── test_function_tools.py     # Unit tests for function tools module
│       ├── test_data_management.py    # Unit tests for data management module
│       └── conftest.py                # Configuration for testing
│
├── requirements.txt          # Dependencies for RAGware
├── README.md                 # Overview and setup instructions
└── LICENSE                   # License information
```

### Explanation:

1. **docs/**: Contains documentation files, including an index.md file for main documentation content.

2. **src/**: Source code directory containing modular components of RAGware.

   - **semantic_search/**: Module for semantic search functionalities.
   - **rag_framework/**: Module integrating semantic search with generative models for RAG tasks.
   - **vector_database/**: Module for storing and retrieving embeddings or vectors.
   - **client_llm/**: Module for interfacing with large language models (LLMs) like GPT-3.
   - **function_tools/**: Module providing utilities for function calling within RAGware.
   - **data_management/**: Module handling file management, persistence, and caching.
   - **tests/**: Directory containing unit tests for each module and a conftest.py for test configuration.
