$(function () {
    // 头像预览
    $('#avatar').change(function () {
        // 1.创建文件阅读器对象
        let avatar_img = new FileReader()
        // 2.获取用户上传的文件对象
        let up_avatar = $(this)[0].files[0];
        // 3.将文件对象交给阅读器对象解析
        avatar_img.readAsDataURL(up_avatar)
        // 4.等待文件阅读器加载完毕，利用文件阅读器将文件展示到前端页面，修改src属性，
        // avatar_img.result 获取图像路径
        avatar_img.onload = function () {
            $('#avatar_img').attr('src', avatar_img.result)
        }
    })
})



function cheackAvatar() {
    // 头像预览
    $('#avatar').change(function () {
        // 1.创建文件阅读器对象
        var avatar_img = new FileReader()
        // 2.获取用户上传的文件对象
        var up_avatar = $(this)[0].files[0];
        // 3.将文件对象交给阅读器对象解析
        avatar_img.readAsDataURL(up_avatar)
        // 4.等待文件阅读器加载完毕，利用文件阅读器将文件展示到前端页面，修改src属性，
        // avatar_img.result 获取图像路径
        avatar_img.onload = function () {
            $('#avatar_img').attr('src', avatar_img.result)
        }
    })
}







