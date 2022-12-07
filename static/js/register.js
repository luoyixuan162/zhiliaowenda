function bindCaptchaBtnClick() {
    // $("#captcha-ptn")  $在整个网页加载完成后获取参数
    // # 表示 id=
    $("#captcha-ptn").on("click", function (event) {
        // $this：代表的是当前按钮的jQuery对象
        var $this = $(this);
        // 阻止默认的提交事件
        event.preventDefault();

        var email = $('input[name="email"]').val();
        if (!email) {
            alert("请先输入邮箱！");
            return;
        }
        // 通过js发送网络请求：Ajax：Async JavaScript And Xml
        $.ajax({
            url: '/user/captcha',
            method: "POST",
            data: {
                'email': email
            },
            success: function (res) {
                var code = res["code"];
                if (code == 200) {
                    // 验证码发送成功，取消点击事件
                    $this.off("click");
                    // 开始倒计时
                    var countDown = 60;
                    var timer =  setInterval(function () {
                        if(countDown>0){
                            $this.text(countDown+"秒后可重新发送")
                        }else {
                            $this.text("获取验证码");
                            // 倒计时结束，重新开启点击事件
                            bindCaptchaBtnClick();
                            // 倒计时结束，不再继续倒计时，要清除倒计时，否则会一直执行
                            clearInterval(timer)
                        }
                        countDown -= 1
                    }, 1000);
                    alert("验证码发送成功,请稍等。点击确定");
                } else {
                    alert(res["message"]);
                }
            },
            function(error){
                console.log(error);
                }
        })
    });  // $ 绑定事件      #表示 'id='


}

// 等网页文档所有元素都加载完成后再执行
$(function () {
    bindCaptchaBtnClick();
});
