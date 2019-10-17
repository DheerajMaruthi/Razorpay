$(document).ready(function() {
  $('.carousel').carousel({
    interval: 1000 * 10
  });
  $(".fancybox").fancybox({
    openEffect: "none",
    closeEffect: "none"
  });
  $('.spread-btn').click(function() {
    $(this).toggleClass('active-class');
    $('.soc-icons').fadeToggle();
  });
  $(".soc-icons, .spread-btn, .donate-btn").click(function(e) {
    e.stopPropagation();
  });
  $('body').on("click", function(e) {
    $('.soc-icons').hide();
  });
  $(".press-pointer").click(function() {
    $('html, body').animate({
      scrollTop: $('#big').offset().top - 120
    }, 700);
  });

  $(".nav-wrapper li a[href^='#']").click(function(e) {
    var top;
    e.preventDefault();
    var position = $($(this).attr("href")).offset().top-100;
    $("body, html").animate({
      scrollTop: position
  }, 500);
  });

  $('.counter-up').each(function() {
    var size = $(this).text().split(".")[1] ? $(this).text().split(".")[1].length : 0;
    $(this).prop('Counter', 0).animate({
      Counter: $(this).text()
    }, {
      duration: 5000,
      step: function(func) {
        $(this).text(parseFloat(func).toFixed(size));
      }
    });
  });

  $("#id_amount_option_2").on("click", function() {
    $('#id_other_amount').fadeIn();
  });

  $('.mob-list ul li a').click(function(){
      $('.mob-list').hide();
  });
  $("#id_amount_option_0, #id_amount_option_1").click("change", function() {
    $('#id_other_amount').fadeOut();
    $("input[type=number]").val("");
    $("#id_other_amount-error").hide()
  });

  $(".navbar-items  li").click(function() {
    $(".navbar-items  li").removeClass("active");
    $(this).addClass("active");
  });

  $(".ham-menu").click(function() {
    $('.mob-list').slideToggle();
  })
  $("#id_dob").datepicker();

  $('#owlTestimonials').owlCarousel({
    responsiveClass: true,
    dots: true,
    autoplay: true,
    responsive: {
      0: {
        items: 1,
        nav: true
      },
      600: {
        items: 1,
        nav: true
      },
      1000: {
        items: 2,
        nav: true
      }
    }
  });

  $("#owlTestimonials .owl-prev").html('<img src="/static/images/left-arrow.png">');
  $("#owlTestimonials .owl-next").html('<img src="/static/images/right-arrow.png">');

  // $("#id_name").keyup(function() {
  //   var name = $(this).val();
  //   if (name.length <= 0) {
  //     $('.name').text('Please enter your name');
  //   } else{
  //     $('.name').text('');
  //   }
  // });


  // $("#id_email").keyup(function() {
  //   var email_address = $(this).val();
  //   var email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
  //   if (!email_address.match(email_regex)) {
  //     $('.email').text('Please enter a valid email.');
  //   } else {
  //     $('.email').text('');
  //   }
  // });

  // $("#id_phonenumber").keyup(function() {
  //   var number = $(this).val();
  //   var phone_reg = /^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$/;
  //   if (!number.match(phone_reg)) {
  //     $('.phone').text('Enter a valid phone number with country code');
  //   } else {
  //     $('.phone').text('')
  //   }
  // });

  $(".press-pointer").click(function() {
    $(".press-pointer").removeClass("active");
    $(this).addClass("active");
  });



  var bigimage = $("#big");
  var thumbs = $("#thumbs");
  var syncedSecondary = true;

  bigimage
    .owlCarousel({
      items: 1,
      nav: false,
      dots: false
    })
    .on("changed.owl.carousel", syncPosition);
  thumbs
    .on("initialized.owl.carousel", function() {
      thumbs
        .find(".owl-item")
        .eq(0)
        .addClass("current");
    })
    .owlCarousel({
      responsiveClass: true,
      dots: true,
      responsive: {
        0: {
          items: 1,
          nav: true
        },
        600: {
          items: 1,
          nav: true
        },
        1000: {
          items: 3,
          nav: true
        }
      }
    })
    .on("changed.owl.carousel", syncPosition2);

  function syncPosition(el) {
    var count = el.item.count - 1;
    var current = Math.round(el.item.index - el.item.count / 2 - 0.5);
    if (current < 0) {
      current = count;
    }
    if (current > count) {
      current = 0;
    }
    thumbs
      .find(".owl-item")
      .removeClass("current")
      .eq(current)
      .addClass("current");
    var onscreen = thumbs.find(".owl-item.active").length - 1;
    var start = thumbs
      .find(".owl-item.active")
      .first()
      .index();
    var end = thumbs
      .find(".owl-item.active")
      .last()
      .index();
    if (current > end) {
      thumbs.data("owl.carousel").to(current, 100, true);
    }
    if (current < start) {
      thumbs.data("owl.carousel").to(current - onscreen, 100, true);
    }
  }

  function syncPosition2(el) {
    if (syncedSecondary) {
      var number = el.item.index;
      bigimage.data("owl.carousel").to(number, 100, true);
    }
  }
  thumbs.on("click", ".owl-item", function(e) {
    e.preventDefault();
    var number = $(this).index();
    bigimage.data("owl.carousel").to(number, 300, true);
  });
  $("#thumbs .owl-prev").html('<img src="/static/images/left-arrow.png">');
  $("#thumbs .owl-next").html('<img src="/static/images/right-arrow.png">');
  var $imageSrc;
  $('.gallery img').click(function() {
    $imageSrc = $(this).data('bigimage');
  });


  $('#image-gallery').on('shown.bs.modal', function(e) {

    $("#image").attr('src', $imageSrc);
  });

  $('#myModal').on('hide.bs.modal', function(e) {
    $("#image").attr('src', '');
  });

  $("body").on("submit", "form", function() {
    $(this).submit(function() {
      return false;
    });
    return true;
  });
  // $('#register input').keyup(function() {
  //     var name = $(this).val();
  //     var nameValue = $(this).attr('name');
  //     console.log(nameValue);
  //     name.trim();
  //     if(nameValue == 'name') {
  //         if (name.length <= 0) {
  //             $('#popover-name').show();
  //         } else if (name.length > 0){
  //             $('#popover-name').hide()
  //         } else {
  //             $('#popover-name').show();
  //         }
  //     }
  //     if(nameValue == 'other_amount') {
  //         if (name.length <= 0) {
  //             $('#popover-name').show();
  //         } else if (name.length > 0){
  //             $('#popover-name').hide()
  //         } else {
  //             $('#popover-name').show();
  //         }
  //     }
  //     if(nameValue == 'email') {
  //         var re = /([A-Z0-9a-z_-][^@])+?@[^$#<>?]+?\.[\w]{2,4}/;
  //          if(!re.test(name)) {
  //              $('#popover-email').show();
  //          } else {
  //              $('#popover-email').hide();
  //          }
  //    }
  //   if(nameValue == 'phonenumber') {
  //       var regex = /^(?:(?:\+|0{0,2})91(\s*|[\-])?|[0]?)?([6789]\d{2}([ -]?)\d{3}([ -]?)\d{4})$/;
  //       console.log(regex.test(name));
  //       if (!regex.test(name)) {
  //           $('#popover-cnumber').show();
  //       } else {
  //           $('#popover-cnumber').hide();
  //       }
  //     }
  // });
});
jQuery.validator.addMethod("onlyCharacters", function(value, element) {
  console.log('ok');
     return /^[a-zA-Z][a-zA-Z\s]*$/.test( value );
}, "Name should contain only characters from a-z or A-Z");
jQuery.validator.addMethod("customemailValidation", function(value, element) {
     return /^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(([0-9]{1,3})|([a-zA-Z]{2,3})|(com|org))$/.test( value );
});
jQuery.validator.addMethod("phoneNumberValidation", function(value, element) {
     return /^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$/.test( value );
}, "Provide valid phone number.");
jQuery.validator.addMethod("panNumberValidation", function(value, element) {
     if (value.length > 0){
        return /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test( value );
     }
     else{
       return true;
     }
}, "Provide valid pan number.");
$(function() {
  $("form[name='reg']").validate({
    rules: {
      name: {
        required: true,
        onlyCharacters: true,
        minlength: 3
      },
      email: {
        required: true,
        customemailValidation: true,
      },
      phonenumber: {
        required: true,
        phoneNumberValidation: true,
      },
      pan: {
        required: true,
        panNumberValidation: true,
      }
    },
    messages: {
      name: {
        required:"Please provide your name.",
        minlength: "Minimum of 3 characters required.",
      },
      phonenumber: {
        required: "Please provide your phonenumber.",
      },
      email: {
        required: "Please provide your email-id.",
        customemailValidation: "Please provide valid email-id"
      }
    },
    submitHandler: function(form) {
      form.submit();
    }
  });
});
