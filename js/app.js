var session = '';

$(document).ready(function() {
  $('input').keydown(function(event) {
    if(event.which == 13) {
      expr = $(this).val();
      $(this).val('');
      $.post('/', {'expr': expr, 'session': session}, function(data) {

        session += '\nInput : ' + expr + '\nOutput: ' + data;
        $('.session').text(session);
      });
    }
  });
});
