import { CreatePost } from "../components/create_post";
const category_section = document.getElementById("category-section");

const add_categories = async () => {
  const response = await fetch("http://127.0.0.1:8000/category/category-list/");
  let categories = await response.json();

  categories.forEach((category) => {
    category_section.innerHTML += `
        <div class="px-6 py-3 bg-orange-400 rounded-lg text-center text-white text-3xl">${category.category_name}</div>
        `;
  });
};

add_categories();
const user = localStorage.getItem("username");

async function getUser() {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/account/get-client-profiles/?user_name=${user}`
    );
    const data = await response.json();
    return data[0];
  } catch (error) {
    console.error("Error fetching user data:", error);
    return null;
  }
}

getUser().then((data) => console.log(data));

async function setData() {
  const useInfo = await getUser();
  const userType = useInfo.account_type;

  if (userType == "Client") {
  } else if (userType == "Freelancer") {
  }
}

setData();

const client_root = document.getElementById("client_root");
console.log(client_root);
client_root.innerHTML += CreatePost
