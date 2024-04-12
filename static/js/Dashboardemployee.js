// Get the form element by its class name

var form = document.querySelector('.datasection');

// Get all input and select elements within the form
var inputs = form.querySelectorAll('input, select');

function toggleSection(sectionId) {
    const allSections = document.querySelectorAll('.midright > div'); // Select all sections
    allSections.forEach(section => {
        if (section.id === sectionId) {
            section.style.display = 'flex'; // Show the selected section
        } else {
            section.style.display = 'none'; // Hide other sections
        }
    });
}

// Loop through each input element and set the disabled attribute
for (var i = 0; i < inputs.length; i++) {
    inputs[i].disabled = true;
}

function enableInputs() {
    var inputs = document.querySelectorAll('.box1 .datasection input, .box1 .datasection select');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].readOnly = false;
        inputs[i].disabled = false;
    }
    document.getElementById('editButton').style.display = 'none';
    document.getElementById('saveButton').style.display = 'inline-block';
}

// function saveInputs() {
//     var inputs = document.querySelectorAll('.box1 .datasection input, .box1 .datasection select');
//     for (var i = 0; i < inputs.length; i++) {
//         inputs[i].readOnly = true;
//         inputs[i].disabled = true;
//     }
//     document.getElementById('editButton').style.display = 'inline-block';
//     document.getElementById('saveButton').style.display = 'none';
// }





//taking data input
function saveInputs() {
    var profileData = {
        personal_info: {
            name: document.getElementById('name').value,
            dob: document.getElementById('dob').value,
            gender: document.getElementById('gender').value,
            age: document.getElementById('age').value,
            phone: document.getElementById('phone').value,
            country: document.getElementById('country').value,
            qualification: document.getElementById('qualification').value,
            experience: document.getElementById('experience').value,
            languages: document.getElementById('languages').value,
            salary_type: document.getElementById('salary_type').value,
            expected_salary: document.getElementById('expected_salary').value,
            job_category: document.getElementById('job_category').value
        }
    };

    console.log(profileData)

    var inputs = document.querySelectorAll('.box1 .datasection input, .box1 .datasection select');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].readOnly = true;
        inputs[i].disabled = true;
    }
    document.getElementById('editButton').style.display = 'inline-block';
    document.getElementById('saveButton').style.display = 'none';

    $.ajax({
        type: "POST",
        url: "/Dashboardemp", // URL of your Flask endpoint
        contentType: "application/json",
        data: JSON.stringify(profileData),
        success: function(response) {
            console.log("Data saved successfully")
            showPopup();
        },
        error: function(error) {
            console.error("Error saving data:", error);
        }
    });
}

function showPopup() {
    var popup = document.getElementById('popup');
    popup.style.display = 'block';
    setTimeout(function() {
        popup.style.display = 'none';
    }, 500); // Hide popup after 2 seconds
}

// fetching all necessary data 
