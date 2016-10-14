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
      contentType: 'application/json; charset=utf-8',
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

// check to see if array of strings are all integers
function validate_ints(strInts, separator, hash_id, num_ints) {
   ok = true;
   ints = strInts.split(separator);
   try {
      for (var i = 0; i < num_ints; i++) {
         if (isNaN(ints[i])) ok = false;
         ii = parseInt(ints[i]);
      }
   } catch (err) {
      ok = false;
   }
   setFieldValid(ok, hash_id)
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

   validate_ints($('#dos').val(), '/', '#valid_dos', 3);
   validate_ints($('#tos').val(), ':', '#valid_tos', 2);

   if (!all_fields_valid) {
      alert("There are invalid input fields. Please check!");
      return;
   }

   // Construct the Json object to be sent to the server
   spotterV = {
      name: spotterNameV,
      email: spotterEmailV
   }
   locationV = {
      name: locNameV,
      lat: locLatV,
      long: locLongV
   }
   acEngine = {
      type: engType.options[engType.selectedIndex].value,
      number: engNumber.options[engNumber.selectedIndex].value,
      positions: engPos.options[engPos.selectedIndex].value,
      noise_desc: $('#engNoise').val(),
      noise_audio: $('#audioPath').html()
   }
   acWing = {
      number: wingNumber.options[wingNumber.selectedIndex].value,
      position: wingLoc.options[wingLoc.selectedIndex].value,
      swept: $('#wingSwept').val()
   }
   acSize = {  
      length: plength.options[plength.selectedIndex].value,
      wingspan: wingSpan.options[wingSpan.selectedIndex].value,
      tail: tailHeight.options[tailHeight.selectedIndex].value
   }

   aircraftV = {
      type: planeType.options[planeType.selectedIndex].value,
      engine: acEngine,
      size: acSize,
      wing: acWing
   }

   sighting = {
      cmd: "save_sighting",
      spotter: spotterV,
      location: locationV,
      date: $('#dos').val(),
      time: $('#tos').val(),
      nvp: numVapours.options[numVapours.selectedIndex].value,
      aircraft: aircraftV,
      markings: $('#markDesc').val(),
      photos: $('#imgPath').html()
   };

   postJSON(servicePage, sighting, function (json) {
      if (json.err) alert(json.err);
      else {
         alert("json.ok=" + json.ok);
      }
   });
}