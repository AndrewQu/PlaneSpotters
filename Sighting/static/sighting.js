servicePage = "service/";

function sightingPageLoaded() {
   var d = new Date();
   dstr = "" + d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear()
   tstr = "" + d.getHours() + ":" + d.getMinutes()
   $('#dos').val(dstr);
   $('#tos').val(tstr);
   $('#wingSwept').val("10");

   csrf_token = $("input:hidden[name=csrfmiddlewaretoken]").val();
   $.ajaxSetup({
      beforeSend: function (xhr, settings) {
         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
         }
      }
   });
}
function csrfSafeMethod(method) {
   // these HTTP methods do not require CSRF protection
   return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function postJSON(url, data_obj, success_handler, args) {
   args = $.extend({
      url: url,
      type: 'POST',
      data: JSON.stringify(data_obj),
//      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      success: success_handler
   }, args);
   return $.ajax(args);
};


function spotterIdChanged() {
   spotterId_val = spotterId.options[spotterId.selectedIndex].value;
   test_id = "$" + spotterId_val + "$";
   if (test_id == "$0$") {
      $('#spotterName').val("");
      $('#spotterEmail').val("");
   }
   else {
      cmd_obj = { cmd: "get_spotter",
         nocache: new Date().getTime(),
         id: spotterId_val
      };
      postJSON(servicePage, cmd_obj, function (json) {
         if (json.err) alert(json.err);
         else {
            $('#spotterName').val(json.name);
            $('#spotterEmail').val(json.email);
         }
      });
   }
}

function locationIdChanged() {
   locId_val = locationId.options[locationId.selectedIndex].value;
   test_id = "$" + locId_val + "$";
   if (test_id == "$0$") {
      $('#locName').val("");
      $('#locLat').val("");
      $('#locLong').val("");
   }
   else {
      cmd_obj = { cmd: "get_loc",
         nocache: new Date().getTime(),
         id: locId_val
      };
      postJSON(servicePage, cmd_obj, function (json) {
         if (json.err) alert(json.err);
         else {
            $('#locName').val(json.name);
            $('#locLat').val(json.lat);
            $('#locLong').val(json.long);
         }
      });
   }
}

function uploadAudio() {
   var fd = new FormData(document.getElementById("audioform"));
   fd.append("label", "audio");
   $.ajax({
      url: "uploadfile/",
      type: "POST",
      data: fd,
      processData: false,  // tell jQuery not to process the data
      contentType: false   // tell jQuery not to set contentType
   }).done(function (json) {
      if (json.path) $('#audioPath').html(json.path);
      else if (json.err) alert(json.err);
      else alert("Error in uploadAudio");
   });
   return false;
}

function uploadImage() {
   var fd = new FormData(document.getElementById("imgform"));
   fd.append("label", "image");
   $.ajax({
      url: "uploadfile/",
      type: "POST",
      data: fd,
      processData: false,  // tell jQuery not to process the data
      contentType: false   // tell jQuery not to set contentType
   }).done(function (json) {
      if (json.path) $('#imgPath').html(json.path);
      else if (json.err) alert(json.err);
      else alert("Error in uploadImage");
   });
   return false;
}

var all_fields_valid = true;

function setFieldValid(valid, hash_id) {
   if (valid) $(hash_id).html("");
   else {
      $(hash_id).html("X");
      all_fields_valid = false;
   }
}

function submitSighting() {
   // Validate fields

   all_fields_valid = true;
   spotterNameV = $('#spotterName').val();
   setFieldValid(spotterNameV.length >= 3, '#valid_spotterName');

   spotterEmailV = $('#spotterEmail').val();
   setFieldValid(spotterEmailV.length > 3 && spotterEmailV.indexOf('@') > 0, '#valid_spotterEmail');

   locNameV = $('#locName').val();
   setFieldValid(locNameV.length >= 3, '#valid_locName');

   locLatV = parseFloat($('#locLat').val());
   setFieldValid(locLatV === locLatV, '#valid_locLat');

   locLongV = parseFloat($('#locLong').val());
   setFieldValid(locLongV === locLongV, '#valid_locLong');

   if (!all_fields_valid) alert("There are invalid input fields. Please check!");

}