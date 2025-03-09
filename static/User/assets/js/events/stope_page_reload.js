// Disable page reload in create account (signup)
$(document).on('submit', '#signup_form', function(e){
    e.preventDefault();

    var username = $('#username').val();
    var email = $('#email').val();
    var password = $('#password').val();
    var cpassword = $('#cpassword').val();
    
    var form_data = new FormData();

    form_data.append('username', username);
    form_data.append('email', email);
    form_data.append('password', password);
    form_data.append('cpassword', cpassword);

    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: "/signup",
        type: "POST",
        mimeType: "multipart/form-data",
        contentType: false,
        processData: false,
        data: form_data,
        headers: {'X-CSRFToken': csrfToken},
        dataType: "json",
        success: function(response){
            if(response.status == 200)
            {
                $("#signup_form").load(location.href + " #signup_form>*", "");

                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-success', 'text-success');
                myAlert.innerText = 'Your Account Is Created, Now Login First...';

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-success', 'text-success');
                    window.location.href = "signin_page";
                }, 2000);
            }
            else if(response.status == 400)
            {
                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-danger', 'text-danger');
                myAlert.innerText = response.error;

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-danger', 'text-danger');
                }, 5000);
            }
        }
    });
});

// Disable page reload in forgot password check email
$(document).on('submit', '#forgot_password_get_email_form', function(e){
    e.preventDefault();

    var email = $('#email').val();
    
    var form_data = new FormData();

    form_data.append('email', email);

    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: "/check_forgot_password_email",
        type: "POST",
        mimeType: "multipart/form-data",
        contentType: false,
        processData: false,
        data: form_data,
        headers: {'X-CSRFToken': csrfToken},
        dataType: "json",
        success: function(response){
            if(response.status == 200)
            {
                $("#forgot_password_get_email_form").hide();
                $("#send_otp_form").show();
                $('#getemail').val(response.email);
            }
            else
            {
                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-danger', 'text-danger');
                myAlert.innerText = response.error;

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-danger', 'text-danger');
                }, 5000);
            }
        }
    });
});

// Disable page reload in login (signin)
$(document).on('submit', '#signin_form', function(e){
    e.preventDefault();

    var usernameoremail = $('#usernameoremail').val();
    var password = $('#password').val();
    
    var form_data = new FormData();

    form_data.append('usernameoremail', usernameoremail);
    form_data.append('password', password);

    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: "/signin",
        type: "POST",
        mimeType: "multipart/form-data",
        contentType: false,
        processData: false,
        data: form_data,
        headers: {'X-CSRFToken': csrfToken},
        dataType: "json",
        success: function(response){
            if(response.status == 200)
            {
                window.location.href = "admin";
            }
            else if(response.status == 201)
            {
                window.location.href = "index";
            }else if(response.status == 202)
            {
                window.location.href = "vendor";
            }
            else if(response.status == 400)
            {
                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-danger', 'text-danger');
                myAlert.innerText = response.error;

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-danger', 'text-danger');
                }, 5000);
            }
        }
    });
});

// Disable page reload in get vendor account request
$(document).on('click', '#get_vendor_account_request', function(e){
    e.preventDefault();

    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: "get_vendor_account_request",
        type: "POST",
        mimeType: "multipart/form-data",
        contentType: false,
        processData: false,
        headers: {'X-CSRFToken': csrfToken},
        dataType: "json",
        success: function(response)
        {
            $(window).scrollTop(0);
            $("#get_vendor_account_request_form").load(location.href + " #get_vendor_account_request_form>*", "");
            if(response.status == 200)
            {
                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-success', 'text-success');
                myAlert.innerText = response.message;

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-success', 'text-success');
                }, 5000);
            }
            else
            {
                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-danger', 'text-danger');
                myAlert.innerText = "Sumthing want wrong please try again some time...";

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-ganger', 'text-danger');
                }, 5000);
            }
        }
    });
});

// Disable page reload in submit review
$(document).on('submit', '#product_review_form', function(e){
    e.preventDefault();

    var ratingValue = $('#ratingValue').val();
    var product_review_message = $('#product_review_message').val();
    var product_id = $('#product_id').val();
    
    var form_data = new FormData();

    form_data.append('ratingValue', ratingValue);
    form_data.append('product_review_message', product_review_message);
    form_data.append('product_id', product_id);

    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: "/add_review/" + product_id,
        type: "POST",
        mimeType: "multipart/form-data",
        contentType: false,
        processData: false,
        data: form_data,
        headers: {'X-CSRFToken': csrfToken},
        dataType: "json",
        success: function(response){
            if(response.status == 200)
            {
                $("#product_review_form").load(location.href + " #product_review_form>*", "");
                $("#Reviews_div").load(location.href + " #Reviews_div>*", "");
                $("#Reviews-count").load(location.href + " #Reviews-count>*", "");

                const stars = document.querySelectorAll('.fa-star');
                for (let i = 1; i < stars.length; i++) {
                    stars[i].classList.remove('filled');
                }
                document.getElementById('ratingValue').value = 1;

                const myAlert = document.getElementById('myAlert');
                myAlert.style.display = 'block';
                myAlert.classList.add('alert-success', 'text-success');
                myAlert.innerText = response.message;

                setInterval(function(){
                    $('.alert').fadeOut();
                    myAlert.style.display = 'none';
                    myAlert.classList.remove('alert-success', 'text-success');
                }, 5000);
            }
        }
    });
});

// Disable page reload in filter in product list
$(document).ready(function(){
    $(".filter-checkbox , #price-filter-btn").on("click", function(){
        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
                return element.value
            })
        })

        $.ajax({
            url: 'filter_product/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('Filtering Product...')
            },
            success: function(response){
                $("#filtered-product").html(response.data)
                $("#filtered-product-count").html(response.data_count)
            }
        })
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert("Price must between " + min_price + ' and ' + max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()
            return false
        }
    })
});

// Disable page reload in add / remove cart product to all page
$(".add-to-cart-btn").on("click", function(){
    let this_val = $(this)
    let index = this_val.attr("data-index")

    let product_id = $(".cart_product_id-" + index).val();
    let product_quantity = $(".cart_product_quantity-" + index).val();
    let product_name = $(".cart_product_name-" + index).val();
    let product_price = $(".product-price-" + index).text();
    let product_img = $(".cart_product_img-" + index).val();

    $.ajax({
        url: '/add-to-cart-product-detail',
        data: {
            'product_id' : product_id,
            'product_quantity' : product_quantity,
            'product_name' : product_name,
            'product_price' : product_price,
            'product_img' : product_img,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('add cart process...')
        },
        success: function(res){
            if(res.status == 200)
            {
                this_val.html('<i class="fi-rs-shopping-cart mr-5"></i>Remove')
                console.log('add cart successfull....')
                $(".cart-items-count").text(res.total_cart_items)
            }
            else if(res.status == 400)
            {
                this_val.html('<i class="fi-rs-shopping-cart mr-5"></i>Add')
                console.log('add cart successfull....')
                $(".cart-items-count").text(res.total_cart_items)
            }
        }
    })
})

$(".delete-product").on("click", function(){
    let product_id = $(this).attr('data-product')
    let this_val = $(this)

    $.ajax({
        url: '/delete_to_cart',
        data: {
            'id' : product_id
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(res){
            this_val.show()
            $(".cart-items-count").text(res.total_cart_items)
            $("#cart-list").html(res.data)
        }
    })
})

$(".update-product").on("click", function(){
    let product_id = $(this).attr('data-product')
    let product_quantity = $('.product_quantity-'+product_id).val()
    let this_val = $(this)

    $.ajax({
        url: '/update_to_cart',
        data: {
            'id' : product_id,
            'product_quantity' : product_quantity,
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(res){
            this_val.show()
            $(".cart-items-count").text(res.total_cart_items)
            $("#cart-list").html(res.data)
        }
    })
})