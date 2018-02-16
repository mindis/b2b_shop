function updatePricelist(product, tag) {
    let obj = ".item-price[data-product=" + product + "][data-tag=" + tag + "]";
    let item = $(".variant-selector[data-product=" + product + "][data-tag=" + tag + "] :selected").val();
    let fill = "<div><table class='table table-striped'><thead><tr><th>кол-во (" + items[item].measure + ")</th><th>цена (руб)</th></tr></thead><tbody>";

    let keys = Object.keys(priceList[item]).map(function(num) {
        return parseInt(num);
    });

    keys.sort(function(a, b) { return a - b; });
    console.log(keys);
    keys.forEach(function(val, index, array){
        fill += "<tr>";
        fill += "<th>" + val + "</th>";
        fill += "<th>" + normalize(priceList[item][val]) + "</th>";
        fill += "</tr>";
    });

    fill += "</tbody></table></div>"
    $(obj).attr("data-content", fill);
}

function notify(text) {
    console.log(text);
    notifyCart(text);
}

function update(product, tag) {
	var q = $(".quantity-selector[data-product=" + product + "][data-tag=" + tag + "]").val();
	var item = $(".variant-selector[data-product=" + product + "][data-tag=" + tag + "] :selected").val();

	$(".item-price[data-product=" + product + "][data-tag=" + tag + "]").text(normalize(getItemPrice(item, q + getQuantityInCart(item))));

	$(".item-count[data-product=" + product + "][data-tag=" + tag + "]").text(items[item].quantity);

	$(".product-sum[data-product=" + product + "][data-tag=" + tag + "]").text(
		normalize(getItemPrice(item, q + getQuantityInCart(item)) * q) + " р");
    updatePricelist(product, tag);
	//console.log(stored[item], item)
}

$(document).ready(function() {
	$(".btn-add-cart").click(function(){
		var tag = $(this).attr("data-tag");
		var product = $(this).attr("data-product");
        update(product, tag);
        var q = $(".quantity-selector[data-product=" + product + "][data-tag=" + tag + "]").val();
		var item = $(".variant-selector[data-product=" + product + "][data-tag=" + tag + "] :selected").val();
		console.log(item, q, tag, product);

		addToCart(item, q, function(data, status){  
            if (data == 'error') { 
                notifyId('#btn_' + product + '_' + tag, 'ошибка');
            } else if (data == 'not authenticated') {
                notifyId('#btn_' + product + '_' + tag, 'Для добавления товаров в корзину, пожалуйста, войдите или зарегистрируйтесь.');
            } else if (data == 'stored quantity is too small'){
                notifyId('#btn_' + product + '_' + tag, 'на складе нет столько товаров');
            } else {
                notifyId('#btn_' + product + '_' + tag, 'добавлено ' + q.toString() + ' ' + items[item].measure);
            }
            $(".quantity-selector[data-product=" + product + "][data-tag=" + tag + "]").val(0);
            update(product, tag);
        });
    });
    $(".variant-selector").change(function(){
        var tag = $(this).attr("data-tag");
		var product = $(this).attr("data-product");
        update(product, tag);
    });
    $(".quantity-selector").on('change keyup paste mouseover', function(){
    	var tag = $(this).attr("data-tag");
		var product = $(this).attr("data-product");
        update(product, tag);
    });

    $(".btn-add-cart").each(function() {
    	var tag = $(this).attr("data-tag");
		var product = $(this).attr("data-product");
        update(product, tag);
    });


});