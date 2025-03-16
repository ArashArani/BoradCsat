document.addEventListener("DOMContentLoaded", () => {
  const PriceUSD = document.querySelectorAll(".price-toman");
  PriceUSD.innerText = Number(PriceUSD.innerText).toLocaleString();
  PriceUSD.forEach((item) => {
    item.innerText = Number(item.innerText).toLocaleString() + " تومان ";
  });

  const HeaderRes = document.getElementById("HeaderRes");
  const CloseBtn = document.getElementById("CloseBtn");
  const MenuBtn = document.getElementById("MenuBtn");

  MenuBtn.addEventListener("click",()=>{
    HeaderRes.style.top = '0'
    CloseBtn.style.display = 'flex'
    MenuBtn.style.display = 'none'
  });
  CloseBtn.addEventListener("click",()=>{
    HeaderRes.style.top = '-100vh'
    CloseBtn.style.display = 'none'
    MenuBtn.style.display = 'flex'
  })




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

document.addEventListener("DOMContentLoaded", ()=> {
 


});
