/*
函数timetojump获取一个id为timer的html元素，将second秒数写入其内容，
秒数如果减1后大于0，则用setTimeout继续执行timetojump，此时的second已经减1了，这样就实现了html倒计时的效果，
当second等于0时，就执行location.href跳转到jumpurl，
我们将js代码存在static/javascript/timer.js中。然后设计一个warn.html，其样式如下：
*/

function timetojump(second,jumpurl){
    var timer= document.getElementById('timer');
    timer.innerHTML=second;
    if(--second>0){
        setTimeout("timetojump("+second+",'"+jumpurl+"')",1000);
        }
    else{
        location.href=jumpurl;
        }
    }