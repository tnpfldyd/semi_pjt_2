function remove(event) {
  console.log(event.target.data.noteId)
  var delete_warning = confirm('쪽지를 삭제하시겠습니까?')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  if (delete_warning == true) {
    axios({
      method: 'post',
      url: `/notes/${event.target.data.noteId}/delete/`,
      headers: {'X-CSRFToken': csrftoken},
      data: {'note_pk': event.target.data.noteId},
    })
    .then(response => {
      const resdata = response.data.pk
      const div = document.getElementById(resdata)
      console.log(div)
      div.remove()
    })
  }
}