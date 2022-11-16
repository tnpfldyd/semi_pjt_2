const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
function remove(event) {
  var delete_warning = confirm('쪽지를 삭제하시겠습니까?');
  if (delete_warning == true) {
    axios({
      method: 'post',
      url: `/notes/${event.target.value}/delete/`,
      headers: {'X-CSRFToken': csrftoken},
      data: {'note_pk': event.target.value}
    })
    .then(response => {
      const resdata = response.data.pk
      const div = document.getElementById(resdata)
      console.log(div)
      div.remove()
    })
  }
}