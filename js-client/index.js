/**
 * JavaScript client for the RAGWare API.
 *
 * @typedef {Object} ContextChunk
 * @property {string} chunk_text
 * @property {number} similarity
 * @property {number|null} [chunk_id]
 *
 * @typedef {Object} QueryResponse
 * @property {boolean} success
 * @property {string} response
 * @property {string} query
 * @property {ContextChunk[]|null} [context]
 * @property {string|null} [error]
 *
 * @typedef {Object} QueryOptions
 * @property {number} [topK=3] Number of relevant chunks to retrieve (1-10).
 * @property {boolean} [returnContext=false] Whether to return the retrieved context chunks.
 * @property {AbortSignal} [signal] Optional abort signal for the request.
 */

export class RAGWareError extends Error {
  /**
   * @param {string} message
   * @param {number} [status]
   * @param {unknown} [body]
   */
  constructor(message, status, body) {
    super(message);
    this.name = "RAGWareError";
    this.status = status;
    this.body = body;
  }
}

export class RAGWareClient {
  /**
   * @param {Object} [options]
   * @param {string} [options.baseUrl="http://localhost:8000"] Base URL of the RAGWare API.
   * @param {typeof fetch} [options.fetch] Custom fetch implementation.
   * @param {Record<string, string>} [options.headers] Extra headers sent with every request.
   */
  constructor({ baseUrl = "http://localhost:8000", fetch: fetchImpl, headers = {} } = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.fetch = fetchImpl ?? globalThis.fetch;
    this.headers = { ...headers };

    if (typeof this.fetch !== "function") {
      throw new Error("No fetch implementation available; pass one via options.fetch");
    }
  }

  /**
   * Check API health.
   * @param {Object} [options]
   * @param {AbortSignal} [options.signal]
   * @returns {Promise<{ status: string }>}
   */
  health({ signal } = {}) {
    return this._request("/health", { method: "GET", signal });
  }

  /**
   * Fetch API metadata and example queries.
   * @param {Object} [options]
   * @param {AbortSignal} [options.signal]
   * @returns {Promise<Object>}
   */
  root({ signal } = {}) {
    return this._request("/", { method: "GET", signal });
  }

  /**
   * Ask a natural-language question about the coffee sales data.
   * @param {string} query
   * @param {QueryOptions} [options]
   * @returns {Promise<QueryResponse>}
   */
  query(query, { topK = 3, returnContext = false, signal } = {}) {
    if (typeof query !== "string" || query.trim() === "") {
      throw new TypeError("query must be a non-empty string");
    }

    return this._request("/query", {
      method: "POST",
      signal,
      body: JSON.stringify({
        query,
        top_k: topK,
        return_context: returnContext,
      }),
    });
  }

  /**
   * @param {string} path
   * @param {{ method: string, body?: string, signal?: AbortSignal }} init
   * @returns {Promise<any>}
   */
  async _request(path, { method, body, signal }) {
    const headers = { Accept: "application/json", ...this.headers };
    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
    }

    const response = await this.fetch(`${this.baseUrl}${path}`, {
      method,
      headers,
      body,
      signal,
    });

    const text = await response.text();
    let payload = null;
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch {
        payload = text;
      }
    }

    if (!response.ok) {
      const detail =
        payload && typeof payload === "object" && "detail" in payload
          ? payload.detail
          : payload || response.statusText;
      throw new RAGWareError(
        `RAGWare request failed (${response.status}): ${detail}`,
        response.status,
        payload
      );
    }

    return payload;
  }
}

export default RAGWareClient;
