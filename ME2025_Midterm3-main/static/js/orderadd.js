// ========== Modal 開關 ==========
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
}

function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}


// ========== 刪除訂單 ==========
function delete_data(value) {
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        location.assign('/'); // 刪除後重新整理
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}


// ========== Part1 Requirement ==========

// 1. 選取商品種類 → 取得該類別的商品名稱列表
function selectCategory() {
    const category = document.getElementById("product_category").value;

    fetch(`/product?category=${category}`)
        .then(res => res.json())
        .then(data => {
            const productSelect = document.getElementById("product_name");
            productSelect.innerHTML = ""; // 清空舊資料

            data.product.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p;
                opt.textContent = p;
                productSelect.appendChild(opt);
            });

            // 自動載入第一筆商品的價格
            if (data.product.length > 0) {
                document.getElementById("product_name").value = data.product[0];
                selectProduct();
            }
        })
        .catch(err => {
            console.error("取得商品列表時發生錯誤：", err);
        });
}


// 2. 選取商品名稱 → 取得單價
function selectProduct() {
    const product = document.getElementById("product_name").value;

    fetch(`/product?product=${product}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("product_price").value = data.price;
            countTotal(); // 單價更新後重新計算小計
        })
        .catch(err => {
            console.error("取得商品價格時發生錯誤：", err);
        });
}


// 3. 計算小計 = 單價 × 數量
function countTotal() {
    const price = parseInt(document.getElementById("product_price").value) || 0;
    const amount = parseInt(document.getElementById("product_amount").value) || 1;

    // 不允許小於 1 的數量
    if (amount <= 0) {
        document.getElementById("product_amount").value = 1;
    }

    document.getElementById("product_total").value = price * amount;
}