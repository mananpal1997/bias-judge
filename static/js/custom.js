$(function(){
	$('#unbias').click(function(){
		$('#unbias').hide();
		var data = $('#textfield').val();
		$.ajax({
			url: '/result',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				//console.log(response);
				var json = $.parseJSON(response);
				var final = "";
				$('#textfield').attr('style', 'display: none');
				$('#textfield').prop('style', 'display: none');
				$('#result-box').html("");
				for(var i in json.sentences)
				{
					if(json.sentences[i][1] != null)
					{
						final = '<span class="tooltip-text">'+String(json.sentences[i][0])+'</span><div class="tooltip-content"><ul>';
						for(var j in json.sentences[i][1])
						{
							final = final+"<li>"+String(json.sentences[i][1][j])+"</li>";
						}
						final = final+"</ul></div>";
					}
					else{
						final = final+String(json.sentences[i][0]);
					}
					$('#result-box').append(final);
					$('#prompt-text').text("Any possible biased statements have been highlighted. Hover over the sentence to see details.");
					$('#prompt-text').css('text-decoration', 'underline');
					$('#result-box').show();
					$('#start-again').removeAttr('style');
				}
				$("#textfield").each(function () {
					$(this).css({'height':'auto','overflow-y':'hidden'}).height(this.scrollHeight);
				}).on('input', function () {
					$(this).css({'height':'auto','overflow-y':'hidden'}).height(this.scrollHeight);
				});

				$('.tooltip-text').each(function() {
					$(this).qtip({
						content: {
							text: $(this).next('.tooltip-content')
						},
						show: {
							solo: true,
							effect: function() {
								$(this).slideDown();
							}
						},
						hide: {
							fixed: true,
							delay: 200,
							effect: function() {
								$(this).slideUp();
							}
						},
						style: {
							classes: "qtip-bootstrap"
						},
						position: {
							my: "top left",
							at: "bottom left"
						}
					});
					$(document).scrollTop($(document).height());
				});
			},
			error: function(error){
				console.log(error);
			}
		});
	});
	$('#start-again').click(function(){
		$('#result-box').html("");
		$('#result-box').hide();
		$('#unbias').show();
		$('#prompt-text').text("Paste your text below and press submit. An example is filled in if you just want to try it out.");
		$('#textfield').removeAttr('style');
		$("#textfield").each(function () {
			$(this).css({'height':'auto','overflow-y':'hidden'}).height(this.scrollHeight);
		}).on('input', function () {
			$(this).css({'height':'auto','overflow-y':'hidden'}).height(this.scrollHeight);
		});
		$('#start-again').attr('style', 'display: none;');
		$('#start-again').prop('style', 'display: none;');
	});
});