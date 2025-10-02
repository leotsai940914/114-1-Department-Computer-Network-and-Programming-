(() => {
    "use strict"; //嚴格模式，不知道什麼意思

    const $ = (sel) => document.querySelector(sel); //小工具，幫忙選取元素
    const form = $("#guess-form"); 
    const input = $("#guess");
    const triesEl = $("#tries"); //這是 <b id="tries">0</b> 的元素
    
    let answer = Math.floor(Math.random() * 101);//產生 0 到 100 的整數
    let tries = 0; //記住輸入的次數

    let startTime = null;
    let timerID = null;
    let elapsedTime = 0;
    
    function startTimer() {
        startTime = Date.now();
        timerID = setInterval(() => {
            elapsedTime = Math.floor((Date.now() - startTime) / 1000);
            $("#timer").textContent = "時間:" + elapsedTime + " 秒";
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerID);
        timerID = null;
    }

    console.log("答案", answer); //先印出答案在 console

    //監聽表單送出事件
    form.addEventListener("submit", (e) => {
        e.preventDefault(); //防止表單送出後頁面重新整理

        const valStr = input.value.trim(); //取得輸入的字串
        const val = Number(valStr); //轉成數字

        if (valStr === "" || Number.isNaN(val)) {
            alert("請輸入數字"); //如果不是數字就跳警告視窗
            return; //結束函式
        }

        if (tries === 0) {
            startTimer(); //開始計時
        }

        tries += 1; //輸入次數 +1
        triesEl.textContent = String(tries); //更新畫面上的輸入次數

        if (val === answer) {
            stopTimer(); //停止計時

            alert(`恭喜你答對了!你共猜了 ${tries} 次，耗時 ${elapsedTime} \n下一題，繼續挑戰!`); //答對就跳出恭喜視窗
           
            //重設遊戲
            answer = Math.floor(Math.random() * 101); //產生新答案
            tries = 0; //重設輸入次數
            triesEl.textContent = "0"; //更新畫面上的輸入次數
            input.value = ""; //清空輸入框
            $("#timer").textContent = "時間:0 秒"; //重設時間顯示
            elapsedTime = 0; //重設經過時間
            console.log("答案", answer); //印出新答案在 console
            
        }   else if (val < answer) {
            alert("太小了!"); //比答案小就跳出太小視窗
        }   else {
            alert("太大了!"); //比答案大就跳出太大視窗
        }

        input.focus(); //讓輸入框重新取得焦點
        input.select(); //選取輸入框的文字，方便直接輸入下一次的數字

        console.log("你輸入的是", val); //印出輸入的數字在 console
    });
})();