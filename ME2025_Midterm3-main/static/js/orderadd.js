// 開啟與關閉Modal
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
}
function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

function delete_data(value) {
    // 發送 DELETE 請求到後端
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回傳錯誤");
        }
        return response.json(); // 假設後端回傳 JSON 格式資料
    })
    .then(result => {
        console.log(result); // 在這裡處理成功的回應
        close_input_table(); // 關閉 modal
        location.assign('/'); // 重新載入頁面
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}