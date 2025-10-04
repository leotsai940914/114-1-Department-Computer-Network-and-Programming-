(() => {
  "use strict";

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const master = $("#checkbox_all");
  const itemCheckboxes = $$(".item-checkbox");

  const rows = document.querySelectorAll(".item-row");


  //calculate the total price
  function calcTotal(){
    let total = 0;
    $$(".item-row").forEach((row) => {
      const price = Number(row.querySelector(".item-price").textContent);
      const qty = Number(row.querySelector(".qty").value);
      const subtotal = price * qty;
      row.querySelector(".subtotal").textContent = subtotal;


      //only selected number would be calculated into total
      if (row.querySelector(".item-checkbox").checked) {
        total += subtotal;
      }
    });
    $("#total").textContent = total;
  }

  //master checkbox control all item checkboxes
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

  //quantity change
  $$(".item-row").forEach((row) => {
    const plusBtn = row.querySelector(".plus");
    const minusBtn = row.querySelector(".minus");
    const qtyInput = row.querySelector(".qty");
    const stock = Number(row.querySelector(".item-stock").textContent);


    plusBtn.addEventListener("click", () => {
      let qty = Number(qtyInput.value);
      if (qty < stock) {
        qtyInput.value = qty + 1;
        calcTotal();
      }
    });

    minusBtn.addEventListener("click", () => {
      let qty = Number(qtyInput.value);
      if (qty > 0) {
        qtyInput.value = qty - 1;
        calcTotal();
      }
    });

    document.querySelector("#checkout").addEventListener("click",() => {
      const totalText = document.querySelector("#total").textContent;
      const total = Number(totalText);

      if  (total <= 0){
        return;
      };
            
    })

    qtyInput.addEventListener("input", () => {
      let qty = Number(qtyInput.value);
      if (isNaN(qty) || qty < 0) qty = 0;
      if (qty > stock) qty = stock;
      qtyInput.value = qty;
      calcTotal();
    });
  });
  
  calcTotal();
  document.querySelector("#checkout").addEventListener("click", () => {
    const total = Number(document.querySelector("#total").textContent);
    if (total <= 0) return;

    let details = "";

    document.querySelectorAll(".item-row").forEach((row) => {
      const checkbox = row.querySelector(".item-checkbox");
      if (!checkbox.checked) return;

      const name = row.querySelector("td:nth-child(2)").innerText.trim();
      const price = Number(row.querySelector(".item-price").textContent);
      const qty = Number(row.querySelector(".qty").value);
      const subtotal = price * qty;

      details += `📦 ${name}\n數量: ${qty} x 價格: ${price} = 小計: ${subtotal}\n\n`;
    });

    details += `🧾 總金額：${total}`;
    alert(details);
  });


})();
