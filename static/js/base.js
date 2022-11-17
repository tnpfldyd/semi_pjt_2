window.setTimeout(function() {
    $(".alert-auto-dismissible").fadeTo(500, 0).slideUp(500, function() {
        $(this).remove();
    });
}, 1500);
function apen(event) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  axios({
    method: 'post',
    url: '/accounts/notice/',
    headers: {'X-CSRFToken': csrftoken},
  })
  .then(response => {
    const items = response.data.items
    const dropul= document.querySelector("#dropul")
    removeAllchild(dropul)
    function removeAllchild(div) {
      while (div.hasChildNodes()) {
        div.removeChild(div.firstChild);
      }
    };
    for (let i=0; i<items.length; i++) {
      let time = moment(items[i][0]).add(9, 'hours').format('YYYY년 MM월 D일, a h:mm:ss');
      console.log(time)
      if (items[i][1][2] === 'card') {
        const li = document.createElement('li')
        const a = document.createElement('a')
        a.className='dropdown-item'
        a.href = `{% url 'cards:usercard_detail' 1 %}`
        a.href = a.href.replace('1', items[i][1][3])
        const p = document.createElement('p')
        const h6 = document.createElement('h6')
        h6.innerText = time
        p.innerText = `${items[i][1][1]} 님이 트리에 ${items[i][1][0]} 을 남겼어요.`
        a.appendChild(h6)
        a.appendChild(p)
        li.appendChild(a)
        dropul.appendChild(li)
      }
      else {
        const li = document.createElement('li')
        const a = document.createElement('a')
        a.className='dropdown-item'
        a.href = `{% url 'notes:detail' 1 %}`
        a.href = a.href.replace('1', items[i][1][3])
        const p = document.createElement('p')
        const h6 = document.createElement('h6')
        h6.innerText = time
        p.innerText = `${items[i][1][1]} 님이 ${items[i][1][0]} 쪽지를 보냈어요.`
        a.appendChild(h6)
        a.appendChild(p)
        li.appendChild(a)
        dropul.appendChild(li)
      }
    }
  })
}