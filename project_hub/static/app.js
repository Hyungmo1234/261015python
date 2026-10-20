const grid = document.getElementById("grid");
const meta = document.getElementById("meta");
const detailDialog = document.getElementById("detail-dialog");
const detailBody = document.getElementById("detail-body");
const manageDialog = document.getElementById("manage-dialog");
const projectForm = document.getElementById("project-form");
const editToken = document.getElementById("edit-token");
const btnManage = document.getElementById("btn-manage");
const btnDelete = document.getElementById("btn-delete");

let state = { projects: [] };

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function statusLabel(s) {
  return (
    { active: "진행 중", idea: "아이디어", paused: "중단", done: "완료" }[s] || s
  );
}

function headers() {
  const h = { "Content-Type": "application/json" };
  const t = editToken.value.trim();
  if (t) h["X-Portal-Token"] = t;
  return h;
}

function renderCard(p) {
  const tags = (p.tags || [])
    .map((t) => `<span class="tag">${esc(t)}</span>`)
    .join("");
  const links = [];
  if (p.site_url) links.push(`<a href="${esc(p.site_url)}" target="_blank" rel="noopener">서비스</a>`);
  if (p.repo_url) links.push(`<a href="${esc(p.repo_url)}" target="_blank" rel="noopener">저장소</a>`);
  return `
    <article class="card" tabindex="0" data-id="${esc(p.id)}" role="button">
      <div class="card-top">
        <span class="status-pill ${esc(p.status || "active")}">${esc(statusLabel(p.status))}</span>
        <button type="button" class="btn tiny ghost edit-btn" data-edit="${esc(p.id)}">수정</button>
      </div>
      <h2>${esc(p.name)}</h2>
      <p>${esc(p.description)}</p>
      <div class="tags">${tags}</div>
      <p class="card-links">${links.join(" · ") || '<span class="muted">링크 없음 (메모만)</span>'}</p>
    </article>`;
}

function renderDetail(p) {
  const git = p.git;
  detailBody.innerHTML = `
    <header class="dialog-head">
      <h2>${esc(p.name)}</h2>
      <button type="button" class="btn ghost" data-close>닫기</button>
    </header>
    <p>${esc(p.description)}</p>
    ${p.notes ? `<p class="note">${esc(p.notes)}</p>` : ""}
    ${p.display_notes ? `<p class="note warn">${esc(p.display_notes)}</p>` : ""}
    <ul class="kv">
      <li><span>상태</span>${esc(statusLabel(p.status))}</li>
      ${p.site_url ? `<li><span>서비스</span><a href="${esc(p.site_url)}" target="_blank">${esc(p.site_url)}</a></li>` : ""}
      ${p.repo_url ? `<li><span>저장소</span><a href="${esc(p.repo_url)}" target="_blank">${esc(p.repo_url)}</a></li>` : ""}
    </ul>
    ${
      git
        ? `<section><h3>Git (로컬 스캔)</h3><ul class="kv mono">
      <li><span>branch</span>${esc(git.branch)}</li>
      <li><span>commit</span>${esc(git.commit)}</li>
      <li><span>message</span>${esc(git.last_subject)}</li>
    </ul></section>`
        : ""
    }
    ${
      p.status_summary?.length
        ? `<section><h3>진행 문서</h3><ul>${p.status_summary.map((s) => `<li>${esc(s)}</li>`).join("")}</ul></section>`
        : ""
    }
    ${
      p.readme_excerpt
        ? `<section><h3>README</h3><p>${esc(p.readme_excerpt)}</p></section>`
        : ""
    }
    <footer><button type="button" class="btn primary" data-edit="${esc(p.id)}">수정</button></footer>
  `;
  detailDialog.showModal();
}

function fillForm(p) {
  document.getElementById("f-id").value = p?.id || "";
  document.getElementById("f-name").value = p?.name || "";
  document.getElementById("f-desc").value = p?.description || "";
  document.getElementById("f-tags").value = (p?.tags || []).join(", ");
  document.getElementById("f-status").value = p?.status || "active";
  document.getElementById("f-site").value = p?.site_url || "";
  document.getElementById("f-repo").value = p?.repo_url || "";
  document.getElementById("f-notes").value = p?.notes || "";
  document.getElementById("f-scan").value = p?.scan_dir || "";
  btnDelete.classList.toggle("hidden", !p?.id);
}

function openManage(project) {
  fillForm(project || null);
  manageDialog.showModal();
}

async function load() {
  grid.innerHTML = `<p class="loading">불러오는 중…</p>`;
  const res = await fetch("/api/portal");
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  state = data;
  document.getElementById("portal-title").textContent = data.portal_title;
  document.getElementById("portal-subtitle").textContent = data.portal_subtitle;
  document.getElementById("owner-line").textContent = data.owner || "My Portal";
  meta.textContent = `데이터: ${data.data_path} · 갱신 ${new Date(data.generated_at).toLocaleString("ko-KR")}`;
  grid.innerHTML = (data.projects || []).map(renderCard).join("") || `<p class="loading">프로젝트가 없습니다. 「프로젝트 관리」에서 추가하세요.</p>`;

  const byId = Object.fromEntries((data.projects || []).map((p) => [p.id, p]));
  grid.querySelectorAll(".card").forEach((el) => {
    el.addEventListener("click", (e) => {
      if (e.target.closest(".edit-btn")) return;
      renderDetail(byId[el.dataset.id]);
    });
  });
  grid.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      openManage(byId[btn.dataset.edit]);
    });
  });
}

projectForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = document.getElementById("f-id").value.trim();
  const body = {
    name: document.getElementById("f-name").value.trim(),
    description: document.getElementById("f-desc").value.trim(),
    tags: document.getElementById("f-tags").value.split(",").map((t) => t.trim()).filter(Boolean),
    status: document.getElementById("f-status").value,
    site_url: document.getElementById("f-site").value.trim() || null,
    repo_url: document.getElementById("f-repo").value.trim() || null,
    notes: document.getElementById("f-notes").value.trim(),
    scan_dir: document.getElementById("f-scan").value.trim() || null,
  };
  const url = id ? `/api/portal/projects/${encodeURIComponent(id)}` : "/api/portal/projects";
  const method = id ? "PUT" : "POST";
  const res = await fetch(url, { method, headers: headers(), body: JSON.stringify(body) });
  if (!res.ok) {
    alert(`저장 실패: ${await res.text()}`);
    return;
  }
  manageDialog.close();
  await load();
});

btnDelete.addEventListener("click", async () => {
  const id = document.getElementById("f-id").value.trim();
  if (!id || !confirm("이 프로젝트를 포털에서 삭제할까요?")) return;
  const res = await fetch(`/api/portal/projects/${encodeURIComponent(id)}`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!res.ok) {
    alert(`삭제 실패: ${await res.text()}`);
    return;
  }
  manageDialog.close();
  await load();
});

btnManage.addEventListener("click", () => openManage(null));

document.body.addEventListener("click", (e) => {
  const close = e.target.closest("[data-close]");
  if (close) {
    detailDialog.close();
    manageDialog.close();
  }
  const edit = e.target.closest("[data-edit]");
  if (edit && detailDialog.open) {
    detailDialog.close();
    const p = state.projects.find((x) => x.id === edit.dataset.edit);
    openManage(p);
  }
});

load().catch((err) => {
  grid.innerHTML = `<p class="loading">오류: ${esc(err.message)}</p>`;
});
