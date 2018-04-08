function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.popup_con').fadeIn('fast');
    //没有实名认证不能进入该页面
    $.get('/api/1.0/users/auth',function (res) {
        if(res.re_code=='0'){
            //判断是否实名认证
            if(!res.user_auth.real_name || !res.user_auth.id_card){
                location.href='/auth.html'
            }
        }else if(res.re_code=='4101'){
            location.href='/login.html'
        }else {
            alert(res.msg)
        }
    });
    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas',function (res) {
        if(res.re_code=='0'){
            render_template=template('areas-tmpl',{'areas':res.areas});
            $('#area-id').html(render_template);
            $('.popup_con').fadeOut('fast');
        }else {
            alert(res.msg);
            $('.popup_con').fadeOut('fast');
        }
    });
    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        $('.popup_con').fadeIn('fast');
        event.preventDefault();
        var params={};
         // 收集form表单中需要提交的input标签,放在一个数组对象中
        // map 遍历对象，比如说数组对象
        // obj == {name: "title", value: "1"}
        $(this).serializeArray().map(function (obj) {
            params[obj.name]=obj.value;
        });
        // 收集房屋设施信息
        var facilities=[];
        //获取所有设施被选中的复选框
        $(':checkbox:checked[name=facility]').each(function (i,ele) {
            //存到列表
            facilities[i]=ele.value;
        });
        //赋值给params
        params['facility']=facilities;
        $.ajax({
                    url:'/api/1.0/houses',
                    type:'post',
                    data:JSON.stringify(params),
                    contentType:'application/json',
                    headers:{'X-CSRFToken':getCookie('csrf_token')},
                    success:function(response){
                        if(response.re_code=='0'){
                            // 成功
                            $('.popup_con').fadeOut('fast');
                            $('#form-house-info').hide();
                            $('#form-house-image').show();
                            $('#house-id').val(response.data.house_id);
                        }else if(response.re_code=='4101'){
                            location.href='/login.html'
                        }else {
                            alert(response.msg);
                            $('.popup_con').fadeOut('fast');
                        }
                    }
                });
    });
    // TODO: 处理图片表单的数据
    $('#form-house-image').submit(function (event) {
        // 开始等待加载特效
        $('.popup_con').fadeIn('fast');
        event.preventDefault();
        var house_id=$('#house-id').val();
        $(this).ajaxSubmit({
            url:'/api/1.0/houses/'+house_id+'/images',
            type:'post',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (res) {
                if(res.re_code=='0'){
                    // 拼接显示房屋图片
                    $('.house-image-cons').append('<img src="'+res.data.url+'" alt="房屋图片" />');
                    // 结束等待加载特效
                    $('.popup_con').fadeOut('fast');
                }else if(res.re_code=='4101'){
                    location.href='/login.html'
                }else {
                    alert(res.msg);
                    $('.popup_con').fadeOut('fast');
                }
            }
        });
    });
});