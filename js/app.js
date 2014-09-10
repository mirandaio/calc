$(document).ready(function() {
  var sfront = [];
  var sback = [];
  $('input').keydown(function(event) {
    if(event.which == 13) {
      var expr = $(this).val();
      $(this).val('');
      $.post('/', {'expr': expr, 'session': sback.join("")}, function(data) {
        sfront.push('\ninput : ', expr, '\noutput: ', data);
        sback.push('\n', expr, '\n=', data);
        $('.session').text(sfront.join(""));
      });
    }
  });
});
