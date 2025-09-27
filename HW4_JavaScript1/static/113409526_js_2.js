(() => {
    "use strict";

    document.write(`
        <div style="width:220px; margin:20px auto;">
            <input id="display" type="text" readonly 
                style="width:100%; height:40px; font-size:18px;"/>
            <div id="buttons"></div>
        </div>
    `);


    //迴圈生成0-9按鈕
    for (let i = 0; i <=9; i++) {
        document.write(`
            <button class="btn" data-val="${i}">${i}</button>`);
        if (i % 3 === 0 && i !== 0) {
            document.write('<br/>');
            //每三個按鈕換行
            }   
    }

    document.write("<br/>"); //數字按鈕和功能按鈕間隔一行

    //功能按鈕
    const ops = ['+', '-', '*', '/', '(',')', '=', 'C'];
    for (let op of ops) {
        document.write(`
            <button class="btn" data-val="${op}">${op}</button>`);
    }

    //等 dom 準備好再綁事件
    window.addEventListener('DOMContentLoaded', () => {
        const display = document.getElementById('display');
        const buttons = document.querySelectorAll('.btn');

        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const val = btn.getAttribute('data-val');

                if (val === 'C') {
                    display.value = '';//清除
                }   else if (val === '=') {
                    try {
                        const expr = display.value;
                        const result = eval(expr);  //計算結果
                        alert(`${expr} = ${result}`);
                        display.value = result; //顯示結果
                    } catch (e) {
                        alert('錯誤的運算式');
                        display.value = '';
                    }
                }else {
                    display.value += val; //顯示按鈕值
                }
            });
        });
    });

        
    

})();