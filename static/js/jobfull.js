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
        jobId:jobId,
        status:"no-response"
    };

    const url = '/jobdata';

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jobdata)
    })

    .then(response =>{
        if(!response.ok){
            throw new Error('Network response was not ok');
        }

        return response.json();
    })

    .then(responseData => {
        console.log('applyed data sent successfully:', responseData);
        // it is optional
        
    })

    .catch(error => {
        console.error('Error sending bookmark data:', error);
    });

    
}