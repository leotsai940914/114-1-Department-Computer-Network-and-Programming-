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

    
    
})();