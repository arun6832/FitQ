const formSteps = document.querySelectorAll('.form-step');
const progressBar = document.querySelector('.progress');
let currentStep = 0;

// List of countries
const countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", 
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", 
    "Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", 
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", 
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", 
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", 
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", 
    "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", 
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", 
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", 
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", 
    "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", 
    "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", 
    "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", 
    "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", 
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
];

// Populate country dropdown
const countrySelect = document.getElementById('country');
countries.forEach(country => {
    const option = document.createElement('option');
    option.value = country;
    option.textContent = country;
    countrySelect.appendChild(option);
});

// Navigate to the next step
function nextStep() {
    if (!validateCurrentStep()) return;

    formSteps[currentStep].classList.remove('active');
    currentStep++;
    if (currentStep < formSteps.length) {
        formSteps[currentStep].classList.add('active');
        updateProgressBar();
    }
}

// Navigate to the previous step
function prevStep() {
    formSteps[currentStep].classList.remove('active');
    currentStep--;
    if (currentStep >= 0) {
        formSteps[currentStep].classList.add('active');
        updateProgressBar();
    }
}

// Review step function
function reviewStep() {
    if (!validateCurrentStep()) return; // Ensure validation before proceeding

    updateReview();
    formSteps[currentStep].classList.remove('active');
    currentStep++;
    formSteps[currentStep].classList.add('active');
    updateProgressBar();
}

// Edit step function
function editStep() {
    formSteps[currentStep].classList.remove('active');
    currentStep--;
    formSteps[currentStep].classList.add('active');
    updateProgressBar();
}

// Update progress bar
function updateProgressBar() {
    const progressPercent = ((currentStep + 1) / formSteps.length) * 100;
    progressBar.style.width = `${progressPercent}%`;
}

function validateCurrentStep() {
    const currentInputs = formSteps[currentStep].querySelectorAll('input, select');
    let valid = true;

    currentInputs.forEach(input => {
        if (input.id === 'dob' && !validateAge(input)) {
            valid = false;
        } else if (!input.checkValidity()) {
            valid = false;
            if (input.id === 'employment' && input.value === '') {
                document.getElementById('employmentError').textContent = 'Employment status is required.';
            } else if (input.id === 'height' && input.value === '') {
                document.getElementById('heightError').textContent = 'Height is required.';
            } else if (input.id === 'weight' && input.value === '') {
                document.getElementById('weightError').textContent = 'Weight is required.';
            }
            input.reportValidity();
        } else {
            if (input.id === 'employment') {
                document.getElementById('employmentError').textContent = '';
            } else if (input.id === 'height') {
                document.getElementById('heightError').textContent = '';
            } else if (input.id === 'weight') {
                document.getElementById('weightError').textContent = '';
            } else if (input.id === 'dob') {
                document.getElementById('dobError').textContent = '';
            }
        }
    });

    return valid;
}



// Validate age based on date of birth
function validateAge(input) {
    const dob = new Date(input.value);
    const today = new Date();
    const age = today.getFullYear() - dob.getFullYear();
    const monthDifference = today.getMonth() - dob.getMonth();
    const dayDifference = today.getDate() - dob.getDate();

    if (
        age < 18 ||
        (age === 18 && (monthDifference < 0 || (monthDifference === 0 && dayDifference < 0)))
    ) {
        document.getElementById('dobError').textContent = 'You must be at least 18 years old.';
        input.setCustomValidity('Invalid age');
        return false;
    } else {
        document.getElementById('dobError').textContent = '';
        input.setCustomValidity('');
        return true;
    }
}

// Navigate to the next step
function nextStep() {
    if (!validateCurrentStep()) return; // Only proceed if the current step is valid

    formSteps[currentStep].classList.remove('active');
    currentStep++;
    if (currentStep < formSteps.length) {
        formSteps[currentStep].classList.add('active');
        updateProgressBar();
    }
}

// Update review information
function updateReview() {
    // Get the original date input value
    const dobInput = document.getElementById('dob').value;
    const formattedDob = formatDate(dobInput);

    // Capitalize the first letter of gender and employment status
    const genderInput = capitalizeFirstLetter(document.getElementById('gender').value);
    const employmentInput = capitalizeFirstLetter(document.getElementById('employment').value);

    // Update the review fields
    document.getElementById('reviewFirstName').textContent = document.getElementById('name').value;
    document.getElementById('reviewGender').textContent = genderInput; // Use the capitalized gender
    document.getElementById('reviewDob').textContent = formattedDob;
    document.getElementById('reviewCountry').textContent = document.getElementById('country').value;
    document.getElementById('reviewEmployment').textContent = employmentInput; // Use the capitalized employment status
    document.getElementById('reviewHeight').textContent = document.getElementById('height').value;
    document.getElementById('reviewWeight').textContent = document.getElementById('weight').value;
}

// Helper function to format date as DD/MM/YYYY
function formatDate(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}-${month}-${year}`;
}

// Helper function to capitalize the first letter of a string
function capitalizeFirstLetter(string) {
    if (!string) return '';
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

// Handle form submission
document.getElementById('fitnessForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Form submitted successfully!');
});
