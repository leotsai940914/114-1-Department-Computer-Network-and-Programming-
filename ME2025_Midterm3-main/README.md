# 第三次測試 - 前後端 & OS & 版控

本次的目標是建立一個訂單管理系統，請同學 Fork 回自己帳號並繳交 Repo 連結，可以使用提供的程式碼改寫或自行重構(注意：HTML-id 命名須與提供的程式碼一致！)。

## 評分標準
- 前端: 實際測試功能是否正常
- 後端、資料庫、OS:
在終端機中執行以下程式碼:
  ```
  python3 -m test.backend
  python3 -m test.database
  python3 -m test.linux
  ```
  如果回覆 OK 則該 Part 滿分(請注意! 程式碼有例外狀況，例如無法執行等，通過測試仍會扣分)。  
  其餘依完成功能部份給分。

## Part1. 前端(20%)
首頁左上角「新增商品資料」的功能目前是缺失的，請依照下列需求，在 orderadd.js 中實作出完整功能。

__需求規格__
1. 表單欄位：
    - 包含 客戶名稱、備註 的輸入欄位。
    - 日期：預設為 當天日期。
    - 數量：數值必須恆大於 0，預設值為 1。
    - 狀態：下拉選單包含「已完成」、「已付款」、「未付款」，預設為 未付款。

2. 連動功能(10%)：
    - 選取 商品種類 (Category) 後，需即時向後端發送請求，取得該種類下的商品列表，並更新 商品名稱 的下拉選單供選取。

3. 自動計算(5%)：
    - 選取 商品名稱 後，需自動取得並顯示該商品的 單價。
    - 當 數量 或 單價 變動時，需自動計算並顯示 小計 (單價 × 數量)。

4. 資料送出(5%)：
    - 表單填寫完畢後，需能將資料以 POST 方法送給後端 /product 路徑，並記錄於資料庫中。

__作答區__
1. orderadd.js
請完成下列 JavaScript 邏輯以實作連動與計算功能：
    ```
    // orderadd.js

    // 1. 選取商品種類後的連動邏輯 (Fetch API)
    function selectCategory() {
        // TODO: Fetch product list by category
    }

    // 2. 選取商品後的價格更新邏輯 (Fetch API)
    function selectProduct() {
        // TODO: Fetch price by product name
    }

    // 3. 計算小計邏輯
    function countTotal() {
        // TODO: Calculate total price
    }

    // 其他輔助函式 (如重置欄位等) 可自由實作
    ```

## Part2. 後端(30%)
請完成 app.py 中的 /product 路由，需支援 GET, POST, DELETE 方法以處理前端請求。
須具備以下功能:  

__需求規格__
1. GET 方法 (查詢資料)(10%)：
    - 若請求包含 category 參數：呼叫 `db.get_product_names_by_category(category)`，並回傳 JSON {"product": [...]}。
    - 若請求包含 product 參數：呼叫 `db.get_product_price(product)`，並回傳 JSON {"price": ...}。

2. POST 方法 (新增訂單)(10%)：
    - 接收前端 Form Data，並整理成包含以下 Key 的字典 (Dictionary)：`product_date`, `customer_name`, `product_name`, `product_amount`, `product_total`, `product_status`, `product_note`。
    - 呼叫 `db.add_order(order_data)` 將資料寫入資料庫。
    - 成功後，重導向 (Redirect) 至首頁 index，並帶上 warning="Order placed successfully"(alert顯示) 訊息。

3. DELETE 方法 (刪除訂單)(10%)：
    - 取得 URL 參數中的 order_id。
    - 呼叫 `db.delete_order(order_id)` 刪除該筆訂單。
    - 成功後回傳 JSON {"message": "Order deleted successfully"} (Status 200)。

__作答區__ 
1. app.py  
請完成 /product 路由函式：
    ```
    @app.route('/product', methods=['GET', 'POST', 'DELETE'])
    def product():
        if request.method == 'GET':
          # TODO: Implement GET logic for category list and product price
        elif request.method == 'POST':
          # TODO: Implement POST logic to add new order
        elif request.method == 'DELETE':
          # TODO: Implement DELETE logic using order_id
    ```

## Part3. 資料庫 (20%)
請完成 `database.py` 中 Database 類別的 CRUD 方法。需撰寫正確的 SQL 語法與 Python 邏輯來操作 SQLite 資料庫。

__需求規格__
1. 資料表結構參考：
    - `commodity`: 包含 `category` (種類), `product` (名稱), `price` (價格)。
    - `order_list`: 包含 `order_id`, `product_date`, `customer_name`, `product_name`, `product_amount`, `product_total`, `product_status`, `product_note`。

2. 功能需求(每個需求4%)：
    - `get_product_names_by_category`: 根據傳入的 category 篩選出所有商品名稱。
    - `get_product_price`: 根據傳入的 product 名稱查詢單價。
    - `add_order`: 將訂單資料字典 (Dictionary) 寫入 `order_list` 資料表。
    - `delete_order`: 根據 `order_id` 刪除特定訂單。
    - `get_all_orders`: 取得所有訂單，並需額外查詢該商品的 `price` 欄位合併回傳。

__作答區__ 
1. database.py
    ```
    def get_product_names_by_category(category):
      # TODO: Execute SQL to select product names by category
    def get_product_price(product):
      # TODO: Execute SQL to select price by product name
    def add_order(order_data):
      # TODO: Execute SQL to insert a new order into order_list
    def get_all_orders():
      # TODO: Execute SQL to get all order information
    def delete_order(order_id):
      # TODO: Execute SQL to delete order by order_id
    ```

## Part4. OS & 版控(30%)
### 專案自動部屬與更新
請撰寫 deploy.sh 需求如下:
  - 首次執行(15%)
    1. 自動 clone repository
    2. 在專案下建立虛擬環境，命名為 .venv
    3. 自動安裝 requirements.txt 中的套件
    4. 啟動 app.py
  - 第二次以後執行(15%)
    1. 自動更新專案版本
    2. 檢查 requirements.txt 中未安裝的套件並安裝
    3. 重啟app.py
