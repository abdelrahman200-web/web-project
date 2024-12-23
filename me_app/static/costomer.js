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
function loadCustomers() {
    fetch('/customers')
        .then(response => response.json())
        .then(customers => {
            const tableBody = document.querySelector("#customerTableBody tbody"); 
            tableBody.innerHTML = ""; 

            customers.forEach(customer => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${customer.identity}</td>
                    <td>${customer.name}</td>
                    <td>${customer.phone}</td>
                    <td>${customer.another_phone || "N/A"}</td>
                    <td>${customer.age}</td>
                    <td>${customer.email || "N/A"}</td>
                    <td>${customer.nationality}</td>
                    <td>${customer.type_of_proof_of}</td>
                    <td>
                        <button class="delete-btn" data-id="${customer.identity}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while loading customers.");
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
