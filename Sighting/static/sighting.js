servicePage = "service/";

function sightingPageLoaded() {

}

function spotterIdChanged() {
   spotterId_val = spotterId.options[spotterId.selectedIndex].value;
   test_id = "$" + spotterId_val + "$";
   if (test_id == "$0$") {
      $('#spotterName').val("");
      $('#spotterEmail').val("");
   }
   else {
      $.getJSON(servicePage, { cmd: "get_spotter",
         nocache: new Date().getTime(),
         id: spotterId_val
      }, function (json) {
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
      $.getJSON(servicePage, { cmd: "get_loc",
         nocache: new Date().getTime(),
         id: locId_val
      }, function (json) {
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
   fd.append("label", "WEBUPLOAD");
   $.ajax({
      url: "uploadfile/",
      type: "POST",
      data: fd,
      processData: false,  // tell jQuery not to process the data
      contentType: false   // tell jQuery not to set contentType
   }).done(function (json) {
      if (json.path) $('#audioPath').html(json.path);
      else alert("Expecting json.path");
   });
   return false;
}