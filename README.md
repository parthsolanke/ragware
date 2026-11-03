# RAGWare

Retrieval-Augmented Generation (RAG)

## Prerequisites

- Python >= 3.13
- An OpenAI API key set as `OPENAI_API_KEY` (put it in a `.env` file at the project root)

## Quick install

Recommended (Poetry):

1. Install dependencies:

   poetry install

2. Run the API:

   ./run.sh

Alternatively (pip):

1. Create and activate a virtual environment:

   python -m venv .venv
   source .venv/bin/activate

2. Install the package in editable mode and run:

   pip install -e .
   python -m src.main

## JavaScript client

A dependency-free client is available in `js-client/` (Node >= 18):

```js
import { RAGWareClient } from "./js-client/index.js";

const client = new RAGWareClient({ baseUrl: "http://localhost:8000" });

const result = await client.query("Which coffee type is most popular?", {
  topK: 3,
  returnContext: true,
});

console.log(result.response);
```

## Notes

- The API server defaults to host `0.0.0.0` and port `8000` (see `src/config.py`).
- `test_queries.sh` posts to `http://localhost:8001` by default — either update the `API_URL` in that script or run the service on port `8001` before using it.
- `test_queries.sh` expects `jq` and `curl` to be available.

## License

MIT
