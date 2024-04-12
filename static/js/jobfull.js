console.log("hello")

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const jobid = urlParams.get('jobid')
console.log(jobid)

function Apply(){
bookmark(jobid)
}


function bookmark(jobId) {
    const jobdata = {
        jobId: jobId,
        status: "no-response"
    };

    const url = '/jobdata';

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jobdata)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Check if response is JSON, otherwise handle as error
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Unexpected response type');
            }
            return response.json();
        })
        .then(responseData => {
            console.log('applied data sent successfully:', responseData);
            alert("Applied for job successfully");
        })
        .catch(error => {
            console.error('Error sending bookmark data:', error);
            alert("Error applying for job");
        });
}
