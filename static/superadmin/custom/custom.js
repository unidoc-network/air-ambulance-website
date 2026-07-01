function restrictAlphabets(e) {
  var x = e.which || e.keyCode;
  var inputValue = e.target.value;

  // Allow backspace
  if (x === 8) {
    return true;
  }

  // Allow numbers 0-9
  if (x >= 48 && x <= 57) {
    return true;
  }

  // Allow only one dot
  if (x === 46 && inputValue.indexOf('.') === -1) {
    return true;
  }

  // Block everything else
  return false;
}


$("#message_div").fadeOut(3000);

function delete_modal(id) {
  $("#hid").val(id);
  $("#modaldemo5").modal('show');
}


function filterdata(data) {
  var page = '1'
  if (data != 'None') {
    page = data
  }



  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function deletedata() {

  page = $("#page").val();
  id = $("#hid").val();

  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, id: id },

    success: function (data) {
      $("#modaldemo5").modal('hide');

      $(".table-responsive").html(data.template)


    }
  });
}







function PopupStatus(id, vl) {

  $.ajax({
    url: '/superadmin/PopupStatus',
    type: 'GET',
    data: { id: id, vl: vl },

    success: function (data) {

      window.location.reload();


    }
  });
}







function filtercategory(data) {
  var page = '1'
  if (data != 'None') {
    page = data
  }


  var search = $('#searchkey').val()
  var status = $('#status').val()

  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function setseq(id, vl) {

  page = $("#page").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, vl: vl, type: 7 },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function categorystatus(id, vl) {
  page = $("#page").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, vl: vl, type: 1 },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function categoryhighlight(id, vl) {

  page = $("#page").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, vl: vl, type: 3 },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function categorydelete() {

  page = $("#page").val();
  id = $("#hid").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, type: 2 },

    success: function (data) {
      $("#modaldemo5").modal('hide');

      $(".table-responsive").html(data.template)


    }
  });
}














function filtertestimonial(data) {
  var page = '1'
  if (data != 'None') {
    page = data
  }


  var search = $('#searchkey').val()
  var status = $('#status').val()

  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function testimonialstatus(id, vl) {

  page = $("#page").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, id: id, vl: vl, type: 1, search: search },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}


function testimonialdelete() {

  page = $("#page").val();
  id = $("#hid").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, id: id, type: 2, search: search },

    success: function (data) {
      $("#modaldemo5").modal('hide');

      $(".table-responsive").html(data.template)


    }
  });
}


function filtergallery(data) {
  var page = '1'
  if (data != 'None') {
    page = data
  }


  var search = $('#searchkey').val()
  var status = $('#status').val()

  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}





function gallerystatus(id, vl) {
  page = $("#page").val();
  console.log("djdjjdjjfhfhf")

  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, vl: vl, type: 1 },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function galleryhighlight(id, vl) {
  page = $("#page").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, vl: vl, type: 3 },

    success: function (data) {

      $(".table-responsive").html(data.template)


    }
  });
}



function gallerydelete() {

  page = $("#page").val();
  id = $("#hid").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, type: 2 },

    success: function (data) {
      $("#modaldemo5").modal('hide');

      $(".table-responsive").html(data.template)


    }
  });
}




function filterteam(data) {
  console.log("Filtering team... Page:", data);
  var page = '1'
  if (data != 'None') {
    page = data
  }
  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  console.log("Search:", search, "Status:", status, "URL:", url);
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search },
    success: function (data) {
      console.log("Filter success. Updating table.");
      $(".table-responsive").html(data.template)
    },
    error: function (err) {
      console.error("Filter error:", err);
    }
  });
}

function teamstatus(id, vl) {
  var page = $("#page").val();
  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, id: id, vl: vl, type: 1, search: search },
    success: function (data) {
      $(".table-responsive").html(data.template)
    }
  });
}

function setseqteam(id, vl) {
  var page = $("#page").val();
  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, search: search, id: id, vl: vl, type: 7 },
    success: function (data) {
      $(".table-responsive").html(data.template)
    }
  });
}

function teamdelete() {
  var page = $("#page").val();
  var id = $("#hid").val();
  var status = $('#status').val()
  var search = $('#searchkey').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: { page: page, status: status, id: id, type: 2, search: search },
    success: function (data) {
      $("#modaldemo5").modal('hide');
      $(".table-responsive").html(data.template)
    }
  });
}


// Dynamic filter reset button color based on active filters
$(document).ready(function() {
    function updateResetBtnColor() {
        var hasActiveFilters = false;
        
        // Check standard search fields
        var searchFields = ['searchkey', 'searchCareer', 'searchApp', 'search'];
        searchFields.forEach(function(id) {
            var el = $('#' + id);
            if (el.length && el.val().trim() !== '') {
                hasActiveFilters = true;
            }
        });
        
        // Check standard status fields
        var statusFields = ['status', 'filterStatus'];
        statusFields.forEach(function(id) {
            var el = $('#' + id);
            if (el.length && el.val() !== 'True') { // True is default active state
                hasActiveFilters = true;
            }
        });
        
        // Date filter
        var elDate = $('#dateFilter');
        if (elDate.length && elDate.val() !== '') {
            hasActiveFilters = true;
        }
        
        // Find reset buttons (usually anchor tags with title='Reset' or containing icon fe-rotate-cw)
        var resetBtns = $('a[title="Reset"], .fe-rotate-cw').closest('a');
        if (hasActiveFilters) {
            resetBtns.removeClass('btn-light').addClass('btn-primary');
        } else {
            resetBtns.removeClass('btn-primary').addClass('btn-light');
        }
    }
    
    // Attach event listeners
    $(document).on('keyup change', 'input[type="text"], select', function() {
        updateResetBtnColor();
    });
    
    // Initial check
    setTimeout(updateResetBtnColor, 100);
});
