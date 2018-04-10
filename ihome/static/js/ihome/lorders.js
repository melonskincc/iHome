//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
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

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // 查询房东的订单
        var queryData = decodeQuery();
    var role = queryData["role"];
    // 查询房客订单
    $.get('/api/1.0/orders?role='+role,function (res) {
        if(res.re_code=='0'){
            render_template=template('orders-list-tmpl',{'orders':res.data.order_list});
            $('.orders-list').html(render_template);
        //  查询成功之后需要设置接单和拒单的处理
        $(".order-accept").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
            $('.modal-accept').on('click',function () {
                $.ajax({
                            url:'/api/1.0/orders/status/'+orderId+'?action=accept',
                            type:'put',
                            headers:{'X-CSRFToken':getCookie('csrf_token')},
                            success:function(response){
                                if(response.re_code=='0'){
                                    // 成功，模态框隐藏，订单状态改为待支付
                                    $('.order-text').find('span').html('待支付');
                                    $('.orders-list li[order-id='+orderId+']').find('.order-operate').hide();
                                    $('.order-operate').hide();
                                    $('#accept-modal').modal('hide');
                                }else if(response.re_code=='4101'){
                                    location.href='/login.html'
                                }else {
                                    alert(response.msg)
                                }
                            }
                        });
            })
        });

        $(".order-reject").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-reject").attr("order-id", orderId);
            $('.modal-reject').on('click',function () {
                var reason=$('#reject-reason').val();
                if(!reason){
                    alert('请填写拒单理由！');
                    return;
                }
                $.ajax({
                            url:'/api/1.0/orders/status/'+orderId+'?action=reject',
                            type:'put',
                            data:JSON.stringify({'reason':reason}),
                            contentType:'application/json',
                            headers:{'X-CSRFToken':getCookie('csrf_token')},
                            success:function(response){
                                if(response.re_code=='0'){
                                      // 成功，模态框隐藏，订单状态改为已拒单
                                    $('.orders-list li[order-id='+orderId+']').find('.order-text span').html('已拒单');
                                    $('.orders-list li[order-id='+orderId+']').find('.order-text ul').append('<li>拒单原因：'+reason+'</li>');
                                    $('.orders-list li[order-id='+orderId+']').find('.order-operate').hide();
                                    $('#reject-modal').modal('hide');
                                }else if(response.re_code=='4101'){
                                    location.href='/login.html'
                                }else {
                                    alert(response.msg)
                                }
                            }
                        });
            })

        });

        }else if(res.re_code=='4101'){
            location.href='/login.html'
        }else {
            alert(res.msg)
        }
    });

});
