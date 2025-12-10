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

    initQuillEditor("quillEditor", "contentInput", "#toolbar");
    initQuillEditor("quillEditor", "contentInput", "#toolbar", "rawContent");
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