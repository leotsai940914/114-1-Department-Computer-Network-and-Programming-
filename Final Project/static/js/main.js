/* ============================================================
   Dropdown（手機 & 桌機共用）
============================================================ */

document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    toggle.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        const menu = this.nextElementSibling;

        // toggle 開關
        const opened = menu.style.display === "block";
        document.querySelectorAll(".dropdown-menu")
            .forEach(m => (m.style.display = "none"));

        menu.style.display = opened ? "none" : "block";
    });
});

// 點擊其他地方時收起 dropdown
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
   全站通用：基本空白欄位防呆（required）
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
   Quill Editor（New Post / Edit Post 共用）
   👉 只在有載入 Quill 的頁面生效
============================================================ */

if (window.Quill) {

    // ---------- 行距：自訂 Attributor ----------
    const Parchment = Quill.import("parchment");

    const lineHeightConfig = {
        scope: Parchment.Scope.BLOCK,
        whitelist: ["1", "1.2", "1.4", "1.6", "1.8", "2.0"]
    };

    const LineHeightStyle = new Parchment.Attributor.Class(
        "line-height",
        "ql-line-height",
        lineHeightConfig
    );

    Quill.register(LineHeightStyle, true);

    // ---------- Divider（hr） ----------
    const Block = Quill.import("blots/block");
    class Divider extends Block {}
    Divider.blotName = "divider";
    Divider.tagName = "hr";
    Quill.register(Divider);


    // ---------- 共用初始化函式 ----------
    function initQuillEditor(editorId, hiddenFieldId, toolbarSelector, rawHTMLId = null) {
        const container = document.getElementById(editorId);
        if (!container) return null;   // 該頁沒有這個編輯器，直接跳出

        const modules = toolbarSelector
            ? { toolbar: toolbarSelector }
            : { toolbar: true };

        const quill = new Quill(`#${editorId}`, {
            theme: "snow",
            placeholder: "請輸入文章內容…",
            modules: modules
        });

        // 若有舊文章內容（Edit 頁）
        if (rawHTMLId) {
            const rawHTMLContainer = document.getElementById(rawHTMLId);
            const rawHTML = rawHTMLContainer ? rawHTMLContainer.innerHTML : "";
            quill.root.innerHTML = rawHTML;
        }

        // #insert-hr 按鈕（若存在）→ 插入 <hr>
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

        // 表單送出 → 塞進 hidden input
        const hiddenField = document.getElementById(hiddenFieldId);
        const parentForm  = container.closest("form");

        if (parentForm && hiddenField) {
            parentForm.addEventListener("submit", function (e) {
                const html = quill.root.innerHTML.trim();

                if (html === "<p><br></p>" || html.length < 5) {
                    alert("文章內容不得為空");
                    e.preventDefault();
                    return;
                }

                hiddenField.value = html;
            });
        }

        return quill;
    }

    // ---------- 新增文章頁 ----------
    initQuillEditor(
        "quillEditor",   // 編輯器容器 id
        "contentInput",  // 隱藏欄位 id
        "#toolbar"       // 工具列 selector（如果你有自訂 toolbar）
    );

    // ---------- 編輯文章頁 ----------
    initQuillEditor(
        "quillEditor",
        "contentInput",
        "#toolbar",
        "rawContent"     // 裝舊文章 HTML 的隱藏 div
    );
}