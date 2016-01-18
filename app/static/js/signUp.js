$(function() {
	$('#btnSignUp').click(function() {
//	$(document).on("click", "#btnSignUp", function(){
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
				success: function(response) {
					console.log(response);
				},
			error: function(error) {
				console.log(error);
			}
		});
	});
});


