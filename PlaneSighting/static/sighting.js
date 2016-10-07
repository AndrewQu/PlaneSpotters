servicePage = "service";

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
      $.getJSON(servicePage, { cmd: "get_spotter", id: spotterId_val }, function (json) {
         alert(json.msg);
      });
   }
}