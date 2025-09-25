(() => {
    "use strict"; //嚴格模式，不知道什麼意思

    const $ = (sel) => document.querySelector(sel); //小工具，幫忙選取元素
    const form = $("#guess-form"); 
    const input = $("#guess");
    
    let answer = Math.floor(Math.random() * 101);//產生 0 到 100 的整數
    console.log("答案", answer); //先印出答案在 console

    //監聽表單送出事件
    form.addEventListener("submit", (e) => {
        e.preventDefault(); //防止表單送出後頁面重新整理

        const val = input.value; //取得輸入的數字
        console.log("你輸入的是", val); //印出輸入的數字在 console
    });

    let tries = 0; //記住輸入的次數

   
   
})();