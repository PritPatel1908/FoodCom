$(document).ready(function() {
    $('#show_password').change(function() {
      if ($(this).is(':checked')) {
        $('#password').attr('type', 'text');
        $('#password-addon i').removeClass('fas fa-eye-slash').addClass('fas fa-eye');
        
        $('#cpassword').attr('type', 'text');
        $('#password-addon i').removeClass('fas fa-eye-slash').addClass('fas fa-eye');
      } else {
        $('#password').attr('type', 'password');
        $('#password-addon i').removeClass('fas fa-eye').addClass('fas fa-eye-slash');
        
        $('#cpassword').attr('type', 'password');
        $('#password-addon i').removeClass('fas fa-eye').addClass('fas fa-eye-slash');
      }
    });
  });