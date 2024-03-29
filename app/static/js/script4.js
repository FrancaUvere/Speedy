const previous = document.querySelector('#previous')
const next = document.querySelector('#next')
const accounts = document.getElementsByClassName('bal')
const transaction = document.querySelector('#show')
const pop_up = document.querySelector('#pop_up')
const cancel = document.querySelector('#cancel')
const open = document.querySelector('#open')

let index=0;
let i = 0;

let currentUrl = window.location.href
let searchParams = new URLSearchParams(window.location.search);

const id="id"
let arg;
let updateURL=0;
next.addEventListener('click', ()=>{
    if (index < accounts.length){
        accounts[index+1].style.display = 'block'
        accounts[index].style.display = "none"
        arg = accounts[index+1].getAttribute("id") 
        searchParams.set(id, arg)
        const updated = searchParams.toString();
        updateURL = window.location.pathname + '?' + updated
        window.history.pushState({}, "", updateURL)
        index += 1;
    }

})

previous.addEventListener('click', ()=>{
    if (index >= 1){
        accounts[index].style.display = 'none'
        accounts[index-1].style.display = "block"
        arg = accounts[index-1].getAttribute("id")
        searchParams.set(id, arg)
        const updated = searchParams.toString();
        updateURL = window.location.pathname + '?' + updated
        window.history.pushState({}, "", updateURL)
        index -= 1;
    }
})

transaction.addEventListener('click', ()=>{
    if (updateURL === 0){
        updateURL = window.location.href
    }
    window.location.href = updateURL; 
})

cancel.addEventListener('click', ()=>{
    pop_up.style.display = 'none'
})

open.addEventListener('click', ()=>{
    pop_up.style.display = 'flex'
})