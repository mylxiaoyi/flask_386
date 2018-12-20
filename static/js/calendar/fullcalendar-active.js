$(function() {

	var todayDate = moment().startOf('day');
	var YM = todayDate.format('YYYY-MM');
	var YESTERDAY = todayDate.clone().subtract(1, 'day').format('YYYY-MM-DD');
	var TODAY = todayDate.format('YYYY-MM-DD');
	var TOMORROW = todayDate.clone().add(1, 'day').format('YYYY-MM-DD');

	$('#calendar').fullCalendar({
		header: {
			left: 'prevYear,prev,next,nextYear today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay,listWeek'
		},
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        eventSources: [
            {
                url: '/events_json'
            }
        ],
        /*eventRender: function(event, $element) {
            $element.popover({
                title: 'Event',
                content: event.title,
                trigger: 'hover',
                placement: 'top',
                container: 'body'
            });
        },*/
        eventClick: function(event, jsEvent, view) {
            window.location.href="/events/update/"+event.id;
        },
        eventDrop: function(event, delta, revertFunc) {
            if (!confirm("Are you sure about this changes?")) {
                revertFunc();
            }
            else {
                $.post('/events_update_json',
                    {
                        'id': event.id,
                        'title': event.title,
                        'start': event.start.format(),
                        'end': event.end.format()
                    }
                ).fail(function() {
                    alert('update failed');
                    revertFunc();
                });
            }
        },
        eventResize: function(event, delta, revertFunc) {
            if (!confirm("is this okay?")) {
                revertFunc();
            }
            else {
                $.post('/events_update_json',
                    {
                        'id': event.id,
                        'title': event.title,
                        'start': event.start.format(),
                        'end': event.end.format()
                    }
                ).fail(function() {
                    alert('update failed');
                    revertFunc();
                });
            }
        }
	});
});
