const grid = document.getElementById("grid");
const detail = document.getElementById("detail");
const meta = document.getElementById("meta");

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderCard(p) {
  const git = p.git;
  const gitLine = git
    ? `${git.branch} · ${git.commit}${git.dirty ? " · 변경 있음" : ""}`
    : p.available
      ? "Git 정보 없음"
      : "경로 없음";
  const badge = p.available
    ? `<span class="badge ok">연결됨</span>`
    : `<span class="badge off">오프라인</span>`;
  const tags = (p.tags || [])
    .map((t) => `<span class="tag">${esc(t)}</span>`)
    .join("");
  return `
    <article class="card" tabindex="0" data-id="${esc(p.id)}" role="button">
      <h2>${esc(p.name)}</h2>
      <p>${esc(p.description)}</p>
      <div class="tags">${tags}</div>
      ${badge}
      <p class="git-row" style="margin-top:0.5rem;color:var(--muted);font-size:0.8rem">${esc(gitLine)}</p>
    </article>`;
}

function renderDetail(p) {
  const git = p.git;
  const pkg = p.package;
  const stats = p.stats;
  const links = (p.links || [])
    .map((l) => {
      const suffix = l.exists ? "" : " (파일 없음)";
      if (p.repo && l.path) {
        return `<li><a href="${esc(p.repo)}/blob/main/${esc(l.path)}" target="_blank" rel="noopener">${esc(l.label)}${suffix}</a></li>`;
      }
      return `<li>${esc(l.label)}${suffix}</li>`;
    })
    .join("");

  detail.innerHTML = `
    <header>
      <h2>${esc(p.name)}</h2>
      <button type="button" class="close" aria-label="닫기">닫기</button>
    </header>
    <div class="section">
      <h3>개요</h3>
      <p>${esc(p.description)}</p>
      ${p.readme_excerpt ? `<p style="margin-top:0.5rem">${esc(p.readme_excerpt)}</p>` : ""}
      ${p.notes ? `<p style="margin-top:0.5rem;color:var(--warn)">${esc(p.notes)}</p>` : ""}
    </div>
    ${
      p.repo
        ? `<div class="section"><h3>GitHub</h3><p><a href="${esc(p.repo)}" target="_blank" rel="noopener">${esc(p.repo)}</a></p></div>`
        : ""
    }
    ${
      git
        ? `<div class="section"><h3>Git</h3>
      <ul>
        <li>브랜치: ${esc(git.branch)}</li>
        <li>커밋: ${esc(git.commit)}</li>
        <li>메시지: ${esc(git.last_subject)}</li>
        <li>일시: ${esc(git.last_commit_at)}</li>
      </ul></div>`
        : ""
    }
    ${
      pkg
        ? `<div class="section"><h3>패키지</h3>
      <p><code>${esc(pkg.path)}</code> — ${esc(pkg.name)}@${esc(pkg.version || "?")}</p>
      <ul>${Object.entries(pkg.scripts || {})
        .map(([k, v]) => `<li>${esc(k)}: <code>${esc(v)}</code></li>`)
        .join("")}</ul></div>`
        : ""
    }
    ${
      p.dev
        ? `<div class="section"><h3>실행</h3><ul>${Object.entries(p.dev)
            .map(([k, v]) => `<li>${esc(k)}: ${esc(v)}</li>`)
            .join("")}</ul></div>`
        : ""
    }
    ${
      p.status_summary?.length
        ? `<div class="section"><h3>진행 (STATUS)</h3><ul>${p.status_summary
            .map((s) => `<li>${esc(s)}</li>`)
            .join("")}</ul></div>`
        : ""
    }
    ${
      stats
        ? `<div class="section"><h3>파일 수 (대략)</h3><p>Python ${stats.py} · TS/TSX ${stats.ts_tsx} · Markdown ${stats.md}</p></div>`
        : ""
    }
    ${links ? `<div class="section"><h3>문서</h3><ul>${links}</ul></div>` : ""}
    ${
      p.path
        ? `<div class="section"><h3>로컬 경로</h3><p class="git-row">${esc(p.path)}</p></div>`
        : ""
    }
  `;

  detail.classList.remove("hidden");
  detail.querySelector(".close").addEventListener("click", () => {
    detail.classList.add("hidden");
  });
}

async function load() {
  grid.innerHTML = `<p class="loading">프로젝트 목록 불러오는 중…</p>`;
  try {
    const res = await fetch("/api/projects");
    if (!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    meta.textContent = `기준 경로: ${data.projects_base || "(미설정)"} · 갱신: ${new Date(
      data.generated_at
    ).toLocaleString("ko-KR")}`;
    grid.innerHTML = data.projects.map(renderCard).join("");
    const byId = Object.fromEntries(data.projects.map((p) => [p.id, p]));
    grid.querySelectorAll(".card").forEach((el) => {
      const open = () => renderDetail(byId[el.dataset.id]);
      el.addEventListener("click", open);
      el.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open();
        }
      });
    });
  } catch (err) {
    grid.innerHTML = `<p class="loading">불러오기 실패: ${esc(err.message)}</p>`;
  }
}

load();
