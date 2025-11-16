function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function RedirectTo(url,time=1000) {
    console.log(url)
    setTimeout(() => {
        window.location.href = url;
      }, time);
}

document.addEventListener('htmx:afterRequest', function(event) { //
    const xhr = event.detail.xhr;

    // Check for 401 Unauthorized status from the backend
    if (xhr.status === 403) { //
        console.log("Session invalid or expired. Redirecting to login page."); //
        // Redirect the user to the login page
        window.location.href = '/login'; // Or your actual login page path
    } else if (xhr.status === 404) { //
        console.log("Resource not found. Redirecting to home page or error page."); //
        // Redirect the user to the home page or a specific error page
        window.location.href = '/'; // Or your dedicated error page path
    }

});

document.addEventListener('htmx:afterOnLoad', function(event) {
    // Check if the response is valid JSON
    let responseData;
    console.log(event.detail.xhr.response,"ress")
    try {
        responseData = JSON.parse(event.detail.xhr.response);
    } catch (e) {
        console.error("Response is not valid JSON:", e);
        return; // Exit if the response is not JSON
    }
    // Check if the JSON has the expected structure
    if (responseData.message && responseData.category) {
        const messageContainer = document.getElementById('flash-message');
        
        messageContainer.className = `flash-message ${responseData.category}`;
        messageContainer.innerHTML = `
            ${responseData.message}
            <span style="margin-left:15px; cursor:pointer; font-weight:bold;">&times;</span>
        `;
        // Make sure the container is visible if it was hidden
        messageContainer.style.display = 'block';

        const redirectUrl = responseData.redirect_url;

        setTimeout(() => {
          messageContainer.style.display = 'none';
          if (redirectUrl) {
            window.location.href = redirectUrl;
          }
        }, 1000);
    }    

});