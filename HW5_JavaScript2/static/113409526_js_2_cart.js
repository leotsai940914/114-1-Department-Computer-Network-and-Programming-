(() => {
  "use strict";

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const master = $("#checkbox_all");
  const itemCheckboxes = $$(".item-checkbox");

  function calcTotal() {
    let total = 0;
    $$(".item-row").forEach((row) => {
      const price = Number(row.querySelector(".item-price").textContent);
      const qty = Number(row.querySelector(".qty").value);
      const subtotal = price * qty;
      row.querySelector(".subtotal").textContent = subtotal;

      if (row.querySelector(".item-checkbox").checked) {
        total += subtotal;
      }
    });
    $("#total").textContent = total;
  }

  master.addEventListener("change", (e) => {
    const checked = e.target.checked;
    itemCheckboxes.forEach((cb) => (cb.checked = checked));
    calcTotal();
  });

  itemCheckboxes.forEach(cb => {
    cb.addEventListener("change", () => {
      const total = itemCheckboxes.length;
      const checkedCount = itemCheckboxes.filter(cb => cb.checked).length;
      master.checked = (checkedCount === total);
      master.indeterminate = (checkedCount > 0 && checkedCount < total);
      calcTotal();
    });  
  });

  $$(".item-row").forEach((row) => {
    const plusBtn = row.querySelector(".plus");
    const minusBtn = row.querySelector(".minus");
    const qtyInput = row.querySelector(".qty");

    plusBtn.addEventListener("click", () => {
      const currentStock = Number(row.querySelector(".item-stock").textContent);
      let qty = Number(qtyInput.value);
      if (qty < currentStock) {
        qtyInput.value = qty + 1;
        calcTotal();
      }
    });

    minusBtn.addEventListener("click", () => {
      let qty = Number(qtyInput.value);
      if (qty > 1) {
        qtyInput.value = qty - 1;
        calcTotal();
      }
    });

    qtyInput.addEventListener("blur", () => {
      let qty = Number(qtyInput.value);
      const currentStock = Number(row.querySelector(".item-stock").textContent);
      if (isNaN(qty) || qty < 1) qty = 1;
      if (qty > currentStock) qty = currentStock;
      qtyInput.value = qty;
      calcTotal();
    });

    qtyInput.addEventListener("input", () => {
      let qty = Number(qtyInput.value);
      const currentStock = Number(row.querySelector(".item-stock").textContent);
      if (isNaN(qty) || qty < 0) qty = 0;
      if (qty > currentStock) qty = currentStock;
      qtyInput.value = qty;
      calcTotal();
    });
  });

  $("#checkout").addEventListener("click", () => {
    const total = Number($("#total").textContent);
    if (total <= 0) return;

    let details = "";

    $$(".item-row").forEach((row) => {
      const checkbox = row.querySelector(".item-checkbox");
      if (!checkbox.checked) return;

      const name = row.querySelector("td:nth-child(2)").innerText.trim();
      const price = Number(row.querySelector(".item-price").textContent);
      const qtyInput = row.querySelector(".qty");
      const qty = Number(qtyInput.value);
      const subtotal = price * qty;

      details += `📦 ${name}\n數量: ${qty} x 價格: ${price} = 小計: ${subtotal}\n\n`;

      checkbox.checked = false;

      const stockEl = row.querySelector(".item-stock");
      let stock = Number(stockEl.textContent);
      stock = Math.max(0, stock - qty);
      stockEl.textContent = stock;

      if (stock > 0) {
        qtyInput.value = 1;
        qtyInput.disabled = false;
      } else {
        qtyInput.value = 0;
        qtyInput.disabled = true;
      }
    });

    master.checked = false;
    master.indeterminate = false;

    details += `🧾 總金額：${total}`;
    alert(details);
    calcTotal(); // 重新計算
  });

  calcTotal();
})();

