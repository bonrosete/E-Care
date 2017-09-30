$(document).ready(function(){
	$('#eventsExample .time').timepicker({
	    'showDuration': false,
	    'timeFormat': 'g:ia',
	    'scrollDefault': 'now',
	    'disableTextInput': true,
	    'minTime': '9:00am',
	    'maxTime': '6:00pm',
	});

	$('#eventsExample .date').datepicker({
		'startDate': '+1w',
		'endDate': '+5w',
	    'format': 'yyyy-mm-dd',
	    'autoclose': true,
	});

	// initialize datepair
	var basicExampleEl = document.getElementById('eventsExample');
	var datepair = new Datepair(basicExampleEl);

	$('#eventsExample').on('changeDate', function() {
	    var date = $("#id_date").val();
	    var doctor_name = $("#id_doctor_name").text();
	    $.ajax({
	    	url: '/ajax/validate_date/',
	    	data: {
	    		'date': date,
	    		'doctor_name': doctor_name,
	    	},
	    	success: function(data) {
	    		var pair = [];
	    		for (var i=0; i<data.length; i++){
	    			pair.push([data[i]['starttime'], data[i]['endtime']])
	    		};
	    		$('#eventsExample .time').timepicker('option', {'disableTimeRanges': pair, 'minTime': '9:00am', 'maxTime': '6:00pm'});
	    	}
	    });
	});
});
	