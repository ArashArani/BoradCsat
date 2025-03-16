document.addEventListener("DOMContentLoaded", () => {
  const PriceUSD = document.querySelectorAll(".price-toman");
  PriceUSD.innerText = Number(PriceUSD.innerText).toLocaleString();
  PriceUSD.forEach((item) => {
    item.innerText = Number(item.innerText).toLocaleString() + " تومان ";
  });
});
document.addEventListener("DOMContentLoaded", function () {
  // انتخاب تمام آیکون‌های نمایش و پنهان کردن پسورد
  const showPassIcons = document.querySelectorAll(".show-pass");
  const noShowIcons = document.querySelectorAll(".no-show");
  const passwordInputs = document.querySelectorAll(".password-input");

  showPassIcons.forEach((icon, index) => {
    icon.addEventListener("click", () => {
      passwordInputs[index].type = "text"; // تغییر نوع input به text
      icon.style.display = "none"; // پنهان کردن آیکون چشم
      noShowIcons[index].style.display = "block"; // نمایش آیکون بستن
    });
  });

  noShowIcons.forEach((icon, index) => {
    icon.addEventListener("click", () => {
      passwordInputs[index].type = "password"; // تغییر نوع input به password
      icon.style.display = "none"; // پنهان کردن آیکون بستن
      showPassIcons[index].style.display = "block"; // نمایش آیکون چشم
    });
  });
});

function calculateFinalPrice() {
  const priceInput = document.getElementById("price");
  const discountInput = document.getElementById("Discount");
  const finalPriceInput = document.getElementById("FinalPrice");

  const price = parseFloat(priceInput.value) || 0; // تبدیل به عدد، در صورت خالی بودن 0 می‌گیرد
  const discount = parseFloat(discountInput.value) || 0; // تبدیل به عدد، در صورت خالی بودن 0 می‌گیرد

  const finalPrice = price - price * (discount / 100); // محاسبه قیمت نهایی

  // فرمت‌بندی قیمت نهایی و نمایش به همراه واحد
  finalPriceInput.value = finalPrice.toLocaleString("fa-IR") + " تومان";
}
calculateFinalPrice();

function CopyText(index) {
  let textToCopy;

  // انتخاب متن بر اساس index
  switch (index) {
    case 1:
      textToCopy = document.querySelectorAll(".card-info-value h4")[0]
        .innerText; // Account Name
      break;
    case 2:
      textToCopy = document.querySelectorAll(".card-info-value h4")[1]
        .innerText; // Sort Code
      break;
    case 3:
      textToCopy = document.querySelectorAll(".card-info-value h4")[2]
        .innerText; // Account Number
      break;
    default:
      return;
  }

  // ایجاد یک عنصر textarea موقت
  var tempInput = document.createElement("textarea");
  tempInput.value = textToCopy;
  document.body.appendChild(tempInput);

  // انتخاب و کپی متن
  tempInput.select();
  document.execCommand("copy");

  // حذف عنصر موقت
  document.body.removeChild(tempInput);

  // پیام تایید
  alert("Text copied to clipboard: " + textToCopy);
}

document.addEventListener("DOMContentLoaded", () => {
  const AdminMnu = document.getElementById("AdminMnu");
  const SideBar = document.getElementById("SideBar");
  const PanelContent = document.getElementById("PanelContent");
  const AdminX = document.getElementById("AdminX");
  AdminMnu.addEventListener("click", () => {
    SideBar.classList.toggle("Active-sidebar");
    AdminMnu.style.display = "none";
    AdminX.style.display = "block";
    PanelContent.classList.toggle("content-active");
  });

  AdminX.addEventListener("click", () => {
    SideBar.classList.remove("Active-sidebar");
    PanelContent.classList.remove("content-active");
    AdminX.style.display = "none";
    AdminMnu.style.display = "block";
  });
});
function checkInput() {
  const emailInput = document.getElementById("emailInput");
  const continueBtn = document.getElementById("continueBtn");

  // Enable the button if the input is not empty
  continueBtn.disabled = !emailInput.value.trim();
}
function toggleReadonly(checkbox) {
  const inputField = document.getElementById("link");
  const stock = document.getElementById("stock");
  inputField.readOnly = !checkbox.checked;
  stock.readOnly = checkbox.checked;
}
const FirstStep = document.getElementById("FirstStep");
const StepDiv1 = document.getElementById("StepDiv1");
const StepDiv2 = document.getElementById("StepDiv2");
const SecendStep = document.getElementById("SecendStep");
function SwipeForward() {
  FirstStep.classList.toggle("First-Step-Done");
  StepDiv1.classList.toggle("done-step-div");
  StepDiv2.classList.toggle("focus-step");
  SecendStep.classList.toggle("Active-Step");
}
function SwipeBack() {
  FirstStep.classList.toggle("First-Step-Done");
  StepDiv1.classList.toggle("done-step-div");
  StepDiv2.classList.toggle("focus-step");
  SecendStep.classList.toggle("Active-Step");
}

document.addEventListener("DOMContentLoaded", () => {
  const HeaderLogin = document.getElementById("HeaderLogin");
  const MenuBtn = document.getElementById("MenuBtn");
  const HeaderSearchRes = document.getElementById("HeaderSearchRes");
  const HeaderBody = document.getElementById("HeaderBody");
  const XBtn = document.getElementById("Xbtn");

  MenuBtn.addEventListener("click", () => {
    HeaderSearchRes.classList.toggle("active-search");
    HeaderBody.classList.toggle("active-body");
    HeaderLogin.classList.toggle("active-login");
    MenuBtn.classList.toggle("menu-rot");
    XBtn.classList.toggle("menu-ac");

    // Use animationend to hide the button after the animation
    MenuBtn.addEventListener(
      "animationend",
      () => {
        MenuBtn.style.display = "none";
        XBtn.style.display = "block";
        MenuBtn.classList.toggle("menu-rot");
        XBtn.classList.toggle("menu-ac");
      },
      { once: true }
    );
  });

  XBtn.addEventListener("click", () => {
    HeaderSearchRes.classList.toggle("active-search");
    HeaderBody.classList.toggle("active-body");
    HeaderLogin.classList.toggle("active-login");

    XBtn.classList.toggle("menu-rot");
    MenuBtn.classList.toggle("menu-ac");

    // Use animationend to hide the button after the animation
    XBtn.addEventListener(
      "animationend",
      () => {
        XBtn.style.display = "none"; // Hide the close button
        MenuBtn.style.display = "block"; // Show the menu button
        XBtn.classList.toggle("menu-rot");
        MenuBtn.classList.toggle("menu-ac");
      },
      { once: true }
    );
  });
});
