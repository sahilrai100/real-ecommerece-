
let btn=document.querySelector('#btn')
let span=document.querySelector('#span')
let h=document.querySelector('#heading')

let body=document.body
btn.addEventListener('click',(e)=>{
    if(body.style.backgroundColor == 'black'){
        body.style.backgroundColor = 'white'
        span.textContent="🌙"
      
    }
    else{
        body.style.backgroundColor = 'black'
        span.textContent="☀️"
            
    }
})




