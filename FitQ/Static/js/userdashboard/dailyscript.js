document.getElementById("submitButton").addEventListener("click", function() {
    const sleepDuration = document.getElementById("sleepDuration").value;
    const waterIntake = document.getElementById("waterIntake").value;
    const screenTime = document.getElementById("screenTime").value;

    // Validate sleep duration
    if (sleepDuration < 1 || sleepDuration > 24) {
        alert("Please enter a valid sleep duration between 1 and 24 hours.");
        return;
    }

    // Validate water intake and screen time
    if (waterIntake < 0) {
        alert("Water intake cannot be negative.");
        return;
    }

    if (screenTime < 0) {
        alert("Screen time cannot be negative.");
        return;
    }

    // If all validation passes
    document.getElementById("wellnessForm").classList.add("hidden");
    document.getElementById("successMessage").classList.remove("hidden");
});



// document.addEventListener("DOMContentLoaded", function() {
//     const successMessage = document.getElementById("successMessage");
//     const form = document.getElementById("wellnessForm");
//     const submitButton = document.getElementById("submitButton");

//     // Get current date and store it
//     const today = new Date().toDateString(); // 'Mon Sep 30 2024' format
//     let currentDay = parseInt(localStorage.getItem("currentDay")) || 1; // Start from Day 1

//     // Check if the user has already submitted for today
//     const lastSubmissionDate = localStorage.getItem("lastSubmissionDate");
    
//     if (lastSubmissionDate === today) {
//         form.classList.add("hidden");
//         successMessage.classList.remove("hidden");
//     } else {
//         successMessage.classList.add("hidden");
//         form.classList.remove("hidden");
//     }

//     submitButton.addEventListener("click", function() {
//         const sleepDuration = document.getElementById("sleepDuration").value;
//         const waterIntake = document.getElementById("waterIntake").value;
//         const screenTime = document.getElementById("screenTime").value;

//         // Validate sleep duration
//         if (sleepDuration < 1 || sleepDuration > 24) {
//             alert("Please enter a valid sleep duration between 1 and 24 hours.");
//             return;
//         }

//         // Validate water intake and screen time
//         if (waterIntake < 0) {
//             alert("Water intake cannot be negative.");
//             return;
//         }

//         if (screenTime < 0) {
//             alert("Screen time cannot be negative.");
//             return;
//         }

//         // Save the form data for the current day in local storage
//         const formData = {
//             sleepDuration,
//             waterIntake,
//             screenTime,
//             workoutDuration: document.getElementById("workoutDuration").value,
//             problemsDuringDay: document.getElementById("problemsDuringDay").value,
//             foodOnTime: document.getElementById("foodOnTime").value,
//             typeOfFood: document.getElementById("typeOfFood").value,
//             smokingHabit: document.getElementById("smokingHabit").value,
//             alcoholConsumption: document.getElementById("alcoholConsumption").value,
//         };

//         localStorage.setItem(`day${currentDay}Data`, JSON.stringify(formData));
//         localStorage.setItem("lastSubmissionDate", today);

//         // Show success message and hide the form
//         form.classList.add("hidden");
//         successMessage.classList.remove("hidden");

//         // Update to the next day for tomorrow
//         if (currentDay < 7) {
//             currentDay++;
//             localStorage.setItem("currentDay", currentDay);
//         } else {
//             alert("You have completed all 7 days!");
//         }
//     });
// });
