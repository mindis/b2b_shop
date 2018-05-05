var curState = "";

function notify(text) {
    console.log(text);
    notifyCart(text);
}


function orderState() {
    if (cartSum < minOrderSum) {
        if (curState != "less") {
            $("#ok").addClass("disabled");
            $("#ok-span").popover("show");
        }
        curState = "less";
    } else {
        if (curState != "greater") {
            $("#ok").removeClass("disabled");
            $("#ok-span").popover("hide");
        }
        curState = "greater";
    }
}

function update(item) {
    var q = parseInt($(".item-quantity[data-product=" + item + "]").val());
    $(".item-price[data-product=" + item + "]").text(normalize(getItemPrice(item, q)));
    $(".item-sum[data-product=" + item + "]").text(normalize(getItemPrice(item, q) * q));
    updateCartSum(function () {
        $("#cart-total").text(normalize(cartSum));
        orderState();
    });
    updateDeliverySum(function () {
        $("#delivery-sum").text(normalize(deliverySum));
    });
    updateTotalSum(function () {
        $("#total").text(normalize(totalSum));
    });
}

$(document).ready(function () {
    $('#ok-span').popover({ trigger: "" });
    $("#nav_cart").attr("class", "active");
    $("#ok-span").attr("data-content", "Минимальная сумма заказа " + normalize(minOrderSum) + "р. ");
    orderState();

    $(".item-del").click(function () {
        var item = $(this).attr("data-product");
        $(".item-quantity[data-product=" + item + "]").val(0);
        setInCart(item, 0, function (data, status) {
            if (data == 'error') {
                notifyId('#btn_rm_' + item, 'ошибка');
                $("#tr_" + item).hide();
            } else if (data == 'not authenticated') {
                notifyId('#btn_rm_' + item, 'Для добавления товаров в корзину, пожалуйста, войдите или зарегистрируйтесь.');
                $("#tr_" + item).hide();
            } else if (data == 'stored quantity is too small') {
                notifyId('#btn_rm_' + item, 'на складе нет столько товаров');
                $("#tr_" + item).hide();
            } else {
                notifyId('#btn_rm_' + item, 'обновлено');
                $("#tr_" + item).hide();
            }
            update(item);
        });
        //update(item);
        $("#tr_" + item).hide();
    });

    $(".item-quantity").on('change keyup paste', function () {
        var item = $(this).attr("data-product");
        var q = parseInt($(".item-quantity[data-product=" + item + "]").val());
        console.log(item, q);
        setInCart(item, q, function (data, status) {
            if (data == 'error') {
                notifyId('#btn_rm_' + item, 'ошибка');
            } else if (data == 'not authenticated') {
                notifyId('#btn_rm_' + item, 'Для добавления товаров в корзину, пожалуйста, войдите или зарегистрируйтесь.');
            } else if (data == 'stored quantity is too small') {
                notifyId('#btn_rm_' + item, 'на складе нет столько товаров');
            } else {
                notifyId('#btn_rm_' + item, 'обновлено');
            }
            update(item);
        });
    });

    $(".item-quantity").on('mouseover', function () {
        var item = $(this).attr("data-product");
        var q = parseInt($(".item-quantity[data-product=" + item + "]").val());
        console.log(item, q);
        setInCart(item, q, function (data, status) {
            console.log(data);
        });
        update(item);
    });

    $(".item-quantity").each(function () {
        var item = $(this).attr("data-product");
        //console.log(cart);
        $(".item-quantity[data-product=" + item + "]").val(cart[item]);
        update(item);
    });

    $('#ok-span').popover({ trigger: "" });
    $('[data-toggle="popover"]').popover({ trigger: "hover" });
});
