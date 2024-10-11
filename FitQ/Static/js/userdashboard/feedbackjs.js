// feedbackjs.js

document.addEventListener("DOMContentLoaded", () => {
    const feedbackForm = document.getElementById('feedbackForm');
    const responseMessage = document.getElementById('responseMessage');

    feedbackForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Input validation
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        // Clear previous error messages
        clearErrors();

        let isValid = true;

        if (name === "") {
            showError('nameError', 'Name is required.');
            isValid = false;
        }

        if (email === "") {
            showError('emailError', 'Email is required.');
            isValid = false;
        } else if (!validateEmail(email)) {
            showError('emailError', 'Please enter a valid email.');
            isValid = false;
        }

        if (message === "") {
            showError('messageError', 'Feedback is required.');
            isValid = false;
        }

        if (isValid) {
            responseMessage.innerText = "Thank you for your feedback!";
            feedbackForm.reset(); // Reset the form
        }
    });

    function showError(id, message) {
        const errorElement = document.getElementById(id);
        errorElement.innerText = message;
    }

    function clearErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => element.innerText = "");
    }

    function validateEmail(email) {
        const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return re.test(email);
    }
});
