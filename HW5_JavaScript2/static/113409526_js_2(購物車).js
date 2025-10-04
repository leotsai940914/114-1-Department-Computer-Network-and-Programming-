(() => {
  "use strict";

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const master = $("#checkbox_all");
  const itemCheckboxes = $$(".item_checkbox");


  //calculate the total price
  function calcTotal(){
    let total = 0;
    $$(".item-row").forEach((row) => {
      const price = Number(row.querySelector(".item-price").textContent);
      const qty = Number(row.querySelector(".item-qty").value);
      const subtotal = price * qty;
      row.querySelector(".item-checkbox").textContent = subtotal;


      //only selected number would be calculated into total
      if (row.querySelector(".item-checkbox").checked) {
        total += subtotal;
      }
    });
    $("#total").textContent = total;
  }

  //master checkbox control all item checkboxes
  



}
