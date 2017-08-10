// Hide the files in the notebook directory view that are unimportant
$('#notebook_list').bind("DOMSubtreeModified", function(){
  [
    'Dockerfile',
    'README.md',
    'start-singleuser.sh',
    'start.sh',
    'requirements.txt',
    'src',
    'jupyter'
  ].forEach(function(s){
    $('.list_item:contains("' + s + '")').hide()
  })
});

$('#notebook_toolbar').clone().insertBefore('#notebook_toolbar').removeClass('list_toolbar').empty()
  .append(
      '<h2>Welcome to the Nightlight Exploratory</h2>' +
      '<p style="font-size: 14px; font-weight: bold;">Access and explore the data through the Jupyter notebooks in the notebooks folder. If this is your first time using jupyter notebooks and this package, then you should check out the <a href="/notebooks/notebooks/getting_started.ipynb">Getting Started</a> notebook.</p>'
      )

