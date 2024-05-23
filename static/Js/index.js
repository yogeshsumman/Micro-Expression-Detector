// Animation on scroll
const observer = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=> {
      if (entry.isIntersecting) {
        entry.target.classList.add('show')
      }else{
        entry.target.classList.remove('show')
      }
    })
  })
  
  const hiddenEle = document.querySelectorAll('.hidden-left')
  hiddenEle.forEach((el) => observer.observe(el));
  
  const observerRight = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=> {
      // console.log(entry);
      if (entry.isIntersecting) {
        entry.target.classList.add('show')
      }else{
        entry.target.classList.remove('show')
      }
    })
  })
  
  const hiddenRightEle = document.querySelectorAll('.hidden-right')
  hiddenRightEle.forEach((el) => observerRight.observe(el));
  
  // Navbar scroll animation
  let navbar = document.getElementById('navbar')
  function navColorChange() {
    let scrollValue = window.scrollY
    
    console.log(scrollValue);
    if (scrollValue > 160) {
      navbar.classList.add('navBg')
    }else{
      navbar.classList.remove('navBg')
    }
  }
  
  window.addEventListener('scroll' , navColorChange)
  