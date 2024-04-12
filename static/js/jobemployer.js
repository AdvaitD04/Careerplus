document.addEventListener("DOMContentLoaded", function() {
    var jobDataElement = document.getElementById("job-data");
    var jobDataString = jobDataElement.textContent.trim();
    var jobData = JSON.parse(jobDataString);
    var originalElement = document.querySelector('.mbox'); // Select the original element outside the loop
    var clonedElements = []; // Array to store cloned elements
    var no = [];

    function printJobData(jobData) {
        console.log(jobData.length);
        
        // Remove existing cloned elements
        clonedElements.forEach(function(clonedElement) {
            clonedElement.remove();
        });

        // Clear the array of cloned elements
        clonedElements = [];

        if (jobData.length > 0) {
            for (var i = 0; i < jobData.length; i++) {
                var nowDate = new Date();
                var clonedElement = originalElement.cloneNode(true);
                clonedElement.querySelector("#role").innerText = jobData[i].General_info.name;
                clonedElement.querySelector("#compname").innerText = jobData[i].General_info.companyname;
                clonedElement.querySelector("#salary").innerText = jobData[i].qualification_salary.salary_range;
                clonedElement.querySelector("#cityloc").innerText = jobData[i].location_more.city;
                clonedElement.querySelector("#exp").innerText = jobData[i].General_info.exp;
                clonedElement.querySelector("#jobdesc").innerText = jobData[i].location_more.job_description;
                var jobDate = new Date(jobData[i].General_info.currentDate);
                var timeDiff = nowDate.getTime() - jobDate.getTime();
                var daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));
                var ago;
                if (daysDiff === 0) {
                    ago = "Today";
                } else if (daysDiff === 1) {
                    ago = "1 Day ago";
                } else if (daysDiff > 1) {
                    ago = daysDiff + " days ago";
                } else {
                    ago = "Unknown";
                }

                // Get the ObjectId as a string
        var objectId = jobData[i]._id;

        // Set data-job-id attribute with the ObjectId
        var bookmarkIcon = clonedElement.querySelector('.bookmark-icon');
        var searchid = clonedElement.querySelector('.bmid');
        bookmarkIcon.setAttribute('data-job-id', objectId);
        no [i+1] = bookmarkIcon.getAttribute('data-job-id');
        console.log(no[i+1]);

        searchid.setAttribute('idforjob', objectId);
        

        

        

    
        


                clonedElement.querySelector("#timeago").innerText = ago;
                // Append the cloned element to its parent
                if (originalElement.parentNode) {
                    originalElement.parentNode.appendChild(clonedElement);
                }
                // Set display property after appending the element
                clonedElement.style.display = 'flex';

                // Add cloned element to the array
                clonedElements.push(clonedElement);

                
            }
        }
    }

    function fetchJobsByLocation(locations) {
        const filters = {
            locations:locations
        };
        
        fetch('/jobemployer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(datajob => {
            jobData = datajob;
            console.log('Received data:', datajob);
            printJobData(jobData);
        })

        .catch(error => {
            console.error('Error fetching job listings:', error);
        });
    }

    var checkboxes = document.querySelectorAll('input[type="checkbox"][name="location"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            var selectedLocations = [];
            document.querySelectorAll('input[type="checkbox"][name="location"]:checked').forEach(function(checkedCheckbox) {
                selectedLocations.push(checkedCheckbox.value);
            });
            fetchJobsByLocation(selectedLocations);
        });
    });

    fetchJobsByLocation([]);
});



function bookmark(jobId) {
    
    console.log(jobId);

    const data = {
        jobId:jobId
    };

    const url = '/jobemployer';

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })

    .then(response =>{
        if(!response.ok){
            throw new Error('Network response was not ok');
        }

        return response.json();
    })

    .then(responseData => {
        console.log('Bookmark data sent successfully:', responseData);
        // it is optional
    })

    .catch(error => {
        console.error('Error sending bookmark data:', error);
    });

    
}


function check(jobId) {
    console.log(jobId);
    
    // Open the jobdata page with the jobid as a query parameter in a new tab
    window.open("/jobdata" + "?jobid=" + jobId, "_blank");
}










