function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息
    $.get('/api/1.0/users',function (res) {
        if(res.re_code=='0'){
            $('#user-avatar').attr('src',res.user.avatar_url);
            $('#user-name').val(res.user.name)
        }else if(res.re_code=='4101'){
            location.href='/'
        }else {
            alert(res.msg)
        }
    });
    // TODO: 管理上传用户头像表单的行为

    // TODO: 管理用户名修改的逻辑

});

