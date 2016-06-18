$(document).ready(function()
{
	function resize(e) {
		$(e).css({'height':'auto','overflow-y':'hidden'}).height(e.scrollHeight);
	}
	$("#textfield").each(function () {
		resize(this);
	}).on('input', function () {
		resize(this);
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
	});
});