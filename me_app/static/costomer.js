document.getElementById("submitBtn").addEventListener("click", function() {
    const identity = document.getElementById("identity").value;
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const anotherPhone = document.getElementById("anotherPhone").value;
    const age = document.getElementById("age").value;
    const email = document.getElementById("email").value;
    const nationality = document.getElementById("nationality").value;
    const proofOf = document.getElementById("proofOf").value; 
    
    if (name && phone && age && nationality && proofOf) {  
        const customerData = {
            identity: identity,
            name: name,
            phone: phone,
            another_phone: anotherPhone || null, 
            age: age,
            email: email || null, 
            nationality: nationality,
            type_of_proof_of: proofOf 
        };
        fetch('/add_customer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(customerData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Customer added successfully!") {
                alert("Customer added successfully!");
                loadCustomers(); 
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while adding the customer.");
        });
    } else {
        alert("Please fill out all required fields.");
    }
});
// Function to load customers (could be called after adding a customer)
function fetchRegistrations() {
    fetch('/registrationAll')
        .then(response => response.json())
        .then(registrations => {
            const tableBody = document.querySelector("#registrationTableBody tbody"); 
            tableBody.innerHTML = ""; // Clear any existing rows

            registrations.forEach(registration => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${registration.CustomerName}</td>
                    <td>${registration.RoomNo}</td>
                    <td>${registration.CheckInDate}</td>
                    <td>${registration.CheckOutDate}</td>
                    <td>${registration.TotalAmount}</td>
                    <td>${registration.PaidAmount}</td>
                    <td>${registration.RemainingAmount}</td>
                    <td>${registration.Status}</td>
                    <td>
                        <button class="delete-btn" data-id="${registration.Id}">Delete</button>
                    </td>
                `;

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while loading registrations.");
        });
}
function toggleForm() {
    var form = document.getElementById("addCustomerForm");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
window.onload = loadCustomers;
