// document.addEventListener("DOMContentLoaded", function() {
    var jobDataElement = document.getElementById("job-data");
    var jobDataString = jobDataElement.textContent.trim();
    
    var jobData = JSON.parse(jobDataString);

    var originalElement = document.querySelector('.mbox'); // Select the original element outside the loop
      console.log(jobData.length)

      if(jobData.length >0){
    for (var i = 0; i < jobData.length; i++) {
        var nowDate = new Date();
        
        // Clone the original element
        var clonedElement = originalElement.cloneNode(true);
        
        // Update content of cloned elements with job data
        clonedElement.querySelector("#role").innerText = jobData[i].General_info.name;
        clonedElement.querySelector("#compname").innerText = jobData[i].General_info.companyname;
        clonedElement.querySelector("#salary").innerText = jobData[i].qualification_salary.salary_range;
        clonedElement.querySelector("#cityloc").innerText = jobData[i].location_more.city;
        clonedElement.querySelector("#exp").innerText = jobData[i].General_info.exp;
        clonedElement.querySelector("#jobdesc").innerText = jobData[i].location_more.job_description;

        // Calculate and display job age
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
        clonedElement.querySelector("#timeago").innerText = ago;
        
        // Append the cloned element to the parent of the original element
        originalElement.parentNode.appendChild(clonedElement);
    }
    
}
originalElement.remove();
// Remove the original element from the DOM
    
// });
