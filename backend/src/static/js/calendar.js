var calendar;
document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');
      calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      firstDay: 1,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',//prevYear,nextYear
        right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listMonth,listYear'
      },
      businessHours: {
        // days of week. an array of zero-based day of week integers (0=Sunday)
        daysOfWeek: [ 1, 2, 3, 4 ,5], // Monday - Thursday
      
        startTime: '10:00', // a start time (10am in this example)
        endTime: '18:00', // an end time (6pm in this example)
      },
     // hiddenDays: [ 2, 4 ] // hide Tuesdays and Thursdays
    });
    calendar.render();
  });