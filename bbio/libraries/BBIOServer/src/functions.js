/*
 functions.js
 Javascript functions for PyBBIO BBIOServer library.
*/

function call_function(function_id, type) {
  /* Interfaces with the BBIOServer request handler to execute
     PyBBIO functions. */
  var params = { "function_id" : function_id };
  if (type == "entry") {
      // Extract the text and add it to the params hash table:
    var text = $('#' + function_id).val()
    if (!text) {
      text += " ";
    }
    params["entry_text"] = text;
  }
  $.get("/cgi-bin/index", params,
  function(return_value){
    if (type == "monitor") {
	// Set the monitor div with the same id as the function 
        // to the return value:
      $('#'+function_id).text(return_value);
    }
  });
};


function start_monitor() {
  /* Called once on page load. Continuously updates monitors. */
  $('.monitor-field').each(function() {
    // The div id is the same as its function's id:
    var function_id = $(this).attr('id');
    call_function(function_id, 'monitor');
  });
  setTimeout(function() { 
    start_monitor();
  }, 200);
} 
