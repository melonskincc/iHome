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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/search.html?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName="";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    location.href = url;
}

$(document).ready(function(){
    //  检查用户的登录状态
    $.get('/api/1.0/sessions',function (res) {
        if (res.re_code=='0'){
            // 响应成功
            if (res.user.user_id && res.user.name){
                //user_id和name都有数据，已登录
                $('.register-login').hide();
                $('.user-info').show();
                $('.user-info').find('a').text(res.user.name)
            }else {
                //未登录
                $('.register-login').show();
                $('.user-info').hide();
            }
        }else {
            alert(res.msg)
        }
    });
    //  获取幻灯片要展示的房屋基本信息
    $.get('/api/1.0/houses/index',function (res) {
        if(res.re_code=='0'){
            render_template=template('swiper-houses-tmpl',{'houses':res.data.houses});
            $('.swiper-wrapper').html(render_template);
        //  数据设置完毕后,需要设置幻灯片对象，开启幻灯片滚动
        var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationClickable: true
    });
        }else {
            alert(res.msg)
        }
    });

    // 获取城区信息,获取完毕之后需要设置城区按钮点击之后相关操作
    $.get('/api/1.0/areas',function (res) {
        if(res.re_code=='0'){
            // 初始化模板
            render_template=template('area-list-tmpl',{areas:res.areas});
            //将模板设置到指定的区域
            $('.area-list').html(render_template);
            $('.area-list a').click(function () {
                // 请选择地区按钮变成选中地址的名字
                $('#area-btn').html($(this).html());
                //设置搜索框area-id属性的值为选择中的aid，name为选中的aname
                $('.search-btn').attr('area-id',$(this).attr('area-id'));
                $('.search-btn').attr('area-name',$(this).html());
                // 隐藏模态框
                $('#area-modal').modal('hide');
            });
        }else {
            alert(res.msg)
        }
    });


    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
});
