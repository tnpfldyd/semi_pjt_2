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
        div.classList = "card mb-3 d-flex mb-3 p-0 btn-1"
        div.style = "max-width: 800px;"
        const div2 = document.createElement('div')
        div2.classList = 'row g-0'
        const div3 = document.createElement('div')
        div3.className = 'col-md-4'
        const img = document.createElement('img')
        img.src = resdata[i].image
        img.classList = "img-fluid rounded-start"
        img.style = "width: 210px; height: 200px;"
        const a = document.createElement('a')
        a.appendChild(img)
        a.href = resdata[i].link
        div3.appendChild(a)
        div2.appendChild(div3)
        const div4 = document.createElement('div')
        div4.className = 'col-md-8'
        const div5 = document.createElement('div')
        div5.className = 'card-body'
        const h5 = document.createElement('h5')
        h5.className = 'card-title'
        h5.innerText = resdata[i].title
        const p = document.createElement('p')
        p.classList = 'card-text text-danger'
        p.innerText = `${resdata[i].lprice} 원`
        const p2 = document.createElement('p')
        p2.innerText = `${resdata[i].mallName}`
        const p3 = document.createElement('p')
        p3.className = 'card-text'
        const a2 = document.createElement('a')
        a2.href = resdata[i].link
        a2.classList = 'text-light btn btn-secondary btn-sm'
        a2.innerText = '구매하러 가기'
        p3.appendChild(a2)
        div5.appendChild(h5)
        div5.appendChild(p)
        div5.appendChild(p2)
        div5.appendChild(p3)
        div4.appendChild(div5)
        div2.appendChild(div4)
        div.appendChild(div2)
        cardDiv.appendChild(div)
      }
    })
  })