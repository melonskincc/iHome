function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TODO: 点击退出按钮时执行的函数
function logout() {
    $.ajax({
        url:'/api/1.0/sessions',
        type:'delete',
        headers:{'X-CSRFToken':getCookie('csrf_token')},
        success:function (res) {
            if(res.re_code=='0'){
                alert(res.msg);
                location.href='/'
            }else {
                alert(res.msg)
            }
        }
    });
}

$(document).ready(function(){

    // TODO: 在页面加载完毕之后去加载个人信息

});
