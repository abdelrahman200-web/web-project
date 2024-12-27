function fetchRegistrations() {
    fetch('/customers')
        .then(response => response.json())
        .then(registrations => {
            const tableBody = document.querySelector("#customerTableBody tbody"); 
            tableBody.innerHTML = ""; // Clear any existing rows

            registrations.forEach(registration => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${registration.identity}</td>
                    <td>${registration.name}</td>
                    <td>${registration.phone}</td>
                    <td>${registration.another_phone}</td>
                    <td>${registration.age}</td>
                    <td>${registration.email}</td>
                    <td>${registration.nationality}</td>
                    <td>${registration.type_of_proof_of}</td>
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
                fetchRegistrations(); 
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
function toggleForm() {
    var form = document.getElementById("addCustomerForm");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
window.onload = fetchRegistrations;
