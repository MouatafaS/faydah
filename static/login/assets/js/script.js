// Signup Page
const form = document.querySelector("form"),
  nextBtn = form.querySelector(".nextBtn"),
  backBtn = form.querySelector(".backBtn"),
  submitBtn = form.querySelector(".submit"), // Added a reference to the submit button
  allInput = form.querySelectorAll(".first input");

let currentPage = 1; // Track the current page of the form

nextBtn.addEventListener("click", (e) => {
  e.preventDefault(); // Prevent the default form submission

  if (currentPage === 1) {
    // Check if all required fields are filled on the first page
    let allFieldsFilled = true;

    allInput.forEach((input) => {
      if (input.value === "") {
        allFieldsFilled = false;
        input.classList.add("required");
      } else {
        input.classList.remove("required");
      }
    });

    if (!allFieldsFilled) {
      // Optionally, display an error message or take action if fields are not filled
      return;
    }
  }

  currentPage++;

  if (currentPage === 2) {
    form.classList.add("secActive");
    nextBtn.style.display = "none";
  }
});

backBtn.addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage--;
    form.classList.remove("secActive");
    nextBtn.style.display = "block";
  }
});

// Handle form submission on the final step
submitBtn.addEventListener("click", () => {
  // Optionally, you can perform final validation here before submitting
  form.submit(); // Submit the form
});
