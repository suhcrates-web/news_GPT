

$(document).ready(function(){
	
	
	$("form").submit(function(event) {
		// Stop the form from submitting normally
		event.preventDefault();
		
		// Get the text from the textarea
		var question0 = $("#question").val();
		$('#make_box').html("작성중....(10초 소요됨)")
		// Send the text to the server using an HTTP POST request
		$.ajax({
			data:{
				cmd : "giveme",
				question0 : question0,
			},
			type : 'POST',
			url : '/donga/ask'
		})
		.done(function(data){
			if (data['cmd'] =='not_yet'){
				$('#make_box').html("작성버튼")
				location.reload()
				alert(data.message)}
			else if (data['cmd'] =='ok'){
				$('#content_box').html(data.message)
				$('#make_box').html("작성완료")
				
			}
		});
	});
});

// $(document).ready(function(){

// })
