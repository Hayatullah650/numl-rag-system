
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const suggestions = [
  {
    category: "Admissions",
    question: "What are the admission criteria for computing programs?"
  },
  {
    category: "Fees",
    question: "What is NUML's fee refund policy?"
  },
  {
    category: "Student policies",
    question: "What does the student handbook say about leave?"
  },
  {
    category: "Examinations",
    question: "What are the examination rules at NUML?"
  }
];

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [logoError, setLogoError] = useState(false);

  async function askQuestion(value = question) {
    const prompt = value.trim();
    if (!prompt || loading) return;

    setQuestion(prompt);
    setAnswer("");
    setSources([]);
    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: prompt })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to get an answer.");
      }

      setAnswer(data.answer || "No answer was returned.");
      setSources(data.sources || []);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to NUML Assistant. Check that the backend is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    askQuestion();
  }

  function startNewQuestion() {
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  }

  return (
    <div className="portal">
      <aside className="sidebar">
        <a className="brand" href="https://www.numl.edu.pk/" target="_blank" rel="noreferrer">
          {!logoError ? (
            <img
              className="brand-logo"
              src="/numl-logo.png"
              alt="NUML logo"
              onError={() => setLogoError(true)}
            />
          ) : (
            <span className="brand-fallback">NUML</span>
          )}
          <span className="brand-copy">
            <strong>NUML</strong>
            <small>Student Information</small>
          </span>
        </a>

        <div className="nav-label">WORKSPACE</div>
        <button className="nav-item active" onClick={startNewQuestion}>
          <span className="nav-symbol">⌂</span>
          AI Assistant
        </button>
        <a className="nav-item" href="https://www.numl.edu.pk/admission/advertisement" target="_blank" rel="noreferrer">
          <span className="nav-symbol">↗</span>
          Admissions
        </a>
        <a className="nav-item" href="https://www.numl.edu.pk/main/cms" target="_blank" rel="noreferrer">
          <span className="nav-symbol">▤</span>
          Student portal
        </a>
        <a className="nav-item" href="https://www.numl.edu.pk/" target="_blank" rel="noreferrer">
          <span className="nav-symbol">◎</span>
          Official website
        </a>

        <div className="sidebar-bottom">
          <div className="help-card">
            <span className="help-mark">i</span>
            <strong>Need official help?</strong>
            <p>Confirm important matters with the relevant university office.</p>
            <a href="https://www.numl.edu.pk/" target="_blank" rel="noreferrer">
              Visit NUML website <span>↗</span>
            </a>
          </div>
          <div className="sidebar-footer">National University of Modern Languages</div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Student Services</span>
            <span className="crumb-divider">/</span>
            <strong>AI Assistant</strong>
          </div>
          <a className="official-link" href="https://www.numl.edu.pk/" target="_blank" rel="noreferrer">
            <span className="status-dot" />
            Official NUML website
            <span>↗</span>
          </a>
        </header>

        <div className="content">
          <section className="welcome">
            <div className="welcome-tag">
              <span className="tag-dot" />
              UNIVERSITY KNOWLEDGE ASSISTANT
            </div>
            <h1>Find the answers<br />you need at <span>NUML.</span></h1>
            <p>
              Ask about admissions, fee policies, examinations and student
              regulations. Get answers grounded in university documents.
            </p>
          </section>

          <section className="question-panel">
            <form onSubmit={handleSubmit}>
              <label htmlFor="question">What would you like to know?</label>
              <textarea
                id="question"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Ask a question about NUML..."
                rows={3}
                maxLength={2000}
                required
              />
              <div className="question-toolbar">
                <span className="input-hint">
                  Answers are generated from available NUML documents.
                </span>
                <button className="ask-button" type="submit" disabled={loading || !question.trim()}>
                  {loading ? "Searching..." : "Ask NUML"}
                  {!loading && <span>→</span>}
                </button>
              </div>
            </form>
          </section>

          {!answer && !loading && !error && (
            <section className="suggestions">
              <div className="section-heading">
                <div>
                  <h2>Explore common questions</h2>
                  <p>Choose a topic to get started.</p>
                </div>
                <span className="suggestion-count">04 TOPICS</span>
              </div>

              <div className="suggestion-grid">
                {suggestions.map((item, index) => (
                  <button
                    className="suggestion-card"
                    key={item.category}
                    onClick={() => askQuestion(item.question)}
                  >
                    <span className={`suggestion-icon icon-${index + 1}`}>
                      {["01", "02", "03", "04"][index]}
                    </span>
                    <span className="suggestion-category">{item.category}</span>
                    <strong>{item.question}</strong>
                    <span className="suggestion-arrow">↗</span>
                  </button>
                ))}
              </div>
            </section>
          )}

          {loading && (
            <section className="response-panel loading-panel">
              <div className="loading-line" />
              <h2>Searching university documents</h2>
              <p>Finding relevant passages and preparing your answer...</p>
            </section>
          )}

          {error && (
            <section className="response-panel error-panel">
              <h2>We couldn't complete your request</h2>
              <p>{error}</p>
              <button className="secondary-button" onClick={() => askQuestion()}>
                Try again
              </button>
            </section>
          )}

          {answer && !loading && (
            <section className="response-panel">
              <div className="answer-heading">
                <div>
                  <span className="response-eyebrow">YOUR RESPONSE</span>
                  <h2>Here's what we found</h2>
                </div>
                <button className="new-question" onClick={startNewQuestion}>
                  + New question
                </button>
              </div>

              <div className="asked-question">
                <span>YOUR QUESTION</span>
                <p>{question}</p>
              </div>

              <div className="answer-body">
                <div className="answer-mark">N</div>
                <div className="answer-copy">
                  <h3>NUML Assistant</h3>
                  <p className="answer-text">{answer}</p>
                </div>
              </div>

              <div className="source-section">
                <div className="source-heading">
                  <div>
                    <h3>Retrieved documents</h3>
                    <p>References used to prepare this response</p>
                  </div>
                  <span className="source-count">{sources.length} SOURCES</span>
                </div>

                {sources.length ? (
                  <div className="source-list">
                    {sources.map((source, index) => (
                      <div className="source-row" key={`${source.source}-${source.page}-${index}`}>
                        <div className="file-mark">PDF</div>
                        <div className="source-info">
                          <strong>{source.source}</strong>
                          <span>NUML document</span>
                        </div>
                        <span className="page-label">Page {source.page}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="no-sources">No source details were returned.</p>
                )}
              </div>

              <p className="answer-disclaimer">
                Verify important policies with the relevant NUML office.
                Retrieved sources are references, not a guarantee that every
                generated claim is fully supported.
              </p>
            </section>
          )}

          <footer className="main-footer">
            <span>NUML · Student Information Assistant</span>
            <span>Powered by university documents and hayat Ullah</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
