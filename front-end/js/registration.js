document.addEventListener("DOMContentLoaded", () => {
  const formContainer = document.getElementById("form-container");
  const step1 = document.getElementById("step1");
  const step2 = document.getElementById("step2");
  const step3 = document.getElementById("step3");
  const successMessage = document.getElementById("successMessage");
  const freelancerBtn = document.getElementById("freelancerBtn");
  const clientBtn = document.getElementById("clientBtn");
  const nextBtn = document.getElementById("nextBtn");
  const categoryButtons = document.getElementById("categoryButtons");
  const signupForm = document.getElementById("signupForm");

  let userType = "";
  let selectedCategory = "";

  freelancerBtn.addEventListener("click", () => {
    userType = "Freelancer";
    step1.classList.add("hidden");
    fetchCategories();
    step2.classList.remove("hidden");
  });

  clientBtn.addEventListener("click", () => {
    userType = "Client";
    step1.classList.add("hidden");
    step3.classList.remove("hidden");
  });

  nextBtn.addEventListener("click", () => {
    if (selectedCategory) {
      step2.classList.add("hidden");
      step3.classList.remove("hidden");
    } else {
      alert("Please select a category.");
    }
  });

  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    nextBtn.disabled = true;

    const formData = {
      user_type: userType,
      profile_category: userType === "Freelancer" ? selectedCategory : "Client",
      first_name: signupForm.first_name.value,
      last_name: signupForm.last_name.value,
      username: signupForm.username.value,
      email: signupForm.email.value,
      password: signupForm.password.value,
      confirm_password: signupForm.confirm_password.value,
    };


    fetch("http://127.0.0.1:8000/account/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
    .then(res=>res.json())
    .then(data=>{
      

      console.log("suc");
    })
    nextBtn.disabled = false;
    localStorage.setItem("username",signupForm.username.value)
    window.location.href=`http://127.0.0.1:5500/front-end/landing.html`
    /* const response = await fetch("http://127.0.0.1:8000/account/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    nextBtn.disabled = false;

    if (response) {
      const data = await response.json();
      
      if (data.message) {
        console.log(data.message);
        step3.classList.add("hidden");
        successMessage.classList.remove("hidden");
      } else {
        alert(data.error || "Registration failed. Please try again.");
      }
    } else {
      const errorData = await response.json();
      alert(errorData.error || "Registration failed. Please try again.");
    } */
  });

  async function fetchCategories() {
    const response = await fetch(
      "http://127.0.0.1:8000/category/category-list/"
    );
    const data = await response.json();

    data.forEach((category) => {
      const button = document.createElement("button");
      button.className =
        "bg-gray-200 text-gray-700 px-4 py-2 m-2 rounded-full shadow hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400";
      button.textContent = category.category_name;
      button.onclick = () => {
        selectedCategory = category.category_name;
        document
          .querySelectorAll("#categoryButtons button")
          .forEach((btn) => btn.classList.remove("bg-gray-300"));
        button.classList.add("bg-gray-300");
      };
      categoryButtons.appendChild(button);
    });
  }
});




