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

// Function to handle file upload
// Function to handle file upload



// Define the fetch request outside the function
const form1 = document.getElementById('form');

form1.addEventListener('submit', function(event) {
  // Prevent default HTML page refresh
  event.preventDefault();

  // Select file upload element
  const uploadElement = document.getElementById('file');

  // Extract the file (for a single file, always 0 in the list)
  const file = uploadElement.files[0];

  // Create new formData object then append file
  const payload = new FormData();
  payload.append('CV', file, 'CV.pdf');

  // POST/PUT with Fetch API
  fetch('https://httpbin.org/post', {
    method: "POST", // or "PUT"
    body: payload,
    // No content-type! With FormData obect, Fetch API sets this automatically.
    // Doing so manually can lead to an error
  })
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.log(err))
});

//input drop box
const dropContainer = document.getElementById("dropcontainer")
const fileInput = document.getElementById("images")

dropContainer.addEventListener("dragover", (e) => {
    // prevent default to allow drop
    e.preventDefault()
}, false)

dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active")
})

dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active")
})

dropContainer.addEventListener("drop", (e) => {
    e.preventDefault()
    dropContainer.classList.remove("drag-active")
    fileInput.files = e.dataTransfer.files
})
