function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    // 判断用户是否登录
    $.get('/api/1.0/sessions',function (res) {
        if(!res.user.user_id && !res.user.name){
            //未登录
            location.href='/login.html'
        }
    });

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg("日期有误，请重新选择!");
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24);
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var queryData = decodeQuery();
    var houseId = queryData["hid"];

    //  获取房屋的基本信息
    $.get('/api/1.0/houses/detail/'+houseId,function (res) {
        if(res.re_code=='0'){
            $('.house-info>img').attr('src',res.data.house.img_urls[0]);
            $('.house-text h3').text(res.data.house.title);
             $('.house-text span').text(parseFloat((res.data.house.price)/100).toFixed(2));
        }else {
            alert(res.msg)
        }
    });
    // 订单提交
    $('.submit-btn').on('click',function () {
        var start_date=$('#start-date').val(),
            end_date=$('#end-date').val();
         if (!start_date || !end_date) {
            alert('请输入时间');
            return;
        }
        var params={
            'start_date':start_date,
            'end_date':end_date,
            'house_id':houseId
        };
        $.ajax({
                    url:'/api/1.0/orders',
                    type:'post',
                    data:JSON.stringify(params),
                    contentType:'application/json',
                    headers:{'X-CSRFToken':getCookie('csrf_token')},
                    success:function(response){
                        if(response.re_code=='0'){
                            // 成功
                            location.href='/orders.html?role=own'
                        }else if(response.re_code=='4101'){
                            location.href='/login.html'
                        }else {
                            alert(response.msg)
                        }
                    }
                });
    });
});
