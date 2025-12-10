// =========================
// Dropdown（手機 & 桌機都能用）
// =========================

// 找到所有 dropdown toggle
document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    toggle.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        const menu = this.nextElementSibling;

        // toggle 展開/收合
        if (menu.style.display === "block") {
            menu.style.display = "none";
        } else {
            // 先關掉其他 dropdown
            document.querySelectorAll(".dropdown-menu").forEach(m => (m.style.display = "none"));
            menu.style.display = "block";
        }
    });
});

// 點擊其他地方就關閉 dropdown
document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-menu").forEach(menu => (menu.style.display = "none"));
});



// =========================
// 前端表單驗證：留言不可空白
// =========================

const commentForm = document.querySelector(".comment-form");

if (commentForm) {
    commentForm.addEventListener("submit", function (e) {
        const nickname = this.querySelector("input[name='nickname']").value.trim();
        const content = this.querySelector("textarea[name='content']").value.trim();

        if (!nickname || !content) {
            alert("暱稱與內容不可為空！");
            e.preventDefault();
        }
    });
}



// =========================
// New Post / Register / Login：空欄位避免提交
// =========================

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
        // 用 required 屬性讓瀏覽器處理，不多做干涉
        // 但如果某些欄位沒 required，這裡會補上一層防護

        const invalid = Array.from(this.querySelectorAll("input, textarea, select"))
            .some(field => field.hasAttribute("required") && !field.value.trim());

        if (invalid) {
            alert("請完整填寫所有必填欄位。");
            e.preventDefault();
        }
    });
});