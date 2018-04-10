function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//点击退出按钮时执行的函数
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

    //  在页面加载完毕之后去加载个人信息
    $.get('/api/1.0/users',function (res) {
        if(res.re_code=='0'){
            // 加载头像
            $('#user-avatar').attr('src',res.user.avatar_url);
            $('#user-name').text(res.user.name);
            $('#user-mobile').text(res.user.phone_num);
        }else if (res.re_code=='4101'){
            // 未登录，跳转到首页
            location.href='/'
        }else {
            alert(res.msg)
        }
    });
});
