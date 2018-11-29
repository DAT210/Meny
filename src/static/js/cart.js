window.onload = init;

//site needs ajax for getting the information from the database
var cart;

class Cart
{
    constructor()
    {
        this.cartitems = [];
        this.totalprice = 0;
    }

    addcartitem(cartitem)
    {
        var duplicates = false;
        if (this.cartitems.length > 0)
        {
            var reply = this.checkcart(cartitem);
            duplicates = reply.itemincart;
        }
        if (duplicates === true)
        {
            this.cartitems[reply.index].amount += cartitem.amount;  //just update the amount
        }
        else
        {
            if (cartitem instanceof Course) //|| typeof cartitem === Course)
            {
                this.cartitems.push(cartitem);
                this.cartitems.sort()
            }
        }
    }

    removecartitem(cartitem)
    {
       if (cartitem instanceof Course) //|| typeof selection === 'string')
        {
            const index = this.cartitems.indexOf(cartitem);
            if (index > -1)
            {
                this.cartitems.splice(index, 1);
                this.cartitems.sort();
            }
        }
    }

    removecartitembyindex(index)
    {
        if (index > -1)
        {
            this.cartitems.splice(index,1);
            this.cartitems.sort();
        }
    }

    mergecartitems(cartitem1,cartitem2,idx1,idx2)
    {
        if (cartitem1 instanceof Course && cartitem2 instanceof Course)
        {

            if (cartitem1.equals(cartitem2) && idx1 !== idx2)
            {
                var combinedcourse = new Course(cartitem1.ID, cartitem1.name, cartitem1.price, cartitem1.amount+cartitem2.amount,cartitem1.editable);
                combinedcourse.selectionArray = cartitem1.selectionArray;

                if (idx1 > -1 && idx2 > -1)
                {
                    if (idx1 > idx2)
                    {
                        this.cartitems.splice(idx1, 1);
                        this.cartitems.splice(idx2, 1, combinedcourse); //since cart is always sorted by name the two duplicate items should be right next to each other in the array
                    }
                    else
                    {
                        this.cartitems.splice(idx2,1);
                        this.cartitems.splice(idx1,1,combinedcourse);
                    }
                }

            }
        }
    }

    checkcart(cartitem)
    {
        var response = {itemincart:false,index:-1};

        if (cartitem instanceof Course)
        {
            for (var idx=0;idx<this.cartitems.length;idx++)
            {
                if (cartitem.equals(this.cartitems[idx]))
                {
                    response.itemincart = true;
                    response.index = idx;
                    break;
                }
            }
        }
        return response;
    }

    getduplicateitem(cartitem)
    {
        if (cartitem instanceof Course)
        {
            for (var idx=0;idx<this.cartitems.length;idx++)
            {
                if (cartitem.equals(this.cartitems[idx]))
                {
                    return this.cartitems[cartitem];
                }
            }
        }
        var emptycourse = new Course(0,"Empty",0,0);
        return emptycourse;
    }
}

class Course
{
    constructor(ID, name, price,amount,editable)
    {
        this.ID = ID;
        this.name = name;
        this.selectionArray = [];
        this.price = price;
        this.amount = amount;
        this.editable = editable;
    }

    addSelection(selection)
    {
        if (selection instanceof Selection)
        {
            if (!this.selectionArray.includes(selection))
            {
                this.selectionArray.push(selection);
                this.selectionArray.sort();
            }
        }
    }

    removeSelection(selection)
    {
        if (selection instanceof Selection)
        {
            const index = this.selectionArray.indexOf(selection);
            if (index > -1)
            {
                this.selectionArray.splice(index,1);
                this.selectionArray.sort();
            }
        }
    }

    equals(course)
    {
        if (!(course instanceof Course))
        {
            return false;
        }

        if (this.ID !== course.ID)
        {
            return false;
        }

        if (this.selectionArray.length !== course.selectionArray.length)
        {
            return false;
        }
        for (var i = 0; i < this.selectionArray.length; i++)
        {
            if (this.selectionArray[i].SID !== course.selectionArray[i].SID)
            {
                return false;
            }
        }
        return true;
    }
}

class Selection
{
    constructor(id,name,price,category)
    {
        this.SID = id;
        this.Sname = name;
        this.Sprice = price;
        this.Category = category;
    }

    editprice(price)
    {
        if (typeof price === "string")
        {
            price = parseFloat(price);
        }
        this.Sprice = price
    }
}

function init()
{
    console.log("Script loaded");
    //var detailsdivs = $(".details");

    var item = $(".item");
    $(item).click(showdetails);
    var cancel = $(".cancel");
    $(cancel).click(hidedetails);

    var addbutton = $(".additem");
    addbutton.click(addtoCartajax);

    var edititembtn = $("#addeditedbutton");
    edititembtn.click(addeditinfo);

    var canceleditbtn = $("#editcancelbutton");
    canceleditbtn.click(editcancel);

    var purchasebtn = $("#purchasebutton");
    purchasebtn.click(confirmpurchase);

    cart = new Cart();
}

function showdetails() //show current details information
{
    var parentdiv = $(this).parent();
    var siblingdiv = $(parentdiv).siblings("div");

    var detailsdivs = $(".details");

    for (var i=0;i<detailsdivs.length;i++)
    {
        if (siblingdiv[0] === detailsdivs[i])
        {
            $(siblingdiv[0]).toggle("fast");
        }
        else
        {
            $(detailsdivs[i]).hide("fast");
        }
    }
    return false
}

function hidedetails()  //hide details information
{
    var parent = $(this).parent();
    $(parent).hide("fast")
}

function addtoCartajax()    //add a cart item to the cart, then updates the cart
{
    var select = $(this).siblings("select")[0];
    var selectid = $(select).attr("id");
    var selectarr = selectid.split("_");
    var amountselected = $(select).val();
    var amount = parseInt(amountselected);
    var id = selectarr[1];

    $.get("/getcourseinfo",{"course_id": id}, function (data)
    {
        var result = JSON.parse(data);
        console.log(result);

        var name = result[id]["c_name"];
        var price = parseFloat(result[id]["price"]);
        var editable = false;
        if (result[id]["selections"].length > 0)
        {
            editable = true;
        }
        var newcourse = new Course(id,name,price,amount,editable);
        cart.addcartitem(newcourse);
        updatecart();
    });
}

function deletecartitem()   //deletes chosen cart item from the cart object and then updates the cart
{
    var chosencartitem = $(this).parent()[0];
    var id=$(chosencartitem).attr("id");
    var arr = id.split("_");
    var index = parseInt(arr[1]);
    cart.removecartitembyindex(index);
    updatecart();

    if (cart.cartitems === 0)
    {
        $("#shoppingcart").hide();
    }

    return false
}

function edititem() //creates the edit popupmenu dependent on the selected course.
{
    var editoptions = $("#editoptions");
    editoptions.html("");
    var chosenitem = $(this).parent();
    var itemid = $(chosenitem).attr("id");
    var itemidarr = itemid.split("_");
    var itemidx = parseInt(itemidarr[1]);
    var chosencourse = cart.cartitems[itemidx];
    var courseid = chosencourse.ID;

    $.get("/getselectioncategory", function (data2) //create the selection categories for the edit page
    {
        var res2 = JSON.parse(data2);

        for(var sc=0;sc<res2.length;sc++)   //create the selection category divide on the editpage
        {
            var categoryname = res2[sc]["sc_name"];
            var catarr = categoryname.split(" ");
            var cateid = catarr[catarr.length-1];   //unique name
            var selectioncourse =$("<div></div>");
            $(selectioncourse).addClass("selcategory");
            $(selectioncourse).text(res2[sc]["sc_name"]);
            $(selectioncourse).attr("id",cateid);
            editoptions.append(selectioncourse)
        }

        $.get("/getcourseselection",{"course_id": courseid}, function (data1)   //place the selection in their proper categories
        {
            var result = JSON.parse(data1);
            console.log(result);
            if (result.length === 0) {
                alert("Cannot edit this item!")
            }
            else
            {
                var blockpage = $(".blockpage");
                $(blockpage).show();
                var editpage = $("#editpage");
                $(editpage).show();
                var category = $(".selcategory");

                for (var i=0;i<result.length;i++)
                {
                    var selection = result[i];

                    for (var j=0;j<$(category).length;j++)
                    {
                        var currentselectioncategory = $(category[j]).attr("id");
                        var selectioncategory = selection["sc_name"];
                        var selectionarr = selectioncategory.split(" ");
                        var currentcatid = selectionarr[selectionarr.length-1];
                        if (currentcatid === currentselectioncategory)
                        {
                            var after = $("<br />");
                            var label = $("<label></label>");
                            var newcheckbox = $("<input type='checkbox' />");
                            newcheckbox.attr("name",selection["sc_id"]+"_"+selection["s_name"]);
                            if (typeof selection["ingredient"] !== "undefined")
                            {
                                newcheckbox.attr("id",itemidx+"_"+selection["sc_id"]+"_ingredient"+selection["ingredient"]["i_id"]+"_"+selection["s_id"]);
                                newcheckbox.attr("value",itemidx+"_"+selection["sc_id"]+"_ingredient"+selection["ingredient"]["i_id"]+"_"+selection["s_id"]);
                            }
                            else
                            {
                                newcheckbox.attr("id", itemidx + "_" + selection["sc_id"] + "_" + selection["s_id"]);
                                newcheckbox.attr("value", itemidx + "_" + selection["sc_id"] + "_" + selection["s_id"]);
                            }
                            newcheckbox.click(checkeditboxes);
                            label.attr("for",itemidx+"_"+selection["sc_id"]+"_"+selection["s_name"]);
                            if (currentselectioncategory !== "removable" && selection["s_price"] != "None")
                            {
                                label.text(selection["s_name"] + " " +selection["s_price"]+"$");
                            }
                            else
                            {
                                label.text(selection["s_name"] + " " + 0.0 + "$");
                            }

                            for (var sel=0;sel<chosencourse.selectionArray.length;sel++) //check whether the selection is already been selected for the current cart item
                            {

                                if(selection["s_name"] === chosencourse.selectionArray[sel].Sname && selection["s_id"] === chosencourse.selectionArray[sel].SID)
                                {
                                    //newcheckbox.prop("checked",true)  //documentation said this was the way to check checkboxes, but didn't work during the creation of the checkbox
                                    newcheckbox.attr("checked",true);
                                }
                            }
                            $(category[j]).append(after);
                            $(category[j]).append(label);
                            $(category[j]).append(newcheckbox);
                        }
                    }
                }
            }
        });
    });
    return false;
}

function checkeditboxes()   //checks whether or not an addable and removable checkboxes contradict eachother
{
    var teststring = "ingredient";

    if ($(this).attr("id").includes(teststring))
    {
        var checkbox = $("input:checkbox");
        for (var ind=0;ind<checkbox.length;ind++)
        {
            var id = $(checkbox[ind]).attr("id");   //cartindx_selectioncategory_ingredientid_selectionid
            var selectedid = $(this).attr("id");

            if (id.includes(teststring) && $(checkbox[ind]).prop("checked") === true && id !== selectedid)
            {
               var arrid = id.split("_");
               var ingredientid = arrid[arrid.length-2];
               var selectioncategory = arrid[1];
               var selectedarrid = selectedid.split("_");
               var selectedingredientid = selectedarrid[selectedarrid.length-2];
               var selectedselectioncategory = selectedarrid[1];

               if (ingredientid === selectedingredientid && selectedselectioncategory <3 && selectioncategory < 3)  //only revert the checkboxes when someone is wants to add ingredient and to remove the same ingredient or vice versa
               {
                   $(checkbox[ind]).prop("checked",false);
               }
            }
        }
    }
}

function editcancel()   //cancels the edit for the chosen course
{
    var blockpage = $(".blockpage");
    $(blockpage).hide();
    var editpage = $("#editpage");
    $(editpage).hide();
}

function addeditinfo()  //add the chosen selections to the course
{
    var allempty = true;
    var checkinfoarr = [];
    var checkboxes = $("input:checkbox");
    var ischecked = $("input:checkbox:checked");
    var checkboxid = $(checkboxes[0]).attr("id");
    var idarr = checkboxid.split("_");
    var cartidx = parseInt(idarr[0]);

    if (ischecked.length === 0 && cart.cartitems[cartidx].selectionArray.length === 0)    //if none of the checkboxes were 'checked' and the item has no selections
    {
        editcancel();
    }
    else
    {
        for (var c = 0; c< checkboxes.length; c++)
        {
            if ($(checkboxes[c]).prop("checked") === true)
            {
                allempty = false
            }
        }
        if (allempty === true)
        {
            cart.cartitems[cartidx].selectionArray = checkinfoarr;
            updatecart();

            var editpage = $("#editpage");
            $(editpage).hide();
            var blockpage = $(".blockpage");
            $(blockpage).hide();
        }
        else
        {
            for (var ch = 0; ch < checkboxes.length; ch++)
            {
                if ($(checkboxes[ch]).prop("checked") === true)
                {
                    var value = $(checkboxes[ch]).attr("value");
                    var valuearr = value.split("_");
                    var id = valuearr[valuearr.length - 1];

                    $.get("/getselectioninfo", {"selection_id": id}, function (data)
                    {
                        var result = JSON.parse(data);
                        var selectioninfo = result[0]; //there will always be just 1 object in this array
                        var newSelection;
                        console.log(selectioninfo["s_price"])
                        if (parseInt(selectioninfo["sc_id"]) === 2  || selectioninfo["s_price"] == "None") {   //check if the category class is removable
                            newSelection = new Selection(selectioninfo["s_id"], selectioninfo["s_name"], 0.0, selectioninfo["sc_id"]);
                        }
                        else
                        {
                            newSelection = new Selection(selectioninfo["s_id"], selectioninfo["s_name"], parseFloat(selectioninfo["s_price"]), selectioninfo["sc_id"]);
                        }

                        checkinfoarr.push(newSelection);
                        cart.cartitems[cartidx].selectionArray = checkinfoarr;

                        for (var d = 0; d < cart.cartitems.length; d++)   //checking for duplicate items in the menu
                        {
                            if (cart.cartitems[cartidx].equals(cart.cartitems[d]) && cartidx !== d) //if there exist 2 identical objects!
                            {
                                cart.mergecartitems(cart.cartitems[cartidx], cart.cartitems[d], cartidx, d);
                                break;
                            }
                        }
                        updatecart();


                        //close the edit functionality
                        var editpage = $("#editpage");
                        $(editpage).hide();
                        var blockpage = $(".blockpage");
                        $(blockpage).hide();
                    });
                }

            }
        }
    }
}

function updatecart()   //creates and updates the cart dependent on the cart object
{
    var shoppingcart = $("#shoppingcart");
    var shoppingitems = $("#shoppingitems");
    $(shoppingitems).html("");
    var cartlenth = cart.cartitems.length;
    if (cartlenth > 0)
    {
        for (var cartind = 0;cartind<cartlenth;cartind++)
        {
            var cartitem = $("<div></div>");
            cartitem.attr("class","cartitem");
            cartitem.attr("id","cart_"+cartind);
            cartitem.text(cart.cartitems[cartind].name);

            var amountdiv = $("<div></div>");
            amountdiv.addClass("amount");
            amountdiv.attr("id","amount_"+cartind);
            amountdiv.text(cart.cartitems[cartind].amount + "x");
            amountdiv.val(cart.cartitems[cartind].amount);
            cartitem.append(amountdiv);

            var divprice = $("<div></div>");
            var price = cart.cartitems[cartind].price*cart.cartitems[cartind].amount;
            var dec2price = price.toFixed(2);
            divprice.attr("class","price");
            divprice.attr("id","price_"+cartind);
            divprice.text(dec2price+"$");
            divprice.val(dec2price);
            cartitem.append(divprice);

            var filterlist = $("<div></div>");
                filterlist.attr("class","filterlist");
                filterlist.attr("id","filterlist_"+cartind);
                cartitem.append(filterlist);
            if (cart.cartitems[cartind].selectionArray.length > 0)  //if the cartitem has selections!
            {
                var ul = $("<ul></ul>");    //create the list

                for (var idx = 0;idx<cart.cartitems[cartind].selectionArray.length;idx++)   //add selections to the cart item
                {
                    var li = $("<li></li>");

                    var extraprice = cart.cartitems[cartind].selectionArray[idx].Sprice * cart.cartitems[cartind].amount;
                    var dec2extraprice = extraprice.toFixed(2);
                    $(li).text(cart.cartitems[cartind].selectionArray[idx].Sname+" "+dec2extraprice+"$");
                    $(li).attr("id","filterid_"+cartind+"_"+idx);
                    ul.append(li);
                }
                filterlist.append(ul);
            }
            var editbutton = $("<a href='#'></a>");
            editbutton.attr("id", "itemeditbutton_" + cartind);
            editbutton.text("Edit");
            if(cart.cartitems[cartind].editable === true)
            {
                editbutton.addClass("btn btn-info btn-sm editbutton");
            }
            else
            {
                editbutton.addClass("btn btn-info btn-sm editbutton disabled");
            }
            editbutton.click(edititem);
            cartitem.append(editbutton);

            var deletebutton = $("<a href='#'></a>");
            deletebutton.attr("class","deletebutton btn btn-danger btn-sm ");
            deletebutton.text("Remove");
            deletebutton.click(deletecartitem);
            cartitem.append(deletebutton);
            shoppingitems.append(cartitem);
        }
        shoppingcart.show();
    }
    else
    {
        shoppingcart.hide();
    }
    updatetotalcost();
}

function updatetotalcost()  //updates the total cost in the cart, both in the cart object and visibly on the webpage
{
    var totalvalue = $("#totalvalue");
    totalvalue.text("");    //total cost resets everytime a new item is added!
    var totalcost = 0;

    for (var p=0;p<cart.cartitems.length;p++)
    {
        var additionalcost = 0;
        var currentprice = cart.cartitems[p].price;
        var selectionlist = cart.cartitems[p].selectionArray;
        var amount = cart.cartitems[p].amount;
        for (var s=0;s<selectionlist.length;s++)
        {
            additionalcost += selectionlist[s].Sprice*amount;
        }
        var cost = amount*currentprice;
        totalcost += cost+additionalcost;
        var twodectotalcost = totalcost.toFixed(2);


    }
    if (totalcost > 0)
    {
        cart.totalprice = parseFloat(twodectotalcost);
        totalvalue.text(cart.totalprice + "$");
    }
    else
    {
        cart.totalprice = 0;
        totalvalue.text(cart.totalprice + "$");
    }
    console.log(cart);
}

function confirmpurchase()  //send the cart information to orders group
{
    console.log("Purchase initiated!");
    var jsoncart = JSON.stringify(cart);
    console.log(jsoncart);
}
