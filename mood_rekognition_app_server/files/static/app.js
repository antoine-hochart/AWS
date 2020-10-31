/*
 * app.js
 */

var backend_ip = '192.168.0.0'

function readFile(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      var htmlPreview =
        '<img width="240" src="' +
        e.target.result +
        '" />' +
        "<p>" +
        input.files[0].name +
        "</p>";
      var wrapperZone = $(input).parent();
      var previewZone = $(input)
        .parent()
        .parent()
        .find(".preview-zone");
      var boxZone = $(input)
        .parent()
        .parent()
        .find(".preview-zone")
        .find(".box")
        .find(".box-body");

      wrapperZone.removeClass("dragover");
      previewZone.removeClass("hidden");
      boxZone.empty();
      boxZone.append(htmlPreview);

      var data_uri = e.target.result;
      $.post(
        'http://'+backend_ip+':5000/get_picture/',
        data_uri,
        result_f,
        'html'
      );
      function result_f(data_back){
        $('#analysis').html($.parseHTML(data_back));
      }
    };

    reader.readAsDataURL(input.files[0]);
  }
}

function reset(e) {
  e.wrap("<form>")
    .closest("form")
    .get(0)
    .reset();
  e.unwrap();
}

$(".dropzone").change(function() {
  readFile(this);
});

$(".dropzone-wrapper").on("dragover", function(e) {
  e.preventDefault();
  e.stopPropagation();
  $(this).addClass("dragover");
});

$(".dropzone-wrapper").on("dragleave", function(e) {
  e.preventDefault();
  e.stopPropagation();
  $(this).removeClass("dragover");
});

$(".remove-preview").on("click", function() {
  var boxZone = $(this)
    .parents(".form-group")
    .find(".box-body");
  var previewZone = $(this).parents(".preview-zone");
  var dropzone = $(this)
    .parents(".form-group")
    .find(".dropzone");
  boxZone.empty();
  previewZone.addClass("hidden");
  reset(dropzone);
});

function rekognize() {
  var pic = $('#preview').contents().length
  if(pic>0){
    $.post(
      'http://'+backend_ip+':5000/analyze/',
      "nothing",
      result_f,
      'html'
    );
    function result_f(data_back){
      $('#result').html($.parseHTML(data_back));
    }
  }
}
