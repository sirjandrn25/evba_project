let current_location = {};
let csrf = "";
let time_control = null;

console.log("hello driver k xa");
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    alert("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  
  current_location['lat'] = position.coords.latitude;
  current_location['long'] = position.coords.longitude;
  console.log(current_location)
  
}
window.onload = getLocation();
const send_help_form = document.getElementById("send_help_form");
let data = {};

send_help_form.addEventListener("submit",e=>{
  e.preventDefault();
  const vehicle_type = e.target.vehicle_type.value;
  const service = e.target.service.value;
  const problem_desc = e.target.problem_desc.value;
  csrf = e.target.csrfmiddlewaretoken.value;



  
  data = {
    'vehilce_type':vehicle_type,
    'service':service,
    problem_desc:problem_desc,
    curr_driver_lat:current_location['lat'],
    curr_driver_long:current_location['long']
  }
  sendHelpRequest();

});

const sendHelpRequest=()=>{
  const url = `http://localhost:8000/tracker/driver/send-help/`;
  const params = {
    method:'POST',
    headers:{
      "Content-Type":"application/json",
      "X-CSRFToken":csrf
    },
    body:JSON.stringify(data)
  }
  fetch(url,params).then(res=>res.json()).then(json_res=>{
    time_control=setTimeout(()=>{
        
        change_last_mechanic_status(false);
        sendAgainHelpRequest();
        
    },30000);
    show_mechanics(json_res);

  })
}
const sendAgainHelpRequest = ()=>{
    const url = `http://${window.location.host}/tracker/driver/send-help-again/`;
    fetch(url).then(res=>res.json()).then(json_res=>{
        if(json_res.status===200){
            data=json_res.detail;
            console.log(data)
            show_mechanics(data);
        }else{
            console.log(json_res)
        }
    }).catch(error=>{
        console.log(error)
    })
}



const url = `ws://${window.location.host}/ws/driver/notifications/`;
const ws = new WebSocket(url);

ws.onopen = event=>{
    console.log("connecting ........");
}

ws.onmessage = event=>{
  
    console.log("messaging .....");
    data = JSON.parse(event.data);
    change_last_mechanic_status(data.is_mechanic_accept)
    if(!data.is_mechanic_accept){
        sendAgainHelpRequest();
    }
    clearTimeout(time_control);
    
   
    
}


ws.onerror = event=>{
  console.log("error message...");
}
ws.onclose = event=>{
  console.log("closing message ...");
}


const show_mechanics = (data)=>{
    const mechanic_table = document.getElementById('mechanic_table');
    const sno = mechanic_table.rows.length+1;
    console.log(data)
    const tr = `<tr>
                    <th scope="row">${sno}</th>
                    <td>${data.mechanic.full_name}</td>
                    <td>${data.distance.toFixed(2)}</td>
                    
                    <td>
                        <span class="badge bg-info">sending ...</span>
                    </td>
                </tr>`;
    mechanic_table.innerHTML +=tr;


}

const change_last_mechanic_status = (accept_status)=>{
    
    const mechanic_table = document.getElementById('mechanic_table');
    // console.log(mechanic_table.rows)
    const tr = mechanic_table.rows[mechanic_table.rows.length-1];
    if(accept_status){
        tr.cells[tr.cells.length - 1].innerHTML = `<span class="badge bg-success">accept</span>`;
    }
    else{
        tr.cells[tr.cells.length - 1].innerHTML = `<span class="badge bg-warning">cancel</span>`;
    }
    

}