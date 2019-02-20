var item_cart = [];
    function display_item_cart(){
        var ordered_items_list=document.getElementById("ordered_items_list");
        /*started with the now cart*/
        while(ordered_items_list.rows.length>0) {
            ordered_items_list.deleteRow(0);
        }
         /*get the items from the cart and push in to the shopping cart*/
        for(var items in item_cart){
            var row=ordered_items_list.insertRow();
            var cellName = row.insertCell(0);
            var cellQuantity = row.insertCell(1);
            cellName.innerHTML = item_cart[items].Name;
            cellQuantity.innerHTML = item_cart[items].Quantity;

        }

    }
    /*remove the cart item from the cart*/
function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    updateCartTotal()
}

    function AddtoCart(name,quantity){
       var singleProduct = {};
       singleProduct.Name=name;
       singleProduct.Quantity=quantity;

       //Add newly created product to our shopping cart
       item_cart.push(singleProduct);
       //call display function to show on the shopping cart

       display_item_cart();

    }

