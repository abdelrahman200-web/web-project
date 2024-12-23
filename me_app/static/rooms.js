document.getElementById("room-form").addEventListener("submit", function (event) {
    event.preventDefault(); 
    
    const roomData = {
        Room_number: document.getElementById("room-number").value,
        Roomtype: document.getElementById("room-type").value,
        floorNumber: document.getElementById("room-floor").value,
        max: document.getElementById("max").value,
        price: document.getElementById("price").value,
        F: document.getElementById("features").value,  
        status: "Ready"
    };
    
    fetch('/addroom', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(roomData)
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.message && data.message === "Room added successfully") {
            loadRooms();
            alert("Room added successfully!");
            document.getElementById("room-form").reset();
        } else {
            alert("Error: " + (data.error || data.message));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the room.');
    });
});
function loadRooms() {
    fetch('/show_rooms')
        .then(response => response.json())
        .then(rooms => {
            const tableBody = document.querySelector("table tbody");
            tableBody.innerHTML = "";

            rooms.forEach(room => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${room.RoomNo}</td>
                    <td>${room.Roomtype}</td>
                    <td>${room.floorNumber}</td>
                    <td>${room.Max}</td>
                    <td>${room.price}</td>
                    <td>${room.F}</td>
                    <td>
                        <button class="delete-btn" data-id="${room.Room_number}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while loading rooms.");
        });
}



window.onload = loadRooms;

