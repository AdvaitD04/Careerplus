// Get the form element by its class name
var currentDate = new Date();
var form = document.querySelector('.datasection');

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


// Get all input and select elements within the form
var inputs = form.querySelectorAll('input, select');

// Loop through each input element and set the disabled attribute
for (var i = 0; i < inputs.length; i++) {
    inputs[i].disabled = true;
}

function enableInputs() {
    var inputs = document.querySelectorAll('.profile .box1 .datasection input,.profile .box1 .datasection select');
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



function showprofile() {
    var profile = document.querySelector('.profile');
    profile.style.display = "none";
}

//taking data input
function saveInputs() {
    var profileData = {
        personal_info: {
            name: document.getElementById('compname').value,
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
    console.log("hello world");

    console.log(profileData)

    var inputs = document.querySelectorAll('.profile .box1 .datasection input,.profile .box1 .datasection select');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].readOnly = true;
        inputs[i].disabled = true;
    }
    document.getElementById('editButton').style.display = 'inline-block';
    document.getElementById('saveButton').style.display = 'none';

    $.ajax({
        type: "POST",
        url: "/Dashboardemployer", // URL of your Flask endpoint
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

function submitFormData() {

    if (!validateForm()) {
        return; // Exit function if validation fails
    }
    var jobcreation = {
        General_info: {
            name: document.getElementById('jobtitle').value,
            job_type: document.getElementById('Job type').value,
            tag: document.getElementById('Tag').value,
            Categ: document.getElementById('Categ').value,
            exp: document.getElementById('exp').value,
            gender: document.getElementById('genderjob').value,
            age: document.getElementById('ager').value,
            job_email: document.getElementById('jemail').value,
            companyname: document.getElementById('compname2').value,
            currentDate: currentDate.toISOString()

        },
        qualification_salary: {
            salary_type: document.getElementById('salary_type').value,
            salary_range: document.getElementById('salary').value,
            skill_required: document.getElementById('skills').value,
            qualification_required: document.getElementById('qualification').value
        },
        location_more: {
            job_location: document.getElementById('joblocation').value,
            city_type: document.getElementById('city type').value,
            country: document.getElementById('country').value,
            city: document.getElementById('city').value,
            job_deadline: document.getElementById('jobdeadline').value,
            job_description: document.getElementById('Job description').value
        }
    };

    console.log(jobcreation);

    $.ajax({
        type: "POST",
        url: "/Dashboardemployer", // URL of your Flask endpoint
        contentType: "application/json",
        data: JSON.stringify(jobcreation),
        success: function(response) {
            console.log("Data saved successfully")
            showPopup();
        },
        error: function(error) {
            console.error("Error saving data:", error);
        }
    });
}


function validateForm() {
    // Validate each form field
    var isValid = true;
    var isEmpty = false;
    var requiredFields = document.querySelectorAll('.Addjob .datasection [required]');
    requiredFields.forEach(function(field) {
        if (!field.value) {
            isValid = false;
            isEmpty = true;
            return;
        }
    });

    // If any field is empty, show alert message
    if (isEmpty) {
        alert("Please fill out all required fields.");
    }

    // Return validation result
    return isValid;
}

function showPopup() {
    var popup = document.getElementById('popup');
    popup.style.display = 'block';
    setTimeout(function() {
        popup.style.display = 'none';
    }, 500); // Hide popup after 2 seconds
}


var jobDate = new Date("2024-03-18");

// Calculate the difference in milliseconds between current date and jobDate
var timeDiff = currentDate.getTime() - jobDate.getTime();

// Convert time difference from milliseconds to days
var daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));

// Display the job age
if (daysDiff === 0) {
    console.log("Today");
} else if (daysDiff === 1) {
    console.log("1 day ago");
} else {
    console.log(daysDiff + " days ago");
}

// fetching all necessary data 


