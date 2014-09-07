var session = '';

$(document).ready(function() {
  $('input').keydown(function(event) {
    if(event.which == 13) {
      expr = $(this).val();
      $.post('/', {'expr': expr}, function(data) {

        session += '\nInput : ' + expr + '\nOutput: ' + data;
        $('.session').text(session);
      });
    }
  });
});
