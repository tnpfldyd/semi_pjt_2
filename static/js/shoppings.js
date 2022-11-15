const select = document.querySelector('#select')
  select.addEventListener('change', function(event) {
    const target = event.target.value
    axios({
      method: 'get',
      url: `/shoppings/${target}/sort/`,
    })
    .then(response => {
      console.log(response.data.items)
      const cardDiv = document.querySelector('#card-div')
      removeAllchild(cardDiv)
      function removeAllchild(div) {
        while (div.hasChildNodes()) {
          div.removeChild(div.firstChild)
        }
      }
      const resdata = response.data.items
      for (let i = 0; i < resdata.length; i++) {
        const div = document.createElement('div')
        div.classList = "card col mx-xl-auto my-3 p-0"
        div.style = "width: 18rem;"
        const img = document.createElement('img')
        img.src = resdata[i].image
        img.className = "card-img-top"
        img.style = "width: 100%;"
        const divchild1 = document.createElement('div')
        divchild1.className = 'card-body'
        const h5 = document.createElement('h5')
        h5.className = 'card-title'
        h5.innerText = resdata[i].title
        divchild1.appendChild(h5)
        const divchild2 = document.createElement('div')
        divchild2.className = 'card-footer'
        const p = document.createElement('p')
        p.className = 'card-text'
        p.innerText = `가격 ${resdata[i].lprice} 원`
        const a = document.createElement('a')
        a.href = resdata[i].link
        a.classList = 'btn btn-primary'
        a.innerText = '구매하러 가기'
        divchild2.appendChild(p)
        divchild2.appendChild(a)
        div.appendChild(img)
        div.appendChild(divchild1)
        div.appendChild(divchild2)
        cardDiv.appendChild(div)
      }
    })
  })