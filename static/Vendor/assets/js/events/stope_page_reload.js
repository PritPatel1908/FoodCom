// Product
// Disable page reload in add product
$(document).on('click', '#add-product', function(e){
    e.preventDefault();

    var product_name = $('#product_name').val();
    var product_description = $('#product_description').val();
    var product_ingredients = $('#product_ingredients').val();
    var product_price = $('#product_price').val();
    var product_old_price = $('#product_old_price').val();
    var product_quantity = $('#product_quantity').val();
    var sub_category_id = $('#sub_category_id').val();
    var product_tags = $('#product_tags').val();
    
    var form_data = new FormData();

    form_data.append('product_name', product_name);
    form_data.append('product_description', product_description);
    form_data.append('product_ingredients', product_ingredients);
    form_data.append('product_price', product_price);
    form_data.append('product_old_price', product_old_price);
    form_data.append('product_quantity', product_quantity);
    form_data.append('sub_category_id', sub_category_id);
    form_data.append('product_tags', product_tags);
    form_data.append('product_img', $('#product_img')[0].files[0]);

    const fileInputs = document.querySelectorAll('#file-input-container input[type="file"]');
    fileInputs.forEach((fileInput) => {
        if (fileInput.files.length > 0) {
          for (let i = 0; i < fileInput.files.length; i++) {
            form_data.append('product_imgs', fileInput.files[i]);
          }
        }
    });
      
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: "add_product",
        type: "POST",
        mimeType: "multipart/form-data",
        contentType: false,
        processData: false,
        data: form_data,
        headers: {'X-CSRFToken': csrfToken},
        dataType: "json",
        success: function(response){
          $(window).scrollTop(0);
          $("#add_product").load(location.href + " #add_product>*", "");
          $("#my_div").load(location.href + " #my_div>*", "");
          if(response.status == 200)
          {
            document.getElementById("alert-success").style.display = 'block';
            document.getElementById("success").innerText = response.message;
            setInterval(function ()
            {      
              document.getElementById("alert-success").style.display = 'none';
            }, 5000);
          }
          else
          {
            document.getElementById("alert-danger").style.display = 'block';
            document.getElementById("danger").innerText = response.message;
            setInterval(function ()
            {      
              document.getElementById("alert-danger").style.display = 'none';
            }, 5000);
          }
        }
    });
});

// Disable page reload in update product
$(document).on('submit', '#edit_product', function(e){
  e.preventDefault();

  var product_id = $('#product_id').val();
  var product_name = $('#product_name').val();
  var product_description = $('#product_description').val();
  var product_ingredients = $('#product_ingredients').val();
  var product_price = $('#product_price').val();
  var product_old_price = $('#product_old_price').val();
  var product_quantity = $('#product_quantity').val();
  var sub_category_id = $('#sub_category_id').val();
  var product_tags = $('#product_tags').val();
  var product_image = $('#product_image').val();
  
  var form_data = new FormData();

  form_data.append('product_id', product_id);
  form_data.append('product_name', product_name);
  form_data.append('product_description', product_description);
  form_data.append('product_ingredients', product_ingredients);
  form_data.append('product_price', product_price);
  form_data.append('product_old_price', product_old_price);
  form_data.append('product_quantity', product_quantity);
  form_data.append('sub_category_id', sub_category_id);
  form_data.append('product_image', product_image);
  form_data.append('product_tags', product_tags);
  form_data.append('product_img', $('#product_img')[0].files[0]);
    
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: product_id + "/update_product",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#edit_product").load(location.href + " #edit_product>*", "");
        $("#my_div").load(location.href + " #my_div>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in delete product
$(document).on('click', '#delete-product', function(e){
  e.preventDefault();

  var product_id = $(this).data('item-id');

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "delete_product/" + product_id,
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#product_list").load(location.href + " #product_list>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Category
// Disable page reload in add category
$(document).on('click', '#add-category', function(e){
  e.preventDefault();

  var category_name = $('#category_name').val();
  
  var form_data = new FormData();

  form_data.append('category_name', category_name);
  form_data.append('category_img', $('#category_img')[0].files[0]);
    
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "add_category",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response){
        $(window).scrollTop(0);
        $("#add_category").load(location.href + " #add_category>*", "");
        $("#my_div").load(location.href + " #my_div>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in update category
$(document).on('click', '#edit-category', function(e){
  e.preventDefault();

  var category_id = $('#category_id').val();
  var category_name = $('#category_name').val();
  var category_image = $('#category_image').val();
  
  var form_data = new FormData();

  form_data.append('category_id', category_id);
  form_data.append('category_name', category_name);
  form_data.append('category_image', category_image);
  form_data.append('category_img', $('#category_img')[0].files[0]);
    
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: category_id + "/update_category",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#edit_category").load(location.href + " #edit_category>*", "");
        $("#my_div").load(location.href + " #my_div>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in delete category
$(document).on('click', '#delete-category', function(e){
  e.preventDefault();

  var category_id = $(this).data('item-id');

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "delete_category/" + category_id,
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#category_list").load(location.href + " #category_list>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Sub Category
// Disable page reload in add subcategory
$(document).on('click', '#add-subcategory', function(e){
  e.preventDefault();

  var subcategory_name = $('#subcategory_name').val();
  var category_id = $('#category_id').val();
  
  var form_data = new FormData();

  form_data.append('subcategory_name', subcategory_name);
  form_data.append('category_id', category_id);
  form_data.append('subcategory_img', $('#subcategory_img')[0].files[0]);
    
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "add_subcategory",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response){
        $(window).scrollTop(0);
        $("#add_subcategory").load(location.href + " #add_subcategory>*", "");
        $("#my_div").load(location.href + " #my_div>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in update subcategory
$(document).on('click', '#edit-subcategory', function(e){
  e.preventDefault();

  var subcategory_id = $('#subcategory_id').val();
  var category_id = $('#category_id').val();
  var subcategory_name = $('#subcategory_name').val();
  var subcategory_image = $('#subcategory_image').val();
  
  var form_data = new FormData();

  form_data.append('subcategory_id', subcategory_id);
  form_data.append('category_id', category_id);
  form_data.append('subcategory_name', subcategory_name);
  form_data.append('subcategory_image', subcategory_image);
  form_data.append('subcategory_img', $('#subcategory_img')[0].files[0]);
    
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: subcategory_id + "/update_subcategory",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#edit_subcategory").load(location.href + " #edit_subcategory>*", "");
        $("#my_div").load(location.href + " #my_div>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in delete category
$(document).on('click', '#delete-subcategory', function(e){
  e.preventDefault();

  var subcategory_id = $(this).data('item-id');

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "delete_subcategory/" + subcategory_id,
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#subcategory_list").load(location.href + " #subcategory_list>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in change basic detail in profile
$(document).on('submit', '#basic_profile_detail_form', function(e){
  e.preventDefault();

  var first_name = $('#first_name').val();
  var last_name = $('#last_name').val();
  var phone = $('#phone').val();
  var no_street_line = $('#no_street_line').val();
  var pincode = $('#pincode').val();
  var dob = $('#dob').val();
  var gender = $('#gender').val();
  var profile_image = $('#profile_image').val();
  
  var form_data = new FormData();

  form_data.append('first_name', first_name);
  form_data.append('last_name', last_name);
  form_data.append('phone', phone);
  form_data.append('no_street_line', no_street_line);
  form_data.append('pincode', pincode);
  form_data.append('dob', dob);
  form_data.append('gender', gender);
  form_data.append('profile_image', profile_image);
  form_data.append('profile_pic', $('#profile_pic')[0].files[0]);

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "update_basic_profile",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#basic_profile_detail_form").load(location.href + " #basic_profile_detail_form>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});

// Disable page reload in change in vendor profile
$(document).on('submit', '#vendor_account_detail_form', function(e){
  e.preventDefault();

  var vendor_name = $('#vendor_name').val();
  var vendor_description = $('#vendor_description').val();
  var vendor_address = $('#vendor_address').val();
  var vendor_phone = $('#vendor_phone').val();
  var shipping_on_time = $('#shipping_on_time').val();
  var vendor_image = $('#vendor_image').val();
  
  var form_data = new FormData();

  form_data.append('vendor_name', vendor_name);
  form_data.append('vendor_description', vendor_description);
  form_data.append('vendor_address', vendor_address);
  form_data.append('vendor_phone', vendor_phone);
  form_data.append('shipping_on_time', shipping_on_time);
  form_data.append('vendor_image', vendor_image);
  form_data.append('vendor_img', $('#vendor_img')[0].files[0]);

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url: "update_vendor_profile",
      type: "POST",
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      data: form_data,
      headers: {'X-CSRFToken': csrfToken},
      dataType: "json",
      success: function(response)
      {
        $(window).scrollTop(0);
        $("#vendor_account_detail_form").load(location.href + " #vendor_account_detail_form>*", "");
        if(response.status == 200)
        {
          document.getElementById("alert-success").style.display = 'block';
          document.getElementById("success").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-success").style.display = 'none';
          }, 5000);
        }
        else
        {
          document.getElementById("alert-danger").style.display = 'block';
          document.getElementById("danger").innerText = response.message;
          setInterval(function ()
          {      
            document.getElementById("alert-danger").style.display = 'none';
          }, 5000);
        }
      }
  });
});