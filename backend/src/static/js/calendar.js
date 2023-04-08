var calendar;
const calendar_list_url = "/api/calendar/list?type=settings",
  events_list = '/api/calendar/events';

document.addEventListener('DOMContentLoaded', function () {
  let calendarEl = document.getElementById('calendar');
  calendar = new FullCalendar.Calendar(calendarEl, {
    eventDidMount: function (info) {
      info.el.innerHTML += //'<div class="event_tooltip">' + '</div>' 
      
       // info.event.extendedProps.description +
       
        '<div class="card event_tooltip"><div class="card_title">Card</div><hr/><div class="card_body"><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p></div></div>'
        info.el.addEventListener("mouseover", position_tooltip);
    },
    events: events_list,
    eventTimeFormat: {
      hour: '2-digit', //2-digit, numeric
      minute: '2-digit', //2-digit, numeric
     // second: '2-digit', //2-digit, numeric
      meridiem: false, //lowercase, short, narrow, false (display of AM/PM)
      hour12: false //true, false
    },
    initialView: 'dayGridMonth',
    firstDay: 1,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title', // prevYear,nextYear
      right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listMonth,listYear'
    },
    businessHours: { // days of week. an array of zero-based day of week integers (0=Sunday)
      daysOfWeek: [
        1,
        2,
        3,
        4,
        5
      ], // Monday - Thursday

      startTime: '10:00', // a start time (10am in this example)
      endTime: '18:00', // an end time (6pm in this example)
    },
    // hiddenDays: [ 2, 4 ] // hide Tuesdays and Thursdays
  });
  calendar.render();
});

function position_tooltip() {
  let tooltip_rect = this.getBoundingClientRect(),
    tooltip_el=this.querySelector(".event_tooltip");
  let y=tooltip_rect.y,
      bottom_h = window.innerHeight - y-tooltip_rect.height;

  //console.log(tooltip_rect.right / (tooltip_rect.width + tooltip_rect.left + tooltip_rect.right));
  if (tooltip_rect.x > window.innerWidth/2) {
  
    tooltip_el.style.left = -tooltip_el.offsetWidth + 'px';
  }

  if ( bottom_h <tooltip_el.offsetHeight) {

    tooltip_el.style.top = bottom_h-tooltip_el.offsetHeight + 'px';
  }
 
  
}
var data;
async function get_calendar_list(url) { // Storing response
  const response = await fetch(url);

  // Storing data in form of JSON
  data = await response.json();
  console.log(data);
  if (response) { // hideloader();
  }
  show(data);
}
// Calling that async function
getapi(calendar_list_url);
