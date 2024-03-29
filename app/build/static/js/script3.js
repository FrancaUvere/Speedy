const accounts = document.getElementsByClassName('acc')
const next = document.querySelector('#next')
const previous = document.querySelector('#previous')
const amount = document.querySelector('#amount_in')
const am_err = document.querySelector('#err')
const acc_num = document.querySelector('#acc_no')
const no_err = document.querySelector('#no_err')

let index=0;
let i = 0;

let currentUrl = window.location.href
let searchParams = new URLSearchParams(window.location.search);

const id="id"
let arg;

next.addEventListener('click', ()=>{
    if (index < accounts.length){
        accounts[index+1].style.display = 'block'
        accounts[index].style.display = "none"
        amount.value = ""
        if (document.contains(am_err)){
            am_err.innerHTML = ""
        }
        arg = accounts[index+1].getAttribute("id") 
        searchParams.set(id, arg)
        const updated = searchParams.toString();
        const updateURL = window.location.pathname + '?' + updated
        window.history.pushState({}, "", updateURL)
        index += 1;
    }

})

previous.addEventListener('click', ()=>{
    if (index >= 1){
        accounts[index].style.display = 'none'
        accounts[index-1].style.display = "block"
        
        amount.value = ''
        if (document.contains(am_err)){
            am_err.innerHTML = ""
        }
        arg = accounts[index-1].getAttribute("id")
        searchParams.set(id, arg)
        const updated = searchParams.toString();
        const updateURL = window.location.pathname + '?' + updated
        window.history.pushState({}, "", updateURL)
        index -= 1;
    }
})



amount.addEventListener('input', (event)=>{
    let currentURL = window.location.href;
    let urlSearchParams = new URLSearchParams(currentURL.split('?')[1]);
    let id = parseInt(urlSearchParams.get('id'), 10);

    fetch(`http://127.0.0.1:5000/api/v1/accounts/${id}`)
    .then(res=>{
        return res.json();
    })
    .then(data=>{
        const acc = data[`${id}`]
        const acc_bal = acc['balance'] 
        const err = document.querySelector('#erro')
        if (Number(event.target.value) > acc_bal){
            event.target.style.color = 'red'
            err.innerText = 'This amount exceeds the amount in your account'
        }
        if (Number(event.target.value) <= acc_bal){
            err.innerText = ''
        }
    })

    if (Number(event.target.value) < 50){
        event.target.style.color = 'red';
    }
    else{
        event.target.style.color = 'black';
    }
})


