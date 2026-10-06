:root {
  --primary: #1d4ed8;
  --primary-dark: #153ea8;
  --danger: #dc2626;
  --success: #16a34a;
  --bg: #f3f6fb;
  --card: #ffffff;
  --text: #111827;
  --muted: #6b7280;
  --border: #dfe7f5;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
}

.hidden {
  display: none !important;
}

.auth-block {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #e0ecff, #f8fafc);
}

.auth-card {
  width: 420px;
  max-width: 90vw;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px 28px;
  box-shadow: 0 10px 30px rgba(29, 78, 216, 0.08);
}

.auth-card h1 {
  margin: 0 0 8px;
  text-align: center;
  color: var(--primary);
}

.auth-card p {
  margin: 0 0 24px;
  text-align: center;
  color: var(--muted);
}

.auth-card label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.auth-card input,
.form-grid input,
.form-grid select,
.form-grid button,
button.secondary-btn,
button.nav-btn {
  font: inherit;
}

.auth-card input,
.form-grid input,
.form-grid select {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 16px;
  background: #fff;
}

button {
  border: 0;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s ease;
}

#loginButton,
.form-grid button {
  width: 100%;
  background: var(--primary);
  color: white;
  padding: 12px 18px;
  font-weight: 700;
}

#loginButton:hover,
.form-grid button:hover {
  background: var(--primary-dark);
}

.error-message {
  min-height: 20px;
  color: var(--danger);
  margin-top: 10px;
  font-size: 0.9rem;
}

small {
  display: block;
  margin-top: 14px;
  text-align: center;
  color: var(--muted);
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #0f172a;
  color: white;
  padding: 16px 24px;
}

.topbar h2 {
  margin: 0;
}

.user-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.secondary-btn {
  background: #1f2937;
  color: white;
  padding: 8px 12px;
}

.nav-tabs {
  display: flex;
  gap: 8px;
  padding: 16px 24px 8px;
  background: #fff;
  border-bottom: 1px solid var(--border);
}

.nav-btn {
  background: #eef2ff;
  color: var(--text);
  padding: 10px 14px;
  font-weight: 600;
}

.nav-btn.active {
  background: var(--primary);
  color: white;
}

.content {
  padding: 24px;
}

.tab-panel {
  display: none;
}

.tab-panel.active {
  display: block;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 18px;
  margin-bottom: 20px;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03);
}

.card span {
  display: block;
  color: var(--muted);
  margin-bottom: 12px;
}

.card strong {
  font-size: 2rem;
}

.panel-header {
  margin-bottom: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 14px;
  align-items: end;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px;
  margin-bottom: 22px;
}

.form-grid button {
  max-width: 200px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

th, td {
  border-bottom: 1px solid var(--border);
  padding: 12px 10px;
  text-align: left;
  vertical-align: top;
}

th {
  background: #eef4ff;
}

tbody tr:last-child td {
  border-bottom: none;
}

.action-btn,
.status-btn {
  padding: 8px 10px;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
}

.action-btn.delete {
  background: var(--danger);
}

.status-btn {
  background: var(--success);
}

@media (max-width: 700px) {
  .nav-tabs {
    overflow-x: auto;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
