"""HTML landing surface for the CivicLibrary runtime."""


def render_public_lookup_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CivicLibrary v0.1.0</title>
  <style>
    :root{--ink:#17223b;--muted:#536075;--line:#cbd7ef;--paper:#f7f9ff;--card:#ffffff;--accent:#325da8;--leaf:#458a63}
    *{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;background:radial-gradient(circle at top right,#dfeaff,transparent 34rem),linear-gradient(135deg,#fbfdff,#f1f7f1);color:var(--ink)}
    main{max-width:1120px;margin:0 auto;padding:3rem 1.25rem}.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:2rem;align-items:center}
    h1{font-size:clamp(2.5rem,7vw,5rem);line-height:.92;margin:.25rem 0}.eyebrow{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    p{font-size:1.08rem;line-height:1.65;color:var(--muted)}.panel,.card{background:rgba(255,255,255,.88);border:1px solid var(--line);border-radius:28px;box-shadow:0 20px 60px rgba(23,34,59,.1)}
    .panel{padding:1.5rem}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2rem 0}.card{padding:1.2rem}.card h2{margin-top:0;color:var(--accent)}
    code{background:#e8eefb;padding:.15rem .35rem;border-radius:.35rem}.boundary{border-left:6px solid var(--leaf);padding-left:1rem}
    a{color:var(--accent);font-weight:700}@media(max-width:760px){.hero,.cards{grid-template-columns:1fr}main{padding:2rem 1rem}h1{font-size:3rem}}
  </style>
</head>
<body>
<main>
  <section class="hero">
    <div>
      <p class="eyebrow">CivicSuite / CivicLibrary</p>
      <h1>Library policy and reference support without patron records.</h1>
      <p>CivicLibrary v0.1.0 helps library staff answer policy and program questions, search collection metadata, draft collection guidance, and keep patron privacy out of scope.</p>
    </div>
    <div class="panel">
      <h2>v0.1.0 boundary</h2>
      <p class="boundary">No patron record access, no circulation history, no holds or fines, no ILS replacement, no live LLM calls, and no connector runtime ship in this release.</p>
    </div>
  </section>
  <section class="cards">
    <article class="card"><h2>Policy Q&A</h2><p>Cited drafts over library policies, program calendars, and public service rules.</p></article>
    <article class="card"><h2>Reference Support</h2><p>Collection metadata search only; patron borrowing and account records stay out.</p></article>
    <article class="card"><h2>Review Required</h2><p>Librarians review every answer, program response, and collection-development note before use.</p></article>
  </section>
  <section class="panel">
    <h2>Architecture</h2>
    <p><strong>Staff or patron question</strong> -> CivicLibrary deterministic API -> CivicCore foundation. Integrated library system adapters are future read-only designs, not v0.1.0 paths.</p>
    <p>Dependency: <code>civiccore==0.2.0</code>. Repo: <a href="https://github.com/CivicSuite/civiclibrary">CivicSuite/civiclibrary</a>.</p>
  </section>
</main>
</body>
</html>"""
