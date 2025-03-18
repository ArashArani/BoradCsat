document.addEventListener("DOMContentLoaded", () => {
  const PriceUSD = document.querySelectorAll(".price-toman");
  const MenuBtn = document.getElementById("MenuBtn");
  const CloseBtn = document.getElementById("CloseBtn");
  const HeaderRes = document.getElementById("HeaderRes");
  PriceUSD.forEach((item) => {
    const priceValue = Number(item.innerText);
    if (!isNaN(priceValue)) {
      item.innerText = priceValue.toLocaleString() + " تومان ";
    }
  });
  MenuBtn.addEventListener("click",()=>{
    HeaderRes.style.top = '0';
    CloseBtn.style.display = 'flex';
    MenuBtn.style.display = 'none'
  })
  CloseBtn.addEventListener("click",()=>{
    HeaderRes.style.top = '-120vh';
    CloseBtn.style.display = 'none';
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

function CopyText(){
  var textToCopy = document.getElementById("CardNumber").innerText ;
  var tempInput = document.createElement("textarea");
  tempInput.value = textToCopy;
  document.body.appendChild(tempInput);

  // انتخاب و کپی متن
  tempInput.select();
  document.execCommand("copy");

  // حذف عنصر موقت
  document.body.removeChild(tempInput);

  // پیام تایید
  alert(textToCopy + " کپی شد . ");
}