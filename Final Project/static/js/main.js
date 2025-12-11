/* ============================================================
   Dropdown（手機 & 桌機共用）
============================================================ */

document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    toggle.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        const menu = this.nextElementSibling;
        const opened = menu.style.display === "block";

        document.querySelectorAll(".dropdown-menu")
            .forEach(m => (m.style.display = "none"));

        menu.style.display = opened ? "none" : "block";
    });
});

document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-menu")
        .forEach(menu => (menu.style.display = "none"));
});

/* Admin mini menu */
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".admin-toggle");
    const menu = document.querySelector(".admin-dropdown");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", (e) => {
        e.stopPropagation();
        menu.classList.toggle("open");
    });
    document.addEventListener("click", () => menu.classList.remove("open"));
});

/* Hamburger for small screens (reuse dropdown toggle) */
document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".nav-links");
    const burger = document.querySelector(".burger-toggle");
    const overlay = document.getElementById("navOverlay");
    if (!nav || !burger) return;

    burger.addEventListener("click", () => {
        nav.classList.toggle("nav-open");
        overlay?.classList.toggle("show");
    });

    overlay?.addEventListener("click", () => {
        nav.classList.remove("nav-open");
        overlay.classList.remove("show");
    });
});

/* Theme toggle */
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector(".theme-toggle");
    if (!btn) return;

    const applyTheme = (mode) => {
        document.documentElement.classList.toggle("dark-mode", mode === "dark");
        localStorage.setItem("theme", mode);
        btn.textContent = mode === "dark" ? "☀" : "☾";
    };

    const saved = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(saved || (prefersDark ? "dark" : "light"));

    btn.addEventListener("click", () => {
        const current = document.documentElement.classList.contains("dark-mode") ? "dark" : "light";
        applyTheme(current === "dark" ? "light" : "dark");
    });
});

/* ============================================================
   留言區：前端表單驗證
============================================================ */

const commentForm = document.querySelector(".comment-form");

if (commentForm) {
    commentForm.addEventListener("submit", function (e) {
        const nickname = this.querySelector("input[name='nickname']").value.trim();
        const content  = this.querySelector("textarea[name='content']").value.trim();

        if (!nickname || !content) {
            alert("暱稱與內容不可為空！");
            e.preventDefault();
        }
    });
}


/* ============================================================
   全站通用：基本必填欄位驗證
============================================================ */

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {

        const invalid = Array.from(
            this.querySelectorAll("input[required], textarea[required], select[required]")
        ).some(field => !field.value.trim());

        if (invalid) {
            alert("請完整填寫所有必填欄位。");
            e.preventDefault();
        }
    });
});


/* ============================================================
   Quill Editor（新增／編輯共用）
============================================================ */

if (window.Quill) {
    const Parchment = Quill.import("parchment");

    const lineHeightConfig = {
        scope: Parchment.Scope.BLOCK,
        whitelist: ["1", "1.2", "1.4", "1.6", "1.8", "2.0"]
    };

    const LineHeightStyle = new Parchment.Attributor.Class(
        "line-height", "ql-line-height", lineHeightConfig
    );
    Quill.register(LineHeightStyle, true);

    const Block = Quill.import("blots/block");
    class Divider extends Block {}
    Divider.blotName = "divider";
    Divider.tagName = "hr";
    Quill.register(Divider);

    function initQuillEditor(editorId, hiddenFieldId, toolbarSelector, rawHTMLId = null) {
        const editor = document.getElementById(editorId);
        if (!editor) return;

        const quill = new Quill(`#${editorId}`, {
            theme: "snow",
            placeholder: "請輸入文章內容…",
            modules: { toolbar: toolbarSelector }
        });

        if (rawHTMLId) {
            const raw = document.getElementById(rawHTMLId)?.innerHTML || "";
            quill.root.innerHTML = raw;
        }

        const hrBtn = document.getElementById("insert-hr");
        if (hrBtn) {
            hrBtn.addEventListener("click", () => {
                const range = quill.getSelection();
                if (range) {
                    quill.insertEmbed(range.index, "divider", true);
                    quill.insertText(range.index + 1, "\n");
                }
            });
        }

        const hidden = document.getElementById(hiddenFieldId);
        if (!hidden) return;  // 若該頁沒有對應 hidden input，直接跳過（避免阻擋其他表單）
        const parentForm = editor.closest("form");

        parentForm?.addEventListener("submit", function (e) {
            const html = quill.root.innerHTML.trim();
            if (html === "<p><br></p>" || html.length < 5) {
                alert("文章內容不得為空");
                e.preventDefault();
                return;
            }
            hidden.value = html;
        });
    }

    // 新增文章（若有 quillEditor）
    initQuillEditor("quillEditor", "contentInput", "#toolbar");

    // 編輯文章（若有 quillEditor-edit）
    initQuillEditor("quillEditor-edit", "contentInput-edit", "#toolbar-edit", "rawContent");
}


/* ============================================================
   Article Images → Lazy Load + Wrap for Lightbox
============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    const content = document.querySelector(".post-detail-content");
    if (!content) return;

    const imgs = content.querySelectorAll("img");

    imgs.forEach(img => {
        img.loading = "lazy";
        img.classList.add("lightbox-img");

        const wrapper = document.createElement("a");
        wrapper.href = img.src;
        wrapper.className = "lightbox-wrapper";

        img.parentNode.insertBefore(wrapper, img);
        wrapper.appendChild(img);
    });
});


/* ============================================================
   Lightbox 點擊放大（完整版）
============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("lightboxOverlay");
    const overlayImg = document.getElementById("lightboxImage");

    document.body.addEventListener("click", function (e) {

        if (e.target.classList.contains("lightbox-img") ||
            e.target.closest(".lightbox-wrapper")) {

            e.preventDefault();

            const img =
                e.target.tagName === "IMG"
                ? e.target
                : e.target.querySelector("img");

            overlayImg.src = img.src;
            overlay.style.display = "flex";
        }
    });

    overlay.addEventListener("click", () => {
        overlay.style.display = "none";
        overlayImg.src = "";
    });
});

/* ============================================================
   TOC：根據 H2/H3 生成目錄
============================================================ */
document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("postContent");
    const toc = document.getElementById("toc");
    const container = document.getElementById("tocContainer");
    if (!content || !toc || !container) return;

    const headings = content.querySelectorAll("h2, h3");
    if (!headings.length) {
        container.style.display = "none";
        return;
    }

    const slugify = (text) =>
        text.trim().toLowerCase()
            .replace(/[^\w\u4e00-\u9fff]+/g, "-")
            .replace(/-+/g, "-")
            .replace(/^-|-$/g, "");

    const list = document.createElement("ul");
    headings.forEach((h) => {
        if (!h.id) {
            const id = slugify(h.textContent || "section");
            h.id = id || `section-${Math.random().toString(16).slice(2, 7)}`;
        }
        const li = document.createElement("li");
        li.className = h.tagName.toLowerCase();

        const a = document.createElement("a");
        a.href = `#${h.id}`;
        a.textContent = h.textContent || h.id;
        li.appendChild(a);
        list.appendChild(li);
    });

    toc.appendChild(list);

    const toggle = container.querySelector(".toc-toggle");
    if (toggle) {
        toggle.addEventListener("click", () => {
            container.classList.toggle("open");
            toggle.textContent = container.classList.contains("open") ? "收合" : "展開";
        });
    }
});
