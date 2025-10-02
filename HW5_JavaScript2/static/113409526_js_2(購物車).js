(() => {
  "use strict";

  const $  = (sel) => document.querySelector(sel);             // 單一
  const $$ = (sel) => Array.from(document.querySelectorAll(sel)); // 多個 → 陣列

  const master = $("#checkbox_all");
  const itemCheckboxes = $$(".item-checkbox");

  // 當「全選」變化時，所有商品 checkbox 跟著改
  master.addEventListener("change", (e) => {
    const checked = e.target.checked; // true/false
    itemCheckboxes.forEach(cb => cb.checked = checked);
  });
})();
