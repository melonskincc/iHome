function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var uuid = "";
var last_uuid='';
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    //向后端发送请求：/imageCode?uuid=uuid&last_uuid=last_uuid
    uuid=generateUUID();  //生成UUID
    var url='/api/1.0/imageCode?uuid=' + uuid+ '&last_uuid=' + last_uuid;   //拼接请求地址
    $('.image-code>img').attr('src',url);  //设置img的src属性
    last_uuid = uuid   //设置上一个UUID
}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // TODO: 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    var phone_num=$('#mobile').val(),
        image_code=$('#imagecode').val(),
        csrf_token=getCookie('csrf_token');
    var params={
        'uuid':uuid,
        'phone_num':phone_num,
        'image_code':image_code
    };
    $.ajax({
        url:'/api/1.0/smsCode',
        type:'post',
        data:JSON.stringify(params),
        contentType:'application/json',
        headers:{'X-CSRFToken':csrf_token},
        success:function (res) {
            if (res.re_code == '0'){
                $('#phonecode').attr('placeholder','验证码发送成功')
                // 验证码发送成功，倒计时60秒
                var time=60;
                var timer=setInterval(function () {
                    $('.phonecode-a').html(time);
                    time-=1;
                    if (time<0){
                    clearInterval(timer);
                    $('.phonecode-a').html('获取验证码');
                    $('.phonecode-a').attr('onclick','sendSMSCode();')
                    }
                },1000)
            }else {
                alert(res.msg);
                $('.phonecode-a').attr('onclick','sendSMSCode();')
            }
        }
    })
}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // TODO: 注册的提交(判断参数是否为空)
    $('.form-register').submit(function (event) {
        // 阻止自己默认的提交表单事件
        event.preventDefault();
        // 获取后端需要的数据，电话号，密码，短信验证码
        var phone_num=$('#mobile').val(),
            phonecode=$('#phonecode').val(),
            password=$('#password').val(),
            regix=/^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$/;
        // 判断是否为空,校验
        if(!regix.exec(phone_num)){
            $('#mobile-err span').text('手机号错误');
            $('#mobile-err').show()
        }
        if(!phonecode) {
            $('#phone-code-err span').text('手机验证码不能为空！');
            $('#phone-code-err').show();
        }
        if(!password){
            $('#password-err span').text('密码不能为空!');
            $('#password-err').show()
        }
        //组织参数
        var params={
            'phone_num':phone_num,
            'phonecode':phonecode,
            'password':password
        };
        // 提交表单
        $.ajax({
            url:'/api/1.0/users',
            type:'post',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function(response){
                if(response.re_code=='0'){
                    // 成功跳转到首页
                    alert(response.msg);
                    location.href='/'
                }else {
                    alert(response.msg)
                }
            }
        });
    });
});
