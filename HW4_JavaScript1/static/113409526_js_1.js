(() => {
    "use strict"; //嚴格模式，不知道什麼意思
    
    //產生 0 到 100 的整數
    let answer = Math.floor(Math.random() * 101);

    //記住輸入的次數
    let tries = 0;

    //先印出答案在 console
    console.log("答案", answer);
})();